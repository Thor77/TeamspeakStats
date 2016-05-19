import pytest

from tsstats.client import Client, Clients

clients = Clients()
cl1 = Client('1')
cl2 = Client('2')
clients += cl1
clients += cl2
uidcl1 = Client('UID1')
uidcl2 = Client('UID2')
clients += uidcl1
clients += uidcl2


def test_client_get():
    assert clients['1'] == cl1
    assert clients['2'] == cl2
    assert clients['UID1'] == uidcl1
    assert clients['UID2'] == uidcl2
    with pytest.raises(KeyError):
        clients['3']
        clients['UID3']


def test_client_repr():
    assert str(clients['1']) == '<1,None>'
    assert str(clients['2']) == '<2,None>'
    assert str(clients['UID1']) == '<UID1,None>'
    assert str(clients['UID2']) == '<UID2,None>'


def test_clients_iter():
    client_list = list(iter(clients))
    assert cl1 in client_list
    assert cl2 in client_list
    assert uidcl1 in client_list
    assert uidcl2 in client_list
