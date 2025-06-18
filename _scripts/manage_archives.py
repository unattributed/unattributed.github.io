# _scripts/manage_archives.py

"""
Regenerates _category_pages/*.md files based on categories found in _posts/*.md.

This script ensures that each category used in post front matter has a corresponding
archive page, formatted correctly for Jekyll and GitHub Pages compatibility. It creates
or updates category archive markdown files with consistent permalink structure and
front matter values.

It also provides options to dry-run, clean up obsolete files, or preview what pages
would be created, supporting safe use during development or automation.

Key features:
- Scans all post files for unique categories (normalized to lowercase)
- Generates matching _category_pages/<category>-archive.md files
- Validates and updates only when changes are detected
- Supports backup and cleanup of outdated category files

CLI flags:
    -n / --dry-run    : Simulate file creation and deletion without writing
    -q / --quiet      : Suppress all non-critical output
    -v / --verbose    : Print detailed progress and summary info
    -f / --fix        : Remove category pages no longer referenced by posts
    -l / --list-new   : Show which category pages would be created (no writes)

Designed to integrate with other content validation tools in the unattributed-theme project.
"""

import os
import sys
import shutil
from jekyll_utilities import (
    get_standard_parser,
    parse_sanitized_yaml,
    normalize_category_name,
    build_category_permalink,
    write_file_if_changed,
    ensure_directory,
)

CATEGORY_DIR = "_category_pages"
POSTS_DIR = "_posts"
BACKUP_DIR = "_tmpbkup/_category_pages"

def extract_all_categories(post_dir):
    categories = set()
    for fname in os.listdir(post_dir):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(post_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            metadata, _ = parse_sanitized_yaml(raw)
            cats = metadata.get("categories", [])
            if isinstance(cats, str):
                cats = [cats]
            categories.update(cats)
        except Exception as e:
            print(f"[warn] Skipping {fname}: {e}", file=sys.stderr)
    return sorted(categories)

def generate_category_filename(category):
    normalized = normalize_category_name(category)
    return f"{normalized}-archive.md"

def expected_front_matter(category):
    normalized = normalize_category_name(category)
    return {
        "layout": "archive",
        "title": f"{category} archive",
        "permalink": f"/{normalized}-archive.html",
        "category": normalized,
    }

def build_content(front_matter):
    lines = ["---"]
    for key in ["layout", "title", "permalink", "category"]:
        value = front_matter[key]
        if isinstance(value, str):
            value = f'"{value}"' if " " in value or value != value.lower() else value
        lines.append(f"{key}: {value}")
    lines.append("---\n")
    return "\n".join(lines)

def backup_file_if_exists(filepath):
    if os.path.exists(filepath):
        ensure_directory(BACKUP_DIR)
        shutil.copy2(filepath, os.path.join(BACKUP_DIR, os.path.basename(filepath)))

def main():
    parser = get_standard_parser("Regenerate _category_pages/*.md from categories in _posts")
    args = parser.parse_args()

    found_categories = extract_all_categories(POSTS_DIR)
    if args.verbose:
        print(f"[info] Found {len(found_categories)} unique categories.")

    generated_files = set()
    for category in found_categories:
        expected = expected_front_matter(category)
        filename = generate_category_filename(category)
        path = os.path.join(CATEGORY_DIR, filename)
        content = build_content(expected)

        if args.list_new:
            if not os.path.exists(path):
                print(f"[new] {filename}")
            continue

        backup_file_if_exists(path)
        write_file_if_changed(path, content, dry_run=args.dry_run, quiet=args.quiet)
        generated_files.add(filename)

    if args.dry_run and not args.quiet:
        print("[dry-run] archive pages updated")
    elif not args.dry_run and args.verbose:
        print("[info] archive pages updated")

    if args.fix:
        for filename in os.listdir(CATEGORY_DIR):
            if filename.endswith(".md") and filename not in generated_files:
                full_path = os.path.join(CATEGORY_DIR, filename)
                if args.dry_run:
                    if not args.quiet:
                        print(f"[dry-run] would delete {full_path}")
                else:
                    backup_file_if_exists(full_path)
                    os.remove(full_path)
                    if not args.quiet:
                        print(f"[delete] {full_path}")

if __name__ == "__main__":
    main()
