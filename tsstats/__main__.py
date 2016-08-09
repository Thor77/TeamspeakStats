# -*- coding: utf-8 -*-

import argparse
import json
import logging
from os.path import abspath, exists

from tsstats import config
from tsstats.exceptions import InvalidConfiguration
from tsstats.log import parse_logs
from tsstats.template import render_template

logger = logging.getLogger('tsstats')


def cli():
    parser = argparse.ArgumentParser(
        description='A simple Teamspeak stats-generator, based on server-logs',
        argument_default=argparse.SUPPRESS
    )
    parser.add_argument(
        '-c', '--config',
        type=str, help='path to config'
    )
    parser.add_argument(
        '--idmap', type=str, help='path to id_map'
    )
    parser.add_argument(
        '-l', '--log',
        type=str, help='path to your logfile(s)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str, help='path to the output-file', default='stats.html'
    )
    parser.add_argument(
        '-d', '--debug',
        help='debug mode', action='store_true'
    )
    parser.add_argument(
        '-nod', '--noonlinedc',
        help='don\'t add connect until now to onlinetime',
        action='store_false', dest='onlinedc'
    )
    options = parser.parse_args()
    if 'config' in options:
        configuration = config.load(options.config)
    else:
        configuration = config.load()
    for option, value in vars(options).items():
        configuration.set('General', option, str(value))
    main(configuration)


def main(configuration):
    if configuration.getboolean('General', 'debug'):
        logger.setLevel(logging.DEBUG)

    idmap = configuration.get('General', 'idmap')
    if idmap:
        idmap = abspath(idmap)
        if not exists(idmap):
            logger.fatal('identmap not found (%s)', idmap)
        # read id_map
        identmap = json.load(open(idmap))
    else:
        identmap = None

    log = configuration.get('General', 'log')
    if not log:
        raise InvalidConfiguration('log or output missing')

    sid_clients = parse_logs(
        log, ident_map=identmap,
        online_dc=configuration.getboolean('General', 'onlinedc')
    )
    for sid, clients in sid_clients.items():
        if sid and len(sid_clients) > 1:
            ext = '.{}'.format(sid)
        else:
            ext = ''
        render_template(
            clients,
            output=abspath(configuration.get('General', 'output') + ext)
        )


if __name__ == '__main__':
    cli()
