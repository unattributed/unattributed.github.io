# _scripts/validate_and_fix_posts.py

"""
Validates and normalizes YAML front matter in _posts/*.md files to ensure
consistent structure and formatting for Jekyll and GitHub Pages.

Features:
- Backups to _tmpbkup/_posts/
- Normalizes YAML key order and format
- Renames files to YYYY-MM-DD-title.md format
- Falls back to file timestamp if front matter date missing
"""

import os
import shutil
import sys
import re
from pathlib import Path
from datetime import datetime
from jekyll_utilities import (
    get_standard_parser,
    load_markdown_files_safe,
    write_markdown_file,
    ensure_directory,
)

POSTS_DIR = "_posts"
BACKUP_DIR = "_tmpbkup/_posts"
REQUIRED_KEYS = ["layout", "title", "date", "author", "categories", "tags"]

def normalize_front_matter(post):
    meta = post.metadata
    fixed = {}

    for key in REQUIRED_KEYS:
        value = meta.get(key)

        if key == "title" and isinstance(value, str):
            fixed[key] = value.strip()

        elif key in ["categories", "tags"]:
            if isinstance(value, str):
                value = [value]
            elif not isinstance(value, list):
                value = []
            fixed[key] = [v.lower() for v in value]

        elif value is not None:
            fixed[key] = str(value).strip()
        else:
            fixed[key] = "" if key not in ["categories", "tags"] else []

    post.metadata = fixed
    return post

def get_date_from_metadata_or_mtime(post, path):
    try:
        return datetime.strptime(post.metadata.get("date", ""), "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        stat = os.stat(path)
        return datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")

def strip_existing_date_prefix(filename):
    # Remove any date-like prefix: e.g. 2024-09-01-title.md or 20240601-title.md
    return re.sub(r"^\d{4}[-]?\d{2}[-]?\d{2}-", "", filename)

def backup_all_files(src_dir, dst_dir, verbose=False):
    ensure_directory(dst_dir)
    for fname in os.listdir(src_dir):
        if fname.endswith(".md"):
            src = os.path.join(src_dir, fname)
            dst = os.path.join(dst_dir, fname)
            shutil.copy2(src, dst)
            if verbose:
                print(f"[info] Backed up {fname} to {dst_dir}")

def validate_and_fix_posts(dry_run=False, quiet=False, verbose=False):
    if not os.path.exists(POSTS_DIR):
        print(f"[error] Missing {POSTS_DIR}/ directory", file=sys.stderr)
        sys.exit(1)

    backup_all_files(POSTS_DIR, BACKUP_DIR, verbose=verbose)

    for path, post in load_markdown_files_safe(POSTS_DIR):
        original_path = path
        original_name = os.path.basename(path)

        post = normalize_front_matter(post)
        post_date = get_date_from_metadata_or_mtime(post, path)

        clean_name = strip_existing_date_prefix(original_name)
        new_name = f"{post_date}-{clean_name}"
        new_path = os.path.join(POSTS_DIR, new_name)

        if original_name != new_name:
            if dry_run:
                print(f"[dry-run] would rename: {original_name} -> {new_name}")
            else:
                os.rename(original_path, new_path)
                path = new_path
                if not quiet:
                    print(f"[rename] {original_name} -> {new_name}")

        if dry_run:
            if not quiet:
                print(f"[✓] Would fix: {os.path.basename(path)}")
        else:
            write_markdown_file(path, post)
            if verbose:
                print(f"[✓] Fixed: {os.path.basename(path)}")

def main():
    parser = get_standard_parser("Validate and normalize front matter in _posts/*.md")
    args = parser.parse_args()
    validate_and_fix_posts(
        dry_run=args.dry_run,
        quiet=args.quiet,
        verbose=args.verbose,
    )
    
def derive_new_filename(post, original_path):
    post_date = get_date_from_metadata_or_mtime(post, original_path)
    clean_name = strip_existing_date_prefix(os.path.basename(original_path))
    return f"{post_date}-{clean_name}"

if __name__ == "__main__":
    main()
