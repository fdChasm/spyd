from twisted.internet import reactor

from cube2common.utils.enum import enum
from spyd.game.timing.callback import Callback, call_all
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper, resume_all, pause_all


states = enum('NOT_STARTED', 'RUNNING', 'PAUSED', 'RESUMING', 'INTERMISSION', 'ENDED')

class GameClock(object):
    
    clock = reactor
    
    def __init__(self):
        self._state = states.NOT_STARTED
        
        self._last_resume_time = None
        self._time_elapsed = None
        
        self._intermission_duration_seconds = None
        
        self._intermission_start_scheduled_callback_wrapper = None
        self._intermission_end_scheduled_callback_wrapper = None
        self._resume_countdown = None
        
        self._timed = True
        
        self._paused_callbacks = []
        self._resumed_callbacks = []
        self._resume_countdown_tick_callbacks = []
        self._timeleft_altered_callbacks = []
        self._intermission_started_callbacks = []
        self._intermission_ended_callbacks = []
        
        self._scheduled_callback_wrappers = []
        
    def _cancel_existing_scheduled_events(self):
        if self._intermission_end_scheduled_callback_wrapper is not None:
            self._intermission_end_scheduled_callback_wrapper.cancel()
            self._intermission_start_scheduled_callback_wrapper = None
            
        if self._intermission_start_scheduled_callback_wrapper is not None:
            self._intermission_start_scheduled_callback_wrapper.cancel()
            self._intermission_start_scheduled_callback_wrapper = None
    
    def start(self, game_duration_seconds, intermission_duration_seconds):
        '''Set the game clock. If a game is currently underway, this will reset the time elapsed and set the amount of time left as specified.'''
        self._timed = True
        
        self._cancel_existing_scheduled_events()
            
        self._intermission_duration_seconds = intermission_duration_seconds
        self._intermission_start_scheduled_callback_wrapper = ScheduledCallbackWrapper(game_duration_seconds)
        self._intermission_start_scheduled_callback_wrapper.external_deferred.addCallback(self._intermission_started)
        
        self._intermission_end_scheduled_callback_wrapper = ScheduledCallbackWrapper(game_duration_seconds+intermission_duration_seconds)
        self._intermission_end_scheduled_callback_wrapper.external_deferred.addCallback(self._intermission_ended)
        
        self._time_elapsed = 0.0
        
    def start_untimed(self):
        self._state = states.PAUSED
        self._timed = False
        self._cancel_existing_scheduled_events()
        self._time_elapsed = 0.0
    
    def add_paused_callback(self, f, *args, **kwargs):
        '''Add a callback function which will be called with the specified arguments each time the game is paused.'''
        self._paused_callbacks.append(Callback(f, args, kwargs))

    def add_resumed_callback(self, f, *args, **kwargs):
        '''Add a callback function which will be called with the specified arguments each time the game is resumed.'''
        self._resumed_callbacks.append(Callback(f, args, kwargs))
    
    def add_resume_countdown_tick_callback(self, f, *args, **kwargs):
        '''Add a callback function which will be called with the specified arguments following the number of seconds until the game resumes each second until it does.'''
        self._resume_countdown_tick_callbacks.append(Callback(f, args, kwargs))
    
    def add_timeleft_altered_callback(self, f, *args, **kwargs):
        '''Add a callback which will be called with the specified arguments following the time left each time the amount of time in the game is altered.'''
        self._timeleft_altered_callbacks.append(Callback(f, args, kwargs))
    
    def add_intermission_started_callback(self, f, *args, **kwargs):
        '''Add a callback which will be called with the specified arguments each time the game clock enters intermission.'''
        self._intermission_started_callbacks.append(Callback(f, args, kwargs))
    
    def add_intermission_ended_callback(self, f, *args, **kwargs):
        '''Add a callback which will be called with the specified arguments each the time game clock leaves intermission.'''
        self._intermission_ended_callbacks.append(Callback(f, args, kwargs))
    
    def resume(self, delay=None):
        '''Resume the clock. If a delay is specified, the timer will resume after that number of seconds.'''
        if self.is_resuming:
            self._resume_countdown.cancel()
        elif not self.is_started:
            pass
        elif not self.is_paused:
            return

        if delay is not None:
            self._resume_countdown = ResumeCountdown(delay, Callback(self._resume_countdown_tick), Callback(self._resumed))
            self._resume_countdown.start()
        else:
            self._resumed()
    
    def pause(self):
        '''Pause the clock.'''
        if self.is_resuming:
            self._resume_countdown.cancel()
            self._resume_countdown = None
        elif not self.is_paused:
            self._paused()
        else:
            return
    
    def schedule_callback(self, seconds):
        '''Schedule a callback after the specified number of seconds on the game clock. Returns a deferred.'''
        scheduled_callback_wrapper = ScheduledCallbackWrapper(seconds)
        self._scheduled_callback_wrappers.append(scheduled_callback_wrapper)
        scheduled_callback_wrapper.internal_deferred.addCallback(self._scheduled_callback_wrappers.remove, scheduled_callback_wrapper)
        if not self.is_paused:
            scheduled_callback_wrapper.resume()
        return scheduled_callback_wrapper.external_deferred
    
    @property
    def is_started(self):
        return self._state not in (states.NOT_STARTED, states.ENDED)
    
    @property
    def is_paused(self):
        '''Is the game clock currently paused.'''
        return self._state in (states.NOT_STARTED, states.PAUSED, states.RESUMING)
    
    @property
    def is_resuming(self):
        '''Is there a resume countdown currently in progress.'''
        return self._state == states.RESUMING

    @property
    def is_game(self):
        '''Returns whether the game is started and not yet in intermission.'''
        return self._state in (states.RUNNING, states.PAUSED, states.RESUMING)

    @property
    def is_intermission(self):
        '''Is the game clock currently in intermission.'''
        return self._state == states.INTERMISSION

    @property
    def timeleft(self):
        '''How much time left on the game clock.'''
        if self._intermission_start_scheduled_callback_wrapper is not None:
            return self._intermission_start_scheduled_callback_wrapper.timeleft
        else:
            return 0.0

    @timeleft.setter
    def timeleft(self, seconds):
        '''Set how many seconds are left on the game clock.'''
        if seconds > 0.0:
            self._intermission_start_scheduled_callback_wrapper.timeleft = seconds
            self._intermission_end_scheduled_callback_wrapper.timeleft = seconds + self._intermission_duration_seconds
            self._timeleft_altered()
        else:
            self._cancel_existing_scheduled_events()
            self._intermission_end_scheduled_callback_wrapper = ScheduledCallbackWrapper(self._intermission_duration_seconds)
            self._intermission_end_scheduled_callback_wrapper.external_deferred.addCallback(self._intermission_ended)
            self._timeleft_altered()

    @property
    def intermission_timeleft(self):
        '''How many seconds are left in the intermission.'''
        if self.is_intermission:
            return self._intermission_end_scheduled_callback_wrapper.timeleft
        else:
            return 0.0

    @property
    def time_elapsed(self):
        '''Return how many seconds this game has been going for.'''
        if self.is_paused:
            return self._time_elapsed
        else:
            return self._time_elapsed + (self.clock.seconds() - self._last_resume_time)

    def _paused(self):
        self._state = states.PAUSED
        self._time_elapsed += self.clock.seconds() - self._last_resume_time
        self._last_resume_time = None
        if self._timed:
            self._intermission_start_scheduled_callback_wrapper.pause()
            self._intermission_end_scheduled_callback_wrapper.pause()
        pause_all(self._scheduled_callback_wrappers)
        call_all(self._paused_callbacks)

    def _resumed(self):
        self._state = states.RUNNING
        self._last_resume_time = self.clock.seconds()
        if self._timed:
            self._intermission_start_scheduled_callback_wrapper.resume()
            self._intermission_end_scheduled_callback_wrapper.resume()
        resume_all(self._scheduled_callback_wrappers)
        call_all(self._resumed_callbacks)
        
    def _resume_countdown_tick(self, seconds):
        call_all(self._resume_countdown_tick_callbacks, seconds)

    def _intermission_started(self, *args, **kwargs):
        self._state = states.INTERMISSION
        call_all(self._intermission_started_callbacks)

    def _intermission_ended(self, *args, **kwargs):
        self._state = states.ENDED
        call_all(self._intermission_ended_callbacks)

    def _timeleft_altered(self):
        call_all(self._timeleft_altered_callbacks, self.timeleft)
