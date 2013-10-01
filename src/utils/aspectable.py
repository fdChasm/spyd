def aspect_exclusive(func):
    '''Set an attribute as an aspect exclusive. This means it will be the only handler 
    for the given attribute across all aspects of the object.'''
    func._is_aspect_exclusive = True
    return func

NoAttribute = object()

class PartiallyCallableAspectAttribute(Exception):
    def __init__(self, key):
        self.message = "Some aspects of the object have functions as attribute '{}' while others have values.".format(key)
        
class MultipleExclusiveAspectAttributes(Exception):
    def __init__(self, key):
        self.message = "Multiple functions marked as exclusive for attribute '{}'.".format(key)
        
class MultipleNonCallableAttributes(Exception):
    def __init__(self, key):
        self.message = "Non-callable attribute '{}' exists on multiple aspects.".format(key)

def is_aspect_exclusive(func):
    return getattr(func, '_is_aspect_exclusive', False)

class CallableSet(object):
    def __init__(self, callables):
        self.callables = callables
        
    def __call__(self, *args, **kwargs):
        return map(lambda c: c(*args, **kwargs), self.callables)

class Aspectable(object):
    def __init__(self, *args, **kwargs):
        self.aspects = map(lambda A: A(self, *args, **kwargs), self.aspects)
        
    def __getattr__(self, key):
        attrs = map(lambda a: getattr(a, key, NoAttribute), self.aspects)
        attrs = filter(lambda attr: attr is not NoAttribute, attrs)
        
        if not len(attrs):
            raise AttributeError(key)
        
        which_callable = map(lambda attr: callable(attr), attrs)
        if any(which_callable):
            if not all(which_callable):
                raise PartiallyCallableAspectAttribute(key)
            
            which_exclusive = map(lambda attr: is_aspect_exclusive(attr), attrs)
            if any(which_exclusive):
                if len(attrs) != 1:
                    raise MultipleExclusiveAspectAttributes(key)
                
                return attrs[0]
            
            return CallableSet(attrs)
        
        if len(attrs) != 1:
            raise MultipleNonCallableAttributes(key)
        
        return attrs[0]