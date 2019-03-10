Development
===========

Contributing
------------
Contributions are very welcome!

Before developing a new (possibly breaking) feature, please open an Issue about it first
so we can discuss your idea and possible implementations.

Please read this document carefully before submitting your Pull Request to avoid failing CI tests.

Style
-----
Your contribution should pass `flake8 <https://flake8.readthedocs.io>`__
as well as `isort <https://github.com/timothycrosley/isort>`__.

Testing
-------
There are unit tests for all parts of the project built with `py.test <https://docs.pytest.org>`__.
Besides ``py.test`` tests require ``BeautifulSoup`` for template-testing.
Those requirements are listed in ``testing_requirements.txt``::

  $ pip install -r requirements-dev.txt
  $ py.test tsstats/tests/

Versioning
----------
TeamspeakStats uses `Semantic Versioning <http://semver.org/>`__.
Please don't bump versions in your Pull Requests, though, we will do that after merging.

Python Versions
---------------
To keep the tool accessible and maintainable at the same time at least ``Python 2.7`` is required,
so keep this in mind when using fancy new features from a recent Python version.
