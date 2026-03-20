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
        self.table_close_order = [1, 9, 8, 7, 6, 5, 4, 3, 2]  # 减桌顺序：优先撤最后使用的球台
        
        # 人数阈值对应的球台数量
        self.table_thresholds = {
            2: 1, 7: 2, 11: 3, 15: 4, 18: 5, 21: 6, 25: 7, 28: 8, 32: 9
        }
        
        # 减桌相关状态
        self.tables_to_close = {}  # 需要关闭的球台字典 {table_id: True}
        self.closing_tables = {}   # 正在关闭过程中的球台
        self.table_reduction_callback = None  # 减桌回调函数
        
        # 已离场桌台队列（用于重新安排选手）
        self.leftover_tables_queue = []  # 已离场的桌台号队列
    
    def calculate_required_tables(self, player_count: int) -> int:
        """根据选手数量计算需要的球台数量"""
        if player_count < 2:
            return 0
        elif player_count <= 6:
            return 1
        elif player_count <= 10:
            return 2
        elif player_count <= 14:
            return 3
        elif player_count <= 17:
            return 4
        elif player_count <= 20:
            return 5
        elif player_count <= 24:
            return 6
        elif player_count <= 27:
            return 7
        elif player_count <= 31:
            return 8
        else:
            return 9
    
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
    
    def set_table_reduction_callback(self, callback):
        """设置减桌回调函数"""
        self.table_reduction_callback = callback
    
    def get_table_players_info(self, table):
        """获取球台选手信息"""
        players_info = []
        
        if table.host:
            players_info.append(f"擂主: {table.host.name}({table.host.current_lives}/{table.host.initial_lives})")
        if table.challenger:
            players_info.append(f"挑战者: {table.challenger.name}({table.challenger.current_lives}/{table.challenger.initial_lives})")
        for i, player in enumerate(table.waiting):
            players_info.append(f"候补{i+1}: {player.name}({player.current_lives}/{player.initial_lives})")
        
        return "\n".join(players_info) if players_info else "无选手"
    
    def check_table_reduction(self):
        """检查是否需要减少球台"""
        remaining_players = self.get_remaining_players_count()
        
        # 先清理已关闭的球台标记
        self.cleanup_closed_tables()
        
        # 清理后再计算当前球台数
        current_tables = self.get_active_tables_count()
        required_tables = self.calculate_required_tables(remaining_players)
        
        print(f"DEBUG: 减桌检查 - 剩余选手: {remaining_players}, 当前球台: {current_tables}, 需要球台: {required_tables}")
        print(f"DEBUG: tables_to_close: {list(self.tables_to_close.keys())}, closing_tables: {list(self.closing_tables.keys())}")
        
        if current_tables > required_tables:
            # 需要减少球台
            tables_to_close_count = current_tables - required_tables
            # 计算还需要标记多少个球台（排除已标记的）
            already_marked = len(self.tables_to_close)
            still_needed = max(0, tables_to_close_count - already_marked)
            print(f"DEBUG: 需要减少 {tables_to_close_count} 张球台，已标记 {already_marked} 张，还需标记 {still_needed} 张")
            if still_needed > 0:
                self.identify_tables_to_close(still_needed)
        else:
            # 如果不需要减桌，清理所有减桌标记
            if self.tables_to_close:
                print(f"DEBUG: 当前球台数({current_tables}) <= 需要球台数({required_tables})，清理所有减桌标记")
                self.tables_to_close.clear()
                self.closing_tables.clear()
    
    def identify_tables_to_close(self, count: int):
        """标识需要关闭的球台"""
        print(f"DEBUG: identify_tables_to_close - count: {count}")
        print(f"DEBUG: table_close_order: {self.table_close_order}")
        
        # 按照减桌顺序标识球台
        tables_identified = 0
        for table_id in self.table_close_order:
            if tables_identified >= count:
                print(f"DEBUG: 已达到需要关闭的球台数量({count})，停止标识")
                break
                
            table = self.get_table_by_id(table_id)
            print(f"DEBUG: 检查球台 {table_id}: active={table.active if table else None}, in_tables_to_close={table_id in self.tables_to_close if table else None}")
            
            if table and table.active and table_id not in self.tables_to_close:
                # 检查球台是否可以立即关闭
                if self.can_close_table_immediately(table):
                    print(f"DEBUG: 球台 {table_id} 可以立即关闭")
                    self.close_table_immediately(table)
                else:
                    # 标记为需要关闭的球台
                    print(f"DEBUG: 标记球台 {table_id} 为需要关闭")
                    self.tables_to_close[table_id] = True
                    self.closing_tables[table_id] = table
                tables_identified += 1
                print(f"DEBUG: 已标识 {tables_identified} 张球台")
        
        print(f"DEBUG: 已标记 {tables_identified} 张球台需要关闭")
    
    def cleanup_closed_tables(self):
        """清理已关闭的球台标记"""
        # 移除已经关闭的球台标记
        tables_to_remove = []
        for table_id in self.tables_to_close:
            table = self.get_table_by_id(table_id)
            if not table or not table.active:
                tables_to_remove.append(table_id)
        
        for table_id in tables_to_remove:
            if table_id in self.tables_to_close:
                del self.tables_to_close[table_id]
            if table_id in self.closing_tables:
                del self.closing_tables[table_id]
            print(f"DEBUG: 清理已关闭球台 {table_id} 的标记")
    
    def cleanup_closing_tables_if_needed(self, required_tables):
        """如果不需要减桌，清理多余的球台标记"""
        current_tables = self.get_active_tables_count()
        
        # 如果当前球台数等于或小于需要球台数，清理所有标记
        if current_tables <= required_tables and self.tables_to_close:
            print(f"DEBUG: 当前球台数({current_tables}) <= 需要球台数({required_tables})，清理所有减桌标记")
            self.tables_to_close.clear()
            self.closing_tables.clear()
    
    def can_close_table_immediately(self, table):
        """检查球台是否可以立即关闭"""
        # 如果球台没有任何选手或候补者，可以立即关闭
        return table.host is None and table.challenger is None and len(table.waiting) == 0
    
    def close_table_immediately(self, table):
        """立即关闭球台"""
        table.active = False
        print(f"球台 {table.table_id} 已立即关闭")
    
    def process_closing_table_after_elimination(self, table):
        """处理被标记为需要关闭的球台在判负离场后的逻辑"""
        if table.table_id not in self.tables_to_close:
            return
            
        # 候补者成为擂主或挑战者，不需要从场外候补区补充
        if table.waiting:
            # 候补者补位
            if table.challenger is None:
                table.challenger = table.waiting.pop(0)
                table.challenger.position = f"{table.table_id}号台挑战者"
            elif table.host is None:
                table.host = table.waiting.pop(0)
                table.host.position = f"{table.table_id}号台擂主"
        
        # 检查是否可以最终关闭球台
        if self.can_finally_close_table(table):
            self.finalize_table_closing(table)
    
    def can_finally_close_table(self, table):
        """检查是否可以最终关闭球台"""
        # 被标记球台：当擂主和挑战者只有一方存在时，就可以最终关闭
        # 不允许从场外候补区新增候补
        return (table.host is not None and table.challenger is None) or \
               (table.host is None and table.challenger is not None)
    
    def finalize_table_closing(self, table):
        """最终关闭球台"""
        # 被标记球台：当擂主和挑战者只有一方存在时，就可以最终关闭
        # 存在的一方需要移动到场外候补区尾部
        
        # 在真正触发撤桌行为时弹出对话框
        if self.table_reduction_callback:
            players_info = self.get_table_players_info(table)
            self.table_reduction_callback(table.table_id, players_info)
        
        # 处理擂主（如果存在）
        if table.host:
            if table.host.current_lives > 0:
                # HP大于0，进入场外候补区尾部
                self.outside_waiting.append(table.host)
                table.host.position = "场外候补"
            else:
                # HP等于0，进入淘汰区
                self.eliminated.append(table.host)
                table.host.position = "已淘汰"
            table.host.table_id = None
            table.host = None
        
        # 处理挑战者（如果存在）
        if table.challenger:
            if table.challenger.current_lives > 0:
                # HP大于0，进入场外候补区尾部
                self.outside_waiting.append(table.challenger)
                table.challenger.position = "场外候补"
            else:
                # HP等于0，进入淘汰区
                self.eliminated.append(table.challenger)
                table.challenger.position = "已淘汰"
            table.challenger.table_id = None
            table.challenger = None
        
        # 清空候补区
        for player in table.waiting:
            if player.current_lives > 0:
                self.outside_waiting.append(player)
                player.position = "场外候补"
            else:
                self.eliminated.append(player)
                player.position = "已淘汰"
            player.table_id = None
        table.waiting = []
        
        table.active = False
        if table.table_id in self.tables_to_close:
            del self.tables_to_close[table.table_id]
        del self.closing_tables[table.table_id]
        
        # 根据情况输出不同的关闭信息
        if table.host is not None and table.challenger is not None:
            print(f"球台 {table.table_id} 已最终关闭，擂主和挑战者双双被移除")
        elif table.host is not None:
            print(f"球台 {table.table_id} 已最终关闭，擂主移动到场外候补区尾部")
        elif table.challenger is not None:
            print(f"球台 {table.table_id} 已最终关闭，挑战者移动到场外候补区尾部")
        else:
            print(f"球台 {table.table_id} 已最终关闭")
    
    def get_table_by_id(self, table_id: int):
        """根据ID获取球台"""
        for table in self.tables:
            if table.table_id == table_id:
                return table
        return None
    
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
        
        # 将桌台加入已离场桌台队列（如果不在队列中且未被标记为需要关闭）
        if table.table_id not in self.leftover_tables_queue and table.table_id not in self.tables_to_close:
            self.leftover_tables_queue.append(table.table_id)
        
        # 特殊场景：如果球桌被标记为撤桌状态且候补为空，胜利者也要一起离场
        if table.table_id in self.tables_to_close and not table.waiting:
            # 将胜利者移动到场外候补区（HP不需要减1）
            if winner.current_lives > 0:
                self.outside_waiting.append(winner)
                winner.position = "场外候补"
                winner.table_id = None
            else:
                self.eliminated.append(winner)
                winner.position = "已淘汰"
                winner.table_id = None
            
            # 将擂主和挑战者都清空
            table.host = None
            table.challenger = None
            
            # 将桌台真正回收（标记为不活跃）
            table.active = False
            
            # 从tables_to_close中移除
            if table.table_id in self.tables_to_close:
                del self.tables_to_close[table.table_id]
            
            # 从closing_tables中移除
            if table.table_id in self.closing_tables:
                del self.closing_tables[table.table_id]
            
            # 从已离场桌台队列中移除
            if table.table_id in self.leftover_tables_queue:
                self.leftover_tables_queue.remove(table.table_id)
            
            print(f"特殊场景：{table.table_id}号球台被标记为撤桌且候补为空，胜利者 {winner.name} 一起离场")
        
        # 场外候补区第一个成为球台候补
        # 如果球台被标记为即将撤桌（在tables_to_close或closing_tables中），不再安排候补
        if (table.table_id not in self.tables_to_close and 
            table.table_id not in self.closing_tables and 
            self.outside_waiting and table.active):
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
        else:
            # HP大于0，移动到候补区尾部（判负离场）
            self.move_to_waiting(player, table_id)
        
        # 检查是否需要减桌（在调整球台位置之前）
        self.check_table_reduction()
        
        # 如果被淘汰的是挑战者，需要调整球台位置
        if was_challenger:
            self.adjust_table_positions_after_challenger_elimination(table)
        # 如果被淘汰的是擂主，需要调整球台位置
        elif was_host:
            self.adjust_table_positions_after_host_elimination(table)
        
        # 如果这个球台被标记为需要关闭，处理减桌逻辑
        if table.table_id in self.tables_to_close:
            self.process_closing_table_after_elimination(table)
        
        # 判负离场后，尽可能安排场外候补选手上桌
        self.fill_leftover_tables()
        
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
        
        # 从场外候补区头部选择进入这张球台
        # 如果球台被标记为即将撤桌（在tables_to_close或closing_tables中），不再安排候补
        if (table.table_id not in self.tables_to_close and 
            table.table_id not in self.closing_tables and 
            self.outside_waiting and table.active):
            # 如果挑战者为空，从场外候补区补充挑战者
            if table.challenger is None:
                new_challenger = self.outside_waiting.pop(0)
                table.challenger = new_challenger
                new_challenger.position = f"{table.table_id}号台挑战者"
                new_challenger.table_id = table.table_id
            # 如果挑战者不为空，从场外候补区补充候补者
            elif len(table.waiting) < 1:
                new_waiting = self.outside_waiting.pop(0)
                table.waiting.append(new_waiting)
                new_waiting.position = f"{table.table_id}号台候补"
                new_waiting.table_id = table.table_id
    
    def adjust_table_positions_after_challenger_elimination(self, table):
        """挑战者被淘汰后调整球台位置"""
        # 擂主不变
        
        # 首先尝试从候补区补位
        if table.waiting:
            table.challenger = table.waiting.pop(0)
            table.challenger.position = f"{table.table_id}号台挑战者"
            table.challenger.table_id = table.table_id  # 确保设置table_id
            
            # 如果候补区有选手补位成挑战者，从场外候补区补充候补选手
            # 如果球台被标记为即将撤桌（在tables_to_close或closing_tables中），不再安排候补
            if (table.table_id not in self.tables_to_close and 
                table.table_id not in self.closing_tables and 
                self.outside_waiting and table.active):
                new_waiting = self.outside_waiting.pop(0)
                table.waiting.append(new_waiting)
                new_waiting.position = f"{table.table_id}号台候补"
                new_waiting.table_id = table.table_id
        else:
            # 如果候补区为空，尝试从场外候补区补充挑战者
            # 如果球台被标记为即将撤桌（在tables_to_close或closing_tables中），不再安排候补
            if (table.table_id not in self.tables_to_close and 
                table.table_id not in self.closing_tables and 
                self.outside_waiting and table.active):
                table.challenger = self.outside_waiting.pop(0)
                table.challenger.position = f"{table.table_id}号台挑战者"
                table.challenger.table_id = table.table_id
                
                # 如果场外候补区还有更多选手，补充候补选手
                if self.outside_waiting and table.active:
                    new_waiting = self.outside_waiting.pop(0)
                    table.waiting.append(new_waiting)
                    new_waiting.position = f"{table.table_id}号台候补"
                    new_waiting.table_id = table.table_id
            else:
                table.challenger = None
    
    def move_to_waiting(self, player, table_id):
        """将选手移动到候补区尾部"""
        # 从当前位置移除选手
        self.remove_player_from_current_position(player, table_id)
        
        # 移动到场外候补区尾部（判负离场）
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
    
    def fill_leftover_tables(self):
        """从已离场桌台队列头部开始安排场外候补选手上桌，尽可能多地安排所有场外候补选手"""
        # 首先处理已离场桌台队列
        while self.leftover_tables_queue and self.outside_waiting:
            # 获取队列头部的桌台号
            table_id = self.leftover_tables_queue[0]
            table = self.get_table_by_id(table_id)
            
            if not table or not table.active:
                # 桌台不存在或不活跃，从队列中移除
                self.leftover_tables_queue.pop(0)
                continue
            
            # 如果桌台被标记为需要关闭，从队列中移除
            if table_id in self.tables_to_close:
                self.leftover_tables_queue.pop(0)
                continue
            
            # 记录安排前的场外候补人数，用于判断是否安排了选手
            before_waiting_count = len(self.outside_waiting)
            
            # 检查桌台的空位情况
            host_needed = table.host is None
            challenger_needed = table.challenger is None
            waiting_needed = len(table.waiting) < 1  # 最多1个候补
            
            # 根据bug0318.md文档的规则：
            # - 如果挑战者和候补者都为空就需要安排挑战者和候补者
            # - 如果挑战者不为空但是候补者为空就安排候补者
            # - 如果挑战者为空但候补者不为空，不需要安排（这种情况不应该发生，因为擂主应该在）
            
            # 检查是否需要安排选手
            if not host_needed and not challenger_needed and not waiting_needed:
                # 桌台已满员，从队列中移除
                self.leftover_tables_queue.pop(0)
                continue
            
            # 安排场外候补选手上桌（尽可能多地安排）
            # 优先级：擂主 > 挑战者 > 候补
            player_assigned = False
            
            # 尝试安排擂主
            if host_needed and self.outside_waiting:
                player = self.outside_waiting.pop(0)
                table.host = player
                player.position = f"{table.table_id}号台擂主"
                player.table_id = table.table_id
                player_assigned = True
            
            # 尝试安排挑战者
            if challenger_needed and self.outside_waiting:
                player = self.outside_waiting.pop(0)
                table.challenger = player
                player.position = f"{table.table_id}号台挑战者"
                player.table_id = table.table_id
                player_assigned = True
            
            # 尝试安排候补
            if waiting_needed and self.outside_waiting:
                player = self.outside_waiting.pop(0)
                table.waiting.append(player)
                player.position = f"{table.table_id}号台候补"
                player.table_id = table.table_id
                player_assigned = True
            
            # 检查安排结果
            if not player_assigned:
                # 未安排上（可能场外候补为空，或者桌台位置已满）
                # 从队列中移除
                self.leftover_tables_queue.pop(0)
            else:
                # 部分安排或全部安排
                # 检查桌台是否已满员
                if table.host is not None and table.challenger is not None and len(table.waiting) >= 1:
                    # 桌台已满员，从队列中移除
                    self.leftover_tables_queue.pop(0)
                # 如果没有满员安排（部分安排），保留这个桌号，等待下次安排
        
        # 然后处理所有活跃的球台，尽可能安排场外候补选手
        # 这是为了确保所有场外候补选手都能被安排上桌
        if self.outside_waiting:
            for table in self.tables:
                if not table.active:
                    continue
                
                # 如果桌台被标记为需要关闭，跳过
                if table.table_id in self.tables_to_close or table.table_id in self.closing_tables:
                    continue
                
                # 检查桌台的空位情况
                host_needed = table.host is None
                challenger_needed = table.challenger is None
                waiting_needed = len(table.waiting) < 1  # 最多1个候补
                
                # 如果桌台已满员，跳过
                if not host_needed and not challenger_needed and not waiting_needed:
                    continue
                
                # 安排场外候补选手上桌（尽可能多地安排）
                # 优先级：擂主 > 挑战者 > 候补
                if host_needed and self.outside_waiting:
                    player = self.outside_waiting.pop(0)
                    table.host = player
                    player.position = f"{table.table_id}号台擂主"
                    player.table_id = table.table_id
                
                if challenger_needed and self.outside_waiting:
                    player = self.outside_waiting.pop(0)
                    table.challenger = player
                    player.position = f"{table.table_id}号台挑战者"
                    player.table_id = table.table_id
                
                if waiting_needed and self.outside_waiting:
                    player = self.outside_waiting.pop(0)
                    table.waiting.append(player)
                    player.position = f"{table.table_id}号台候补"
                    player.table_id = table.table_id
    
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
        
        # 处理已离场桌台队列，安排场外候补选手上桌
        self.fill_leftover_tables()