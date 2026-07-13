import importlib
import pkgutil
import inspect

import core.plugins.scanners as scanners_pkg
from core.plugins.registry import get_registry


def auto_load_plugins():
    """
    Scan all plugin modules and auto-register BasePlugin subclasses
    """

    registry = get_registry()

    for module in pkgutil.walk_packages(
        scanners_pkg.__path__,
        scanners_pkg.__name__ + "."
    ):
        mod = importlib.import_module(module.name)

        print(f"[PLUGIN IMPORTED] {module.name}")

        for _, obj in inspect.getmembers(mod, inspect.isclass):

            # must be a real plugin class
            if hasattr(obj, "name") and obj.name:

                try:
                    instance = obj()
                    registry.register(instance)
                    print(f"[PLUGIN REGISTERED] {obj.name}")

                except Exception as e:
                    print(f"[PLUGIN ERROR] {obj} -> {e}")