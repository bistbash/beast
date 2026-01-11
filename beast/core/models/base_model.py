"""
Base Model for all entities
Provides common functionality for dynamic models
"""

from abc import ABC
from typing import Dict, Any, Optional
from datetime import datetime


class BaseModel(ABC):
    """Base class for all models in the system"""
    
    def __init__(self, **kwargs):
        self._metadata: Dict[str, Any] = {}
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
        
        # Allow dynamic attribute assignment
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif isinstance(value, BaseModel):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        return result
    
    def from_dict(self, data: Dict[str, Any]):
        """Load model from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) or not key.startswith('_'):
                setattr(self, key, value)
        return self
    
    def set_metadata(self, key: str, value: Any):
        """Set metadata value"""
        self._metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value"""
        return self._metadata.get(key, default)
    
    def update(self, **kwargs):
        """Update model fields"""
        for key, value in kwargs.items():
            if hasattr(self, key) or not key.startswith('_'):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        return self
