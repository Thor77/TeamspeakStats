# TeamspeakStats [![Build Status](https://travis-ci.org/Thor77/TeamspeakStats.svg?branch=master)](https://travis-ci.org/Thor77/TeamspeakStats) [![Coverage Status](https://coveralls.io/repos/Thor77/TeamspeakStats/badge.svg?branch=master&service=github)](https://coveralls.io/github/Thor77/TeamspeakStats?branch=master) [![Code Health](https://landscape.io/github/Thor77/TeamspeakStats/master/landscape.svg?style=flat)](https://landscape.io/github/Thor77/TeamspeakStats/master) [![PyPI](https://img.shields.io/pypi/v/tsstats.svg)](https://pypi.python.org/pypi/tsstats) [![Documentation Status](https://readthedocs.org/projects/teamspeakstats/badge/?version=latest)](http://teamspeakstats.readthedocs.io/en/latest/?badge=latest)
A simple Teamspeak stat-generator - based on server-logs

![screenshot](screenshot.png)

# Installation
- Install the package via PyPi `pip install tsstats`
- Clone this repo `git clone https://github.com/Thor77/TeamspeakStats` and install with `python setup.py install`
- Just use the package as is via `python -m tsstats [-h]`

# Usage
- Create a config (see [Configuration](https://github.com/Thor77/TeamspeakStats#configuration))
- Run the script `tsstats [-h]`

# CMD-Arguments
```
usage: tsstats [-h] [-c CONFIG] [--idmap IDMAP] [-l LOG] [-o OUTPUT] [-d]
                   [-nod]

A simple Teamspeak stats-generator - based on server-logs

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to config
  --idmap IDMAP         path to id_map
  -l LOG, --log LOG     path to your logfile(s)
  -o OUTPUT, --output OUTPUT
                        path to the output-file
  -d, --debug           debug mode
  -nod, --noonlinedc    don't add connect until now to onlinetime
  -t TEMPLATE, --template TEMPLATE
                        path to custom template
  -dtf DATETIMEFORMAT, --datetimeformat DATETIMEFORMAT
                        format of date/time-values (datetime.strftime)
```

# Configuration

#### [General]
| Key | Description |
|-----|-------------|
| log | Path to TS3Server-logfile(s) (supports [globbing](https://docs.python.org/3/library/glob.html)) |
| output | Path to the location, where the generator will put the generated `.html`-file |
| idmap | Path to [IdentMap](http://teamspeakstats.readthedocs.io/en/latest/identmap.html) |
| debug | debug mode |
| onlinedc | Add timedelta from last-connect until now to onlinetime for connected clients |
| template | Path to a custom template file (relative from `tsstats/` or absolute) |
| datetimeformat | Format of date/time-values used for render-timestamp and last online (using [datetime.strftime](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)) |


## Example
```
[General]
log = /usr/local/bin/teamspeak-server/logs/ts3server*_1.log
output = /var/www/html/stats.html
```

# ID-Mapping
`id_map.json`  
You can map multiple ID's to one (for example, when an user creates a new identity)
## Example
```json
{
	"1": "2",
	"3": "2"
}
```
The online-time of `1` and `3` will be added to the online-time of `2`

# Contributing
Please make sure tests are succeeding and your code follows [flake8](https://flake8.readthedocs.io)-guidelines.

## Run tests
- Install testing-requirements `pip install -r testing_requirements.txt`
- Run `py.test tsstats/`

# TODO
- Localization
