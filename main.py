import os
import json
import argparse

from scripts.tree.tree_view import tree_core, tree_full
from workflow.pipeline import scan


# =========================================================
# Args
# =========================================================
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        default="scan",
        choices=["scan", "tree-core", "tree-full"]
    )

    return parser.parse_args()


# =========================================================
# Main Dispatcher ONLY
# =========================================================
def main():

    args = get_args()

    # -----------------------------------------------------
    # Tree Mode
    # -----------------------------------------------------
    if args.mode == "tree-core":
        tree_core()
        return

    if args.mode == "tree-full":
        tree_full(".")
        return

    # -----------------------------------------------------
    # Scan Mode (Pipeline Entry)
    # -----------------------------------------------------
    if args.mode == "scan":
        scan()
        return

    # -----------------------------------------------------
    # Safety fallback
    # -----------------------------------------------------
    print(f"[ERROR] Unknown mode: {args.mode}")


# =========================================================
# Entry
# =========================================================
if __name__ == "__main__":
    main()