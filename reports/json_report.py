from datetime import datetime, timezone, timedelta


def generate_report(ctx: dict):

    dt = datetime.now(
        timezone(
            timedelta(hours=8)
        )
    )


    metadata = ctx.get(
        "metadata",
        {}
    )


    return {

        "metadata": {

            "framework": "Local WPCTF",

            "version": metadata.get(
                "framework_version",
                "v1.1.2"
            ),

            "target": ctx.get(
                "target_url"
            ),

            "timestamp": dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        },


        "classification":
            ctx.get(
                "classification"
            ),


        "scan_results":
            ctx.get(
                "scan_results"
            ),


        "analysis":
            ctx.get(
                "analysis"
            ),


        "risk_profile":
            ctx.get(
                "risk_profile"
            ),


        "endpoints":
            ctx.get(
                "endpoints"
            ),


        "attack_graph":
            ctx.get(
                "attack_graph"
            ),


        # PentestAgent output
        "agent_results":
            metadata.get(
                "agent_results",
                {}
            )

    }