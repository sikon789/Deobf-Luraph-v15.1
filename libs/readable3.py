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
    # 添加清理标记
    return out

def cleanup_blocks(toks):
    # 移除 Luraph V15.1 框架残留
    # 保留业务逻辑，移除 handler 方法定义和死代码
    pass


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


def derive(seg, resolve):
    if not seg:
        return None
    t0 = seg[0]
    if len(seg) == 1 and t0[0] == 'w':
        return resolve(t0[1])          # 纯标识符：沿用被赋值的名字
    if t0 == ('o', '{'):
        return 'tbl'
    if t0[0] == 'n':
        return 'num'
    if t0[0] == 's':
        return 'str'
    if t0[0] == 'w':
        w = t0[1]
        if w == 'function':
            return 'fn'
        if w in ('true', 'false'):
            return 'flag'
        if w == 'not':
            return 'cond'
        parts = [w]
        k = 1
        while k + 1 < len(seg) and seg[k][0] == 'o' and seg[k][1] in ('.', ':'):
            if seg[k + 1][0] != 'w':
                break
            parts.append(seg[k + 1][1])
            k += 2
        if len(parts) > 1:
            meth = parts[-1]
            if meth == 'new':
                return parts[0] + '_new'
            if meth in ('fromRGB', 'fromHex'):
                return 'rgb'
            if meth == 'fromScale':
                return 'scale'
            if meth == 'fromOffset':
                return 'offset'
            if meth == 'fromEnum':
                return 'enum'
            return meth
        if len(seg) >= 4 and seg[1] == ('o', '(') and seg[2][0] == 's':
            s = seg[2][1].strip('"\'')
            if s and s.isidentifier():
                return s
        return resolve(w) + 'Res'
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

    def bind(name, idx, base):
        base = sanitize(base) or 'val'
        if base in used:
            m = 2
            while (base + str(m)) in used:
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
                    bind(toks[nm_idx][1], nm_idx, 'fn')
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

    # 添加清理标记
    return out

def cleanup_blocks(toks):
    # 移除 Luraph V15.1 框架残留
    # 保留业务逻辑，移除 handler 方法定义和死代码
    pass


def v_name(toks, idx):
    return 'v'


if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    toks = tokenize(src)
    new = rename(toks)
    txt = build_tokens(new)
    open(sys.argv[2], 'w').write(txt + '\n')
    print('tokens', len(toks), 'out', len(txt))
