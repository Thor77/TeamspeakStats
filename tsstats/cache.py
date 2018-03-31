# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import pickle
from collections import MutableMapping, namedtuple

logger = logging.getLogger('tsstats')
CachedLog = namedtuple('CachedLog', ['path', 'hash', 'events'])


def _calculate_hash(path):
    '''
    Calculate hash of a file using sha256

    :param path: path to file
    :type path: str

    :return: hash of the file
    :rtype: str
    '''
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class Cache(MutableMapping):
    '''
    Cache for parsed events from a logfile
    '''
    def __init__(self, path, data={}):
        '''
        Initialize Cache at `path`

        :param path: path to cache file
        :param data: initial cached data

        :type path: str
        :type data: dict
        '''
        self.path = path
        self.store = data
        self.initial_store_version = self.store.setdefault('version', 0)

    @classmethod
    def read(cls, path):
        '''
        Create a new Cache-instance with data read from `path`

        :param path: path to cache file
        :type path: str

        :return: Cache-instance with data from `path`
        :rtype: tsstats.cache.Cache
        '''
        data = {}
        if os.path.exists(path):
            logger.debug('Reading cache from %s', path)
            with open(path, 'rb') as f:
                try:
                    data = pickle.load(f)
                except (EOFError, pickle.UnpicklingError, KeyError):
                    logger.warning('Couldn\'t read cache')
        return cls(path, data)

    def write(self, path=None):
        '''
        Dump cache to `path`

        but only if there were any changes, if not, it will silently skip
        writing

        :param path: path to cache file
        :type path: str
        '''
        if not path:
            path = self.path
        if self.initial_store_version == self.store['version']:
            logger.debug('Cached content did not change, skipping write')
            return
        logger.debug('Writing cache to %s', path)
        with open(path, 'wb') as f:
            pickle.dump(self.store, f)

    def needs_parsing(self, path):
        '''
        Determine if a logfile needs parsing (=> is not cached or was updated)

        :param path: path to logfile
        :type path: str

        :return: if parsing is necessary for logfile at `path`
        :rtype: bool
        '''
        if path not in self.store:
            return True
        return _calculate_hash(path) != self.store[path].hash

    @property
    def cached_files(self):
        store_keys = list(self.store.keys())
        store_keys.remove('version')
        return store_keys

    def __setitem__(self, path, events):
        self.store[path] = CachedLog(path, _calculate_hash(path), list(events))
        self.store['version'] += 1

    def __getitem__(self, path):
        return self.store[path]

    def __delitem__(self, path):
        del self.store[path]

    def __iter__(self):
        return iter(self.cached_files)

    def __len__(self):
        return len(self.cached_files)
