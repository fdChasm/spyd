'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.constants import material_types

def convertoldmaterial(mat):
    return ((mat&7) << material_types.MATF_VOLUME_SHIFT) | (((mat>>3)&3) << material_types.MATF_CLIP_SHIFT) | (((mat>>5)&7) << material_types.MATF_FLAG_SHIFT)