import re
import configparser
from time import mktime
from datetime import datetime, timedelta
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


def add_disconnect(clid, nick, logdatetime):
    check_client(clid, nick)
    connect = datetime.fromtimestamp(clients[clid]['last_connect'])
    delta = logdatetime - connect
    minutes = delta.seconds // 60
    increase_onlinetime(clid, minutes)
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
        add_disconnect(clid, clients[clid]['nick'], today)


# helper functions
def desc(key):
    r = []
    values = {}
    for clid in clients:
        if key in clients[clid]:
            values[clid] = clients[clid][key]
    for clid in sorted(values, key=values.get, reverse=True):
        value = values[clid]
        r.append((clients[clid]['nick'], value))
    return r


#################
# Generate HTML #
#################
output = []
# head
output.append('''
<html>
    <head>
        <title>TeamspeakStats</title>
        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
        <style>
        h1 {text-align: center;}
        </style>
<!-- Piwik -->
<script type="text/javascript">
  var _paq = _paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="//analytics.crapwa.re/";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', 1]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="//analytics.crapwa.re/piwik.php?idsite=1" style="border:0;" alt="" /></p></noscript>
<!-- End Piwik Code -->
    </head>
    <body>
''')
# body
if len(clients) < 1:
    print('No clients found!')
    print('Keine Daten gefunden!')
    import sys
    sys.exit()

onlinetime_desc = desc('onlinetime')
if len(onlinetime_desc) >= 1:
    output.append('<h1>Onlinezeit</h1>')
    output.append('<ul class="list-group">')
    colored_class = False
    for nick, onlinetime in onlinetime_desc:
        if onlinetime > 60:
            onlinetime_str = str(onlinetime // 60) + 'h'
            m = onlinetime % 60
            if m > 0:
                onlinetime_str += ' ' + str(m) + 'm'
        else:
            onlinetime_str = str(onlinetime) + 'm'
        colored = ''
        if colored_class:
            colored = ' style="background-color: #eee"'
        output.append('<li class="list-group-item"{}><span class="badge">{}</span>{}</li>'.format(colored, onlinetime_str, nick))
        colored_class = not colored_class
    output.append('</ul>')

kicks_desc = desc('kicks')
if len(kicks_desc) >= 1:
    output.append('<h1>Kicks</h1>')
    output.append('<ul class="list-group">')
    for nick, kicks in kicks_desc:
        output.append('<li class="list-group-item"><span class="badge">{}</span>{}</li>'.format(kicks, nick))
    output.append('</ul>')

pkicks_desc = desc('pkicks')
if len(pkicks_desc) >= 1:
    output.append('<h1>Gekickt worden</h1>')
    output.append('<ul class="list-group">')
    for nick, pkicks in pkicks_desc:
        output.append('<li class="list-group-item"><span class="badge">{}</span>{}</li>'.format(pkicks, nick))
    output.append('</ul>')

bans_desc = desc('bans')
if len(bans_desc) >= 1:
    output.append('<h1>Bans</h1>')
    output.append('<ul class="list-group">')
    for nick, bans in pkicks_desc:
        output.append('<li class="list-group-item"><span class="badge">{}</span>{}</li>'.format(bans, nick))
    output.append('</ul>')

generation_end = datetime.now()
generation_delta = generation_end - generation_start
output.append('<p style="text-align: center">generiert in {}.{} Sekunden am {}</p>'.format(generation_delta.seconds, generation_delta.microseconds, generation_end.strftime('%d.%m.%Y um %H:%M')))
output.append('</body></html>')

with open(output_path, 'w+') as f:
    f.write('\n'.join(output))
