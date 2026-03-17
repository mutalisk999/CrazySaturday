import tkinter as tk
from tkinter import ttk, scrolledtext
from models import Game

class CrazySaturdayApp:
    def __init__(self):
        self.game = Game()
        self.root = tk.Tk()
        self.root.title("疯狂星期六抢1大赛")
        self.root.geometry("1000x700")
        
        # 示例选手列表（用于重新开始游戏时使用）
        self.example_players = [
            ('张三', 4), ('李四', 5), ('王五', 3), ('赵六', 6),
            ('钱七', 4), ('孙八', 5), ('周九', 3), ('吴十', 4),
            ('郑十一', 5), ('王十二', 4), ('李十三', 3), ('赵十四', 6),
            ('钱十五', 4), ('孙十六', 5), ('周十七', 3), ('吴十八', 4),
            ('郑十九', 5), ('王二十', 4), ('李二十一', 3), ('赵二十二', 6),
            ('钱二十三', 4), ('孙二十四', 5), ('周二十五', 3), ('吴二十六', 4),
            ('郑二十七', 5), ('王二十八', 4), ('李二十九', 3), ('赵三十', 6),
            ('钱三十一', 4), ('孙三十二', 5), ('周三十三', 3), ('吴三十四', 4),
            ('郑三十五', 5), ('王三十六', 4)
        ]
        
        # 初始选手列表为空，用户需要手动添加选手
        
        self.create_setup_screen()
    
    def create_setup_screen(self):
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="疯狂星期六抢1大赛 - 选手设置", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 选手列表 - 使用滚动区域
        players_label = tk.Label(self.root, text="选手列表:", font=('Arial', 12, 'bold'))
        players_label.pack(anchor='w', padx=20)
        
        # 创建选手列表的滚动区域
        players_container = tk.Frame(self.root)
        players_container.pack(fill='both', expand=True, padx=20, pady=5)
        
        # 创建Canvas和Scrollbar
        players_canvas = tk.Canvas(players_container, height=200)
        scrollbar = ttk.Scrollbar(players_container, orient="vertical", command=players_canvas.yview)
        players_frame = tk.Frame(players_canvas)
        
        players_frame.bind(
            "<Configure>",
            lambda e: players_canvas.configure(scrollregion=players_canvas.bbox("all"))
        )
        
        players_canvas.create_window((0, 0), window=players_frame, anchor="nw")
        players_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 显示当前选手，每个选手带删除按钮
        self.player_frames = []  # 保存选手框架的引用
        for i, player in enumerate(self.game.players):
            player_frame = tk.Frame(players_frame)
            player_frame.pack(fill='x', padx=10, pady=2)
            
            player_text = f"{i+1}. {player.name} - 初始命数: {player.initial_lives}"
            player_label = tk.Label(player_frame, text=player_text, anchor='w')
            player_label.pack(side='left')
            
            # 删除按钮
            delete_button = tk.Button(player_frame, text="删除", 
                                    command=lambda idx=i: self.remove_player(idx),
                                    bg='red', fg='white', font=('Arial', 8))
            delete_button.pack(side='right', padx=5)
            
            self.player_frames.append(player_frame)
        
        players_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加选手区域
        add_frame = tk.Frame(self.root)
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(add_frame, text="添加新选手:").pack(side='left')
        self.name_entry = tk.Entry(add_frame, width=15)
        self.name_entry.pack(side='left', padx=5)
        
        tk.Label(add_frame, text="初始命数:").pack(side='left')
        self.lives_var = tk.StringVar(value='4')
        lives_combo = ttk.Combobox(add_frame, textvariable=self.lives_var, 
                                   values=[2,3,4,5,6,7,8], width=5)
        lives_combo.pack(side='left', padx=5)
        
        add_button = tk.Button(add_frame, text="添加选手", command=self.add_player)
        add_button.pack(side='left', padx=10)
        
        # 开始比赛按钮
        if len(self.game.players) >= 2:
            start_button = tk.Button(self.root, text="开始比赛", 
                                   command=self.start_game,
                                   bg='green', fg='white', font=('Arial', 12, 'bold'))
            start_button.pack(pady=20)
        else:
            warning_label = tk.Label(self.root, text="至少需要2名选手才能开始比赛", 
                                    fg='red')
            warning_label.pack(pady=20)
    
    def create_game_screen(self):
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="疯狂星期六抢1大赛 - 比赛进行中", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # 左侧：球台区域
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        tables_label = tk.Label(left_frame, text="球台区域", font=('Arial', 12, 'bold'))
        tables_label.pack(anchor='w')
        
        # 球台滚动区域
        tables_canvas = tk.Canvas(left_frame, height=400)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=tables_canvas.yview)
        scrollable_frame = ttk.Frame(tables_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: tables_canvas.configure(scrollregion=tables_canvas.bbox("all"))
        )
        
        tables_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        tables_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 显示球台
        for table in self.game.tables:
            if table.active:
                table_frame = ttk.LabelFrame(scrollable_frame, text=f"{table.table_id}号球台")
                table_frame.pack(fill='x', padx=5, pady=5)
                
                # 擂主
                host_text = f"擂主: {table.host.name if table.host else '无'}"
                if table.host:
                    host_text += f" ({table.host.current_lives}/{table.host.initial_lives})"
                    host_color = 'red' if table.host.current_lives == 1 else 'black'
                else:
                    host_color = 'black'
                
                host_label = tk.Label(table_frame, text=host_text, fg=host_color, anchor='w')
                host_label.pack(fill='x', padx=10)
                
                # 挑战者
                challenger_text = f"挑战者: {table.challenger.name if table.challenger else '无'}"
                if table.challenger:
                    challenger_text += f" ({table.challenger.current_lives}/{table.challenger.initial_lives})"
                    challenger_color = 'red' if table.challenger.current_lives == 1 else 'black'
                else:
                    challenger_color = 'black'
                
                challenger_label = tk.Label(table_frame, text=challenger_text, fg=challenger_color, anchor='w')
                challenger_label.pack(fill='x', padx=10)
                
                # 候补
                waiting_label = tk.Label(table_frame, text=f"候补: {len(table.waiting)}人", anchor='w')
                waiting_label.pack(fill='x', padx=10)
        
        tables_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 右侧：候补和淘汰区域 - 使用下拉菜单
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='y', padx=10)
        
        # 创建Notebook（选项卡控件）
        notebook = ttk.Notebook(right_frame, width=250)
        
        # 场外候补区选项卡
        waiting_frame = ttk.Frame(notebook)
        notebook.add(waiting_frame, text="场外候补区")
        
        waiting_text = scrolledtext.ScrolledText(waiting_frame, width=28, height=10)
        waiting_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        waiting_players = [f"{p.name} ({p.current_lives}/{p.initial_lives})" 
                          for p in self.game.outside_waiting]
        waiting_text.insert('1.0', '\n'.join(waiting_players) if waiting_players else "暂无选手")
        waiting_text.config(state='disabled')
        
        # 已淘汰选手区选项卡
        eliminated_frame = ttk.Frame(notebook)
        notebook.add(eliminated_frame, text="已淘汰选手区")
        
        eliminated_text = scrolledtext.ScrolledText(eliminated_frame, width=28, height=10)
        eliminated_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        eliminated_players = [p.name for p in self.game.eliminated]
        eliminated_text.insert('1.0', '\n'.join(eliminated_players) if eliminated_players else "暂无选手")
        eliminated_text.config(state='disabled')
        
        notebook.pack(fill='both', expand=True, pady=5)
        
        # 底部控制区域
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill='x', pady=10)
        
        next_button = tk.Button(bottom_frame, text="下一步", 
                               command=self.next_step,
                               bg='blue', fg='white', font=('Arial', 12, 'bold'))
        next_button.pack(side='left', padx=20)
        
        status_label = tk.Label(bottom_frame, 
                              text=f"剩余选手: {self.game.get_remaining_players_count()}",
                              font=('Arial', 12))
        status_label.pack(side='left', padx=20)
    
    def create_finished_screen(self):
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="疯狂星期六抢1大赛 - 比赛结束", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 冠军
        if self.game.winner:
            champion_label = tk.Label(self.root, 
                                     text=f"🏆 冠军: {self.game.winner.name} 🏆",
                                     font=('Arial', 14, 'bold'), fg='gold')
            champion_label.pack(pady=10)
        
        # 统计信息
        stats_label = tk.Label(self.root, text="选手统计:", font=('Arial', 12, 'bold'))
        stats_label.pack(anchor='w', padx=20)
        
        # 统计内容
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(fill='both', expand=True, padx=20)
        
        # 按最长连胜排序
        sorted_players = sorted(self.game.players, key=lambda p: p.max_streak, reverse=True)
        
        for i, player in enumerate(sorted_players[:10]):
            stat_text = f"{i+1}. {player.name}: 胜{player.wins}负{player.losses} 最长连胜{player.max_streak}"
            stat_label = tk.Label(stats_frame, text=stat_text, anchor='w')
            stat_label.pack(fill='x', padx=10)
        
        # 重新开始按钮
        restart_button = tk.Button(self.root, text="重新开始", 
                                 command=self.restart_game,
                                 bg='green', fg='white', font=('Arial', 12, 'bold'))
        restart_button.pack(pady=20)
    
    def add_player(self):
        name = self.name_entry.get().strip()
        lives = self.lives_var.get()
        
        if name and lives:
            self.game.add_player(name, int(lives))
            self.name_entry.delete(0, 'end')
            self.create_setup_screen()
    
    def remove_player(self, index: int):
        """删除指定索引的选手"""
        if 0 <= index < len(self.game.players):
            self.game.remove_player(index)
            self.create_setup_screen()
    
    def start_game(self):
        if self.game.start_game():
            self.create_game_screen()
    
    def next_step(self):
        self.game.update()
        if self.game.game_state == "running":
            self.create_game_screen()
        else:
            self.create_finished_screen()
    
    def restart_game(self):
        # 重新开始游戏
        self.game = Game()
        
        # 重新添加示例选手
        for name, lives in self.example_players:
            self.game.add_player(name, lives)
        
        self.create_setup_screen()
    
    def run(self):
        self.root.mainloop()