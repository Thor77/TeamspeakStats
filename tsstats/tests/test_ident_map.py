from tsstats.client import Clients

ident_map = {
    '1': '2',
    '5': '2',
    'UID1': 'UID2',
    'UID5': 'UID2'
}
clients = Clients(ident_map)


def test_get_id():
    assert clients['1'].identifier == '2'
    assert clients['5'].identifier == '2'


def test_get_uid():
    assert clients['UID1'].identifier == 'UID2'
    assert clients['UID5'].identifier == 'UID2'
