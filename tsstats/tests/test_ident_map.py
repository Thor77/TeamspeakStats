from tsstats.client import Client, Clients

ident_map = {
    '1': '2',
    '5': '2',
    'UID1': 'UID2',
    'UID5': 'UID2'
}
clients = Clients(ident_map)
cl = Client('2', 'Client2')
uidcl = Client('UID2', 'Client2++')
clients += cl
clients += uidcl


def test_ident_map():
    assert clients['1'] == cl
    assert clients['5'] == cl
    assert clients['UID1'] == uidcl
    assert clients['UID5'] == uidcl
