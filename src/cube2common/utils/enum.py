class enum(object):
    """@DynamicAttrs"""
    __by_values = {}
    def __init__(self, *items, **kwitems):
        self.__by_names = {}
        self.__by_values = {}
        
        i = 0
        for item in items:
            self.__by_names[item] = i
            self.__by_values[i] = item
            self.__setattr__(item, i)
            i += 1
            
        for item, value in kwitems.items():
            self.__by_names[item] = value
            self.__by_values[value] = item
            self.__setattr__(item, value)
            
    def by_value(self, value):
        return self.__by_values.get(value, None)
    
    def has_value(self, value):
        return value in self.__by_values
    
    def by_name(self, item):
        return self.__by_names.get(item, None)
    
    def contains(self, item):
        return item in self.__by_names
