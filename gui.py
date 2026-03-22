import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from models import Game, FixedParticipant, FixedParticipantManager, TableThresholdsManager

class CrazySaturdayApp:
    def __init__(self):
        self.game = Game()
        self.root = tk.Tk()
        self.root.title("疯狂星期六抢1大赛")
        self.root.geometry("1100x700")
        
        # 示例选手列表（用于重新开始游戏时使用）
        self.example_players = [
            ('张三', 2), ('李四', 3), ('王五', 2), ('赵六', 3),
            ('钱七', 2), ('孙八', 3), ('周九', 2), ('吴十', 3),
            ('郑十一', 2), ('王十二', 3), ('李十三', 2), ('赵十四', 3),
            ('钱十五', 2), ('孙十六', 3), ('周十七', 2), ('吴十八', 3),
            ('郑十九', 2), ('王二十', 3), ('李二十一', 2), ('赵二十二', 3),
            ('钱二十三', 2), ('孙二十四', 3), ('周二十五', 2), ('吴二十六', 3),
            ('郑二十七', 2), ('王二十八', 3), ('李二十九', 2), ('赵三十', 3),
            ('钱三十一', 2), ('孙三十二', 3), ('周三十三', 2), ('吴三十四', 3),
            ('郑三十五', 2), ('王三十六', 3)
        ]
        
        # 测试模式变量
        self.test_mode_var = tk.BooleanVar(value=False)
        
        # 固定参赛选手管理器
        self.fixed_participant_manager = FixedParticipantManager()
        
        # 球桌阈值管理器
        self.thresholds_manager = TableThresholdsManager()
        
        # 默认不装载示例选手，保持空列表
        self.game = Game(self.thresholds_manager)
        
        # 设置减桌回调函数
        self.game.set_table_reduction_callback(self.show_table_reduction_dialog)
        
        self.create_setup_screen()
    
    def create_setup_screen(self):
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="疯狂星期六抢1大赛 - 选手设置", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 测试模式复选框 - 使用已有的变量
        test_mode_check = tk.Checkbutton(self.root, text="测试模式", 
                                        variable=self.test_mode_var,
                                        command=self.on_test_mode_change,
                                        font=('Arial', 12))
        test_mode_check.pack(pady=5)
        
        # 选手列表 - 使用表格显示
        players_label = tk.Label(self.root, text="选手列表:", font=('Arial', 12, 'bold'))
        players_label.pack(anchor='w', padx=20)
        
        # 创建表格容器
        players_container = tk.Frame(self.root)
        players_container.pack(fill='both', expand=True, padx=20, pady=5)
        
        # 创建Treeview表格
        columns = ('序号', '姓名', 'HP值')
        self.players_table = ttk.Treeview(players_container, columns=columns, show='tree headings', height=10)
        
        # 设置列标题
        self.players_table.heading('序号', text='序号')
        self.players_table.heading('姓名', text='姓名')
        self.players_table.heading('HP值', text='HP')
        
        # 设置列宽度和样式 - 动态适配容器宽度
        self.players_table.column('#0', width=0, stretch=False)  # 隐藏树形列
        self.players_table.column('序号', width=80, anchor='center', stretch=False)  # 固定宽度
        self.players_table.column('姓名', width=100, anchor='center', stretch=True)   # 动态宽度
        self.players_table.column('HP值', width=80, anchor='center', stretch=True)  # 减少宽度，小点更紧凑
        
        # 配置表格样式 - 显示行和列分隔线
        style = ttk.Style()
        
        # 创建红色边框样式
        style.configure('Red.TLabelframe', borderwidth=3, relief='solid', bordercolor='red')
        style.configure('Red.TLabelframe.Label', foreground='red')
        
        # 配置Treeview样式，显示网格线
        style.configure("Custom.Treeview", 
                       background="white",
                       foreground="black",
                       rowheight=35,  # 增加行高确保8个红心能显示
                       fieldbackground="white")
        
        # 配置HP列显示红色小点
        # 序号和姓名列保持黑色显示
        
        # 使用红色小点●显示HP值，序号和姓名保持黑色显示
        # Treeview限制：无法单独设置列颜色，但红色小点本身具有颜色效果
        
        # 配置表头样式
        style.configure("Custom.Treeview.Heading", 
                       background="lightgray",
                       foreground="black",
                       font=('Microsoft YaHei', 11, 'bold'))
        
        # 配置选中状态
        style.map("Custom.Treeview", 
                 background=[('selected', '#0078d7')],
                 foreground=[('selected', 'white')])
        
        # 应用自定义样式
        self.players_table.configure(style="Custom.Treeview")
        
        # 设置表格显示选项，确保显示分隔线
        self.players_table['show'] = 'tree headings'
        
        # 设置列分隔符
        for col in columns:
            self.players_table.column(col, anchor='center', stretch=False)
        
        # 使用替代方法显示网格线 - 配置单元格边框
        style.configure("Custom.Treeview", 
                       bordercolor="black",
                       lightcolor="black",
                       darkcolor="black",
                       borderwidth=1)
        
        # 配置表头单元格边框
        style.configure("Custom.Treeview.Heading", 
                       bordercolor="black",
                       lightcolor="black",
                       darkcolor="black",
                       borderwidth=1)
        
        # 设置表格布局以显示网格线
        style.layout("Custom.Treeview", [
            ('Custom.Treeview.treearea', {'sticky': 'nswe', 'border': '1'})
        ])
        
        # 为每个单元格设置边框
        for col in columns:
            self.players_table.column(col, anchor='center', stretch=False)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(players_container, orient="vertical", command=self.players_table.yview)
        self.players_table.configure(yscrollcommand=scrollbar.set)
        
        # 填充表格数据 - HP值用红色小点显示
        for i, player in enumerate(self.game.players):
            # 将HP值转换为红色小点 - 使用更紧凑的显示
            dots = '●' * player.initial_lives
            self.players_table.insert('', 'end', values=(i+1, player.name, dots))
        
        # 直接为容器添加边框，而不是创建新的框架
        players_container.configure(borderwidth=2, relief="solid")
        
        # 正常打包表格和滚动条
        self.players_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 选中提示（移动到添加选手区域）
        self.selection_label = tk.Label(self.root, text="请先选中要删除的选手", fg='gray')
        self.selection_label.pack(pady=5, padx=20, anchor='w')
        
        # 绑定选择事件和双击编辑事件
        self.players_table.bind('<<TreeviewSelect>>', self.on_table_select)
        self.players_table.bind('<Double-1>', self.on_double_click)
        
        # 绑定鼠标移动事件，显示HP数字提示
        self.players_table.bind('<Motion>', self.on_mouse_motion)
        
        # 绑定窗口大小变化事件，动态调整列宽
        self.root.bind('<Configure>', self.on_window_resize)
        
        # 工具提示相关变量
        self.tooltip = None
        self.tooltip_text = None
        
        # 编辑相关变量
        self.editing_entry = None
        self.editing_item = None
        self.editing_column = None
        
        # 添加选手区域
        add_frame = tk.Frame(self.root)
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(add_frame, text="添加新选手:").pack(side='left')
        # 创建可输入的下拉框
        self.name_var = tk.StringVar()
        self.name_combobox = ttk.Combobox(add_frame, textvariable=self.name_var, width=15)
        self.name_combobox.pack(side='left', padx=5)
        # 填充固定参赛选手到下拉框
        self.refresh_name_combobox()
        # 绑定选择事件
        self.name_combobox.bind('<<ComboboxSelected>>', self.on_name_selected)
        
        tk.Label(add_frame, text="初始HP:").pack(side='left')
        self.lives_var = tk.StringVar(value='4')
        
        # 创建HP选项框 - 直接显示2-8的所有选项
        hp_options_frame = tk.Frame(add_frame)
        hp_options_frame.pack(side='left', padx=5)
        
        # 创建2-8的选项按钮
        for hp_value in [2, 3, 4, 5, 6, 7, 8]:
            hp_radio = tk.Radiobutton(hp_options_frame, 
                                     text=str(hp_value),
                                     variable=self.lives_var,
                                     value=str(hp_value),
                                     font=('Arial', 9))
            hp_radio.pack(side='left', padx=2)
        
        add_button = tk.Button(add_frame, text="添加选手", command=self.add_player)
        add_button.pack(side='left', padx=10)
        
        delete_button = tk.Button(add_frame, text="删除选中选手", 
                                command=self.delete_selected_player,
                                bg='red', fg='white', font=('Arial', 10))
        delete_button.pack(side='left', padx=10)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # 设定球桌阈值按钮
        thresholds_button = tk.Button(button_frame, text="设定球桌阈值", 
                                     command=self.create_table_thresholds_screen,
                                     bg='purple', fg='white', font=('Arial', 12, 'bold'))
        thresholds_button.pack(side='left', padx=10)
        
        # 固定参赛选手按钮
        fixed_button = tk.Button(button_frame, text="固定参赛选手", 
                               command=self.create_fixed_participants_screen,
                               bg='orange', fg='white', font=('Arial', 12, 'bold'))
        fixed_button.pack(side='left', padx=10)
        
        # 加载历史状态按钮
        load_button = tk.Button(button_frame, text="加载历史状态", 
                               command=self.load_history_state,
                               bg='blue', fg='white', font=('Arial', 12, 'bold'))
        load_button.pack(side='left', padx=10)
        
        # 重新开始比赛按钮
        if len(self.game.players) >= 2:
            start_button = tk.Button(button_frame, text="重新开始比赛", 
                                   command=self.restart_game,
                                   bg='green', fg='white', font=('Arial', 12, 'bold'))
            start_button.pack(side='left', padx=10)
        else:
            warning_label = tk.Label(button_frame, text="至少需要2名选手才能开始比赛", 
                                    fg='red')
            warning_label.pack(side='left')
    
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
        
        # 显示球台 - 水平排列
        row_frame = None
        tables_per_row = 3  # 每行显示3个球台
        table_count = 0
        
        # 按照table_priority顺序排序球台
        table_priority = self.game.table_priority
        # 创建一个字典，将table_id映射到优先级索引
        table_id_to_priority = {table_id: i for i, table_id in enumerate(table_priority)}
        # 按照优先级排序球台
        sorted_tables = sorted(self.game.tables, key=lambda t: table_id_to_priority.get(t.table_id, 999))
        
        for table in sorted_tables:
            if table.active:
                # 检查球台是否被标记为需要关闭
                is_closing_table = table.table_id in self.game.tables_to_close
                
                # 每行开始时创建新的行框架
                if table_count % tables_per_row == 0:
                    row_frame = tk.Frame(scrollable_frame)
                    row_frame.pack(fill='x', padx=5, pady=5)
                
                # 根据是否即将撤桌设置标题颜色
                title_text = f"{table.table_id}号球台"
                if is_closing_table:
                    title_text += " (即将撤桌)"
                
                table_frame = ttk.LabelFrame(row_frame, text=title_text, width=300)
                table_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
                
                # 设置边框颜色
                if is_closing_table:
                    table_frame.configure(style='Red.TLabelframe')
                
                table_count += 1
                
                # 擂主区域 - 包含判负离场按钮和选手信息
                host_frame = tk.Frame(table_frame)
                host_frame.pack(fill='x', padx=10)
                
                # 擂主判负离场按钮 - 只有当擂主和挑战者都存在时才显示
                if table.host and table.challenger:
                    host_button = tk.Button(host_frame, text="负", width=3, fg='blue', bg='yellow',
                                          command=lambda p=table.host, tid=table.table_id: 
                                          self.eliminate_player(p, tid, "擂主"))
                    host_button.pack(side='left', padx=(0, 5))
                
                # 擂主信息标签 - 分为两个标签，只有选手名字变红
                host_label_prefix = tk.Label(host_frame, text="擂主: ", anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                host_label_prefix.pack(side='left')
                
                if table.host:
                    host_name_text = f"{table.host.name} ({table.host.current_lives}/{table.host.initial_lives})"
                    host_name_color = 'red' if table.host.current_lives == 1 else 'black'
                else:
                    host_name_text = '无'
                    host_name_color = 'black'
                
                host_label_name = tk.Label(host_frame, text=host_name_text, fg=host_name_color, anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                host_label_name.pack(side='left', fill='x', expand=True)
                
                # 挑战者区域 - 包含判负离场按钮和选手信息
                challenger_frame = tk.Frame(table_frame)
                challenger_frame.pack(fill='x', padx=10)
                
                # 挑战者判负离场按钮 - 只有当擂主和挑战者都存在时才显示
                if table.host and table.challenger:
                    challenger_button = tk.Button(challenger_frame, text="负", width=3, fg='blue', bg='yellow',
                                                 command=lambda p=table.challenger, tid=table.table_id: 
                                                 self.eliminate_player(p, tid, "挑战者"))
                    challenger_button.pack(side='left', padx=(0, 5))
                
                # 挑战者信息标签 - 分为两个标签，只有选手名字变红
                challenger_label_prefix = tk.Label(challenger_frame, text="挑战者: ", anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                challenger_label_prefix.pack(side='left')
                
                if table.challenger:
                    challenger_name_text = f"{table.challenger.name} ({table.challenger.current_lives}/{table.challenger.initial_lives})"
                    challenger_name_color = 'red' if table.challenger.current_lives == 1 else 'black'
                else:
                    challenger_name_text = '无'
                    challenger_name_color = 'black'
                
                challenger_label_name = tk.Label(challenger_frame, text=challenger_name_text, fg=challenger_name_color, anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                challenger_label_name.pack(side='left', fill='x', expand=True)
                
                # 候补 - 显示详细信息（候补选手不能被淘汰）
                waiting_frame = tk.Frame(table_frame)
                waiting_frame.pack(fill='x', padx=10)
                
                # 候补区域占位按钮（保持对齐）
                placeholder_button = tk.Button(waiting_frame, text=" ", width=3, state='disabled', bg='yellow')
                placeholder_button.pack(side='left', padx=(0, 5))
                
                if table.waiting:
                    # 显示候补选手姓名和HP值
                    waiting_label = tk.Label(waiting_frame, text="候补:", anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                    waiting_label.pack(side='left')
                    
                    for i, player in enumerate(table.waiting):
                        player_text = f"{player.name}({player.current_lives}/{player.initial_lives})"
                        if i > 0:
                            player_text = "，" + player_text
                        
                        # HP为1的选手显示为红色
                        if player.current_lives == 1:
                            player_label = tk.Label(waiting_frame, text=player_text, anchor='w', font=('Microsoft YaHei', 11, 'bold'), fg='red')
                        else:
                            player_label = tk.Label(waiting_frame, text=player_text, anchor='w', font=('Microsoft YaHei', 11, 'bold'))
                        player_label.pack(side='left')
                        
                        # 候补选手不能被下场，不绑定右键菜单
                else:
                    waiting_label = tk.Label(waiting_frame, text="候补: 0人", anchor='w')
                    waiting_label.pack(side='left', fill='x', expand=True)
        
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
        
        # 使用 Treeview 显示场外候补选手
        waiting_tree = ttk.Treeview(waiting_frame, columns=("姓名", "HP"), show='headings', height=10)
        waiting_tree.heading("姓名", text="姓名")
        waiting_tree.heading("HP", text="HP")
        waiting_tree.column("姓名", width=120, anchor='center')
        waiting_tree.column("HP", width=80, anchor='center')
        
        # 添加滚动条
        waiting_scrollbar = ttk.Scrollbar(waiting_frame, orient="vertical", command=waiting_tree.yview)
        waiting_tree.configure(yscrollcommand=waiting_scrollbar.set)
        
        waiting_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        waiting_scrollbar.pack(side='right', fill='y', pady=5)
        
        # 插入场外候补选手，HP为1的显示为红色
        if self.game.outside_waiting:
            for p in self.game.outside_waiting:
                hp_text = f"{p.current_lives}/{p.initial_lives}"
                # HP为1的选手显示为红色
                if p.current_lives == 1:
                    waiting_tree.insert('', 'end', values=(p.name, hp_text), tags=('red_hp',))
                else:
                    waiting_tree.insert('', 'end', values=(p.name, hp_text))
            waiting_tree.tag_configure('red_hp', foreground='red')
        else:
            waiting_tree.insert('', 'end', values=("暂无选手", ""))
        
        # 已淘汰选手区选项卡
        eliminated_frame = ttk.Frame(notebook)
        notebook.add(eliminated_frame, text="已淘汰选手区")
        
        # 使用 Treeview 显示已淘汰选手
        eliminated_tree = ttk.Treeview(eliminated_frame, columns=("姓名",), show='headings', height=10)
        eliminated_tree.heading("姓名", text="姓名")
        eliminated_tree.column("姓名", width=200, anchor='center')
        
        # 添加滚动条
        eliminated_scrollbar = ttk.Scrollbar(eliminated_frame, orient="vertical", command=eliminated_tree.yview)
        eliminated_tree.configure(yscrollcommand=eliminated_scrollbar.set)
        
        eliminated_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        eliminated_scrollbar.pack(side='right', fill='y', pady=5)
        
        if self.game.eliminated:
            for p in self.game.eliminated:
                eliminated_tree.insert('', 'end', values=(p.name,))
        else:
            eliminated_tree.insert('', 'end', values=("暂无选手",))
        
        # 连胜统计排行选项卡
        streak_frame = ttk.Frame(notebook)
        notebook.add(streak_frame, text="连胜统计排行")
        
        # 使用 Treeview 显示连胜统计
        streak_tree = ttk.Treeview(streak_frame, columns=("排名", "姓名", "最大连胜", "当前连胜"), show='headings', height=10)
        streak_tree.heading("排名", text="排名")
        streak_tree.heading("姓名", text="姓名")
        streak_tree.heading("最大连胜", text="最大连胜")
        streak_tree.heading("当前连胜", text="当前连胜")
        streak_tree.column("排名", width=60, anchor='center')
        streak_tree.column("姓名", width=100, anchor='center')
        streak_tree.column("最大连胜", width=80, anchor='center')
        streak_tree.column("当前连胜", width=80, anchor='center')
        
        # 添加滚动条
        streak_scrollbar = ttk.Scrollbar(streak_frame, orient="vertical", command=streak_tree.yview)
        streak_tree.configure(yscrollcommand=streak_scrollbar.set)
        
        streak_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        streak_scrollbar.pack(side='right', fill='y', pady=5)
        
        # 按最大连赢数排序选手
        active_players = [p for p in self.game.players if not p.is_eliminated()]
        sorted_by_streak = sorted(active_players, key=lambda p: p.max_streak, reverse=True)
        
        if sorted_by_streak:
            for i, p in enumerate(sorted_by_streak):
                streak_tree.insert('', 'end', values=(i+1, p.name, p.max_streak, p.streak))
        else:
            streak_tree.insert('', 'end', values=("", "暂无选手", "", ""))
        
        # 比赛对局详情信息选项卡
        match_details_frame = ttk.Frame(notebook)
        notebook.add(match_details_frame, text="比赛对局详情信息")
        
        # 使用 Treeview 显示对局详情
        match_tree = ttk.Treeview(match_details_frame, columns=("桌号", "时间", "胜者", "负者"), show='headings', height=10)
        match_tree.heading("桌号", text="桌号")
        match_tree.heading("时间", text="时间")
        match_tree.heading("胜者", text="胜者")
        match_tree.heading("负者", text="负者")
        match_tree.column("桌号", width=60, anchor='center')
        match_tree.column("时间", width=80, anchor='center')
        match_tree.column("胜者", width=100, anchor='center')
        match_tree.column("负者", width=100, anchor='center')
        
        # 添加滚动条
        match_scrollbar = ttk.Scrollbar(match_details_frame, orient="vertical", command=match_tree.yview)
        match_tree.configure(yscrollcommand=match_scrollbar.set)
        
        match_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        match_scrollbar.pack(side='right', fill='y', pady=5)
        
        # 显示对局详情 - 一行显示一局比赛
        match_records = getattr(self.game, 'match_records', [])
        if match_records:
            # 将记录按桌号和时间分组，每两条记录为一局比赛
            for i in range(0, len(match_records), 2):
                if i + 1 < len(match_records):
                    winner_record = match_records[i]
                    loser_record = match_records[i + 1]
                    time_str = winner_record.start_time.strftime("%H:%M:%S")
                    match_tree.insert('', 'end', values=(winner_record.table_id, time_str, winner_record.player_name, loser_record.player_name))
        else:
            match_tree.insert('', 'end', values=("", "", "暂无对局记录", ""))
        
        notebook.pack(fill='both', expand=True, pady=5)
        
        # 底部状态显示区域
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill='x', pady=10)
        
        # 左侧：回到主界面按钮和状态标签
        left_frame = tk.Frame(bottom_frame)
        left_frame.pack(side='left', padx=20)
        
        # 回到主界面按钮
        back_button = tk.Button(left_frame, text="回到主界面",
                               command=self.create_setup_screen,
                               bg='orange', fg='white',
                               font=('Microsoft YaHei', 11, 'bold'),
                               width=12)
        back_button.pack(side='left', padx=5)
        
        status_label = tk.Label(left_frame, 
                              text=f"剩余选手: {self.game.get_remaining_players_count()}",
                              font=('Arial', 12))
        status_label.pack(side='left', padx=20)
        
        # 状态机控制区域
        state_frame = tk.Frame(bottom_frame)
        state_frame.pack(side='right', padx=20)
        
        # 状态数量
        state_count = self.game.get_state_count()
        current_index = self.game.get_current_state_index()
        
        if state_count > 0:
            # 状态索引显示
            index_label = tk.Label(state_frame, 
                                 text=f"状态: {current_index}/{state_count - 1}",
                                 font=('Arial', 10, 'bold'))
            index_label.pack(side='left', padx=5)
            
            # 向左按钮
            prev_button = tk.Button(state_frame, text="◀", 
                                  command=self.prev_state,
                                  state='disabled' if current_index <= 0 else 'normal',
                                  font=('Arial', 12, 'bold'), width=3)
            prev_button.pack(side='left', padx=2)
            
            # 向右按钮
            next_button = tk.Button(state_frame, text="▶", 
                                  command=self.next_state,
                                  state='disabled' if current_index >= state_count - 1 else 'normal',
                                  font=('Arial', 12, 'bold'), width=3)
            next_button.pack(side='left', padx=2)
            
            # 当前状态描述
            state_desc = self.game.get_state_description(current_index)
            state_label = tk.Label(state_frame, text=state_desc, font=('Arial', 10))
            state_label.pack(side='left', padx=5)
            
            # 进入状态按钮
            enter_state_button = tk.Button(state_frame, text="进入状态", 
                                         command=self.enter_current_state,
                                         bg='blue', fg='white', font=('Arial', 10, 'bold'))
            enter_state_button.pack(side='left', padx=5)
    
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
    
    def on_table_select(self, event):
        """表格选择事件处理"""
        selected = self.players_table.selection()
        if selected:
            self.selection_label.config(text=f"已选中 {len(selected)} 名选手", fg='green')
        else:
            self.selection_label.config(text="请先选中要删除的选手", fg='gray')
    
    def delete_selected_player(self):
        """删除选中的选手"""
        selected = self.players_table.selection()
        if not selected:
            # 显示错误提示
            error_window = tk.Toplevel(self.root)
            error_window.title("错误")
            error_window.geometry("300x100")
            error_window.transient(self.root)
            error_window.grab_set()
            
            error_label = tk.Label(error_window, text="请先选中要删除的选手！", 
                                  fg='red', font=('Arial', 10))
            error_label.pack(pady=20)
            
            ok_button = tk.Button(error_window, text="确定", command=error_window.destroy)
            ok_button.pack(pady=10)
            return
        
        # 获取选中的行索引（从后往前删除，避免索引变化）
        indices = []
        for item in selected:
            values = self.players_table.item(item)['values']
            if values:
                indices.append(values[0] - 1)  # 序号减1得到索引
        
        # 从后往前删除，避免索引变化
        indices.sort(reverse=True)
        for idx in indices:
            if 0 <= idx < len(self.game.players):
                self.game.remove_player(idx)
        
        # 刷新界面
        self.create_setup_screen()
    
    def on_double_click(self, event):
        """双击编辑事件处理"""
        # 获取点击的位置
        region = self.players_table.identify_region(event.x, event.y)
        if region not in ['cell', 'tree']:
            return
        
        # 获取点击的项目和列
        item = self.players_table.identify_row(event.y)
        column = self.players_table.identify_column(event.x)
        
        if not item or column == '#1':  # 序号列不可编辑
            return
        
        # 只允许编辑姓名和HP值列
        if column not in ['#2', '#3']:
            return
        
        # 确保选中该行
        self.players_table.selection_set(item)
        
        # 开始编辑
        self.start_editing(item, column)
    
    def start_editing(self, item, column):
        """开始编辑单元格"""
        # 清除之前的编辑状态
        if self.editing_entry:
            self.finish_editing()
        
        # 获取当前值
        values = self.players_table.item(item, 'values')
        if column == '#2':  # 姓名列
            current_value = values[1]
        elif column == '#3':  # HP值列
            # HP值列显示红色小点，但编辑时需要显示原始数值
            # 从小点字符串推断原始HP值
            dots_text = values[2]
            # 计算小点数量（每个●占1个字符）
            hp_value = len(dots_text)  # 每个●是1个字符
            current_value = str(hp_value)
        else:
            return
        
        # 获取单元格位置
        bbox = self.players_table.bbox(item, column)
        if not bbox:
            return
        
        # 创建编辑框
        self.editing_entry = tk.Entry(self.players_table, 
                                     font=('Arial', 10),
                                     justify='center')
        self.editing_entry.insert(0, current_value)
        self.editing_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        
        # 设置焦点和绑定事件
        self.editing_entry.focus_set()
        self.editing_entry.select_range(0, 'end')
        self.editing_entry.bind('<Return>', lambda e: self.finish_editing())
        self.editing_entry.bind('<FocusOut>', lambda e: self.finish_editing())
        self.editing_entry.bind('<Escape>', lambda e: self.cancel_editing())
        
        # 保存编辑状态
        self.editing_item = item
        self.editing_column = column
    
    def finish_editing(self):
        """完成编辑"""
        if not self.editing_entry:
            return
        
        new_value = self.editing_entry.get().strip()
        
        # 先清理编辑状态，避免界面刷新时的冲突
        self.cleanup_editing()
        
        # 验证和更新数据
        if self.validate_and_update(new_value):
            # 更新成功，刷新界面
            self.create_setup_screen()
        else:
            # 验证失败，不需要刷新界面，数据保持不变
            pass
    
    def cancel_editing(self):
        """取消编辑"""
        self.cleanup_editing()
    
    def cleanup_editing(self):
        """清理编辑状态"""
        if self.editing_entry:
            try:
                self.editing_entry.destroy()
            except:
                pass  # 如果控件已经被销毁，忽略错误
            self.editing_entry = None
        self.editing_item = None
        self.editing_column = None
    
    def validate_and_update(self, new_value):
        """验证新值并更新数据"""
        if not self.editing_item or not self.editing_column:
            return False
        
        # 获取选手索引
        values = self.players_table.item(self.editing_item, 'values')
        player_index = values[0] - 1
        
        if player_index < 0 or player_index >= len(self.game.players):
            return False
        
        player = self.game.players[player_index]
        
        if self.editing_column == '#2':  # 姓名列
            # 验证姓名
            if not new_value:
                self.show_error("姓名不能为空！")
                return False
            
            # 验证姓名首字符：只允许中文或大小写字母
            first_char = new_value[0]
            if not (('\u4e00' <= first_char <= '\u9fff') or  # 中文字符
                    ('A' <= first_char <= 'Z') or              # 大写字母
                    ('a' <= first_char <= 'z')):              # 小写字母
                self.show_error("姓名首字符必须是中文或大小写字母！")
                return False
            
            # 检查姓名重复（排除当前选手）
            for i, p in enumerate(self.game.players):
                if i != player_index and p.name == new_value:
                    self.show_error(f"选手'{new_value}'已存在！")
                    return False
            
            # 更新姓名
            player.name = new_value
            return True
            
        elif self.editing_column == '#3':  # HP值列
            # 验证HP值
            try:
                hp_value = int(new_value)
                if hp_value < 2 or hp_value > 8:
                    self.show_error("HP值必须在2-8之间！")
                    return False
            except ValueError:
                self.show_error("HP值必须是数字！")
                return False
            
            # 更新HP值
            player.initial_lives = hp_value
            player.current_lives = hp_value  # 同时更新当前HP
            return True
        
        return False
    
    def show_error(self, message):
        """显示错误提示"""
        error_window = tk.Toplevel(self.root)
        error_window.title("错误")
        error_window.geometry("300x100")
        error_window.transient(self.root)
        error_window.grab_set()
        
        error_label = tk.Label(error_window, text=message, 
                              fg='red', font=('Arial', 10))
        error_label.pack(pady=20)
        
        ok_button = tk.Button(error_window, text="确定", command=error_window.destroy)
        ok_button.pack(pady=10)
    
    def add_player(self):
        name = self.name_var.get().strip()
        lives = self.lives_var.get()
        
        if name and lives:
            # 检查姓名是否重复
            if self.game.is_name_duplicate(name):
                # 显示错误提示
                error_window = tk.Toplevel(self.root)
                error_window.title("错误")
                error_window.geometry("300x100")
                error_window.transient(self.root)
                error_window.grab_set()
                
                error_label = tk.Label(error_window, text=f"选手'{name}'已存在，请使用不同的姓名！", 
                                      fg='red', font=('Arial', 10))
                error_label.pack(pady=20)
                
                ok_button = tk.Button(error_window, text="确定", command=error_window.destroy)
                ok_button.pack(pady=10)
                return
            
            # 验证姓名首字符：只允许中文或大小写字母
            first_char = name[0]
            if not (('\u4e00' <= first_char <= '\u9fff') or  # 中文字符
                    ('A' <= first_char <= 'Z') or              # 大写字母
                    ('a' <= first_char <= 'z')):              # 小写字母
                # 显示错误提示
                error_window = tk.Toplevel(self.root)
                error_window.title("错误")
                error_window.geometry("300x100")
                error_window.transient(self.root)
                error_window.grab_set()
                
                error_label = tk.Label(error_window, text="姓名首字符必须是中文或大小写字母！", 
                                      fg='red', font=('Arial', 10))
                error_label.pack(pady=20)
                
                ok_button = tk.Button(error_window, text="确定", command=error_window.destroy)
                ok_button.pack(pady=10)
                return
            
            # 添加选手
            if self.game.add_player(name, int(lives)):
                self.name_var.set("")
                self.create_setup_screen()
    
    def refresh_name_combobox(self):
        """刷新姓名下拉框的选项"""
        if hasattr(self, 'name_combobox'):
            self.name_combobox['values'] = self.fixed_participant_manager.get_all_names()
    
    def on_name_selected(self, event):
        """选择固定参赛选手时自动填充HP"""
        selected_name = self.name_var.get()
        participant = self.fixed_participant_manager.get_participant(selected_name)
        if participant:
            self.lives_var.set(str(participant.initial_hp))
    
    def on_window_resize(self, event):
        """窗口大小变化事件处理 - 动态调整表格列宽"""
        # 只有在设置界面才处理列宽调整
        if hasattr(self, 'players_table') and self.players_table.winfo_exists():
            # 获取表格容器的当前宽度
            container_width = self.players_table.winfo_width()
            
            # 如果容器宽度有效，则调整列宽
            if container_width > 100:
                # 计算可用宽度（减去滚动条和边框）
                available_width = container_width - 20  # 减去滚动条和边距
                
                # 设置固定列宽
                fixed_widths = 80 + 80  # 序号列和HP值列的固定宽度
                
                # 计算姓名列的动态宽度
                name_width = max(120, available_width - fixed_widths)
                
                # 更新列宽
                self.players_table.column('姓名', width=name_width)
    
    def on_mouse_motion(self, event):
        """鼠标移动事件处理 - 显示HP数字提示"""
        # 获取鼠标位置对应的行和列
        item = self.players_table.identify_row(event.y)
        column = self.players_table.identify_column(event.x)
        
        # 只有在HP列才显示提示
        if item and column == '#3':  # HP值列
            # 获取该行的数据
            values = self.players_table.item(item, 'values')
            if values and len(values) >= 3:
                # 计算HP值（小点数量）
                dots_text = values[2]
                hp_value = len(dots_text)
                
                # 显示工具提示
                self.show_tooltip(event.x_root, event.y_root, f"HP: {hp_value}")
        else:
            # 隐藏工具提示
            self.hide_tooltip()
    
    def show_tooltip(self, x, y, text):
        """显示工具提示"""
        # 如果提示文本相同且已经显示，则不重复创建
        if self.tooltip_text == text and self.tooltip and self.tooltip.winfo_exists():
            # 更新位置
            self.tooltip.geometry(f"+{x+10}+{y+10}")
            return
        
        # 隐藏之前的提示
        self.hide_tooltip()
        
        # 创建新提示
        self.tooltip_text = text
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x+10}+{y+10}")
        
        # 设置提示样式
        label = tk.Label(self.tooltip, text=text, background="lightyellow", 
                        relief="solid", borderwidth=1, font=('Arial', 9))
        label.pack(ipadx=5, ipady=2)
        
        # 设置自动隐藏
        self.tooltip.after(3000, self.hide_tooltip)
    
    def hide_tooltip(self):
        """隐藏工具提示"""
        if self.tooltip and self.tooltip.winfo_exists():
            self.tooltip.destroy()
            self.tooltip = None
            self.tooltip_text = None
    
    def remove_player(self, index: int):
        """删除指定索引的选手"""
        if 0 <= index < len(self.game.players):
            self.game.remove_player(index)
            self.create_setup_screen()
    
    def start_game(self):
        if self.game.start_game():
            self.create_game_screen()
    
    def load_history_state(self):
        """加载历史状态"""
        if self.game.load_states_from_file():
            # 状态加载成功，跳转到游戏界面
            self.create_game_screen()
        else:
            # 状态加载失败
            messagebox.showinfo("提示", "没有找到历史状态文件，无法加载历史状态")
    
    # 右键菜单功能已删除，改用判负离场按钮
    
    def eliminate_player(self, player, table_id, position):
        """选手判负离场"""
        print(f"DEBUG: eliminate_player 被调用 - 选手: {player.name}, 球台: {table_id}, 位置: {position}")
        
        # 确认对话框
        confirm = messagebox.askyesno(
            "确认判负离场", 
            f"确定要让 {table_id} 号台的 {player.name} 判负离场吗？\n\n当前HP: {player.current_lives}/{player.initial_lives}"
        )
        
        if not confirm:
            print("DEBUG: 用户取消了判负离场操作")
            return
        
        print("DEBUG: 用户确认了判负离场操作")
        print(f"DEBUG: self.game 对象 id: {id(self.game)}")
        print(f"DEBUG: self.game.eliminate_player 方法: {self.game.eliminate_player}")
        
        # 执行离场逻辑
        success = self.game.eliminate_player(player, table_id)
        print(f"DEBUG: eliminate_player 返回: {success}")
        
        if success:
            print("DEBUG: 判负离场逻辑执行成功")
            # 离场后立即触发上场逻辑（安排场外候补选手上桌）
            self.game.fill_leftover_tables()
            # 刷新界面
            self.create_game_screen()
            messagebox.showinfo("离场成功", f"选手 {player.name} 已判负离场")
        else:
            print("DEBUG: 判负离场逻辑执行失败")
            messagebox.showerror("离场失败", "判负离场操作失败，请重试")
    
    def show_table_reduction_dialog(self, table_id, players_info):
        """显示减桌对话框"""
        messagebox.showinfo(
            "球台撤桌通知",
            f"{table_id}号球台需要撤桌！\n\n"
            f"该球台的选手需要移步到场外候补区等待：\n"
            f"{players_info}\n\n"
            f"请确认继续操作。"
        )
    
    def next_step(self):
        self.game.fill_leftover_tables()
        self.game.update()
        if self.game.game_state == "running":
            self.create_game_screen()
        else:
            self.create_finished_screen()
    
    def prev_state(self):
        """回退到上一个状态"""
        current_index = self.game.get_current_state_index()
        if current_index > 0:
            self.game.restore_state(current_index - 1)
            self.create_game_screen()
    
    def next_state(self):
        """前进到下一个状态"""
        current_index = self.game.get_current_state_index()
        state_count = self.game.get_state_count()
        if current_index < state_count - 1:
            self.game.restore_state(current_index + 1)
            self.create_game_screen()
    
    def enter_current_state(self):
        """进入当前状态 - 删除之后的所有状态"""
        self.game.delete_future_states()
        # 保存状态到文件
        self.game.save_states_to_file()
        messagebox.showinfo("状态确认", "已进入当前状态，之后的状态已删除！")
        self.create_game_screen()
    
    def on_test_mode_change(self):
        """测试模式复选框变化事件处理"""
        if self.test_mode_var.get():
            # 清空现有选手
            self.game.players = []
            # 添加测试选手
            for name, lives in self.example_players:
                self.game.add_player(name, lives)
        else:
            # 清空选手列表
            self.game.players = []
        
        # 重新创建整个界面
        self.create_setup_screen()
    
    def update_players_table(self):
        """更新选手表格内容"""
        # 清空表格
        for item in self.players_table.get_children():
            self.players_table.delete(item)
        
        # 填充表格数据 - HP值用红色小点显示
        for i, player in enumerate(self.game.players):
            # 将HP值转换为红色小点 - 使用更紧凑的显示
            dots = '●' * player.initial_lives
            self.players_table.insert('', 'end', values=(i+1, player.name, dots))
    
    def restart_game(self):
        import os
        import json
        
        # 保存当前选手列表
        current_players = [(p.name, p.initial_lives) for p in self.game.players]
        
        # 删除历史状态文件
        state_file = "game_states.json"
        if os.path.exists(state_file):
            os.remove(state_file)
            print(f"已删除状态文件: {state_file}")
        
        # 重新开始游戏
        self.game = Game()
        
        # 重新添加之前保存的选手
        if current_players:
            for name, lives in current_players:
                self.game.add_player(name, lives)
        else:
            # 如果没有选手，添加示例选手
            for name, lives in self.example_players:
                self.game.add_player(name, lives)
        
        # 开始新比赛并进入第二页
        if self.game.start_game():
            # 创建一个空的状态文件
            self.game.save_states_to_file()
            self.create_game_screen()
    
    def create_table_thresholds_screen(self):
        """创建球桌阈值设定界面"""
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="设定球桌阈值", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 返回按钮
        back_button = tk.Button(self.root, text="返回主界面", 
                                command=self.create_setup_screen,
                                font=('Arial', 12), width=15)
        back_button.pack(pady=10)
        
        # 说明文字
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text="说明：修改阈值后，game_states.json 历史状态文件将被删除！", 
                fg='red', font=('Arial', 12, 'bold')).pack()
        
        # 阈值输入区域
        thresholds_frame = tk.Frame(self.root)
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
        self.threshold_vars = []
        default_thresholds = self.thresholds_manager.thresholds
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
            self.threshold_vars.append(var)
            
            # 绑定回调函数，当值变化时联动更新后面的值
            var.trace_add('write', lambda name, index, mode, idx=i: self.on_threshold_change(idx))
            
            entry = tk.Entry(row_frame, textvariable=var, width=10, font=('Arial', 12))
            entry.pack(side=tk.LEFT, padx=5)
            
            tk.Label(row_frame, text="人", font=('Arial', 12)).pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        save_button = tk.Button(button_frame, text="保存阈值", 
                               command=self.save_table_thresholds,
                               bg='green', fg='white', font=('Arial', 12, 'bold'), width=12)
        save_button.pack(side=tk.LEFT, padx=10)
        
        reset_button = tk.Button(button_frame, text="恢复默认", 
                                command=self.reset_table_thresholds,
                                bg='orange', fg='white', font=('Arial', 12, 'bold'), width=12)
        reset_button.pack(side=tk.LEFT, padx=10)
    
    def on_threshold_change(self, changed_index):
        """当某个阈值被修改时，联动更新后面的值"""
        try:
            # 获取当前修改的值
            current_value = int(self.threshold_vars[changed_index].get())
            
            # 联动更新后面的每个值，确保至少比前一个大1
            for i in range(changed_index + 1, 8):
                try:
                    # 获取当前值
                    prev_value = int(self.threshold_vars[i-1].get())
                    current_var_value = int(self.threshold_vars[i].get())
                    
                    # 如果当前值小于等于前面的值，设置为前面的值+1
                    if current_var_value <= prev_value:
                        self.threshold_vars[i].set(str(prev_value + 1))
                except ValueError:
                    pass
        except ValueError:
            pass
    
    def save_table_thresholds(self):
        """保存球桌阈值"""
        try:
            # 获取输入的阈值
            thresholds = []
            for var in self.threshold_vars:
                value = int(var.get())
                thresholds.append(value)
            
            # 验证并保存
            success, error_msg = self.thresholds_manager.set_thresholds(thresholds)
            if success:
                # 重新初始化game，使用新的阈值
                self.game = Game(self.thresholds_manager)
                self.game.set_table_reduction_callback(self.show_table_reduction_dialog)
                
                messagebox.showinfo("成功", "球桌阈值保存成功！\ngame_states.json 历史状态文件已删除。")
                self.create_setup_screen()
            else:
                messagebox.showerror("错误", f"阈值设置失败：{error_msg}")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数！")
    
    def reset_table_thresholds(self):
        """恢复默认阈值"""
        default_thresholds = TableThresholdsManager.DEFAULT_THRESHOLDS
        success, error_msg = self.thresholds_manager.set_thresholds(default_thresholds)
        if success:
            # 重新初始化game，使用新的阈值
            self.game = Game(self.thresholds_manager)
            self.game.set_table_reduction_callback(self.show_table_reduction_dialog)
            
            messagebox.showinfo("成功", "已恢复默认阈值！\ngame_states.json 历史状态文件已删除。")
            self.create_table_thresholds_screen()
        else:
            messagebox.showerror("错误", f"恢复默认失败：{error_msg}")
    
    def create_fixed_participants_screen(self):
        """创建固定参赛选手管理界面"""
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(self.root, text="固定参赛选手管理", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 返回按钮
        back_button = tk.Button(self.root, text="返回主界面", 
                                command=self.create_setup_screen,
                                font=('Arial', 12), width=15)
        back_button.pack(pady=10)
        
        # 主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：选手列表
        list_frame = tk.Frame(main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(list_frame, text="固定参赛选手列表", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # 创建带垂直滚动条的框架
        tree_frame = tk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview显示选手列表
        columns = ("name", "contact", "email", "address", "initial_hp")
        self.fixed_participants_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.fixed_participants_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置Treeview使用滚动条
        self.fixed_participants_tree.configure(yscrollcommand=scrollbar.set)
        
        self.fixed_participants_tree.heading("name", text="姓名")
        self.fixed_participants_tree.heading("contact", text="联系方式")
        self.fixed_participants_tree.heading("email", text="邮箱")
        self.fixed_participants_tree.heading("address", text="家庭住址")
        self.fixed_participants_tree.heading("initial_hp", text="初始HP")
        
        self.fixed_participants_tree.column("name", width=100)
        self.fixed_participants_tree.column("contact", width=120)
        self.fixed_participants_tree.column("email", width=150)
        self.fixed_participants_tree.column("address", width=200)
        self.fixed_participants_tree.column("initial_hp", width=60)
        
        self.fixed_participants_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fixed_participants_tree.bind("<<TreeviewSelect>>", self.on_fixed_participant_select)
        
        # 右侧：编辑区域
        edit_frame = tk.Frame(main_frame)
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        tk.Label(edit_frame, text="选手信息编辑", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # 表单框架
        form_frame = tk.Frame(edit_frame)
        form_frame.pack(pady=10)
        
        # 姓名
        name_label_frame = tk.Frame(form_frame)
        name_label_frame.grid(row=0, column=0, sticky=tk.E, pady=5)
        tk.Label(name_label_frame, text="姓名").pack(side=tk.LEFT)
        tk.Label(name_label_frame, text="*", fg="red").pack(side=tk.LEFT)
        tk.Label(name_label_frame, text=":").pack(side=tk.LEFT)
        self.fp_name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.fp_name_var, width=25).grid(row=0, column=1, pady=5)
        
        # 联系方式
        contact_label_frame = tk.Frame(form_frame)
        contact_label_frame.grid(row=1, column=0, sticky=tk.E, pady=5)
        tk.Label(contact_label_frame, text="联系方式").pack(side=tk.LEFT)
        tk.Label(contact_label_frame, text="*", fg="red").pack(side=tk.LEFT)
        tk.Label(contact_label_frame, text=":").pack(side=tk.LEFT)
        self.fp_contact_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.fp_contact_var, width=25).grid(row=1, column=1, pady=5)
        
        # 邮箱
        tk.Label(form_frame, text="邮箱:").grid(row=2, column=0, sticky=tk.E, pady=5)
        self.fp_email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.fp_email_var, width=25).grid(row=2, column=1, pady=5)
        
        # 家庭住址
        tk.Label(form_frame, text="家庭住址:").grid(row=3, column=0, sticky=tk.E, pady=5)
        self.fp_address_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.fp_address_var, width=25).grid(row=3, column=1, pady=5)
        
        # 初始HP
        hp_label_frame = tk.Frame(form_frame)
        hp_label_frame.grid(row=4, column=0, sticky=tk.E, pady=5)
        tk.Label(hp_label_frame, text="初始HP").pack(side=tk.LEFT)
        tk.Label(hp_label_frame, text="*", fg="red").pack(side=tk.LEFT)
        tk.Label(hp_label_frame, text=":").pack(side=tk.LEFT)
        self.fp_hp_var = tk.IntVar(value=2)
        hp_frame = tk.Frame(form_frame)
        hp_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        for hp in range(2, 9):
            tk.Radiobutton(hp_frame, text=str(hp), variable=self.fp_hp_var, value=hp).pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = tk.Frame(edit_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="添加选手", command=self.add_fixed_participant, 
                 width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="修改选手", command=self.update_fixed_participant, 
                 width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="删除选手", command=self.delete_fixed_participant, 
                 width=12).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="清空表单", command=self.clear_fixed_participant_form, 
                 width=12).grid(row=1, column=0, columnspan=3, pady=5)
        
        # 当前选中的选手
        self.current_selected_fixed_participant = None
        
        # 刷新选手列表
        self.refresh_fixed_participants_list()
    
    def refresh_fixed_participants_list(self):
        """刷新固定参赛选手列表"""
        # 清空列表
        for item in self.fixed_participants_tree.get_children():
            self.fixed_participants_tree.delete(item)
        
        # 添加所有选手
        for participant in self.fixed_participant_manager.get_all_participants():
            self.fixed_participants_tree.insert("", tk.END, values=(
                participant.name,
                participant.contact,
                participant.email,
                participant.address,
                participant.initial_hp
            ))
    
    def on_fixed_participant_select(self, event):
        """选择选手时填充表单"""
        selected_items = self.fixed_participants_tree.selection()
        if selected_items:
            item = self.fixed_participants_tree.item(selected_items[0])
            values = item["values"]
            self.fp_name_var.set(values[0])
            self.fp_contact_var.set(values[1])
            self.fp_email_var.set(values[2])
            self.fp_address_var.set(values[3])
            self.fp_hp_var.set(values[4])
            self.current_selected_fixed_participant = values[0]
    
    def add_fixed_participant(self):
        """添加固定参赛选手"""
        name = self.fp_name_var.get().strip()
        contact = self.fp_contact_var.get().strip()
        email = self.fp_email_var.get().strip()
        address = self.fp_address_var.get().strip()
        initial_hp = self.fp_hp_var.get()
        
        # 验证必填字段
        if not name or not contact:
            messagebox.showerror("错误", "姓名和联系方式为必填项！")
            return
        
        # 验证姓名格式（和主界面保持一致）
        if len(name) < 1 or len(name) > 20:
            messagebox.showerror("错误", "姓名长度必须在1-20个字符之间！")
            return
        
        # 创建选手
        participant = FixedParticipant(name, contact, email, address, initial_hp)
        
        # 添加选手
        if self.fixed_participant_manager.add_participant(participant):
            messagebox.showinfo("成功", f"选手 {name} 添加成功！")
            self.refresh_fixed_participants_list()
            self.clear_fixed_participant_form()
        else:
            messagebox.showerror("错误", f"选手 {name} 已存在！")
    
    def update_fixed_participant(self):
        """更新固定参赛选手"""
        if not self.current_selected_fixed_participant:
            messagebox.showerror("错误", "请先选择要修改的选手！")
            return
        
        name = self.fp_name_var.get().strip()
        contact = self.fp_contact_var.get().strip()
        email = self.fp_email_var.get().strip()
        address = self.fp_address_var.get().strip()
        initial_hp = self.fp_hp_var.get()
        
        # 验证必填字段
        if not name or not contact:
            messagebox.showerror("错误", "姓名和联系方式为必填项！")
            return
        
        # 验证姓名格式
        if len(name) < 1 or len(name) > 20:
            messagebox.showerror("错误", "姓名长度必须在1-20个字符之间！")
            return
        
        # 创建选手
        participant = FixedParticipant(name, contact, email, address, initial_hp)
        
        # 更新选手
        if self.fixed_participant_manager.update_participant(self.current_selected_fixed_participant, participant):
            messagebox.showinfo("成功", f"选手信息更新成功！")
            self.refresh_fixed_participants_list()
            self.clear_fixed_participant_form()
        else:
            messagebox.showerror("错误", "选手更新失败，可能姓名已存在！")
    
    def delete_fixed_participant(self):
        """删除固定参赛选手"""
        if not self.current_selected_fixed_participant:
            messagebox.showerror("错误", "请先选择要删除的选手！")
            return
        
        name = self.current_selected_fixed_participant
        if messagebox.askyesno("确认", f"确定要删除选手 {name} 吗？"):
            if self.fixed_participant_manager.delete_participant(name):
                messagebox.showinfo("成功", f"选手 {name} 删除成功！")
                self.refresh_fixed_participants_list()
                self.clear_fixed_participant_form()
    
    def clear_fixed_participant_form(self):
        """清空表单"""
        self.fp_name_var.set("")
        self.fp_contact_var.set("")
        self.fp_email_var.set("")
        self.fp_address_var.set("")
        self.fp_hp_var.set(2)
        self.current_selected_fixed_participant = None
        # 取消选择
        for item in self.fixed_participants_tree.selection():
            self.fixed_participants_tree.selection_remove(item)
    
    def run(self):
        self.root.mainloop()