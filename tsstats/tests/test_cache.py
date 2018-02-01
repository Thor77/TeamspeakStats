# -*- coding: utf-8 -*-
import os


import shutil

import pytest

from tsstats.cache import Cache, CachedLog, _calculate_hash
from tsstats.log import parse_logs
from tsstats.tests.test_log import testlog_path


@pytest.fixture
def cache_path(request):
    cache_path = 'tsstats/tests/res/tsstats.cache'

    def clean():
        if os.path.exists(cache_path):
            os.remove(cache_path)

    request.addfinalizer(clean)
    yield cache_path


@pytest.fixture
def cache(cache_path):
    return Cache(cache_path)


# UNIT
def test_cache_add_get_remove_iter_len(cache):
    expected_cachedlog = CachedLog(
        testlog_path, _calculate_hash(testlog_path), []
    )
    cache[testlog_path] = []
    assert cache.store[testlog_path] == expected_cachedlog
    assert cache[testlog_path] == expected_cachedlog
    assert next(iter(cache)) == testlog_path
    assert len(cache) == 1
    del cache[testlog_path]
    assert len(cache) == 0


def test_cache_read_write(cache):
    cache[testlog_path] = []
    cache.write()
    cache2 = Cache.read(cache.path)
    assert cache2[testlog_path] == CachedLog(
        testlog_path, _calculate_hash(testlog_path), []
    )


def test_cache_needs_parsing(cache, tmpdir):
    tmplog_path = str(tmpdir.mkdir('cache').join('test.log'))
    # copy logfile to temporary location
    shutil.copy(testlog_path, tmplog_path)

    assert cache.needs_parsing(tmplog_path)
    cache[tmplog_path] = []
    assert not cache.needs_parsing(tmplog_path)
    with open(tmplog_path, 'a') as f:
        f.writelines(['content'])
    assert cache.needs_parsing(tmplog_path)


# INTEGRATION
def test_cache_integration(cache_path):
    assert next(parse_logs(testlog_path, online_dc=False)) == \
        next(parse_logs(testlog_path, online_dc=False, cache_path=cache_path))
