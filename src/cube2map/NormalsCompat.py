'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.utils import readbvec

class NormalsCompat(object):
    normals = [0]*4
    
    @staticmethod
    def read(f):
        nc = NormalsCompat()
        nc.normals = map(lambda _: readbvec(f), xrange(4))
        return nc