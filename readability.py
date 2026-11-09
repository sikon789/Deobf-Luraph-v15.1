#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
readability.py —— 量化对比两份反混淆产物的可读性

不看「感觉」，只算可验证的指标：
    1. 结构完整性：能否被解析器通过（语法正确 = 能直接读/改）
    2. 语义保真：还原了多少实际语句，而不是注释和占位
    3. 命名质量：机名（arg1/v123/Tab2）占比
    4. 缩进规整：真缩进 vs 一行到底
    5. 注释占比：可读的说明性文字
    6. 噪音：空占位、⚠ 标记、TODO、反编译失败痕迹
"""
import re
import sys
from pathlib import Path


def load(p):
    return Path(p).read_text(encoding="utf-8", errors="ignore")


def has_lua_syntax_ok(p):
    """用 luau 跑一次，能过解析就算语法 OK"""
    import subprocess
    for cand in ("/var/minis/workspace/pkg_en/bin/luau.aarch64",
                 "/var/minis/workspace/pkg_en/bin/luau"):
        if Path(cand).is_file():
            try:
                r = subprocess.run([cand, str(p)], capture_output=True,
                                   text=True, timeout=120)
                err = (r.stderr or "") + (r.stdout or "")
                if "Expected" in err and "when parsing" in err:
                    return False, err.strip().split("\n")[0][:80]
                return True, "解析通过"
            except Exception as e:
                return None, str(e)[:60]
    return None, "无 luau"


def analyze(path):
    src = load(path)
    lines = src.split("\n")
    n = len(lines)
    nonblank = [l for l in lines if l.strip()]
    code_lines = [l for l in nonblank
                  if not l.strip().startswith("--")]

    # --- 机名统计 ---
    # 关键区分：v3 这类如果在本文件里被 `local v3` 声明过，
    # 它就是一个普通的局部变量（反编译器没法还原原名，但语义完整），
    # 不能和 Slider3 / Tab2 / fn2 这种「连声明都函数化」的机名混为一谈。
    declared = set(re.findall(r'\blocal\s+([A-Za-z_]\w*)', src))
    declared |= set(re.findall(r'function\s+([A-Za-z_]\w*)\s*\(', src))
    declared |= set(re.findall(r'for\s+([A-Za-z_]\w*)\s*,?', src))

    def is_temp(nm):
        """形如 v3 / a12 / i5 的短名 —— 反编译器的临时寄存器命名"""
        return bool(re.fullmatch(r'[a-zA-Z]\d+', nm))

    # 注意排除真正的 API 名：UDim2 / Color3 / Vector2 / BackgroundColor3
    # 这些是合法的 Roblox 类型，不能算机名
    API_NAMES = {
        "UDim2", "UDim", "Color3", "Vector2", "Vector3", "CFrame", "Vector2int16",
        "Vector3int16", "Rect", "NumberSequence", "ColorSequence", "BrickColor",
        "Font", "UDim2Scalar", "Enum",
    }
    # 只统计「明显是机器起名」的模式。
    # 不统计 v123 / i26 这类 —— 它们是正常的短局部变量（循环计数器等），
    # 统计进去会把任何代码都判成不可读。
    # 分三档：
    #   SEMI  —— 有语义前缀但带编号（tbl3 / fn47 / onFrame12），半可读
    #   FULL  —— 纯编号（arg1 / v2），几乎不可读
    SEMI_PREFIX = ('tbl', 'fn', 'rgb', 'result', 'item', 'onFrame', 'onTick',
                   'onInput', 'draw', 'update', 'render', 'refresh', 'create',
                   'destroy', 'tween', 'safeCall', 'setupEnv', 'saveFile',
                   'loadFile', 'raycast', 'disconnect', 'num', 'str', 'flag',
                   'cond', 'scale', 'offset', 'enum', 'map', 'list',
                   'onFrame', 'onStep', 'onInputChanged', 'onInputEnded',
                   'onClick', 'onCharacter', 'onHumanoid', 'onCamera',
                   'onHealth', 'onKey', 'onToggle', 'onChange', 'onRelease',
                   'onPress', 'initServices', 'process', 'handler', 'callback',
                   'loop', 'tick', 'frame', 'updateLoop', 'conn')
    raw_names = [n for n in re.findall(
        r'\b([A-Za-z_]\w*\d+)\b', src) if n not in API_NAMES]
    semi, full, unresolvable, api_suffixed = [], [], [], []
    for nm_i in raw_names:
        pre = nm_i.rstrip('0123456789')
        # API 名 + 数字后缀（GetService2 / Instance_new3 / UDim2 之类）
        # 这是重名消解，不是机器命名
        if re.fullmatch(r'(GetService|Instance_new|Instance|FindFirstChild|'
                        r'WaitForChild|UDim|UDim2|Color3|Color|Vector2|Vector3|'
                        r'CFrame|pcall|pcallRes|safeCall|Add|Remove|Create|'
                        r'Destroy|Connect|Disconnect|Tween|TweenService|'
                        r'Enum|Drawing_new|Drawing|BackgroundColor|TextColor|'
                        r'BackgroundTransparency|TextTransparency|Size|Position|'
                        r'AnchorPoint|BorderSize|BorderColor|Font|TextScaled|'
                        r'Parent|Name|Visible|Transparency|Value)\d*', nm_i):
            api_suffixed.append(nm_i)
        elif re.fullmatch(r'(UDim2|Color3|Vector2|Vector3|UDim|CFrame)$', pre):
            api_suffixed.append(nm_i)
        elif pre in SEMI_PREFIX:
            semi.append(nm_i)
        elif re.fullmatch(r'[A-Za-z_]+_\d+', nm_i):
            # X_7 / tbl_7 这种「容器+下标」，是有语义的
            semi.append(nm_i)
        elif pre in ('arg', '__part', 'A', 'R'):
            # VM 参数寄存器，源码里本来就没有名字 → 不算「起名差」，另行计入 unresolvable
            unresolvable.append(nm_i)
        elif re.fullmatch(r'[a-zA-Z]\d+', nm_i):
            # v3 / i26 这类短名：解构变量或循环计数器，Lua 里很常见
            unresolvable.append(nm_i)
        else:
            full.append(nm_i)
    machine = full
    temps = semi
    real_words = re.findall(r'\b(?:local|function|if|then|else|for|while|'
                            r'return|end|GetService|Color3|UDim2|'
                            r'ESP|Players|Camera|Key|Text|Box)\b', src)
    # 有意义的业务名（长度>4、含语义）
    semantic = re.findall(r'\b([A-Za-z_][A-Za-z0-9_]{4,})\b', src)
    semantic_set = set(semantic)

    # --- 缩进 ---
    indented = sum(1 for l in code_lines if l[:1] in (" ", "\t"))

    # --- 注释 ---
    comments = sum(1 for l in nonblank if l.strip().startswith("--"))
    block_comment_chars = sum(len(m) for m in re.findall(r'--\[\[.*?\]\]', src, re.S))

    # --- 噪音 ---
    warn_marks = src.count("⚠")
    todo = len(re.findall(r'\b(TODO|FIXME|devirt|unlifted|not recovered|'
                          r'无法还原|未还原|缺失)\b', src, re.I))
    empty_blocks = len(re.findall(r'function\s*\([^)]*\)\s*end\b', src))
    placeholder = len(re.findall(r'\b(nil\s*--|--\s*占位|placeholder)\b', src, re.I))

    # --- 语句密度：真实调用/赋值 ---
    calls = len(re.findall(r'\w+\s*[:(]\s*[^)]*\)', src))
    assignments = len(re.findall(r'^\s*(local\s+)?[\w.\[\]"]+\s*=', src, re.M))
    control = len(re.findall(r'^\s*(if|for|while|repeat)\b', src, re.M))

    # --- 字符串内容（业务文案）---
    strings = re.findall(r'"([^"\\]{4,})"', src)
    readable_strings = [s for s in strings
                        if not s.startswith(("http", "rbxasset", "\\"))
                        and re.search(r'[A-Za-z\u4e00-\u9fff]{4,}', s)]

    funcs = len(re.findall(r'\bfunction\b', src)) - \
        len(re.findall(r'\bfunction\b', "".join(
            re.findall(r'--\[\[.*?\]\]', src, re.S))))
    ok, msg = has_lua_syntax_ok(path)

    return {
        "path": str(path),
        "bytes": len(src.encode()),
        "lines": n,
        "code_lines": len(code_lines),
        "nonblank": len(nonblank),
        "syntax_ok": ok,
        "syntax_msg": msg,
        "machine_names": len(machine),
        "unresolvable": len(unresolvable),
        "temp_vars": len(temps),
        "declared_count": len(declared),
        "semantic_names": len(semantic_set),
        "indent_pct": 100.0 * indented / len(code_lines) if code_lines else 0,
        "comments": comments,
        "comment_pct": 100.0 * comments / len(nonblank) if nonblank else 0,
        "warn_marks": warn_marks,
        "todo": todo,
        "empty_blocks": empty_blocks,
        "calls": calls,
        "assignments": assignments,
        "control": control,
        "readable_strings": len(readable_strings),
        "slot_reads": len(re.findall(r'\b\w+\[\d+\]\.\w+', src)),
        "long_lines": sum(1 for l in code_lines if len(l) > 120),
        "max_line": max((len(l) for l in code_lines), default=0),
        "functions": max(funcs, 1),
        "avg_line_len": sum(len(l) for l in lines) / n if n else 0,
    }


def score(d):
    """0-100 综合分。权重按「拿到手能不能直接读懂/改动」定。"""
    s = 0
    detail = []
    # 满分：语法30 + 语句密度15 + 命名15 + 缩进10 + 无噪音5 + 逻辑完整度20 + 文案5
    #       = 100

    # 1) 语法正确 30 分 —— 不能解析就等于不能读
    if d["syntax_ok"] is True:
        s += 30
        detail.append(("语法可解析", 30, "✓ " + d["syntax_msg"]))
    elif d["syntax_ok"] is False:
        detail.append(("语法可解析", 0, "✗ " + d["syntax_msg"]))
    else:
        s += 15
        detail.append(("语法可解析", 15, "? " + d["syntax_msg"]))

    # 2) 语义密度 15 分 —— 真语句 vs 空壳
    density = (d["calls"] + d["assignments"] + d["control"]) / max(d["code_lines"], 1)
    pts = min(15, int(15 * min(density / 0.8, 1.0)))
    s += pts
    detail.append(("语句密度", pts, f"{density:.2f} 语句/行"))

    # 3) 命名质量 15 分 —— 真机名越少越好（临时变量不算重罚）
    total_names = (d["machine_names"] + d["temp_vars"] * 0.3
                   + d["semantic_names"])
    if total_names:
        # 半语义（tbl_7 / onFrame2）按 0.35 折算，原名不可得的不计罚
        weighted = d["machine_names"] + d["temp_vars"] * 0.35
        denom = d["machine_names"] + d["temp_vars"] + d["semantic_names"]
        machine_pct = 100.0 * weighted / max(denom, 1)
        pts = max(0, int(15 * (1 - min(machine_pct / 40, 1))))
    else:
        pts = 8
        machine_pct = 0
    s += pts
    detail.append(("命名质量", pts,
                   f"机名 {d['machine_names']} / 半语义 {d['temp_vars']} / "
                   f"原名不可得 {d['unresolvable']}"))

    # 4) 缩进规整 10 分
    pts = min(10, int(10 * min(d["indent_pct"] / 60, 1.0)))
    s += pts
    detail.append(("缩进规整", pts, f"{d['indent_pct']:.0f}% 行有缩进"))

    # 5) 无噪音 3 分
    noise = d["warn_marks"] * 2 + d["todo"] * 2 + d["empty_blocks"]
    pts = max(0, 3 - min(3, noise // 4))
    s += pts
    detail.append(("无噪音", pts,
                   f"⚠×{d['warn_marks']} TODO×{d['todo']} 空函数×{d['empty_blocks']}"))

    # 6) 逻辑完整度 20 分 —— 最关键：代码在不在
    #    「⚠ 回调体空」= 逻辑真的丢了，不是排版问题
    omitted = d["warn_marks"]
    funcs = d["functions"]
    if funcs:
        omit_pct = 100.0 * omitted / funcs
        pts = max(0, int(20 * (1 - min(omit_pct / 30, 1))))
    else:
        pts = 10
        omit_pct = 0
    s += pts
    detail.append(("逻辑完整度", pts,
                   f"{omitted} 处函数体缺失 / 共 {funcs} 个函数 ({omit_pct:.0f}%)"))

    # 6.5) 行长合理度 5 分（从「无噪音」里挪 3 分出来）
    long_pct = 100.0 * d["long_lines"] / max(d["code_lines"], 1)
    pts = max(0, 5 - int(min(5, long_pct / 4)))
    s += pts
    detail.append(("行长合理", pts, f"{d['long_lines']} 行 >120 字符 ({long_pct:.1f}%)"))

    # 7) 业务文案 5 分
    pts = min(5, int(5 * min(d["readable_strings"] / 60, 1.0)))
    s += pts
    detail.append(("业务文案", pts, f"{d['readable_strings']} 条"))

    return s, detail


def bar(v, w=24):
    n = int(w * v / 100)
    return "█" * n + "░" * (w - n)


def main():
    if len(sys.argv) < 3:
        print("用法: readability.py <旧产物> <新产物>")
        return 1

    a, b = analyze(sys.argv[1]), analyze(sys.argv[2])
    sa, da = score(a)
    sb, db = score(b)

    W = 26
    print("=" * 78)
    print("  可读性量化对比")
    print("=" * 78)
    print(f"  旧: {Path(sys.argv[1]).name:<40} {a['bytes']:>10,} 字节  {a['lines']:>6,} 行")
    print(f"  新: {Path(sys.argv[2]).name:<40} {b['bytes']:>10,} 字节  {b['lines']:>6,} 行")
    print()

    print(f"  {'维度':<14}{'旧':>6}{'新':>7}   说明")
    print("  " + "-" * 72)
    for (name, pa, why_a), (_, pb, why_b) in zip(da, db):
        print(f"  {name:<14}{pa:>5}/{max(pa,pb) and '' or ''}"
              f"{'':<1}{pb:>6}   ")
        print(f"  {'':<14}{'':>6}{'':>7}   旧: {why_a}")
        print(f"  {'':<14}{'':>6}{'':>7}   新: {why_b}")
    print()
    print("  " + "-" * 72)
    print(f"  {'总分':<14}{sa:>6}{sb:>7}")
    print(f"  {'':<14}{bar(sa)}{'  '}{bar(sb)}")
    print()

    print("  ── 原始数据 ──")
    keys = [("行数", "lines"), ("代码行", "code_lines"),
            ("真机名", "machine_names"), ("临时变量", "temp_vars"),
            ("语义名", "semantic_names"), ("调用", "calls"),
            ("赋值", "assignments"), ("控制流", "control"),
            ("函数", "functions"),
            ("槽位访问", "slot_reads"), ("长行>120", "long_lines"),
            ("注释行", "comments"), ("可读文案", "readable_strings"),
            ("平均行长", "avg_line_len")]
    print(f"  {'指标':<12}{'旧':>12}{'新':>12}")
    for label, k in keys:
        va, vb = a[k], b[k]
        if isinstance(va, float):
            print(f"  {label:<12}{va:>12.1f}{vb:>12.1f}")
        else:
            print(f"  {label:<12}{va:>12,}{vb:>12,}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
