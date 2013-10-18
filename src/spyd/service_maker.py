import logging
import os
import shutil
import sys

from twisted.python import log

from spyd.config_loader import config_loader
from spyd.spyd_server import SpydServer


def make_service(options):
    server_directory = options.get('servdir') or 'my_spyd_server'

    if options.get('init'):
        if os.path.exists(server_directory):
            print "The {!r} directory already exists, please only use the -i with a server directory path which does not exist and should be created.".format(server_directory)
            sys.exit(1)

        import spyd

        data_path = spyd.__path__ + ['data']
        data_path = os.path.join(*data_path)

        shutil.copytree(data_path, server_directory)

        if os.path.exists(server_directory):
            print "The specified server directory has been created; {!r} Remove the -i flag to run.".format(server_directory)
            sys.exit(0)
        else:
            print "Error failed to create the specified server directory."
            sys.exit(1)

    if not os.path.exists(server_directory):
        print "The specified server directory, {!r}, does not exist. Use the -i flag to create it.".format(server_directory)
        sys.exit(1)

    os.chdir(server_directory)
    print "Using server directory; {!r}".format(os.path.abspath(os.curdir))

    config = config_loader('config.json')

    # logging.basicConfig(level=logging.DEBUG)

    # log.startLogging(sys.stdout)

    spyd = SpydServer(config)

    return spyd.root_service
