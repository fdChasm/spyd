from twisted.internet import defer, reactor
from spyd.game.timing.callback import Callback, call_all

class ScheduledCallbackWrapper(object):
    '''Holds a deferred and either delayed call or a delay seconds value.'''
    
    clock = reactor
    
    def __init__(self, seconds):
        self._finished_callbacks = set()
        self._timeup_callbacks = set()
        
        self._cancelled = False
        self._delayed_call = None
        self._delay_seconds = seconds
        
    def pause(self):
        if self.is_paused or self._cancelled:
            return
        self._delay_seconds = self.timeleft
        self._delayed_call.cancel()
        self._delayed_call = None

    def resume(self):
        if not self.is_paused or self._cancelled:
            return
        self._delayed_call = self.clock.callLater(self._delay_seconds, self._timeup)
        self._delay_seconds = None
        
    def add_finished_callback(self, func, *args, **kwargs):
        callback = Callback(func, args, kwargs)
        self._finished_callbacks.add(callback)

    def add_timeup_callback(self, func, *args, **kwargs):
        callback = Callback(func, args, kwargs)
        self._timeup_callbacks.add(callback)

    def _finished_cleanup(self):
        self._timeup_callbacks.clear()
        self._finished_callbacks.clear()
        self._delayed_call = None
        self._delay_seconds = 0.0

    def _timeup(self):
        call_all(self._finished_callbacks)
        if not self._cancelled:
            call_all(self._timeup_callbacks)
            self._delay_seconds = 0.0
        self._finished_cleanup()

    def cancel(self):
        call_all(self._finished_callbacks)
        if self._delayed_call is not None and not self._delayed_call.called:
            self._delayed_call.cancel()
        self._cancelled = True
        self._finished_cleanup()
        
    @property
    def timeleft(self):
        if self._delayed_call is None:
            return self._delay_seconds
        else:
            return max(0.0, self._delayed_call.getTime() - self.clock.seconds())
        
    @timeleft.setter
    def timeleft(self, seconds):
        was_paused = self.is_paused
        if was_paused:
            self.pause()
        self._delay_seconds = seconds
        if was_paused:
            self.resume()

    @property
    def is_paused(self):
        return self._delayed_call is None

def pause_all(scheduled_callback_wrapper_list):
    for scheduled_callback_wrapper in scheduled_callback_wrapper_list:
        scheduled_callback_wrapper.pause()

def resume_all(scheduled_callback_wrapper_list):
    for scheduled_callback_wrapper in scheduled_callback_wrapper_list:
        scheduled_callback_wrapper.resume()
