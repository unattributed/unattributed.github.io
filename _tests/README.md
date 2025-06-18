---
---

````markdown
# Jekyll Theme Test Suite

This directory contains Pytest-based unit tests for validating automation scripts in the `unattributed-theme` Jekyll project. These tests ensure high reliability and correctness across all content management tools.

---

## 📁 Test Index

### 1. `test_validate_and_fix_posts.py`

Tests functionality of `_scripts/validate_and_fix_posts.py`.

**What it covers:**
- YAML front matter normalization and order
- Filename derivation and sanitization
- Date extraction and Markdown output format
- Safe parsing and round-trip validation of post metadata

---

### 2. `test_manage_archives.py`

Validates behavior of `_scripts/manage_archives.py`.

**What it covers:**
- Category normalization (`c++ → cpp`, etc.)
- Permalink generation for category archives
- Archive page file naming logic

---

### 3. `test_jekyll_utilities.py`

Unit tests for utility functions in `jekyll_utilities.py`.

**What it covers:**
- Filename and permalink sanitization
- JSON-safe file writing with change detection
- CLI parser flag logic (dry-run, quiet, verbose)

---

## 🧪 Shared Fixtures

### `conftest.py`

Provides reusable Pytest fixtures for creating temporary directories and sample Markdown files.

**Fixtures included:**
- `temp_post_dir`: Simulates `_posts/` structure
- `sample_post_file`: Populates a default post file
- `temp_archive_dir`: Simulates `_category_pages/` structure

These fixtures ensure test isolation and avoid modifying actual site content during test runs.

---

## ✅ How to Run Tests

Activate your virtual environment and run:

```bash
pytest -v _tests/
````

You can run specific files or functions as needed:

```bash
pytest _tests/test_manage_archives.py
pytest -k test_normalize_category_name
```

---

## 🧠 Best Practice

Run tests locally before pushing to GitHub to catch regressions early. The test suite is lightweight and runs quickly in CI pipelines.

---

## 🗃️ Directory Structure

```
_tests/
├── conftest.py
├── test_jekyll_utilities.py
├── test_manage_archives.py
├── test_validate_and_fix_posts.py
└── README.md
```

---

## 🧑‍💻 Contributing

When updating scripts, always include new tests or update existing ones to reflect any change in behavior. Follow existing patterns for fixtures, assertions, and dry-run validation.

