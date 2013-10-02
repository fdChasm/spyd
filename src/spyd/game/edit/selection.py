from cube2common.vec import vec
from spyd.utils.dictionary_get import dictget


arg_names = ('sel_ox', 'sel_oy', 'sel_oz', 'sel_sx', 'sel_sy', 'sel_sz', 'sel_grid', 'sel_orient', 'sel_cx', 'sel_cxs', 'sel_cy', 'sel_cys', 'sel_corner')

class Selection(object):
    @staticmethod
    def from_message(message):
        args = dictget(message, *arg_names)
        return Selection(*args)
    
    def __init__(self, sel_ox, sel_oy, sel_oz, sel_sx, sel_sy, sel_sz, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner):
        self.origin = vec(sel_ox, sel_oy, sel_oz)
        self.source = vec(sel_sx, sel_sy, sel_sz)
        
        self.grid_size = sel_grid
        self.orientation = sel_orient
        
        self.cx = sel_cx
        self.cxs = sel_cxs
        self.cy = sel_cy
        self.cys = sel_cys
        
        self.corner = sel_corner