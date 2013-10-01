import struct

class ReadCubeDataStream(object):
    def __init__(self, data=""):
        try:
            if isinstance(data, ReadCubeDataStream):
                self.data = bytearray(data.data)
            elif isinstance(data, bytearray) or type(data) == str:
                self.data = bytearray(data)
            else:
                print "I don't know what I got so just trying to map to a bytearray using ord. This shouldn't happen, it is slow."
                self.data = bytearray(map(ord, data))
        except:
            print "Data causing exception: '{}', type = {}".format(data, type(data))
            raise
                
        self.length = len(self.data)
        self.pos = 0
        
    def empty(self):
        return self.pos >= self.length
        
    def __str__(self):
        return str(self.data[self.pos:])
    
    def __len__(self):
        return self.length - self.pos
    
    def read(self, n, peek=False):
        if n > len(self):
            print self.pos, self.length, len(self), n, repr(self.data)
            raise IndexError()
        try:
            #if n == 1:
            #    return bytearray((self.data[self.pos],))
            #else:
            return self.data[self.pos:self.pos+n]
        finally:
            if not peek: self.pos += n
            
    def getbyte(self, peek=False):
        try:
            return self.data[self.pos]
        finally:
            if not peek: self.pos += 1
        
    def getint(self, peek=False):
        c = self.getbyte(peek)
        
        if c == 0x80:
            t = self.read(3 if peek else 2, peek)
            if peek: t = str(t[1:])
            else: t = str(t)
            return struct.unpack('h', t)[0]
        elif c == 0x81:
            t = self.read(5 if peek else 4, peek)
            if peek: t = str(t[1:])
            else: t = str(t)
            return struct.unpack('i', t)[0]
        else:
            if(c & 0x80):
                return -0x100 + c
            return c
        
    def getuint(self, peek=False):
        n = self.getbyte()
        if(n & 0x80):
            n += (self.getbyte(peek) << 7) - 0x80;
            if(n & (1<<14)):
                n += (self.getbyte(peek) << 14) - (1<<14)
            if(n & (1<<21)): 
                n += (self.getbyte(peek) << 21) - (1<<21)
            if(n & (1<<28)): 
                n |= -1<<28
        return n;
        
    def getfloat(self, peek=False):
        return struct.unpack('<f', str(self.read(4, peek)))[0]
        
    def getstring(self, peek=False):
        try:
            for i in xrange(self.pos, self.length):
                if self.data[i] == 0:
                    return str(self.read(i-self.pos, peek))
        except:
            print repr(self.data)
            raise
        finally:
            if not peek: self.getbyte(peek) # Throw away the null terminator

