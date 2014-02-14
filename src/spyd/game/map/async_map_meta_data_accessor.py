from twisted.internet import defer, protocol, reactor
from twisted.protocols.basic import NetstringReceiver
import json
import itertools
import os.path
import sys

class NetstringParser(NetstringReceiver):
    def __init__(self):
        self.received = []

    def stringReceived(self, string):
        self.received.append(string)

    def popMessage(self):
        return self.received.pop(0)

    def hasMessage(self):
        return len(self.received) > 0

class NetStringProcessProtocol(protocol.ProcessProtocol):
    def __init__(self):
        self.parser = NetstringParser()

    def connectionMade(self):
        self.parser.makeConnection(self.transport)
        self.ready()

    def outReceived(self, data):
        self.parser.dataReceived(data)
        while self.parser.hasMessage():
            self.messageReceived(self.parser.popMessage())

    def messageReceived(self, message):
        raise NotImplementedError()

    def sendMessage(self, message):
        self.parser.sendString(json.dumps(message))

class JsonRpcProcessProtocol(NetStringProcessProtocol):
    def __init__(self):
        NetStringProcessProtocol.__init__(self)
        self.request_id = itertools.count()

        # reqid: deferred
        self.requests = {}

    def messageReceived(self, message):
        message = json.loads(message)
        reqid = message['reqid']
        deferred = self.requests.pop(reqid)
        if message.get('error', None) is not None:
            deferred.errback(Exception(message['error']))
        else:
            deferred.callback(message['result'])

    def callMethod(self, method, *args, **kwargs):
        reqid = self.request_id.next()
        self.requests[reqid] = defer.Deferred()
        self.sendMessage({'method': method, 'args': args, 'kwargs': kwargs, 'reqid': reqid})
        return self.requests[reqid]

    def ready(self):
        pass

    def errReceived(self, data):
        sys.stderr.write(data)

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)

class AsyncMapMetaDataAccessor(object):
    def __init__(self, package_dir):
        directory = os.path.dirname(__file__)
        map_data_reader_filename = os.path.join(directory, 'map_data_reader_process.py')
        self.map_data_reader_process_procotol = JsonRpcProcessProtocol()
        reactor.spawnProcess(self.map_data_reader_process_procotol, "python2.7", ["-u", map_data_reader_filename], env={'PYTHONPATH': os.environ['PYTHONPATH']})

        self.package_dir = package_dir

        self._cached_map_meta = {}
        self._map_name_cache = None

    def call_method(self, *args, **kwargs):
        return self.map_data_reader_process_procotol.callMethod(*args, **kwargs)

    def get_map_path(self, map_name):
        map_filename = "{}.ogz".format(map_name)
        return os.path.join(self.package_dir, "base", map_filename)

    def get_map_data(self, map_name, default=None):
        if map_name in self._cached_map_meta:
            return defer.succeed(self._cached_map_meta.get(map_name))
        else:
            def cache_map_meta(map_meta_data):
                self._cached_map_meta[map_name] = map_meta_data
                return map_meta_data

            deferred = self.call_method('read_map_data', self.get_map_path(map_name))
            deferred.addCallback(cache_map_meta)

            return deferred

    def get_map_names(self):
        if self._map_name_cache is not None:
            return defer.succeed(self._map_name_cache)
        else:
            def cache_map_names(map_names):
                self._map_name_cache = map_names
                return self._map_name_cache

            map_glob_expression = os.path.join(self.package_dir, "base", "*.ogz")

            deferred = self.call_method('read_map_names', map_glob_expression)
            deferred.addCallback(cache_map_names)

            return deferred
