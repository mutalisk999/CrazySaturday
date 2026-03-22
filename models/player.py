from typing import Optional

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
