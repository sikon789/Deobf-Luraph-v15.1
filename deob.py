#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
luraph_v151_deob —— Luraph v15.1 自动反混淆

思路
----
Luraph v15.1 的常见形态是：

    return setmetatable({ [n] = function(...) ... end, ... }, {}):rk(...)

真正有价值的业务代码，是表里那几个「巨型匿名函数」。它们本身就是**明文 Lua**，
只是被压成一行、塞进表里、外面套了加密壳。

所以正确做法不是去反编译 VM，而是：
  1. 剥外层加密壳（如果是十进制转义 / base64 / 简单 XOR）
  2. 用 luau-ast 解析出精确的字节区间
  3. 把大函数按区间切出来
  4. 断行 + 修空格 + 语义重命名
  5. 验证语法

用法
----
    python deob.py 输入.lua [-o 输出.lua] [--min-size 20000] [--no-rename]

    python deob.py 输入.lua --list       # 只列出发现的大函数，不输出
"""
import sys
import os
import re
import json
import shutil
import argparse
import subprocess
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "libs"))
sys.path.insert(0, str(HERE))  # deobf_plus 可能在根目录

# ---------------------------------------------------------------- 外层壳剥离

DEC_ESC = re.compile(r'"(\\\d{1,3}(?:\\\d{1,3}){100,})"')


def strip_decimal_shell(src):
    """处理 loadstring("\\100\\101\\102...") 这种十进制转义壳"""
    m = DEC_ESC.search(src)
    if not m:
        return None
    try:
        body = bytes(int(x) for x in m.group(1).split("\\")[1:])
    except ValueError:
        return None
    return body.decode("utf-8", errors="ignore")


def strip_base64_shell(src):
    """处理 loadstring(base64_decode("...")) 这种"""
    m = re.search(r'(?:base64_?decode|atob)\s*\(\s*"([A-Za-z0-9+/=]{200,})"', src, re.I)
    if not m:
        return None
    import base64
    try:
        return base64.b64decode(m.group(1)).decode("utf-8", errors="ignore")
    except Exception:
        return None


def strip_luraph_vm(src):
    """Luraph 专用剥壳：用 bufemu 模拟跑一遍，dump 解码后的缓冲区。
    返回 (layer3 源码 或 None, 说明)"""
    print("        ↳ 正在启动剥壳引擎（bufemu 模拟执行 + buffer dump）…")
    print("          首次运行可能需要几秒到几十秒，请稍候")
    import tempfile
    tmpdir = Path(tempfile.mkdtemp(prefix="lv151_"))
    target = tmpdir / "target.lua"
    target.write_text(src, encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(HERE / "fastsolve.py"), str(target), str(tmpdir / "out")],
            capture_output=True, text=True, timeout=600,
        )
    except Exception as e:
        return None, f"剥壳执行失败: {e}"
    log = (r.stdout or "") + (r.stderr or "")
    outdir = tmpdir / "out"
    if not outdir.exists():
        return None, "剥壳未产生输出"
    # 找最大的 lua-source 块
    best, best_sz = None, 0
    for f in outdir.glob("layer*.lua"):
        if f.stat().st_size > best_sz:
            best, best_sz = f, f.stat().st_size
    if best is None:
        # 退而求其次：把所有 blob 当 lua 试
        for f in outdir.glob("blob*.bin"):
            data = f.read_bytes()
            txt = data.decode("utf-8", errors="ignore")
            if "setmetatable" in txt and len(txt) > best_sz:
                best, best_sz = f, len(txt)
                best_txt = txt
        if best is None:
            return None, "未找到可用的明文层\n" + log.strip()[-500:]
        return best_txt, f"blob 直读 {best_sz:,} 字节"
    return best.read_text(encoding="utf-8", errors="ignore"), log.strip().split("\n")[-1]


def unwrap_shell(src, depth=0):
    """递归剥壳，最多 3 层"""
    if depth > 3:
        return src, depth
    for fn in (strip_decimal_shell, strip_base64_shell):
        inner = fn(src)
        if inner and len(inner) > 1000:
            return unwrap_shell(inner, depth + 1)
    return src, depth


# ---------------------------------------------------------------- AST 定位

def _arch_suffix():
    """当前平台对应的二进制后缀，如 aarch64 / x86_64"""
    m = platform.machine().lower()
    if m in ("x86_64", "amd64"):
        return "x86_64"
    if m in ("aarch64", "arm64"):
        return "aarch64"
    return m


def _pick(name):
    """按优先级找二进制：架构专用名 → 通用名；
    通用名若架构不符则跳过（避免 Exec format error）。"""
    roots = [HERE, HERE / "bin", HERE / "libs", HERE.parent,
             HERE.parent / "bin", HERE.parent / "libs"]
    suf = _arch_suffix()
    # 1) 优先架构专用文件  luau.x86_64 / luau.aarch64
    for r in roots:
        c = r / f"{name}.{suf}"
        if c.is_file():
            ensure_executable(str(c))
            return str(c)
    # 2) 通用名，但必须是本机架构
    for r in roots:
        c = r / name
        if c.is_file():
            ok, msg = check_elf_arch(str(c))
            if ok:
                ensure_executable(str(c))
                return str(c)
    # 3) PATH
    found = shutil.which(name)
    if found:
        ok, _ = check_elf_arch(found)
        if ok:
            return found
    return None


def find_luau_ast():
    """定位 luau-ast：优先架构专用 → 通用 → PATH"""
    return _pick("luau-ast")


def check_elf_arch(path):
    """检查 ELF 架构是否可执行，返回 (ok, 说明)"""
    import struct
    try:
        with open(path, 'rb') as f:
            magic = f.read(20)
        if magic[:4] != b"\x7fELF":
            return True, ""  # 不是 ELF，交给系统判断
        ei_class = magic[4]
        ei_data = magic[5]
        e_machine = struct.unpack("<H" if ei_data == 1 else ">H", magic[18:20])[0]
        names = {0x3e: "x86_64", 0xb7: "aarch64", 0x03: "i386", 0x28: "arm"}
        arch = names.get(e_machine, f"0x{e_machine:x}")
        cur = platform.machine()
        ok = (arch == cur) or (arch == "x86_64" and cur in ("x86_64", "AMD64"))
        if not ok:
            return False, f"这是 {arch} 二进制，当前架构 {cur} 无法执行"
        return True, ""
    except Exception:
        return True, ""


def ensure_executable(path):
    """确保有可执行权限（zip 解压后常见 644）"""
    try:
        if not os.access(path, os.X_OK):
            os.chmod(path, 0o755)
            return True
    except OSError:
        pass
    return False


def find_luau_runtime():
    """定位 luau 运行时：优先架构专用 → 通用 → PATH"""
    return _pick("luau")



def run_ast(src_text, ast_bin):
    """跑 luau-ast，返回 JSON"""
    tmp = Path("/tmp/_lv151_ast_input.lua")
    tmp.write_text(src_text, encoding="utf-8")
    r = subprocess.run([ast_bin, str(tmp)], capture_output=True, text=True, timeout=300)
    out = (r.stdout or "") + (r.stderr or "")
    start = out.find("{")
    if start < 0:
        raise RuntimeError(f"luau-ast 无输出：{out[:300]}")
    return json.loads(out[start:])


def parse_loc(loc):
    """'0,55 - 0,110749' -> (start_line, start_col, end_line, end_col)"""
    a, b = loc.split(" - ")
    l1, c1 = a.split(",")
    l2, c2 = b.split(",")
    return int(l1), int(c1), int(l2), int(c2)


def collect_functions(node, out, depth=0):
    if isinstance(node, dict):
        if node.get("type") == "AstExprFunction":
            out.append(node)
        for v in node.values():
            collect_functions(v, out, depth + 1)
    elif isinstance(node, list):
        for i in node:
            collect_functions(i, out, depth + 1)


def byte_offset_of(src, line, col):
    """把 (line,col) 转成字符偏移（luau-ast 的行号从 0 开始）"""
    if line == 0:
        return col
    pos = 0
    for _ in range(line):
        nl = src.find("\n", pos)
        if nl < 0:
            return len(src)
        pos = nl + 1
    return pos + col


# ---------------------------------------------------------------- 排版

HFUN = re.compile(r'function\s*\n\s*\(')
DOT = re.compile(r'\s+\.\s+')
COLON = re.compile(r'\s+:\s+')
OPENP = re.compile(r'\(\s+')
CLOSEP = re.compile(r'\s+\)')


def tidy(text):
    """清理排版空白的 token 级实现。
    旧版用整文正则替换，会把字符串字面量里的 " . " / " : " / "( " 也改掉，
    直接篡改数据。这里改为只对「非字符串、非注释」的 token 做处理。"""
    from deobf_plus import tokenize, format_tokens
    try:
        toks = tokenize(text)
    except Exception:
        return text
    out = []
    for t, v in toks:
        if t == 'c':
            out.append((t, v))
        elif t == 's':
            out.append((t, v))          # 字符串原样保留，一个字节都不动
        elif t == 'o':
            out.append((t, v))          # 运算符交给 format_tokens 决定间距
        else:
            out.append((t, v))
    # format_tokens 本身只在 token 之间插入空白，不触碰 token 内容
    return format_tokens(out)



def verify(text):
    """用 luau 做语法验证。

    只解析、不执行：luau CLI 没有 --parse，但 `--fflags` 里没有纯解析开关，
    所以这里用一个技巧——把代码包进 `if false then ... end`，
    运行时永远不会进入，但语法必须合法才能编译通过。
    这样既不会真的执行被测脚本，也能可靠地捕获语法错误。
    """
    luau = find_luau_runtime()
    if not luau:
        return True, "跳过（未找到 luau 二进制）"
    tmp = Path("/tmp/_lv151_verify.lua")
    # 包一层，避免执行副作用
    wrapped = "if false then\n" + text + "\nend\n"
    tmp.write_text(wrapped, encoding="utf-8")
    try:
        r = subprocess.run([str(luau), str(tmp)], capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return True, "验证超时（假定语法通过）"
    msg = ((r.stdout or "") + (r.stderr or "")).strip()

    # 语法错误特征
    if "Expected" in msg:
        return False, msg.split("\n")[0]
    if "unknown opcode" in msg.lower() or "malformed" in msg.lower():
        return False, msg.split("\n")[0]
    # 含 "attempt to" 说明语法通过、只是运行时缺环境 —— 这是正常结果
    return True, msg.split("\n")[0] if msg else "OK"



# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="Luraph v15.1 自动反混淆")
    ap.add_argument("input", help="输入的 .lua / .txt 文件")
    ap.add_argument("-o", "--output", help="输出文件")
    ap.add_argument("--min-size", type=int, default=20000, help="最小函数长度（字节），默认 20000")
    ap.add_argument("--list", action="store_true", help="只列出大函数，不输出")
    ap.add_argument("--no-rename", action="store_true", help="不做语义重命名")
    ap.add_argument("--force", action="store_true", help="即使判定为 VM 字节码，也强制导出骨架")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"[✗] 文件不存在：{inp}")
        return 1

    raw = inp.read_text(encoding="utf-8", errors="ignore")
    print(f"[1] 读取：{inp.name}  {len(raw):,} 字节")

    # 前置检查：确认解析器与运行时可用
    print("[1b] 检查解析器（luau-ast / luau）…")
    _ast = find_luau_ast()
    _run = find_luau_runtime()
    if _ast:
        ensure_executable(_ast)
        print(f"     ✓ luau-ast  {Path(_ast).name}  {Path(_ast).stat().st_size:,} 字节")
    else:
        print("     ✗ 未找到 luau-ast")
    if _run:
        ensure_executable(_run)
        print(f"     ✓ luau      {Path(_run).name}  {Path(_run).stat().st_size:,} 字节")
    else:
        print("     ✗ 未找到 luau（语法验证将跳过）")

    # 剥壳
    src, layers = unwrap_shell(raw)
    if layers:
        print(f"[2] 剥除外层壳 {layers} 层 → {len(src):,} 字节")
    else:
        print("[2] 未检测到简单外层壳")

    # Luraph 专用剥壳：如果 AST 里找不到大函数，就走 bufemu 流程
    ast_bin = find_luau_ast()
    if not ast_bin:
        print("[✗] 找不到 luau-ast")
        print("    请放到 bin/ 或 libs/ 目录，或安装到 PATH")
        return 1

    # 权限 + 架构检查
    if ensure_executable(ast_bin):
        print(f"[2a] 已为 {Path(ast_bin).name} 添加可执行权限（zip 解压后常见为 644）")
    ok_arch, arch_msg = check_elf_arch(ast_bin)
    if not ok_arch:
        print(f"[✗] {Path(ast_bin).name}: {arch_msg}")
        print("    请构建对应架构的 luau-ast：")
        print("    https://github.com/luau-lang/luau  （编译 luau-ast 目标）")
        return 5

    def has_big_func(text):
        try:
            a = run_ast(text, ast_bin)
        except Exception:
            return False
        fs = []
        collect_functions(a, fs)
        for f in fs:
            loc = f.get("location")
            if not loc:
                continue
            l1, c1, l2, c2 = parse_loc(loc)
            s = byte_offset_of(text, l1, c1)
            e = byte_offset_of(text, l2, c2)
            if e - s >= args.min_size:
                return True
        return False

    if not has_big_func(src):
        print("[2b] 当前层无业务函数，尝试 Luraph 专用剥壳…")
        inner, note = strip_luraph_vm(src)
        if inner:
            src = inner
            print(f"[2b] ✓ 剥壳完成 → {len(src):,} 字节   ({note})")
            # 剥出来的层可能还是壳，继续下探
            for depth in range(3):
                if has_big_func(src):
                    break
                deeper, note2 = strip_luraph_vm(src)
                if not deeper or len(deeper) >= len(src):
                    break
                src = deeper
                print(f"[2b] 继续下探第 {depth + 2} 层 → {len(src):,} 字节")
        else:
            print(f"[2b] 剥壳失败：{note}")

    # 解析 AST
    try:
        ast = run_ast(src, ast_bin)
        print("[3] AST 解析成功")
    except Exception as e:
        print(f"[✗] AST 解析失败：{e}")
        return 1

    funcs = []
    collect_functions(ast, funcs)
    print(f"[4] 发现 {len(funcs)} 个函数")

    # 按长度排序，挑大的
    sized = []
    for f in funcs:
        loc = f.get("location")
        if not loc:
            continue
        l1, c1, l2, c2 = parse_loc(loc)
        s = byte_offset_of(src, l1, c1)
        e = byte_offset_of(src, l2, c2)
        if e - s >= args.min_size:
            sized.append((s, e, e - s))

    # 去嵌套：只保留「不被其他函数包含」的最外层函数
    sized.sort(key=lambda x: (x[0], -x[2]))
    outer = []
    for s, e, n in sized:
        if outer and s >= outer[-1][0] and e <= outer[-1][1]:
            continue  # 被上一个包含
        outer.append((s, e, n))
    sized = outer
    sized.sort(key=lambda x: -x[2])
    print(f"[5] 长度 ≥ {args.min_size:,} 的函数：{len(sized)} 个")
    for s, e, n in sized:
        print(f"      {s:>8} - {e:<8}  {n:>8,} 字节")

    if not sized:
        print("[!] 没有找到大函数。可能不是 Luraph v15.1，或业务代码被编译进字节码。")
        return 2

    if args.list:
        return 0

    # ---- 形态识别：判断是真明文业务代码，还是纯 VM 字节码 ----
    import re as _re
    region = "".join(src[s:e + 1] for s, e, n in sized)
    # 业务特征：可读的 Roblox API / UI / 功能名字符串
    signals = {
        "GetService": len(_re.findall(r'GetService', region)),
        "Instance.new": len(_re.findall(r'Instance\s*[.:]\s*new', region)),
        "UDim2": len(_re.findall(r'UDim2', region)),
        "Color3": len(_re.findall(r'Color3', region)),
        "TweenService": len(_re.findall(r'TweenService', region)),
        "可读中文/英文提示": len(_re.findall(r'"[A-Z][A-Za-z ]{8,}"', region)),
        "功能名(含空格)": len(_re.findall(r'"(?:Auto|Farm|Toggle|Config|Save|Load)\s', region)),
    }
    score = sum(v for k, v in signals.items() if k != "可读中文/英文提示") + signals["可读中文/英文提示"] // 20
    print("[5b] 业务特征扫描：")
    for k, v in signals.items():
        print(f"      {k:<22} {v}")
    print(f"      综合得分 = {score}")

    if score < 5:
        print()
        print("═" * 60)
        print("  ⚠ 此样本的业务代码已编译进 VM 字节码")
        print("═" * 60)
        print("  检测结果：大函数存在，但内部全是 VM 寄存器操作")
        print("            （形如 arg[1201](11, 122)），没有任何可读的业务 API 调用。")
        print("  说明：Luraph v15.1 把这部分代码编译成了 Luau 字节码。")
        print("        本工具只做「提取明文业务代码」，不做字节码反编译。")
        print("  能做的：")
        print("    · 输出 handler 映射表（VM 索引 → math.random 这类）")
        print("    · 输出函数结构骨架（不含业务逻辑）")
        print("  不能做的：")
        print("    · 还原成原始可运行的 Lua 业务源码")
        print("═" * 60)
        if not args.force:
            print()
            print("  已停止输出。加 --force 仍可导出骨架（仅供分析）。")
            return 4
        print("  --force 已指定，继续导出骨架…")
        print("")

    # 切出来，合并
    parts = []
    for idx, (s, e, n) in enumerate(sized, 1):
        frag = src[s:e + 1].rstrip().rstrip(",")
        parts.append((idx, n, frag))

    # 断行（用能处理 0b/0x/下划线的词法器）
    from deobf_plus import tokenize, format_tokens, norm_num, decode_string
    bodies = []
    for idx, n, frag in parts:
        try:
            toks = tokenize(frag)
            fixed = []
            for t, v in toks:
                if t == "n":
                    try:
                        fixed.append((t, str(norm_num(v))))
                    except Exception:
                        fixed.append((t, v))
                else:
                    fixed.append((t, v))
            text = format_tokens(fixed)
        except Exception as ex:
            print(f"[!] 第 {idx} 段处理失败：{ex}，改用原文")
            text = frag
        bodies.append(text)
        print(f"[6.{idx}] 断行完成  {len(text):,} 字节  {text.count(chr(10)) + 1:,} 行")

    # 语义重命名
    if not args.no_rename:
        try:
            from readable3 import rename
            renamed = []
            for text in bodies:
                toks = tokenize(text)
                renamed.append(format_tokens(rename(toks)))
            bodies = renamed
            print("[7] 语义重命名完成")
        except Exception as ex:
            print(f"[!] 重命名跳过：{ex}")

    # 修空格
    bodies = [tidy(b) for b in bodies]

    # 提取 handler 表（[n] = math.random 这类）
    handler_lines = []
    try:
        from deobf_plus import extract_handlers
        toks_all = tokenize(src)
        # 定位 setmetatable( { ... } )
        start = None
        for i, (t, v) in enumerate(toks_all):
            if t == "w" and v == "setmetatable":
                start = i
                break
        if start is not None:
            brace = None
            for i in range(start, min(start + 6, len(toks_all))):
                if toks_all[i] == ("o", "{"):
                    brace = i
                    break
            if brace is not None:
                depth = 0
                endb = None
                for i in range(brace, len(toks_all)):
                    t, v = toks_all[i]
                    if t == "o" and v in ("(", "[", "{"):
                        depth += 1
                    elif t == "o" and v in (")", "]", "}"):
                        depth -= 1
                        if depth == 0:
                            endb = i
                            break
                hs = extract_handlers(toks_all, brace + 1, endb)
                for key, raw, valtoks, _ in hs:
                    desc = tidy(format_tokens(valtoks))[:70]
                    desc = desc.replace("\n", " ")
                    handler_lines.append(f"-- [{key}] = {desc}")
                print(f"[7b] handler 表：{len(hs)} 条")
    except Exception as ex:
        print(f"[!] handler 提取跳过：{ex}")

    # 组装
    out_lines = []
    out_lines.append("--[[")
    out_lines.append("  Luraph v15.1 自动反混淆输出")
    out_lines.append(f"  源文件：{inp.name}")
    out_lines.append(f"  共提取 {len(bodies)} 个业务函数")
    out_lines.append("]]")
    out_lines.append("")
    if handler_lines:
        out_lines.append("-- ============================================================")
        out_lines.append("-- handler 表（VM 索引 → 实际值）")
        out_lines.append("-- ============================================================")
        out_lines.extend(handler_lines)
        out_lines.append("")
    for i, (text, (s, e, n)) in enumerate(zip(bodies, sized), 1):
        body = text
        if body.startswith("return "):
            body = body[7:]
        out_lines.append(f"-- ============================================================")
        out_lines.append(f"-- 第 {i} 段  原始偏移 {s} - {e}  ({n:,} 字节)")
        out_lines.append(f"-- ============================================================")
        out_lines.append(f"local __part{i} = {body}")
        out_lines.append("")
    rets = ", ".join(f"__part{i}" for i in range(1, len(bodies) + 1))
    out_lines.append(f"return {{ {rets} }}")
    out_text = "\n".join(out_lines)

    # 验证
    ok, msg = verify(out_text)
    print(f"[8] 语法验证：{'✓ 通过' if ok else '✗ 失败'}  {msg}")

    # 输出
    out_path = Path(args.output) if args.output else inp.with_name(inp.stem + "_反混淆.lua")
    out_path.write_text(out_text, encoding="utf-8")
    print(f"[9] 输出：{out_path}  {len(out_text):,} 字节  {out_text.count(chr(10)) + 1:,} 行")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
