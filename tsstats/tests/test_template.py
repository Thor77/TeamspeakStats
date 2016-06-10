import logging
from os import remove

import pytest
from bs4 import BeautifulSoup

from tsstats.log import parse_log
from tsstats.template import render_template
from tsstats.utils import seconds_to_text

output_path = 'tsstats/tests/res/output.html'
clients = parse_log('tsstats/tests/res/test.log')

logger = logging.getLogger('tsstats')


@pytest.fixture
def output(request):
    def clean():
        remove('tsstats/tests/res/output.html')
    request.addfinalizer(clean)


@pytest.fixture
def soup(output):
    render_template(clients, output_path)
    return BeautifulSoup(open(output_path), 'html.parser')


def test_debug(output):
    logger.setLevel(logging.DEBUG)
    render_template(clients, output_path)
    logger.setLevel(logging.INFO)
    soup = BeautifulSoup(open(output_path), 'html.parser')
    # check debug-label presence
    assert soup.find_all(class_='alert alert-danger')
    for client_item in soup.find_all('li'):
        nick = client_item.find('span').text
        # check for right identifier
        nick, encl_identifier = nick.split()
        identifier = encl_identifier.replace('(', '').replace(')', '')
        assert clients[identifier].nick == nick


def test_onlinetime(soup):
    assert seconds_to_text(clients['1'].onlinetime) == \
        soup.find('span', class_='badge').text
