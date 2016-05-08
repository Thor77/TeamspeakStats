import pyflakes.api


def test_pyflakes():
    ''' Test that at least tsstats.py conforms to PyFlakes '''
    result = pyflakes.api.checkPath('**/*.py')
    assert result == 0
