import sys

from distutils.core import setup

packages = [
        'spyd.authentication',
        'spyd.authentication.services',
        'spyd.authentication.services.maestro',
        'spyd.authentication.services.vanilla',
        'spyd.game',
        'spyd.game.awards',
        'spyd.game.client',
        'spyd.game.client.message_handlers',
        'spyd.game.command',
        'spyd.game.command.commands',
        'spyd.game.edit',
        'spyd.game.gamemode',
        'spyd.game.gamemode.bases',
        'spyd.game.map',
        'spyd.game.player',
        'spyd.game.room',
        'spyd.game.room.client_event_handlers',
        'spyd.game.room.player_event_handlers',
        'spyd.game.timing',
        'spyd.permissions',
        'spyd.protocol',
        'spyd.punitive_effects',
        'spyd.server',
        'spyd.server.binding',
        'spyd.server.gep_message_handlers',
        'spyd.server.lan_info',
        'spyd.server.metrics',
        'spyd.utils',
]

packages.extend([
    'spyd',
    'cube2map',
    'txENet',
    'twisted.plugins'
])

dependencies = [
    "twisted",
    "pycube2crypto",
    'pycube2common>=0.0.0',
    'pycube2protocol>=0.0.0',
    'pycube2demo>=0.0.0',
    "txCascil",
    "txCarbonClient",
    "pyenet>=0.0.0",
    "python-Levenshtein",
    "simplejson",
    "simple_json"
]

setup(
    name="spyd",
    version="0.1",
    packages=packages,
    package_dir={'' : 'src'},
    package_data={
        'twisted': ['plugins/spyd_server.py'],
        'spyd': ['data/*.json']
    },
    install_requires=dependencies,
    author="Chasm",
    author_email="fd.chasm@gmail.com",
    url="https://github.com/fdChasm/spyd",
    license="MIT",
    description="A Python implementation of the Sauerbraten Cube 2 server on top of Twisted.",
    dependency_links = [
        'http://github.com/fdChasm/pyenet/tarball/master#egg=pyenet-0.1.0',
        'http://github.com/fdChasm/pycube2common/tarball/master#egg=pycube2common-0.1.0',
        'http://github.com/fdChasm/pycube2protocol/tarball/master#egg=pycube2protocol-0.1.0',
        'http://github.com/fdChasm/pycube2demo/tarball/master#egg=pycube2demo-0.1.0',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Games/Entertainment :: First Person Shooters",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: zlib/libpng License",
        "Natural Language :: English"
    ],
)
