from os import remove

import pytest

from tsstats import exceptions
from tsstats.__main__ import main
from tsstats.log import parse_logs

clients = parse_logs('tsstats/tests/res/test.log')


@pytest.fixture
def output(request):
    def clean():
        remove('tsstats/tests/res/output.html')
    request.addfinalizer(clean)


def test_main(output):
    main(config_path='tsstats/tests/res/config.ini')


def test_main_config_not_found():
    with pytest.raises(exceptions.ConfigNotFound):
        main(config_path='/some/where/no/conf.ini')


def test_main_idmap_load(output):
    main(config_path='tsstats/tests/res/config.ini',
         id_map_path='tsstats/tests/res/id_map.json')


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
    parse_logs('tsstats/tests/res/test.log', file_log=True)
    open('debug.txt')
    remove('debug.txt')


def test_parse_broken():
    with pytest.raises(exceptions.InvalidLog):
        parse_logs('tsstats/tests/res/test.log.broken')


def test_iter_clients():
    clients_length = len(clients.clients_by_id) + len(clients.clients_by_uid)
    clients_iter = [client for client in clients]
    assert len(clients_iter) == clients_length
