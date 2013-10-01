#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
import zlib
import gzip
import struct
from cube2common.constants import cs_id_types, MAXENTS, game_entity_types

def read_map_data(map_filename):
    meta_data = {'vars': {}, 'ents': []}
    
    with gzip.open(map_filename) as f:
        magic, version, headersize, worldsize, numents, numpvs, lightmaps = struct.unpack("4s6i", f.read(28))
        
        meta_data['version'] = version
        meta_data['worldsize'] = worldsize
        
        if version <= 28:
            lightprecision, lighterror, lightlod = struct.unpack("3i", f.read(12))
            
            ambient         = struct.unpack("B",   f.read(1))
            watercolor      = struct.unpack("3B",  f.read(3))
            blendmap        = struct.unpack("B",   f.read(1))
            lerpangle       = struct.unpack("B",   f.read(1))
            lerpsubdiv      = struct.unpack("B",   f.read(1))
            lerpsubdivsize  = struct.unpack("B",   f.read(1))
            bumperror       = struct.unpack("B",   f.read(1))
            skylight        = struct.unpack("3B",  f.read(3))
            lavacolor       = struct.unpack("3B",  f.read(3))
            waterfallcolor  = struct.unpack("3B",  f.read(3))
            reserved        = struct.unpack("10B", f.read(10))
            
            maptitle = struct.unpack("128s", f.read(128))
            
            meta_data['vars']['maptitle'] = maptitle
        else:
            if version <= 29:
                blendmap, numvars = struct.unpack("2i", f.read(8))
            else:
                blendmap, numvars, numvslots = struct.unpack("3i", f.read(12))
           
        if version <= 28:
            numvars = 0
    
        if version <= 29:
            numvslots = 0
    
        for i in xrange(numvars):
            var_type = struct.unpack("b", f.read(1))[0]
            ilen     = struct.unpack("<H", f.read(2))[0]
            var_name = f.read(ilen)
            if var_type == cs_id_types.ID_VAR:
                var_value = struct.unpack("i", f.read(4))[0]
            elif var_type == cs_id_types.ID_FVAR:
                var_value = struct.unpack("f", f.read(4))[0]
            elif var_type == cs_id_types.ID_SVAR:
                slen = struct.unpack("H", f.read(2))[0]
                var_value = f.read(slen)
                
            #print "{:.8}: {:.32s} = {}".format(cs_id_types.by_value(var_type), var_name, var_value)
            
            meta_data['vars'][var_name] = var_value
            
        if version >= 16:
            gt_len = struct.unpack("b", f.read(1))[0]
            game_type = f.read(gt_len+1)
        else:
            game_type = 'fps'
            
        meta_data['gametype'] = game_type

        if version >= 16:
            eif = struct.unpack("H", f.read(2))[0]
            extra_size = struct.unpack("H", f.read(2))[0]
            f.read(extra_size)
    
        if version < 14:
            f.read(256)
        else:
            nummru = struct.unpack("H", f.read(2))[0]
            f.read(nummru*2)
            
        for i in range(min(numents, MAXENTS)):
            x, y, z = struct.unpack("3f", f.read(12))
            attrs = struct.unpack('5h', f.read(10))
            ent_type, reserved = struct.unpack('2B', f.read(2))
            
            #if game_entity_types.by_value(ent_type) == "FLAG":
            #    print x, y, z, attrs, game_entity_types.by_value(ent_type), reserved
                
            ent = {'id': i, 'type': ent_type, 'x': x, 'y': y, 'z': z, 'attrs': attrs, 'reserved': reserved}
            meta_data['ents'].append(ent)
    
    try:
        with gzip.open(map_filename) as f:
            meta_data['crc'] = zlib.crc32(f.read()) & 0xffffffff
    except IOError:
        meta_data['crc'] = 0
        
    return meta_data