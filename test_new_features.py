#!/usr/bin/env python3
"""测试新功能"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Game, TableThresholdsManager

def test_initial_table_count():
    """测试初始球台数量设置"""
    print("测试1: 初始球台数量设置")
    
    # 创建游戏实例
    game = Game()
    
    # 测试默认值
    assert game.initial_table_count == 9, f"默认球台数量应该是9，实际是{game.initial_table_count}"
    print("✓ 默认球台数量正确：9")
    
    # 测试设置不同的球台数量
    game.initial_table_count = 5
    assert game.initial_table_count == 5, f"球台数量应该是5，实际是{game.initial_table_count}"
    print("✓ 设置球台数量正确：5")
    
    print("测试1通过！\n")

def test_setup_tables():
    """测试球台初始化"""
    print("测试2: 球台初始化")
    
    game = Game()
    
    # 测试默认初始化（9张球台）
    game.setup_tables()
    assert len(game.tables) == 9, f"应该有9张球台，实际有{len(game.tables)}张"
    print(f"✓ 默认初始化球台数量正确：{len(game.tables)}张")
    
    # 验证球台顺序
    expected_order = [2, 3, 4, 5, 6, 7, 8, 9, 1]
    actual_order = [t.table_id for t in game.tables]
    assert actual_order == expected_order, f"球台顺序应该是{expected_order}，实际是{actual_order}"
    print(f"✓ 球台顺序正确：{actual_order}")
    
    # 测试自定义球台数量（5张）
    game.setup_tables(5)
    assert len(game.tables) == 5, f"应该有5张球台，实际有{len(game.tables)}张"
    print(f"✓ 自定义球台数量正确：{len(game.tables)}张")
    
    # 验证球台顺序
    expected_order = [2, 3, 4, 5, 6]
    actual_order = [t.table_id for t in game.tables]
    assert actual_order == expected_order, f"球台顺序应该是{expected_order}，实际是{actual_order}"
    print(f"✓ 自定义球台顺序正确：{actual_order}")
    
    print("测试2通过！\n")

def test_manual_close_table():
    """测试手动撤台"""
    print("测试3: 手动撤台")
    
    game = Game()
    game.setup_tables(5)
    
    # 添加测试选手
    for i in range(10):
        game.add_player(f"选手{i+1}", 3)
    
    # 开始游戏
    game.start_game(5)
    
    # 测试手动撤台
    initial_active_count = game.get_active_tables_count()
    print(f"初始活跃球台数量：{initial_active_count}")
    
    # 尝试撤掉2号球台
    success = game.manual_close_table(2)
    assert success, "撤台操作应该成功"
    print("✓ 撤台操作成功")
    
    # 验证球台是否被标记
    assert 2 in game.tables_to_close, "2号球台应该被标记为撤台"
    print("✓ 球台已标记为撤台")
    
    print("测试3通过！\n")

def test_state_save_restore():
    """测试状态保存和恢复"""
    print("测试4: 状态保存和恢复")
    
    game = Game()
    game.setup_tables(5)
    
    # 添加测试选手
    for i in range(10):
        game.add_player(f"选手{i+1}", 3)
    
    # 开始游戏
    game.start_game(5)
    
    # 保存初始状态
    initial_table_count = game.initial_table_count
    print(f"初始球台数量：{initial_table_count}")
    
    # 修改球台数量
    game.initial_table_count = 7
    
    # 恢复状态
    game.restore_state(0)
    
    # 验证球台数量是否恢复
    assert game.initial_table_count == initial_table_count, \
        f"球台数量应该恢复为{initial_table_count}，实际是{game.initial_table_count}"
    print(f"✓ 球台数量恢复正确：{game.initial_table_count}")
    
    print("测试4通过！\n")

def test_boundary_conditions():
    """测试边界条件"""
    print("测试5: 边界条件")
    
    game = Game()
    
    # 测试球台数量范围限制
    game.setup_tables(0)  # 应该被限制为1
    assert len(game.tables) == 1, f"球台数量应该被限制为1，实际是{len(game.tables)}"
    print("✓ 球台数量下限限制正确")
    
    game.setup_tables(15)  # 应该被限制为9
    assert len(game.tables) == 9, f"球台数量应该被限制为9，实际是{len(game.tables)}"
    print("✓ 球台数量上限限制正确")
    
    # 测试只剩最后一张球台时不能撤台
    game.setup_tables(1)
    for i in range(10):
        game.add_player(f"选手{i+1}", 3)
    game.start_game(1)
    
    success = game.manual_close_table(2)  # 2号球台是唯一活跃的球台
    assert not success, "只剩最后一张球台时应该不能撤台"
    print("✓ 最后一张球台撤台限制正确")
    
    print("测试5通过！\n")

if __name__ == "__main__":
    print("=" * 60)
    print("开始测试新功能")
    print("=" * 60 + "\n")
    
    try:
        test_initial_table_count()
        test_setup_tables()
        test_manual_close_table()
        test_state_save_restore()
        test_boundary_conditions()
        
        print("=" * 60)
        print("所有测试通过！✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ 测试失败：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
