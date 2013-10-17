from __future__ import absolute_import
from spyd.registry_manager import register
import json

@register('gep_packing', 'json')
class JsonPacking(object):
    @staticmethod
    def pack(message):
        return json.dumps(message)

    @staticmethod
    def unpack(data):
        return json.loads(data)
