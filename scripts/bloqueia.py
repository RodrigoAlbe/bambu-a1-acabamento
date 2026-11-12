# Pinta bloqueador de suporte (paint_supports="8") em todo triângulo virado pra baixo (normal z < 0) dentro das caixas.
# uso: python bloqueia.py <in.3mf> <out.3mf> xmin,xmax,ymin,ymax,zmin,zmax [...]
#   caixas em coordenadas do objeto (as que contatos.py imprime); só vale pra 3MF com 3D/Objects/object_1.model
import re, sys, zipfile
import numpy as np
CAIXAS = [tuple(map(float, a.split(','))) for a in sys.argv[3:]]
assert CAIXAS, 'passe ao menos uma caixa' 
zin = zipfile.ZipFile(sys.argv[1]); nome = '3D/Objects/object_1.model'
m = zin.read(nome).decode()
V = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', m), float)
tri_re = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"([^/]*)/>')
n = 0
def sub(mt):
    global n
    i = [int(mt.group(k)) for k in (1, 2, 3)]; p = V[i]; c = p.mean(0)
    nz = np.cross(p[1] - p[0], p[2] - p[0]); nz = nz[2] / (np.linalg.norm(nz) + 1e-12)
    if nz < 0 and any(a <= c[0] <= b and e <= c[1] <= f and g <= c[2] <= h for a, b, e, f, g, h in CAIXAS):
        assert 'paint_supports' not in mt.group(4); n += 1
        return f'<triangle v1="{i[0]}" v2="{i[1]}" v3="{i[2]}"{mt.group(4)} paint_supports="8"/>'
    return mt.group(0)
m2 = tri_re.sub(sub, m)
with zipfile.ZipFile(sys.argv[2], 'w', zipfile.ZIP_DEFLATED) as z:
    for it in zin.infolist(): z.writestr(it, m2 if it.filename == nome else zin.read(it))
print('triângulos bloqueados:', n)
