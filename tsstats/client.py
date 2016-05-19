import logging

from tsstats.exceptions import InvalidLog
from collections import MutableMapping

logger = logging.getLogger('tsstats')


class Clients(MutableMapping):
    '''
    A high-level-interface to multiple Client-objects
    '''
    def __init__(self, ident_map=None, *args, **kwargs):
        '''
        Initialize a new Client-collection

        :param ident_map: Identity-map (see :ref:`IdentMap`)
        :type ident_map: dict
        '''
        self.ident_map = ident_map or {}

        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __add__(self, client):
        '''
        Add a Client to the collection

        :param client: Client to add to the collection
        :type id_or_uid: Client
        '''
        self.store[client.identifier] = client
        return self

    def __iter__(self):
        '''
        Yield all Client-objects from the collection
        '''
        return iter(self.store.values())

    def __getitem__(self, key):
        return self.store[self.ident_map.get(key, key)]

    def __delitem__(self, key):
        del self.store[key]

    def __len__(self):
        return len(self.store)

    def __setitem__(self, key, value):
        key = self.ident_map.get(key, key)
        self.store[key] = value


class Client(object):
    '''
    Client provides high-level-access to a Teamspeak-Client
    '''

    def __init__(self, identifier, nick=None):
        '''
        Initialize a new Client

        :param identifier: Identifier of the client
        :type identifier: int or str
        '''
        # public
        self.identifier = identifier
        self.nick = nick
        self.connected = 0
        self.onlinetime = 0
        self.kicks = 0
        self.pkicks = 0
        self.bans = 0
        self.pbans = 0
        self.last_seen = 0
        # private
        self._last_connect = 0

    def connect(self, timestamp):
        '''
        Connect client at `timestamp`

        :param timestamp: time of connect
        :type timestamp: int
        '''
        logger.debug('CONNECT %s', self)
        self.connected += 1
        self._last_connect = timestamp

    def disconnect(self, timestamp):
        '''
        Disconnect client at `timestamp`

        :param timestamp: time of disconnect
        :type timestamp: int
        '''
        logger.debug('DISCONNECT %s', self)
        if not self.connected:
            logger.debug('^ disconnect before connect')
            raise InvalidLog('disconnect before connect!')
        self.connected -= 1
        session_time = timestamp - self._last_connect
        self.onlinetime += session_time
        self.last_seen = timestamp

    def kick(self, target):
        '''
        Let client kick `target`

        :param target: client to kick
        :type target: Client
        '''
        logger.debug('KICK %s -> %s', self, target)
        target.pkicks += 1
        self.kicks += 1

    def ban(self, target):
        '''
        Let client ban `target`

        :param target: client to ban
        :type target: Client
        '''
        logger.debug('BAN %s -> %s', self, target)
        target.pbans += 1
        self.bans += 1

    def __str__(self):
        return '<{},{}>'.format(self.identifier, self.nick)

    def __getitem__(self, item):
        return self.__getattribute__(item)
