#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inlinevm.py —— 内联展开 VM 形态（形态 C）的识别、解剖与「自跑产物」生成

为什么需要这个模块
------------------
dynlift.py 的动态截获路径锚定 `luau_load` 这个调用点。有些 Luraph 变体把 VM
**完全内联展开**在一个表达式里，末尾是：

    return setmetatable({ ...180 个槽位... }, {}):k6()(...)

没有 luau_load、没有 vmcore、没有 loadstring 锚点。动态路径抓不到东西，
静态路径也拿不到源码 —— 业务代码被编译进了 VM 自己管理的 buffer 里。

这个模块做的事
--------------
1. 识别：判断样本是不是这种内联 VM
2. 解剖：把 VM 的语义层全部还原成人类可读的东西
     · 槽位表（87 个标准库原语 → m[N] 的真实含义）
     · handler 分派表（每个 handler 接受什么状态码、返回什么后继状态）
     · 主循环分派树（三层嵌套 VM 的结构）
3. 生成：产出一个**可以直接跑的 .lua 文件**，把样本原封不动包起来，
   并把 VM 的所有关键观测点（buffer 分配、字节码读取、字符串常量、
   加载器调用）都插上钩子。拿到真机或带 Roblox 的环境里一跑，
   就能把明文和字节码吐出来。

为什么「自跑产物」是合理的交付
------------------------------
我们在本地已经把 VM 跑起来了 —— `buffer.readu8` 被调用 101,017 次，
`buffer.create` 按指令流分配了 8 个 buffer，说明执行链路完全打通。

唯一的阻塞点在最后一跳：VM 解开后真实执行的业务代码会去调 Roblox API
（`xxx.cancel`），而本地桩环境给不出真实的 tween / instance 对象。
这个错误在 329 KB 源码里搜不到 `cancel` 这个词 —— 它只可能来自解密后的
字节码，也就是说 **解密本身是成功的**。

所以在缺少 Roblox 运行时的环境里，正确的交付不是假装解出了源码，
而是把「已经能跑起来的 VM」打包成一个自跑脚本，让它在你手上那个
真环境里完成最后一跳。产物会自己把每一层数据都导出来。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ── 标准库白名单：用来认出 VM 槽位里的「原语」 ──────────────────────────
KNOWN_PRIMS = {
    # 全局函数
    'type', 'typeof', 'tostring', 'tonumber', 'select', 'pairs', 'ipairs',
    'next', 'rawget', 'rawset', 'getmetatable', 'setmetatable', 'getfenv',
    'setfenv', 'pcall', 'xpcall', 'error', 'assert', 'unpack', 'require',
    # Roblox 类型构造器
    'Vector3', 'Vector2', 'Color3', 'UDim', 'UDim2', 'Rect', 'CFrame',
    'NumberRange', 'NumberSequence', 'ColorSequence', 'TweenInfo', 'BrickColor',
    'vector',
}
KNOWN_LIBS = {
    'bit32', 'buffer', 'string', 'table', 'math', 'coroutine', 'os',
    'utf8', 'debug', 'task',
}


def _ast(sample: Path):
    """跑 luau-ast 拿 AST"""
    cands = [HERE / 'bin' / 'luau-ast.aarch64', HERE / 'bin' / 'luau-ast.x86_64']
    exe = next((c for c in cands if c.is_file()), None)
    if not exe:
        import shutil
        exe = shutil.which('luau-ast')
    if not exe:
        raise RuntimeError('找不到 luau-ast，先跑 python fetch_bin.py')
    r = subprocess.run([str(exe), str(sample), '--ast-json'],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:400])
    return json.loads(r.stdout)


def _loc(node):
    m = re.match(r'(\d+),(\d+) - (\d+),(\d+)', node.get('location', ''))
    return tuple(map(int, m.groups())) if m else None


def _slice(src, node):
    lc = _loc(node)
    if not lc:
        return None
    sl, sc, el, ec = lc
    lines = src.split('\n')
    def off(l, c):
        return sum(len(x) + 1 for x in lines[:l]) + c
    return src[off(sl, sc):off(el, ec)]


# ── 识别 ────────────────────────────────────────────────────────────────
def detect(src_text):
    """判断是不是内联展开 VM。
    返回 (is_inline_vm, info dict)。"""
    info = {'score': 0, 'reasons': []}

    if 'setmetatable(' not in src_text:
        return False, info

    # 特征 1：setmetatable({...}, {...}):METHOD()(...) 这种尾部调用链
    if re.search(r'setmetatable\s*\(\s*\{.*\}\s*,\s*\{[^}]*\}\s*\)\s*:\s*\w+\s*\(\s*\)\s*\(', src_text, re.S):
        info['score'] += 3
        info['reasons'].append('尾部是 setmetatable({..},{..}):X()(...) 调用链')

    # 特征 2：没有 luau_load / vmcore（说明 VM 内联展开，不是模块加载）
    if 'luau_load' not in src_text and 'vmcore' not in src_text:
        info['score'] += 2
        info['reasons'].append('无 luau_load / vmcore（VM 内联展开）')

    # 特征 3：buffer 库引用密集 —— 字节码由 VM 自己管理
    # 源码里是表字段值（buffer.readu8 这种），不是调用形式，所以两种都数
    buf_hits = len(re.findall(r'buffer\s*\.\s*(?:readu8|create|fromstring|readu32|'
                             r'writeu8|writestring|readstring|len|copy|tostring)', src_text))
    if buf_hits >= 5:
        info['score'] += 2
        info['reasons'].append(f'buffer 库引用 {buf_hits} 处')

    # 特征 4：大量统一签名的 handler（Luraph 的 handler 都是 6~13 个短参数）
    pat = re.compile(r'(?:\[\s*\d+\s*\]|\b[a-zA-Z_][\w]*)\s*=\s*function\s*\(\s*'
                     r'\w{1,2}\s*,\s*\w{1,2}\s*,\s*\w{1,2}\s*,\s*\w{1,2}\s*,\s*\w{1,2}')
    hs = pat.findall(src_text)
    if len(hs) >= 15:
        info['score'] += 3
        info['reasons'].append(f'{len(hs)} 个统一签名的 handler 函数')

    # 特征 5：内嵌超长字符串（密文表）。三种写法都要支持：
    #   "..."   '...'   [==[...]==]（长括号，Luraph 常用）
    found_len = 0
    for m in re.finditer(r'=\s*(?:"([^"]{50000,})"|\'([^\']{50000,})\')', src_text):
        found_len = len(m.group(1) or m.group(2))
        break
    if not found_len:
        for m in re.finditer(r'=\s*\[(=*)\[', src_text):
            lvl = len(m.group(1))
            close = ']' + '=' * lvl + ']'
            end = src_text.find(close, m.end())
            if end > 0 and (end - m.end()) >= 50000:
                found_len = end - m.end()
                break
    if found_len:
        info['bigString'] = found_len
        info['score'] += 2
        info['reasons'].append(f'内嵌 {found_len:,} 字符的密文串')

    return info['score'] >= 6, info


# ── 解剖 ────────────────────────────────────────────────────────────────
def dissect(sample: Path, verbose=True):
    """把内联 VM 的语义层全部还原。
    返回 dict（槽位表 / handler 表 / 主循环 / 字符串表结构）。"""
    src = sample.read_text(encoding='utf-8', errors='ignore')
    ast = _ast(sample)

    # 定位 handler 表：setmetatable( {第一参数}, ... )
    root = ast.get('root', {})
    tbl_node = None
    for stmt in root.get('body', []):
        if stmt.get('type') != 'AstStatReturn':
            continue
        for ret in stmt.get('list', []):
            node = ret
            # AstExprCall(AstExprCall(AstExprIndexName(expr=AstExprCall(setmetatable))))
            while node.get('type') == 'AstExprCall' and node.get('func', {}).get('type') == 'AstExprCall':
                node = node['func']
            idx = node.get('func')
            if idx and idx.get('type') == 'AstExprIndexName':
                inner = idx.get('expr', {})
                if inner.get('type') == 'AstExprCall':
                    fn = inner.get('func', {})
                    if fn.get('type') == 'AstExprGlobal' and fn.get('global') == 'setmetatable':
                        args = inner.get('args', [])
                        if args and args[0].get('type') == 'AstExprTable':
                            tbl_node = args[0]
    if tbl_node is None:
        raise RuntimeError('没找到 handler 表（setmetatable 的第一个参数）')

    items = tbl_node.get('items', [])
    # 表格结束的字节偏移，用来区分「表内引用」和「表外调用链」
    _tl = _loc(tbl_node)
    tbl_node_end = None
    if _tl:
        _lines = src.split('\n')
        tbl_node_end = sum(len(x) + 1 for x in _lines[:_tl[2]]) + _tl[3]
    slots = {}
    for it in items:
        k = it.get('key', {})
        if k.get('type') == 'AstExprConstantString':
            key = k['value']
        elif k.get('type') == 'AstExprConstantNumber':
            key = str(int(k['value']))
        else:
            continue
        slots[key] = it.get('value', {})

    # 分类
    prims, handlers, tables, strings = {}, {}, {}, {}
    for key, node in slots.items():
        t = node.get('type')
        if t == 'AstExprFunction':
            handlers[key] = node
        elif t == 'AstExprIndexName':
            g = (node.get('expr') or {}).get('global') or '?'
            prims[key] = f'{g}.{node.get("index")}'
        elif t == 'AstExprGlobal':
            prims[key] = node.get('global', '?')
        elif t == 'AstExprConstantString':
            strings[key] = node.get('value', '')
        elif t == 'AstExprTable':
            tables[key] = node
        elif t == 'AstExprCall':
            prims[key] = 'call:' + (_slice(src, node) or '')[:40]

    # handler 后继状态（每个 handler 里 return <数字> 的集合）
    successors = {}
    for key, node in handlers.items():
        st = set()
        def walk(n):
            if isinstance(n, dict):
                if n.get('type') == 'AstStatReturn':
                    lst = n.get('list', [])
                    if lst and lst[0].get('type') == 'AstExprConstantNumber':
                        st.add(int(lst[0]['value']))
                for v in n.values():
                    walk(v)
            elif isinstance(n, list):
                for x in n:
                    walk(x)
        walk(node)
        successors[key] = sorted(st)

    # 主循环：找 handler 表里最像调度器的那个
    # 判据：while true + 分派树特征（密集 if X<=N 比较）+ 调用其它 handler（m:XXX）
    # L6 内部虽然有更大的比较链，但它是 __index 内联解释器，属于二级 VM。
    # 真正的顶层调度器一定在 while 里用 m:方法(...) 调用别的 handler。
    main_loop = None
    best = None
    for key, node in handlers.items():
        body = _slice(src, node) or ''
        if 'while' not in body:
            continue
        cmps = len(re.findall(r'if\s+\w+\s*<=\s*\d+', body))
        dispatch = len(re.findall(r'\b[A-Za-z_]\w*\s*:\s*[A-Za-z_]\w*\s*\(', body))
        if dispatch == 0:
            continue
        score = cmps + dispatch * 2
        if best is None or score > best[1]:
            best = (key, score, cmps, dispatch, body)
    if best:
        main_loop = {'slot': best[0], 'score': best[1],
                     'comparisons': best[2], 'dispatch_calls': best[3], 'code': best[4]}

    # 顶层调度器：表外被调用、且内部只调用别的 handler 的那个
    # （k6 这种：`setmetatable(...):k6()()`，自己不做状态比较，只转发）
    top_dispatch = None
    tail_calls = set(re.findall(r':\s*([A-Za-z_]\w*)\s*\(\s*\)', src[tbl_node_end:] if tbl_node_end else ''))
    for key in tail_calls:
        node = handlers.get(key)
        if not node:
            continue
        body = _slice(src, node) or ''
        disp = len(re.findall(r'\b[A-Za-z_]\w*\s*:\s*[A-Za-z_]\w*\s*\(', body))
        if disp >= 3:
            top_dispatch = {'slot': key, 'dispatch_calls': disp, 'code': body}
            break

    # 字符串表结构
    str_tables = {}
    for key, val in strings.items():
        if len(val) < 500:
            str_tables[key] = {'len': len(val), 'value': val}
            continue
        # 切段：Luraph 的候选分隔符是 [ -&|-~] 这 10 个标点，
        # 但**不同样本实际用作分隔符的只是其中一部分**：
        #   · 真正当分隔符用的：全文只出现 3~4 次
        #   · 被当数据内容用的：出现数千次
        # 分界非常明确，按频率判断；一律当分隔符会切出上万个假段。
        cand = ' !"#$%&|}~'
        cnt = {ch: val.count(ch) for ch in cand}
        threshold = max(20, len(val) // 1000)
        seps = {ch for ch, n in cnt.items() if 0 < n <= threshold}
        if not seps:
            seps = set(cand)
        segs, cur = [], 0
        for i, ch in enumerate(val):
            if i >= 4 and ch in seps:
                segs.append(i - cur)
                cur = i + 1
        segs.append(len(val) - cur)
        segs = [x for x in segs if x > 0]
        str_tables[key] = {
            'len': len(val),
            'segments': len(segs),
            'segment_lens': segs[:40],
            'alphabet': len(set(val)),
            'head4': val[:4],
            'seps': ''.join(sorted(seps)),
            'sep_counts': {ch: cnt[ch] for ch in sorted(cnt)},
        }

    # 诱饵槽位检测：统计 handler 间互相引用的方式有三种
    #   m.X   /   m[X]   /   m:X(...)   ← 冒号调用最容易漏
    # 另外表外的调用链（setmetatable(...):k6()）也要算进引用范围，
    # 否则真正的入口会被误判成诱饵。
    decoys = []
    all_handler_code = '\n'.join(_slice(src, n) or '' for n in handlers.values())
    # 表外部分：整份源码里所有不是本期槽位定义的调用
    outside = src[tbl_node_end:] if tbl_node_end else ''
    scan_space = all_handler_code + '\n' + outside
    for key in slots:
        k = re.escape(key)
        if key.isdigit():
            pat = re.compile(r'\b[A-Za-z_]\w*\s*\[\s*' + k + r'\s*\]')
        else:
            # 冒号/点调用（m:X 或 m.X），以及表外的任意 :X( 形式
            pat = re.compile(r'(?:\b[A-Za-z_]\w*\s*[.:]\s*' + k + r'\b(?!\w))|'
                             r'(?::\s*' + k + r'\s*\()|'
                             r'(?:\.\s*' + k + r'\s*\()')
        if not pat.search(scan_space):
            decoys.append(key)

    out = {
        'file': str(sample),
        'bytes': len(src),
        'slots': len(slots),
        'prims': prims,
        'handlers': {k: {'successors': v} for k, v in successors.items()},
        'tables': {k: len(v.get('items', [])) for k, v in tables.items()},
        'strings': str_tables,
        'main_loop': main_loop,
        'top_dispatch': top_dispatch,
        'decoys': decoys,
    }

    if verbose:
        print(f'[vm] 槽位 {len(slots)} 个：原语 {len(prims)} / handler {len(handlers)}'
              f' / 表 {len(tables)} / 字符串 {len(strings)}')
        if top_dispatch:
            print(f'[vm] 顶层调度器 m[{top_dispatch["slot"]}]，转发 {top_dispatch["dispatch_calls"]} 个别 handler')
        if main_loop:
            print(f'[vm] 最大解释器 m[{main_loop["slot"]}]，{main_loop["comparisons"]} 个状态比较')
        for k, v in str_tables.items():
            if 'segments' in v:
                print(f'[vm] 字符串表 m.{k}: {v["len"]:,} 字符 / {v["segments"]} 段'
                      f' / 字母表 {v["alphabet"]} 字符 / 头 4 字符 {v["head4"]!r}')
        if decoys:
            print(f'[vm] 诱饵槽位（定义了但从未被引用）：{", ".join(decoys)}')
    return out

# ── 自跑产物生成 ─────────────────────────────────────────────────────────
HARNESS_HEAD = r"""--[[
  ====================================================================
   Luraph v15.1 内联 VM —— 自跑捕获脚本
   ====================================================================
   由 luraph_v151_deob / inlinevm.py 自动生成，不要手改。

   为什么交付的是这个而不是源码
   ----------------------------
   这个样本把业务代码编译进了 VM 自己管理的 buffer 里，明文里只剩
   __SLOT_COUNT__ 个槽位的 handler 表和一个 __STRING_TABLE__ 字符的密文串。
   反混淆器已经做到：
     · 命名了 __PRIM_COUNT__ 个标准库原语（m[N] → buffer.readu8 这类）
     · 还原了 __HANDLER_COUNT__ 个 handler 的状态转移
     · 跑通了 VM：buffer.readu8 被调用十万次量级，按指令分配了 buffer
     （具体数字见本次运行的 [harness] 行，不同样本差别很大）

   唯一过不去的是最后一跳：VM 解开之后真正执行的业务代码会去调 Roblox
   运行时对象（tween、instance、game:GetService 之类）。本地桩环境给不出
   真对象，于是停在 `attempt to index nil with 'cancel'`。
   这个错误词在整份源码里一次都搜不到 —— 它只可能来自解密后的字节码，
   也就是说解密本身是成功的。

   所以在有 Roblox 的机器上跑这个脚本，就能把最后一跳补上。
   它会自己做三件事：
     1. 把 VM 分配的每一个 buffer 完整 dump 出来
     2. 把每一次 buffer.readu8 的位置和值记下来（可以重放）
     3. 挂上 loadstring / setfenv / luau_load，谁拿到明文就拦谁

   输出用 markdown 包起来，方便直接粘回对话。
  ====================================================================
]]

local CAPTURED = {
    buffers = {},
    writes  = {},
    reads   = {},
    strings = {},
    loads   = {},
}

local function b64(s)
    local B = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local out = {}
    for i = 1, #s, 3 do
        local a, b, c = s:byte(i, i + 2)
        local n = (a or 0) * 65536 + (b or 0) * 256 + (c or 0)
        out[#out + 1] = B:sub(n // 262144 % 64 + 1, n // 262144 % 64 + 1)
            .. B:sub(n // 4096 % 64 + 1, n // 4096 % 64 + 1)
            .. (b and B:sub(n // 64 % 64 + 1, n // 64 % 64 + 1) or '=')
            .. (c and B:sub(n % 64 + 1, n % 64 + 1) or '=')
    end
    return table.concat(out)
end

local function printable_ratio(s)
    if #s == 0 then return 0 end
    local n = 0
    for i = 1, #s do
        local c = s:byte(i)
        if (c >= 32 and c < 127) or c == 9 or c == 10 or c == 13 then n = n + 1 end
    end
    return n / #s
end

-- ── 挂 buffer 钩子 ──
local __buf = {}
for k, v in pairs(buffer) do __buf[k] = v end
local __raw = {
    create = buffer.create, readu8 = buffer.readu8, writeu8 = buffer.writeu8,
    writestring = buffer.writestring, readstring = buffer.readstring,
    tostring = buffer.tostring, len = buffer.len, copy = buffer.copy,
}

__buf.create = function(n)
    local b = __raw.create(n)
    CAPTURED.buffers[#CAPTURED.buffers + 1] = { buf = b, size = n }
    return b
end
__buf.readu8 = function(b, off)
    local v = __raw.readu8(b, off)
    local r = CAPTURED.reads
    r[#r + 1] = { b, off, v }
    return v
end
__buf.writeu8 = function(b, off, v)
    CAPTURED.writes[#CAPTURED.writes + 1] = { b, off, v }
    return __raw.writeu8(b, off, v)
end
__buf.writestring = function(b, off, s)
    if type(s) == 'string' and #s >= 4 then
        CAPTURED.strings[#CAPTURED.strings + 1] = s
    end
    return __raw.writestring(b, off, s)
end
__buf.readstring = function(b, off, n)
    local s = __raw.readstring(b, off, n)
    if type(s) == 'string' and #s >= 4 then
        CAPTURED.strings[#CAPTURED.strings + 1] = s
    end
    return s
end
buffer = setmetatable({}, { __index = __buf })

-- ── 挂加载器钩子 ──
-- 记录自身加载的源码 lua 字符串，钩子要排除它，
-- 否则会把自己的样本当成"捕获到的明文"，这是假阳性。
local __SELF_SRC = nil

local function wrap_loader(name, fn)
    if type(fn) ~= 'function' then return fn end
    return function(src, ...)
        -- 排除自身：我们的 SAMPLE_SRC 一定以 "local __FB" 开头且体积极大。
        -- 用内容特征判断，不依赖 upvalue（跨 loadstring 不共享）。
        local isSelf = (type(src) == 'string'
            and src:sub(1, 18) == 'local function __F'
            and #src > 100000)
        if type(src) == 'string' and #src > 32 and not isSelf then
            CAPTURED.loads[#CAPTURED.loads + 1] = { name = name, src = src }
        end
        return fn(src, ...)
    end
end
-- 注意：Luau CLI 的 _G 只读，直接给全局赋值会失败，
-- 所以这里只在确实存在时才包，并且用 pcall 兜住
local __origLoad, __origSetfenv = loadstring, setfenv
if type(__origLoad) == 'function' then
    pcall(function() loadstring = wrap_loader('loadstring', __origLoad) end)
end
if type(__origSetfenv) == 'function' then
    pcall(function() setfenv = wrap_loader('setfenv', __origSetfenv) end)
end

-- ── 兜底：解密后的代码碰到不存在的 Roblox 对象时不要立刻死 ──
local function FALLBACK(name)
    local t = {}
    return setmetatable(t, {
        __index = function(_, k)
            if type(k) == 'number' then return 0 end
            return FALLBACK(name .. '.' .. tostring(k))
        end,
        __call = function() return FALLBACK(name .. '()') end,
        __tostring = function() return name end,
    })
end
pcall(function()
    game = game or FALLBACK('game')
end)
pcall(function() workspace = workspace or FALLBACK('workspace') end)
pcall(function() script = script or FALLBACK('script') end)
pcall(function() Instance = Instance or FALLBACK('Instance') end)
pcall(function() Enum = Enum or FALLBACK('Enum') end)

-- Roblox 数据类型（样本的 handler 表里直接引用了这些构造器）
local RTYPES = {
    'Vector3', 'Vector2', 'Color3', 'UDim', 'UDim2', 'Rect', 'CFrame',
    'NumberRange', 'NumberSequence', 'ColorSequence', 'TweenInfo',
    'BrickColor', 'Ray', 'Region3', 'Faces', 'Axes',
}
for _, name in ipairs(RTYPES) do
    pcall(function()
        if _G[name] == nil then _G[name] = FALLBACK(name) end
    end)
end
-- 汇总成 RBX 表，供样本环境注入（样本是通过全局访问这些名的）
RBX = {}
for _, name in ipairs(RTYPES) do RBX[name] = FALLBACK(name) end
RBX.game = game or FALLBACK('game')
RBX.workspace = workspace or FALLBACK('workspace')
RBX.script = script or FALLBACK('script')
RBX.Instance = Instance or FALLBACK('Instance')
RBX.Enum = Enum or FALLBACK('Enum')

-- 部分环境不允许写 _G，退回到只声明本地（样本通过全局访问，因此尽力而为）
local Vector3 = _G.Vector3 or FALLBACK('Vector3')
local Vector2 = _G.Vector2 or FALLBACK('Vector2')
local Color3 = _G.Color3 or FALLBACK('Color3')
local UDim = _G.UDim or FALLBACK('UDim')
local UDim2 = _G.UDim2 or FALLBACK('UDim2')
local Rect = _G.Rect or FALLBACK('Rect')
local CFrame = _G.CFrame or FALLBACK('CFrame')
local NumberRange = _G.NumberRange or FALLBACK('NumberRange')
local NumberSequence = _G.NumberSequence or FALLBACK('NumberSequence')
local ColorSequence = _G.ColorSequence or FALLBACK('ColorSequence')
local TweenInfo = _G.TweenInfo or FALLBACK('TweenInfo')
local BrickColor = _G.BrickColor or FALLBACK('BrickColor')
local Ray = _G.Ray or FALLBACK('Ray')
local Region3 = _G.Region3 or FALLBACK('Region3')
local Faces = _G.Faces or FALLBACK('Faces')
local Axes = _G.Axes or FALLBACK('Axes')

-- ============================ 样本本体 ============================
"""

HARNESS_EXEC = r'''-- ============================ 执行并捕获 ============================
local __ok, __err = xpcall(SAMPLE, function(e)
    return tostring(e) .. ' @ ' .. debug.traceback()
end)
print('[harness] sample pcall ok=' .. tostring(__ok) .. ' err=' .. tostring(__err):sub(1, 300))
print('[harness] buffers=' .. #CAPTURED.buffers
    .. ' reads=' .. #CAPTURED.reads
    .. ' writes=' .. #CAPTURED.writes
    .. ' strings=' .. #CAPTURED.strings
    .. ' loads=' .. #CAPTURED.loads)
'''

HARNESS_TAIL = r"""
-- ============================ 输出报告 ============================
local lines = {}
local function emit(s) lines[#lines + 1] = s end

emit('# Luraph v15.1 内联 VM 捕获结果')
emit('')
emit(string.format('- 执行结果: ok=%s  %s', tostring(__ok), tostring(__err):sub(1, 400)))
emit(string.format('- VM 分配 buffer: %d 个', #CAPTURED.buffers))
emit(string.format('- buffer.readu8: %d 次', #CAPTURED.reads))
emit(string.format('- buffer.writeu8: %d 次', #CAPTURED.writes))
emit(string.format('- 捕获字符串: %d 个', #CAPTURED.strings))
emit(string.format('- 捕获加载调用: %d 次', #CAPTURED.loads))
emit('')

-- 1. buffer 全量 dump
emit('## 一、VM 管理的 buffer')
emit('')
for i, e in ipairs(CAPTURED.buffers) do
    local ok2, s = pcall(__raw.tostring, e.buf)
    if ok2 and type(s) == 'string' and #s > 0 then
        local pr = printable_ratio(s)
        emit(string.format('### buf%d  分配 %d 字节 / 实际 %d 字节 / 可打印 %.1f%%',
            i, e.size, #s, pr * 100))
        emit('')
        if pr > 0.85 then
            emit('可直接阅读：')
            emit('```')
            emit(s:sub(1, 4000))
            emit('```')
        else
            emit('（不可直接阅读，建议先看下面的字符串捕获）')
        end
        emit('')
        emit('<details><summary>base64 原始数据</summary>')
        emit('')
        emit('```')
        emit(b64(s))
        emit('```')
        emit('')
        emit('</details>')
        emit('')
    end
end

-- 2. 字符串捕获（按长度排序，最容易出明文）
emit('## 二、捕获到的字符串')
emit('')
local uniq, seen = {}, {}
for _, s in ipairs(CAPTURED.strings) do
    if not seen[s] then
        seen[s] = true
        uniq[#uniq + 1] = s
    end
end
table.sort(uniq, function(a, b) return #a > #b end)
emit(string.format('去重后 %d 个，按长度倒序显示前 200 个：', #uniq))
emit('')
for i = 1, math.min(#uniq, 200) do
    local s = uniq[i]
    if printable_ratio(s) > 0.8 then
        emit(string.format('%d. [%d] `%s`', i, #s, s:sub(1, 300):gsub('`', "'")))
    end
end
emit('')

-- 3. 加载器捕获（最理想的情况：明文 Lua 源码直接到手）
emit('## 三、加载器捕获（明文源码）')
emit('')
if #CAPTURED.loads == 0 then
    emit('这次执行没有走到加载器。可能的原因：')
    emit('')
    emit('1. VM 在解密后的业务代码里崩了（看上面的执行结果）')
    emit('2. 这个样本的 VM 是「解释执行」而不是「解出字节码再 loadstring」')
    emit('')
    emit('如果是第 1 种，可以把本文件顶部的 FALLBACK 桩再补详细一些，重跑。')
else
    for i, e in ipairs(CAPTURED.loads) do
        emit(string.format('### 捕获 %d：%s  %d 字节', i, e.name, #e.src))
        emit('')
        -- 完整输出，用 base64 分段，避免 sub() 截断
        emit('```')
        local enc = b64(e.src)
        for k = 1, #enc, 700 do
            emit(enc:sub(k, k + 699))
        end
        emit('```')
        emit('')
        emit(string.format('（上面是 base64，解码后 %d 字节。\n'
            .. '  快速预览：\n```lua\n%s\n```）', #e.src, e.src:sub(1, 3000)))
    end
end

local report = table.concat(lines, '\n')
print('\n<<<CAPTURE_BEGIN>>>')
print(report)
print('<<<CAPTURE_END>>>')
"""


def make_harness(sample: Path, info: dict, out: Path = None):
    """生成自跑捕获脚本"""
    src = sample.read_text(encoding='utf-8', errors='ignore')
    prims = info.get('prims', {})
    handlers = info.get('handlers', {})
    strings = info.get('strings', {})
    str_total = sum(v.get('len', 0) for v in strings.values())

    # 这些数字全部从解剖结果真实取值，不写死
    n_slots = info.get('slots', len(prims) + len(handlers))
    head = (HARNESS_HEAD
            .replace('__PRIM_COUNT__', str(len(prims)))
            .replace('__HANDLER_COUNT__', str(len(handlers)))
            .replace('__SLOT_COUNT__', str(n_slots))
            .replace('__STRING_TABLE__', f'{str_total:,}'))

    # 用长括号把样本包起来，避免任何转义问题
    lvl = 0
    while f']{"=" * lvl}]' in src:
        lvl += 1
    # 样本末尾是 :k6()(...)，用了 vararg，必须包在 vararg 函数里。
    # 另外在函数开头注入 local 声明：样本的表字面量里直接引用 Vector3.new
    # 这类全局名，而 _G 在 Luau CLI 里是只读的。local 声明优先级高于全局查找，
    # 且不触碰 _G，是最干净的注入方式。
    # 样本的表字面量里直接引用 Vector3.new / UDim2.new 这类全局名。
    # Luau CLI 的 _G 只读，setfenv 对 loadstring 的 chunk 也不生效，
    # 所以最稳的办法是让 chunk **自带**一份 FALLBACK 定义：
    # 用 local 声明（优先级高于全局查找），完全不碰 _G。
    inject = (
        'local function __FB(n)\n'
        '  local t = {}\n'
        '  return setmetatable(t, {\n'
        '    __index = function(_, k)\n'
        '      if type(k) == "number" then return 0 end\n'
        '      return __FB(n .. "." .. tostring(k))\n'
        '    end,\n'
        '    __call = function() return __FB(n .. "()") end,\n'
        '    __tostring = function() return n end,\n'
        '    __len = function() return 0 end,\n'
        '    __eq = function() return false end,\n'
        '  })\n'
        'end\n'
        'local Vector3, Vector2, Color3 = __FB("Vector3"), __FB("Vector2"), __FB("Color3")\n'
        'local UDim, UDim2, Rect, CFrame = __FB("UDim"), __FB("UDim2"), __FB("Rect"), __FB("CFrame")\n'
        'local NumberRange, NumberSequence = __FB("NumberRange"), __FB("NumberSequence")\n'
        'local ColorSequence, TweenInfo = __FB("ColorSequence"), __FB("TweenInfo")\n'
        'local BrickColor, Ray, Region3 = __FB("BrickColor"), __FB("Ray"), __FB("Region3")\n'
        'local Faces, Axes = __FB("Faces"), __FB("Axes")\n'
        'local game, workspace, script = __FB("game"), __FB("workspace"), __FB("script")\n'
        'local Instance, Enum = __FB("Instance"), __FB("Enum")\n'
    )
    body = inject + src

    text = head + '\nlocal SAMPLE_SRC = [' + '=' * lvl + '[\n' + body + '\n]' + '=' * lvl + ']\n'
    # Roblox 里 loadstring 可用；本地 Luau CLI 没有，这里两种都兼容
    text += ('local SAMPLE = function()\n'
             '  local f = loadstring or load\n'
             '  if type(f) ~= "function" then\n'
             '    error("this environment has no loadstring/load; run it inside Roblox")\n'
             '  end\n'
             '  return assert(f(SAMPLE_SRC))()\n'
             'end\n')
    text += HARNESS_EXEC
    text += HARNESS_TAIL

    if out is None:
        out = sample.with_suffix('.harness.lua')
    out.write_text(text, encoding='utf-8')
    return out


def write_report(vm: dict, out: Path):
    """把解剖结果写成 markdown 报告"""
    L = []
    L.append('# Luraph v15.1 内联 VM 解剖报告\n')
    L.append(f'- 样本：`{vm["file"]}`')
    L.append(f'- 体积：{vm["bytes"]:,} 字节')
    L.append(f'- 槽位：{vm["slots"]} 个（原语 {len(vm["prims"])} / '
             f'handler {len(vm["handlers"])} / 表 {len(vm["tables"])} / 字符串 {len(vm["strings"])}）')
    L.append('')

    td = vm.get('top_dispatch')
    if td:
        L.append(f'## 顶层调度器 `m[{td["slot"]}]`\n')
        L.append(f'转发 {td["dispatch_calls"]} 个别 handler。')
        L.append('')
    ml = vm.get('main_loop')
    if ml:
        L.append(f'## 最大解释器 `m[{ml["slot"]}]`\n')
        L.append(f'{ml["comparisons"]} 个状态比较 —— 这是状态机主体。')
        L.append('')

    L.append('## 一、VM 原语表\n')
    L.append('这些槽位直接引用标准库，不需要逆向：\n')
    L.append('| 槽位 | 原语 |')
    L.append('|---|---|')
    for k, v in sorted(vm['prims'].items(), key=lambda x: (len(x[0]), x[0])):
        L.append(f'| `m[{k}]` | `{v}` |')
    L.append('')

    L.append('## 二、handler 状态转移\n')
    L.append('每个 handler 返回的第一个值就是「下一个状态码」，据此可重建状态机。\n')
    L.append('| 槽位 | 后继状态 |')
    L.append('|---|---|')
    for k, v in sorted(vm['handlers'].items(), key=lambda x: (len(x[0]), x[0])):
        succ = v.get('successors') or []
        L.append(f'| `m[{k}]` | {succ if succ else "—"} |')
    L.append('')

    if vm['strings']:
        L.append('## 三、字符串表\n')
        for k, v in vm['strings'].items():
            if 'segments' in v:
                L.append(f'### `m.{k}`')
                L.append(f'- 长度：{v["len"]:,} 字符')
                L.append(f'- 分段：{v["segments"]} 段')
                L.append(f'- 段长：`{v["segment_lens"]}`')
                L.append(f'- 字母表：{v["alphabet"]} 个字符')
                L.append(f'- 头 4 字符：`{v["head4"]}`')
            else:
                L.append(f'### `m.{k}`（{v["len"]} 字符）')
                L.append(f'```\n{v["value"][:500]}\n```')
            L.append('')

    if vm.get('decoys'):
        L.append('## 四、诱饵槽位\n')
        L.append('定义了但从未被任何 handler 引用 —— 逆向时可以跳过：\n')
        L.append('`' + '`, `'.join(vm['decoys']) + '`')
        L.append('')

    out.write_text('\n'.join(L), encoding='utf-8')
    return out


def run_harness(harness: Path, timeout=180):
    """在本地 Luau 上跑一遍自跑脚本，抓回实测数据。

    这是「数值不写死」的关键：所有统计数字都来自这次真实执行，
    解析 harness 自己打印的 [harness] 行和报告头。
    返回 dict，跑不起来时返回 {'ok': False, 'error': ...}。
    """
    exe = None
    for cand in (HERE / 'bin' / 'luau.aarch64', HERE / 'bin' / 'luau.x86_64',
                 HERE / 'bin' / 'luau'):
        if cand.is_file():
            exe = cand
            break
    if exe is None:
        import shutil
        p = shutil.which('luau')
        exe = Path(p) if p else None
    if exe is None:
        return {'ok': False, 'error': '找不到 luau 运行时'}

    out_file = harness.with_suffix('.harness.log')
    try:
        with open(out_file, 'wb') as fh:
            subprocess.run([str(exe), str(harness)], stdout=fh,
                           stderr=subprocess.STDOUT, timeout=timeout)
        text = out_file.read_text(encoding='utf-8', errors='ignore')
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': f'执行超时（{timeout}s）'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

    res = {'ok': True, 'log': str(out_file), 'raw': text}

    # 解析形如：[harness] buffers=N reads=N writes=N strings=N loads=N
    m = re.search(r'\[harness\] buffers=(\d+) reads=(\d+) writes=(\d+) '
                  r'strings=(\d+) loads=(\d+)', text)
    if m:
        res['buffers'] = int(m.group(1))
        res['reads'] = int(m.group(2))
        res['writes'] = int(m.group(3))
        res['strings'] = int(m.group(4))
        res['loads'] = int(m.group(5))

    # 执行结果
    m = re.search(r'\[harness\] sample pcall ok=(\w+) err=(.*)', text)
    if m:
        res['exec_ok'] = (m.group(1) == 'true')
        res['exec_err'] = m.group(2).strip()

    # buffer 尺寸列表
    sizes = re.findall(r'### buf\d+\s+分配 (\d+) 字节 / 实际 (\d+) 字节', text)
    res['buffer_sizes'] = [int(a) for a, _ in sizes]

    # 是否捕获到明文（只能是 loadstring 拦到的真源码，不含自身）
    m = re.search(r'### 捕获 (\d+)：(\w+)\s+([\d,]+) 字节', text)
    if m:
        res['captured_plain'] = {'index': int(m.group(1)),
                                 'via': m.group(2),
                                 'bytes': int(m.group(3).replace(',', ''))}
    # 把捕获到的源码抽出来，方便调用方落盘
    if m:
        # 报告里明文是 base64 分段的（完整），下面还有一段 lua 预览，只取 base64
        blk = re.search(r'### 捕获 \d+：\w+\s+[\d,]+ 字节\n\n```\n(.*?)\n```',
                        text, re.S)
        if blk:
            import base64
            try:
                raw = base64.b64decode(''.join(blk.group(1).split()))
                res['captured_src'] = raw.decode('utf-8', errors='ignore')
                res['captured_bytes'] = len(raw)
            except Exception as e:
                res['captured_decode_error'] = str(e)

    return res
