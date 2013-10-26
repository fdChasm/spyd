from twisted.internet import reactor


class RateLimiter(object):

    clock = reactor

    def __init__(self, limit):
        self._limit = limit
        self._this_sec = None
        self._count_this_sec = 0

    def check_drop(self):
        curr_sec = int(self.clock.seconds())
        if self._this_sec != curr_sec:
            self._this_sec = curr_sec
            self._count_this_sec = 0

        self._count_this_sec += 1

        return self._count_this_sec > self._limit
