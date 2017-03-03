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
    items = soup.find('ul', id='1.onlinetime').find_all('li')
    assert len(items) == 2
    for item in items:
        nick, onlinetime = item.find_all('span')
        nick = nick.text
        onlinetime = onlinetime.text
        # find corresponding client-object
        client = filter(
            lambda c: c.nick == nick and c.onlinetime > timedelta(0),
            clients
        )
        # assert existence
        assert client
        client = client[0]
        # compare onlinetimes
        client_onlinetime_text = seconds_to_text(
            int(client.onlinetime.total_seconds())
        )
        assert onlinetime == client_onlinetime_text


def test_filter_threshold():
    sorted_clients = sort_clients(
        clients, lambda c: c.onlinetime.total_seconds())
    assert len(filter_threshold(sorted_clients, -1)) == len(sorted_clients)
    assert len(filter_threshold(sorted_clients, 20)) == 1
    assert len(filter_threshold(sorted_clients, 500)) == 0
