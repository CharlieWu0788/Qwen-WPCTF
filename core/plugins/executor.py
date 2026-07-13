import importlib
import pkgutil

import core.plugins.scanners.platform as platform_pkg
import core.plugins.scanners.recon as recon_pkg
import core.plugins.scanners.vulnerability as vuln_pkg


def load_all_plugins():
    """
    Force import all plugins so they self-register
    """

    packages = [platform_pkg, recon_pkg, vuln_pkg]

    for pkg in packages:
        for _, name, _ in pkgutil.iter_modules(pkg.__path__):
            importlib.import_module(f"{pkg.__name__}.{name}")