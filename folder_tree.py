#!/usr/bin/env python3
"""
Folder Tree Generator
Creates a visual representation of folder structure
"""

import sys
from pathlib import Path


def generate_tree(directory, prefix="", max_depth=None, current_depth=0):
    """Generate tree structure for a directory"""
    if max_depth is not None and current_depth >= max_depth:
        return

    try:
        path = Path(directory)
        if not path.exists():
            print(f"Error: Directory '{directory}' does not exist")
            return

        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")

            if item.is_dir() and not item.name.startswith("."):
                extension = "    " if is_last else "│   "
                generate_tree(item, prefix + extension, max_depth, current_depth + 1)

    except PermissionError:
        print(f"{prefix}└── [Permission Denied]")
    except Exception as e:
        print(f"{prefix}└── [Error: {e}]")


def main():
    if len(sys.argv) < 2:
        print("Usage: python folder_tree.py <directory_path> [max_depth]")
        print("Example: python folder_tree.py C:\\Users 3")
        return

    directory = sys.argv[1]
    max_depth = None

    if len(sys.argv) > 2:
        try:
            max_depth = int(sys.argv[2])
        except ValueError:
            print("Error: max_depth must be a number")
            return

    print(f"Folder tree for: {directory}")
    print("=" * 50)
    generate_tree(directory, max_depth=max_depth)


if __name__ == "__main__":
    main()
