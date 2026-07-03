from workflow.preflight.target_loader import load_target
from workflow.preflight.profile_loader import load_profile

from workflow.preflight.validator import (
    validate_target,
    validate_profile,
)

from workflow.preflight.environment_check import check_environment
from workflow.preflight.context_builder import build_target_context


def prepare_target():

    target = load_target()

    validate_target(target)

    profile = load_profile(
        target["profile"]
    )

    validate_profile(profile)

    environment = check_environment(
        target["url"]
    )

    if not environment["reachable"]:
        raise RuntimeError(
            "Target is unreachable."
        )

    context = build_target_context(
        target,
        profile
    )

    context["environment"] = environment

    return context