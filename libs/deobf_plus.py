#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luraph v15.1 静态反混淆 · 增强版 (deobf_plus)
基于本仓库原工具 (beautify2.tokenize / readable3.rename / build_tokens) 的思路重写，
修正并补强了原工具对 v15.1 无效的地方：

  1. 正确的 Luau 词法：支持 0b/0B/0x/0X + 下划线数字分隔符。
     原 tokenizer 会把 0B110001_1_1_111 切成 ("n","0") + ("w","B110001_1_1_111")，
     排版后变成 `0 B110001_1_1_111`，直接破坏语法。
  2. 字符串转义解码：\\xNN / \\NNN / \\u{XXXX} / \\z 还原成明文，
     例如 math["\\x72\\x61\\110\\100\\x6f\\x6d"] -> math["random"]（语义等价、无损）。
  3. 常量算术折叠：((0b1100+0b1)+(0B101111-0b100001)) -> 60。
  4. handler 表语义标注：抽取 [key]=value 映射，写入代码注释并导出 handler_map.md。
  5. 变量语义重命名（复用 libs/readable3.py）+ 语句级缩进排版。

只做静态等价变换，不执行任何被分析脚本。业务层源码需要动态执行 VM 解密桩才能拿到，
本工具不负责这一步。

用法: python3 deobf_plus.py <input.lua|.txt> -o <output.lua> [--no-rename] [--map <map.md>]
"""
import sys
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "libs"))

# ---------------------------------------------------------------- 词法分析
OPS = (
    '...', '..=', '===', '==', '~=', '<=', '>=', '<<=', '>>=',
    '..', '::', '->', '//', '+=', '-=', '*=', '/=', '%=', '^=', '&=', '|=',
    '<<', '>>', '^', '&', '|', '~',
)


def tokenize(s):
    """返回 [(type, text)]，type ∈ w(标识符) n(数字) s(字符串) o(运算符/标点) c(注释)"""
    i, n = 0, len(s)
    out = []
    while i < n:
        c = s[i]

        if c in ' \t\r\n':
            i += 1
            continue

        # ---- 注释 ----
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

        # ---- 长字符串 [=[...]=] ----
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

        # ---- 短字符串 ----
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
            lit = ''.join(buf)
            out.append(('s', lit))
            i = j
            continue

        # ---- 数字（含 0b/0x 前缀与 _ 分隔符） ----
        if c.isdigit() or (c == '.' and i + 1 < n and s[i + 1].isdigit()):
            j = i
            if c == '0' and i + 1 < n and s[i + 1] in 'xXbB':
                prefix = s[i + 1].lower()
                valid = '0123456789abcdefABCDEF_' if prefix == 'x' else '01_'
                j = i + 2
                while j < n and s[j] in valid:
                    j += 1
            else:
                while j < n and (s[j].isdigit() or s[j] == '_'):
                    j += 1
                # 小数点：排除 `..` 连接符
                if j < n and s[j] == '.' and (j + 1 >= n or s[j + 1] != '.'):
                    j += 1
                    while j < n and (s[j].isdigit() or s[j] == '_'):
                        j += 1
                # 指数
                if j < n and s[j] in 'eE':
                    k = j + 1
                    if k < n and s[k] in '+-':
                        k += 1
                    if k < n and s[k].isdigit():
                        j = k
                        while j < n and (s[j].isdigit() or s[j] == '_'):
                            j += 1
            out.append(('n', s[i:j]))
            i = j
            continue

        # ---- 标识符 ----
        if c.isalpha() or c == '_':
            j = i
            while j < n and (s[j].isalnum() or s[j] == '_'):
                j += 1
            out.append(('w', s[i:j]))
            i = j
            continue

        # ---- 运算符 ----
        for op in OPS:
            if s.startswith(op, i):
                out.append(('o', op))
                i += len(op)
                break
        else:
            out.append(('o', c))
            i += 1
    return out


# ---------------------------------------------------------------- 数字归一化
def parse_num(lit):
    t = lit.replace('_', '')
    try:
        if t[:2].lower() == '0x':
            return int(t, 16)
        if t[:2].lower() == '0b':
            return int(t, 2)
        if re.fullmatch(r'[+-]?\d+', t):
            return int(t)
        return float(t)
    except ValueError:
        return None


def norm_num(lit):
    v = parse_num(lit)
    if v is None:
        return lit
    if isinstance(v, int):
        return str(v)
    return repr(v)


# ---------------------------------------------------------------- 字符串解码
ESC_SIMPLE = {
    'a': 7, 'b': 8, 'f': 12, 'n': 10, 'r': 13, 't': 9, 'v': 11,
    '\\': 92, '"': 34, "'": 39, '[': 91, ']': 93,
}


def decode_string(lit):
    """把 Lua 短字符串解码成 bytes；失败返回 None。"""
    if len(lit) < 2 or lit[0] not in '"\'' or lit[-1] != lit[0]:
        return None
    body = lit[1:-1]
    out = bytearray()
    i = 0
    while i < len(body):
        ch = body[i]
        if ch != '\\':
            out.extend(ch.encode('utf-8'))
            i += 1
            continue
        i += 1
        if i >= len(body):
            return None
        e = body[i]
        if e == 'x':
            if i + 2 >= len(body) or not re.fullmatch(r'[0-9a-fA-F]{2}', body[i + 1:i + 3]):
                return None
            out.append(int(body[i + 1:i + 3], 16))
            i += 3
        elif e == 'u' and i + 1 < len(body) and body[i + 1] == '{':
            k = body.find('}', i + 2)
            if k < 0 or not re.fullmatch(r'[0-9a-fA-F]+', body[i + 2:k]):
                return None
            try:
                out.extend(chr(int(body[i + 2:k], 16)).encode('utf-8'))
            except ValueError:
                return None
            i = k + 1
        elif e == 'z':
            i += 1
            while i < len(body) and body[i] in ' \t\r\n':
                i += 1
        elif e.isdigit():
            m = re.match(r'\d{1,3}', body[i:])
            if not m:
                return None
            out.append(int(m.group()) & 0xFF)
            i += len(m.group())
        elif e in ESC_SIMPLE:
            out.append(ESC_SIMPLE[e])
            i += 1
        else:
            return None
    return bytes(out)


def reencode_string(lit):
    """解码后若全部为可打印 ASCII，则改写成明文短字符串（等价变换）。"""
    raw = decode_string(lit)
    if raw is None or not raw:
        return lit
    if any(b < 0x20 or b > 0x7E for b in raw):
        return lit  # 含二进制 payload，保留原转义以免破坏数据
    txt = raw.decode('ascii')
    if '"' not in txt and '\\' not in txt:
        return '"' + txt + '"'
    if "'" not in txt and '\\' not in txt:
        return "'" + txt + "'"
    # 含引号或反斜杠：重新转义
    esc = txt.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return '"' + esc + '"'


# ---------------------------------------------------------------- 常量折叠
ALLOWED_EXPR = re.compile(r'^[\d\s+\-*/%^~&|().]+$')


def fold_consts(toks):
    """把连续「纯数字+算术运算符」（可含括号/一元符号）段折叠为一个数字 token。

    只折叠结果为非负整数的情况：负数写成 '-1' 会被重新词法化成两个 token，
    会破坏等价性，故跳过。
    """
    ok_ops = {'+', '-', '*', '/', '//', '%', '^', '~', '&', '|', '<<', '>>', '(', ')'}
    starts = {'(', '-', '~', '+'}

    def can_start(i):
        if i == 0:
            return True
        pt, pv = toks[i - 1]
        if pt in ('w', 'n', 's') or pv in (')', ']', '}'):
            return False
        return True

    out = []
    i, n = 0, len(toks)
    while i < n:
        t, v = toks[i]
        is_start = (t == 'n') or (t == 'o' and v in starts and can_start(i))
        if not is_start:
            out.append(toks[i])
            i += 1
            continue
        j = i
        while j < n and (toks[j][0] == 'n' or
                         (toks[j][0] == 'o' and toks[j][1] in ok_ops)):
            j += 1
        seg = toks[i:j]
        folded = False
        if (len(seg) >= 3 and any(tt == 'n' for tt, _ in seg) and
                any(tt == 'o' and vv not in ('(', ')') for tt, vv in seg)):
            expr = ''.join(norm_num(x) if tt == 'n' else x for tt, x in seg)
            if ALLOWED_EXPR.fullmatch(expr):
                try:
                    val = eval(expr.replace('^', '**'), {'__builtins__': {}}, {})  # noqa: S307
                    if isinstance(val, (int, float)) and 0 <= val < 2 ** 53:
                        if isinstance(val, float):
                            if val.is_integer():
                                val = int(val)
                            else:
                                val = None
                        if val is not None:
                            out.append(('n', str(val)))
                            folded = True
                except Exception:
                    pass
        if not folded:
            out.extend(seg)
        i = j
    return out


# ---------------------------------------------------------------- handler 表解析
def find_table_body(toks, start):
    """从 start 处的 '{' 找到配对 '}'，返回 (body_start, body_end)。"""
    depth = 0
    for k in range(start, len(toks)):
        t, v = toks[k]
        if t == 'o' and v in ('(', '[', '{'):
            depth += 1
        elif t == 'o' and v in (')', ']', '}'):
            depth -= 1
            if depth == 0:
                return start + 1, k
    return start + 1, len(toks)


NUM_KEY_RE = re.compile(r'^(?:0[xXbB][0-9a-fA-F_]+|[0-9][0-9_]*)$')


def extract_handlers(toks, body_start, body_end):
    """抽取顶层 [数字键] = value 元素，返回 [(key_int, key_raw, value_tokens, elem_start_idx)]"""
    # 找顶层逗号后的 [数字]= 作为元素边界
    bounds = [body_start]
    depth = 0
    for k in range(body_start, body_end):
        t, v = toks[k]
        if t == 'o' and v in ('(', '[', '{'):
            depth += 1
        elif t == 'o' and v in (')', ']', '}'):
            depth -= 1
        elif t == 'o' and v == ',' and depth == 0:
            # 逗号后紧跟 [ 数字 ]
            if (k + 3 < body_end and toks[k + 1] == ('o', '[') and
                    toks[k + 2][0] == 'n' and NUM_KEY_RE.fullmatch(toks[k + 2][1]) and
                    toks[k + 3] == ('o', ']')):
                bounds.append(k + 1)
    elems = []
    for bi, st in enumerate(bounds):
        en = bounds[bi + 1] - 1 if bi + 1 < len(bounds) else body_end  # 减去分隔逗号
        if st + 3 > en:
            continue
        if not (toks[st] == ('o', '[') and toks[st + 1][0] == 'n' and
                NUM_KEY_RE.fullmatch(toks[st + 1][1]) and toks[st + 2] == ('o', ']')):
            continue
        key_raw = toks[st + 1][1]
        key_int = parse_num(key_raw)
        if key_int is None:
            continue
        # 跳过 '='
        p = st + 3
        if p < en and toks[p] == ('o', '='):
            p += 1
        elems.append((key_int, key_raw, toks[p:en], st))
    return elems


def describe_value(vt):
    """把 handler 值概括成可读描述。"""
    v = [x for x in vt if x[0] != 'c']
    if not v:
        return '(空)'
    # 库["成员"] 形式
    if len(v) >= 4 and v[0][0] == 'w' and v[1] == ('o', '[') and v[2][0] == 's' and v[3] == ('o', ']'):
        raw = decode_string(v[2][1])
        member = raw.decode('ascii', 'replace') if raw and all(0x20 <= b <= 0x7E for b in raw) else v[2][1]
        return f'{v[0][1]}.{member}'
    if len(v) == 1 and v[0][0] == 'w':
        return v[0][1]
    if v[0][0] == 'w' and v[0][1] == 'function':
        # 参数个数
        depth, cnt = 0, 0
        for t, x in v[1:]:
            if t == 'o' and x == '(':
                depth += 1
                continue
            if t == 'o' and x == ')':
                break
            if depth == 1 and t == 'w':
                cnt += 1
        return f'function({cnt} 参数) …'
    if all(t == 'n' for t, _ in v):
        return '常量 ' + ' '.join(norm_num(x) for _, x in v)
    # 折叠后的常量表达式
    expr = ''.join(norm_num(x) if t == 'n' else x for t, x in v[:12])
    if len(expr) > 90:
        expr = expr[:90] + '…'
    return expr or '(复合表达式)'


# ---------------------------------------------------------------- 排版
BLOCK_OPEN = {'function', 'then', 'do', 'repeat'}
BLOCK_CLOSE = {'end', 'until'}
STMT_START = {'local', 'return', 'if', 'for', 'while', 'break', 'continue'}
TIGHT = {'(', ')', '[', ']', '{', '}', '.', ':', '::', ','}


def format_tokens(toks):
    lines = []
    cur = []
    indent = 0
    depth = 0            # 括号深度
    pending_fn = False   # function 参数列表尚未闭合
    fn_paren = 0
    force_break = [False]   # 上一个 token 是分号 → 下一个 token 必须新起一行
    brace = 0               # 花括号深度（只算 {}，不算 ()/[]）
    cur_indent = [0]        # 当前行的缩进级别（行首锁定）

    def flush(ind=None):
        nonlocal cur
        t = ''.join(cur).strip()
        if t:
            use = cur_indent[0] if ind is None else ind
            lines.append('    ' * min(max(use, 0), 16) + t)
        cur = []

    prev = None
    cur_indent[0] = 0

    for typ, v in toks:
        # 行首锁定缩进：cur 为空 = 即将开始新行
        if not cur and typ != 'c':
            # 块结束关键字（end/until）要先减一级
            lv = indent - 1 if (typ == 'w' and v in BLOCK_CLOSE) else indent
            cur_indent[0] = max(0, lv + max(0, brace))
        if force_break[0] and typ != 'c':
            flush()
            force_break[0] = False
        if typ == 'c':
            flush()
            lines.append('    ' * min(max(indent, 0), 16) + v)
            prev = None
            continue

        if typ == 'o':
            if v in ('(', '[', '{'):
                depth += 1
                if v == '{':
                    brace += 1
                if pending_fn and v == '(':
                    fn_paren += 1
            elif v in (')', ']', '}'):
                depth -= 1
                if v == '}':
                    brace = max(0, brace - 1)
            if v in TIGHT and v != ',':
                cur.append(v)
                prev = 'tight'
                # function 参数列表闭合 -> 换行并进入块
                if pending_fn and v == ')':
                    fn_paren -= 1
                    if fn_paren == 0:
                        flush()
                        indent += 1
                        pending_fn = False
                continue
            if v == ',':
                cur.append(',')
                # 表/参数列表里每个元素一行。depth 跟踪的是所有括号，
                # 这里只在「当前行已经有内容」时断行，避免空行。
                if brace >= 1 and cur:
                    flush()
                prev = 'tight'
                continue
            if v == ';':
                # 分号在 Lua 里只是可选语句分隔符。改成断行（语义等价）。
                # 注意 flush() 只把累积内容推成一行，若此时 cur 为空
                # （例如前一个 token 刚闭合大括号），就必须补一个空标记，
                # 否则下一个 token 会接着上一次的 flush 结果拼在同一行。
                flush()
                force_break[0] = True
                prev = None
                continue
            # 单目运算符：不加右侧空格
            if v in ('#', '-', '~') and prev in (None, 'op', 'tight', 'stmt', '('):
                cur.append(v)
                prev = 'op'
                continue
            cur.append(' ' + v + ' ')
            prev = 'op'
            continue

        # word / number / string
        if typ == 'w' and v in BLOCK_CLOSE:
            flush()
            indent -= 1
            cur_indent[0] = max(0, indent + max(0, brace))
            cur.append(v)
            flush()
            prev = 'w'
            continue
        if typ == 'w' and v in ('else', 'elseif'):
            flush()
            indent -= 1
            cur_indent[0] = max(0, indent + max(0, brace))
            cur.append(v + ' ')
            if v == 'else':
                flush()
                indent += 1
            prev = 'stmt'
            continue
        if typ == 'w' and v in STMT_START:
            # Luau 支持 if 表达式，关键字可能出现在表达式中间；
            # 这里只保证与前一个 token 有分隔，绝不强行断行（断行会丢 token）。
            if cur and not cur[-1].endswith(' '):
                cur.append(' ')
            cur.append(v + ' ')
            prev = 'stmt'
            continue
        if typ == 'w' and v == 'function':
            if prev in ('w', 'n', 's'):
                cur.append(' ')
            cur.append(v)
            pending_fn = True
            fn_paren = 0
            prev = 'w'
            continue
        if typ == 'w' and v in BLOCK_OPEN:
            if prev in ('w', 'n', 's'):
                cur.append(' ')
            cur.append(v)
            flush()
            indent += 1
            prev = 'w'
            continue

        if prev in ('w', 'n', 's', 'stmt') and (not cur or not cur[-1].endswith(' ')):
            cur.append(' ')
        cur.append(v)
        prev = typ

    flush()
    # 把独占一行的分隔逗号并回上一行，避免 `end` / `,` 分成两行
    merged = []
    for line in lines:
        if line.strip() == ',' and merged:
            merged[-1] += ','
        else:
            merged.append(line)
    return '\n'.join(merged)


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser(description='Luraph v15.1 静态反混淆增强版')
    ap.add_argument('input')
    ap.add_argument('-o', '--output', required=True)
    ap.add_argument('--map', default=None, help='导出 handler 映射表 (markdown)')
    ap.add_argument('--no-rename', action='store_true', help='不做变量语义重命名')
    args = ap.parse_args()

    src = Path(args.input).read_text(encoding='utf-8', errors='ignore')
    toks = tokenize(src)
    print(f'[1] 词法: {len(toks):,} tokens')

    # 数字归一化 + 字符串解码
    toks = [(t, norm_num(v) if t == 'n' else (reencode_string(v) if t == 's' else v))
            for t, v in toks]
    print('[2] 数字归一化 + 字符串转义解码完成')

    toks = fold_consts(toks)
    print(f'[3] 常量折叠完成: {len(toks):,} tokens')

    # 变量重命名（复用仓库 readable3）
    if not args.no_rename:
        try:
            from libs.readable3 import rename as do_rename
            toks = do_rename(toks)
            print('[4] 语义重命名完成 (libs/readable3.py)')
        except Exception as e:
            print(f'[4] 重命名跳过: {e}')
    else:
        print('[4] 按参数跳过重命名')

    # 定位顶层 setmetatable({...}, {}) 的 handler 表
    tbl_start = None
    for i, (t, v) in enumerate(toks):
        if t == 'w' and v == 'setmetatable':
            for k in range(i + 1, min(i + 5, len(toks))):
                if toks[k] == ('o', '('):
                    if k + 1 < len(toks) and toks[k + 1] == ('o', '{'):
                        tbl_start = k + 1
                    break
            if tbl_start is not None:
                break

    # 统计各数字索引在正文（形如 V[key]）中被引用的次数
    import collections
    ref = collections.Counter()
    for i in range(len(toks) - 2):
        if toks[i][0] == 'w' and toks[i + 1] == ('o', '[') and toks[i + 2][0] == 'n':
            v = parse_num(toks[i + 2][1])
            if v is not None:
                ref[v] += 1

    handlers = []
    if tbl_start is not None:
        bs, be = find_table_body(toks, tbl_start)
        handlers = extract_handlers(toks, bs, be)
        print(f'[5] handler 表: 定位到 {bs}..{be}，抽取 {len(handlers)} 个顶层条目')

        # 由后往前插入注释，避免索引偏移
        inserts = []
        for key_int, key_raw, vt, st in handlers:
            desc = describe_value(vt)
            inserts.append((st, ('c', f'-- [{key_int}] = {desc}')))
        for st, ct in sorted(inserts, key=lambda x: -x[0]):
            toks.insert(st, ct)
    else:
        print('[5] 未定位到顶层 handler 表，跳过映射标注')

    out_text = format_tokens(toks)
    Path(args.output).write_text(out_text + '\n', encoding='utf-8')
    print(f'[6] 输出: {args.output}  ({len(out_text):,} 字节, {len(out_text.splitlines()):,} 行)')

    # 无损性校验：重新词法化，比较非注释 token
    re_toks = [x for x in tokenize(out_text) if x[0] != 'c']
    orig_toks = [x for x in toks if x[0] != 'c']
    if re_toks == orig_toks:
        print('[7] 无损性校验通过：token 序列与变换后完全一致（未破坏语法）')
    else:
        print(f'[7] 警告: token 数 {len(re_toks)} vs {len(orig_toks)}，请人工检查')

    if args.map and handlers:
        rows = ['# Luraph v15.1 handler 映射表', '',
                f'共 {len(handlers)} 个顶层条目。key 已归一化为十进制，便于在代码中检索 `V[<key>]`。', '',
                '说明：`V[大数字]` 是查 handler 表；`V[0]`~`V[200]` 一类小索引是 VM 寄存器 / 栈槽，不属于本表。', '',
                '| key (十进制) | 原始键字面量 | 含义 / 值 | 正文引用次数 |',
                '| ---: | --- | --- | ---: |']
        for key_int, key_raw, vt, _ in sorted(handlers):
            desc = describe_value(vt).replace('|', '\\|')
            rows.append(f'| {key_int} | `{key_raw}` | {desc} | {ref.get(key_int, 0)} |')
        Path(args.map).write_text('\n'.join(rows) + '\n', encoding='utf-8')
        print(f'[8] 映射表: {args.map}')


if __name__ == '__main__':
    main()
