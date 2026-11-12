# Mede os troncos do suporte numa altura: quantos e o diâmetro de cada (pelo trajeto de suporte na camada).
# uso: .venv/bin/python troncos.py <s.3mf> <z_mm>
import re, sys, zipfile
import numpy as np
from scipy.ndimage import label
zalvo = float(sys.argv[2]); g = zipfile.ZipFile(sys.argv[1]).read('Metadata/plate_1.gcode').decode('utf8','replace').splitlines()
x=y=z=0.0; feat=''; pts=[]; num=re.compile(r'([XYZE])(-?[\d.]+)')
for ln in g:
    if ln.startswith('; FEATURE:'): feat=ln[10:].strip().lower(); continue
    if not ln.startswith(('G1 ','G2 ','G3 ')): continue
    d=dict(num.findall(ln.split(';')[0])); nx=float(d.get('X',x)); ny=float(d.get('Y',y)); z=float(d.get('Z',z))
    if 'E' in d and float(d['E'])>0 and 'support' in feat and abs(z-zalvo)<0.05:
        for t in np.linspace(0,1,max(2,int(np.hypot(nx-x,ny-y)/0.2))): pts.append((x+(nx-x)*t, y+(ny-y)*t))
    x,y=nx,ny
p=np.array(pts); c=0.25; lo=p.min(0); ij=((p-lo)/c).astype(int); grid=np.zeros(ij.max(0)+1,bool); grid[ij[:,0],ij[:,1]]=True
from scipy.ndimage import binary_closing
lab,n=label(binary_closing(grid,iterations=3)); diam=[2*np.sqrt((lab==k).sum()*c*c/np.pi) for k in range(1,n+1)]
diam=sorted([d for d in diam if d>0.8])
print(f'z={zalvo}: {len(diam)} troncos; diâmetro mediana {np.median(diam):.1f} mm, menor {diam[0]:.1f}, maior {diam[-1]:.1f}')
