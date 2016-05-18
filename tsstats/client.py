import logging

from tsstats.exceptions import InvalidLog

logger = logging.getLogger('tsstats')


class Clients(object):
    '''
    Clients provides high-level-access to multiple Client-objects
    '''

    def __init__(self, ident_map={}):
        '''
        Initialize a new Client-collection

        :param ident_map: Identity-map (see :ref:`IdentMap`)
        :type ident_map: dict
        '''
        self.clients_by_id = {}
        self.clients_by_uid = {}
        self.ident_map = ident_map

    def is_id(self, id_or_uid):
        try:
            int(id_or_uid)
            return True
        except ValueError:
            return False

    def __add__(self, id_or_uid):
        '''
        Add a Client to the collection

        :param id_or_uid: id or uid of the Client
        :type id_or_uid: int or str
        '''
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self.clients_by_id[id_or_uid] = Client(id_or_uid)
        else:
            if id_or_uid not in self.clients_by_uid:
                self.clients_by_uid[id_or_uid] = Client(id_or_uid)
        return self

    def __getitem__(self, id_or_uid):
        '''
        Get a Client from the collection

        :param id_or_uid: id or uid of the Client
        :type id_or_uid: int or str
        '''
        if id_or_uid in self.ident_map:
            id_or_uid = self.ident_map[id_or_uid]
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self += id_or_uid
            return self.clients_by_id[id_or_uid]
        else:
            if id_or_uid not in self.clients_by_uid:
                self += id_or_uid
            return self.clients_by_uid[id_or_uid]

    def __iter__(self):
        '''
        Yield all Client-objects from the collection

        clients by uid following clients by id
        '''
        for id_client in self.clients_by_id.values():
            yield id_client
        for uid_client in self.clients_by_uid.values():
            yield uid_client


class Client(object):
    '''
    Client provides high-level-access to a Teamspeak-Client
    '''

    def __init__(self, identifier):
        '''
        Initialize a new Client

        :param identifier: Identifier of the client
        :type identifier: int or str
        '''
        # public
        self.identifier = identifier
        self.nick = None
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
        return {
            'identifier': self.identifier,
            'nick': self.nick,
            'connected': self.connected,
            'onlinetime': self.onlinetime,
            'kicks': self.kicks,
            'pkicks': self.pkicks,
            'bans': self.bans,
            'pbans': self.pbans,
        }[item]
