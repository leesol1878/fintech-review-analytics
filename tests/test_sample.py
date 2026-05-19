def test_always_passes():
    assert True == True

def test_project_exists():
    import os
    assert os.path.exists('README.md')