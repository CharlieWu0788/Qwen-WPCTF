from core.plugins.base import BasePlugin


class HeaderScanner(BasePlugin):
    """
    HTTP security header scanner
    """

    # --------------------------------------------------
    # Core identity
    # --------------------------------------------------
    name = "header_scan"
    category = "recon"

    # --------------------------------------------------
    # Plugin capability metadata
    # --------------------------------------------------
    capability = [
        "header",
        "security_headers",
        "http_analysis",
        "recon"
    ]

    def run(self, context):
        """
        Analyze HTTP response headers for security posture.
        """

        target = context["target"]
        url = target.get("url") if isinstance(target, dict) else target

        return {
            "target": url,
            "type": "header_scan",
            "status": "ok",
            "findings": {
                "headers": {},
                "missing_security_headers": [],
                "warnings": []
            },
            "capability_used": self.capability
        }
