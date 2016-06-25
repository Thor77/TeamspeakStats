# -*- coding: utf-8 -*-

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import logging

logger = logging.getLogger('tsstats')


def parse_config(config_path):
    '''
    parse config at `config_path`

    :param config_path: path to config-file
    :type config_path: str

    :return: values of config
    :rtype: tuple
    '''
    logger.debug('reading config')
    config = ConfigParser()
    config.read(config_path)
    # use dict(ConfigParser.items) to get an easy-to-use interface
    # compatible with py2 and py3
    config_items = dict(config.items('General'))
    if 'debug' in config_items:
        config_items['debug'] = config.getboolean('General', 'debug')
    if 'onlinedc' in config_items:
        config_items['onlinedc'] = config.getboolean('General', 'onlinedc')
    logger.debug('raw config: %s', config_items)
    return (
        config_items.get('idmap'),
        config_items.get('log'),
        config_items.get('output'),
        config_items.get('debug', False),
        config_items.get('onlinedc', True)
    )
