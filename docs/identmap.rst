IdentMap
========

An IdentMap is used to map multiple (U)ID's of one client to one client.
This can be useful, if a user creates multiple identities and you want to summarize all actions from all identities.
To pass an IdentMap to TeamspeakStats, create your IdentMap as shown above and pass it to the cli::

  tsstats --idmap <path to idmap.json>

TeamspeakStats' IdentMap-file is saved in json-format::

  [
    {
      "primary_id": "1",
      "alternate_ids": ["2", "3", "4"]
    }
  ]

If you would pass this IdentMap to TeamspeakStats and your log would contain entries for clients with id's 1, 2, 3 and 4,
your output will just show data for one client (1).

The format is flexible enough to support other arbitrary data to assist you in maintaining your IdentMap::

  [
    {
      "name": "Friend 1",
      "primary_id": "1",
      "alternate_ids": ["2", "3", "4"]
    }
  ]

The parser will ignore all nodes other than the "primary_id" and "alternate_ids" nodes, allowing you to use them for whatever you want.

The original IdentMap format is still supported::

  {
    '2': '1',
    '3': '1',
    '4': '1'
  }

While it is less expressive, it is also less verbose.
