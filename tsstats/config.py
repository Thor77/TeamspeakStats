from os.path import abspath

from tsstats.exceptions import InvalidConfig

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def parse_config(config_path):
    config = ConfigParser()
    config.read(config_path)
    if not config.has_section('General') or not \
        (config.has_option('General', 'log') and
         config.has_option('General', 'output')):
        raise InvalidConfig
    return (abspath(config.get('General', 'log')),
            abspath(config.get('General', 'output')))
