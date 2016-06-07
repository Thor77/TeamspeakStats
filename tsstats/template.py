# -*- coding: utf-8 -*-

import logging
from os.path import dirname
from time import localtime, strftime

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
    clients_onlinetime_ = sort_clients(clients, 'onlinetime')
    clients_onlinetime = [
        (client, seconds_to_text(onlinetime))
        for client, onlinetime in clients_onlinetime_
    ]

    clients_kicks = sort_clients(clients, 'kicks')
    clients_pkicks = sort_clients(clients, 'pkicks')
    clients_bans = sort_clients(clients, 'bans')
    clients_pbans = sort_clients(clients, 'pbans')
    objs = [('Onlinetime', clients_onlinetime), ('Kicks', clients_kicks),
            ('passive Kicks', clients_pkicks),
            ('Bans', clients_bans), ('passive Bans', clients_pbans)]

    # render
    template_loader = ChoiceLoader([
        PackageLoader(__package__, ''),
        FileSystemLoader(dirname(__file__))
    ])
    template_env = Environment(loader=template_loader)

    def fmttime(timestamp):
        return strftime('%x %X', localtime(int(timestamp)))
    template_env.filters['frmttime'] = fmttime
    template = template_env.get_template('template.html')
    with open(output, 'w') as f:
        f.write(template.render(title=title, objs=objs,
                                debug=logger.level <= logging.DEBUG))
