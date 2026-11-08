#!/usr/bin/env python3
"""Line-break + indent minified Lua/Luau. Depth-clamped, lossless ($ checked)."""
import sys, re

OPEN = {'function', 'then', 'do', 'repeat'}
MID = {'else', 'elseif'}
CLOSE = {'end', 'until'}
MAXD = 14


def tokenize(s):
    i, n = 0, len(s)
    out = []
    while i < n:
        c = s[i]
        if c in ' \t\r\n':
            i += 1
            continue
        if s.startswith('--', i):
            j = i + 2
            if j < n and s[j] == '[':
                k = j + 1
                while k < n and s[k] == '=':
                    k += 1
                if k < n and s[k] == '[':
                    eq = s[j + 1:k]
                    close = ']' + eq + ']'
                    e = s.find(close, k + 1)
                    e = n if e < 0 else e + len(close)
                    out.append(('c', s[i:e]))
                    i = e
                    continue
            e = s.find('\n', i)
            e = n if e < 0 else e
            out.append(('c', s[i:e]))
            i = e
            continue
        if c in '"\'':
            j = i + 1
            buf = [c]
            while j < n:
                d = s[j]
                buf.append(d)
                if d == '\\':
                    if j + 1 < n:
                        buf.append(s[j + 1])
                    j += 2
                    continue
                j += 1
                if d == c:
                    break
            out.append(('s', ''.join(buf)))
            i = j
            continue
        if c == '[':
            k = i + 1
            while k < n and s[k] == '=':
                k += 1
            if k < n and s[k] == '[':
                eq = s[i + 1:k]
                close = ']' + eq + ']'
                e = s.find(close, k + 1)
                e = n if e < 0 else e + len(close)
                out.append(('s', s[i:e]))
                i = e
                continue
        if c.isdigit() or (c == '.' and i + 1 < n and s[i + 1].isdigit()):
            j = i
            if c == '0' and i + 1 < n and s[i + 1] in 'xX':
                j = i + 2
                while j < n and s[j] in '0123456789abcdefABCDEF':
                    j += 1
            else:
                while j < n and s[j].isdigit():
                    j += 1
                if j < n and s[j] == '.' and (j + 1 >= n or s[j + 1] != '.'):
                    j += 1
                    while j < n and s[j].isdigit():
                        j += 1
                if j < n and s[j] in 'eE':
                    k = j + 1
                    if k < n and s[k] in '+-':
                        k += 1
                    if k < n and s[k].isdigit():
                        j = k
                        while j < n and s[j].isdigit():
                            j += 1
            out.append(('n', s[i:j]))
            i = j
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < n and (s[j].isalnum() or s[j] == '_'):
                j += 1
            out.append(('w', s[i:j]))
            i = j
            continue
        for op in ('...', '..=', '==', '~=', '<=', '>=', '..', '::', '->', '//',
                   '+=', '-=', '*=', '/=', '%=', '^='):
            if s.startswith(op, i):
                out.append(('o', op))
                i += len(op)
                break
        else:
            out.append(('o', c))
            i += 1
    return out


def build(s):
    return build_tokens(tokenize(s))


def build_tokens(toks):
    lines = []
    cur = []
    d = 0

    def flush():
        nonlocal cur
        t = ''.join(cur).strip()
        if t:
            lines.append(('    ' * min(max(d, 0), MAXD)) + t)
        cur = []

    prev = None
    for typ, v in toks:
        if typ == 'c':
            flush()
            lines.append('    ' * min(max(d, 0), MAXD) + v)
            prev = None
            continue
        if typ == 'w' and v in ('local', 'return'):
            if v == 'return' and prev == 'w' and cur and cur[-1] in ('and', 'or', 'not', '='):
                pass
            elif prev in ('w', 'n', 's'):
                cur.append(' ')
            flush()
            cur.append(v + ' ')
            prev = v
            continue
        if typ == 'w' and v in CLOSE:
            if prev in ('w', 'n', 's'):
                cur.append(' ')
            flush()
            d -= 1
            cur.append(v)
            flush()
            prev = v
            continue
        if typ == 'w' and v in MID:
            if prev in ('w', 'n', 's'):
                cur.append(' ')
            flush()
            d -= 1
            cur.append(v)
            flush()
            d += 1
            prev = v
            continue
        if typ == 'w' and v in OPEN:
            if prev in ('w', 'n', 's'):
                cur.append(' ')
            cur.append(v)
            flush()
            d += 1
            prev = v
            continue
        if typ == 'o' and v == ';':
            cur.append(';')
            flush()
            prev = None
            continue
        if typ == 'o' and v == ',':
            cur.append(', ')
            prev = None
            continue
        if typ == 'o' and v in '()[]{}':
            cur.append(v)
            prev = 'w' if v in ')]}' else None
            continue
        if typ in ('w', 'n', 's') and prev in ('w', 'n', 's'):
            cur.append(' ')
        elif typ in ('w', 'n', 's'):
            pass
        elif typ == 'o':
            cur.append(' ' + v + ' ')
            prev = None
            continue
        cur.append(v)
        prev = typ
    flush()
    return '\n'.join(lines)


if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    out = build(src)
    open(sys.argv[2], 'w').write(out + '\n')
    ls = [len(l) for l in out.split('\n')]
    print('lines', len(ls), 'bytes', len(out), 'maxline', max(ls), 'median', sorted(ls)[len(ls) // 2])
