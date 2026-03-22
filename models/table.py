from typing import Optional, List
from models.player import Player

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
