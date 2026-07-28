def generate_attack_plan(intelligence):

    plan = {
        "sql": [],
        "xss": [],
        "auth": [],
        "upload": [],
        "bruteforce": [],
        "agent_tasks": []
    }


    # ---------------------------------
    # Target extraction
    # ---------------------------------

    target = (
        intelligence.get("target")
        or intelligence.get("url")
        or intelligence.get("raw", {})
        .get("metadata", {})
        .get("target")
    )


    # ---------------------------------
    # Surface based planning
    # ---------------------------------

    for u in (
        intelligence.get("urls", [])
        +
        intelligence.get("endpoints", [])
    ):


        plan["sql"].append(u)

        plan["xss"].append(u)



        if "login" in u.lower():

            plan["auth"].append(u)



        if "upload" in u.lower():

            plan["upload"].append(u)



    # ---------------------------------
    # Generate PentestAgent tasks
    # ---------------------------------

    generated_targets = set()


    for finding in intelligence.get(
        "findings",
        []
    ):


        if not target:

            continue



        task_key = (
            target,
            finding.get("scanner"),
            finding.get("type")
        )


        if task_key in generated_targets:

            continue


        generated_targets.add(task_key)



        plan["agent_tasks"].append(
            {

                "mode": "agent",

                # IMPORTANT
                # PentestAgent receives real target
                "target": target,


                # keep scanner information
                # for reasoning
                "module":
                    finding.get(
                        "scanner"
                    ),


                "reason": finding

            }
        )



    # ---------------------------------
    # Fallback high risk modules
    # ---------------------------------

    if not plan["agent_tasks"]:


        for module in intelligence.get(
            "high_risk_modules",
            []
        ):


            if not target:

                continue



            plan["agent_tasks"].append(
                {

                    "mode":"agent",

                    "target":target,

                    "module":module,

                    "reason":
                        "high risk module"

                }
            )


    return plan