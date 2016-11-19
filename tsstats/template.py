# -*- coding: utf-8 -*-

import logging
from collections import namedtuple
from datetime import datetime
from os.path import dirname, join

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from tsstats.utils import filter_threshold, seconds_to_text, sort_clients

logger = logging.getLogger('tsstats')

SortedClients = namedtuple('SortedClients', [
    'onlinetime', 'kicks', 'pkicks', 'bans', 'pbans'])


def prepare_clients(clients, onlinetime_threshold=-1):
    '''
    Prepare `clients` for rendering

    sort them and convert onlinetime to string
    '''
    # sort by onlinetime
    onlinetime_ = sort_clients(
        clients, lambda c: c.onlinetime.total_seconds()
    )
    # filter clients not matching threshold
    onlinetime_ = filter_threshold(onlinetime_,
                                   onlinetime_threshold)
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


def render_template(clients, output, title='TeamspeakStats',
                    template='stats.jinja2', datetime_fmt='%x %X %Z',
                    onlinetime_threshold=-1):
    '''
    render template with `clients`

    :param clients: clients to fill template with
    :param output: path to output-file
    :param template_name: path to template-file
    :param title: title of the resulting html-document
    :param template_path: path to template-file
    :param datetime_fmt: custom datetime-format
    :param onlinetime_threshold: threshold for clients onlinetime

    :type clients: tsstats.client.Clients
    :type output: str
    :type template_name: str
    :type title: str
    :type template_path: str
    :type datetime_fmt: str
    :type onlinetime_threshold: int
    '''
    prepared_clients = prepare_clients(clients)
    objs = [
        ('Onlinetime', prepared_clients.onlinetime),
        ('Kicks', prepared_clients.kicks),
        ('passive Kicks', prepared_clients.pkicks),
        ('Bans', prepared_clients.bans),
        ('passive Bans', prepared_clients.pbans)
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
    template_env.filters['frmttime'] = frmttime
    template = template_env.get_template(template)
    logger.debug('Rendering template %s', template)
    template.stream(title=title, objs=objs,
                    debug=logger.level <= logging.DEBUG,
                    creation_time=datetime.utcnow())\
        .dump(output, encoding='utf-8')
    logger.debug('Wrote rendered template to %s', output)
