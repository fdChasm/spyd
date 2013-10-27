import sys

from distutils.core import setup

packages = [
        'spyd.authentication',
        'spyd.authentication.services',
        'spyd.authentication.services.vanilla',
        'spyd.game',
        'spyd.game.awards',
        'spyd.game.client',
        'spyd.game.command',
        'spyd.game.command.commands',
        'spyd.game.edit',
        'spyd.game.gamemode',
        'spyd.game.gamemode.bases',
        'spyd.game.map',
        'spyd.game.player',
        'spyd.game.room',
        'spyd.game.timing',
        'spyd.permissions',
        'spyd.protocol',
        'spyd.punitive_effects',
        'spyd.server',
        'spyd.server.binding',
        'spyd.server.extension',
        'spyd.server.extension.authentication_controllers',
        'spyd.server.extension.message_handlers',
        'spyd.server.extension.packings',
        'spyd.server.extension.transports',
        'spyd.server.lan_info',
        'spyd.server.metrics',
        'spyd.utils',
]

packages.extend([
    'spyd',
    'cube2common',
    'cube2common.utils',
    'cube2crypto',
    'cube2map',
    'txENet',
    'twisted.plugins'
])

setup(
    name="spyd",
    version="0.1",
    packages=packages,
    package_dir={'' : 'src'},
    package_data={
        'twisted': ['plugins/spyd_server.py'],
        'spyd': ['data/*.json']
    },
    install_requires=["twisted", "pycrypto", "txCarbonClient", "pyenet>=0.0.0", "python-Levenshtein", "simplejson", "simple_json", "pyclj"],
    author="Chasm",
    author_email="fd.chasm@gmail.com",
    url="https://github.com/fdChasm/spyd",
    license="MIT",
    description="A Python implementation of the Sauerbraten Cube 2 server on top of Twisted.",
    dependency_links = [
        'http://github.com/fdChasm/pyenet/tarball/master#egg=pyenet-0.1.0',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Games/Entertainment :: First Person Shooters",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: zlib/libpng License",
        "Natural Language :: English"
    ],
)
