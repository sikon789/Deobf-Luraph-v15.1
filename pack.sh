#!/bin/sh
# pack.sh —— 打包代码包（不含二进制）
#
# 教训：以前直接在工作目录里 rm 掉 tools/ 和 bin/ 再 zip，
# 结果把工作目录自己的文件删了，还打出了空 tools/。
# 现在一律复制到临时目录再压缩，工作目录一个字节都不动。

set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/var/minis/attachments/luraph_v151_code.zip}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "[pack] 复制代码到临时目录…"
cd "$SRC"
# 只带源码与文档；二进制、反编译器、示例样本都不进代码包
find . -maxdepth 2 -type f \
    \( -name '*.py' -o -name '*.lua' -o -name '*.md' -o -name '*.txt' \
       -o -name '.gitignore' -o -name 'LICENSE*' -o -name '*.sh' \) \
    ! -path './bin/*' ! -path './tools/*' ! -path './examples/*' \
    ! -path './out_release/*' ! -name '*.pyc' \
    -exec cp --parents {} "$TMP"/ \;

echo "[pack] 检查必带文件："
for f in deob.py dynlift.py lift.py fetch_bin.py build_x86.py \
         make_release.py fastsolve.py mkfast.py bufemu.lua robstub.lua \
         readability.py report.py pretty.py pack.sh \
         humanize.py reslot.py inlinevm.py \
         libs/deobf_plus.py libs/beautify2.py libs/readable3.py; do
    if [ -f "$TMP/$f" ]; then
        printf '  ✓ %-24s %8s 字节\n' "$f" "$(stat -c%s "$TMP/$f")"
    else
        printf '  ✗ 缺少 %s\n' "$f"
        exit 1
    fi
done

echo "[pack] 压缩…"
rm -f "$OUT"
(cd "$TMP" && zip -qr "$OUT" .)
echo "[pack] 完成：$OUT  $(stat -c%s "$OUT") 字节"
echo "[pack] 内容："
unzip -l "$OUT" | tail -20
