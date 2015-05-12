# TeamspeakStats
A simple Teamspeak stat-generator - based on server-logs

# Usage
Run `tsstats.py` and point your web-server to the generated .html-file, now you will see some stats for your Teamspeak-Server parsed from the logs.

# Configuration

###Configname
`config.ini`
#### Keys
`[General]`
- logfile `Path to TS3Server-logfile`
- outputfile `Path to the location, where the generator will put the generated .html-file`
`[HTML]`
- title `HTML-Title`
- onlinetime `Show the onlinetime-section (default=True)`
- kicks `Show the kicks-section (default=True)`
- pkicks `Show the passive-kicks-section (default=True)`
- bans `Show the bans-section (default=True)`

## Example
```
[General]
logfile = /usr/local/bin/teamspeak-server/logs/ts3server_2015-03-02__14_01_43.110983_1.log
outputfile = /var/www/html/stats.html
[HTML]
title = TeamspeakStats
bans = False
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
- find a better way to count kicks and bans
