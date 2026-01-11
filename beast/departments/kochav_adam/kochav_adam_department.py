"""
כוח אדם - Human Resources Department
Manages personnel, assignments, and roles
"""

from typing import Dict, Any, List
from beast.departments.base_department import BaseDepartment
from beast.core.models.user import User


class KochavAdamDepartment(BaseDepartment):
    """מחלקת כוח אדם - Human Resources Department"""
    
    @property
    def name(self) -> str:
        return "כוח אדם"
    
    @property
    def name_en(self) -> str:
        return "kochav_adam"
    
    def __init__(self, registry=None, event_system=None):
        super().__init__(registry, event_system)
        self.users: Dict[str, User] = {}
    
    def initialize(self):
        """Initialize the department"""
        super().initialize()
    
    def register_user(self, user: User):
        """Register a new user"""
        if user.id_number in self.users:
            raise ValueError(f"משתמש עם תעודת זהות {user.id_number} כבר קיים")
        
        self.users[user.id_number] = user
        
        # Emit event
        self.emit_event("user_created", {
            "id_number": user.id_number,
            "full_name": user.full_name,
            "rank_name": user.rank_name,
            "department": user.department,
            "class_name": user.class_name
        })
    
    def get_user(self, id_number: str) -> User:
        """Get user by ID number"""
        return self.users.get(id_number)
    
    def get_available_automations(self) -> Dict[str, Any]:
        """Get available automations"""
        return {
            "personnel_report": None,  # To be implemented
            "role_assignment": None     # To be implemented
        }
