from time import sleep

import pytest

from tsstats.exceptions import InvalidLog
from tsstats.log import parse_log, parse_logs

testlog_path = 'tsstats/tests/res/test.log'


@pytest.fixture
def clients():
    return parse_log(testlog_path)


def test_log_client_count(clients):
    assert len(clients) == 3


def test_log_onlinetime(clients):
    assert clients['1'].onlinetime == 402
    assert clients['2'].onlinetime == 20


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
    assert len(parse_log(testlog_path)) == \
        len(parse_logs(testlog_path))


@pytest.mark.slowtest
def test_log_client_online():
    clients = parse_log(testlog_path)
    assert clients['1'].onlinetime == 402
    sleep(2)
    clients = parse_log(testlog_path)
    assert clients['1'].onlinetime == 404
