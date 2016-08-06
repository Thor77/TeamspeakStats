try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from os import remove
from os.path import abspath, exists

import pytest

from tsstats.config import load

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
        'debug': 'true',
        'onlinedc': 'false'
    })
    configuration = load(configpath)
    assert configuration.get('General', 'idmap') ==\
        'tsstats/tests/res/id_map.json'
    assert configuration.get('General', 'log') == 'tsstats/tests/res/test.log'
    assert configuration.get('General', 'output') == 'output.html'
    assert configuration.getboolean('General', 'debug') is True
    assert configuration.getboolean('General', 'onlinedc') is False
