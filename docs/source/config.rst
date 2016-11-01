Config
******
The configfile is using the .ini-format.
Currently all settings are read from the ``[General]``-section.

+--------+----------------+
| Key    | Description    |
+========+================+
| log    | Path to        |
|        | TS3Server-logf |
|        | ile(s)         |
|        | (supports      |
|        | `globbing <htt |
|        | ps://docs.pyth |
|        | on.org/3/libra |
|        | ry/glob.html>` |
|        | __)            |
+--------+----------------+
| output | Path to the    |
|        | location,      |
|        | where the      |
|        | generator will |
|        | put the        |
|        | generated      |
|        | ``.html``-file |
+--------+----------------+
| idmap  | Path to        |
|        | `IdentMap <htt |
|        | p://teamspeaks |
|        | tats.readthedo |
|        | cs.io/en/lates |
|        | t/identmap.htm |
|        | l>`__          |
+--------+----------------+
| debug  | debug mode     |
+--------+----------------+
| online | Add timedelta  |
| dc     | from           |
|        | last-connect   |
|        | until now to   |
|        | onlinetime for |
|        | connected      |
|        | clients        |
+--------+----------------+
| templa | Path to a      |
| te     | custom         |
|        | template file  |
|        | (relative from |
|        | ``tsstats/``   |
|        | or absolute)   |
+--------+----------------+
| dateti | Format of      |
| meform | date/time-valu |
| at     | es             |
|        | used for       |
|        | render-timesta |
|        | mp             |
|        | and last       |
|        | online (using  |
|        | `datetime.strf |
|        | time <https:// |
|        | docs.python.or |
|        | g/3/library/da |
|        | tetime.html#st |
|        | rftime-strptim |
|        | e-behavior>`__ |
|        | )              |
+--------+----------------+
