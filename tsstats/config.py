# -*- coding: utf-8 -*-
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

import logging

logger = logging.getLogger('tsstats')


DEFAULT_CONFIG = {
    'General': {
        'debug': False,
        'debugstdout': False,
        'log': '',
        'output': 'tsstats.html',
        'idmap': '',
        'onlinedc': True,
        'template': 'index.jinja2',
        'datetimeformat': '%x %X %Z',
        'onlinetimethreshold': -1,
        'lastseenrelative': True
    }
}


def load(path=None):
    '''
    parse config at `config_path`

    :param config_path: path to config-file
    :type config_path: str

    :return: values of config
    :rtype: tuple
    '''
    logger.debug('reading config')
    config = RawConfigParser()
    # use this way to set defaults, because ConfigParser.read_dict
    # is not available < 3.2
    for section, items in DEFAULT_CONFIG.items():
        if section not in config.sections():
            config.add_section(section)
        for key, value in items.items():
            config.set(section, key, str(value))
    if path:
        config.read(path)
    return config
