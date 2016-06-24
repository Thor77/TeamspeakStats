# -*- coding: utf-8 -*-

import logging
import re
from collections import namedtuple
from datetime import datetime
from glob import glob
from os.path import basename

from tsstats.client import Client, Clients

re_log_filename = re.compile(r'ts3server_(?P<date>\d{4}-\d\d-\d\d)'
                             '__(?P<time>\d\d_\d\d_\d\d.\d+)_(?P<sid>\d).log')
re_log_entry = re.compile('(?P<timestamp>\d{4}-\d\d-\d\d\ \d\d:\d\d:\d\d.\d+)'
                          '\|\ *(?P<level>\w+)\ *\|\ *(?P<component>\w+)\ *'
                          '\|\ *(?P<sid>\d+)\ *\|\ *(?P<message>.*)')
re_dis_connect = re.compile(r"'(.*)'\(id:(\d*)\)")
re_disconnect_invoker = re.compile(
    r'invokername=(.*)\ invokeruid=(.*)\ reasonmsg'
)

log_timestamp_format = '%Y-%m-%d %H:%M:%S.%f'

TimedLog = namedtuple('TimedLog', ['path', 'timestamp'])


logger = logging.getLogger('tsstats')


def parse_logs(log_glob, ident_map=None, *args, **kwargs):
    '''
    parse logs from `log_glob`

    :param log_glob: path to server-logs (supports globbing)
    :param ident_map: identmap used for Client-initializations

    :type log_glob: str
    :type ident_map: dict

    :return: clients bundled by virtual-server
    :rtype: dict
    '''
    vserver_clients = {}
    for virtualserver_id, logs in\
            _bundle_logs(log_file for log_file in glob(log_glob)).items():
        clients = Clients(ident_map)
        for log in logs:
            _parse_details(log.path, clients=clients, *args, **kwargs)
        if len(clients) >= 1:
            vserver_clients[virtualserver_id] = clients
    return vserver_clients


def _bundle_logs(logs):
    '''
    bundle `logs` by virtualserver-id
    and sort by timestamp from filename (if exists)

    :param logs: list of paths to logfiles

    :type logs: list

    :return: `logs` bundled by virtualserver-id and sorted by timestamp
    :rtype: dict{str: [TimedLog]}
    '''
    vserver_logfiles = {}  # sid: [/path/to/log1, ..., /path/to/logn]
    for log in logs:
        # try to get date and sid from filename
        match = re_log_filename.match(basename(log))
        if match:
            match = match.groupdict()
            timestamp = datetime.strptime('{0} {1}'.format(
                match['date'], match['time'].replace('_', ':')),
                log_timestamp_format)
            tl = TimedLog(log, timestamp)
            sid = match['sid']
            if sid in vserver_logfiles:
                # if already exists, keep list sorted by timestamp
                vserver_logfiles[sid].append(tl)
                vserver_logfiles[sid] =\
                    sorted(vserver_logfiles[sid],
                           key=lambda tl: tl.timestamp)
            else:
                # if not exists, just create a list
                vserver_logfiles[match['sid']] = [tl]
        else:
            # fallback to plain sorting
            vserver_logfiles.setdefault('', [])\
                .append(TimedLog(log, None))
            vserver_logfiles[''] =\
                sorted(vserver_logfiles[''],
                       key=lambda tl: tl.path)
    return vserver_logfiles


def _parse_details(log_path, ident_map=None, clients=None, online_dc=True):
    '''
    extract details from log-files

    detailed parsing is done here: onlinetime, kicks, pkicks, bans, pbans

    :param log_path: path to log-file
    :param ident_map: :doc:`identmap`
    :param clients: clients-object to add parsing-results to
    :param online_cd: disconnect online clients after parsing

    :type log_path: str
    :type ident_map: dict
    :type clients: tsstats.client.Clients
    :type online_cd: bool

    :return: parsed clients
    :rtype: tsstats.client.Clients
    '''
    if clients is None:
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
        logdatetime = datetime.strptime(match['timestamp'],
                                        log_timestamp_format)
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
    if online_dc:
        for client in clients:
            if client.connected:
                client.disconnect(datetime.utcnow())
                client.connected += 1
    logger.debug('Finished parsing of %s', log_file.name)
    return clients
