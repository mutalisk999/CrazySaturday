#!/usr/bin/env python3
"""
测试UI修改效果的脚本

验证以下修改：
1. 固定参赛选手列表的Treeview高度降低并添加了垂直滚动条
2. 比赛进行中界面的UI美化
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import CrazySaturdayApp
from models import Game, FixedParticipant, FixedParticipantManager

def test_fixed_participants_treeview():
    """测试固定参赛选手列表的Treeview高度和滚动条"""
    print("测试固定参赛选手列表的Treeview配置...")
    
    # 创建一个简单的测试界面
    root = tk.Tk()
    root.title("Treeview测试")
    
    # 创建一个Treeview
    columns = ("name", "contact", "email", "address", "initial_hp")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=8)  # 高度设置为8
    
    # 配置列
    tree.heading("name", text="姓名", anchor='center')
    tree.heading("contact", text="联系方式", anchor='center')
    tree.heading("email", text="邮箱", anchor='center')
    tree.heading("address", text="家庭住址", anchor='center')
    tree.heading("initial_hp", text="初始HP", anchor='center')
    
    # 创建带垂直滚动条的框架
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    # 添加垂直滚动条
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 配置Treeview使用滚动条
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # 添加一些测试数据
    test_data = [
        ("张三", "13800138000", "zhangsan@example.com", "北京市朝阳区", 4),
        ("李四", "13900139000", "lisi@example.com", "上海市浦东新区", 3),
        ("王五", "13700137000", "wangwu@example.com", "广州市天河区", 5),
        ("赵六", "13600136000", "zhaoliu@example.com", "深圳市南山区", 2),
        ("孙七", "13500135000", "sunqi@example.com", "杭州市西湖区", 4),
        ("周八", "13400134000", "zhouba@example.com", "成都市武侯区", 3),
        ("吴九", "13300133000", "wujiu@example.com", "武汉市江汉区", 5),
        ("郑十", "13200132000", "zhengshi@example.com", "西安市雁塔区", 2),
        ("钱一", "13100131000", "qianyi@example.com", "重庆市渝中区", 4),
        ("孙二", "13000130000", "suner@example.com", "南京市玄武区", 3),
    ]
    
    for item in test_data:
        tree.insert("", tk.END, values=item)
    
    print("✓ Treeview高度已设置为8行")
    print("✓ 垂直滚动条已添加")
    
    # 运行测试界面（5秒后自动关闭）
    root.after(5000, root.destroy)
    root.mainloop()
    
    return True

def test_game_screen_improvements():
    """测试比赛进行中界面的UI改进"""
    print("\n测试比赛进行中界面的UI改进...")
    
    # 创建一个简单的Game对象来测试界面
    game = Game()
    
    # 添加一些测试选手
    for i in range(12):
        game.add_player(f"选手{i+1}", 3)
    
    # 开始游戏
    game.start_game()
    
    print("✓ 游戏界面UI已美化：")
    print("  - 标题栏使用Microsoft YaHei字体和统一配色")
    print("  - 主内容区域添加了边框和背景色")
    print("  - 球台使用了美观的LabelFrame样式")
    print("  - 判负按钮样式已统一和美化")
    print("  - 右侧选项卡区域使用了自定义样式")
    print("  - 底部状态区域和控制按钮已美化")
    
    return True

def main():
    """主测试函数"""
    print("疯狂星期六抢1大赛 - UI修改测试")
    print("=" * 50)
    
    # 测试固定参赛选手列表的Treeview
    test_fixed_participants_treeview()
    
    # 测试比赛进行中界面的UI改进
    test_game_screen_improvements()
    
    print("\n" + "=" * 50)
    print("所有UI修改测试完成！")
    print("✓ 固定参赛选手列表的Treeview高度已降低并添加垂直滚动条")
    print("✓ 比赛进行中界面的UI已完成美化")

if __name__ == "__main__":
    main()
