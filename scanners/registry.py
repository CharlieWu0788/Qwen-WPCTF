from scanners.plugins.sql_scan import scan_sql_injection
from scanners.plugins.xss_scan import scan_xss
from scanners.plugins.wordpress_scan import scan_wordpress
from scanners.plugins.auth_scan import scan_auth

from core.schema.safe_wrap import safe_scanner_result


# =========================================================
# Scanner Registry
# =========================================================

SCANNER_REGISTRY = {

    "wordpress": {
        "name": "WordPress Scanner",
        "function": scan_wordpress
    },

    "sql": {
        "name": "SQL Injection Scanner",
        "function": scan_sql_injection
    },

    "xss": {
        "name": "Cross-Site Scripting Scanner",
        "function": scan_xss
    },

    "auth": {
        "name": "Authentication Scanner",
        "function": scan_auth
    }

}


# =========================================================
# Execute Scanners
# =========================================================

def execute_scanners(url: str, scanner_list: list) -> dict:

    results = {}

    total = len(scanner_list)
    completed = 0
    failed = 0

    print("\n==================================================")
    print("Scanner Registry")
    print("==================================================")
    print(f"\nTarget URL : {url}")
    print(f"Running {total} scanner(s)...\n")

    for index, scanner in enumerate(scanner_list, start=1):

        scanner_info = SCANNER_REGISTRY.get(scanner)

        if scanner_info is None:

            print(f"[{index}/{total}] {scanner}")
            print("    ✗ Unknown scanner\n")

            failed += 1
            continue

        scanner_name = scanner_info["name"]
        scanner_function = scanner_info["function"]

        print(f"[{index}/{total}] {scanner_name}")

        try:

            # ---------------------------------------------
            # Execute Scanner
            # ---------------------------------------------
            result = scanner_function(url)

            # ---------------------------------------------
            # Schema Enforcement
            # ---------------------------------------------
            result = safe_scanner_result(result)

            results[scanner] = result

            print("    ✓ Completed\n")

            completed += 1

        except Exception as e:

            print("    ✗ Failed")
            print(f"    {e}\n")

            failed += 1

    print("--------------------------------------------------")
    print(f"Completed : {completed}")
    print(f"Failed    : {failed}")
    print("==================================================\n")

    return results

def get_scanner(name):
    if name not in SCANNER_REGISTRY:
        raise ValueError(f"Unknown scanner: {name}")
    return name