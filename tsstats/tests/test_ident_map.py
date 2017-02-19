import pytest

from tsstats.client import Client, Clients
from tsstats.utils import transform_pretty_identmap


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


@pytest.mark.parametrize('test_input,expected', [
    (
        [
            {'primary_id': '1', 'alternate_ids': ['3', '6']},
            {'primary_id': '4', 'alternate_ids': ['9', '42', '23']}
        ],
        (('3', '1'), ('6', '1'), ('9', '4'), ('42', '4'), ('23', '4'))
    ),
    (
        [
            {'name': 'Friend 1', 'primary_id': '2', 'alternate_ids': ['4']},
            {
                'name': 'Friend 3',
                'primary_id': '8',
                'alternate_ids': ['9', '14']
            }
        ],
        (('4', '2'), ('9', '8'), ('14', '8'))
    )
])
def test_transform_pretty_identmap(test_input, expected):
    transformed_identmap = transform_pretty_identmap(test_input)
    for alternate, primary in expected:
        assert transformed_identmap[alternate] == primary
