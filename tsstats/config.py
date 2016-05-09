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
        (config.has_option('General', 'logfile') and
         config.has_option('General', 'outputfile')):
        raise InvalidConfig

    log_path = abspath(config.get('General', 'logfile'))
    output_path = abspath(config.get('General', 'outputfile'))
    return log_path, output_path
