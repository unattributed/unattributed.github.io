#!/usr/bin/env python3
"""
Corrupt permalinks in _category_pages/*.md by removing .html suffix.

This is a test utility to verify that _scripts/fix_category_pages.py detects and fixes bad permalinks.
Backs up all original files to _tmpbkup/_category_pages/ before modifying.
"""

import shutil
from pathlib import Path
import random

CATEGORY_DIR = Path("_category_pages")
BACKUP_DIR = Path("_tmpbkup/_category_pages")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def corrupt_permalink_lines(text):
    lines = text.splitlines()
    modified_lines = []
    changed = False

    for line in lines:
        if line.strip().startswith("permalink:") and line.strip().endswith(".html"):
            if random.choice([True, False]):
                corrupted = line.strip().replace(".html", "")
                modified_lines.append(corrupted)
                changed = True
                continue
        modified_lines.append(line)

    return "\n".join(modified_lines) + "\n", changed

def shuffle_permalinks():
    modified = 0

    for file in CATEGORY_DIR.glob("*.md"):
        original_text = file.read_text(encoding="utf-8")
        new_text, changed = corrupt_permalink_lines(original_text)

        if changed:
            shutil.copy(file, BACKUP_DIR / file.name)
            file.write_text(new_text, encoding="utf-8")
            print(f"[shuffled] {file.name}")
            modified += 1

    print(f"[done] Modified {modified} files in _category_pages/ and backed up to {BACKUP_DIR}/")

if __name__ == "__main__":
    shuffle_permalinks()
