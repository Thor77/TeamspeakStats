# TeamspeakStats
A simple Teamspeak stat-generator - based on server-logs

# Usage
Run `tsstats.py` and point your web-server to the generated .html-file, now you will see some stats for your Teamspeak-Server parsed from the logs.

# Configuration

###Configname
`config.ini`
###Sections
`[General]`
### Keys
- title `HTMl-Title`
- logfile `Path to TS3Server-logfile`
- outputfile `Path to the location, where the generator will put the generated .html-file`

## Example
```
[General]
title = TeamspeakStats
logfile = /usr/local/bin/teamspeak-server/logs/ts3server_2015-03-02__14_01_43.110983_1.log
outputfile = /var/www/html/stats.html
```

# TODO
- Localization
