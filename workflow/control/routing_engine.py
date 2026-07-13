def generate_attack_plan(intelligence):

    plan = {
        "sql": [],
        "xss": [],
        "auth": [],
        "upload": [],
        "bruteforce": [],
        "agent_tasks": []
    }

    for u in intelligence["urls"] + intelligence["endpoints"]:

        plan["sql"].append(u)
        plan["xss"].append(u)

        if "login" in u:
            plan["auth"].append(u)

        if "upload" in u:
            plan["upload"].append(u)

    for m in intelligence["high_risk_modules"]:
        plan["agent_tasks"].append({
            "mode": "FULL_PENTEST",
            "target": m
        })

    return plan