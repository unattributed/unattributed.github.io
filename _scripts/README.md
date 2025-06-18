---

### `_scripts/README.md`

````markdown
# Jekyll Theme Content Automation

This directory contains automation scripts that help maintain consistency and prevent content errors in the `unattributed-theme` Jekyll blog. These tools are designed to simplify common tasks for both beginners and experts, especially when deploying on GitHub Pages where strict formatting matters.

---

## 📁 Script Index

### 1. `validate_and_fix_posts.py`
Ensures that all Markdown posts in `_posts/` contain well-formed YAML front matter in a consistent structure.

**What it does:**
- Validates presence and order of keys: `layout`, `title`, `date`, `author`, `categories`, `tags`
- Ensures `categories` and `tags` are lowercase, alphanumeric, and stored as YAML arrays
- Corrects improperly formatted or inconsistent metadata

**Example usage:**
```bash
python3 _scripts/validate_and_fix_posts.py --dry-run --verbose
````

**Flags supported:**

* `-n`, `--dry-run`     : Simulate changes, do not write files
* `-v`, `--verbose`     : Detailed output
* `-q`, `--quiet`       : Suppress output unless error occurs

---

### 2. `manage_archives.py`

Generates and maintains category archive pages in `_category_pages/` to reflect the actual categories used in `_posts/`.

**What it does:**

* Reads all `categories` from `_posts/*.md`
* Normalizes and creates corresponding `_category_pages/<category>-archive.md` files
* Removes orphaned archive pages if `--fix` is used
* Backs up files before modifying or deleting
* Allows previewing which new archive pages would be created

**Example usage:**

```bash
python3 _scripts/manage_archives.py --fix --verbose
```

**To list pages that would be created but not write them:**

```bash
python3 _scripts/manage_archives.py --list-new
```

**Flags supported:**

* `-n`, `--dry-run`     : Simulate file writes/deletes
* `-f`, `--fix`         : Remove unused archive files
* `-l`, `--list-new`    : Show which files would be created
* `-v`, `--verbose`     : Print detailed progress
* `-q`, `--quiet`       : Suppress output unless error occurs

---

## 🛠 Utility Module

### `jekyll_utilities.py`

This module provides shared functionality used by both scripts.

**Includes:**

* CLI argument parser (`get_standard_parser`)
* YAML front matter parser and validator
* File write with change detection and JSON validation
* Category name normalization (`c++ → cpp`, `c# → csharp`)
* Permalink builder and directory safeguards

You don’t need to run this file directly. It powers the above tools and ensures consistent behavior across scripts.

---

## ✅ Usage Notes

* All scripts are **safe by default**, and support `--dry-run` mode.
* Designed to run on Linux, macOS, and GitHub-hosted runners.
* Make sure to activate your Python virtual environment if required:

  ```bash
  source .venv/bin/activate
  ```

---

## 🧠 Best Practice

Run these scripts before pushing changes to GitHub Pages. They help catch subtle formatting issues and ensure category archives are always in sync.

---

## 🗃️ Directory Structure Overview

```
_posts/
├── 2023-12-31-example.md
└── ...
_category_pages/
├── ai-archive.md
├── security-archive.md
└── ...
_scripts/
├── validate_and_fix_posts.py
├── manage_archives.py
├── jekyll_utilities.py
└── README.md
```

---

## 🧑‍💻 Contributing

When adding new scripts, always use the `get_standard_parser()` from `jekyll_utilities.py` and implement dry-run and verbose support. This ensures consistency across tooling in the theme.

---

