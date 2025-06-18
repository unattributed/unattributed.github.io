#!/usr/bin/env python3
"""
Randomly reorder front matter keys in _posts/*.md to simulate misformatted YAML.
Backs up original versions to _tmpbkup/_posts/ for safe rollback.
Useful for testing validate_and_fix_posts.py with --verbose mode.
"""

import random
from pathlib import Path

REQUIRED_KEYS = ["layout", "title", "date", "author", "categories", "tags"]
POSTS_DIR = Path("_posts")
BACKUP_DIR = Path("_tmpbkup/_posts")

def parse_front_matter(lines):
    if lines[0].strip() != "---":
        return None, None
    try:
        end = lines[1:].index("---\n") + 1
    except ValueError:
        return None, None
    return lines[1:end], lines[end+1:]

def is_valid_front_matter(lines):
    keys = [line.split(":")[0].strip() for line in lines if ": " in line]
    return all(k in keys for k in REQUIRED_KEYS)

def shuffle_front_matter_block(block):
    random.shuffle(block)
    return block

def backup_original(path):
    rel = path.relative_to(POSTS_DIR)
    backup_path = BACKUP_DIR / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def process_file(path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    front, body = parse_front_matter(lines)
    if not front or not is_valid_front_matter(front):
        return False

    backup_original(path)

    shuffled = shuffle_front_matter_block(front[:])
    new_content = ["---\n"] + shuffled + ["---\n"] + body
    path.write_text("".join(new_content), encoding="utf-8")
    return True

def main():
    print("[*] Shuffling YAML keys in _posts/*.md...")
    modified = 0
    for md in POSTS_DIR.glob("*.md"):
        if process_file(md):
            print(f"[shuffled] {md.name}")
            modified += 1
    print(f"[done] {modified} files shuffled and backed up to _tmpbkup/_posts/")

if __name__ == "__main__":
    main()
