'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.ivec import ivec

facecoords = (
    (
        ivec(0,8,8), ivec(0,8,0), ivec(0,0,0), ivec(0,0,8)
    )
    ,
    (
        ivec(8,8,8), ivec(8,0,8), ivec(8,0,0), ivec(8,8,0)
    )
    ,
    (
        ivec(8,0,8), ivec(0,0,8), ivec(0,0,0), ivec(8,0,0)
    )
    ,
    (
        ivec(0,8,0), ivec(0,8,8), ivec(8,8,8), ivec(8,8,0)
    )
    ,
    (
        ivec(0,0,0), ivec(0,8,0), ivec(8,8,0), ivec(8,0,0)
    )
    ,
    (
        ivec(0,0,8), ivec(8,0,8), ivec(8,8,8), ivec(0,8,8)
    ))