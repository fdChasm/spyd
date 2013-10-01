'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.VSlot import load_vslot, VSlot
from cube2map.utils import readint

def load_vslots(f, numvslots):
    vs = numvslots
    prev = {}
    vslots = []
    while vs > 0:
        changed = readint(f)
        if changed < 0:
            for _ in xrange(-changed):
                index = len(vslots)
                vslots.append(VSlot(index))
            vs += changed
        else:
            index = len(vslots)
            prev[index] = readint(f)
            vslots.append(load_vslot(f, index, changed))
            vs -= 1
            
    for i in xrange(len(vslots)):
        if prev[i] < len(vslots):
            vslots[prev[i]].next = vslots[i]
            
    return vslots