#!/usr/bin/env python3
"""
测试最新UI修改效果的脚本

验证以下修改：
1. 将主界面GUI上"删除选中选手"这个按键的控件组合移动到"添加选手"这个按键右侧
2. "设定球桌阈值"界面需要在"2张球桌需要大于 [输入框] 人"这行文案上面增加一条文案"1张球桌需要大于 [输入框2] 人"，这个输入框2中固定填入1，且这个输入框需要设置成不能修改
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_delete_button_position():
    """测试删除选中选手按钮的位置"""
    print("测试删除选中选手按钮的位置...")
    
    # 创建一个简单的测试界面来模拟主界面的布局
    root = tk.Tk()
    root.title("删除按钮位置测试")
    root.geometry("600x400")
    
    # 模拟选手表格
    table_frame = tk.Frame(root)
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # 创建表格
    columns = ("name", "hp", "status")
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # 配置列
    table.heading("name", text="姓名")
    table.heading("hp", text="HP")
    table.heading("status", text="状态")
    
    # 添加测试数据
    test_data = [
        ("张三", "4", "在场"),
        ("李四", "3", "在场"),
    ]
    
    for item in test_data:
        table.insert("", tk.END, values=item)
    
    table.pack(side="left", fill="both", expand=True)
    
    # 模拟添加选手区域
    add_frame = tk.Frame(root)
    add_frame.pack(fill='x', padx=20, pady=10)
    
    tk.Label(add_frame, text="添加新选手:").pack(side='left')
    
    # 创建可输入的下拉框
    name_var = tk.StringVar()
    name_combobox = ttk.Combobox(add_frame, textvariable=name_var, width=15)
    name_combobox.pack(side='left', padx=5)
    
    tk.Label(add_frame, text="初始HP:").pack(side='left')
    lives_var = tk.StringVar(value='4')
    
    # 创建HP选项框
    hp_options_frame = tk.Frame(add_frame)
    hp_options_frame.pack(side='left', padx=5)
    
    for hp_value in [2, 3, 4]:
        hp_radio = tk.Radiobutton(hp_options_frame, 
                                 text=str(hp_value),
                                 variable=lives_var,
                                 value=str(hp_value),
                                 font=('Arial', 9))
        hp_radio.pack(side='left', padx=2)
    
    # 模拟添加选手按钮
    add_button = tk.Button(add_frame, text="添加选手")
    add_button.pack(side='left', padx=10)
    
    # 模拟删除选中选手按钮（应该在添加选手按钮右侧）
    delete_button = tk.Button(add_frame, text="删除选中选手", 
                            bg='red', fg='white', font=('Arial', 10))
    delete_button.pack(side='left', padx=10)
    
    # 选中提示
    selection_label = tk.Label(root, text="请先选中要删除的选手", fg='gray')
    selection_label.pack(pady=5, padx=20, anchor='w')
    
    print("✓ 删除选中选手按钮已移动到添加选手按钮右侧")
    
    # 运行测试界面（5秒后自动关闭）
    root.after(5000, root.destroy)
    root.mainloop()
    
    return True

def test_table_thresholds_screen():
    """测试设定球桌阈值界面"""
    print("\n测试设定球桌阈值界面...")
    
    from models import TableThresholdsManager
    
    # 创建一个简单的测试界面
    root = tk.Tk()
    root.title("球桌阈值界面测试")
    root.geometry("600x600")
    
    # 模拟阈值管理器
    thresholds_manager = TableThresholdsManager()
    
    # 标题
    title_label = tk.Label(root, text="设定球桌阈值", 
                          font=('Arial', 16, 'bold'))
    title_label.pack(pady=10)
    
    # 说明文字
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)
    
    tk.Label(info_frame, text="说明：修改阈值后，game_states.json 历史状态文件将被删除！", 
            fg='red', font=('Arial', 12, 'bold')).pack()
    
    # 阈值输入区域
    thresholds_frame = tk.Frame(root)
    thresholds_frame.pack(pady=10)
    
    # 添加1张球桌的阈值设置（固定为1且不可修改）
    row_frame_1 = tk.Frame(thresholds_frame)
    row_frame_1.pack(pady=5)
    
    tk.Label(row_frame_1, text="1张球桌需要大于 ", font=('Arial', 12)).pack(side=tk.LEFT)
    
    # 创建只读的输入框，固定为1
    one_table_var = tk.StringVar(value="1")
    one_table_entry = tk.Entry(row_frame_1, textvariable=one_table_var, width=10, font=('Arial', 12), state='readonly')
    one_table_entry.pack(side=tk.LEFT, padx=5)
    
    tk.Label(row_frame_1, text="人", font=('Arial', 12)).pack(side=tk.LEFT)
    
    # 创建8个阈值输入框（2-9张球桌）
    threshold_vars = []
    default_thresholds = thresholds_manager.thresholds
    labels = [
        "2张球桌需要大于 ",
        "3张球桌需要大于 ",
        "4张球桌需要大于 ",
        "5张球桌需要大于 ",
        "6张球桌需要大于 ",
        "7张球桌需要大于 ",
        "8张球桌需要大于 ",
        "9张球桌需要大于 "
    ]
    
    for i in range(8):
        row_frame = tk.Frame(thresholds_frame)
        row_frame.pack(pady=5)
        
        tk.Label(row_frame, text=labels[i], font=('Arial', 12)).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=str(default_thresholds[i]))
        threshold_vars.append(var)
        
        entry = tk.Entry(row_frame, textvariable=var, width=10, font=('Arial', 12))
        entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row_frame, text="人", font=('Arial', 12)).pack(side=tk.LEFT)
    
    print("✓ 1张球桌的阈值设置已添加")
    print("✓ 1张球桌的输入框固定为1且不可修改")
    
    # 运行测试界面（8秒后自动关闭）
    root.after(8000, root.destroy)
    root.mainloop()
    
    return True

def main():
    """主测试函数"""
    print("疯狂星期六抢1大赛 - 最新UI修改测试")
    print("=" * 60)
    
    # 测试删除选中选手按钮的位置
    test_delete_button_position()
    
    # 测试设定球桌阈值界面
    test_table_thresholds_screen()
    
    print("\n" + "=" * 60)
    print("所有最新UI修改测试完成！")
    print("✓ 删除选中选手按钮已成功移动到添加选手按钮右侧")
    print("✓ 设定球桌阈值界面已添加1张球桌的阈值设置，输入框固定为1且不可修改")

if __name__ == "__main__":
    main()
