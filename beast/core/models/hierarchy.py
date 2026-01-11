"""
Dynamic Hierarchy System
Hierarchy is loaded from configuration, allowing runtime changes
"""

from typing import Dict, List, Optional, Set
from beast.core.models.base_model import BaseModel
from beast.core.registry import Registry


class Rank:
    """
    Dynamic Rank representation
    Can be created from configuration or programmatically
    """
    
    def __init__(self, 
                 name: str,
                 display_name: str,
                 level: int,
                 can_manage_classes: bool = False,
                 can_manage_maks: bool = False,
                 can_manage_memach: bool = False,
                 departments: Optional[List[str]] = None,
                 parent_ranks: Optional[List[str]] = None):
        """
        Initialize a rank
        
        Args:
            name: Internal name (e.g., "maks", "memach")
            display_name: Display name in Hebrew (e.g., "מק\"ס/ית")
            level: Hierarchy level (higher = more authority)
            can_manage_classes: Can manage classes
            can_manage_maks: Can manage MAKS
            can_manage_memach: Can manage MEMACH
            departments: Departments this rank can work in
            parent_ranks: Rank names that can manage this rank
        """
        self.name = name
        self.display_name = display_name
        self.level = level
        self.can_manage_classes = can_manage_classes
        self.can_manage_maks = can_manage_maks
        self.can_manage_memach = can_manage_memach
        self.departments = departments or []
        self.parent_ranks = parent_ranks or []
    
    def can_manage_rank(self, other_rank: 'Rank') -> bool:
        """Check if this rank can manage another rank"""
        if other_rank.name in self.parent_ranks:
            return True
        
        # Higher level ranks can manage lower level ranks
        return self.level > other_rank.level
    
    @classmethod
    def from_config(cls, config: Dict) -> 'Rank':
        """Create rank from configuration dictionary"""
        return cls(
            name=config.get('name', ''),
            display_name=config.get('display_name', ''),
            level=config.get('level', 0),
            can_manage_classes=config.get('can_manage_classes', False),
            can_manage_maks=config.get('can_manage_maks', False),
            can_manage_memach=config.get('can_manage_memach', False),
            departments=config.get('departments', []),
            parent_ranks=config.get('parent_ranks', [])
        )
    
    def __repr__(self):
        return f"Rank(name={self.name}, display_name={self.display_name}, level={self.level})"


class HierarchyManager:
    """
    Manages the dynamic hierarchy system
    Loads ranks from configuration and provides hierarchy queries
    """
    
    def __init__(self, registry: Optional[Registry] = None):
        self.registry = registry
        self._ranks: Dict[str, Rank] = {}
        self._load_from_registry()
    
    def _load_from_registry(self):
        """Load hierarchy configuration from registry"""
        if self.registry:
            config = self.registry.get_hierarchy_config()
            if config:
                self.load_from_config(config)
    
    def load_from_config(self, config: Dict):
        """
        Load hierarchy from configuration
        
        Expected config structure:
        {
            "ranks": [
                {
                    "name": "shocher",
                    "display_name": "שוחר/ת",
                    "level": 0,
                    ...
                },
                ...
            ]
        }
        """
        ranks_config = config.get('ranks', [])
        self._ranks.clear()
        
        for rank_config in ranks_config:
            rank = Rank.from_config(rank_config)
            self._ranks[rank.name] = rank
    
    def get_rank(self, rank_name: str) -> Optional[Rank]:
        """Get a rank by name"""
        return self._ranks.get(rank_name)
    
    def add_rank(self, rank: Rank):
        """Add or update a rank dynamically"""
        self._ranks[rank.name] = rank
    
    def remove_rank(self, rank_name: str):
        """Remove a rank (if not in use)"""
        if rank_name in self._ranks:
            del self._ranks[rank_name]
    
    def list_ranks(self) -> List[Rank]:
        """List all ranks, sorted by level"""
        return sorted(self._ranks.values(), key=lambda r: r.level)
    
    def can_manage(self, manager_rank_name: str, managed_rank_name: str) -> bool:
        """Check if one rank can manage another"""
        manager = self.get_rank(manager_rank_name)
        managed = self.get_rank(managed_rank_name)
        
        if not manager or not managed:
            return False
        
        return manager.can_manage_rank(managed)
    
    def reload(self):
        """Reload hierarchy from registry configuration"""
        self._load_from_registry()
