import pep8


def test_pep8_comformance():
    ''' Test that the code conforms to PEP8 '''
    pep8style = pep8.StyleGuide(config_file='.pep8')
    result = pep8style.check_files(['tsstats.py', 'tests/test_config.py', 'tests/test_general.py', 'tests/test_style.py'])
    assert result.total_errors == 0
