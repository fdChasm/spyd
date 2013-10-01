from twisted.internet import defer, reactor

from sauerpyd.timing.exceptions import AlreadyPausedException, AlreadyResumedException


class ScheduledCallbackWrapper(object):
    '''Holds a deferred and either delayed call or a delay seconds value.'''
    
    clock = reactor
    
    def __init__(self, seconds):
        # The external deferred gets returned to the client scheduling an event.
        # We use the internal deferred to make sure this gets cleaned up whether or not it is cancelled.
        self.external_deferred = defer.Deferred()
        self.internal_deferred = defer.Deferred()
        
        self.internal_deferred.chainDeferred(self.external_deferred)
        
        self._delayed_call = None
        self._delay_seconds = seconds
        
    def pause(self):
        if self.is_paused:
            return
        self._delay_seconds = self.timeleft
        self._delayed_call.cancel()
        self._delayed_call = None

    def resume(self):
        if not self.is_paused:
            return
        self._delayed_call = self.clock.callLater(self._delay_seconds, self.internal_deferred.callback, True)
        self._delay_seconds = None

    def cancel(self):
        self.external_deferred.cancel()
        self._delayed_call.cancel()
        self.internal_deferred.callback(False)
        
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
