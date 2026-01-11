
__version__ = "0.1.0"
__author__ = "Techni Beer Sheva"

from beast.core.registry import Registry
from beast.core.plugin_loader import PluginLoader

# יצירת instances גלובליים
registry = Registry()
plugin_loader = PluginLoader(registry)

__all__ = ['registry', 'plugin_loader', 'Registry', 'PluginLoader']
