import argparse
import json
import logging
from os.path import abspath, exists

from tsstats.config import parse_config
from tsstats.exceptions import InvalidConfig
from tsstats.log import parse_logs
from tsstats.template import render_template

logger = logging.getLogger('tsstats')


def cli():
    parser = argparse.ArgumentParser(
        description='A simple Teamspeak stats-generator - based on server-logs'
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
    args = parser.parse_args()
    main(**vars(args))


def main(config=None, idmap=None, log=None, output=None, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)

    if config:
        config = abspath(config)
        if not exists(config):
            logger.fatal('config not found (%s)', config)
        idmap, log, output, debug = parse_config(config)
        if debug:
            logger.setLevel(logging.DEBUG)

    if idmap:
        idmap = abspath(idmap)
        if not exists(idmap):
            logger.fatal('identmap not found (%s)', idmap)
        # read id_map
        identmap = json.load(open(idmap))
    else:
        identmap = None

    if not log or not output:
        raise InvalidConfig('log or output missing')

    clients = parse_logs(log, ident_map=identmap)
    render_template(clients, output=abspath(output))


if __name__ == '__main__':
    cli()
