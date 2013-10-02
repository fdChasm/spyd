class Timer(object):
    def __init__(self, game_clock):
        self.game_clock = game_clock
        self.reset()
        
    def reset(self):
        self.start_time = self.game_clock.time_elapsed
        self.accumulator = 0
    
    @property
    def paused(self):
        return self.start_time is None
        
    @property
    def time_elapsed(self):
        if self.paused:
            return self.accumulator
        else:
            return self.accumulator + (self.game_clock.time_elapsed - self.start_time)
    
    def pause(self):
        self.accumulator += self.time_elapsed
        self.start_time = None
        
    def resume(self):
        self.start_time = self.game_clock.time_elapsed
