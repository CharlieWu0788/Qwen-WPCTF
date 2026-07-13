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
# Preflight Hook (future extension point)
# =========================================================
def preflight_hook(mode: str):
    """
    Reserved for future:
    - environment validation
    - dependency check
    - plugin sanity check
    """
    print(f"[WPCTF] Mode = {mode}")


# =========================================================
# Main Dispatcher ONLY
# =========================================================
def main():

    args = get_args()

    preflight_hook(args.mode)

    try:

        # -----------------------------------------------------
        # Tree Mode (Core View)
        # -----------------------------------------------------
        if args.mode == "tree-core":
            tree_core()
            return

        # -----------------------------------------------------
        # Tree Mode (Full View)
        # -----------------------------------------------------
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

    except KeyboardInterrupt:
        print("\n[WPCTF] Interrupted by user")
    except Exception as e:
        print(f"[WPCTF][FATAL ERROR] {e}")


# =========================================================
# Entry
# =========================================================
if __name__ == "__main__":
    main()