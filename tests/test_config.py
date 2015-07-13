import configparser
from os import remove
from os.path import exists
import tsstats
from nose.tools import raises, with_setup


def create_config(values, key='General'):
    config = configparser.ConfigParser()
    config[key] = values
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def clean_config():
    if exists('config.ini'):
        remove('config.ini')


def clean_result():
    if exists('output.html'):
        remove('output.html')


@with_setup(clean_config, clean_config)
@raises(Exception)
def test_invalid_config():
    config = configparser.ConfigParser()
    create_config({
        'logfile': 'tests/res/test.log',
        'outputfile': '',
        'deebug': 'false',
    })
    _, _, _, _ = parse_config(config_path)


@with_setup(clean_config, clean_config)
@raises(Exception)
def test_debug_without_debugfile():
    config = configparser.ConfigParser()
    create_config({
        'logfile': 'tests/res/test.log',
        'debug': 'true',
        'debugfile': 'false',
    })
    _, _, _, _ = parse_config(config_path)
    open('debug.txt', 'r')
