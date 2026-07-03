# =========================================================
# Target Profiles
# =========================================================

TARGET_PROFILES = {

    "dvwa": {

        "name": "DVWA",

        "scanners": [
            "sql",
            "xss",
            "auth"
        ],

        "description": "General Web Security Training"

    },

    "sqli-labs": {

        "name": "SQLi-Labs",

        "scanners": [
            "sql"
        ],

        "description": "SQL Injection Practice"

    },

    "upload-labs": {

        "name": "Upload-Labs",

        "scanners": [
            "upload"
        ],

        "description": "File Upload Security"

    },

    "generic": {

        "name": "Generic",

        "scanners": [
            "sql",
            "xss",
            "upload",
            "auth"
        ],

        "description": "Generic Web Application"

    }

}