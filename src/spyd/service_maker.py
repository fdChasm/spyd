import logging
import os
import shutil
import sys

from twisted.application.service import MultiService

from spyd.log import SpydLogger

logging.setLoggerClass(SpydLogger)
logger = logging.getLogger(__name__)

import spyd as spyd_root_module
from spyd.config_loader import config_loader
from spyd.spyd_server import SpydServer


def fatal(msg):
    logger.critical(msg)
    sys.exit(1)

def success(msg):
    logger.info(msg)
    sys.exit(0)

class WrapperService(MultiService):
    def __init__(self, options):
        self._options = options
        MultiService.__init__(self)

    def startService(self):
        options = self._options

        server_directory = options.get('servdir') or 'my_spyd_server'

        server_directory = os.path.expanduser(server_directory)

        if not len(logging._handlers):
            logging.basicConfig()

        if options.get('init'):
            if os.path.exists(server_directory):
                fatal("The {!r} directory already exists, please only use the -i with a server directory path which does not exist and should be created.".format(server_directory))

            data_path = spyd_root_module.__path__ + ['data']
            data_path = os.path.join(*data_path)

            shutil.copytree(data_path, server_directory)

            if os.path.exists(server_directory):
                success("The specified server directory has been created; {!r} Remove the -i flag to run.".format(server_directory))
            else:
                fatal("Error failed to create the specified server directory.")

        if not os.path.exists(server_directory):
            fatal("The specified server directory, {!r}, does not exist. Use the -i flag to create it.".format(server_directory))

        os.chdir(server_directory)
        logger.info("Using server directory; {!r}".format(os.path.abspath(os.curdir)))

        config = config_loader('config.json')

        spyd = SpydServer(config)

        spyd.root_service.setServiceParent(self)

        MultiService.startService(self)

        logger.spyd_event("Server started.")
