import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def scan_sql_injection(url):
    """
    SQL Injection scanner (V1.0.1 schema-safe version)
    """

    PAYLOADS = [
        "'",
        '"',
        "' AND 1=1--",
        "' AND 1=2--",
        '" AND 1=1--',
        '" AND 1=2--',
    ]

    ERROR_MESSAGES = [
        "sql syntax",
        "mysql",
        "mariadb",
        "postgresql",
        "sqlite",
        "odbc",
        "oracle",
        "unclosed quotation mark",
        "database error",
        "syntax error",
        "warning: mysql",
        "pg_query",
    ]

    # --------------------------------------
    # V1 schema-stable result object
    # --------------------------------------
    result = {
        "sql_injection_detected": False,
        "evidence": [],
        "tested_payloads": PAYLOADS,
        "error": None
    }

    try:
        baseline = requests.get(url, timeout=5)
        baseline_status = baseline.status_code
        baseline_length = len(baseline.text)

    except requests.RequestException as e:
        result["error"] = str(e)
        return result

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        result["evidence"].append(
            "No URL parameters found for SQL injection testing"
        )
        return result

    detected = False
    evidence = []

    for param in params:
        original_value = params[param][0]

        for payload in PAYLOADS:

            test_params = params.copy()
            test_params[param] = [original_value + payload]

            test_query = urlencode(test_params, doseq=True)

            test_url = urlunparse(
                (
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    test_query,
                    parsed.fragment,
                )
            )

            try:
                response = requests.get(test_url, timeout=5)
                response_text = response.text.lower()

                # --------------------------------------
                # Error pattern detection
                # --------------------------------------
                for error in ERROR_MESSAGES:
                    if error in response_text:
                        detected = True
                        evidence.append(
                            f"SQL error pattern detected on '{param}' using payload '{payload}'"
                        )
                        break

                # --------------------------------------
                # Server error signal
                # --------------------------------------
                if response.status_code >= 500:
                    detected = True
                    evidence.append(
                        f"HTTP {response.status_code} on '{param}' using payload '{payload}'"
                    )

                # --------------------------------------
                # Response diff analysis
                # --------------------------------------
                length_diff = abs(len(response.text) - baseline_length)

                if baseline_length > 0:
                    diff_percent = (length_diff / baseline_length) * 100

                    if diff_percent > 30:
                        evidence.append(
                            f"Response anomaly ({diff_percent:.1f}%) on '{param}' using payload '{payload}'"
                        )

                # --------------------------------------
                # Status change detection
                # --------------------------------------
                if response.status_code != baseline_status:
                    evidence.append(
                        f"Status code shift {baseline_status} -> {response.status_code} on '{param}'"
                    )

            except requests.RequestException:
                # V1 rule: do NOT treat exception as evidence
                continue

    # --------------------------------------
    # Final schema assignment
    # --------------------------------------
    result["sql_injection_detected"] = detected
    result["evidence"] = list(set(evidence))

    return result