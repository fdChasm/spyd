from __future__ import absolute_import
from spyd.registry_manager import register
import clj

@register('gep_packing', 'clj')
class EdnPacking(object):
    @staticmethod
    def pack(message):
        return clj.dumps(message)

    @staticmethod
    def unpack(data):
        return clj.loads(data)
