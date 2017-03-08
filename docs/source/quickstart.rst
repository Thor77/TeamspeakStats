Quickstart
**********
First, you have to get and install a decent version of `Python <https://python.org/>`_ (at least 2.7).
Now you have various options to use TeamspeakStats, going from easy to hard:

1. Install the tool via pip ``pip install tsstats``
2. Clone the sourcecode ``git clone https://github.com/Thor77/TeamspeakStats``

  * **A** Just run the script from your local copy ``python -m tsstats``
  * **B** Install the script with the included *setup.py* ``python setup.py install``

To start, you can just use cli-arguments to control the behaviour of TeamspeakStats::

  usage: tsstats [-h] [-c CONFIG] [--idmap IDMAP] [-l LOG] [-o OUTPUT] [-d]
                     [-nod]

  A simple Teamspeak stats-generator - based on server-logs

  optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                          path to config
    --idmap IDMAP         path to id_map
    -l LOG, --log LOG     path to your logfile(s). pass a directory to use all
                          logfiles inside it
    -o OUTPUT, --output OUTPUT
                          path to the output-file
    -d, --debug           debug mode
    -nod, --noonlinedc    don't add connect until now to onlinetime
    -t TEMPLATE, --template TEMPLATE
                          path to custom template
    -dtf DATETIMEFORMAT, --datetimeformat DATETIMEFORMAT
                          format of date/time-values (datetime.strftime)

Take a look at :doc:`cli` to get a more in-depth explanation of the available flags.
If you want to use TeamspeakStats in a script (or cron) you should consider creating
a :doc:`config`.
