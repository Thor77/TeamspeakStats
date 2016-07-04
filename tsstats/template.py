# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from os.path import dirname

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from tsstats.utils import seconds_to_text, sort_clients

logger = logging.getLogger('tsstats')


def render_template(clients, output, title='TeamspeakStats'):
    '''
    render template with `clients`

    :param clients: clients to fill template with
    :param output: path to output-file
    :param template_name: path to template-file
    :param title: title of the resulting html-document

    :type clients: tsstats.client.Clients
    :type output: str
    :type template_name: str
    :type title: str
    '''
    # prepare clients
    clients_onlinetime_ = sort_clients(
        clients, lambda c: c.onlinetime.total_seconds()
    )
    clients_onlinetime = [
        (client, seconds_to_text(int(onlinetime)))
        for client, onlinetime in clients_onlinetime_
    ]

    clients_kicks = sort_clients(clients, lambda c: c.kicks)
    clients_pkicks = sort_clients(clients, lambda c: c.pkicks)
    clients_bans = sort_clients(clients, lambda c: c.bans)
    clients_pbans = sort_clients(clients, lambda c: c.pbans)
    objs = [('Onlinetime', clients_onlinetime), ('Kicks', clients_kicks),
            ('passive Kicks', clients_pkicks),
            ('Bans', clients_bans), ('passive Bans', clients_pbans)]

    # render
    template_loader = ChoiceLoader([
        PackageLoader(__package__, ''),
        FileSystemLoader(dirname(__file__))
    ])
    template_env = Environment(loader=template_loader)

    def frmttime(timestamp):
        if not timestamp:
            return ''
        return timestamp.strftime('%x %X %Z')
    template_env.filters['frmttime'] = frmttime
    template = template_env.get_template('template.html')
    with open(output, 'w') as f:
        f.write(template.render(title=title, objs=objs,
                                debug=logger.level <= logging.DEBUG,
                                creation_time=datetime.now()))
