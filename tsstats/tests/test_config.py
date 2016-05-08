try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from os import remove
from os.path import abspath, exists

from nose.tools import raises, with_setup

from tsstats import exceptions
from tsstats.config import parse_config

configpath = abspath('tsstats/tests/res/test.cfg')


def create_config(values, key='General'):
    config = ConfigParser()
    config[key] = values
    with open(configpath, 'w') as configfile:
        config.write(configfile)


def clean_config():
    if exists(configpath):
        remove(configpath)


@with_setup(clean_config, clean_config)
@raises(exceptions.InvalidConfig)
def test_invalid_config():
    create_config({
        'loggfile': 'tsstats/tests/res/test.log',
        'outputfile': ''
    })
    _, _, _, _ = parse_config(configpath)


@with_setup(clean_config, clean_config)
def test_config():
    create_config({
        'logfile': 'tsstats/tests/res/test.log',
        'outputfile': 'output.html',
        'debug': 'true'
    })
    log_path, output_path = parse_config(configpath)
    assert log_path == abspath('tsstats/tests/res/test.log')
    assert output_path == abspath('output.html')
