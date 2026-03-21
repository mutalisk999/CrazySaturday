#!/usr/bin/env python3
"""
测试脚本：验证球桌挑战者判负后的撤桌逻辑
场景：某球桌 擂主hp 2/3 挑战者hp 1/2，桌上没有候补，场外也没有候补
"""

from models import Game

# 创建游戏实例
game = Game()

# 设置测试模式 - 添加足够的选手，确保使用多个球台
# 设置为9个选手，应该使用4张球台（根据规则：15-17人使用4张球台？不，让我查一下calculate_required_tables方法）
# calculate_required_tables方法：
# 2-6人：1张
# 7-10人：2张
# 11-14人：3张
# 15-17人：4张
# 所以添加15个选手，确保使用4张球台
for i in range(15):
    initial_hp = 3 if i == 0 else 2  # 第一个选手初始HP为3，其他人初始HP为2
    game.add_player(f'选手{i+1}', initial_hp)

# 开始游戏
game.start_game()

# 查看实际创建的球台
print("实际创建的球台：")
for table in game.tables:
    print(f"球台{table.table_id}，状态：{table.active}")

# 选择第一个球台进行测试
table = game.tables[0]
table_id = table.table_id

# 找到对应的选手
player1 = table.host  # 擂主
player2 = table.challenger  # 挑战者

# 确保球台状态符合测试场景：擂主hp 2/3，挑战者hp 1/2，桌上没有候补，场外也没有候补
print("\n设置测试场景...")

# 手动调整选手HP
if player1:
    player1.current_lives = 2  # 设置为2/3 HP
    player1.initial_lives = 3
if player2:
    player2.current_lives = 1  # 设置为1/2 HP
    player2.initial_lives = 2

# 清空球台候补和场外候补区
table.waiting = []
game.outside_waiting = []

print(f"\n{table_id}号球台初始状态：")
print(f"擂主={player1.name}({player1.current_lives}/{player1.initial_lives})，挑战者={player2.name}({player2.current_lives}/{player2.initial_lives})，候补={len(table.waiting)}")
print(f"场外候补区人数：{len(game.outside_waiting)}")
print(f"需要关闭的球台：{list(game.tables_to_close.keys())}")

# 模拟判定挑战者负
print(f"\n执行{table_id}号球台挑战者判负操作...")
game.eliminate_player(player2, table_id)

print(f"\n操作后状态：")
print(f"{table_id}号球台是否活跃：{table.active}")
print(f"擂主状态：{player1.name}，位置={player1.position}，HP={player1.current_lives}/{player1.initial_lives}")
print(f"挑战者状态：{player2.name}，位置={player2.position}，HP={player2.current_lives}/{player2.initial_lives}")
print(f"场外候补区：{[p.name for p in game.outside_waiting]}")
print(f"需要关闭的球台：{list(game.tables_to_close.keys())}")
print(f"正在关闭的球台：{list(game.closing_tables.keys())}")

# 验证修复结果
if not table.active:
    print(f"\n✅ 测试通过：{table_id}号球台已成功关闭")
    if player1.position == "场外候补" and player1.current_lives == 2:
        print("✅ 测试通过：擂主已正确移动到场外候补区，HP保持2/3不变")
    else:
        print(f"❌ 测试失败：擂主未正确处理，位置={player1.position}，HP={player1.current_lives}/{player1.initial_lives}")
    if player2.position == "已淘汰" and player2.current_lives == 0:
        print("✅ 测试通过：挑战者已正确淘汰")
    else:
        print(f"❌ 测试失败：挑战者未正确淘汰，位置={player2.position}，HP={player2.current_lives}/{player2.initial_lives}")
else:
    print(f"\n❌ 测试失败：{table_id}号球台未关闭")
