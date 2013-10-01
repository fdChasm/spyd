class Expiry(object):
    def __init__(self, game_clock, duration):
        self.game_clock = game_clock
        self.unblock_time = self.game_clock.time_elapsed + duration

    def extend(self, seconds, maximum=None):
        if maximum is not None:
            seconds = min(self.remaining + seconds, maximum)
        self.unblock_time += seconds

    @property
    def remaining(self):
        return max(0, self.unblock_time - self.game_clock.time_elapsed)

    @property
    def is_expired(self):
        return self.game_clock.time_elapsed >= self.unblock_time
