# TeamspeakStats [![Build Status](https://drone.io/github.com/Thor77/TeamspeakStats/status.png)](https://drone.io/github.com/Thor77/TeamspeakStats/latest)
A simple Teamspeak stat-generator - based on server-logs

# Installation
- Install [Python](https://python.org)
- Clone this repo `git clone https://github.com/Thor77/TeamspeakStats`
- Install requirements `pip3 install -r requirements.txt`

# Usage
Run `tsstats.py` and point your web-server to the generated .html-file, now you will see some stats for your Teamspeak-Server parsed from the logs.

# Tests
- Install nose `pip3 install nose`
- Run `nosetests`

# Configuration

###Configname
`config.ini`
#### Keys
`[General]`
- logpath `Path to TS3Server-logfile` (supports [globbing](https://docs.python.org/3/library/glob.html))
- outputfile `Path to the location, where the generator will put the generated .html-file`
- debug `Enable debug-mode`
- debugfile `Enable debug-log to file`  

`[HTML]`
- title `HTML-Title`


## Example
```
[General]
logfile = /usr/local/bin/teamspeak-server/logs/ts3server*_1.log
outputfile = /var/www/html/stats.html
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

# TODO
- Localization
