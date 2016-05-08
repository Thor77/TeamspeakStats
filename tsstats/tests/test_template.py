from os import remove

from bs4 import BeautifulSoup

from tsstats.utils import seconds_to_text
from tsstats.log import parse_logs
from tsstats.template import render_template

output_path = 'tsstats/tests/res/output.html'
clients = parse_logs('tsstats/tests/res/test.log')


class TestTemplate:
    def teardown_class():
        remove(output_path)

    def test_debug(self):
        render_template(clients, output_path, debug=True)
        soup = BeautifulSoup(open(output_path), 'html.parser')
        # check red label
        assert soup.find_all(class_='alert alert-danger')
        # check ident present after nick
        li = soup.find('li')
        assert li
        assert '(' in li.text.split()[1]

    def test_data(self):
        render_template(clients, output_path)
        soup = BeautifulSoup(open(output_path), 'html.parser')
        # check onlinetime-data
        assert seconds_to_text(clients['1'].onlinetime) == \
            soup.find('span', class_='badge').text
