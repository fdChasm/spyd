import logging
import os
import sys

from twisted.python import log

from spyd.config_loader import config_loader
from spyd.spyd_server import SpydServer


def make_service(options):
    home_directory = os.path.abspath(options.get('homedir'))
    os.chdir(home_directory)

    config_filename = os.path.abspath(options.get('config'))
    config = config_loader(config_filename)

    #logging.basicConfig(level=logging.DEBUG)
    
    #log.startLogging(sys.stdout)

    spyd = SpydServer(config)

    return spyd.root_service
