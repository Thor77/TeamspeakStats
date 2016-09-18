# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from os.path import dirname

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from tsstats.utils import seconds_to_text, sort_clients

logger = logging.getLogger('tsstats')


def render_template(clients, output, title='TeamspeakStats',
                    template_path='template.html', datetime_fmt='%x %X %Z'):
    '''
    render template with `clients`

    :param clients: clients to fill template with
    :param output: path to output-file
    :param template_name: path to template-file
    :param title: title of the resulting html-document
    :param template_path: path to template-file
    :param datetime_fmt: custom datetime-format

    :type clients: tsstats.client.Clients
    :type output: str
    :type template_name: str
    :type title: str
    :type template_path: str
    :type datetime_fmt: str
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
        formatted = timestamp.strftime(datetime_fmt)
        logger.debug('Formatting timestamp %s -> %s', timestamp, formatted)
        return formatted
    template_env.filters['frmttime'] = frmttime
    template = template_env.get_template(template_path)
    logger.debug('Rendering template %s', template)
    with open(output, 'w') as f:
        f.write(template.render(title=title, objs=objs,
                                debug=logger.level <= logging.DEBUG,
                                creation_time=datetime.now()))
        logger.debug('Wrote rendered template to %s', output)
