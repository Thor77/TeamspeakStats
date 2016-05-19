import logging
from os import remove

import pytest

from tsstats import exceptions
from tsstats.__main__ import main
from tsstats.log import parse_logs

clients = parse_logs('tsstats/tests/res/test.log')


logger = logging.getLogger('tsstats')


@pytest.fixture
def output(request):
    def clean():
        remove('tsstats/tests/res/output.html')
    request.addfinalizer(clean)


def test_main(output):
    main(config_path='tsstats/tests/res/config.ini')


def test_main_config_not_found():
    with pytest.raises(exceptions.ConfigNotFound):
        main(config_path='/some/where/no/conf.ini')


def test_main_idmap_load(output):
    main(config_path='tsstats/tests/res/config.ini',
         id_map_path='tsstats/tests/res/id_map.json')


def test_debug_log():
    logger.setLevel(logging.DEBUG)
    parse_logs('tsstats/tests/res/test.log')
    logger.setLevel(logging.INFO)
    open('debug.txt')
    remove('debug.txt')
