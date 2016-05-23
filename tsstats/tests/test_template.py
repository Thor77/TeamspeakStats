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


def test_debug(output):
    logger.setLevel(logging.DEBUG)
    render_template(clients, output_path)
    logger.setLevel(logging.INFO)
    soup = BeautifulSoup(open(output_path), 'html.parser')
    # check red label
    assert soup.find_all(class_='alert alert-danger')
    # check ident present after nick
    li = soup.find('li')
    assert li
    assert '(' in li.text.split()[1]


def test_data(output):
    render_template(clients, output_path)
    soup = BeautifulSoup(open(output_path), 'html.parser')
    # check onlinetime-data
    assert seconds_to_text(clients['1'].onlinetime) == \
        soup.find('span', class_='badge').text
