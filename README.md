# Luraph v15.1 反混淆工具

自动识别样本形态，能解的完整解出，不能解的明确告诉你原因 —— **不报假成功**。

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

### 形态 B：业务代码编译进 VM 字节码 ❌ 不假装能解

明文里只剩 handler 表，你的代码已经变成 Luau 字节码：

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
├── fastsolve.py         剥壳执行器
├── mkfast.py            剥壳探针生成
├── bufemu.lua           buffer 模拟
├── robstub.lua          Roblox 环境桩
├── examples/            示例样本（从 Release 下载）
└── README.md
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

## v1.3.0 (2026-11-09)

### 新增：x86_64 二进制（免自己编译）

`bin/` 现在同时提供两套：

| 文件 | 架构 | 大小 |
|------|------|------|
| `luau.aarch64` / `luau-ast.aarch64` | ARM64 | 2.6 MB / 6.5 MB |
| `luau.x86_64` / `luau-ast.x86_64` | x86-64 | 3.6 MB / 8.7 MB |

**运行时自动按 `platform.machine()` 选对应版本**，用户不用手改文件名。

查找顺序：`luau-ast.<架构>` → `luau-ast`（架构校验）→ PATH。

### 新增：build_x86.py 自动构建脚本

如果官方二进制不可用，可以自己构建：

```bash
python build_x86.py          # 自动装工具链、下依赖、编译
python build_x86.py --check  # 只检查现有二进制架构
```

脚本全程打印进度，缺什么自动补：

```
[平台] 当前架构 aarch64
[工具链] 安装缺失组件：clang lld
[依赖] 下载 musl-1.2.5-r12 …
[依赖] ✓ musl 就绪（403,208 字节）
[依赖] 下载 musl-dev-1.2.5-r12 …
[配置] 运行 cmake…
[编译] Luau.Ast.CLI（首次约 10-20 分钟）…
[编译] ✓ Luau.Ast.CLI 完成
[产物] luau-ast.x86_64  9,086,832 字节
```

会自动处理的问题：
- 缺 `clang` / `lld` / `cmake` → `apk add`
- 缺 x86_64 的 libc / libstdc++ → 从 Alpine 官方源下载解压成 sysroot
- 缺 `linux/kd.h` → 自动补 `linux-headers` 包
- 编译器 ID 检测阶段的链接失败 → 用包装脚本把 `-fuse-ld=lld` 固化进去

### 改进：运行前打印准备状态

```
[1] 读取：sample.lua  636,457 字节
[1b] 检查解析器（luau-ast / luau）…
     ✓ luau-ast  luau-ast  6,711,744 字节
     ✓ luau      luau  2,692,816 字节
[2b] 正在启动剥壳引擎（bufemu 模拟执行 + buffer dump）…
     首次运行可能需要几秒到几十秒，请稍候
[2b] ✓ 剥壳完成 → 948,746 字节
```

### 修复

- `tidy()` 改为 token 级处理，不再篡改字符串字面量
- `verify()` 包一层 `if false then ... end`，只做编译期检查，永不执行被测代码
- `fastsolve.py` / `mkfast.py` 移除硬编码路径，改为多目录回退
- `loadstring` / `setfenv` 兼容 Luau（改用 `load` 回退）
- 附带 `robstub.lua`（原仓库缺失）

---

