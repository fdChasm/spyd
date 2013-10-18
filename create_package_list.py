import pkgutil
import spyd
package=spyd
print "packages = ["
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+'.',
                                                      onerror=lambda x: None):
    if ispkg:
        print "\t'{}',".format(modname)
print "]"