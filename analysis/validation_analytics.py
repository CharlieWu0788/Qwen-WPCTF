def analyze_validation(analysis_input):
    """
    Analyze validation outcomes.
    """

    validation_results = analysis_input.get("test_tasks", [])

    validated = 0
    failed = 0
    untested = 0

    for result in validation_results:

        if not isinstance(result, dict):
            result = {"raw": result}

        evidence = result.get("evidence", [])

        if result.get("validated", False):
            validated += 1

        elif evidence and evidence[0] == "No executor available":
            untested += 1

        else:
            failed += 1

    total = validated + failed + untested

    score = 0

    if total:
        score = round(validated / total * 100, 2)

    return {
        "validated": validated,
        "failed": failed,
        "untested": untested,
        "validation_score": score
    }