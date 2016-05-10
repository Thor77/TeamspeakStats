import logging
from os.path import abspath
from time import localtime, strftime

from jinja2 import Environment, FileSystemLoader

from tsstats.utils import seconds_to_text, sort_clients

logger = logging.getLogger('tsstats')


def render_template(clients, output, template_name='tsstats/template.html',
                    title='TeamspeakStats'):
    # prepare clients
    clients_onlinetime_ = sort_clients(clients.clients_by_id, 'onlinetime')
    clients_onlinetime = [
        (client, seconds_to_text(onlinetime))
        for client, onlinetime in clients_onlinetime_
    ]

    clients_kicks = sort_clients(clients.clients_by_uid, 'kicks')
    clients_pkicks = sort_clients(clients.clients_by_id, 'pkicks')
    clients_bans = sort_clients(clients.clients_by_uid, 'bans')
    clients_pbans = sort_clients(clients.clients_by_id, 'pbans')
    objs = [('Onlinetime', clients_onlinetime), ('Kicks', clients_kicks),
            ('passive Kicks', clients_pkicks),
            ('Bans', clients_bans), ('passive Bans', clients_pbans)]

    # render
    template_loader = FileSystemLoader(abspath('.'))
    template_env = Environment(loader=template_loader)

    def fmttime(timestamp):
        return strftime('%x %X', localtime(int(timestamp)))
    template_env.filters['frmttime'] = fmttime
    template = template_env.get_template(template_name)
    with open(output, 'w') as f:
        f.write(template.render(title=title, objs=objs,
                                debug=logger.level <= logging.DEBUG))
