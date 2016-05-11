import logging

from tsstats.exceptions import InvalidLog

logger = logging.getLogger('tsstats')


class Clients(object):

    def __init__(self, ident_map={}):
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
        if self.is_id(id_or_uid):
            if id_or_uid not in self.clients_by_id:
                self.clients_by_id[id_or_uid] = Client(id_or_uid)
        else:
            if id_or_uid not in self.clients_by_uid:
                self.clients_by_uid[id_or_uid] = Client(id_or_uid)
        return self

    def __getitem__(self, id_or_uid):
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
        for id_client in self.clients_by_id.values():
            yield id_client
        for uid_client in self.clients_by_uid.values():
            yield uid_client


class Client(object):

    def __init__(self, identifier):
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
        client connects at "timestamp"
        '''
        logger.debug('CONNECT %s', self)
        self.connected += 1
        self._last_connect = timestamp

    def disconnect(self, timestamp):
        '''
        client disconnects at "timestamp"
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
        client kicks "target" (Client-obj)
        '''
        logger.debug('KICK %s -> %s', self, target)
        target.pkicks += 1
        self.kicks += 1

    def ban(self, target):
        '''
        client bans "target" (Client-obj)
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
