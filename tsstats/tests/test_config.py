# -*- coding: utf-8 -*-
import pytest

from tsstats.config import load


@pytest.fixture
def config():
    return load()


def test_config(config):
    assert not config.getboolean('General', 'debug')
    assert config.getboolean('General', 'onlinedc')
    config.set('General', 'idmap', 'tsstats/tests/res/id_map.json')
    assert config.get('General', 'idmap') ==\
        'tsstats/tests/res/id_map.json'
    config.set('General', 'log', 'tsstats/tests/res/test.log')
    assert config.get('General', 'log') == 'tsstats/tests/res/test.log'
    config.set('General', 'output', 'output.html')
    assert config.get('General', 'output') == 'output.html'


def test_read():
    config = load(path='tsstats/tests/res/config.ini')
    # test defaults
    assert not config.getboolean('General', 'debug')
    # test written values
    assert config.get('General', 'log') == 'tsstats/tests/res/test.log'
    assert config.get('General', 'output') == 'tsstats/tests/res/output.html'
