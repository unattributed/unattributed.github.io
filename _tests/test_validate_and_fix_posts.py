# _tests/test_validate_and_fix_posts.py

import pytest
import _scripts.validate_and_fix_posts as validate_and_fix_posts
import _scripts.jekyll_utilities as jekyll_utilities
from textwrap import dedent
from pathlib import Path


@pytest.fixture
def sample_front_matter():
    return {
        "layout": "post",
        "title": "Hello World",
        "date": "2023-06-01",
        "author": "foo",
        "categories": ["C++"],
        "tags": ["CI"]
    }


def test_normalize_front_matter(sample_front_matter):
    post = type("Post", (), {})()
    post.metadata = sample_front_matter.copy()
    normalized_post = validate_and_fix_posts.normalize_front_matter(post)
    normalized = normalized_post.metadata

    assert normalized["categories"] == ["c++"] or normalized["categories"] == ["cpp"]
    assert normalized["tags"] == ["ci"]
    assert normalized["layout"] == "post"
    assert normalized["author"] == "foo"


def test_derive_new_filename(sample_front_matter):
    post = type("Post", (), {})()
    post.metadata = sample_front_matter.copy()
    original_path = Path("2023-06-01-hello-world.md")
    filename = validate_and_fix_posts.derive_new_filename(post, original_path)
    assert filename == "2023-06-01-hello-world.md"


def test_extract_front_matter_date():
    metadata = {
        "layout": "post",
        "title": "Sample Post",
        "date": "2023-10-12",
        "author": "foo",
        "categories": ["devops"],
        "tags": ["ci"]
    }
    result = jekyll_utilities.extract_front_matter_date(metadata)
    assert result == "2023-10-12"


def test_sanitize_filename():
    assert jekyll_utilities.sanitize_filename("C++ Notes") == "c-notes"
    assert jekyll_utilities.sanitize_filename("My File!") == "my-file"
    assert jekyll_utilities.sanitize_filename("Python_3.10") == "python-3-10"


def test_parse_sanitized_yaml_and_write_markdown_file(tmp_path):
    raw_md = dedent("""\
        ---
        layout: post
        title: Hello World
        date: 2024-04-01
        author: bar
        categories: [DevOps]
        tags: [CI]
        ---
        Content body goes here.
    """)
    input_file = tmp_path / "2024-04-01-hello-world.md"
    input_file.write_text(raw_md, encoding="utf-8")

    metadata, content = jekyll_utilities.parse_sanitized_yaml(input_file.read_text())
    assert metadata["title"] == "Hello World"
    assert metadata["author"] == "bar"

    output_file = tmp_path / "output.md"
    post = type("Post", (), {})()
    post.metadata = metadata
    post.content = content
    jekyll_utilities.write_markdown_file(str(output_file), post)

    assert output_file.exists()
    output_contents = output_file.read_text(encoding="utf-8")
    assert "title: \"Hello World\"" in output_contents
    assert "author: bar" in output_contents
