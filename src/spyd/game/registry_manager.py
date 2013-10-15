class RegistryManager(object):

    # key: registry name
    # value: Registration
    registries = {}
        
    @classmethod
    def register(cls, registry_name, registered_object, args, kwargs):
        if registry_name not in cls.registries:
            cls.registries[registry_name] = []
            
        registry = cls.registries[registry_name]
        
        registry.append(Registration(registered_object, args, kwargs))
        
    @classmethod
    def get_registrations(cls, registry_name):
        return cls.registries.get(registry_name, ())

class Registration(object):
    def __init__(self, registered_object, args, kwargs):
        self.registered_object = registered_object
        self.args   = list(args)
        self.kwargs = kwargs

def register(registry_name, *args, **kwargs):
    def decorator(registered_object):
        RegistryManager.register(registry_name, registered_object, args, kwargs)
        return registered_object
    return decorator

