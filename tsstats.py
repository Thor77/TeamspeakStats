import re
import glob
import json
import logging
import argparse
import datetime
from os import sep
import configparser
from sys import argv
from time import mktime
from time import strftime, localtime
from os.path import exists
from jinja2 import Environment, FileSystemLoader


class Exceptions:
    class ConfigNotFound(Exception):
        pass

    class InvalidConfig(Exception):
        pass

    class InvalidLog(Exception):
        pass

exceptions = Exceptions


class Clients:

    def __init__(self, ident_map={}):
        self.clients_by_id = {}
        self.clients_by_uid = {}
        self.ident_map = ident_map

    def is_id(self, id_or_uid):
        try:
            int(id_or_uid)
            return True
        except ValueError:
            return False

    def __add__(self, id_or_uid):
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self.clients_by_id[id_or_uid] = Client(id_or_uid)
        else:
            if id_or_uid not in self.clients_by_uid:
                self.clients_by_uid[id_or_uid] = Client(id_or_uid)
        return self

    def __getitem__(self, id_or_uid):
        if id_or_uid in self.ident_map:
            id_or_uid = self.ident_map[id_or_uid]
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self += id_or_uid
            return self.clients_by_id[id_or_uid]
        else:
            if id_or_uid not in self.clients_by_uid:
                self += id_or_uid
            return self.clients_by_uid[id_or_uid]

    def __iter__(self):
        for id_client in self.clients_by_id.values():
            yield id_client
        for uid_client in self.clients_by_uid.values():
            yield uid_client


class Client:

    def __init__(self, identifier):
        # public
        self.identifier = identifier
        self.nick = None
        self.connected = 0
        self.onlinetime = 0
        self.kicks = 0
        self.pkicks = 0
        self.bans = 0
        self.pbans = 0
        self.last_seen = 0
        # private
        self._last_connect = 0

    def connect(self, timestamp):
        '''
        client connects at "timestamp"
        '''
        logging.debug('CONNECT {}'.format(str(self)))
        self.connected += 1
        self._last_connect = timestamp

    def disconnect(self, timestamp):
        '''
        client disconnects at "timestamp"
        '''
        logging.debug('DISCONNECT {}'.format(str(self)))
        if not self.connected:
            logging.debug('^ disconnect before connect')
            raise exceptions.InvalidLog('disconnect before connect!')
        self.connected -= 1
        session_time = timestamp - self._last_connect
        self.onlinetime += session_time
        self.last_seen = timestamp

    def kick(self, target):
        '''
        client kicks "target" (Client-obj)
        '''
        logging.debug('KICK {} -> {}'.format(str(self), str(target)))
        target.pkicks += 1
        self.kicks += 1

    def ban(self, target):
        '''
        client bans "target" (Client-obj)
        '''
        logging.debug('BAN {} -> {}'.format(str(self), str(target)))
        target.pbans += 1
        self.bans += 1

    def __str__(self):
        return '<{},{}>'.format(self.identifier, self.nick)

    def __getitem__(self, item):
        return {
            'identifier': self.identifier,
            'nick': self.nick,
            'connected': self.connected,
            'onlinetime': self.onlinetime,
            'kicks': self.kicks,
            'pkicks': self.pkicks,
            'bans': self.bans,
            'pbans': self.pbans,
        }[item]


re_dis_connect = re.compile(r"'(.*)'\(id:(\d*)\)")
re_disconnect_invoker = re.compile(
    r"invokername=(.*)\ invokeruid=(.*)\ reasonmsg"
)
path_split = __file__.split(sep)[:-1]
abspath = sep.join(path_split)
if len(path_split) > 0:
    abspath += sep


def gen_abspath(filename):
    return filename if filename.startswith(sep) else abspath + filename


def _get_sorted(stor, key):
    clients = stor.values()
    cl_data = [(client, client[key]) for client in clients if client[key] > 0]
    return sorted(cl_data, key=lambda data: data[1], reverse=True)


def _format_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours = str(hours) + 'h ' if hours > 0 else ''
    minutes = str(minutes) + 'm ' if minutes > 0 else ''
    seconds = str(seconds) + 's' if seconds > 0 else ''
    return hours + minutes + seconds


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

    # find all log-files and open them
    log_files = [open(file_name) for file_name in glob.glob(log_path)]

    for log_file in log_files:
        # process lines
        logging.debug('Started parsing of {}'.format(log_file.name))
        for line in log_file:
            parts = line.split('|')
            log_format = '%Y-%m-%d %H:%M:%S.%f'
            stripped_time = datetime.datetime.strptime(parts[0], log_format)
            logdatetime = int(stripped_time.timestamp())
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


def render_template(clients, output, template_name='template.html',
                    title='TeamspeakStats', debug=False):
    # prepare clients
    clients_onlinetime_ = _get_sorted(clients.clients_by_id, 'onlinetime')
    clients_onlinetime = [
        (client, _format_seconds(onlinetime))
        for client, onlinetime in clients_onlinetime_
    ]

    clients_kicks = _get_sorted(clients.clients_by_uid, 'kicks')
    clients_pkicks = _get_sorted(clients.clients_by_id, 'pkicks')
    clients_bans = _get_sorted(clients.clients_by_uid, 'bans')
    clients_pbans = _get_sorted(clients.clients_by_id, 'pbans')
    objs = [('Onlinetime', clients_onlinetime), ('Kicks', clients_kicks),
            ('passive Kicks', clients_pkicks),
            ('Bans', clients_bans), ('passive Bans', clients_pbans)]

    # render
    template_loader = FileSystemLoader(abspath)
    template_env = Environment(loader=template_loader)

    def frmttime(timestamp):
        return strftime('%x %X', localtime(int(timestamp)))
    template_env.filters['frmttime'] = frmttime
    template = template_env.get_template(template_name)
    with open(output, 'w') as f:
        f.write(template.render(title=title, objs=objs, debug=debug))


def parse_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    if 'General' not in config or not \
            ('logfile' in config['General'] and
                'outputfile' in config['General']):
        raise exceptions.InvalidConfig

    general = config['General']
    log_path = gen_abspath(general['logfile'])
    output_path = gen_abspath(general['outputfile'])
    return log_path, output_path


def main(config_path='config.ini', id_map_path='id_map.json',
         debug=False, debugfile=False):
    # check cmdline-args
    config_path = gen_abspath(config_path)
    id_map_path = gen_abspath(id_map_path)

    if not exists(config_path):
        raise exceptions.ConfigNotFound(config_path)

    if exists(id_map_path):
        # read id_map
        id_map = json.load(open(id_map_path))
    else:
        id_map = {}

    log_path, output_path = parse_config(config_path)
    clients = parse_logs(log_path, ident_map=id_map, file_log=debugfile)
    render_template(clients, output=output_path, debug=debug)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A simple Teamspeak stats-generator - based on server-logs'
    )
    parser.add_argument(
        '--config', type=str, help='path to config', default='config.ini'
    )
    parser.add_argument(
        '--idmap', type=str, help='path to id_map', default='id_map.json'
    )
    parser.add_argument(
        '--debug', help='debug mode', action='store_true'
    )
    parser.add_argument(
        '--debugfile', help='write debug-log to file', action='store_true'
    )
    args = parser.parse_args()
    main(args.config, args.idmap, args.debug, args.debugfile)
