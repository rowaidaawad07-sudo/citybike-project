from abc import ABC, abstractmethod
from datetime import datetime

class Entity(ABC):
    """كلاس أساسي مجرد لجميع الكيانات"""
    
    def __init__(self, entity_id: str):
        self._id = entity_id
        self._created_at = datetime.now()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass