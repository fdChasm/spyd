from twisted.python import log
import logging
from logging import Logger

logging.addLevelName(45, 'SPYD')

class SpydLogger(Logger):
    def spyd_event(self, msg):
        self.log(45, msg)

def _get_logger(level):
    observer = log.PythonLoggingObserver()
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s: %(message)s')
    return observer.emit

def logger():
    return _get_logger(level=logging.INFO)

def quiet_logger():
    return _get_logger(level=logging.WARNING)

def debug_logger():
    return _get_logger(level=logging.DEBUG)
