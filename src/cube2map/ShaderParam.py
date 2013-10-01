'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
class ShaderParam(object):
    def __init__(self, param_name, param_type):
        self.name = param_name
        self.type = param_type
        self.index = -1
        self.loc = -1
        self.val = []