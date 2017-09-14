import pytest

from tsstats.client import Client, Clients


@pytest.fixture(scope='module')
def clients():
    clients = Clients()
    cl1 = Client('1')
    cl2 = Client('2')
    clients += cl1
    clients += cl2
    uidcl1 = Client('UID1')
    uidcl2 = Client('UID2')
    clients += uidcl1
    clients += uidcl2
    return (clients, cl1, cl2, uidcl1, uidcl2)


def test_client_get(clients):
    clients, cl1, cl2, uidcl1, uidcl2 = clients
    assert clients['1'] == cl1
    assert clients['2'] == cl2
    assert clients['UID1'] == uidcl1
    assert clients['UID2'] == uidcl2
    with pytest.raises(KeyError):
        clients['3']
        clients['UID3']


def test_client_repr(clients):
    clients, _, _, _, _ = clients
    assert str(clients['1']) == '<1, None>'
    assert str(clients['2']) == '<2, None>'
    assert str(clients['UID1']) == '<UID1, None>'
    assert str(clients['UID2']) == '<UID2, None>'
    assert str(clients) == \
        "['<1, None>', '<2, None>', '<UID2, None>', '<UID1, None>']"


def test_client_nick(clients):
    _, cl1, _, _, _ = clients
    assert cl1.nick is None
    assert not cl1.nick_history
    cl1.nick = 'Client1'
    assert cl1.nick == 'Client1'
    assert None not in cl1.nick_history
    cl1.nick = 'NewClient1'
    assert cl1.nick == 'NewClient1'
    assert 'Client1' in cl1.nick_history


def test_clients_iter(clients):
    clients, cl1, cl2, uidcl1, uidcl2 = clients
    client_list = list(iter(clients))
    assert cl1 in client_list
    assert cl2 in client_list
    assert uidcl1 in client_list
    assert uidcl2 in client_list


def test_clients_delete(clients):
    clients, cl1, _, _, _ = clients
    del clients['1']
    assert cl1 not in clients
