from os.path import abspath

from tsstats.exceptions import InvalidConfig

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def parse_config(config_path):
    config = ConfigParser()
    config.read(config_path)
    if 'General' not in config or not \
            ('logfile' in config['General'] and
                'outputfile' in config['General']):
        raise InvalidConfig

    general = config['General']
    log_path = abspath(general['logfile'])
    output_path = abspath(general['outputfile'])
    return log_path, output_path
