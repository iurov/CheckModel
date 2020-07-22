import numpy as np
from os import listdir
from os.path import isfile, join

k = 0
class WavefrontOBJ:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None              
        self.mtllibs   = []                 
        self.mtls      = [ default_mtl ]    
        self.mtlid     = []                 
        self.vertices  = []                 
        self.normals   = []                 
        self.texcoords = []                 
        self.polygons  = []                 

def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:
    def parse_vertex( vstr ):
        vals = vstr.split('/')
        vid = int(vals[0])-1
        tid = int(vals[1])-1 if len(vals) > 1 and vals[1] else -1
        nid = int(vals[2])-1 if len(vals) > 2 else -1
        return (vid,tid,nid)
        global k
        k=0

    
    try:
        with open( filename, 'r' ) as objf:
            obj = WavefrontOBJ(default_mtl=default_mtl)
            obj.path = filename
            cur_mat = obj.mtls.index(default_mtl)
            for line in objf:
                toks = line.split()
                if not toks:
                    continue
                if toks[0] == 'v':
                    obj.vertices.append( [ float(v) for v in toks[1:]] )
                elif toks[0] == 'vn':
                    obj.normals.append( [ float(v) for v in toks[1:]] )
                elif toks[0] == 'vt':
                    obj.texcoords.append( [ float(v) for v in toks[1:]] )
                elif toks[0] == 'f':
                    poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                    if triangulate:
                        for i in range(2,len(poly)):
                            obj.mtlid.append( cur_mat )
                            obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
                    else:   
                        obj.mtlid.append(cur_mat)
                        obj.polygons.append( poly )
                elif toks[0] == 'mtllib':
                    obj.mtllibs.append( toks[1] )
                elif toks[0] == 'usemtl':
                    if toks[1] not in obj.mtls:
                        obj.mtls.append(toks[1])
                    cur_mat = obj.mtls.index( toks[1] )
            return obj
    except:
        try:
            with open( filename, 'r', encoding='utf8') as objf:
                obj = WavefrontOBJ(default_mtl=default_mtl)
                obj.path = filename
                cur_mat = obj.mtls.index(default_mtl)
                for line in objf:
                    toks = line.split()
                    if not toks:
                        continue
                    if toks[0] == 'v':
                        obj.vertices.append( [ float(v) for v in toks[1:]] )
                    elif toks[0] == 'vn':
                        obj.normals.append( [ float(v) for v in toks[1:]] )
                    elif toks[0] == 'vt':
                        obj.texcoords.append( [ float(v) for v in toks[1:]] )
                    elif toks[0] == 'f':
                        poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                        if triangulate:
                            for i in range(2,len(poly)):
                                obj.mtlid.append( cur_mat )
                                obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
                        else:   
                            obj.mtlid.append(cur_mat)
                            obj.polygons.append( poly )
                    elif toks[0] == 'mtllib':
                        obj.mtllibs.append( toks[1] )
                    elif toks[0] == 'usemtl':
                        if toks[1] not in obj.mtls:
                            obj.mtls.append(toks[1])
                        cur_mat = obj.mtls.index( toks[1] )
                return obj
        except:
            print('Неверный форматъ файла')
            global k
            k=1

def save_obj( obj: WavefrontOBJ, filename: str ):
    """Saves a WavefrontOBJ object to a file

    Warning: Contains no error checking!

    """
    with open( filename, 'w' ) as ofile:
        for mlib in obj.mtllibs:
            ofile.write('mtllib {}\n'.format(mlib))
        for vtx in obj.vertices:
            ofile.write('v '+' '.join(['{}'.format(v) for v in vtx])+'\n')
        for tex in obj.texcoords:
            ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
        for nrm in obj.normals:
            ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
        if not obj.mtlid:
            obj.mtlid = [-1] * len(obj.polygons)
        poly_idx = np.argsort( np.array( obj.mtlid ) )
        cur_mat = -1
        for pid in poly_idx:
            if obj.mtlid[pid] != cur_mat:
                cur_mat = obj.mtlid[pid]
                ofile.write('usemtl {}\n'.format(obj.mtls[cur_mat]))
            pstr = 'f '
            for v in obj.polygons[pid]:
                # UGLY!
                vstr = '{}/{}/{} '.format(v[0]+1,v[1]+1 if v[1] >= 0 else 'X', v[2]+1 if v[2] >= 0 else 'X' )
                vstr = vstr.replace('/X/','//').replace('/X ', ' ')
                pstr += vstr
            ofile.write( pstr+'\n')

def triang(name_obj, name_mtl, name_save):
    obj = load_obj( name_obj, default_mtl=name_mtl, triangulate=True )
    save_obj( obj, name_save)