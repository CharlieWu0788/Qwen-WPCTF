import importlib
import pkgutil
import core.plugins.scanners as scanners_pkg


def load_all_plugins():
    """
    FULL RECURSIVE MODULE IMPORT (REAL FIX)
    """

    def import_submodules(package):
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):

            full_name = f"{package.__name__}.{name}"

            module = importlib.import_module(full_name)
            print(f"[PLUGIN LOADED] {full_name}")

            # 🔥 CRITICAL: recursively go deeper
            if hasattr(module, "__path__"):
                import_submodules(module)

    import_submodules(scanners_pkg)