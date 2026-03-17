#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打包脚本 - 使用PyInstaller打包疯狂星期六程序
"""

import PyInstaller.__main__
import os

def main():
    """主打包函数"""
    print("开始打包疯狂星期六程序...")
    
    # PyInstaller配置参数
    params = [
        'crazy_saturday.py',           # 主程序文件
        '--name=CrazySaturday',        # 可执行文件名称
        '--onefile',                   # 打包成单个可执行文件
        '--windowed',                  # 窗口程序（不显示控制台）
        '--icon=NONE',                 # 不使用图标
        '--add-data=.;.',              # 添加当前目录所有文件
        '--clean',                     # 清理临时文件
        '--noconfirm',                 # 不确认覆盖
    ]
    
    print("打包参数:", params)
    
    try:
        # 执行打包
        PyInstaller.__main__.run(params)
        print("✅ 打包完成！")
        print("可执行文件位置: dist/CrazySaturday.exe")
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())