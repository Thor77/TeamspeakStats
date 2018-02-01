# -*- coding: utf-8 -*-
import logging
from collections import namedtuple
from os.path import dirname, join

import pendulum
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from tsstats.log import Server
from tsstats.utils import filter_threshold, seconds_to_text, sort_clients

logger = logging.getLogger('tsstats')

SortedClients = namedtuple('SortedClients', [
    'onlinetime', 'kicks', 'pkicks', 'bans', 'pbans'])


def prepare_clients(clients, onlinetime_threshold=-1):
    '''
    Prepare `clients` for rendering

    sort them, clean their nick-history and convert onlinetime to string

    :param clients: List of clients to prepare
    :param onlinetime_threshold: threshold for clients onlinetime

    :type clients: tsstats.client.Clients
    :type onlinetime_treshold: int

    :return: `clients` sorted by onlinetime, kics, pkicks, bans and pbans
    :rtype: tsstats.template.SortedClients
    '''
    # sort by onlinetime
    onlinetime_ = sort_clients(
        clients, lambda c: c.onlinetime.total_seconds()
    )
    # filter clients not matching threshold
    onlinetime_ = filter_threshold(onlinetime_, onlinetime_threshold)
    # convert timespans to text
    onlinetime = [
        (client, seconds_to_text(int(onlinetime)))
        for client, onlinetime in onlinetime_
    ]
    return SortedClients(
        onlinetime=onlinetime,
        kicks=sort_clients(clients, lambda c: c.kicks),
        pkicks=sort_clients(clients, lambda c: c.pkicks),
        bans=sort_clients(clients, lambda c: c.bans),
        pbans=sort_clients(clients, lambda c: c.pbans)
    )


def render_servers(servers, output, title='TeamspeakStats',
                   template='index.jinja2', datetime_fmt='%x %X %Z',
                   onlinetime_threshold=-1, lastseen_relative=True):
    '''
    Render `servers`

    :param servers: list of servers to render
    :param output: path to output-file
    :param template_name: path to template-file
    :param title: title of the resulting html-document
    :param template_path: path to template-file
    :param datetime_fmt: custom datetime-format
    :param onlinetime_threshold: threshold for clients onlinetime
    :param lastseen_relative: render last seen timestamp relative


    :type servers: [tsstats.log.Server]
    :type output: str
    :type template_name: str
    :type title: str
    :type template_path: str
    :type datetime_fmt: str
    :type onlinetime_threshold: int
    :type lastseen_relative: bool
    '''
    # preparse servers
    prepared_servers = [
        Server(sid, prepare_clients(clients, onlinetime_threshold))
        for sid, clients in servers
    ]
    # render
    template_loader = ChoiceLoader([
        PackageLoader(__package__, 'templates'),
        FileSystemLoader(join(dirname(__file__), 'templates'))
    ])
    template_env = Environment(loader=template_loader)

    def frmttime(timestamp):
        if not timestamp:
            return ''
        formatted = timestamp.strftime(datetime_fmt)
        logger.debug('Formatting timestamp %s -> %s', timestamp, formatted)
        return formatted

    def lastseen(timestamp):
        if lastseen_relative:
            return timestamp.diff_for_humans()
        else:
            return frmttime(timestamp)
    template_env.filters['frmttime'] = frmttime
    template_env.filters['lastseen'] = lastseen
    template = template_env.get_template(template)
    logger.debug('Rendering template %s', template)
    template.stream(title=title, servers=prepared_servers,
                    debug=logger.level <= logging.DEBUG,
                    creation_time=pendulum.utcnow())\
        .dump(output, encoding='utf-8')
    logger.debug('Wrote rendered template to %s', output)
