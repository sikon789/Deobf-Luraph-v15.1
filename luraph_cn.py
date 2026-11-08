#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luraph v15.1 一键反混淆工具 - 带清理模式
版本：v1.1.0

使用方法:
    python luraph_cn_clean.py <输入文件> -o <输出文件> [--clean]

示例:
    python luraph_cn_clean.py StealAnEggg.txt -o output.lua --clean
    python luraph_cn_clean.py protected.lua -o output_deob.lua
"""
import sys
import os
import argparse
from pathlib import Path

# 添加 libs 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "libs"))

def main():
    parser = argparse.ArgumentParser(
        description="Luraph v15.1 一键反混淆工具（带清理功能）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
作者：开放源代码项目
版本：v1.1.0
许可：MIT License

示例:
  python luraph_cn_clean.py input.lua -o output.lua
  python luraph_cn_clean.py input.txt -o output.lua --clean
  
--clean 选项会移除框架残留、调试代码和死代码，保留核心业务逻辑。
        """
    )
    parser.add_argument(
        "input",
        help="受 Luraph v15.1 保护的 .lua 或 .txt 文件"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出文件名 (默认使用输入文件名 _deob.lua)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细处理信息"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="清理框架残留、调试代码和死代码，只保留核心业务逻辑"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖已存在的输出文件"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件 '{input_path}' 不存在")
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"错误: '{input_path}' 不是一个文件")
        sys.exit(1)
    
    # 读取输入
    try:
        data = input_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"错误: 读取文件失败: {e}")
        sys.exit(1)
    
    if not data.strip():
        print("错误: 输入文件内容为空")
        sys.exit(1)
    
    try:
        # 导入核心模块
        from libs.beautify2 import tokenize, build_tokens
        from libs.readable3 import rename
        
        if args.verbose:
            print(f"正在处理: {input_path.name}")
            print(f"输入大小: {len(data):,} 字节")
        
        # 执行反混淆
        toks = tokenize(data)
        renamed = rename(toks)
        
        # 清理模式
        if args.clean:
            if args.verbose:
                print("正在执行清理模式...")
            from libs.cleanup import cleanup_luraph_v2 as cleanup_luraph
            renamed = cleanup_luraph(renamed, keep_business=True)
            output = build_tokens(renamed)
            if args.verbose:
                print(f"清理后令牌数: {len(renamed):,}")
        else:
            output = build_tokens(renamed)
        
        # 确定输出路径
        if args.output:
            out_path = Path(args.output)
        else:
            if args.clean:
                out_path = input_path.with_name(
                    input_path.stem + "_cleaned.lua"
                )
            else:
                out_path = input_path.with_name(
                    input_path.stem + "_反混淆化.lua"
                )
        
        # 检查是否覆盖
        if out_path.exists() and not args.force:
            print(f"警告: 文件 '{out_path}' 已存在")
            print("请使用 --force 参数覆盖")
            sys.exit(1)
        
        # 写出结果
        out_path.write_text(output, encoding="utf-8")
        
        print(f"\n✓ 反混淆完成!")
        print(f"输出文件: {out_path.absolute()}")
        print(f"文件熵大小: {len(output):,} 字节")
        
        if args.verbose:
            print(f"\n处理统计:")
            print(f"  原始 tokens: {len(toks):,}")
            print(f"  重命名后 tokens: {len(renamed):,}")
            print(f"  格式化后字节: {len(output):,}")
            print(f"  压缩率: {len(output)/len(data)*100:.1f}%")
        
        if args.clean:
            print(f"\n清理模式已启用 - 移除了框架残留和死代码")
        
    except Exception as e:
        print(f"错误: 反混淆过程中发生异常")
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"详情: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
