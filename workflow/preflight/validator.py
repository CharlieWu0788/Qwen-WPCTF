def validate_target(target):
    if not target:
        raise ValueError("Target not found")


def validate_profile(profile):
    if not profile:
        raise ValueError("Profile not found")


def validate_scanners(scanners):
    if not scanners:
        raise ValueError("No scanners resolved")