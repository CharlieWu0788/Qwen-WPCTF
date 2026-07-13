def build_intelligence(scan_results, llm_analysis=None):

    intelligence = {
        "urls": [],
        "endpoints": [],
        "inputs": [],
        "auth_points": [],
        "high_risk_modules": [],
        "raw": scan_results,
        "llm": llm_analysis or {}
    }

    for name, result in scan_results.items():

        if not isinstance(result, dict):
            continue

        for u in result.get("urls", []):
            if u not in intelligence["urls"]:
                intelligence["urls"].append(u)

        for e in result.get("endpoints", []):
            if e not in intelligence["endpoints"]:
                intelligence["endpoints"].append(e)

        for p in result.get("parameters", []):
            if p not in intelligence["inputs"]:
                intelligence["inputs"].append(p)

        if result.get("auth_detected"):
            intelligence["auth_points"].append(name)

        if result.get("risk_score", 0) > 0.7:
            intelligence["high_risk_modules"].append(name)

    return intelligence