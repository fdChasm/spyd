class PingBuffer(object):
    BUFFERSIZE = 15
    def __init__(self):
        self.pings = []
    
    def add(self, ping):
        self.pings.append(ping)
        if len(self.pings) > self.BUFFERSIZE:
            self.pings.pop(0)
            
    def avg(self):
        return float(sum(self.pings)) / max(len(self.pings), 1)
