# _scripts/jekyll_utilities.py

"""
Utility functions for managing Jekyll content in the unattributed-theme project.

This module provides reusable helpers for:
- Parsing sanitized YAML front matter from markdown files
- Normalizing category names to lowercase, filesystem-safe values
- Building category permalinks and filenames
- Writing files safely with change detection, dry-run support, and optional JSON validation
- Providing a standardized argument parser for consistency across scripts

Used by automation tools in _scripts/ to validate, fix, and manage site content
in line with GitHub Pages-compatible Jekyll requirements.

Supports common CLI flags:
    -n / --dry-run    : Simulate actions without modifying files
    -q / --quiet      : Suppress output except for errors
    -v / --verbose    : Print detailed processing information
    -f / --fix        : Remove stale or unused output files
    -l / --list-new   : Show which files would be created without writing them

This module should remain lightweight and dependency-free, suitable for GitHub-hosted workflows.
"""

import argparse
import hashlib
import os
import re
import sys
import yaml
import json
from datetime import datetime

def get_standard_parser(description="Process markdown files"):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-n", "--dry-run", action="store_true", help="Run without writing changes")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output except for errors")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed output")
    parser.add_argument("-f", "--fix", action="store_true", help="Remove outdated files")
    parser.add_argument("-s", "--search", type=str, help="Keyword to search for in post content")
    parser.add_argument("-l", "--list-new", action="store_true", help="List new categories that will be created")
    return parser

def parse_sanitized_yaml(raw: str):
    if raw.startswith("---"):
        _, fm, *rest = raw.split("---", 2)
        content = rest[0] if rest else ""
        metadata = yaml.safe_load(fm)
        return metadata or {}, content.strip()
    raise ValueError("Missing YAML front matter")

def sanitize_filename(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def extract_front_matter_date(metadata: dict, fallback: str = "") -> str:
    if "date" in metadata:
        return str(metadata["date"])[:10]
    match = re.search(r"\d{4}-\d{2}-\d{2}", fallback)
    return match.group(0) if match else "1970-01-01"

def write_markdown_file(path: str, post) -> None:
    lines = ["---"]
    for key in ["layout", "title", "date", "author", "categories", "tags"]:
        value = post.metadata.get(key)
        if isinstance(value, list):
            value = "[" + ", ".join(value) + "]"
        elif isinstance(value, str):
            value = f'"{value}"' if key == "title" else value
        else:
            value = str(value)
        lines.append(f"{key}: {value}")
    lines.append("---\n")
    lines.append(post.content or "")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def validate_json(content: str) -> bool:
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {str(e)}", file=sys.stderr)
        return False

def write_file_if_changed(path: str, content: str, dry_run=False, quiet=False, caller_handles_message=False):
    if path.endswith(".json"):
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for {path}: {str(e)}")

    old = ""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old = f.read()

    changed = content.strip() != old.strip()
    message = ""

    if changed:
        if dry_run:
            message = f"[dry-run] would write: {path}"
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            message = f"[write] {path}"

    if changed and not caller_handles_message and not quiet:
        print(message)

    return changed, message

def normalize_category_name(cat: str) -> str:
    cat = cat.lower()
    return {"c++": "cpp", "c#": "csharp"}.get(cat, sanitize_filename(cat))

def build_category_permalink(cat: str) -> str:
    return f"/{normalize_category_name(cat)}-archive.html"

def load_markdown_files_safe(directory):
    for filename in os.listdir(directory):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(directory, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            metadata, content = parse_sanitized_yaml(raw)
            if not metadata:
                continue
            post = type("Post", (), {})()
            post.metadata = metadata
            post.content = content
            yield path, post
        except Exception as e:
            print(f"[warn] Skipping {filename}: {e}", file=sys.stderr)
