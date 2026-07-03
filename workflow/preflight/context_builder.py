def build_target_context(
    target,
    profile
):

    return {

        "target": target,

        "profile": profile,

        "url": target["url"],

        "environment": None

    }