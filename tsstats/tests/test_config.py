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
