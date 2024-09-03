# Network Monitor App
# plugin_manager.py
# version: 1.2
# description: Manages the loading and initialization of plugins for the Network Monitor application.

import os
import importlib.util

class PluginManager:
    def __init__(self, plugins_folder):
        self.plugins_folder = plugins_folder

    def load_plugins(self, application):
        """Dynamically load and initialize plugins from the plugins folder."""
        plugin_files = [f for f in os.listdir(self.plugins_folder) if f.endswith('.py') and f != '__init__.py']
        for plugin_file in plugin_files:
            plugin_name = plugin_file[:-3]  # Strip the .py extension
            module_name = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugins_folder, plugin_file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Initialize the plugin
            if hasattr(module, 'init_plugin'):
                module.init_plugin(application)
            else:
                print(f"Plugin {plugin_name} does not have an init_plugin function")
