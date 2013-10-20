from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application import service

from spyd.options import Options
from spyd import service_maker

class SpydServiceMaker(object):

    implements(service.IServiceMaker, IPlugin)
    
    tapname = "spyd"
    description = "A Sauerbraten server."
    options = Options
    
    def makeService(self, options):
        return service_maker.WrapperService(options)

spyd = SpydServiceMaker()
