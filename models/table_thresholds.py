from typing import List, Tuple

class TableThresholdsManager:
    """球桌阈值管理类"""
    DEFAULT_THRESHOLDS = [6, 10, 14, 17, 20, 24, 27, 31]
    THRESHOLDS_FILE = "table_thresholds.json"
    STATE_HISTORY_FILE = "game_states.json"
    
    def __init__(self):
        self.thresholds = self.DEFAULT_THRESHOLDS.copy()
        self.load()
    
    def load(self):
        """从文件加载球桌阈值"""
        import os
        import json
        
        if os.path.exists(self.THRESHOLDS_FILE):
            try:
                with open(self.THRESHOLDS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) == 8:
                        self.thresholds = data
            except Exception as e:
                print(f"加载球桌阈值失败: {e}")
                self.thresholds = self.DEFAULT_THRESHOLDS.copy()
    
    def save(self):
        """保存球桌阈值到文件"""
        import json
        
        with open(self.THRESHOLDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.thresholds, f, ensure_ascii=False)
    
    def validate_thresholds(self, thresholds):
        """校验阈值是否有效"""
        if len(thresholds) != 8:
            return False, "阈值数量必须为8个"
        
        for i, t in enumerate(thresholds):
            if not isinstance(t, int) or t <= 0:
                return False, f"第{i+1}个阈值必须是正整数"
        
        for i in range(1, len(thresholds)):
            if thresholds[i] <= thresholds[i-1]:
                return False, f"第{i+1}个阈值必须大于第{i}个阈值"
        
        return True, ""
    
    def set_thresholds(self, thresholds):
        """设置新的阈值，返回是否成功和错误信息"""
        is_valid, error_msg = self.validate_thresholds(thresholds)
        if not is_valid:
            return False, error_msg
        
        self.thresholds = thresholds.copy()
        self.save()
        
        import os
        if os.path.exists(self.STATE_HISTORY_FILE):
            try:
                os.remove(self.STATE_HISTORY_FILE)
            except Exception as e:
                print(f"删除历史状态文件失败: {e}")
        
        return True, ""
    
    def get_thresholds_dict(self):
        """获取阈值字典格式"""
        return {
            1: 1,
            self.thresholds[0]: 2,
            self.thresholds[1]: 3,
            self.thresholds[2]: 4,
            self.thresholds[3]: 5,
            self.thresholds[4]: 6,
            self.thresholds[5]: 7,
            self.thresholds[6]: 8,
            self.thresholds[7]: 9
        }
