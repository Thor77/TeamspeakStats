try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from os import remove
from os.path import abspath, exists

import pytest

from tsstats import exceptions
from tsstats.config import parse_config

configpath = abspath('tsstats/tests/res/test.cfg')


def create_config(values, key='General'):
    config = ConfigParser()
    config.add_section('General')
    for option, value in values.items():
        config.set('General', option, value)
    with open(configpath, 'w') as configfile:
        config.write(configfile)


@pytest.fixture
def config(request):
    def clean():
        if exists(configpath):
            remove(configpath)
    request.addfinalizer(clean)


def test_invalid_config(config):
    create_config({
        'loggfile': 'tsstats/tests/res/test.log',
        'outputfile': ''
    })
    with pytest.raises(exceptions.InvalidConfig):
        _, _, _, _ = parse_config(configpath)


def test_config(config):
    create_config({
        'logfile': 'tsstats/tests/res/test.log',
        'outputfile': 'output.html',
        'debug': 'true'
    })
    log_path, output_path = parse_config(configpath)
    assert log_path == abspath('tsstats/tests/res/test.log')
    assert output_path == abspath('output.html')
