from glob import glob

import pep8
from pyflakes.api import checkPath


def test_pep8_comformance():
    ''' Test that the code conforms to PEP8 '''
    pep8style = pep8.StyleGuide(config_file='.pep8')
    files = glob('tests/*.py')
    files.append('tsstats.py')
    result = pep8style.check_files(files)
    assert result.total_errors == 0


def test_pyflakes():
    ''' Test that at least tsstats.py conforms to PyFlakes '''
    result = checkPath('tsstats.py')
    assert result == 0
