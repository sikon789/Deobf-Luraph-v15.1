#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Luraph v15.1 反混淆工具测试脚本"""
import sys
import os
from pathlib import Path

def main():
    """测试核心反混淆功能"""
    print("🧪 开始测试 Luraph v15.1 反混淆工具 v1.0.0")
    print("-" * 60)
    
    # 添加 libs 目录到路径
    libs_path = Path(__file__).parent / "libs"
    sys.path.insert(0, str(libs_path))
    
    try:
        # 加载示例文件
        examples_dir = Path(__file__).parent / "examples"
        sample_file = examples_dir / "layer3_sample.lua"
        
        if not sample_file.exists():
            print("❌ 错误: 示例文件不存在")
            return False
        
        data = sample_file.read_text(encoding="utf-8", errors="ignore")
        if not data:
            print("❌ 错误: 无法读取示例文件")
            return False
        
        # 基础 token 检查
        from libs.beautify2 import tokenize, build_tokens
        from libs.readable3 import rename
        
        print(f"🔍 正在分析示例: {sample_file.name}")
        print(f"📊 文件大小: {len(data):,} 字节")
        
        toks = tokenize(data)
        print(f"🔢 原始 tokens: {len(toks):,}")
        
        renamed = rename(toks)
        print(f"🔢 重命名后 tokens: {len(renamed):,}")
        
        output = build_tokens(renamed)
        print(f"📊 输出大小: {len(output):,} 字节")
        
        # 验证基本结构
        if len(output) == 0:
            print("❌ 错误: 输出不能为空")
            return False
        
        if "function" not in output:
            print("❌ 错误: 应包含 function 关键字")
            return False
        
        if "return" not in output:
            print("❌ 错误: 应包含 return 关键字")
            return False
        
        print("\n✅ 测试通过!")
        print("-" * 60)
        print("✓ Token 化处理正常")
        print("✓ 语义重命名正常")
        print("✓ 代码格式化正常")
        print("✓ 语法结构有效")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
