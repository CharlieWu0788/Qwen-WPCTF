from config.target_profiles import TARGET_PROFILES


def load_profile(profile_name):
    if profile_name not in TARGET_PROFILES:
        raise ValueError(f"Unknown profile: {profile_name}")

    return TARGET_PROFILES[profile_name]