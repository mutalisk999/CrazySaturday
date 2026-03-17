import random
from typing import List, Dict, Optional

class Player:
    def __init__(self, name: str, initial_lives: int):
        self.name = name
        self.initial_lives = initial_lives
        self.current_lives = initial_lives
        self.position = "场外候补"
        self.table_id = None
        self.wins = 0
        self.losses = 0
        self.streak = 0
        self.max_streak = 0
        
    def lose_life(self):
        if self.current_lives > 0:
            self.current_lives -= 1
            return True
        return False
    
    def is_eliminated(self):
        return self.current_lives <= 0
    
    def win_match(self):
        self.wins += 1
        self.streak += 1
        if self.streak > self.max_streak:
            self.max_streak = self.streak
    
    def lose_match(self):
        self.losses += 1
        self.streak = 0

class Table:
    def __init__(self, table_id: int):
        self.table_id = table_id
        self.host = None  # 擂主
        self.challenger = None  # 挑战者
        self.waiting = []  # 球台候补
        self.active = True
    
    def has_match(self):
        return self.host is not None and self.challenger is not None
    
    def add_player(self, player: Player, position: str):
        if position == "擂主":
            self.host = player
            player.position = f"{self.table_id}号台擂主"
            player.table_id = self.table_id
        elif position == "挑战者":
            self.challenger = player
            player.position = f"{self.table_id}号台挑战者"
            player.table_id = self.table_id
        elif position == "候补":
            self.waiting.append(player)
            player.position = f"{self.table_id}号台候补"
            player.table_id = self.table_id

class Game:
    def __init__(self):
        self.players = []
        self.tables = []
        self.outside_waiting = []  # 场外候补
        self.eliminated = []  # 已淘汰选手
        self.game_state = "setup"  # setup, running, finished
        self.current_match_table = None
        self.winner = None
        
        # 球台使用顺序
        self.table_priority = [2, 3, 4, 5, 6, 7, 8, 9, 1]
        self.table_close_order = [1, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # 人数阈值对应的球台数量
        self.table_thresholds = {
            2: 1, 7: 2, 11: 3, 15: 4, 18: 5, 21: 6, 25: 7, 28: 8, 32: 9
        }
    
    def setup_tables(self, player_count: int):
        # 根据人数确定球台数量
        table_count = 1
        for threshold, count in sorted(self.table_thresholds.items()):
            if player_count >= threshold:
                table_count = count
        
        # 创建球台
        self.tables = []
        tables_to_use = self.table_priority[:table_count]
        for table_id in tables_to_use:
            self.tables.append(Table(table_id))
    
    def is_name_duplicate(self, name: str) -> bool:
        """检查姓名是否已存在"""
        return any(player.name == name for player in self.players)
    
    def add_player(self, name: str, initial_lives: int) -> bool:
        """添加选手，如果姓名重复则返回False"""
        if self.is_name_duplicate(name):
            return False
        player = Player(name, initial_lives)
        self.players.append(player)
        return True
    
    def remove_player(self, index: int):
        """删除指定索引的选手"""
        if 0 <= index < len(self.players):
            return self.players.pop(index)
        return None
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        
        self.setup_tables(len(self.players))
        
        # 随机分配选手到球台区和场外候补区
        random.shuffle(self.players)
        
        # 分配选手到球台
        table_index = 0
        for i, player in enumerate(self.players):
            if i < len(self.tables) * 3:  # 每个球台最多3人
                table = self.tables[table_index]
                if len(table.waiting) == 0 and table.host is None:
                    table.add_player(player, "擂主")
                elif len(table.waiting) == 0 and table.challenger is None:
                    table.add_player(player, "挑战者")
                else:
                    table.add_player(player, "候补")
                
                table_index = (table_index + 1) % len(self.tables)
            else:
                self.outside_waiting.append(player)
                player.position = "场外候补"
        
        self.game_state = "running"
        return True
    
    def get_active_tables_count(self):
        return sum(1 for table in self.tables if table.active)
    
    def get_remaining_players_count(self):
        return len([p for p in self.players if not p.is_eliminated()])
    
    def check_table_reduction(self):
        remaining_players = self.get_remaining_players_count()
        
        # 检查是否需要减少球台
        for threshold, table_count in self.table_thresholds.items():
            if remaining_players == threshold - 1:
                # 需要关闭球台
                tables_to_close = self.table_close_order[:len(self.tables) - table_count + 1]
                for table_id in tables_to_close:
                    if table_id in [t.table_id for t in self.tables if t.active]:
                        self.close_table(table_id)
    
    def close_table(self, table_id: int):
        for table in self.tables:
            if table.table_id == table_id and table.active:
                table.active = False
                
                # 将球台上的选手移到场外候补区
                if table.host:
                    self.outside_waiting.append(table.host)
                    table.host.position = "场外候补"
                    table.host.table_id = None
                if table.challenger:
                    self.outside_waiting.append(table.challenger)
                    table.challenger.position = "场外候补"
                    table.challenger.table_id = None
                for player in table.waiting:
                    self.outside_waiting.append(player)
                    player.position = "场外候补"
                    player.table_id = None
                
                table.host = None
                table.challenger = None
                table.waiting = []
                break
    
    def play_match(self, table: Table):
        if not table.has_match():
            return None
        
        # 简单随机决定胜负
        winner = random.choice([table.host, table.challenger])
        loser = table.challenger if winner == table.host else table.host
        
        # 更新统计数据
        winner.win_match()
        loser.lose_match()
        
        # 败者失去一条命
        loser_lost_life = loser.lose_life()
        
        # 位置轮转
        self.rotate_positions(table, winner, loser, loser_lost_life)
        
        return winner, loser
    
    def rotate_positions(self, table: Table, winner: Player, loser: Player, loser_lost_life: bool):
        # 败者移到场外候补区队尾
        if not loser.is_eliminated():
            self.outside_waiting.append(loser)
            loser.position = "场外候补"
            loser.table_id = None
        else:
            self.eliminated.append(loser)
            loser.position = "已淘汰"
            loser.table_id = None
        
        # 胜者成为擂主
        table.host = winner
        winner.position = f"{table.table_id}号台擂主"
        
        # 球台候补区第一个成为挑战者
        if table.waiting:
            table.challenger = table.waiting.pop(0)
            table.challenger.position = f"{table.table_id}号台挑战者"
        else:
            table.challenger = None
        
        # 场外候补区第一个成为球台候补
        if self.outside_waiting and table.active:
            new_waiting = self.outside_waiting.pop(0)
            table.waiting.append(new_waiting)
            new_waiting.position = f"{table.table_id}号台候补"
            new_waiting.table_id = table.table_id
    
    def eliminate_player(self, player, table_id):
        """淘汰选手 - HP减1后根据剩余HP移动到相应区域，并调整球台位置"""
        # 检查选手是否存在
        if player not in self.players:
            return False
        
        # 找到对应的球台
        table = None
        for t in self.tables:
            if t.table_id == table_id:
                table = t
                break
        
        if not table:
            return False
        
        # HP减1
        player.current_lives -= 1
        
        # 记录选手的原始位置
        was_host = (table.host == player)
        was_challenger = (table.challenger == player)
        
        # 根据HP值决定移动位置
        if player.current_lives <= 0:
            # HP为0，移动到淘汰区（彻底被淘汰）
            player.current_lives = 0
            self.move_to_eliminated(player, table_id)
            
            # 如果被淘汰的是挑战者，需要调整球台位置
            if was_challenger:
                self.adjust_table_positions_after_challenger_elimination(table)
        else:
            # HP大于0，移动到候补区尾部（本局离场）
            self.move_to_waiting(player, table_id)
            
            # 本局离场需要调整球台位置
            if was_host:
                self.adjust_table_positions_after_host_elimination(table)
            elif was_challenger:
                self.adjust_table_positions_after_challenger_elimination(table)
        
        return True
    
    def adjust_table_positions_after_host_elimination(self, table):
        """擂主被淘汰后调整球台位置"""
        # 挑战者变成擂主
        if table.challenger:
            table.host = table.challenger
            table.host.position = f"{table.table_id}号台擂主"
            table.challenger = None
        else:
            table.host = None
        
        # 候补者补位成挑战者
        if table.waiting:
            table.challenger = table.waiting.pop(0)
            table.challenger.position = f"{table.table_id}号台挑战者"
        
        # 从场外候补区头部选择进入这张球台的候补区
        if self.outside_waiting and table.active:
            new_waiting = self.outside_waiting.pop(0)
            table.waiting.append(new_waiting)
            new_waiting.position = f"{table.table_id}号台候补"
            new_waiting.table_id = table.table_id
    
    def adjust_table_positions_after_challenger_elimination(self, table):
        """挑战者被淘汰后调整球台位置"""
        # 擂主不变
        # 候补者补位成挑战者
        if table.waiting:
            table.challenger = table.waiting.pop(0)
            table.challenger.position = f"{table.table_id}号台挑战者"
        else:
            table.challenger = None
        
        # 从场外候补区头部选择进入这张球台的候补区
        if self.outside_waiting and table.active:
            new_waiting = self.outside_waiting.pop(0)
            table.waiting.append(new_waiting)
            new_waiting.position = f"{table.table_id}号台候补"
            new_waiting.table_id = table.table_id
    
    def move_to_waiting(self, player, table_id):
        """将选手移动到候补区尾部"""
        # 从当前位置移除选手
        self.remove_player_from_current_position(player, table_id)
        
        # 移动到场外候补区尾部（本局离场）
        self.outside_waiting.append(player)
        player.position = "场外候补"
        player.table_id = None
    
    def move_to_eliminated(self, player, table_id):
        """将选手移动到淘汰区"""
        # 从当前位置移除选手
        self.remove_player_from_current_position(player, table_id)
        
        # 移动到淘汰区
        self.eliminated.append(player)
        player.position = "已淘汰"
        player.table_id = None
    
    def remove_player_from_current_position(self, player, table_id):
        """从当前位置移除选手"""
        # 从球台移除
        for table in self.tables:
            if table.table_id == table_id:
                if table.host == player:
                    table.host = None
                elif table.challenger == player:
                    table.challenger = None
                elif player in table.waiting:
                    table.waiting.remove(player)
                break
        
        # 从场外候补区移除
        if player in self.outside_waiting:
            self.outside_waiting.remove(player)
    
    def update(self):
        if self.game_state != "running":
            return
        
        # 检查比赛是否结束
        remaining_players = self.get_remaining_players_count()
        if remaining_players <= 1:
            self.game_state = "finished"
            if remaining_players == 1:
                self.winner = [p for p in self.players if not p.is_eliminated()][0]
            return
        
        # 检查是否需要减少球台
        self.check_table_reduction()
        
        # 在每个活跃球台上进行比赛
        for table in self.tables:
            if table.active and table.has_match():
                self.play_match(table)