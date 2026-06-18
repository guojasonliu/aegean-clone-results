#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


RESULTS_ROOT = Path(__file__).resolve().parent


def display_path(path: Path) -> str:
    return str(path.relative_to(RESULTS_ROOT))


def keep_only_node0(*, dry_run: bool) -> int:
    removed = 0

    for path in sorted(RESULTS_ROOT.rglob("node*.log")):
        if path.name == "node0.log":
            continue
        if not path.is_file():
            continue

        if dry_run:
            print(f"Would remove {display_path(path)}")
        else:
            path.unlink()
            print(f"Removed {display_path(path)}")
        removed += 1

    action = "Would remove" if dry_run else "Removed"
    print(f"{action} {removed} file(s) under {RESULTS_ROOT}")
    return removed


def preserve_for_all(path: Path) -> bool:
    name = path.name
    return (
        name == ".git"
        or name == "README.md"
        or name.endswith(".py")
        or name.endswith(".sh")
    )


def delete_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def clean_all(*, dry_run: bool) -> int:
    to_delete = [
        path
        for path in sorted(RESULTS_ROOT.iterdir())
        if not preserve_for_all(path)
    ]

    if not to_delete:
        print("Nothing to delete.")
        return 0

    heading = "The following would be removed:" if dry_run else "The following will be removed:"
    print(heading)
    for path in to_delete:
        print(f"  {display_path(path)}")

    if dry_run:
        print(f"Would delete {len(to_delete)} path(s).")
        return len(to_delete)

    answer = input("\nProceed? [yes/no] ")
    if answer not in {"yes", "y", "Y", "YES"}:
        print("Aborted.")
        return 0

    for path in to_delete:
        delete_path(path)
    print("Deleted.")
    return len(to_delete)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Clean generated result files. By default, remove node*.log files "
            "except node0.log; with --all, remove generated result directories "
            "and files while preserving scripts, README.md, and .git."
        )
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Remove generated results, matching the old clean.sh behavior.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths that would be removed without deleting them.",
    )
    args = parser.parse_args()

    if args.all:
        clean_all(dry_run=args.dry_run)
    else:
        keep_only_node0(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
