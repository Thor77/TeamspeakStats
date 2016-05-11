import argparse
import json
import logging
from os.path import abspath, exists

from tsstats.config import parse_config
from tsstats.exceptions import ConfigNotFound
from tsstats.log import parse_logs
from tsstats.template import render_template

logger = logging.getLogger('tsstats')


def cli():
    parser = argparse.ArgumentParser(
        description='A simple Teamspeak stats-generator - based on server-logs'
    )
    parser.add_argument(
        '--config', type=str, help='path to config', default='config.ini'
    )
    parser.add_argument(
        '--idmap', type=str, help='path to id_map', default='id_map.json'
    )
    parser.add_argument(
        '--debug', help='debug mode', action='store_true'
    )
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    main(args.config, args.idmap)


def main(config_path='config.ini', id_map_path='id_map.json'):
    # check cmdline-args
    config_path = abspath(config_path)
    id_map_path = abspath(id_map_path)

    if not exists(config_path):
        raise ConfigNotFound(config_path)

    if exists(id_map_path):
        # read id_map
        id_map = json.load(open(id_map_path))
    else:
        id_map = {}

    log, output = parse_config(config_path)
    clients = parse_logs(log, ident_map=id_map)
    render_template(clients, output=output)


if __name__ == '__main__':
    cli()
