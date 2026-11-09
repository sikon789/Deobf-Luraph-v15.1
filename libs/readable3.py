#!/usr/bin/env python3
"""Lua/Luau 语义重命名：单遍作用域解析（支持同名重复声明）+ 按初始化表达式推导名字。"""
import sys
from beautify2 import tokenize, build_tokens

RESERVED = {
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for', 'function',
    'goto', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat', 'return',
    'then', 'true', 'until', 'while', 'continue', 'self',
}

BAD_BASE = RESERVED | {
    'game', 'workspace', 'script', 'shared', 'plugin', '_G', 'print', 'warn',
    'error', 'type', 'typeof', 'pairs', 'ipairs', 'next', 'select', 'pcall',
    'xpcall', 'setmetatable', 'getmetatable', 'rawget', 'rawset', 'tostring',
    'tonumber', 'table', 'string', 'math', 'os', 'task', 'buffer', 'bit32',
    'utf8', 'coroutine', 'debug', 'loadstring', 'load', 'require', 'setfenv',
    'getfenv', 'Enum', 'Instance', 'Color3', 'UDim2', 'UDim', 'Vector2',
    'Vector3', 'CFrame', 'Font', 'TweenInfo', 'ColorSequence', 'NumberSequence',
    'ColorSequenceKeypoint', 'NumberSequenceKeypoint', 'Rect', 'BrickColor',
    'readfile', 'writefile', 'isfile', 'isfolder', 'makefolder', 'getgenv',
    'identifyexecutor', 'request', 'tick', 'time', 'wait', 'spawn', 'delay',
    'value', 'name', 'index', 'set', 'get',
}


class Scope:
    __slots__ = ('parent', 'names')

    def __init__(self, parent):
        self.parent = parent
        self.names = {}      # orig -> [(decl_token_idx, newname)]


def sanitize(base):
    if not base:
        return None
    s = ''.join(ch if (ch.isalnum() or ch == '_') else '_' for ch in str(base)).strip('_')
    if not s:
        return None
    if s[0].isdigit():
        s = 'v' + s
    return s


def split_exprs(toks, start, end):
    out, depth, cur = [], 0, start
    for k in range(start, end):
        t, v = toks[k]
        if t == 'o':
            if v in '([{':
                depth += 1
            elif v in ')]}':
                depth -= 1
            elif v == ',' and depth == 0:
                out.append((cur, k))
                cur = k + 1
    out.append((cur, end))
    return out


def expr_end(toks, k, n):
    """从 k 起找到一个表达式/语句的结束位置。"""
    depth = 0
    while k < n:
        t, v = toks[k]
        if t == 'o':
            if v in '([{':
                depth += 1
            elif v in ')]}':
                depth -= 1
                if depth < 0:
                    return k
            elif depth == 0 and v in (',', ';'):
                return k
        elif t == 'w' and depth == 0 and v in ('local', 'end', 'return', 'else', 'elseif', 'until'):
            return k
        k += 1
    return k


_KEYWORDS = {
    'and', 'break', 'continue', 'do', 'else', 'elseif', 'end', 'false',
    'for', 'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
    'return', 'then', 'true', 'until', 'while', 'type', 'export',
}


def derive(seg, resolve):
    if not seg:
        return None
    t0 = seg[0]
    if len(seg) == 1 and t0[0] == 'w':
        return resolve(t0[1])          # 纯标识符：沿用被赋值的名字
    if t0 == ('o', '{'):
        # 表字面量：用第一个非空字段名当线索
        # {conns = {}, drawings = {}, ...}   -> conns
        # {on = false, slot = 2, ...}        -> on
        # {sprint = {...}, speed = {...}}     -> 用外层字段名
        for k in range(1, min(len(seg) - 1, 24)):
            if seg[k][0] == 'w' and k + 1 < len(seg) and seg[k + 1] == ('o', '='):
                cand = seg[k][1]
                if cand.isidentifier() and cand not in _KEYWORDS:
                    return cand
        return 'tbl'
    if t0[0] == 'n':
        return 'num'
    if t0[0] == 's':
        return 'str'
    if t0[0] == 'w':
        w = t0[1]
        if w == 'function':
            # 匿名函数：从函数体里第一条有意义的 API 调用猜用途
            # 注意 seg 是 token 列表，不是字符串
            body = ' '.join(t[1] for t in seg[:400])
            for kw, nm in (
                ('RenderStepped', 'onFrame'),
                ('Heartbeat', 'onTick'),
                ('Stepped', 'onStep'),
                ('InputBegan', 'onInput'),
                ('InputChanged', 'onInputChanged'),
                ('InputEnded', 'onInputEnded'),
                ('MouseButton1Click', 'onClick'),
                ('GetService', 'initServices'),
                ('pcall', 'safeCall'),
                ('tween', 'tween'),
                ('Create', 'create'),
                ('Destroy', 'destroy'),
                ('Disconnect', 'disconnect'),
                ('getgenv', 'setupEnv'),
                ('writefile', 'saveFile'),
                ('readfile', 'loadFile'),
                ('Drawing', 'draw'),
                ('Raycast', 'raycast'),
            ):
                if kw in body:
                    return nm
            return 'fn'
        if w in ('true', 'false'):
            return 'flag'
        if w == 'not':
            return 'cond'
        # 下标取值 tbl[7] / arg[96]：直接用「容器名+下标」
        if len(seg) >= 3 and seg[1] == ('o', '[') and seg[2][0] == 'n':
            return f"{w}_{seg[2][1]}"
        parts = [w]
        k = 1
        while k + 1 < len(seg) and seg[k][0] == 'o' and seg[k][1] in ('.', ':'):
            if seg[k + 1][0] != 'w':
                break
            parts.append(seg[k + 1][1])
            k += 2
        if len(parts) > 1:
            meth = parts[-1]
            obj = parts[0]
            # 类型构造：Color3.fromRGB -> color, UDim2.new -> dim
            type_map = {
                'Color3': 'color', 'CFrame': 'cf', 'Vector2': 'vec2',
                'Vector3': 'vec3', 'UDim2': 'dim', 'UDim': 'dim',
                'Rect': 'rect', 'NumberSequence': 'seq', 'ColorSequence': 'colorSeq',
                'Content': 'content', 'Font': 'font', 'BrickColor': 'brickColor',
            }
            if obj in type_map:
                if meth in ('fromRGB', 'fromHex', 'new'):
                    return type_map[obj]
            if meth == 'new':
                # Drawing.new -> drawing；Instance.new -> inst
                return {'Drawing': 'drawing'}.get(obj, obj + '_new')
            if meth.startswith('Get') and meth.endswith('FromCharacter'):
                return 'player'
            if meth in ('fromScale',):
                return 'scale'
            if meth in ('fromOffset',):
                return 'offset'
            if meth in ('fromEnum',):
                return 'enum'
            # 查询类：FindFirstChild -> child
            q = {
                'FindFirstChild': 'child', 'FindFirstChildOfClass': 'child',
                'WaitForChild': 'child', 'GetChildren': 'children',
                'GetDescendants': 'descendants', 'GetPlayers': 'players',
                'GetMouseLocation': 'mousePos',
                'WorldToViewportPoint': 'screenPos', 'Raycast': 'hit',
            }
            if meth in q:
                return q[meth]
            return meth
        if len(seg) >= 4 and seg[1] == ('o', '(') and seg[2][0] == 's':
            s = seg[2][1].strip('"\'')
            if s and s.isidentifier():
                return s
        # 调用结果：用被调函数名 + 语义后缀，而不是一律 +Res
        #   Drawing.new(...)      -> newDrawing
        #   workspace:FindFirstChild("x") -> x 或 foundChild
        #   player:GetPlayerFromCharacter() -> foundPlayer
        callee = resolve(w)
        suffix_map = {
            'new': 'obj', 'Create': 'obj', 'newInstance': 'obj',
            'FindFirstChild': 'child', 'FindFirstChildOfClass': 'child',
            'WaitForChild': 'child', 'GetChildren': 'children',
            'GetDescendants': 'descendants',
            'GetPlayerFromCharacter': 'player', 'GetPlayers': 'players',
            'GetMouseLocation': 'mousePos', 'WorldToViewportPoint': 'screenPos',
            'Raycast': 'hit', 'GetPartsInPart': 'parts',
            'PCall': 'res', 'pcall': 'res',
        }
        tail = parts[-1] if len(parts) > 1 else ''
        if tail in suffix_map:
            return suffix_map[tail] + (callee if callee not in ('fn', 'tbl') else '')
        if callee and callee not in ('fn', 'tbl', 'v'):
            return callee + 'Res'
        return 'Res'
    if t0[0] == 'w':
        # tbl[7] / arg[96] 这种下标取值：用「容器名 + 下标」更具体
        k = 1
        while k + 1 < len(seg) and seg[k] == ('o', '['):
            if seg[k + 1][0] == 'n':
                return f"{t0[1]}{seg[k + 1][1]}"
            break
    return None


def rename(toks):
    n = len(toks)
    root = Scope(None)
    cur = root
    out = list(toks)
    used = set(BAD_BASE)
    newnames = [None] * n

    def resolve(name):
        s = cur
        while s is not None:
            lst = s.names.get(name)
            if lst:
                return lst[-1][1]
            s = s.parent
        return name

    def declare(name, idx):
        base = newnames[idx] if 0 <= idx < n else None
        lst = cur.names.get(name)
        if lst is None:
            lst = []
            cur.names[name] = lst
        lst.append((idx, base))

    def in_scope_listed(nm):
        """只在当前作用域链上查重名。
        早先用全文件集合 used，导致每个局部变量 C 都撞名变成 C2/C3/...
        最后满屏 v1234。真正需要的是「同一作用域内不重名」。"""
        sc = cur
        while sc is not None:
            for lst in sc.names.values():
                for _, b in lst:
                    if b == nm:
                        return True
            sc = sc.parent
        return nm in BAD_BASE

    def bind(name, idx, base):
        base = sanitize(base) or 'val'
        # 单字母原名：只有「没推出更好的名字」时才保留
        if (len(name) <= 2 and name.isalpha() and name.isidentifier()
                and base in ('v', 'val', 'Res', 'num', 'str', 'cond', 'flag')):
            if not in_scope_listed(name):
                newnames[idx] = name
                return name
        if in_scope_listed(base):
            m = 2
            while in_scope_listed(base + str(m)):
                m += 1
            base = base + str(m)
        used.add(base)
        newnames[idx] = base
        return base

    i = 0
    stack = [root]
    while i < n:
        t, v = toks[i]

        if t == 'o':
            if v in ('(', '[', '{'):
                pass
            i += 1
            continue

        if t != 'w':
            i += 1
            continue

        # ---- local ----
        if v == 'local':
            j = i + 1
            if j < n and toks[j] == ('w', 'function'):
                nm_idx = j + 1 if (j + 1 < n and toks[j + 1][0] == 'w') else None
                if nm_idx is not None:
                    # 从函数体推断用途，而不是一律叫 fn
                    # 取函数体前 400 个 token 做关键词匹配
                    body = ' '.join(t[1] for t in toks[j:min(n, j + 400)])
                    base = 'fn'
                    for kw, nm in (
                        ('RenderStepped', 'onFrame'),
                        ('Heartbeat', 'onTick'),
                        ('Stepped', 'onStep'),
                        ('InputBegan', 'onInput'),
                        ('InputChanged', 'onInputChanged'),
                        ('InputEnded', 'onInputEnded'),
                        ('MouseButton1Click', 'onClick'),
                        ('pcall', 'safeCall'),
                        ('Drawing', 'draw'),
                        ('Raycast', 'raycast'),
                        ('getgenv', 'setupEnv'),
                        ('writefile', 'saveFile'),
                        ('readfile', 'loadFile'),
                        ('Tween', 'tween'),
                        ('Create', 'create'),
                        ('Destroy', 'destroy'),
                        ('Disconnect', 'disconnect'),
                        ('Humanoid', 'onHumanoid'),
                        ('Character', 'onCharacter'),
                        ('Camera', 'onCamera'),
                        ('Health', 'onHealth'),
                        ('Update', 'update'),
                        ('Render', 'render'),
                        ('Refresh', 'refresh'),
                        ('Draw', 'draw'),
                    ):
                        if kw in body:
                            base = nm
                            break
                    bind(toks[nm_idx][1], nm_idx, base)
                    declare(toks[nm_idx][1], nm_idx)
                    out[nm_idx] = ('w', newnames[nm_idx])
                i = j
                continue
            names = []
            while j < n and toks[j][0] == 'w':
                names.append(j)
                j += 1
                if j < n and toks[j] == ('o', ','):
                    j += 1
                    continue
                break
            # 先算 RHS（此时局部变量尚未生效）
            exprs = []
            k = j
            if k < n and toks[k] == ('o', '='):
                end = expr_end(toks, k + 1, n)
                exprs = split_exprs(toks, k + 1, end)
            for idx2, name_idx in enumerate(names):
                seg = None
                if idx2 < len(exprs):
                    a, b = exprs[idx2]
                    seg = toks[a:b]
                base = derive(seg, resolve)
                if base is None:
                    base = v_name(toks, name_idx)
                nm = toks[name_idx][1]
                nb = bind(nm, name_idx, base)
                out[name_idx] = ('w', nb)
                declare(nm, name_idx)
            i = j
            continue

        # ---- function ----
        if v == 'function':
            # 名字链
            j = i + 1
            ismethod = False
            if j < n and toks[j][0] == 'w':
                # 只在不是匿名函数时消费名字
                pass
            while j < n and toks[j][0] == 'w':
                j += 1
                if j < n and toks[j] == ('o', '.'):
                    j += 1
                elif j < n and toks[j] == ('o', ':'):
                    j += 1
                    ismethod = True
                else:
                    break
            cur = Scope(cur)
            stack.append(cur)
            if ismethod:
                declare('self', i)
            if j < n and toks[j] == ('o', '('):
                j += 1
                k = 0
                params = []
                while j < n and toks[j] != ('o', ')'):
                    if toks[j][0] == 'w':
                        params.append(j)
                    j += 1
                for q, pidx in enumerate(params):
                    nm = toks[pidx][1]
                    nb = bind(nm, pidx, 'arg')
                    out[pidx] = ('w', nb)
                    declare(nm, pidx)
                j += 1
            i = j
            continue

        # ---- for ----
        if v == 'for':
            j = i + 1
            fvars = []
            while j < n and toks[j] != ('w', 'do') and toks[j] != ('w', 'in'):
                if toks[j][0] == 'w':
                    fvars.append(j)
                j += 1
            numeric = (j < n and toks[j] == ('w', 'do'))
            cur = Scope(cur)
            stack.append(cur)
            for q, pidx in enumerate(fvars):
                nm = toks[pidx][1]
                if numeric:
                    base = 'i'
                elif len(fvars) == 2:
                    base = 'i' if q == 0 else 'item'
                else:
                    base = 'k' if q % 2 == 0 else 'item'
                nb = bind(nm, pidx, base)
                out[pidx] = ('w', nb)
                declare(nm, pidx)
            # 走到 do 之后继续（do 会再开一层）
            i = j
            continue

        if v in ('then', 'do', 'repeat'):
            cur = Scope(cur)
            stack.append(cur)
            i += 1
            continue

        if v in ('end', 'until'):
            if len(stack) > 1:
                stack.pop()
            cur = stack[-1]
            i += 1
            continue

        if v in ('else', 'elseif'):
            if len(stack) > 1:
                stack.pop()
            cur = Scope(cur)
            stack.append(cur)
            i += 1
            continue

        # ---- 普通标识符 ----
        if v in ('nil', 'true', 'false', 'and', 'or', 'not', 'in', 'goto'):
            i += 1
            continue
        prev = toks[i - 1] if i > 0 else None
        nxt = toks[i + 1] if i + 1 < n else None
        if prev and prev[0] == 'o' and prev[1] in ('.', ':', '::'):
            i += 1
            continue
        if nxt and nxt == ('o', '=') and prev and prev[0] == 'o' and prev[1] in ('{', ','):
            i += 1
            continue
        nm = resolve(v)
        if nm != v:
            out[i] = ('w', nm)
        i += 1

    for idx2, (tt, vv) in enumerate(toks):
        if tt == 'w' and vv in RESERVED:
            out[idx2] = ('w', vv)

    return out


def v_name(toks, idx):
    nm = toks[idx][1] if 0 <= idx < len(toks) else 'v'
    if len(nm) <= 2 and nm.isalpha():
        return nm      # 单字母原名保留，比 v123 好读
    return nm if nm.isidentifier() else 'v'


if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    toks = tokenize(src)
    new = rename(toks)
    txt = build_tokens(new)
    open(sys.argv[2], 'w').write(txt + '\n')
    print('tokens', len(toks), 'out', len(txt))
