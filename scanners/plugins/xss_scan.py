import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scan_xss(url):
    """
    XSS scanner (V1.0.1 schema-safe version)
    """

    PAYLOADS = [
        "<script>alert(1)</script>",
        "\"><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>"
    ]

    # --------------------------------------
    # V1 schema-stable result
    # --------------------------------------
    result = {
        "xss_detected": False,
        "evidence": [],
        "tested_payloads": PAYLOADS,
        "error": None
    }

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as e:
        result["error"] = str(e)
        return result

    forms = soup.find_all("form")

    if not forms:
        result["evidence"].append("No forms discovered")
        return result

    result["evidence"].append(f"Discovered {len(forms)} form(s)")

    detected = False
    evidence = []

    for form in forms:

        action = form.get("action")
        method = form.get("method", "get").lower()

        target_url = urljoin(url, action) if action else url

        evidence.append(
            f"Testing form at {target_url} using {method.upper()}"
        )

        inputs = form.find_all(["input", "textarea"])

        for payload in PAYLOADS:

            form_data = {}

            for field in inputs:

                name = field.get("name")

                if not name:
                    continue

                field_type = field.get("type", "text").lower()

                if field_type in ["text", "search", "email", "url", "hidden", "textarea"]:
                    form_data[name] = payload
                else:
                    form_data[name] = "test"

            try:
                if method == "post":
                    test_response = requests.post(
                        target_url,
                        data=form_data,
                        timeout=5
                    )
                else:
                    test_response = requests.get(
                        target_url,
                        params=form_data,
                        timeout=5
                    )

                response_text = test_response.text

                # --------------------------------------
                # Reflection detection
                # --------------------------------------
                if payload in response_text:
                    detected = True
                    evidence.append(
                        f"Unescaped payload reflected at {target_url}"
                    )

                elif "alert(1)" in response_text:
                    evidence.append(
                        f"Encoded payload reflected at {target_url}"
                    )

            except requests.RequestException:
                # V1 rule: do not treat request failure as evidence
                continue

    # --------------------------------------
    # Final schema assignment
    # --------------------------------------
    result["xss_detected"] = detected
    result["evidence"] = list(set(evidence))

    return result