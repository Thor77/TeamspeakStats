# -*- coding: utf-8 -*-
# TODO: Implemented online_dc again
import itertools
import logging
import re
from codecs import open
from collections import namedtuple
from glob import glob
from os.path import basename

import pendulum

from tsstats import events
from tsstats.client import Clients

re_log_filename = re.compile(r'ts3server_(?P<date>\d{4}-\d\d-\d\d)'
                             '__(?P<time>\d\d_\d\d_\d\d.\d+)_(?P<sid>\d).log')
re_log_entry = re.compile('(?P<timestamp>\d{4}-\d\d-\d\d\ \d\d:\d\d:\d\d.\d+)'
                          '\|\ *(?P<level>\w+)\ *\|\ *(?P<component>\w+)\ *'
                          '\|\ *(?P<sid>\d+)\ *\|\ *(?P<message>.*)')
re_dis_connect = re.compile(
    r"client (?P<action>(dis)?connected) '(?P<nick>.*)'\(id:(?P<clid>\d+)\)")
re_disconnect_invoker = re.compile(
    r'invokername=(.*)\ invokeruid=(.*)\ reasonmsg'
)

TimedLog = namedtuple('TimedLog', ['path', 'timestamp'])
Server = namedtuple('Server', ['sid', 'clients'])

logger = logging.getLogger('tsstats')


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
            timestamp = pendulum.parse('{0} {1}'.format(
                match['date'], match['time'].replace('_', ':'))
            )
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
                vserver_logfiles[sid] = [tl]
        else:
            # fallback to plain sorting
            vserver_logfiles.setdefault('', [])\
                .append(TimedLog(log, None))
            vserver_logfiles[''] =\
                sorted(vserver_logfiles[''],
                       key=lambda tl: tl.path)
    return vserver_logfiles


def _parse_line(line):
    parsed_events = []
    match = re_log_entry.match(line)
    if not match:
        logger.debug('No match: "%s"', line)
        return []
    match = match.groupdict()
    logdatetime = pendulum.parse(match['timestamp'])
    message = match['message']
    if message.startswith('client'):
        match = re_dis_connect.match(message)
        if not match:
            logger.debug('Unsupported client action: "%s"', message)
            return []
        nick, clid = match.group('nick'), match.group('clid')

        parsed_events.append(events.nick(logdatetime, clid, nick))

        action = match.group('action')
        if action == 'connected':
            parsed_events.append(events.connect(logdatetime, clid))
        elif action == 'disconnected':
            parsed_events.append(events.disconnect(logdatetime, clid))
            if 'invokeruid' in message:
                re_disconnect_data = re_disconnect_invoker.findall(
                    message)
                invokernick, invokeruid = re_disconnect_data[0]
                parsed_events.append(
                    events.nick(logdatetime, invokeruid, invokernick)
                )
                if 'bantime' in message:
                    parsed_events.append(
                        events.ban(logdatetime, invokeruid, clid)
                    )
                else:
                    parsed_events.append(
                        events.kick(logdatetime, invokeruid, clid)
                    )
        return parsed_events


def parse_logs(log_glob, ident_map=None, online_dc=True, *args, **kwargs):
    '''
    parse logs from `log_glob`

    :param log_glob: path to server-logs (supports globbing)
    :param ident_map: identmap used for Client-initializations

    :type log_glob: str
    :type ident_map: dict
    '''
    for virtualserver_id, logs in _bundle_logs(glob(log_glob)).items():
        clients = Clients(ident_map)
        for log in logs:
            with open(log.path, encoding='utf-8') as f:
                # parse logfile line by line and filter lines without events
                events = filter(None, map(_parse_line, f))
                # chain apply events to Client-obj
                clients.apply_events(itertools.chain.from_iterable(events))
        if len(clients) >= 1:
            # assemble Server-obj and yield
            yield Server(virtualserver_id, clients)
