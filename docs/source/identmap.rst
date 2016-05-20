IdentMap
********
An IdentMap is used to map multiple (U)ID's of one client to one client.
This can be useful, if a user creates multiple identities and you want to summarize all actions from all identities.

TeamspeakStats' IdentMap-file is saved in json-format::

  {
    '2': '1',
    '3': '1',
    '4': '1'
  }


If you would pass this IdentMap to TeamspeakStats and your log would contain entries for clients with id's 1, 2, 3 and 4,
your output will just show data for one client (1).

To pass an IdentMap to TeamspeakStats, create your IdentMap as shown above and pass it to the cli::

  tsstats --idmap <path to idmap.json>
