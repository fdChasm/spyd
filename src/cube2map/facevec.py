'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.errors import InvalidOverloadArguments
class facevec(object):
    x = 0
    y = 0
    
    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.x, self.y = args
        else:
            raise InvalidOverloadArguments()
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
