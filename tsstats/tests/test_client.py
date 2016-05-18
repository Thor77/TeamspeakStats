from tsstats.client import Clients

clients = Clients()
clients += 1
clients += 2
clients += 'UID1'
clients += 'UID2'


def test_client_get():
    '''
    Currently not testable because of tsstats.client.Clients add-behaviour
    '''
    pass


def test_client_seperation():
    assert len(clients.clients_by_id) == 2
    assert len(clients.clients_by_uid) == 2


def test_client_repr():
    assert str(clients['1']) == '<1,None>'
    assert str(clients['2']) == '<2,None>'
    assert str(clients['UID1']) == '<UID1,None>'
    assert str(clients['UID2']) == '<UID2,None>'


def test_clients_iter():
    clients_length = len(clients.clients_by_id) + len(clients.clients_by_uid)
    clients_iter = [client for client in clients]
    assert len(clients_iter) == clients_length
