#!/usr/bin/env python3
"""
疯狂星期六抢1大赛 - 主程序入口

这是一个基于tkinter的乒乓球比赛模拟游戏，完全按照rules.md文档中的规则实现。
"""

from gui import CrazySaturdayApp

def main():
    """主程序入口"""
    app = CrazySaturdayApp()
    app.run()

if __name__ == "__main__":
    main()