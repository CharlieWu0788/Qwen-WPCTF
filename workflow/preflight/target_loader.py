import json
from config.targets import resolve_target


def load_target(config_path="config/config.json"):

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    target_key = config.get("target")

    target = resolve_target(target_key)

    target["id"] = target_key

    return target