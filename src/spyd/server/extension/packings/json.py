from spyd.registry_manager import register
import json

@register('gep_packing', 'json')
class JsonPacking(object):
    @staticmethod
    def pack(self, message):
        return json.dumps(message)

    @staticmethod
    def unpack(self, data):
        return json.loads(data)
