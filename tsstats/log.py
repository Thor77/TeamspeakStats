import logging
import re
from datetime import datetime
from glob import glob

from tsstats.client import Client, Clients

re_log_entry = re.compile('(?P<timestamp>\d{4}-\d\d-\d\d\ \d\d:\d\d:\d\d.\d+)'
                          '\|(?P<level>\w+)\ +\|(?P<component>\w+)'
                          '\|\ +(?P<sid>\d+)\|\ (?P<message>.*)')
re_dis_connect = re.compile(r"'(.*)'\(id:(\d*)\)")
re_disconnect_invoker = re.compile(
    r'invokername=(.*)\ invokeruid=(.*)\ reasonmsg'
)


logger = logging.getLogger('tsstats')


def parse_logs(log_glob, ident_map=None):
    clients = Clients(ident_map)
    for log_file in sorted(log_file for log_file in glob(log_glob)):
        clients = parse_log(log_file, ident_map, clients)
    return clients


def parse_log(log_path, ident_map=None, clients=None):
    if not clients:
        clients = Clients(ident_map)
    log_file = open(log_path)
    # process lines
    logger.debug('Started parsing of %s', log_file.name)
    for line in log_file:
        match = re_log_entry.match(line)
        if not match:
            logger.debug('No match: "%s"', line)
            continue
        match = match.groupdict()
        log_format = '%Y-%m-%d %H:%M:%S.%f'
        stripped_time = datetime.strptime(match['timestamp'], log_format)
        logdatetime = int((stripped_time - datetime(1970, 1, 1))
                          .total_seconds())
        message = match['message']
        if message.startswith('client'):
            nick, clid = re_dis_connect.findall(message)[0]
            client = clients.setdefault(clid, Client(clid, nick))
            client.nick = nick  # set nick to display changes
            if message.startswith('client connected'):
                client.connect(logdatetime)
            elif message.startswith('client disconnected'):
                client.disconnect(logdatetime)
                if 'invokeruid' in message:
                    re_disconnect_data = re_disconnect_invoker.findall(
                        message)
                    invokernick, invokeruid = re_disconnect_data[0]
                    invoker = clients.setdefault(invokeruid,
                                                 Client(invokeruid))
                    invoker.nick = invokernick
                    if 'bantime' in message:
                        invoker.ban(client)
                    else:
                        invoker.kick(client)
    logger.debug('Finished parsing of %s', log_file.name)
    return clients
