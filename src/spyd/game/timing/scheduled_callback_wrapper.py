from twisted.internet import defer, reactor

def try_cancel(deferred):
    if deferred is None: return
    if hasattr(deferred, 'called') and deferred.called: return
    deferred.cancel()

class ScheduledCallbackWrapper(object):
    '''Holds a deferred and either delayed call or a delay seconds value.'''
    
    clock = reactor
    
    def __init__(self, seconds):
        # The external deferred gets returned to the client scheduling an event.
        # We use the internal deferred to make sure this gets cleaned up whether or not it is cancelled.
        self.external_deferred = defer.Deferred()
        self.internal_deferred = defer.Deferred()
        
        # Ignore the DeferredCancelled errors
        #self.external_deferred.addErrback(lambda e: None)
        #self.internal_deferred.addErrback(lambda e: None)
        
        self.internal_deferred.chainDeferred(self.external_deferred)
        
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
        self._delayed_call = self.clock.callLater(self._delay_seconds, self.internal_deferred.callback, True)
        self._delay_seconds = None

    def cancel(self):
        try_cancel(self.external_deferred)
        try_cancel(self._delayed_call)
        self.external_deferred = None
        self._delayed_call = None
        try:
            self.internal_deferred.callback(False)
        except:
            pass
        self._cancelled = True
        self._delay_seconds = 0.0
        
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
