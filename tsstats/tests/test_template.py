import logging
from datetime import timedelta
from os import remove

import pytest
from bs4 import BeautifulSoup

from tsstats.log import Server, _parse_details
from tsstats.template import render_servers
from tsstats.utils import filter_threshold, seconds_to_text, sort_clients

output_path = 'tsstats/tests/res/output.html'
clients = _parse_details('tsstats/tests/res/test.log', online_dc=False)
servers = [Server(1, clients)]

logger = logging.getLogger('tsstats')


@pytest.fixture
def output(request):
    def clean():
        remove(output_path)
    request.addfinalizer(clean)


@pytest.fixture
def soup(output):
    render_servers(servers, output_path)
    return BeautifulSoup(open(output_path), 'html.parser')


def test_debug(output):
    logger.setLevel(logging.DEBUG)
    render_servers(servers, output_path)
    logger.setLevel(logging.INFO)
    soup = BeautifulSoup(open(output_path), 'html.parser')
    # check debug-label presence
    assert soup.find_all(style='color: red; padding-right: 10px;')
    for client_item in soup.find('ul', id='1.onlinetime').find_all('li'):
        nick = client_item.find('span').text
        # check for right identifier
        nick, encl_identifier = nick.split()
        identifier = encl_identifier.replace('(', '').replace(')', '')
        assert clients[identifier].nick == nick


def test_onlinetime(soup):
    # move this into a (parameterized) fixture or function
    items = soup.find('ul', id='1.onlinetime').find_all('li')
    nick_data = {}
    for item in items:
        nick, data = item.find_all('span')
        nick_data[nick.text] = data.text
    # seperate between uuid and id-clients or merge them some way
    # => assert len(items) == len(clients.id)
    assert len(items) == 2
    for client in clients:
        if client.nick in nick_data and client.onlinetime > timedelta(0):
            # remove this clause after splitting cients
            # (uuid-clients will never have a online-time, because
            #  they're only used for bans and kicks)
            assert nick_data[client.nick] == \
                seconds_to_text(int(client.onlinetime.total_seconds()))


def test_filter_threshold():
    sorted_clients = sort_clients(
        clients, lambda c: c.onlinetime.total_seconds())
    assert len(filter_threshold(sorted_clients, -1)) == len(sorted_clients)
    assert len(filter_threshold(sorted_clients, 20)) == 1
    assert len(filter_threshold(sorted_clients, 500)) == 0
