from typing import Dict, Any


class AppClassifier:
    """
    Structured Application Classifier (V2.1)

    Purpose:
    - Classify target application type
    - Fuse evidence from multiple scanners
    - Return confidence and classification metadata

    Notes:
    - This classifier does NOT decide attack strategy.
    - Attack planning belongs to the workflow layer.
    """

    def classify(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:

        wordpress_result = self._result(scan_results, "wordpress")
        auth_result = self._result(scan_results, "auth")
        api_result = self._result(scan_results, "api")
        header_result = self._result(scan_results, "header")

        score = 0.0
        evidence = []
        tags = []

        # -------------------------------------------------
        # WordPress Scanner
        # -------------------------------------------------

        if wordpress_result.get("wordpress_detected", False):
            score += 0.60
            evidence.append("wordpress_signature")
            tags.append("wordpress")

        # -------------------------------------------------
        # Authentication Scanner
        # -------------------------------------------------

        login_urls = auth_result.get("login_urls", [])

        for url in login_urls:
            lower_url = str(url).lower()

            if "wp-login.php" in lower_url:
                score += 0.25
                evidence.append("wp_login_detected")
                tags.append("wordpress")
                break

        # -------------------------------------------------
        # Link Evidence
        # -------------------------------------------------

        discovered_links = auth_result.get("discovered_links", [])

        for item in discovered_links:

            if isinstance(item, dict):
                text = str(item.get("text", "")).lower()
                url = str(item.get("url", "")).lower()
            else:
                text = str(item).lower()
                url = ""

            if "wordpress" in text or "wordpress.org" in url:
                score += 0.15
                evidence.append("wordpress_reference")
                tags.append("wordpress")
                break

        # -------------------------------------------------
        # REST API Fingerprint (Future)
        # -------------------------------------------------

        if api_result.get("wordpress_api_detected", False):
            score += 0.20
            evidence.append("wp_rest_api")
            tags.append("wordpress")

        # -------------------------------------------------
        # HTTP Header Fingerprint (Future)
        # -------------------------------------------------

        if header_result.get("wordpress_header_detected", False):
            score += 0.15
            evidence.append("wp_header")
            tags.append("wordpress")

        # -------------------------------------------------
        # Training Platform Detection
        # -------------------------------------------------

        training_keywords = [
            "dvwa",
            "juice",
            "juice shop",
            "webgoat",
            "mutillidae",
        ]

        login_text = " ".join(str(x).lower() for x in login_urls)

        for keyword in training_keywords:

            if keyword in login_text:
                score += 0.40
                evidence.append(f"{keyword}_detected")
                tags.append("training_platform")

        # -------------------------------------------------
        # Decision
        # -------------------------------------------------

        score = min(score, 1.0)

        if "wordpress" in tags and score >= 0.40:
            app_type = "wordpress"

        elif "training_platform" in tags:
            app_type = "training_platform"

        else:
            app_type = "generic_web"

        return {
            "app_type": app_type,
            "confidence": round(score, 2),
            "evidence": sorted(set(evidence)),
            "tags": sorted(set(tags)),
            "attack_suggestions": []
        }

    def _result(self, scan_results: Dict[str, Any], name: str) -> Dict[str, Any]:
        result = scan_results.get(name) or scan_results.get(f"{name}_scan") or {}
        return result if isinstance(result, dict) else {}


def classify_application(scan_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience wrapper.
    """
    return AppClassifier().classify(scan_results)
