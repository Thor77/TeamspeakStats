Command Line Interface
======================

.. code-block:: console

    $ tsstats --help
    usage: tsstats [-h] [-c CONFIG] [--idmap IDMAP] [-l LOG] [-o OUTPUT] [-d]
                   [-ds] [-nod] [-t TEMPLATE] [-dtf DATETIMEFORMAT]
                   [-otth ONLINETIMETHRESHOLD]

    A simple Teamspeak stats-generator, based solely on server-logs

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
      -ds, --debugstdout    write debug output to stdout
      -nod, --noonlinedc    don't add connect until now to onlinetime
      -t TEMPLATE, --template TEMPLATE
                            path to custom template
      -dtf DATETIMEFORMAT, --datetimeformat DATETIMEFORMAT
                            format of date/time-values (datetime.strftime)
      -otth ONLINETIMETHRESHOLD, --onlinetimethreshold ONLINETIMETHRESHOLD
                            threshold for displaying onlinetime (in seconds)
