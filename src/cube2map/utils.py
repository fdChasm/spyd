from cube2common.bvec import bvec
import ctypes
import struct

def clamp(a, b, c):
    return max(b, min(a, c))

def floor(v):
    return int(v)

def ushort(v):
    return ctypes.c_ushort(v)

def readchar(f):
    return struct.unpack('b', f.read(1))[0]

def readuchar(f):
    return struct.unpack('B', f.read(1))[0]

def readint(f):
    return struct.unpack("i", f.read(4))[0]

def readushort(f):
    return struct.unpack("H", f.read(2))[0]

def readfloat(f):
    return struct.unpack("f", f.read(4))[0]

def readbvec(f):
    return bvec(readuchar(f), readuchar(f), readuchar(f))