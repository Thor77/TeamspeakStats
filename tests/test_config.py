import configparser
from os import remove
from os.path import exists
from tsstats import parse_config, exceptions, gen_abspath
from nose.tools import raises, with_setup

configpath = gen_abspath('tests/res/test.cfg')


def create_config(values, key='General'):
    config = configparser.ConfigParser()
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
        'loggfile': 'tests/res/test.log',
        'outputfile': ''
    })
    _, _, _, _ = parse_config(configpath)


@with_setup(clean_config, clean_config)
def test_config():
    create_config({
        'logfile': 'tests/res/test.log',
        'outputfile': 'output.html',
        'debug': 'true'
    })
    log_path, output_path, debug, debug_file = parse_config(configpath)
    assert log_path == gen_abspath('tests/res/test.log')
    assert output_path == gen_abspath('output.html')
    assert debug
    assert not debug_file
