'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.constants import empty_material_types

def isclipped(mat):
    return mat == empty_material_types.MAT_GLASS