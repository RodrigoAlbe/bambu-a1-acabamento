# Lista os grupos de contato do suporte (interface) em coordenadas do objeto do 3MF.
# uso: .venv/bin/python contatos.py <s.3mf fatiado> <3mf fonte>
import re, sys, zipfile
import numpy as np
g = zipfile.ZipFile(sys.argv[1]).read('Metadata/plate_1.gcode').decode('utf8','replace').splitlines()
x=y=z=0.0; feat=''; peca=[]; it=[]; num=re.compile(r'([XYZE])(-?[\d.]+)')
for ln in g:
    if ln.startswith('; FEATURE:'): feat=ln[10:].strip().lower(); continue
    if not ln.startswith(('G1 ','G2 ','G3 ')): continue
    d=dict(num.findall(ln.split(';')[0])); x=float(d.get('X',x)); y=float(d.get('Y',y)); z=float(d.get('Z',z))
    if 'E' in d and float(d['E'])>0:
        if 'support interface' in feat: it.append((x,y,z))
        elif feat=='outer wall' and z>0.5: peca.append((x,y,z))  # bbox só da parede externa
peca=np.array(peca); it=np.array(it)
m=zipfile.ZipFile(sys.argv[2]).read('3D/Objects/object_1.model').decode()
V=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',m),float)
off=V.min(0)-peca.min(0); it=it+off
print('objeto min',V.min(0).round(1),'max',V.max(0).round(1))
# agrupa por camada de z (1 mm) e x (8 mm)
key=np.c_[np.round(it[:,2]), np.round(it[:,0]/8)]
for k in np.unique(key,axis=0):
    s=it[(key==k).all(1)]
    if len(s)<8: continue
    print(f'z≈{k[0]:5.0f}  x {s[:,0].min():6.1f}..{s[:,0].max():6.1f}  y {s[:,1].min():6.1f}..{s[:,1].max():6.1f}  n={len(s)}')
