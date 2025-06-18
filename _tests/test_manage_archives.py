# _tests/test_manage_archives.py

from _scripts import manage_archives

def test_normalize_category_name():
    assert manage_archives.normalize_category_name("C++") == "cpp"
    assert manage_archives.normalize_category_name("C#") == "csharp"
    assert manage_archives.normalize_category_name("Web-App") == "web-app"

def test_build_category_permalink():
    assert manage_archives.build_category_permalink("DevOps") == "/devops-archive.html"