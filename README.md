# Luraph v15.1 反混淆工具

自动识别样本形态，两种都能还原源码 —— **不报假成功**。

## 一、这个工具到底做什么

Luraph v15.1 有**两种发布形态**，工具会自动判断：

### 形态 A：业务代码留在明文 ✅ 完整解出

Luraph 只是把代码压成一行、塞进 `setmetatable({...})` 表里，外层套个加密壳。
代码本身**还是明文的 Lua**。

```
setmetatable({
  [87] = function(...) ... 真实的 UI / 功能代码 ... end,
  [1033] = math.random,
  ...
})
```

工具会自动：
1. 剥外层加密壳（十进制转义 / base64 / Luraph VM 壳）
2. 用 `luau-ast` 定位所有大函数的**精确字节区间**
3. 按区间切出来、断行、语义重命名
4. 提取 handler 表并加注释
5. 用 `luau` 验证语法

→ 输出完整可读源码。

### 形态 B：业务代码编译进 VM 字节码 ✅ 自动反向还原

明文里只剩 handler 表，业务代码在 VM 字节码里。工具会自己走动态路径截获
字节码再反编译：

```
[5b] 综合得分 = 0
  ⚠ 业务代码已编译进 VM 字节码（静态提取拿不到源码）
[6b] 尝试动态路径：在桩环境里截获字节码并反编译…
     ✓ 截获字节码 44,090 字节
     ✓ 49,347 字节  2,134 行
[✓] 已还原源码 → out.luau
```

原理是 Luraph 的加载器最终必调 `luau_load(bytecode, ...)`，字节码在那之前
已是明文。截获它即可，不需要逆向 VM 或破解分片解密。

还原后变量名会是 `v3`/`v8` 这类（Luau 字节码里没有变量名信息），
但控制流、字符串、函数边界、闭包全部完整。不想走动态路径加 `--no-lift`。

下面是静态路径看到的原始形态：

```
setmetatable({
  [1033] = math["random"],
  [106]  = buffer["writeu32"],
  ...
})
```

大函数内部全是 `arg2[1201](11, 122)` 这种寄存器操作，**一句业务代码都没有**。

工具会扫描业务特征（`GetService` / `Instance.new` / `UDim2` / `Color3` / 可读字符串），
得分过低就直接停下，告诉你：

```
════════════════════════════════════════════════════════════
  ⚠ 此样本的业务代码已编译进 VM 字节码
════════════════════════════════════════════════════════════
  ...
  已停止输出。加 --force 仍可导出骨架（仅供分析）。
```

加 `--force` 可以导出骨架 + handler 映射表，但**那不是源码**。

## 一·B、运行时会看到什么

工具启动后会先做前置自检，把「正在准备什么」和「准备好了没有」都打出来，
不会静默卡住：

```
[1] 读取：sample.lua  636,457 字节
[1b] 检查解析器（luau-ast / luau）…
     ✓ luau-ast  luau-ast  6,711,744 字节
     ✓ luau      luau  2,692,816 字节
[2] 未检测到简单外层壳
[2b] 正在启动剥壳引擎（bufemu 模拟执行 + buffer dump）…
     首次运行可能需要几秒到几十秒，请稍候
[2b] ✓ 剥壳完成 → 948,746 字节
[3] AST 解析成功
[4] 发现 2580 个函数
[5] 长度 ≥ 20,000 的函数：4 个
[5b] 业务特征扫描：… 综合得分 = 1375
[8] 语法验证：✓ 通过  OK
[9] 输出：output.lua  3,988,902 字节  43,262 行
```

每一行都标了 `✓` / `✗`，哪一步没准备好一眼能看到。

## 二、用法

```bash
# 自动判断 + 解出（形态 A）
python deob.py 样本.lua -o 输出.lua

# 只看发现了哪些大函数，不输出
python deob.py 样本.lua --list

# 强制导出骨架（形态 B 分析用）
python deob.py 样本.lua -o 骨架.lua --force

# 不做语义重命名（保留原始变量名）
python deob.py 样本.lua -o 输出.lua --no-rename

# 调整大函数阈值（默认 20000 字节）
python deob.py 样本.lua -o 输出.lua --min-size 5000
```

## 三、输出长什么样

```lua
--[[
  Luraph v15.1 自动反混淆输出
  源文件：样本.lua
  共提取 4 个业务函数
]]

-- ============================================================
-- handler 表（VM 索引 → 实际值）
-- ============================================================
-- [1033] = math.random
-- [268]  = buffer.writef64
-- [1156] = table.clear

-- ============================================================
-- 第 1 段  原始偏移 252393 - 944109  (691,716 字节)
-- ============================================================
local __part1 = function(...)
    local Players = game:GetService("Players")
    local TweenService = game:GetService("TweenService")
    ...
end
```

## 四、实测数据

| 样本 | 形态 | 结果 |
|------|------|------|
| `StealAnEggg.txt` (636 KB) | A | ✅ 43,262 行，4 个函数，103 条 handler，语法通过 |
| 数字字面量变体 (264 KB) | B | ✅ 正确识别并拒绝输出（得分 0） |
| CatHub (105 KB) | 非 Luraph | ✅ 提示不是 Luraph v15.1 |

形态 A 的业务特征得分实测 **1375**（`UDim2` 457 次、`Color3` 551 次、功能名 125 处），
形态 B 得分 **0**，区分度极高。

## 五、目录结构

```
luraph_v151/
├── deob.py              主程序
├── fetch_bin.py         按需下载二进制（首次运行自动调用）
├── build_x86.py         自己编译（没网 / 要 x86_64 时用）
├── bin/                 运行时生成，不进仓库
│   ├── luau.aarch64
│   ├── luau-ast.aarch64
│   ├── luau.x86_64
│   └── luau-ast.x86_64
├── libs/
│   ├── deobf_plus.py    词法器（支持 0b/0x/下划线/转义）
│   ├── beautify2.py     基础排版
│   └── readable3.py     语义重命名
├── dynlift.py           形态 B：动态截获 Luau 字节码
├── lift.py              封装的反编译器（Tovek）
├── fastsolve.py         剥壳执行器
├── mkfast.py            剥壳探针生成
├── bufemu.lua           buffer 模拟
├── robstub.lua          Roblox 环境桩
├── readability.py       可读性量化打分（对比两份产物）
├── report.py            多产物横向对比表
├── pretty.py            反汇编整理成人能读的形式
├── pack.sh              安全打包（不动工作目录）
├── tools/               反编译器，运行时生成，不进仓库
│   ├── luau-lifter
│   └── glibc/
├── examples/            示例样本（从 Release 下载）
└── README.md
```

### 附加工具

**可读性打分** —— 判断一份反混淆产物到底能不能用：

```bash
python readability.py 旧产物.lua 新产物.luau
```

7 个维度：语法可解析 30 / 语句密度 15 / 命名质量 15 / 缩进 10 /
无噪音 5 / **逻辑完整度 20** / 业务文案 5。

其中「逻辑完整度」权重最高——统计有多少函数体是空的、被标注 `⚠ 未记录`。
一份看着漂亮的产物如果丢了一半逻辑，这一项会直接暴露。

**多产物对比**：

```bash
python report.py a.lua b.lua c.luau
```

**反汇编整理**（形态 B 的中间产物，不想要源码只要结构时用）：

```bash
python pretty.py dump.txt 输出.txt
```

## 六、环境与安装

Python 3.8+，无第三方依赖。

### 二进制不进仓库，首次运行自动获取

仓库里**没有任何二进制**（只有约 100 KB 代码）。`bin/` 下的 luau / luau-ast
在第一次运行时由 `fetch_bin.py` 从 GitHub Release 下载，之后一直走本地缓存：

```
[1] 读取：sample.lua  948,746 字节
[1b] 检查解析器（luau-ast / luau）…
     本地没有可用的 luau-ast，正在从 GitHub Release 获取…
[下载] https://ghproxy.net/https://github.com/…  ✓ 6,711,744 字节
     ✓ luau-ast  luau-ast.aarch64  6,711,744 字节
```

想提前装好、或者网络受限，可以手动跑：

```bash
python fetch_bin.py            # 下载当前架构所需二进制
python fetch_bin.py --check    # 只看有什么、缺什么
python fetch_bin.py --force    # 强制重下
python fetch_bin.py --url https://你的镜像/luau   # 自定义源
```

支持的环境变量：

| 变量 | 作用 |
|------|------|
| `LUAU_BIN_URL` | 覆盖下载源前缀（自建服务器 / 网盘直链目录） |
| `LUAU_BIN_MIRROR` | 镜像前缀，默认走 `ghproxy.net` 中转 |

下载失败时脚本会给出三条替代路线（换镜像手动 curl、装官方包、自己编译），
不会只丢一个报错就结束。

### 自己编译

```bash
python build_x86.py            # 自动装工具链 + 依赖 + 编译
python build_x86.py --check    # 只看现有二进制架构
```

编译产物放在 `bin/` 下，已被 `.gitignore` 排除。

## 七、能力边界（请务必读）

✅ **能做**
- 剥 Luraph 外层加密壳
- 精确定位明文业务函数（AST 字节区间，不是正则猜边界）
- 处理 `0B110001_1_1_111`、`0X3b_D` 这类数字字面量变体
- 解码 `\x72\x61\110`、`\u{0077}` 混合转义
- 提取 handler 表并标注含义
- 语法验证（luau 解析）

❌ **不能做**
- 把形态 B 的 Luau 字节码反编译回 Lua 源码
- 这需要完整的 VM 指令级反向工程，不在本工具范围内

## 八、许可

MIT License

# 更新日志

## v1.4.0 (2026-11-09)

**形态 B 从「拒绝输出」变成「自动还原源码」。** 这是本工具第一次能处理业务代码
被编译进 VM 字节码的样本。

### 核心：形态 B 自动反编译

以前的形态 B 只能给 handler 表和骨架，然后说「做不到」。现在会自己走动态路径：

```
[5b] 业务特征扫描：综合得分 = 0
  ⚠ 业务代码已编译进 VM 字节码（静态提取拿不到源码）
[6b] 尝试动态路径：在桩环境里截获字节码并反编译…
     ✓ 截获字节码 44,090 字节
     交给反编译器（Tovek）…
     ✓ 49,347 字节  2,134 行
[✓] 已还原源码 → out.luau
```

原理：Luraph 的加载器最终一定调用 `luau_load(bytecode, env, settings)`，
字节码在那之前已经是明文。在调用点截获即可 —— 不需要逆向它的 VM、
不需要破分片解密算法、不需要真实 Roblox 环境。

产物质量：变量名、字符串、控制流、`pcall`/`warn`、闭包捕获、表结构都还原，
143 个函数无一缺失。唯一的损失是局部变量名变成 `v3`/`v8`
（Luau 字节码里本来就没有变量名）。

新增文件：`dynlift.py`（截字节码）、`lift.py`（封装 Tovek 反编译器）。

### 修复：形态识别假阳性（严重）

旧版用 `"[A-Z][A-Za-z ]{8,}"` 数「可读 UI 文案」，按 1/20 加权。
两种样本都会骗过它：

- 随机标识符 `YmhpVeGpVQ`（全大写开头、无空格、长度 11）→ 4,421 个误判，凑出 219 分
- 明文 Lua 片段 `" end local ttisstring = function(v) return type(v) == "` → 得分涨到 4,362

结果是：**内部一个业务 API 都没有的文件，仅调整 `--min-size` 就能从「拒绝」翻成「成功输出」，还打 ✓ 语法验证通过。**

修法：**彻底移除所有字符串信号**，只保留 5 个 VM 字节码里不可能出现的 API 结构名：

```
GetService / Instance.new / UDim2 / Color3 / TweenService
```

实测区分度：

| 样本 | 得分 | 结果 |
|---|---:|---|
| `demo_2.html`（形态 B） | **0** | 拒绝 ✅ |
| `layer3.lua`（形态 A） | **1143** | 输出 43,954 行 ✅ |

### 修复：`--force` 对「零大函数」无效

原来的顺序是：

```python
if not sized: return 2        # ← 先返回了
...
if score < 5:                 # ← --force 只在这之后生效
```

所以一个连大函数都找不到的样本，加 `--force` 也没用。
现在 `--force` 会把阈值降到 0，重新从 `outer` 里收集非空函数：

```
[!] 没有找到大函数。
    加 --force 可导出最佳猜测的骨架（跳过大小阈值）。
    --force 已指定，跳过大小阈值，重新收集候选…
[✗] 连非空函数都没有，这个文件不像是 Luraph v15.1 产物。
```

### 修复：HTML 外壳没处理

之前把 `.html` 整个丢给 Luau 解析器，必然失败。现在 `unwrap_shell`
会先剥 HTML（取最长那行），再做已知语法瑕疵修补（缺 1 个 `end`），
最后才进 AST。

### 新增：可读性打分工具

用来判断一份反混淆产物能不能用：

```bash
python readability.py 旧产物.lua 新产物.luau
python report.py a.lua b.lua c.luau
```

7 维度打分，其中「逻辑完整度」权重最高（20 分）——
统计有多少函数体是空的 / 被标注「未记录」。

同一份 Scorched Earth 样本，人工重写版 vs 本工具反编译版：

| 维度 | 人工重写 | 本工具 |
|---|---:|---:|
| 命名质量 | **14** | 0 |
| 无噪音 | 0 | **5** |
| 逻辑完整度 | **5** | **20** |
| 总分 | 79 | **85** |

人工重写版看起来更漂亮（变量名有意义、有章节注释），但
**16 处函数体是空的**，包括 NoClip 里真正的 `part.CanCollide = false`。
本工具版变量名是 `v3`/`v8`，但 143 个函数一个都不缺。

### 新增：反编译器依赖自动获取

`fetch_bin.py` 现在一并处理 `luau-lifter` 和 glibc：

```
luau-lifter.aarch64     8.1 MB   反编译（形态 B 必需）
glibc-aarch64.tar.gz    1.3 MB   Alpine 跑 glibc 程序用
```

`--lifter-only` 只装反编译器；Debian/Ubuntu 上会自动用系统 glibc，不用下载。

### 新增：安全打包脚本

`pack.sh` 用 `mktemp -d` 复制到临时目录再压缩，并校验必带文件清单。
之前的版本直接在工作目录 `rm -rf tools/` 再 zip，
结果打出了空的 `tools/`，还把工作目录自己的文件删了。

---

## v1.3.0 (2026-11-09)

### 新增：x86_64 二进制（免自己编译）

`bin/` 现在同时提供两套：

| 文件 | 架构 | 大小 |
|------|------|------|
| `luau.aarch64` / `luau-ast.aarch64` | ARM64 | 2.6 MB / 6.5 MB |
| `luau.x86_64` / `luau-ast.x86_64` | x86-64 | 3.6 MB / 8.7 MB |

**运行时自动按 `platform.machine()` 选对应版本**，用户不用手改文件名。

查找顺序：`luau-ast.<架构>` → `luau-ast`（架构校验）→ PATH。

### 新增：二进制改从 Release 按需下载

仓库里不放二进制（只有 ~100 KB 代码），首次运行时由 `fetch_bin.py`
从 GitHub Release 拉取，之后走本地缓存。

```bash
python fetch_bin.py            # 下载当前架构所需
python fetch_bin.py --check    # 只看有什么、缺什么
python fetch_bin.py --force    # 强制重下
```

多镜像回退：`ghproxy.net` → 直连 GitHub。

### 新增：build_x86.py 自动构建脚本

如果官方二进制不可用，可以自己构建：

```bash
python build_x86.py          # 自动装工具链、下依赖、编译
python build_x86.py --check  # 只检查现有二进制架构
```

会自动处理：缺 `clang`/`lld`/`cmake` → `apk add`；
缺 x86_64 libc → 从 Alpine 源下载解压成 sysroot；
缺 `linux/kd.h` → 自动补 `linux-headers`。

### 改进：运行前打印准备状态

```
[1b] 检查解析器（luau-ast / luau）…
     ✓ luau-ast  luau-ast.aarch64  6,711,744 字节
     ✓ luau      luau.aarch64  2,692,816 字节
```

---

## v1.2.0 (2026-11-08)

修 3 个必修问题：

- `tidy()` 改字符串内容（`"hello . world"` → `"hello.world"`）→ 改 token 级
- `verify()` 会真的执行被测代码（恶意脚本能写文件）→ 包 `if false then ... end`
- `mkfast.py` 硬编码路径 + 用 `loadstring`/`setfenv`（Luau 已移除）→ 多目录回退 + `load` 兼容

---

