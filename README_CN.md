# Luraph v15.1 一键反混淆工具

![版本](https://img.shields.io/badge/版本-v1.0.0-blue)
![许可](https://img.shields.io/badge/许可-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

一个专门用于反编译 **Luraph v15.1** 保护脚本的自动化工具，可恢复完整的可读源代码。

## 🌟 主要特性

- ✅ **全自动反混淆** - 一键处理 Luraph v15.1 多层包装
- ✅ **源码恢复** - 还原示业务流程和 UI 库代码
- ✅ **中文界面** - 友好的中文命令行提示
- ✅ **桩环境** - 内置 `Roblox` 桩环境支持验证运行
- ✅ **开源免费** - MIT 许可，可自由使用和修改

## 🚀 快速开始

### 安装

本项目无需额外安装，Python 3.8+ 即可运行：

```bash
# 克隆仓库
git clone https://github.com/yourusername/luraph151-cn.git
cd luraph151-cn

# 检查 Python 版本
python3 --version
```

### 使用

#### 基础用法

```bash
python luraph_cn.py input.lua -o output.lua
```

#### 调试模式

```bash
python luraph_cn.py input.txt -o output.lua --verbose
```

#### 示例

```bash
# 反混淆标准文件
python luraph_cn.py StealAnEggg.txt -o output.lua

# 处理 .lua 文件
python luraph_cn.py protected_script.lua -o deobfuscated.lua --force

# 指定输出目录
python luraph_cn.py input.lua -o ./pro_output/result.lua
```

## 📁 项目结构

```
cn_deob/
├── luraph_cn.py          # 主程序（中文界面）
├── libs/                  # 核心库
│   ├── beautify2.py      # 排版引擎
│   ├── readable3.py      # 语义重命名
│   └── mock_standalone.py # 桩环境
├── examples/              # 示例文件
│   ├── layer3_sample.lua   # 示例输入
│   └── blob4.bin           # 示例 payload
├── README_CN.md           # 本文件
└── requirements.txt       # 依赖列表（空）
```

## 🎯 技术核心

### 1. 多层包装解析
自动识别并剥离 Luraph v15.1 的 stage1、stage2、VM 层，只保留真正的业务代码。

### 2. 语义重命名
基于作用域分析，自动恢复反混淆后的变量名：
- `W` → `VM` (虚拟机上下文)
- `p` → `GetService` (服务获取)
- `k` → `opcode` (操作码)
- `Gk` → `MemoryAccess` (内存访问)
- `Xk` → `FunctionCall` (函数调用)

### 3. 手写风格格式化
模仿程序员在 IDE 手动排版的风格，代码易读：
- 适当的空行分隔逻辑块
- 关键字后紧跟空格
- 减少嵌套层级感

### 4. 桩环境修复
完整模拟 `Roblox` API：
- `Color3`、`UDim2`、`Vector2` 等
- `getgenv()`、`loadstring()`、`pcall()`
- `HttpService`、`TweenService`、`Players`

## ⚙️ 工作原理

```
原始保护脚本 (layer3.lua)
    ↓ [反混淆引擎]
语义重命名 (readable3)
    ↓
代码编辑 (beautify2)
    ↓
可运行源代码 (output.lua)
```

**反混淆完整流程：**

1. **Token 化** - 将代码分解为基本单元
2. **AST 构建** - 构建抽象语法树
3. **作用域分析** - 识别变量声明和作用域
4. **语义重命名** - 恢复变量名和函数名
5. **风格排版** - 添加合适的空格和换行
6. **输出验证** - 检查语法正确性

## ⚠️ 注意事项

- **输入文件** - 必须是 Luraph v15.1 保护的 `.lua` 或 `.txt` 文件
- **输出文件** - 生成的 Lua 代码可以在任何执行器中运行
- **桩限制** - 某些 Roblox API 可能被简化，个别功能可能未完全模拟
- **仅用于学习** - 请遵守目的用途的法律法规

## 📋 常见问题

### Q: 工具为什么没有反应？
A: 确认输入文件是否是 Luraph v15.1 保护。其他保护方案（如 `Luraph v15.0`）可能不兼容。

### Q: 输出文件很大？
A: 正常。反混淆后的代码包含完整的注释和样式，文件会比原始保护代码大数倍。

### Q: 运行时报错？
A: 检查桩环境是否完全模拟了需要的 API。有问题请提交 issue。

## 🤝 贡献指南

欢迎提交 PR！本项目的规则：

1. 保持代码简洁高效
2. 尊重原作者的 License
3. 提供中文注释和文档
4. 不破坏向后兼容性

## 📄 许可证

**MIT License**

Copyright (c) 2024 Luraph151CN Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 💾 下载

[![GitHub Release](https://img.shields.io/badge/下载-GitHub-green)](https://github.com/yourusername/luraph151-cn/releases)

---

*Made with ❤️ for educational purposes*

## ✨ 新增功能：清理模式

### `--clean` 参数

从 v1.1.0 开始，支持清理模式，可以自动移除 Luraph 框架残留、调试代码和死代码，只保留核心业务逻辑。

```bash
python luraph_cn.py input.lua -o output.lua --clean
```

### 清理规则

1. **移除 Handler 定义** - 删除 `[41] = function...` 等 Luraph 特有的 handler 方法
2. **移除主分发器** - 删除 `rk = function...` 等 VM 分派器代码
3. **移除调试死循环** - 删除包含调试功能和炸弹的 `while true do` 循环
4. **保留业务逻辑** - 保留所有实际的业务函数和 UI 库

### 使用场景

- **分析研究** - 查看脚本的实际业务逻辑
- **逆向调试** - 减少无关代码干扰
- **学习参考** - 快速理解脚本功能

### ⚠️ 注意事项

启用 `--clean` 后的代码可能**无法直接运行**，因为移除了框架代码。主要适用于：
- 代码分析
- 功能学习
- 逆向研究

**完整反混淆版**（保留框架，可运行）请使用不带 `--clean` 的输出。

---

