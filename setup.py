from setuptools import setup

setup(
    name='tsstats',
    version='0.6.2',
    author='Thor77',
    author_email='thor77@thor77.org',
    description='A simple Teamspeak stats-generator',
    keywords='ts3 teamspeak teamspeak3 tsstats teamspeakstats',
    url='https://github.com/Thor77/TeamspeakStats',
    packages=['tsstats'],
    entry_points={
        'console_scripts': [
            'tsstats = tsstats.__main__:cli'
        ]
    },
    package_data={
        'tsstats': ['template.html']
    },
    install_requires=[
        'Jinja2>=2.8'
    ],
)
