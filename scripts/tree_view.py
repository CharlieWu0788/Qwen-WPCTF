import os

# -----------------------------------------------------
# EXACT MATCH IGNORE
# -----------------------------------------------------

IGNORE_FILES = {
    ".DS_Store",
}

IGNORE_EXTENSIONS = {
    ".pyc"
}

IGNORE_DIRS_CORE = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "thirdparty"
}

IGNORE_DIRS_FULL = {
    ".git",
    ".venv",
    "venv",
    "__pycache__"   # 🚨 FULL 模式也清理 cache
}


# -----------------------------------------------------
# CORE / FULL ENTRY
# -----------------------------------------------------

def tree_core(path="."):
    print("\n[CORE VIEW]\n")
    print(".")
    _tree(path, mode="core")


def tree_full(path="."):
    print("\n[FULL VIEW]\n")
    print(".")
    _tree(path, mode="full")


# -----------------------------------------------------
# FILTER LOGIC
# -----------------------------------------------------

def should_ignore_dir(name: str, mode: str) -> bool:
    if mode == "core":
        return name in IGNORE_DIRS_CORE
    return name in IGNORE_DIRS_FULL


def should_ignore_file(name: str) -> bool:
    if name in IGNORE_FILES:
        return True

    _, ext = os.path.splitext(name)
    return ext in IGNORE_EXTENSIONS


# -----------------------------------------------------
# TREE ENGINE
# -----------------------------------------------------

def _tree(dir_path, prefix="", mode="core"):
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return

    # 过滤
    filtered_items = []

    for item in items:
        path = os.path.join(dir_path, item)
        is_dir = os.path.isdir(path)

        if is_dir:
            if should_ignore_dir(item, mode):
                continue
        else:
            if should_ignore_file(item):
                continue

        filtered_items.append(item)

    for i, item in enumerate(filtered_items):
        path = os.path.join(dir_path, item)
        is_dir = os.path.isdir(path)

        connector = "└── " if i == len(filtered_items) - 1 else "├── "
        suffix = "/" if is_dir else ""

        print(prefix + connector + item + suffix)

        if is_dir:
            extension = "    " if i == len(filtered_items) - 1 else "│   "
            _tree(path, prefix + extension, mode)


# -----------------------------------------------------
# TEST
# -----------------------------------------------------

if __name__ == "__main__":
    tree_core(".")