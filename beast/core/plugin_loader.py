"""
Dynamic Plugin Loader
Loads and manages plugins and departments dynamically
"""

import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Any, Optional, Type
from beast.core.registry import Registry


class PluginLoader:
    """
    Loads plugins and departments dynamically from filesystem
    Supports hot-reloading and dynamic discovery
    """
    
    def __init__(self, registry: Registry):
        self.registry = registry
        self._loaded_modules: Dict[str, Any] = {}
    
    def load_department_from_module(self, module_path: str, department_class_name: str) -> Any:
        """
        Load a department from a Python module
        
        Args:
            module_path: Full module path (e.g., 'beast.departments.hadracha.classes')
            department_class_name: Name of the department class
        
        Returns:
            Department instance
        """
        try:
            module = importlib.import_module(module_path)
            department_class = getattr(module, department_class_name)
            
            # Verify it's a department class
            from beast.departments.base_department import BaseDepartment
            if not issubclass(department_class, BaseDepartment):
                raise TypeError(f"{department_class_name} is not a valid department class")
            
            instance = department_class()
            self._loaded_modules[module_path] = module
            return instance
            
        except ImportError as e:
            raise ImportError(f"Failed to import module {module_path}: {e}")
        except AttributeError as e:
            raise AttributeError(f"Class {department_class_name} not found in {module_path}: {e}")
    
    def load_department_from_file(self, file_path: Path) -> Any:
        """
        Load a department from a Python file
        
        Args:
            file_path: Path to the Python file containing the department
        
        Returns:
            Department instance
        """
        # Convert file path to module path
        # This is a simplified version - in production, you'd need more complex handling
        spec = importlib.util.spec_from_file_location("dynamic_department", file_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load spec from {file_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find department class in module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            from beast.departments.base_department import BaseDepartment
            if issubclass(obj, BaseDepartment) and obj != BaseDepartment:
                instance = obj()
                return instance
        
        raise ValueError(f"No department class found in {file_path}")
    
    def discover_departments(self, base_path: Path) -> Dict[str, Path]:
        """
        Discover all department modules in a directory
        
        Args:
            base_path: Base directory to search
        
        Returns:
            Dictionary mapping department names to their file paths
        """
        departments = {}
        
        for dept_dir in base_path.iterdir():
            if dept_dir.is_dir() and not dept_dir.name.startswith('__'):
                # Look for __init__.py or main module file
                init_file = dept_dir / "__init__.py"
                if init_file.exists():
                    departments[dept_dir.name] = init_file
        
        return departments
    
    def reload_module(self, module_path: str):
        """Reload a previously loaded module"""
        if module_path in self._loaded_modules:
            importlib.reload(self._loaded_modules[module_path])
