#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pretty.py —— 把 Luau 反汇编 dump 整理成人能读的形式

输入是 /tmp/body.txt 那种格式：
    PROTOS 153 STR 436 VER 3
    PROTO 1 name=(??) nparams=0 vararg=false sizecode=11 nk=6 line=8
      0: A=0 opmode=4 D=1 opname=GETIMPORT ...
      K0=STR loadstring

输出：
    · 按功能聚类的字符串清单
    · 每个 proto 的指令（一行一条，操作数解析成可读形式）
    · 调用图（谁调谁）
    · 可疑常量表（外链、反检测、调试开关）
"""
import re
import sys
from collections import defaultdict, Counter

IN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/body.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "disasm_readable.txt"

OPS_WITH_ABC = {"ADD", "SUB", "MUL", "DIV", "MOD", "POW", "IDIV",
                "AND", "OR", "CONCAT", "GETTABLE", "SETTABLE", "NEWTABLE",
                "GETUPVAL", "SETUPVAL", "JUMPIFEQ", "JUMPIFLE", "JUMPIFLT",
                "JUMPIFNOTEQ", "JUMPIFNOTLE", "JUMPIFNOTLT", "NAMECALL",
                "FORNPREP", "FORNLOOP", "FORGLOOP", "FORGPREP"}


def parse_dump(path):
    protos = []
    cur = None
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("PROTO "):
                m = re.match(
                    r"PROTO (\d+) name=(.*?) nparams=(\d+) vararg=(\w+) "
                    r"sizecode=(\d+) nk=(\d+) line=(\d+)", line)
                if m:
                    cur = {
                        "id": int(m.group(1)),
                        "name": m.group(2),
                        "nparams": int(m.group(3)),
                        "vararg": m.group(4) == "true",
                        "sizecode": int(m.group(5)),
                        "nk": int(m.group(6)),
                        "line": int(m.group(7)),
                        "ins": [],
                        "k": [],
                    }
                    protos.append(cur)
            elif cur is not None and re.match(r"^\s+\d+: ", line):
                body = line.split(": ", 1)[1]
                d = {}
                for part in body.split(" "):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        d[k] = v
                if d.get("opname") == "auxvalue":
                    if cur["ins"]:
                        cur["ins"][-1]["aux"] = d.get("value", "")
                    continue
                cur["ins"].append(d)
            elif cur is not None and re.match(r"^\s+K\d+=", line):
                cur["k"].append(line.strip())
    return protos


def op_of(ins):
    return ins.get("opname", "?")


def render(ins, k):
    """一条指令渲染成可读形式"""
    op = op_of(ins)
    a = ins.get("A")
    b = ins.get("B")
    c = ins.get("C")
    d = ins.get("D")

    def kval(name):
        """K 字段可能是字符串常量名，也可能是字符串下标"""
        if not name:
            return ""
        return name

    parts = [op]
    if op in ("LOADK", "GETIMPORT"):
        kk = ins.get("K", "")
        if op == "GETIMPORT":
            parts.append(f"R{a} <- import({kk})")
        else:
            parts.append(f"R{a} = \"{kk}\"")
    elif op == "NAMECALL":
        parts.append(f"R{a} : {kval(ins.get('K',''))} (self=R{b})")
    elif op == "CALL":
        try:
            src = int(b) - 1
            parts.append(f"R{a} = call(R{src}, {c} ret)")
        except (TypeError, ValueError):
            parts.append(f"R{a} = call(R{b}, {c} ret)")
    elif op == "RETURN":
        try:
            bb = int(b)
        except (TypeError, ValueError):
            bb = 1
        if bb == 0:
            parts.append(f"return R{a}.. (multi)")
        elif bb == 1:
            parts.append("return")
        else:
            try:
                parts.append(f"return R{a}..R{int(a)+bb-2}")
            except (TypeError, ValueError):
                parts.append(f"return R{a}..(+{bb})")
    elif op == "GETTABLE":
        parts.append(f"R{a} = R{b}[R{c}]" if c not in ("0", "-1") else f"R{a} = R{b}[K{c}]")
    elif op == "SETTABLE":
        parts.append(f"R{a}[{b}] = R{c}")
    elif op == "NEWTABLE":
        parts.append(f"R{a} = {{}}")
    elif op.startswith("JUMP"):
        tgt = (int(d) if d and d.lstrip("-").isdigit() else 0)
        parts.append(f"-> +{tgt}  (comp R{a} vs R{d if 'd' in ins else ''})")
    elif op in ("ADD", "SUB", "MUL", "DIV", "MOD", "POW"):
        sym = {"ADD": "+", "SUB": "-", "MUL": "*", "DIV": "/",
               "MOD": "%", "POW": "^"}.get(op, op)
        parts.append(f"R{a} = R{b} {sym} {c if c not in ('0','-1') else 'K'+str(c)}")
    elif op == "CONCAT":
        parts.append(f"R{a} = concat(R{b}..R{c})")
    elif op == "GETUPVAL":
        parts.append(f"R{a} = U{b}")
    elif op == "SETUPVAL":
        parts.append(f"U{b} = R{a}")
    elif op == "FORNPREP":
        parts.append(f"fornum R{a} from R{a+1} to R{a+2} step R{a+3} -> +{d}")
    elif op == "FORNLOOP":
        parts.append(f"next R{a} -> +{d}")
    elif op == "FORGPREP":
        parts.append(f"forgen prep R{a} iter=R{a+1} -> +{d}")
    elif op == "FORGLOOP":
        parts.append(f"forgen next R{a} -> +{d}")
    elif op in ("CLOSEUPVALS", "PREPVARARGS", "LOADNIL", "LOP", "FASTCALL"):
        pass
    else:
        if a is not None:
            parts.append(f"R{a}")
        if b is not None and b not in ("0",):
            parts.append(f"B{b}")
        if c is not None and c not in ("0",):
            parts.append(f"C{c}")
        if d is not None:
            parts.append(f"D{d}")
    if ins.get("aux"):
        parts.append(f"aux={ins['aux']}")
    return " ".join(parts)


def main():
    protos = parse_dump(IN)
    if not protos:
        print("没解析到 proto，检查输入格式")
        return 1

    all_k = []
    for p in protos:
        all_k.extend(p["k"])

    strings = sorted({k.split("=", 1)[1][4:] for k in all_k if k.split("=", 1)[1].startswith("STR ")})

    L = []
    L.append("=" * 78)
    L.append("  Luraph v15.1 业务字节码 — 可读反汇编")
    L.append(f"  来源: {IN}")
    L.append(f"  {len(protos)} 个 proto，{len(strings)} 个字符串常量")
    L.append("=" * 78)
    L.append("")

    # ---- 1. 字符串分类 ----
    L.append("【一、字符串常量（按用途分类）】")
    L.append("")
    cats = {
        "网络/外链": [s for s in strings if s.startswith(("http://", "https://", "raw."))],
        "Roblox API": [s for s in strings if s in {
            "GetService", "Instance", "HttpGet", "HttpGetAsync", "Players",
            "Workspace", "Lighting", "RunService", "UserInputService",
            "TweenService", "CoreGui", "FireServer", "InvokeServer",
            "RemoteEvent", "BindAction", "FindFirstChild", "WaitForChild",
            "Raycast", "CFrame", "Vector3", "Vector2", "Color3", "UDim2", "UDim",
            "Enum", "ScreenGui", "Frame", "TextLabel", "TextButton", "TextBox",
            "ImageLabel", "ScrollingFrame", "UIStroke", "UICorner", "UIGradient",
            "WorldToViewportPoint", "Character", "Humanoid", "HumanoidRootPart",
            "Camera", "LocalPlayer", "GetMouseLocation", "IsKeyDown",
            "AssemblyLinearVelocity", "BasePart", "BrickColor", "Transparency",
            "BackgroundTransparency", "BackgroundColor3", "TextColor3",
            "TextTransparency", "BorderSizePixel", "BorderColor3", "AnchorPoint",
            "Size", "Position", "Parent", "Name", "Visible", "Color",
        }],
        "功能名（可读）": [s for s in strings if s in {
        } or (len(s) > 6 and (" " in s or s.isupper() or "_" in s)
              and not s.replace("_", "").isalnum())],
        "疑似密钥/令牌": [s for s in strings if re.fullmatch(r"[A-Za-z0-9_\-]{32,}", s)],
    }
    seen = set()

    def emit(title, items):
        items = [x for x in items if x not in seen and x]
        if not items:
            return
        seen.update(items)
        L.append(f"  ── {title}  ({len(items)} 个)")
        for x in items[:60]:
            L.append(f"     {x}")
        if len(items) > 60:
            L.append(f"     … 还有 {len(items) - 60} 个")
        L.append("")

    emit("网络 / 外链", cats["网络/外链"])
    emit("Roblox API", cats["Roblox API"])
    emit("疑似密钥 / 令牌", cats["疑似密钥/令牌"])

    rest = [s for s in strings if s not in seen and s.strip()]
    emit("其余字符串（业务文案、配置键名等）", rest)

    # ---- 2. 调用图 ----
    L.append("【二、proto 概览（按代码量排序，前 25）】")
    L.append("")
    L.append(f"  {'ID':>4}  {'指令数':>6}  {'参数':>4}  {'常量':>4}  {'行':>6}  名称")
    L.append("  " + "-" * 72)
    for p in sorted(protos, key=lambda x: -x["sizecode"])[:25]:
        nm = p["name"] if p["name"] not in ("(??)", "") else "—"
        L.append(f"  {p['id']:>4}  {p['sizecode']:>6}  {p['nparams']:>4}  "
                 f"{p['nk']:>4}  {p['line']:>6}  {nm}")
    L.append("")

    # ---- 3. 关键业务 proto 的指令 ----
    big = sorted(protos, key=lambda x: -x["sizecode"])[:3]
    L.append("【三、主要业务函数反汇编】")
    L.append("")
    for p in big:
        L.append("=" * 78)
        L.append(f"PROTO {p['id']}   指令 {p['sizecode']} 条   参数 {p['nparams']}   行 {p['line']}")
        L.append("=" * 78)
        for i, ins in enumerate(p["ins"]):
            L.append(f"  {i:>4}  {render(ins, p['k'])}")
        if p["k"]:
            L.append("  ── 常量表 ──")
            for k in p["k"]:
                L.append("     " + k)
        L.append("")

    # ---- 4. 可疑点 ----
    L.append("【四、值得注意的点】")
    L.append("")
    flags = []
    for s in strings:
        if s.startswith("http"):
            flags.append(f"外部脚本加载：{s}")
        if s in ("loadstring", "dofile", "require", "load"):
            flags.append(f"动态代码执行：{s}")
        if any(w in s.lower() for w in ("hook", "bypass", "anti", "detect",
                                        "exploit", "inject", "tamper")):
            flags.append(f"反检测 / 注入相关：{s}")
        if any(w in s.lower() for w in ("key", "token", "auth", "license",
                                        "whitelist", "admin", "owner")):
            flags.append(f"鉴权相关：{s}")
    if flags:
        for f in dict.fromkeys(flags):
            L.append("  • " + f)
    else:
        L.append("  （未发现明显可疑项）")
    L.append("")

    text = "\n".join(L)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"写出 {OUT}  {len(text):,} 字节  {text.count(chr(10)) + 1:,} 行")
    print(f"  proto {len(protos)} 个 / 字符串 {len(strings)} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
