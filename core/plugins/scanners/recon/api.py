from core.plugins.base import BasePlugin


class APIReconScanner(BasePlugin):
    """
    API surface reconnaissance scanner
    """

    # --------------------------------------------------
    # Core identity (IMPORTANT)
    # --------------------------------------------------
    name = "api_scan"
    category = "recon"

    # --------------------------------------------------
    # Plugin capability metadata
    # --------------------------------------------------
    capability = [
        "api",
        "endpoint_discovery",
        "surface_recon"
    ]

    def run(self, context):
        """
        Execute API reconnaissance scan.

        Args:
            context (dict): runtime context

        Returns:
            dict: scan result
        """
        target = context["target"]

        return {
            "target": target,
            "type": "api_recon",
            "status": "ok",
            "findings": [],
            "capability_used": self.capability
        }
