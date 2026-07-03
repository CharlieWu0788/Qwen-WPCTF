import requests
from bs4 import BeautifulSoup


def scan_wordpress(url):
    """
    WordPress detection scanner (V1.0.1 schema-safe version)

    Returns:
        dict: stable schema object with no structural variation
    """

    # --------------------------------------
    # Default schema (V1 requirement: stable keys)
    # --------------------------------------
    result = {
        "wordpress_detected": False,
        "evidence": [],
        "error": None
    }

    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True
        )
    except requests.RequestException as e:
        result["error"] = str(e)
        return result

    # --------------------------------------
    # HTTP validation (schema-stable failure path)
    # --------------------------------------
    if response.status_code < 200 or response.status_code >= 300:
        result["error"] = f"HTTP {response.status_code}"
        return result

    soup = BeautifulSoup(response.text, 'html.parser')
    evidence_list = []

    content_lower = response.text.lower()

    # --------------------------------------
    # Evidence detection (pure feature extraction)
    # --------------------------------------
    if "wp-content" in content_lower:
        evidence_list.append("wp-content found")

    if "wp-includes" in content_lower:
        evidence_list.append("wp-includes found")

    generator = soup.find("meta", attrs={"name": "generator"})

    if generator is not None:
        content = generator.get("content", "")
        if isinstance(content, str) and "wordpress" in content.lower():
            evidence_list.append("generator tag found")

    # --------------------------------------
    # Decision logic (pure deterministic rule)
    # --------------------------------------
    result["wordpress_detected"] = any(
        ev in [
            "wp-content found",
            "wp-includes found",
            "generator tag found"
        ]
        for ev in evidence_list
    )

    result["evidence"] = evidence_list

    return result