try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import logging

logger = logging.getLogger('tsstats')


def parse_config(config_path):
    logger.debug('reading config')
    config = ConfigParser()
    config.read(config_path)
    # use dict(ConfigParser.items) to get an easy-to-use interface
    # compatible with py2 and py3
    config_items = dict(config.items('General'))
    if 'debug' in config_items:
        config_items['debug'] = config.getboolean('General', 'debug')
    logger.debug('raw config: %s', config_items)
    return (
        config_items.get('idmap'),
        config_items.get('log'),
        config_items.get('output'),
        config_items.get('debug', False)
    )
