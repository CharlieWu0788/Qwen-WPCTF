def dispatch_agents(plan, pentest_agent):

    results = {}

    for task in plan.get("agent_tasks", []):
        target = task.get("target")
        result_key = _result_key(target)

        try:
            if pentest_agent is None:
                results[result_key] = {
                    "error": "pentest_agent not configured",
                    "target": target
                }
                continue

            results[result_key] = pentest_agent.run(
                target=target,
                mode=task.get("mode", "FULL_PENTEST")
            )

        except Exception as e:
            results[result_key] = {
                "error": str(e),
                "target": target
            }

    return results


def _result_key(target):
    if isinstance(target, dict):
        return str(
            target.get("id")
            or target.get("name")
            or target.get("target")
            or target.get("url")
            or target
        )

    return str(target)
