'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
faceedgesidx = [ # ordered edges surrounding each orient
# 0..1 = row edges, 2..3 = column edges
    [ 4,  5,  8, 10 ],
    [ 6,  7,  9, 11 ],
    [ 8,  9,  0, 2  ],
    [ 10, 11, 1, 3  ],
    [ 0,  1,  4, 6  ],
    [ 2,  3,  5, 7  ],
]

def faceedges(c, orient, edges):
    for k in xrange(4):
        edges[k] = c.edges[faceedgesidx[orient][k]];