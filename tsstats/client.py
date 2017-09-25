# -*- coding: utf-8 -*-
import datetime
import logging
from collections import MutableMapping

logger = logging.getLogger('tsstats')


class Clients(MutableMapping):
    '''
    A high-level-interface to multiple Client-objects
    '''
    def __init__(self, ident_map=None, *args, **kwargs):
        '''
        Initialize a new Client-collection

        :param ident_map: Identity-map (see :doc:`identmap`)
        :type ident_map: dict
        '''
        self.ident_map = ident_map or {}

        self.store = dict()
        self.update(dict(*args, **kwargs))

    def apply_events(self, events):
        '''
        Apply events to this Client-collection

        :param events: list of events to apply
        :type events: list
        '''
        for event in events:
            # find corresponding client
            client = self.setdefault(
                event.identifier,
                Client(self.ident_map.get(event.identifier, event.identifier))
            )
            if event.action == 'set_nick':
                client.nick = event.arg
                continue
            if event.arg_is_client:
                # if arg is client, replace identifier with Client-obj
                event = event._replace(
                    arg=self.setdefault(event.arg, Client(event.arg))
                )
            client.__getattribute__(event.action)(event.arg)

    def __add__(self, client):
        '''
        Add a Client to the collection

        :param client: Client to add to the collection
        :type id_or_uid: Client
        '''
        identifier = client.identifier
        self.store[self.ident_map.get(identifier, identifier)] = client
        return self

    def __iter__(self):
        '''
        Yield all Client-objects from the collection
        '''
        return iter(self.store.keys())

    def __getitem__(self, key):
        return self.store[self.ident_map.get(key, key)]

    def __delitem__(self, key):
        del self.store[key]

    def __len__(self):
        return len(self.store)

    def __setitem__(self, key, value):
        self.store[self.ident_map.get(key, key)] = value

    def __str__(self):
        return str(list(map(str, self)))


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
        self._nick = nick
        self.nick_history = set()
        self.connected = 0
        self.onlinetime = datetime.timedelta()
        self.kicks = 0
        self.pkicks = 0
        self.bans = 0
        self.pbans = 0
        self.last_seen = None
        # private
        self._last_connect = 0

    @property
    def nick(self):
        return self._nick

    @nick.setter
    def nick(self, new_nick):
        if self._nick and new_nick != self._nick:
            # add old nick to history
            self.nick_history.add(self._nick)
        # set new nick
        self._nick = new_nick

    def connect(self, timestamp):
        '''
        Connect client at `timestamp`

        :param timestamp: time of connect
        :type timestamp: int
        '''
        logger.debug('[%s] CONNECT %s', timestamp, self)
        self.connected += 1
        self._last_connect = timestamp

    def disconnect(self, timestamp):
        '''
        Disconnect client at `timestamp`

        :param timestamp: time of disconnect
        :type timestamp: int
        '''
        logger.debug('[%s] DISCONNECT %s', timestamp, self)
        if not self.connected:
            logger.debug('^ disconnect before connect')
            return
        self.connected -= 1
        session_time = timestamp - self._last_connect
        logger.debug('Session lasted %s', session_time)
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
        return u'<{}, {}>'.format(self.identifier, self.nick)

    def __repr__(self):
        return self.__str__()
