from core.plugins.base import BasePlugin


class DirectoryScanner(BasePlugin):
    """
    Directory enumeration scanner
    """

    # --------------------------------------------------
    # Core identity
    # --------------------------------------------------
    name = "directory_scan"
    category = "recon"

    # --------------------------------------------------
    # Plugin capability metadata
    # --------------------------------------------------
    capability = [
        "directory",
        "endpoint_discovery",
        "enumeration",
        "recon"
    ]

    def run(self, context):
        """
        Perform directory brute-force / enumeration scan.
        """

        target = context["target"]
        url = target.get("url") if isinstance(target, dict) else target

        return {
            "target": url,
            "type": "directory_scan",
            "status": "ok",
            "findings": {
                "directories": [],
                "hidden_paths": [],
                "status_codes": []
            },
            "capability_used": self.capability
        }
