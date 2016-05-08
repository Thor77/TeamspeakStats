import logging
import re
from datetime import datetime
from glob import glob

from tsstats.client import Clients

re_dis_connect = re.compile(r"'(.*)'\(id:(\d*)\)")
re_disconnect_invoker = re.compile(
    r'invokername=(.*)\ invokeruid=(.*)\ reasonmsg'
)


def parse_logs(log_path, ident_map={}, file_log=False):
    clients = Clients(ident_map)
    # setup logging
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    if file_log:
        # file logger
        file_handler = logging.FileHandler('debug.txt', 'w', 'UTF-8')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        file_handler.setLevel(logging.DEBUG)
        log.addHandler(file_handler)
    # stream logger (unused)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    # find all log-files and open them TODO: move this into main
    file_paths = sorted([file_path for file_path in glob(log_path)])

    for file_path in file_paths:
        log_file = open(file_path)
        # process lines
        logging.debug('Started parsing of {}'.format(log_file.name))
        for line in log_file:
            parts = line.split('|')
            log_format = '%Y-%m-%d %H:%M:%S.%f'
            stripped_time = datetime.strptime(parts[0], log_format)
            logdatetime = int((stripped_time - datetime(1970, 1, 1))
                              .total_seconds())
            data = '|'.join(parts[4:]).strip()
            if data.startswith('client'):
                nick, clid = re_dis_connect.findall(data)[0]
                if data.startswith('client connected'):
                    client = clients[clid]
                    client.nick = nick
                    client.connect(logdatetime)
                elif data.startswith('client disconnected'):
                    client = clients[clid]
                    client.nick = nick
                    client.disconnect(logdatetime)
                    if 'invokeruid' in data:
                        re_disconnect_data = re_disconnect_invoker.findall(
                            data)
                        invokernick, invokeruid = re_disconnect_data[0]
                        invoker = clients[invokeruid]
                        invoker.nick = invokernick
                        if 'bantime' in data:
                            invoker.ban(client)
                        else:
                            invoker.kick(client)
        logging.debug('Finished parsing of {}'.format(log_file.name))
    return clients
