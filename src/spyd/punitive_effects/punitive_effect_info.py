import time

class PermaExpiryInfo(object):
    @property
    def expired(self):
        return False

class TimedExpiryInfo(object):
    def __init__(self, expiry_time):
        self.expiry_time = expiry_time

    @property
    def expired(self):
        return time.time() > self.expiry_time

class EffectInfo(object):
    def __init__(self, expiry_info):
        self.expiry_info = expiry_info

    @property
    def expired(self):
        return self.expiry_info.expired
