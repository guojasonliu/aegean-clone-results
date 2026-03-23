#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def keep_only_node0(root: Path, dry_run: bool) -> int:
    removed = 0

    for path in root.rglob("node*.log"):
        if path.name == "node0.log":
            continue
        if not path.is_file():
            continue

        if dry_run:
            print(f"Would remove {path}")
        else:
            path.unlink()
            print(f"Removed {path}")
        removed += 1

    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove all node*.log files under a directory except node0.log."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be removed without deleting them.",
    )
    args = parser.parse_args()

    root = Path(".").resolve()
    removed = keep_only_node0(root, args.dry_run)

    action = "Would remove" if args.dry_run else "Removed"
    print(f"{action} {removed} file(s) under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
