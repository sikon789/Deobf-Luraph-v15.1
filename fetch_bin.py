#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_bin.py —— 按需下载 luau / luau-ast 二进制

二进制不进 Git 仓库（体积大、和版本无关），改为首次运行时从
GitHub Release 拉取，之后缓存在 bin/ 里。这样仓库只有 ~100 KB。

用法:
    python fetch_bin.py             # 下载当前架构所需二进制
    python fetch_bin.py --check     # 只看现在有什么、缺什么
    python fetch_bin.py --force     # 强制重新下载
    python fetch_bin.py --url URL   # 用自定义源（镜像 / 自建服务器）

环境变量:
    LUAU_BIN_URL     覆盖下载源前缀，默认 GitHub Release
    LUAU_BIN_MIRROR  镜像前缀（内地用，如 https://ghproxy.net/）

被 deob.py 自动调用，一般不用手动跑。
"""
import os
import sys
import shutil
import platform
import subprocess
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = HERE / "bin"

# Release 地址。换版本时改这两行即可
REPO = "sikon789/Deobf-Luraph-v15.1"
TAG = "v1.3.0"

# 文件清单：仓库内名字 → (Release 附件名)
ARTIFACTS = ["luau", "luau-ast"]

# 默认镜像（内地直连 GitHub 常超时）
DEFAULT_MIRRORS = [
    "https://ghproxy.net/https://github.com/{repo}/releases/download/{tag}/{name}",
    "https://github.com/{repo}/releases/download/{tag}/{name}",
]


def say(stage, msg):
    print(f"[{stage}] {msg}", flush=True)


def arch_suffix():
    m = platform.machine().lower()
    if m in ("x86_64", "amd64"):
        return "x86_64"
    if m in ("aarch64", "arm64"):
        return "aarch64"
    return m


def elf_arch(path):
    """返回 (ok_for_this_machine, 架构名)。非 ELF 视为 python 脚本，放行。"""
    try:
        with open(path, "rb") as f:
            hdr = f.read(20)
    except OSError:
        return False, "读不到"
    if hdr[:4] != b"\x7fELF":
        return True, "非ELF"
    e_machine = struct.unpack("<H", hdr[18:20])[0]
    names = {0x3E: "x86_64", 0xB7: "aarch64", 0x03: "i386", 0x28: "arm"}
    got = names.get(e_machine, f"0x{e_machine:x}")
    return got == arch_suffix(), got


def check(path):
    """检查某个现有文件是否可用"""
    p = Path(path)
    if not p.is_file():
        return False, "不存在"
    if p.stat().st_size < 1000:
        return False, f"只有 {p.stat().st_size} 字节，像是占位文件"
    ok, got = elf_arch(str(p))
    if not ok:
        return False, f"架构是 {got}，不是 {arch_suffix()}"
    if not os.access(str(p), os.X_OK):
        try:
            p.chmod(0o755)
        except OSError:
            return False, "不可执行且无法改权限"
    return True, got


def resolve(name):
    """找已存在的可用二进制：先带后缀，再通用名"""
    suf = arch_suffix()
    for cand in (BIN / f"{name}.{suf}", BIN / name, HERE / f"{name}.{suf}", HERE / name):
        ok, why = check(cand)
        if ok:
            return cand
    return None


def try_system(name):
    """退路：PATH 里的同名程序（如 pip/apt 装的 luau）"""
    found = shutil.which(name)
    if not found:
        return None
    ok, _ = elf_arch(found)
    return Path(found) if ok else None


def download(url, dest):
    cmd = ["curl", "-fsSL", "--max-time", "300", "--retry", "2",
           "-o", str(dest), url]
    if not shutil.which("curl"):
        cmd = ["wget", "-q", "-T", "300", "-O", str(dest), url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not dest.exists() or dest.stat().st_size < 1000:
        err = (r.stderr or r.stdout or "").strip().split("\n")[-1]
        say("失败", f"{url[:60]}…  {err[:80]}")
        return False
    say("完成", f"{url[:60]}…  {dest.stat().st_size:,} 字节")
    return True


def fetch(name, force=False, custom_url=None):
    suf = arch_suffix()
    if not force:
        got = resolve(name)
        if got:
            say("缓存", f"{name} 已就绪 → {got.name}（{got.stat().st_size:,} 字节）")
            return str(got)

    BIN.mkdir(exist_ok=True)
    tmp = BIN / f".{name}.{suf}.part"
    asset = f"{name}.{suf}"

    if custom_url:
        candidates = [custom_url.rstrip("/") + "/" + asset]
    else:
        env = os.environ.get("LUAU_BIN_URL")
        if env:
            candidates = [env.rstrip("/") + "/" + asset]
        else:
            tmpl = os.environ.get("LUAU_BIN_MIRROR")
            if tmpl:
                candidates = [tmpl.rstrip("/") + "/"
                              f"https://github.com/{REPO}/releases/download/{TAG}/{asset}"]
            else:
                candidates = [t.format(repo=REPO, tag=TAG, name=asset)
                              for t in DEFAULT_MIRRORS]

    for url in candidates:
        if download(url, tmp):
            dest = BIN / f"{name}.{suf}"
            shutil.move(str(tmp), str(dest))
            dest.chmod(0o755)
            ok, why = check(dest)
            if ok:
                say("完成", f"{dest.name}  {dest.stat().st_size:,} 字节  ✓")
                return str(dest)
            say("警告", f"下载到的文件不可用（{why}）")
            dest.unlink(missing_ok=True)

    # 下载失败 → 退路
    tmp.unlink(missing_ok=True)
    sysb = try_system(name)
    if sysb:
        say("退路", f"用系统 PATH 里的 {sysb}")
        return str(sysb)

    say("失败", f"{name} 下载不到，本地也没有可用的")
    print(f"""
三个办法任选一个：

  1) 换镜像手动下载
     curl -L --max-time 300 -o bin/{name}.{suf} \\
       https://ghproxy.net/https://github.com/{REPO}/releases/download/{TAG}/{asset}

  2) 装官方包（有 apt / apk / brew 的环境）
     astro add luau   （或从 https://github.com/luau-lang/luau/releases 取）

  3) 自己编译（需要 clang + cmake）
     python build_x86.py
""", flush=True)
    return None


def main():
    name_arg = [a for a in sys.argv[1:] if not a.startswith("-")]
    force = "--force" in sys.argv
    custom = None
    for i, a in enumerate(sys.argv):
        if a == "--url" and i + 1 < len(sys.argv):
            custom = sys.argv[i + 1]

    targets = [name_arg[0]] if name_arg and name_arg[0] in ARTIFACTS else ARTIFACTS

    if "--check" in sys.argv:
        say("平台", f"{platform.machine()} → {arch_suffix()}")
        missing = 0
        for n in ARTIFACTS:
            got = resolve(n)
            if got:
                ok, arch = check(got)
                say("已有", f"{n}: {got}  {got.stat().st_size:,} 字节  {arch}")
            else:
                say("缺失", f"{n}: 需要 {n}.{arch_suffix()}")
                missing += 1
        return 0 if not missing else 1

    say("平台", f"{platform.machine()} → {arch_suffix()}")
    ok_all = True
    for n in targets:
        if not fetch(n, force=force, custom_url=custom):
            ok_all = False
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
