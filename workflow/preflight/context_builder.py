from engines.pentestagent_engine import PentestAgentEngine


def build_target_context(
    target,
    profile
):

    return {

        "target": target,

        "profile": profile,

        "url": target["url"],

        "environment": None,

        # PentestAgent execution engine
        "pentest_agent": PentestAgentEngine()

    }