#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trace_vm.py —— 对「VM 内联展开」的 Luraph 样本做执行轨迹追踪

适用场景（这是第三种形态）：
    - 业务代码编译进 VM 指令
    - 没有 luau_load / loadstring / vmcore 可 hook
    - 只有一个或多个 `while true do local D=F[b]; if D<61 then ...` 分派循环

做法：
    在分派点注入记录代码，把 (opcode, 操作数) 序列打出来。
    配合桩环境跑起来，得到指令流；再按 opcode 归类统计，
    能还原出「这个脚本到底调用了哪些 API、有哪些功能」。

局限（必须说清楚）：
    只有实际执行到的分支才有记录。没走到的代码看不到。

用法:
    python trace_vm.py <样本.lua> [--max-ops 20000] [--out 轨迹.txt]
"""
import re
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 分派点：local D=F[b];if D<61 —— 变量名和比较值都可能变
DISPATCH_RE = re.compile(
    r'local\s+(\w+)\s*=\s*(\w+)\s*\[\s*(\w+)\s*\]\s*;\s*if\s+\1\s*[<>]=?\s*\d+')


def find_dispatchers(src):
    return [(m.start(), m.group(1), m.group(2), m.group(3))
            for m in DISPATCH_RE.finditer(src)]


def build_hook(var, table, index, limit):
    """在分派点的 if 之前插入记录"""
    return (f'if _TRACE_N and _TRACE_N<{limit} then _TRACE_N=_TRACE_N+1 '
            f'print("@@OP@@"..tostring({var}).."|"..tostring({index})) end ')


def inject(src, limit=20000):
    """在所有分派点注入记录代码，返回 (新源码, 注入点数量)"""
    ds = find_dispatchers(src)
    if not ds:
        return None, 0
    # 从后往前插，避免偏移变化
    out = src
    for pos, var, table, index in reversed(ds):
        hook = build_hook(var, table, index, limit)
        out = out[:pos] + hook + out[pos:]
    return out, len(ds)


STUB_HEADER = '''
-- 执行轨迹追踪用的桩头：把 Roblox 全局都变成「什么都能做」的对象
local _TRACE_N = 0
local function mk(name)
    local t = {}
    return setmetatable(t, {
        __index = function(_, k)
            if type(k) == 'number' then
                return 0
            end
            return mk(name .. '.' .. tostring(k))
        end,
        __newindex = function() end,
        __call = function(...) return mk(name .. '()') end,
        __tostring = function() return name end,
        __concat = function(a, b) return tostring(a) .. tostring(b) end,
        __add = function() return 0 end, __sub = function() return 0 end,
        __mul = function() return 0 end, __div = function() return 0 end,
        __mod = function() return 0 end, __pow = function() return 0 end,
        __unm = function() return 0 end,
        __lt = function() return false end, __le = function() return false end,
        __eq = function() return false end,
        __len = function() return 0 end,
    })
end

local _env = setmetatable({
    -- 追踪输出靠它，必须是真的 print
    print = print,
}, {
    __index = function(_, k)
        if k == 'game' or k == 'workspace' or k == 'script' then
            return mk(tostring(k))
        end
        if k == 'typeof' then return function(v) return type(v) end end
        if k == 'Vector3' or k == 'Vector2' or k == 'CFrame'
           or k == 'Color3' or k == 'UDim2' or k == 'UDim'
           or k == 'Rect' or k == 'NumberSequence' or k == 'ColorSequence' then
            return mk(tostring(k))
        end
        if k == 'Enum' then return mk('Enum') end
        if k == 'loadstring' or k == 'load' then
            return function() return function() end end
        end
        if k == 'getgenv' or k == 'getfenv' then return function() return _env end end
        if k == 'setfenv' then return function() end end
        if k == 'pcall' or k == 'xpcall' then
            return function(f, ...) if type(f) == 'function' then
                local ok, e = pcall(f, ...) return ok, e end return false end
        end
        if k == 'task' then return { wait = function() end, spawn = function(f) if type(f)=='function' then pcall(f) end end,
            delay = function(_, f) if type(f)=='function' then pcall(f) end end,
            defer = function(f) if type(f)=='function' then pcall(f) end end } end
        if k == 'tick' or k == 'time' or k == 'os' then
            return mk(tostring(k))
        end
        -- 不能屏蔽 print：追踪记录就靠它。只屏蔽 warn（噪音大）。
        if k == 'warn' then return function() end end
        if k == 'string' or k == 'table' or k == 'math' or k == 'bit32'
           or k == 'buffer' or k == 'coroutine' or k == 'utf8' then
            return _G[k]
        end
        return mk(tostring(k))
    end,
    __newindex = function() end,
})
'''


def run_trace(sample, limit=20000):
    """注入并运行，返回轨迹行"""
    luau = None
    for c in (HERE / 'bin' / 'luau.aarch64', HERE / 'bin' / 'luau.x86_64',
              HERE / 'bin' / 'luau'):
        if c.is_file():
            luau = c
            break
    if luau is None:
        luau = shutil.which('luau')
    if not luau:
        print("[✗] 找不到 luau 运行时")
        return None

    src = Path(sample).read_text(encoding='utf-8', errors='ignore')
    injected, n = inject(src, limit)
    if injected is None:
        print("[✗] 找不到 VM 分派点（local X=Y[Z];if X<64 这种模式）")
        return None
    print(f"[trace] 在 {n} 处 VM 分派点注入记录代码")

    td = Path(tempfile.mkdtemp(prefix='tracevm_'))
    f = td / 'traced.lua'
    # 桩头 + 样本（样本用 setfenv 切环境）
    # 不要包进 function()...end —— 样本里有顶层 `...`（vararg），
    # 包起来会报 "Cannot use '...' outside of a vararg function"。
    # 直接把样本放在桩头之后，用 pcall 包住即可。
    # 关键：样本必须跑在桩环境里，否则它访问的 Rect/UDim 等
    # 在 Luau CLI 里是 nil，VM 一启动就崩。
    # 做法：stub 头 + 用 load 把样本编译成函数，再 setfenv 到 _env。
    # Luau 的 load(chunk, name, mode, env) 直接接受 env，
    # 没有 setfenv（那是 Lua 5.1 API）。用 load 的第四参数切环境。
    body = STUB_HEADER + '\nlocal _src = [===[\n' + injected + '\n]===]\n'
    # Luau CLI: load 是 nil，loadstring + setfenv 可用（Lua 5.1 风格）。
    # 两个都试一遍，兼容不同运行时。
    body += ('local _ld = loadstring or load\n'
             'local _fn = _ld and _ld(_src, "traced")\n'
             'if not _fn then print("@@LOADFAIL 无 loadstring/load") return end\n'
             'if setfenv then pcall(setfenv, _fn, _env) end\n'
             'local ok, err = pcall(_fn)\n'
             'if not ok then print("@@ERR " .. tostring(err)) end\n')
    f.write_text(body, encoding='utf-8')

    try:
        r = subprocess.run([str(luau), str(f)], capture_output=True,
                           text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("[✗] 超时")
        return None

    out = (r.stdout or '') + '\n' + (r.stderr or '')
    ops = re.findall(r'@@OP@@(\d+)\|(\d+)', out)
    if not ops:
        tail = out.strip().split('\n')[0][:150] if out.strip() else '(无输出)'
        print(f"[✗] 没抓到指令：{tail}")
        return None
    print(f"[trace] 记录 {len(ops):,} 条指令执行")
    return ops


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    limit = 20000
    for i, a in enumerate(sys.argv):
        if a == '--max-ops' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    if not args:
        print(__doc__)
        return 1

    ops = run_trace(args[0], limit)
    if not ops:
        return 1

    from collections import Counter
    c = Counter(op for op, _ in ops)
    print(f"\n[trace] opcode 分布（共 {len(c)} 种）：")
    for op, cnt in c.most_common(20):
        print(f"    opcode {op:>4}: {cnt:>7,} 次")

    if len(args) > 1:
        Path(args[1]).write_text(
            '\n'.join(f"{o}\t{i}" for o, i in ops), encoding='utf-8')
        print(f"\n[trace] 轨迹已写出 → {args[1]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
