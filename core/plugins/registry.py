class PluginRegistry:
    def __init__(self):
        self.plugins = {}
        self.graph = {}

    def register(self, plugin):
        self.plugins[plugin.name] = plugin
        self.graph[plugin.name] = {
            "category": plugin.category,
            "capability": plugin.capability
        }

    def get(self, name):
        return self.plugins.get(name)

    def all(self):
        return self.plugins

    def get_all_plugins(self):
        return list(self.plugins.values())


_registry = PluginRegistry()

def get_registry():
    return _registry