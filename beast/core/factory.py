"""
Factory for initializing the entire system
Loads configurations and registers all departments
"""

from pathlib import Path
from typing import Optional
from beast.core.registry import Registry
from beast.core.event_system import EventSystem
from beast.core.config_loader import ConfigLoader
from beast.core.plugin_loader import PluginLoader
from beast.core.models.hierarchy import HierarchyManager
from beast.departments.hadracha import HadrachaDepartment
from beast.departments.logistika import LogistikaDepartment
from beast.departments.kochav_adam import KochavAdamDepartment
from beast.departments.tifool import TifoolDepartment
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import CONFIG_DIR, HIERARCHY_CONFIG_PATH, DEPARTMENTS_CONFIG_PATH


class BeastFactory:
    """
    Factory class for creating and initializing the entire BEAST system
    """
    
    def __init__(self):
        self.registry = Registry()
        self.event_system = EventSystem()
        self.config_loader = ConfigLoader(self.registry)
        self.plugin_loader = PluginLoader(self.registry)
        self.hierarchy_manager: Optional[HierarchyManager] = None
    
    def initialize(self):
        """
        Initialize the entire system
        Loads configurations and registers all departments
        """
        # Load hierarchy configuration
        hierarchy_config_path = HIERARCHY_CONFIG_PATH
        if hierarchy_config_path.exists():
            self.config_loader.load_hierarchy_config(hierarchy_config_path)
            self.hierarchy_manager = HierarchyManager(self.registry)
        else:
            # Create default hierarchy manager
            self.hierarchy_manager = HierarchyManager(self.registry)
        
        # Load and register departments
        self._load_departments()
        
        return self
    
    def _load_departments(self):
        """Load all departments from configuration or defaults"""
        # Try to load from configuration
        depts_config_path = DEPARTMENTS_CONFIG_PATH
        if depts_config_path.exists():
            depts_config = self.config_loader.load_from_file(depts_config_path)
            departments_config = depts_config.get('departments', [])
            
            for dept_config in departments_config:
                if dept_config.get('enabled', True):
                    try:
                        dept = self.plugin_loader.load_department_from_module(
                            dept_config['module_path'],
                            dept_config['class_name']
                        )
                        dept.registry = self.registry
                        dept.event_system = self.event_system
                        
                        # Special handling for Hadracha (needs hierarchy manager)
                        if isinstance(dept, HadrachaDepartment):
                            dept.hierarchy_manager = self.hierarchy_manager
                        
                        dept.initialize()
                        self.registry.register_department(dept_config['name'], dept)
                    except Exception as e:
                        print(f"Warning: Failed to load department {dept_config['name']}: {e}")
        else:
            # Load default departments directly
            self._load_default_departments()
    
    def _load_default_departments(self):
        """Load default departments if configuration is not available"""
        departments = [
            HadrachaDepartment(registry=self.registry, 
                              event_system=self.event_system,
                              hierarchy_manager=self.hierarchy_manager),
            LogistikaDepartment(registry=self.registry, event_system=self.event_system),
            KochavAdamDepartment(registry=self.registry, event_system=self.event_system),
            TifoolDepartment(registry=self.registry, event_system=self.event_system),
        ]
        
        for dept in departments:
            dept.initialize()
            self.registry.register_department(dept.name_en, dept)
    
    def get_system_info(self) -> dict:
        """Get information about the initialized system"""
        return {
            "departments": self.registry.list_departments(),
            "automations": self.registry.list_automations(),
            "hierarchy_ranks": [r.name for r in self.hierarchy_manager.list_ranks()] if self.hierarchy_manager else []
        }


def create_beast() -> BeastFactory:
    """
    Convenience function to create and initialize the BEAST system
    
    Returns:
        Initialized BeastFactory instance
    """
    factory = BeastFactory()
    factory.initialize()
    return factory
