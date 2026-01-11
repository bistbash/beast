"""
Dynamic Registry System
Manages registration and retrieval of departments, automations, and plugins
"""

from typing import Dict, Any, List, Optional, Type
from abc import ABC, abstractmethod


class Registry:
    """
    Central registry for all dynamic components
    Supports runtime registration of departments, automations, and plugins
    """
    
    def __init__(self):
        self._departments: Dict[str, Any] = {}
        self._automations: Dict[str, List[Any]] = {}
        self._plugins: Dict[str, Any] = {}
        self._hierarchy_config: Optional[Dict] = None
    
    def register_department(self, name: str, department_instance: Any):
        """Register a department with the system"""
        if name in self._departments:
            raise ValueError(f"Department '{name}' is already registered")
        self._departments[name] = department_instance
    
    def get_department(self, name: str) -> Optional[Any]:
        """Retrieve a registered department"""
        return self._departments.get(name)
    
    def list_departments(self) -> List[str]:
        """List all registered department names"""
        return list(self._departments.keys())
    
    def unregister_department(self, name: str):
        """Remove a department from registry"""
        if name in self._departments:
            del self._departments[name]
    
    def register_automation(self, department: str, automation_name: str, automation_instance: Any):
        """Register an automation for a specific department"""
        if department not in self._automations:
            self._automations[department] = {}
        if automation_name in self._automations[department]:
            raise ValueError(f"Automation '{automation_name}' already exists in department '{department}'")
        self._automations[department][automation_name] = automation_instance
    
    def get_automation(self, department: str, automation_name: str) -> Optional[Any]:
        """Retrieve a specific automation"""
        if department not in self._automations:
            return None
        return self._automations[department].get(automation_name)
    
    def list_automations(self, department: Optional[str] = None) -> Dict[str, List[str]]:
        """List all automations, optionally filtered by department"""
        if department:
            return {department: list(self._automations.get(department, {}).keys())}
        return {dept: list(autos.keys()) for dept, autos in self._automations.items()}
    
    def register_plugin(self, plugin_name: str, plugin_instance: Any):
        """Register a plugin"""
        if plugin_name in self._plugins:
            raise ValueError(f"Plugin '{plugin_name}' is already registered")
        self._plugins[plugin_name] = plugin_instance
    
    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Retrieve a plugin"""
        return self._plugins.get(plugin_name)
    
    def set_hierarchy_config(self, config: Dict):
        """Set the hierarchy configuration dynamically"""
        self._hierarchy_config = config
    
    def get_hierarchy_config(self) -> Optional[Dict]:
        """Get the current hierarchy configuration"""
        return self._hierarchy_config
    
    def reload_department(self, name: str):
        """Reload a department (useful for hot-reloading)"""
        dept = self.get_department(name)
        if dept and hasattr(dept, 'reload'):
            dept.reload()
            return True
        return False
