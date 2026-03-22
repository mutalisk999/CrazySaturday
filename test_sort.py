# 测试胜率排序逻辑

class MockPlayer:
    def __init__(self, name, wins, losses):
        self.name = name
        self.wins = wins
        self.losses = losses

# 创建测试数据
players = [
    MockPlayer("A", 5, 5),  # 胜率 0.5
    MockPlayer("B", 8, 2),  # 胜率 0.8
    MockPlayer("C", 2, 8),  # 胜率 0.2
    MockPlayer("D", 0, 0),  # 胜率 0.0
    MockPlayer("E", 3, 0),  # 胜率 1.0
    MockPlayer("F", 7, 3),  # 胜率 0.7
]

# 测试降序排序
print("=== 降序排序 (reverse=True) ===")
sorted_desc = sorted(players, key=lambda p: float(p.wins) / float(p.wins + p.losses) if (p.wins + p.losses) > 0 else 0.0, reverse=True)
for p in sorted_desc:
    total = p.wins + p.losses
    rate = p.wins / total if total > 0 else 0.0
    print(f"{p.name}: {p.wins}胜 {p.losses}负, 胜率: {rate:.2f}")

# 测试升序排序
print("\n=== 升序排序 (reverse=False) ===")
sorted_asc = sorted(players, key=lambda p: float(p.wins) / float(p.wins + p.losses) if (p.wins + p.losses) > 0 else 0.0, reverse=False)
for p in sorted_asc:
    total = p.wins + p.losses
    rate = p.wins / total if total > 0 else 0.0
    print(f"{p.name}: {p.wins}胜 {p.losses}负, 胜率: {rate:.2f}")
