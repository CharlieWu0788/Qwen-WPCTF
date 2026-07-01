def analyze_risk(analysis_input):
    """
    Analyze risk distribution.
    """

    surface_list = analysis_input.get("surface_list", [])

    critical = 0
    high = 0
    medium = 0
    low = 0

    for surface in surface_list:

        score = surface.get("risk_score", 0)

        if score >= 0.85:
            critical += 1

        elif score >= 0.70:
            high += 1

        elif score >= 0.40:
            medium += 1

        else:
            low += 1

    total = len(surface_list)

    return {
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "total": total
    }