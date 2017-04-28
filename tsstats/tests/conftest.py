from os import remove

import pytest


@pytest.fixture
def output(request):
    output_path = 'tsstats/tests/res/output.html'

    def clean():
        remove(output_path)
    request.addfinalizer(clean)
    yield output_path
