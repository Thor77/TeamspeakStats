# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import pickle
from collections import MutableMapping, namedtuple

logger = logging.getLogger('tsstats')
CachedLog = namedtuple('CachedLog', ['path', 'hash', 'events'])


def _calculate_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class Cache(MutableMapping):
    def __init__(self, path, data={}):
        self.path = path
        self.store = data
        self.initial_store_version = self.store.setdefault('version', 0)

    @classmethod
    def read(cls, path):
        data = {}
        if os.path.exists(path):
            logger.debug('Reading cache from %s', path)
            with open(path, 'rb') as f:
                try:
                    data = pickle.load(f)
                except EOFError:
                    logger.debug('Couldn\'t read cache')
        return cls(path, data)

    def write(self, path=None):
        if not path:
            path = self.path
        if self.initial_store_version == self.store['version']:
            logger.debug('Cached content did not change, skipping write')
            return
        logger.debug('Writing cache to %s', path)
        with open(path, 'wb') as f:
            pickle.dump(self.store, f)

    def needs_parsing(self, path):
        if path not in self.store:
            return True
        return _calculate_hash(path) != self.store[path].hash

    def __setitem__(self, path, events):
        self.store[path] = CachedLog(path, _calculate_hash(path), list(events))
        self.store['version'] += 1

    def __getitem__(self, path):
        return self.store[path]

    def __delitem__(self, path):
        del self.store[path]

    def __iter__(self):
        return iter(self.store.keys())

    def __len__(self):
        return len(self.store)
