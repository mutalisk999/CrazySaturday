from typing import Dict, List, Optional

class FixedParticipant:
    """固定参赛选手类"""
    def __init__(self, name: str, contact: str, email: str = "", address: str = "", initial_hp: int = 2):
        self.name = name
        self.contact = contact
        self.email = email
        self.address = address
        self.initial_hp = initial_hp
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "name": self.name,
            "contact": self.contact,
            "email": self.email,
            "address": self.address,
            "initial_hp": self.initial_hp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        return cls(
            name=data["name"],
            contact=data["contact"],
            email=data.get("email", ""),
            address=data.get("address", ""),
            initial_hp=data.get("initial_hp", 2)
        )

class FixedParticipantManager:
    """固定参赛选手管理类"""
    def __init__(self, filename: str = "fixed_participants.json"):
        self.filename = filename
        self.participants: Dict[str, FixedParticipant] = {}
        self.load()
    
    def load(self):
        """从文件加载固定参赛选手"""
        import os
        import json
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.participants = {}
                    for name, participant_data in data.items():
                        self.participants[name] = FixedParticipant.from_dict(participant_data)
            except Exception as e:
                print(f"加载固定参赛选手失败: {e}")
                self.participants = {}
    
    def save(self):
        """保存固定参赛选手到文件"""
        import json
        
        data = {}
        for name, participant in self.participants.items():
            data[name] = participant.to_dict()
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_participant(self, participant: FixedParticipant) -> bool:
        """添加固定参赛选手"""
        if participant.name in self.participants:
            return False
        self.participants[participant.name] = participant
        self.save()
        return True
    
    def update_participant(self, old_name: str, participant: FixedParticipant) -> bool:
        """更新固定参赛选手"""
        if old_name in self.participants:
            if old_name != participant.name and participant.name in self.participants:
                return False
            del self.participants[old_name]
            self.participants[participant.name] = participant
            self.save()
            return True
        return False
    
    def delete_participant(self, name: str) -> bool:
        """删除固定参赛选手"""
        if name in self.participants:
            del self.participants[name]
            self.save()
            return True
        return False
    
    def get_participant(self, name: str) -> Optional[FixedParticipant]:
        """获取固定参赛选手"""
        return self.participants.get(name)
    
    def get_all_participants(self) -> List[FixedParticipant]:
        """获取所有固定参赛选手"""
        return list(self.participants.values())
    
    def get_all_names(self) -> List[str]:
        """获取所有固定参赛选手姓名"""
        return list(self.participants.keys())
