TeamspeakStats |Build Status| |Build status| |Coverage Status| |Code Health| |PyPI| |Documentation Status|
==========================================================================================================

A simple Teamspeak stat-generator - based solely on server-logs

|screenshot|

Installation
============

-  Install the package via PyPi ``pip install tsstats``
-  Clone this repo
   ``git clone https://github.com/Thor77/TeamspeakStats`` and install
   with ``python setup.py install``
-  Just use the package as is via ``python -m tsstats [-h]``

Usage
=====

-  Run the script ``tsstats [-h]``
-  Optionally create a config-file (see
   `Configuration <https://teamspeakstats.readthedocs.io/en/latest/config.html>`__)
-  The package works entirely off your Teamspeak server's logs, so that
   no ServerQuery account is necessary

Example
=======

::

    tsstats -l /var/log/teamspeak3-server/ -o /var/www/tsstats.html

Parse logs in ``/var/log/teamspeak3-server`` and write output to ``/var/www/tsstats.html``.

For more details checkout the `documentation <http://teamspeakstats.readthedocs.io/en/latest/>`__!

.. |screenshot| image:: https://raw.githubusercontent.com/Thor77/TeamspeakStats/master/screenshot.png
.. |Build Status| image:: https://travis-ci.org/Thor77/TeamspeakStats.svg?branch=master
   :target: https://travis-ci.org/Thor77/TeamspeakStats
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/u9cx7krwmmevbvl2/branch/master?svg=true
   :target: https://ci.appveyor.com/project/Thor77/teamspeakstats
.. |Coverage Status| image:: https://coveralls.io/repos/Thor77/TeamspeakStats/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/Thor77/TeamspeakStats?branch=master
.. |Code Health| image:: https://landscape.io/github/Thor77/TeamspeakStats/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Thor77/TeamspeakStats/master
.. |PyPI| image:: https://img.shields.io/pypi/v/tsstats.svg
   :target: https://pypi.python.org/pypi/tsstats
.. |Documentation Status| image:: https://readthedocs.org/projects/teamspeakstats/badge/?version=latest
   :target: http://teamspeakstats.readthedocs.io/en/latest/?badge=latest
