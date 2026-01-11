"""
Configuration Loader
Loads and manages dynamic configurations from files or database
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from beast.core.registry import Registry


class ConfigLoader:
    """
    Loads configurations dynamically
    Supports JSON and YAML formats
    Can reload configurations at runtime
    """
    
    def __init__(self, registry: Registry):
        self.registry = registry
        self._configs: Dict[str, Dict] = {}
    
    def load_from_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load configuration from a file
        
        Args:
            file_path: Path to configuration file (JSON or YAML)
        
        Returns:
            Configuration dictionary
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            elif file_path.suffix == '.json':
                config = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {file_path.suffix}")
        
        config_name = file_path.stem
        self._configs[config_name] = config
        return config
    
    def load_hierarchy_config(self, file_path: Path):
        """
        Load hierarchy configuration and register it
        
        Args:
            file_path: Path to hierarchy configuration file
        """
        config = self.load_from_file(file_path)
        self.registry.set_hierarchy_config(config)
        return config
    
    def get_config(self, config_name: str) -> Optional[Dict]:
        """Get a loaded configuration"""
        return self._configs.get(config_name)
    
    def reload_config(self, file_path: Path) -> Dict[str, Any]:
        """Reload a configuration file"""
        return self.load_from_file(file_path)
    
    def set_config(self, config_name: str, config: Dict[str, Any]):
        """Set configuration programmatically"""
        self._configs[config_name] = config
