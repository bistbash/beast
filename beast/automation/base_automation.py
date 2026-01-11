"""
Base Automation Class
All automations must inherit from this class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAutomation(ABC):
    """Base class for all automations"""
    
    def __init__(self, department: Any):
        """
        Initialize automation
        
        Args:
            department: Department instance that owns this automation
        """
        self.department = department
        self.last_run: Optional[datetime] = None
        self.enabled = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Automation name in Hebrew"""
        pass
    
    @property
    @abstractmethod
    def name_en(self) -> str:
        """Automation name in English"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the automation
        
        Args:
            **kwargs: Automation-specific parameters
        
        Returns:
            Result dictionary
        """
        pass
    
    def can_run(self) -> bool:
        """Check if automation can run"""
        return self.enabled
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Run the automation (wrapper around execute)"""
        if not self.can_run():
            return {"success": False, "error": "Automation is disabled"}
        
        try:
            result = self.execute(**kwargs)
            self.last_run = datetime.now()
            result["success"] = True
            result["timestamp"] = self.last_run.isoformat()
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_info(self) -> Dict[str, Any]:
        """Get automation information"""
        return {
            "name": self.name,
            "name_en": self.name_en,
            "department": self.department.name_en if self.department else None,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None
        }
