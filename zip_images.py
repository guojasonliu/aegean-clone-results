#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from collections import Counter
from pathlib import Path


IMAGE_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def find_images(results_root: Path, graphs_dir: Path) -> list[Path]:
    images = []
    for path in sorted(results_root.rglob("*")):
        if is_relative_to(path, graphs_dir):
            continue
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(path)
    return images


def destination_name(
    path: Path, results_root: Path, graphs_dir: Path, duplicate_names: set[str]
) -> Path:
    if path.name not in duplicate_names:
        return graphs_dir / path.name

    relative = path.relative_to(results_root)
    return graphs_dir / "__".join(relative.parts)


def copy_images(results_root: Path, output_dir: Path) -> int:
    graphs_dir = output_dir / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)

    images = find_images(results_root, graphs_dir)
    name_counts = Counter(path.name for path in images)
    duplicate_names = {name for name, count in name_counts.items() if count > 1}

    for path in images:
        destination = destination_name(path, results_root, graphs_dir, duplicate_names)
        shutil.copy2(path, destination)

    return len(images)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy all images under results/ into OUTPUT/graphs/."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("."),
        help="Directory where graphs/ will be created. Defaults to the current directory.",
    )
    args = parser.parse_args()

    results_root = Path(__file__).resolve().parent
    output_dir = args.output.resolve()
    copied = copy_images(results_root, output_dir)

    print(f"Copied {copied} image(s) to {output_dir / 'graphs'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
