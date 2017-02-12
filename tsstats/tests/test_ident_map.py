import pytest

from tsstats.client import Client, Clients


@pytest.fixture(scope='module')
def identmap_clients():
    clients = Clients({
            '1': '2',
            '5': '2',
            'UID1': 'UID2',
            'UID5': 'UID2'
    })
    cl = Client('2', 'Client2')
    uidcl = Client('UID2', 'Client2++')
    clients += cl
    clients += uidcl
    return (clients, cl, uidcl)


def test_ident_map(identmap_clients):
    clients, cl, uidcl = identmap_clients
    assert clients['1'] == cl
    assert clients['5'] == cl
    assert clients['UID1'] == uidcl
    assert clients['UID5'] == uidcl
