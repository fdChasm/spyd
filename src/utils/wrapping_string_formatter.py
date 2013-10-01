import string

class WrappingStringFormatter(string.Formatter):
    def __init__(self, *args, **kwargs):
        self.wrappers = {}
        
    def get_field(self, field_name, args, kwargs):
        if '#' in field_name:
            wrapper_name, field_name = field_name.split('#', 1)
            wrapper = self.wrappers[wrapper_name]
            obj, used_key = string.Formatter.get_field(self, field_name, args, kwargs)
            obj = wrapper(obj)
        else:
            obj, used_key = string.Formatter.get_field(self, field_name, args, kwargs)
        return obj, used_key
    
    def register_wrapper(self, wrapper_name, wrapper):
        self.wrappers[wrapper_name] = wrapper