from core.plugins.registry import get_registry


def auto_select_plugins(profile: dict):
    registry = get_registry()

    selected = []

    # DVWA / WP / generic fallback
    profile_caps = set(profile.get("capability", []))
    profile_categories = set(profile.get("allowed_categories", []))

    for name, plugin in registry.all().items():

        # safety check
        if not hasattr(plugin, "capability"):
            continue

        plugin_caps = set(plugin.capability)

        # --------------------------------------------------
        # MATCH LOGIC
        # --------------------------------------------------

        # 1. category match
        category_match = (
            hasattr(plugin, "category") and
            plugin.category in profile_categories
        )

        # 2. capability overlap match
        capability_match = len(profile_caps & plugin_caps) > 0

        # 3. fallback: if profile is empty → include all
        if not profile_caps and not profile_categories:
            selected.append(name)
            continue

        if category_match or capability_match:
            selected.append(name)

    return selected
