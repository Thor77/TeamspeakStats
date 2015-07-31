from bs4 import BeautifulSoup
from tsstats import parse_logs, render_template, _format_seconds
from os import remove

output_path = 'tests/res/output.html'
clients = parse_logs('tests/res/test.log')


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
        assert _format_seconds(clients['1'].onlinetime) == soup.find('span').text
