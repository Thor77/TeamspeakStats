import re
import sys
import glob
import json
import configparser
from os.path import exists
from telnetlib import Telnet
from time import mktime, sleep
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader


def exit(error):
    print('FATAL ERROR:', error)
    import sys
    sys.exit(1)

# get path
arg = sys.argv[0]
arg_find = arg.rfind('/')
if arg_find == -1:
    path = '.'
else:
    path = arg[:arg_find]
path += '/'

config_path = path + 'config.ini'
id_map_path = path + 'id_map.json'

# exists config-file
if not exists(config_path):
    exit('Couldn\'t find config-file at {}'.format(config_path))

# parse config
config = configparser.ConfigParser()
config.read(config_path)
# check keys
if 'General' not in config or 'HTML' not in config:
    exit('Invalid config!')
general = config['General']
html = config['HTML']
if ('logfile' not in general or 'outputfile' not in general) or ('title' not in html):
    exit('Invalid config!')
log_path = general['logfile']
if not exists(log_path):
    exit('Couldn\'t access log-file!')
output_path = general['outputfile']
title = html['title']
show_onlinetime = html.get('onlinetime', True)
show_kicks = html.get('kicks', True)
show_pkicks = html.get('pkicks', True)
show_bans = html.get('bans', True)
show_pbans = html.get('pbans', True)

if exists(id_map_path):
    # read id_map
    id_map = json.load(open(path + 'id_map.json'))
else:
    id_map = {}

generation_start = datetime.now()
clients = {}  # clid: {'nick': ..., 'onlinetime': ..., 'kicks': ..., 'pkicks': ..., 'bans': ..., 'last_connect': ..., 'connected': ...}
kicks = {}

cldata = re.compile(r"'(.*)'\(id:(\d*)\)")
cldata_ban = re.compile(r"by\ client\ '(.*)'\(id:(\d*)\)")
cldata_invoker = re.compile(r"invokerid=\d*\ invokername=(.*)\ invokeruid=(.*)\ reasonmsg")


def add_connect(clid, nick, logdatetime):
    check_client(clid, nick)
    clients[clid]['last_connect'] = mktime(logdatetime.timetuple())
    clients[clid]['connected'] = True


def add_disconnect(clid, nick, logdatetime, set_connected=True):
    check_client(clid, nick)
    connect = datetime.fromtimestamp(clients[clid]['last_connect'])
    delta = logdatetime - connect
    minutes = delta.seconds // 60
    increase_onlinetime(clid, minutes)
    if set_connected:
        clients[clid]['connected'] = False


def add_ban(clid, nick):
    check_client(clid, nick)
    if 'bans' in clients[clid]:
        clients[clid]['bans'] += 1
    else:
        clients[clid]['bans'] = 1


def add_pban(clid, nick):
    check_client(clid, nick)
    if 'pbans' in clients[clid]:
        clients[clid]['pbans'] += 1
    else:
        clients[clid]['pbans'] = 1


####
#
#
#  TODO
#
#
###
def add_kick(cluid, nick):
    if cluid not in kicks:
        kicks[cluid] = {}
    if 'kicks' in kicks[cluid]:
        kicks[cluid]['kicks'] += 1
    else:
        kicks[cluid]['kicks'] = 1
    kicks[cluid]['nick'] = nick


def add_pkick(clid, nick):
    check_client(clid, nick)
    if 'pkicks' in clients[clid]:
        clients[clid]['pkicks'] += 1
    else:
        clients[clid]['pkicks'] = 1


def increase_onlinetime(clid, onlinetime):
    if 'onlinetime' in clients[clid]:
        clients[clid]['onlinetime'] += onlinetime
    else:
        clients[clid]['onlinetime'] = onlinetime


def check_client(clid, nick):
    if clid not in clients:
        clients[clid] = {}
    clients[clid]['nick'] = nick

log_files = [file_name for file_name in glob.glob(log_path)]
log_lines = []
for log_file in log_files:
    for line in open(log_file, 'r'):
        log_lines.append(line)
today = datetime.utcnow()
for line in log_lines:
    parts = line.split('|')
    logdatetime = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
    sid = int(parts[3].strip())
    data = '|'.join(parts[4:]).strip()
    if data.startswith('client'):
        r = cldata.findall(data)[0]
        nick = r[0]
        clid = r[1]
        if clid in id_map:
            clid = id_map[clid]
        if data.startswith('client connected'):
            add_connect(clid, nick, logdatetime)
        elif data.startswith('client disconnected'):
            add_disconnect(clid, nick, logdatetime)
            if 'bantime' in data:
                add_pban(clid, nick)
            elif 'invokerid' in data:
                add_pkick(clid, nick)
                r = cldata_invoker.findall(data)[0]
                nick = r[0]
                cluid = r[1]
                add_kick(cluid, nick)
    elif data.startswith('ban added') and 'cluid' in data:
        r = cldata_ban.findall(data)[0]
        nick = r[0]
        clid = r[1]
        add_ban(clid, nick)

for clid in clients:
    if 'connected' not in clients[clid]:
        clients[clid]['connected'] = False
    if clients[clid]['connected']:
        add_disconnect(clid, clients[clid]['nick'], today, set_connected=False)


generation_end = datetime.now()
generation_delta = generation_end - generation_start


# helper functions
def desc(key, data_dict=clients):
    r = []
    values = {}
    for clid in data_dict:
        if key in data_dict[clid]:
            values[clid] = data_dict[clid][key]
    for clid in sorted(values, key=values.get, reverse=True):
        value = values[clid]
        r.append((clid, data_dict[clid]['nick'], value))
    return r


def render_template():
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template('template.html')
    # format onlinetime
    onlinetime_desc = desc('onlinetime')
    for idx, (clid, nick, onlinetime) in enumerate(onlinetime_desc):
        if onlinetime > 60:
            onlinetime_str = str(onlinetime // 60) + 'h'
            m = onlinetime % 60
            if m > 0:
                onlinetime_str += ' ' + str(m) + 'm'
        else:
            onlinetime_str = str(onlinetime) + 'm'
        onlinetime_desc[idx] = (clid, nick, onlinetime_str, clients[clid]['connected'])

    kicks_desc = desc('kicks', data_dict=kicks)
    pkicks_desc = desc('pkicks')
    bans_desc = desc('bans')
    pbans_desc = desc('pbans')
    show_kicks = len(kicks_desc) > 0
    show_pkicks = len(pkicks_desc) > 0
    show_bans = len(bans_desc) > 0
    show_pbans = len(pbans_desc) > 0
    with open(output_path, 'w+') as f:
        f.write(template.render(title=title, onlinetime=onlinetime_desc, kicks=kicks_desc, pkicks=pkicks_desc, bans=bans_desc, pbans=pbans_desc, seconds='{}.{}'.format(generation_delta.seconds, generation_delta.microseconds),
                date=generation_end.strftime('%d.%m.%Y %H:%M'),
                show_onlinetime=show_onlinetime,
                show_kicks=show_kicks,
                show_pkicks=show_pkicks,
                show_bans=show_bans,
                show_pbans=show_pbans))

if len(clients) < 1:
    print('Not enough data!')
else:
    render_template()
