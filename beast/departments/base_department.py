"""
Base Department Class
All departments must inherit from this class
Provides common functionality and plugin interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from beast.core.registry import Registry
from beast.core.event_system import EventSystem


class BaseDepartment(ABC):
    """
    Base class for all departments
    Provides plugin interface and common functionality
    """
    
    def __init__(self, registry: Optional[Registry] = None, 
                 event_system: Optional[EventSystem] = None):
        """
        Initialize department
        
        Args:
            registry: Registry instance for registration
            event_system: Event system for communication
        """
        self.registry = registry
        self.event_system = event_system
        self._automations: Dict[str, Any] = {}
        self._initialized = False
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Department name in Hebrew"""
        pass
    
    @property
    @abstractmethod
    def name_en(self) -> str:
        """Department name in English (for internal use)"""
        pass
    
    def initialize(self):
        """
        Initialize the department
        Called after registration
        """
        if self._initialized:
            return
        
        # Register automations
        self._register_automations()
        
        # Subscribe to events if needed
        if self.event_system:
            self._subscribe_to_events()
        
        self._initialized = True
    
    def _register_automations(self):
        """Register department automations - override in subclasses"""
        automations = self.get_available_automations()
        if self.registry:
            for auto_name, auto_instance in automations.items():
                self.registry.register_automation(
                    self.name_en, 
                    auto_name, 
                    auto_instance
                )
                self._automations[auto_name] = auto_instance
    
    def _subscribe_to_events(self):
        """Subscribe to relevant events - override in subclasses"""
        pass
    
    @abstractmethod
    def get_available_automations(self) -> Dict[str, Any]:
        """
        Return available automations for this department
        
        Returns:
            Dictionary mapping automation names to instances
        """
        pass
    
    def get_automation(self, automation_name: str) -> Optional[Any]:
        """Get an automation by name"""
        return self._automations.get(automation_name)
    
    def reload(self):
        """Reload department (for hot-reloading)"""
        # Unregister old automations
        if self.registry:
            for auto_name in self._automations.keys():
                # Note: Registry doesn't have unregister_automation yet
                # We can add it if needed
                pass
        
        # Re-initialize
        self._initialized = False
        self._automations.clear()
        self.initialize()
    
    def emit_event(self, event_type: str, data: Dict[str, Any], 
                   metadata: Optional[Dict[str, Any]] = None):
        """Emit an event"""
        if self.event_system:
            self.event_system.emit(event_type, self.name_en, data, metadata)
    
    def get_info(self) -> Dict[str, Any]:
        """Get department information"""
        return {
            "name": self.name,
            "name_en": self.name_en,
            "automations": list(self._automations.keys()),
            "initialized": self._initialized
        }
