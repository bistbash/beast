"""
User Model with Dynamic Role System
Users can have different ranks that are loaded from configuration
"""

from typing import Optional, List
from datetime import datetime
from beast.core.models.base_model import BaseModel
from beast.core.models.hierarchy import Rank, HierarchyManager


class User(BaseModel):
    """
    User model with dynamic role assignment
    Supports all ranks defined in hierarchy configuration
    """
    
    def __init__(self,
                 id_number: str,
                 full_name: str,
                 rank_name: str,
                 department: Optional[str] = None,
                 class_name: Optional[str] = None,
                 hierarchy_manager: Optional[HierarchyManager] = None,
                 **kwargs):
        """
        Initialize a user
        
        Args:
            id_number: Unique ID number
            full_name: Full name in Hebrew
            rank_name: Rank name (must exist in hierarchy)
            department: Department name (optional)
            class_name: Class name if user is MAKS or student
            hierarchy_manager: Hierarchy manager instance
            **kwargs: Additional dynamic attributes
        """
        super().__init__(**kwargs)
        self.id_number = id_number
        self.full_name = full_name
        self.rank_name = rank_name
        self.department = department
        self.class_name = class_name
        self._hierarchy_manager = hierarchy_manager
        self._rank: Optional[Rank] = None
        
        # Load rank if hierarchy manager is available
        if self._hierarchy_manager:
            self._rank = self._hierarchy_manager.get_rank(rank_name)
    
    @property
    def rank(self) -> Optional[Rank]:
        """Get the user's rank object"""
        if self._rank is None and self._hierarchy_manager:
            self._rank = self._hierarchy_manager.get_rank(self.rank_name)
        return self._rank
    
    @property
    def display_rank(self) -> str:
        """Get display name of rank"""
        if self.rank:
            return self.rank.display_name
        return self.rank_name
    
    def is_maks(self) -> bool:
        """Check if user is MAKS"""
        return self.rank_name == "maks"
    
    def is_memach(self) -> bool:
        """Check if user is MEMACH"""
        return self.rank_name == "memach"
    
    def is_student(self) -> bool:
        """Check if user is a student (shocher)"""
        return self.rank_name == "shocher"
    
    def can_manage_class(self) -> bool:
        """Check if user can manage classes"""
        if self.rank:
            return self.rank.can_manage_classes
        return False
    
    def can_manage_user(self, other_user: 'User') -> bool:
        """Check if this user can manage another user"""
        if not self.rank or not other_user.rank:
            return False
        return self.rank.can_manage_rank(other_user.rank)
    
    def get_managed_class(self) -> Optional[str]:
        """Get the class name this user manages (if MAKS)"""
        if self.is_maks() or (self.rank and self.rank.can_manage_classes):
            return self.class_name
        return None
    
    def update_rank(self, new_rank_name: str):
        """Update user's rank"""
        self.rank_name = new_rank_name
        if self._hierarchy_manager:
            self._rank = self._hierarchy_manager.get_rank(new_rank_name)
        self.updated_at = datetime.now()
    
    def set_hierarchy_manager(self, hierarchy_manager: HierarchyManager):
        """Set hierarchy manager (useful for dynamic reloading)"""
        self._hierarchy_manager = hierarchy_manager
        if self._hierarchy_manager:
            self._rank = self._hierarchy_manager.get_rank(self.rank_name)
    
    def __repr__(self):
        return f"User(id={self.id_number}, name={self.full_name}, rank={self.display_rank})"
