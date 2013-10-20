class Callback(object):
    def __init__(self, f, args=(), kwargs={}):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        
    def call(self, *args, **kwargs):
        args = list(args)
        args.extend(self.args)
        kwargs.update(self.kwargs)
        self.f(*args, **kwargs)
        
def call_all(callback_list, *args, **kwargs):
    callback_list = list(callback_list)
    for callback in callback_list:
        callback.call(*args, **kwargs)
