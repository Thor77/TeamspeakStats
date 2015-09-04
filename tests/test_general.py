from os import remove

from nose.tools import raises

from tsstats import exceptions, main, parse_logs

clients = parse_logs('tests/res/test.log')


def test_main():
    main(config_path='tests/res/config.ini')


@raises(exceptions.ConfigNotFound)
def test_main_config_not_found():
    main(config_path='/some/where/no/conf.ini')


def test_main_idmap_load():
    main(config_path='tests/res/config.ini',
         id_map_path='tests/res/id_map.json')


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


def test_client_repr():
    assert str(clients['1']) == '<1,Client1>'


def test_debug_log():
    clients = parse_logs('tests/res/test.log', file_log=True)
    open('debug.txt')
    remove('debug.txt')


@raises(exceptions.InvalidLog)
def test_parse_broken():
    clients = parse_logs('tests/res/test.log.broken')


def test_iter_clients():
    clients_length = len(clients.clients_by_id) + len(clients.clients_by_uid)
    clients_iter = [client for client in clients]
    assert len(clients_iter) == clients_length
