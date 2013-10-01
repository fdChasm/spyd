class Observation(object):
    def __init__(self, observable, observer_method):
        self.observable = observable
        self.observer_method = observer_method

    def stop_observing(self):
        self.observable.stop_observing(self.observer_method)

class Observable(object):
    def __init__(self):
        self._observer_methods = set()

    def notify(self):
        for observer_method in self._observer_methods:
            observer_method(self)

    def observe(self, observer_method):
        self._observer_methods.add(observer_method)
        return Observation(self, observer_method)

    def stop_observing(self, observer_method):
        if observer_method in self._observer_methods:
            self._observer_methods.remove(observer_method)
