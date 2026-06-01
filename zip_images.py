#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
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


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def is_generated_graph(path: Path, results_root: Path, graphs_dir: Path) -> bool:
    if is_relative_to(path, graphs_dir):
        return True

    relative_parts = path.relative_to(results_root).parts
    return "graphs" in relative_parts[:-1]


def find_images(results_root: Path, graphs_dir: Path) -> tuple[list[Path], int]:
    images = []
    skipped = 0
    for path in sorted(results_root.rglob("*")):
        if not is_image(path):
            continue
        if is_generated_graph(path, results_root, graphs_dir):
            skipped += 1
            continue
        images.append(path)
    return images, skipped


def clean_graphs_dir(graphs_dir: Path) -> int:
    if not graphs_dir.exists():
        return 0

    removed = 0
    for path in graphs_dir.iterdir():
        if is_image(path):
            path.unlink()
            removed += 1
    return removed


def destination_name(path: Path, graphs_dir: Path, used_names: set[str]) -> Path:
    candidate = path.name
    stem = path.stem
    suffix = path.suffix
    index = 2

    while candidate in used_names:
        candidate = f"{stem}_{index}{suffix}"
        index += 1

    used_names.add(candidate)
    return graphs_dir / candidate


def copy_images(results_root: Path, output_dir: Path) -> tuple[int, int, int]:
    graphs_dir = output_dir / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)
    removed = clean_graphs_dir(graphs_dir)

    images, skipped = find_images(results_root, graphs_dir)
    used_names = {path.name for path in graphs_dir.iterdir()}

    for path in images:
        destination = destination_name(path, graphs_dir, used_names)
        shutil.copy2(path, destination)

    return len(images), skipped, removed


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
    copied, skipped, removed = copy_images(results_root, output_dir)

    print(
        f"Copied {copied} image(s) to {output_dir / 'graphs'} "
        f"(skipped {skipped} generated graph image(s), removed {removed} old image(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
