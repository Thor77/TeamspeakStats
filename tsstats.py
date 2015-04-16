import re
import sys
import configparser
from time import mktime
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
if 'General' not in config or not ('logfile' in config['General'] and 'outputfile' in config['General']):
    print('Invalid configuration!')
    import sys
    sys.exit()
log_path = config['General']['logfile']
output_path = config['General']['outputfile']

generation_start = datetime.now()
clients = {}  # clid: {'nick': ..., 'onlinetime': ..., 'kicks': ..., 'pkicks': ..., 'bans': ..., 'last_connect': ..., 'connected': ...}

cldata = re.compile(r"'(.*)'\(id:(\d*)\)")
cldata_ban = re.compile(r"by\ client\ '(.*)'\(id:(\d*)\)")
cldata_invoker = re.compile(r"invokerid=(\d*)\ invokername=(.*)\ invokeruid")


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


def add_kick(clid, nick):
    check_client(clid, nick)
    if 'kicks' in clients[clid]:
        clients[clid]['kicks'] += 1
    else:
        clients[clid]['kicks'] = 1


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


with open(log_path, 'r') as f:
    today = datetime.utcnow()
    for line in f:
        parts = line.split('|')
        logdatetime = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
        sid = int(parts[3].strip())
        data = '|'.join(parts[4:]).strip()
        if data.startswith('client'):
            r = cldata.findall(data)[0]
            nick = r[0]
            id = r[1]
            if data.startswith('client connected'):
                add_connect(id, nick, logdatetime)
            elif data.startswith('client disconnected'):
                add_disconnect(id, nick, logdatetime)
                if 'invokerid' in data:
                    add_pkick(id, nick)
                    r = cldata_invoker.findall(data)[0]
                    nick = r[1]
                    id = r[0]
                    add_kick(id, nick)
        elif data.startswith('ban added') and 'cluid' in data:
            r = cldata_ban.findall(data)[0]
            nick = r[0]
            id = r[1]
            add_ban(id, nick)

for clid in clients:
    if 'connected' not in clients[clid]:
        clients[clid]['connected'] = False
    if clients[clid]['connected']:
        add_disconnect(clid, clients[clid]['nick'], today, set_connected=False)


generation_end = datetime.now()
generation_delta = generation_end - generation_start


# helper functions
def desc(key):
    r = []
    values = {}
    for clid in clients:
        if key in clients[clid]:
            values[clid] = clients[clid][key]
    for clid in sorted(values, key=values.get, reverse=True):
        value = values[clid]
        r.append((clid, clients[clid]['nick'], value))
    return r


def render_template():
    arg = sys.argv[0]
    arg_find = arg.rfind('/')
    if arg_find == -1:
        path = '.'
    else:
        path = arg[:arg_find] + '/'

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

    with open(output_path, 'w+') as f:
        f.write(template.render(onlinetime=onlinetime_desc, kicks=desc('kicks'), pkicks=desc('pkicks'), bans=desc('bans'), seconds='{}.{}'.format(generation_delta.seconds, generation_delta.microseconds), date=generation_end.strftime('%d.%m.%Y um %H:%M')))

if len(clients) < 1:
    print('Not enough data!')
else:
    render_template()
