# Acha onde cada galho de suporte termina encostando na peça (até 0,4 mm abaixo dela) (qualquer tipo de suporte, não só interface), em coordenadas do objeto.
# uso: python3 pontas.py <s.3mf fatiado> <fonte.3mf> [zmin_objeto]
import re, sys, zipfile
import numpy as np
from collections import defaultdict
g = zipfile.ZipFile(sys.argv[1]).read('Metadata/plate_1.gcode').decode('utf8','replace').splitlines()
zmin = float(sys.argv[3]) if len(sys.argv) > 3 else 0
x=y=z=0.0; feat=''; peca=[]; sup=defaultdict(set); pc=defaultdict(set); num=re.compile(r'([XYZE])(-?[\d.]+)'); C=0.5
for ln in g:
    if ln.startswith('; FEATURE:'): feat=ln[10:].strip().lower(); continue
    if not ln.startswith(('G1 ','G2 ','G3 ')): continue
    d=dict(num.findall(ln.split(';')[0])); nx=float(d.get('X',x)); ny=float(d.get('Y',y)); z=float(d.get('Z',z))
    if 'E' in d and float(d['E'])>0:
        if 'support' in feat:
            for t in np.linspace(0,1,max(2,int(np.hypot(nx-x,ny-y)/C)+1)):
                sup[round(z,2)].add((int((x+(nx-x)*t)/C), int((y+(ny-y)*t)/C)))
        elif z>0.5:
            if feat=='outer wall': peca.append((nx,ny,z))  # bbox só da parede externa (brim/skirt deslocavam)
            for t in np.linspace(0,1,max(2,int(np.hypot(nx-x,ny-y)/C)+1)):
                pc[round(z,2)].add((int((x+(nx-x)*t)/C), int((y+(ny-y)*t)/C)))
    x,y=nx,ny
peca=np.array(peca)
zf=zipfile.ZipFile(sys.argv[2]); m=zf.read(sorted(n for n in zf.namelist() if n.startswith('3D/Objects/') and n.endswith('.model'))[0]).decode()  # nem sempre é object_1
V=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',m),float); off=V.min(0)-peca.min(0)
zs=sorted(sup); tops=[]
for a,b in zip(zs, zs[1:]+[None]):
    acima=sup[b] if b is not None else set()
    viz=lambda c: any((c[0]+i,c[1]+j) in acima for i in (-1,0,1) for j in (-1,0,1))
    cima=set().union(*[pc.get(round(a+0.08*k,2),set()) for k in range(1,6)])  # peça até 0,4 mm acima
    toca=lambda c: any((c[0]+i,c[1]+j) in cima for i in (-1,0,1) for j in (-1,0,1))
    tops += [(c[0]*C, c[1]*C, a) for c in sup[a] if not viz(c) and toca(c)]
T=np.array(tops)+off; T=T[T[:,2]>zmin]
key=np.c_[np.round(T[:,2]/2)*2, np.round(T[:,0]/6), np.round(T[:,1]/6)]
for k in np.unique(key,axis=0):
    s=T[(key==k).all(1)]
    if len(s)>=3: print(f'z≈{k[0]:4.0f}  x {s[:,0].mean():6.1f}  y {s[:,1].mean():6.1f}  n={len(s)}')
