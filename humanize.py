#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
humanize.py —— 把反混淆产物整理成「像人写的」样子

纯文本后处理，不改变语义。做的事：

  1. 长行折行：超过 MAX_LEN 的逻辑链（and / or / .. / + 等）在运算符后断开，
     续行按括号层级缩进，与主流 Lua 风格一致
  2. 表字面量：每个字段一行（已在 format 阶段做过，这里兜底）
  3. 函数之间空一行
  4. 去掉冗余空行（连续 2 行以上压成 1 行）
  5. 运算符两侧空格、逗号后空格
  6. 删除行尾多余空白

用法:
    python humanize.py 输入.luau [输出.luau]
    python humanize.py 输入.luau --max-len 100
"""
import re
import sys
from pathlib import Path

MAX_LEN = 100

# 断行优先级：越靠前越优先（人写代码时也是先在这几处断）
BREAK_PRIORITY = [
    ', ',          # 参数/表元素之间
    ' and ', ' or ',
    ' .. ',
    ' == ', ' ~= ', ' <= ', ' >= ',
    ' + ', ' - ',
    ' * ', ' / ',
]
BREAK_AFTER = BREAK_PRIORITY
# 这些出现在字符串/注释里时不能碰，靠 split_tokens 判断

LINE_COMMENT = re.compile(r'^(.*?)(\s*--(?!\[\[).*)$')
STRING_LIT = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')


def mask_strings(line):
    """把字符串内容换成占位，避免在里面断行/改空格"""
    out = []
    hidden = []

    def sub(m):
        hidden.append(m.group(0))
        return f'\x00{len(hidden) - 1}\x00'

    return STRING_LIT.sub(sub, line), hidden


def unmask(line, hidden):
    for i, s in enumerate(hidden):
        line = line.replace(f'\x00{i}\x00', s)
    return line


def tidy_spacing(line):
    """运算符、关键字两侧空格"""
    masked, hidden = mask_strings(line)
    # 逗号后加空格
    masked = re.sub(r',(?=[^\s\)\]\}])', ', ', masked)
    # 右括号/标识符后紧跟关键字：)do / ]then / end)if
    masked = re.sub(r'([)\]"\'])\s*(do|then|end|else|elseif)\b', r'\1 \2', masked)
    # 标识符后紧跟 then/do —— 必须确认左边是分隔符，
    # 否则 soundUndo 这种标识符会被切开（曾被切坏成 "soundUn do"）
    masked = re.sub(r'\)(or|and)\b', r') \1', masked)
    # "* 1" / "+ 1" 前的多余空格保持，但去掉 " ]" 这种
    masked = re.sub(r'\s+([,;)\]}])', r'\1', masked)
    return unmask(masked, hidden)
    # 二元运算符两侧空格
    masked = re.sub(r'\s{2,}(?=\S)', lambda m: m.group(0), masked)
    return unmask(masked, hidden)


def leading_ws(line):
    return line[:len(line) - len(line.lstrip())]


def break_long_line(line, max_len=MAX_LEN):
    """把超长行在逻辑运算符处断开，返回多行列表"""
    if len(line) <= max_len:
        return [line]

    indent = leading_ws(line)
    # 保护字符串内容，但保留字符串外的全部结构（括号、运算符）
    masked, hidden = mask_strings(line)
    # 先规范逗号空格，否则 ", " 断点根本匹配不到（原文常写 "a,b"）
    masked = re.sub(r',(?=[^\s\)\]\}])', ', ', masked)
    if len(masked) <= max_len:
        return [unmask(masked, hidden)]
    base_indent = len(indent)

    def in_string(idx):
        """idx 是否落在 \x00N\x00 占位符内部"""
        # 向前找最近的 \x00，看它到 idx 之间是否只有数字
        k = masked.rfind('\x00', 0, idx + 1)
        if k < 0:
            return False
        seg = masked[k:idx + 1]
        # 形如 \x00 12 ... 且还没遇到闭合的 \x00 → 在占位符内
        body = seg[1:]
        if '\x00' in body:
            return False          # 已经闭合过，不在内部
        return body.isdigit() or body == ''

    parts = []
    rest = masked
    guard = 0
    while len(rest) > max_len and guard < 12:
        guard += 1
        window = rest[:max_len]
        cut = -1
        # 按优先级找：高优先级只要在窗口后半段就用它
        for pri, op in enumerate(BREAK_AFTER):
            pos = -1
            start = 0
            while True:
                idx = window.find(op, start)
                if idx < 0:
                    break
                if idx > 0 and not in_string(idx):
                    pos = idx
                start = idx + 1
            if pos <= 0:
                continue
            # 记录高优先级运算符的「最后一个可用位置」
            if pos > max_len * 0.3:
                cut = pos + len(op) - 1
                break
            if cut < 0:
                cut = pos + len(op) - 1
        if cut <= 0:
            break
        head = rest[:cut].rstrip()
        # 若断点切在占位符中间，回退到占位符起点
        m2 = re.search(r'\x00\d*$', head)
        if m2:
            head = head[:m2.start()].rstrip()
            cut = len(head)
        parts.append(head)
        rest = '    ' + rest[cut:].lstrip()

    parts.append(rest)
    if len(parts) == 1:
        return [line]

    out = []
    for i, p in enumerate(parts):
        if i == 0:
            out.append(unmask(p, hidden))
        else:
            out.append(indent + unmask(p, hidden) if not p.startswith('    ')
                       else indent + unmask(p, hidden))
    return out


def process(text, max_len=MAX_LEN):
    lines = text.split('\n')
    out = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            out.append('')
            continue

        # 注释行原样保留
        if line.lstrip().startswith('--'):
            out.append(line)
            continue

        line = tidy_spacing(line)
        for piece in break_long_line(line, max_len):
            out.append(piece.rstrip())

    # ---- 函数之间空行 ----
    res = []
    for i, l in enumerate(out):
        s = l.strip()
        prev = out[i - 1].strip() if i > 0 else ''
        # 顶层/次层 end 之后若是新语句，补空行
        if (s and prev == 'end' and re.match(r'(local\s+function|function|local\s+\w+\s*=)', s)
                and len(leading_ws(l)) <= 4):
            res.append('')
        res.append(l)

    # ---- 压掉连续空行 ----
    final = []
    for l in res:
        if not l.strip():
            if final and not final[-1].strip():
                continue
        final.append(l)

    while final and not final[-1].strip():
        final.pop()

    return '\n'.join(final) + '\n'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    max_len = MAX_LEN
    for i, a in enumerate(sys.argv):
        if a == '--max-len' and i + 1 < len(sys.argv):
            max_len = int(sys.argv[i + 1])

    if not args:
        print(__doc__)
        return 1

    src = Path(args[0])
    dst = Path(args[1]) if len(args) > 1 else src.with_suffix('.human.luau')
    text = src.read_text(encoding='utf-8', errors='ignore')

    before = text.count('\n')
    out = process(text, max_len)
    after = out.count('\n')
    dst.write_text(out, encoding='utf-8')
    print(f"[humanize] {src.name} {before:,} 行 → {dst.name} {after:,} 行")
    return 0


if __name__ == '__main__':
    sys.exit(main())
