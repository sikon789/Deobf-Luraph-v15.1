#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_release.py —— 生成 Release 需要的独立附件

GitHub 的 Release 附件必须是单独文件，不能是 zip 里的成员。
（zip 里的文件下载后要解压，fetch_bin.py 没法直接用。）

所以把 bin/ 下每个架构的二进制单独准备成 <name>.<arch>，
放进 out_release/，直接拖到 Release 页面上传即可。

用法:
    python make_release.py              # 生成当前架构 + 所有已有架构
    python make_release.py --tag v1.3.0 # 同时打印上传说明
"""
import sys
import shutil
import struct
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = HERE / "bin"
OUT = HERE / "out_release"
REPO = "sikon789/Deobf-Luraph-v15.1"


def elf_arch(path):
    with open(path, "rb") as f:
        hdr = f.read(20)
    if hdr[:4] != b"\x7fELF":
        return "unknown"
    m = struct.unpack("<H", hdr[18:20])[0]
    return {0x3E: "x86_64", 0xB7: "aarch64", 0x03: "i386", 0x28: "arm"}.get(m, f"0x{m:x}")


def main():
    tag = "v1.3.0"
    for i, a in enumerate(sys.argv):
        if a == "--tag" and i + 1 < len(sys.argv):
            tag = sys.argv[i + 1]

    if not BIN.is_dir():
        print(f"[错误] 没有 {BIN} 目录")
        return 1

    files = sorted(p for p in BIN.iterdir() if p.is_file() and not p.name.startswith("."))
    if not files:
        print("[错误] bin/ 是空的，先跑 python fetch_bin.py 或 build_x86.py")
        return 1

    OUT.mkdir(exist_ok=True)
    for f in OUT.iterdir():
        if f.is_file():
            f.unlink()

    print(f"[信息] 当前平台 {platform.machine()}")
    total = 0
    for f in files:
        arch = elf_arch(f)
        base = f.name.split(".")[0]           # luau / luau-ast
        dest = OUT / f"{base}.{arch}"         # 统一成 <name>.<arch>
        if dest.exists() and dest != f:
            print(f"[跳过] {dest.name} 已存在")
            continue
        shutil.copy2(f, dest)
        sz = dest.stat().st_size
        total += sz
        print(f"[生成] {dest.name:<22} {sz:>12,} 字节  ({arch})")

    print(f"\n[汇总] {len(list(OUT.iterdir()))} 个文件，共 {total:,} 字节")
    print(f"[位置] {OUT}\n")
    print("=" * 66)
    print("上传步骤（GitHub 网页）")
    print("=" * 66)
    print(f"""
1. 打开 https://github.com/{REPO}/releases/new
2. 选 tag:  {tag}      （没有就新建）
3. 标题:    Luraph v15.1 Deob Tool {tag}
4. 把 out_release/ 里的文件全部拖进「Attach binaries」框
5. 发布

fetch_bin.py 会按下面的地址取：
  https://github.com/{REPO}/releases/download/{tag}/luau.aarch64
  https://github.com/{REPO}/releases/download/{tag}/luau-ast.aarch64
  https://github.com/{REPO}/releases/download/{tag}/luau.x86_64
  https://github.com/{REPO}/releases/download/{tag}/luau-ast.x86_64

名字必须一模一样（<程序名>.<架构>），否则下载会 404。

仓库本体保持轻量：
  - bin/ 已写进 .gitignore
  - 只提交 .py / .md / .lua 代码，约 100 KB
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
