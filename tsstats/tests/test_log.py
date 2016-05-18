import pytest
from tsstats.log import parse_logs


@pytest.fixture
def clients():
    return parse_logs('tsstats/tests/res/test.log')


def test_log_client_count(clients):
    assert len(clients.clients_by_id) == 2
    assert len(clients.clients_by_uid) == 1


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
