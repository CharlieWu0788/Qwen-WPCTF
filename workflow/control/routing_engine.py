def generate_attack_plan(intelligence):

    plan = {
        "sql": [],
        "xss": [],
        "auth": [],
        "upload": [],
        "bruteforce": [],
        "agent_tasks": []
    }


    target_url = intelligence.get(
        "target_url"
    )


    # -----------------------------
    # Build normal attack paths
    # -----------------------------
    for u in intelligence.get(
        "urls",
        []
    ) + intelligence.get(
        "endpoints",
        []
    ):

        plan["sql"].append(u)

        plan["xss"].append(u)


        if "login" in u.lower():

            plan["auth"].append(u)


        if "upload" in u.lower():

            plan["upload"].append(u)



    # -----------------------------
    # Generate PentestAgent tasks
    # -----------------------------
    for finding in intelligence.get(
        "findings",
        []
    ):

        plan["agent_tasks"].append(
            {
                "mode": "FULL_PENTEST",
                "target": target_url,
                "reason": finding
            }
        )



    # -----------------------------
    # Fallback high risk modules
    # -----------------------------
    if not plan["agent_tasks"]:

        for module in intelligence.get(
            "high_risk_modules",
            []
        ):

            plan["agent_tasks"].append(
                {
                    "mode": "FULL_PENTEST",
                    "target": target_url,
                    "reason": {
                        "module": module,
                        "reason": "high risk module"
                    }
                }
            )


    return plan