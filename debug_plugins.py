from core.plugins.registry import get_registry
from core.plugins.loader import load_all_plugins

registry = get_registry()

load_all_plugins()

plugins = registry.get_all_plugins()

print("COUNT =", len(plugins))

for p in plugins:
    print(p.name, p.category, p.capability)