from tsstats import parse_logs
from sys import stderr

clients = parse_logs('tests/res/test.log')


def test_length():
    assert len(clients.clients_by_id) == 2
    assert len(clients.clients_by_uid) == 1


def test_getter():
    # check getter not raise
    assert clients['UIDClient2'].onlinetime == 0


def test_parse_onlinetime():
    # check different dicts
    assert clients['1'].onlinetime == 402
    assert clients['2'].onlinetime == 20


def test_parse_kicks():
    assert clients['UIDClient1'].kicks == 1


def test_parse_pkicks():
    assert clients['2'].pkicks == 1


def test_parse_bans():
    assert clients['UIDClient1'].bans == 1


def test_parse_pbans():
    assert clients['2'].pbans == 1
