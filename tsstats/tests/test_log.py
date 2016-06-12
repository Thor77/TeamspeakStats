from datetime import timedelta
from time import sleep

import pytest

from tsstats.exceptions import InvalidLog
from tsstats.log import parse_log, parse_logs

testlog_path = 'tsstats/tests/res/test.log'


@pytest.fixture
def clients():
    return parse_log(testlog_path, online_dc=False)


def test_log_client_count(clients):
    assert len(clients) == 3


def test_log_onlinetime(clients):
    assert clients['1'].onlinetime == timedelta(0, 402, 149208)
    assert clients['2'].onlinetime == timedelta(0, 19, 759644)


def test_log_kicks(clients):
    assert clients['UIDClient1'].kicks == 1


def test_log_pkicks(clients):
    assert clients['2'].pkicks == 1


def test_log_bans(clients):
    assert clients['UIDClient1'].bans == 1


def test_log_pbans(clients):
    assert clients['2'].pbans == 1


def test_log_invalid():
    with pytest.raises(InvalidLog):
        parse_log('tsstats/tests/res/test.log.broken')


def test_log_multiple():
    assert len(parse_log(testlog_path, online_dc=False)) == \
        len(parse_logs(testlog_path, online_dc=False))


@pytest.mark.slowtest
def test_log_client_online():
    clients = parse_log(testlog_path)
    old_onlinetime = int(clients['1'].onlinetime.total_seconds())
    sleep(2)
    clients = parse_log(testlog_path)
    assert int(clients['1'].onlinetime.total_seconds()) == old_onlinetime + 2
