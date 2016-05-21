try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from os import remove
from os.path import abspath, exists

import pytest

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


def test_config(config):
    create_config({
        'idmap': 'tsstats/tests/res/id_map.json',
        'log': 'tsstats/tests/res/test.log',
        'output': 'output.html',
        'debug': 'true'
    })
    idmap, log, output, debug = parse_config(configpath)
    assert idmap == 'tsstats/tests/res/id_map.json'
    assert log == 'tsstats/tests/res/test.log'
    assert output == 'output.html'
    assert debug is True
