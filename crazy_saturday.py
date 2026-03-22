#!/usr/bin/env python3
"""
疯狂星期六抢1大赛 - 主程序入口

这是一个基于tkinter的桌球比赛模拟游戏，完全按照rules.md文档中的规则实现。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import CrazySaturdayApp

def main():
    """主程序入口"""
    app = CrazySaturdayApp()
    app.run()

if __name__ == "__main__":
    main()