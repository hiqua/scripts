#!/usr/bin/env python3
"""
Merge the content of all files from the given folder recursively into a single .md file.
"""
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Merge all files recursively into a single file."
    )
    parser.add_argument(
        "folder", type=str, help="Path to the folder containing the files."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output markdown file (default: FOLDER_NAME.md).",
    )
    args = parser.parse_args()

    base = Path(args.folder)
    if args.output:
        out = Path(args.output)
    else:
        out = base.with_suffix(".md")

    with out.open("w", encoding="utf-8") as fout:
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            fout.write(f"\n\n# [File]: {p.relative_to(base)}\n\n")
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                text = "UNREADABLE"
            fout.write(text)


if __name__ == "__main__":
    main()
