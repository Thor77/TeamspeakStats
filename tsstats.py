import re
import glob
import json
import logging
import datetime
import configparser
from sys import argv
from time import mktime
from os.path import exists, abspath
from jinja2 import Environment, FileSystemLoader

# logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
# create handler
file_handler = logging.FileHandler('debug.txt', 'w', 'UTF-8')
file_handler.setFormatter(logging.Formatter('%(message)s'))
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
# add handler
log.addHandler(file_handler)
log.addHandler(stream_handler)


class Clients:

    def __init__(self):
        self.clients_by_id = {}
        self.clients_by_uid = {}

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
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self += id_or_uid
            return self.clients_by_id[id_or_uid]
        else:
            if id_or_uid not in self.clients_by_uid:
                self += id_or_uid
            return self.clients_by_uid[id_or_uid]

clients = Clients()


class Client:

    def __init__(self, identifier):
        # public
        self.identifier = identifier
        self.nick = None
        self.connected = 0
        self.onlinetime = datetime.timedelta()
        self.kicks = 0
        self.pkicks = 0
        self.bans = 0
        self.pbans = 0
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
            raise Exception('disconnect before connect!')
        self.connected -= 1
        session_time = timestamp - self._last_connect
        self.onlinetime += session_time

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

    def __format__(self):
        return self.__str__()

# check cmdline-args
config_path = argv[1] if len(argv) >= 2 else 'config.ini'
config_path = abspath(config_path)
id_map_path = argv[2] if len(argv) >= 3 else 'id_map.json'
id_map_path = abspath(id_map_path)

if not exists(config_path):
    raise Exception('Couldn\'t find config-file at {}'.format(config_path))

if exists(id_map_path):
    # read id_map
    id_map = json.load(open(path + 'id_map.json'))
else:
    id_map = {}

# parse config
config = configparser.ConfigParser()
config.read(config_path)
# check keys
if 'General' not in config:
    raise Exception('Invalid config! Section "General" missing!')
general = config['General']
html = config['HTML'] if 'HTML' in config.sections() else {}
if not ('logfile' in general or 'outputfile' in general):
    raise Exception('Invalid config! "logfile" and/or "outputfile" missing!')
log_path = general['logfile']
output_path = general['outputfile']
debug = general.get('debug', 'true') in ['true', 'True']
title = html.get('title', 'TeamspeakStats')
if not debug:
    logging.disable(logging.DEBUG)

generation_start = datetime.datetime.now()

re_dis_connect = re.compile(r"'(.*)'\(id:(\d*)\)")
re_disconnect_invoker = re.compile(r"invokername=(.*)\ invokeruid=(.*)\ reasonmsg")

# find all log-files and collect lines
log_files = [file_name for file_name in glob.glob(log_path) if exists(file_name)]
log_lines = []
for log_file in log_files:
    for line in open(log_file, 'r'):
        log_lines.append(line)


def get_client(clid):
    if clid in id_map:
        clid = id_map[clid]
    client = clients[clid]
    client.nick = nick
    return client

# process lines
for line in log_lines:
    parts = line.split('|')
    logdatetime = datetime.datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
    data = '|'.join(parts[4:]).strip()
    if data.startswith('client'):
        nick, clid = re_dis_connect.findall(data)[0]
        if data.startswith('client connected'):
            client = get_client(clid)
            client.connect(logdatetime)
        elif data.startswith('client disconnected'):
            client = get_client(clid)
            client.disconnect(logdatetime)
            if 'invokeruid' in data:
                re_disconnect_data = re_disconnect_invoker.findall(data)
                invokernick, invokeruid = re_disconnect_data[0]
                invoker = clients[invokeruid]
                invoker.nick = invokernick
                if 'bantime' in data:
                    invoker.ban(client)
                else:
                    invoker.kick(client)

generation_end = datetime.datetime.now()
generation_delta = generation_end - generation_start

# render template
template = Environment(loader=FileSystemLoader(abspath('.'))).get_template('template.html')
# sort all values desc
cl_by_id = clients.clients_by_id
cl_by_uid = clients.clients_by_uid
clients_onlinetime_ = sorted([(client, client.onlinetime) for client in cl_by_id.values()], key=lambda data: data[1], reverse=True)
clients_onlinetime = []
for client, onlinetime in clients_onlinetime_:
    minutes, seconds = divmod(client.onlinetime.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours = str(hours) + 'h ' if hours != 0 else ''
    minutes = str(minutes) + 'm ' if minutes != 0 else ''
    seconds = str(seconds) + 's' if seconds != 0 else ''
    clients_onlinetime.append((client, hours + minutes + seconds))
clients_kicks = sorted([(client, client.kicks) for client in cl_by_uid.values() if client.kicks > 0], key=lambda data: data[1], reverse=True)
clients_pkicks = sorted([(client, client.pkicks) for client in cl_by_id.values() if client.pkicks > 0], key=lambda data: data[1], reverse=True)
clients_bans = sorted([(client, client.bans) for client in cl_by_uid.values() if client.bans > 0], key=lambda data: data[1], reverse=True)
clients_pbans = sorted([(client, client.pbans) for client in cl_by_id.values() if client.pbans > 0], key=lambda data: data[1], reverse=True)
objs = [('Onlinetime', clients_onlinetime), ('Kicks', clients_kicks),
        ('passive Kicks', clients_pkicks),
        ('Bans', clients_bans), ('passive Bans', clients_pbans)]  # (headline, list)

with open(output_path, 'w') as f:
    f.write(template.render(title=title, objs=objs, generation_time='{}.{}'.format(generation_delta.seconds, generation_delta.microseconds), time=generation_end.strftime('%d.%m.%Y %H:%M'), debug=debug))
