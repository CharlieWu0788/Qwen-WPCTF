from datetime import datetime, timezone, timedelta


def generate_report(ctx: dict):

    # =========================================================
    # Time (Asia/Shanghai / UTC+8)
    # =========================================================
    dt = datetime.now(timezone(timedelta(hours=8)))

    # =========================================================
    # Report Structure
    # =========================================================
    return {
        "metadata": {
            "framework": "Local WPCTF",
            "version": ctx.get("metadata", {}).get("framework_version", "v1.1.2"),
            "target": ctx.get("target_url"),
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S")
        },

        # =========================================================
        # Core classification
        # =========================================================
        "classification": ctx.get("classification"),

        # =========================================================
        # Raw scan results
        # =========================================================
        "scan_results": ctx.get("scan_results"),

        # =========================================================
        # Rule-based + LLM analysis layer
        # =========================================================
        "analysis": ctx.get("analysis"),


        # =========================================================
        # Risk / posture layer
        # =========================================================
        "risk_profile": ctx.get("risk_profile"),

        # =========================================================
        # Attack surface / endpoints
        # =========================================================
        "endpoints": ctx.get("endpoints"),

        # =========================================================
        # Graph (if present)
        # =========================================================
        "attack_graph": ctx.get("attack_graph"),
    }