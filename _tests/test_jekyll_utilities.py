# _tests/test_jekyll_utilities.py

import pytest
import os
import jekyll_utilities

def test_sanitize_filename():
    assert jekyll_utilities.sanitize_filename("2023-01-01-sample.md") == "2023-01-01-sample-md"
    assert jekyll_utilities.sanitize_filename("My Title!.md") == "my-title-md"
    assert jekyll_utilities.sanitize_filename("C++ is fun.md") == "c-is-fun-md"

def test_normalize_category_name():
    assert jekyll_utilities.normalize_category_name("C++") == "cpp"
    assert jekyll_utilities.normalize_category_name("c#") == "csharp"
    assert jekyll_utilities.normalize_category_name("DevOps") == "devops"

def test_build_category_permalink():
    assert jekyll_utilities.build_category_permalink("DevOps") == "/devops-archive.html"

def test_write_file_if_changed_dry_run_and_json(tmp_path):
    test_file = tmp_path / "test.json"
    content = '{"key": "value"}'

    # First write (should happen)
    changed, message = jekyll_utilities.write_file_if_changed(str(test_file), content, dry_run=True, quiet=False)
    assert changed
    assert "would write" in message

    # Second write (no change)
    test_file.write_text(content)
    changed, message = jekyll_utilities.write_file_if_changed(str(test_file), content, dry_run=True, quiet=True)
    assert not changed

def test_get_standard_parser_flags_and_defaults():
    parser = jekyll_utilities.get_standard_parser()
    args = parser.parse_args([])
    assert not args.dry_run
    assert not args.quiet
    assert not args.verbose
