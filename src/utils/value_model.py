from utils.observable import Observable

class ValueModel(Observable):
    def __init__(self, value):
        Observable.__init__(self)
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self.notify()
