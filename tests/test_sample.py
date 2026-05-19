def test_always_passes():
    assert True == True

def test_readme_exists():
    import os
    assert os.path.exists('README.md')

def test_requirements_exists():
    import os
    assert os.path.exists('requirements.txt')