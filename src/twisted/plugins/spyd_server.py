from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application import service

from spyd.options import Options
from spyd.wrapper_service import WrapperService

class SpydServiceMaker(object):

    implements(service.IServiceMaker, IPlugin)
    
    tapname = "spyd"
    description = "A Sauerbraten server."
    options = Options
    
    def makeService(self, options):
        return WrapperService(options)

spyd = SpydServiceMaker()
