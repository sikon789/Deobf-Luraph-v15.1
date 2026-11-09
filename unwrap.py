#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unwrap.py —— 去掉 Luraph 的纯包装函数层，减少无谓缩进

Luraph 把业务代码包成：

    local __part1 = function(arg, ..., arg7)
        return function(arg8, arg9, arg10)
            return function( ... )
                -- 真正的业务代码（缩进 12+）
            end
        end
    end

外层那几层只是闭包包装，函数体里第一句就是 `return function`，
不含任何逻辑。剥掉后：

    local __part1 = function(...)
        -- 真正的业务代码（缩进 4）
    end

对外行为完全一致：__part1 仍然是可调用函数。

判定很严：每层必须是 `function(...)`，且函数体**第一句就是 return function**，
否则视为有实质逻辑，不剥。
"""
import re
import sys
from pathlib import Path

# Lua 关键字里会增加块层级的
BLOCK_OPEN = {'function', 'if', 'for', 'while', 'do', 'repeat'}


def tokenize(src):
    """返回 [(kind, text, pos)]，kind ∈ w/o/s/n/c
    只用于配平，不需要完整词法。"""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        # 空白
        if c in ' \t\r\n':
            i += 1
            continue
        # 注释
        if src.startswith('--', i):
            j = src.find('\n', i)
            i = (j + 1) if j > 0 else n
            out.append(('c', '', i))
            continue
        # 长括号字符串
        m = re.match(r'\[(=*)\[', src[i:])
        if m:
            eq = m.group(1)
            close = ']' + eq + ']'
            j = src.find(close, i + m.end())
            j = (j + len(close)) if j > 0 else n
            out.append(('s', src[i:j], i))
            i = j
            continue
        # 普通字符串
        if c in '"\'':
            q = c
            j = i + 1
            while j < n:
                if src[j] == '\\':
                    j += 2
                    continue
                if src[j] == q:
                    j += 1
                    break
                j += 1
            out.append(('s', src[i:j], i))
            i = j
            continue
        # 标识符
        if c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'):
                j += 1
            out.append(('w', src[i:j], i))
            i = j
            continue
        # 数字
        if c.isdigit():
            j = i
            while j < n and (src[j].isalnum() or src[j] in '._'):
                j += 1
            out.append(('n', src[i:j], i))
            i = j
            continue
        out.append(('o', c, i))
        i += 1
    return out


def match_block(toks, fn_idx):
    """fn_idx 指向 function 关键字。返回它对应 end 的 token 下标。"""
    depth = 0
    i = fn_idx
    n = len(toks)
    while i < n:
        kind, text, _ = toks[i]
        if kind == 'w':
            if text in ('function', 'if', 'for', 'while', 'do', 'repeat'):
                depth += 1
            elif text == 'end':
                depth -= 1
                if depth == 0:
                    return i
            elif text == 'until':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def shift_left(text, spaces):
    out = []
    for ln in text.split('\n'):
        if not ln.strip():
            out.append('')
            continue
        k = 0
        while k < spaces and k < len(ln) and ln[k] == ' ':
            k += 1
        out.append(ln[k:])
    return '\n'.join(out)


def unwrap_one(text):
    """处理文件里所有 `local __partN = function(...) return function...`
    返回 (新文本, 处理层数)"""
    total = 0
    for _ in range(20):
        toks = tokenize(text)
        # 找 local __partN = function
        found = None
        for k in range(len(toks) - 3):
            if (toks[k][0] == 'w' and toks[k][1] == 'local'
                    and toks[k + 1][0] == 'w'
                    and toks[k + 1][1].startswith('__part')
                    and toks[k + 2] == ('o', '=', toks[k + 2][2])
                    and toks[k + 3][0] == 'w' and toks[k + 3][1] == 'function'):
                found = k + 3
                break
        if found is None:
            break

        outer_fn = found
        # 逐层剥
        cur_fn = outer_fn
        layers = 0
        while layers < 6:
            # 找这个 function 的参数列表结束
            j = cur_fn + 1
            if toks[j] != ('o', '(', toks[j][2]):
                break
            parend = j
            depth = 0
            while j < len(toks):
                if toks[j][0] == 'o' and toks[j][1] == '(':
                    depth += 1
                elif toks[j][0] == 'o' and toks[j][1] == ')':
                    depth -= 1
                    if depth == 0:
                        parend = j
                        break
                j += 1
            # 参数列表后第一句必须是 return function
            k2 = parend + 1
            if k2 < len(toks) and toks[k2][0] == 'w' and toks[k2][1] == 'return':
                if k2 + 1 < len(toks) and toks[k2 + 1][0] == 'w' and toks[k2 + 1][1] == 'function':
                    cur_fn = k2 + 1
                    layers += 1
                    continue
            break

        if layers == 0:
            break

        # 内层 function 的 end
        inner_end = match_block(toks, cur_fn)
        if inner_end < 0:
            break

        # 内层代码范围：cur_fn 的参数列表之后 到 inner_end 之前
        j = cur_fn + 1
        depth = 0
        while j < len(toks):
            if toks[j][0] == 'o' and toks[j][1] == '(':
                depth += 1
            elif toks[j][0] == 'o' and toks[j][1] == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body_start_pos = toks[j][2] + 1
        body_end_pos = toks[inner_end][2]

        # 外层 function 的起点与缩进
        outer_pos = toks[outer_fn][2]
        line_start = text.rfind('\n', 0, outer_pos) + 1
        outer_indent = outer_pos - line_start

        body = text[body_start_pos:body_end_pos]
        first_line = body.lstrip('\n')
        lead = len(first_line) - len(first_line.lstrip(' '))
        target = outer_indent + 4
        body = shift_left(body, max(0, lead - target))

        # 原文件里内层 end 之后的 layers-1 个 end 要吃掉
        tail_pos = body_end_pos + 3          # 跳过 'end'
        rest = text[tail_pos:]
        eaten = 0
        while eaten < layers:
            m2 = re.match(r'[ \t]*\n?[ \t]*end', rest)
            if not m2:
                break
            rest = rest[m2.end():]
            eaten += 1

        # 外层参数原样保留
        outer_paren_start = toks[outer_fn + 1][2]
        pdepth = 0
        ppos = outer_paren_start
        while ppos < len(text):
            if text[ppos] == '(':
                pdepth += 1
            elif text[ppos] == ')':
                pdepth -= 1
                if pdepth == 0:
                    break
            ppos += 1
        outer_params = text[outer_paren_start:ppos + 1]

        head = text[:outer_pos]
        new_text = (head + 'function' + outer_params + '\n'
                    + body.rstrip() + '\n'
                    + ' ' * outer_indent + 'end'
                    + rest)
        text = new_text
        total += 1

    return text, total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print(__doc__)
        return 1
    src = Path(args[0])
    dst = Path(args[1]) if len(args) > 1 else src.with_suffix('.unwrap.luau')
    text = src.read_text(encoding='utf-8', errors='ignore')
    out, n = unwrap_one(text)
    dst.write_text(out, encoding='utf-8')
    indents = [len(l) - len(l.lstrip()) for l in out.split('\n') if l.strip()]
    print(f"[unwrap] 剥掉 {n} 段包装层，最大缩进 {max(indents, default=0)} 空格 → {dst}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
