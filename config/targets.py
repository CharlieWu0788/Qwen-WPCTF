# -----------------------------------------------------
# Target Registry
# -----------------------------------------------------

TARGETS = {

    1: {
        "id": "wordpress",
        "name": "WordPress",
        "url": "http://localhost:8081/",
        "profile": "wordpress"
    },

    2: {
        "id": "dvwa",
        "name": "DVWA",
        "url": "http://10.1.200.100/DVWA/",
        "profile": "dvwa"
    },

    3: {
        "id": "sqli-labs",
        "name": "SQLi-Labs",
        "url": "http://10.1.200.100/sqli-labs/",
        "profile": "sqli-labs"
    },

    4: {
        "id": "upload-labs",
        "name": "Upload-Labs",
        "url": "http://10.1.200.100/upload-labs/",
        "profile": "upload-labs"
    }
}

# -----------------------------------------------------
# Alias Index (multi-key resolution)
# -----------------------------------------------------

TARGET_ALIAS = {}

for k, v in TARGETS.items():

    # numeric key: "1", "2"...
    TARGET_ALIAS[str(k)] = v

    # string id: "wordpress", "dvwa"...
    TARGET_ALIAS[v["id"]] = v

    # uppercase convenience
    TARGET_ALIAS[v["id"].upper()] = v


# -----------------------------------------------------
# Resolver API
# -----------------------------------------------------

def resolve_target(target_key):
    """
    Resolve target by:
    - int index: 1,2,3,4
    - string id: "wordpress", "dvwa"
    - string numeric: "1"
    """

    # direct alias match
    if target_key in TARGET_ALIAS:
        return TARGET_ALIAS[target_key]

    # try int conversion fallback
    try:
        return TARGETS[int(target_key)]
    except Exception:
        pass

    raise ValueError(f"Unknown target: {target_key}")