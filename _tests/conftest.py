# _tests/conftest.py
"""
Shared fixtures and helpers for pytest test files in the unattributed-theme project.
"""

import pytest
import tempfile
from pathlib import Path
from textwrap import dedent


@pytest.fixture
def temp_post_dir():
    """Create a temporary _posts/ directory for test files."""
    with tempfile.TemporaryDirectory() as tempdir:
        posts_dir = Path(tempdir) / "_posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        yield posts_dir


@pytest.fixture
def sample_post_file(temp_post_dir):
    """Return a path to a sample markdown post with default front matter."""
    file = temp_post_dir / "2025-01-01-sample.md"
    file.write_text(dedent("""\
        ---
        title: Test Post
        categories: ["Security"]
        tags: ["AWS"]
        ---
        Post content.
    """))
    return file


@pytest.fixture
def temp_archive_dir():
    """Create a temporary _category_pages/ directory for archive tests."""
    with tempfile.TemporaryDirectory() as tempdir:
        archive_dir = Path(tempdir) / "_category_pages"
        archive_dir.mkdir(parents=True, exist_ok=True)
        yield archive_dir
