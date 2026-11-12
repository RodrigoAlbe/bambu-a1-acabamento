"""Gera layer_heights_profile.txt adaptativo + suave para um 3MF do Bambu.

Porta do SlicingAdaptive / smooth_height_profile do PrusaSlicer (base do Bambu Studio).
uso: python3 adaptive.py entrada.3mf saida.3mf [qualidade=0.5] [raio=5]
shortcut: next_layer_height simplificado (min das faces que cruzam a camada), igual ao
espírito do original mas não bit a bit; conferir no fatiamento.
"""
import json, re, sys, zipfile
import numpy as np

SURFACE_CONST = 0.18403
FIRST, LMIN, LMAX = 0.2, 0.08, 0.28

src, dst = sys.argv[1], sys.argv[2]
quality = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
radius = int(sys.argv[4]) if len(sys.argv) > 4 else 5

z = zipfile.ZipFile(src)
cfg = json.loads(z.read("Metadata/project_settings.config"))
LH = float(cfg["layer_height"])
d_min, d_mid, d_max = SURFACE_CONST * LMIN, (SURFACE_CONST + .5) * LH, (SURFACE_CONST + .5) * LMAX
dev = d_min + (d_mid - d_min) * 2 * quality if quality < .5 else d_max + (d_mid - d_max) * 2 * (1 - quality)

root = z.read("3D/3dmodel.model").decode()
comp = dict(re.findall(r'<object id="(\d+)"[^>]*>\s*<components>\s*<component p:path="/([^"]+)"', root))
xform = {o: np.array(t.split(), float) for o, t in re.findall(r'<item objectid="(\d+)"[^>]*transform="([^"]+)"', root)}
# object_id do perfil = posição em model.objects = ordem dos <object> com componentes no 3dmodel.model
order = list(comp)


def mesh(path):
    s = z.read(path).decode()
    v = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', s), float)
    f = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', s), int)
    return v, f


def profile(v, f, t):
    v = v @ t[:9].reshape(3, 3) + t[9:]  # 3MF: vetor linha * M
    v[:, 2] -= v[:, 2].min()
    tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    cos = np.abs(n[:, 2]); sin = np.sqrt(np.clip(1 - cos ** 2, 0, 1))
    with np.errstate(divide="ignore"):
        h = np.where(cos > 1e-5, 1.44 * dev * np.sqrt(sin / np.maximum(cos, 1e-12)), np.inf)
    zlo, zhi = tri[:, :, 2].min(1), tri[:, :, 2].max(1)
    keep = zhi - zlo > 1e-4  # faces horizontais não contam
    zlo, zhi, h = zlo[keep], zhi[keep], h[keep]
    o = np.argsort(zlo); zlo, zhi, h = zlo[o], zhi[o], h[o]
    top = v[:, 2].max()
    prof = [0., FIRST, FIRST, FIRST]
    pz = FIRST
    while pz + 1e-4 < top:
        hh = LMAX
        for _ in range(2):  # refina: faces dentro de [pz, pz+hh]
            k = np.searchsorted(zlo, pz + hh)  # faces que começam abaixo do topo da camada
            hh = float(np.clip(h[:k][zhi[:k] > pz + 1e-4].min(initial=LMAX), LMIN, LMAX))
        prof += [pz, hh]; pz += hh
    prof = smooth(prof)
    # o slicer descarta o perfil se o último z não for o topo do objeto (PrintObject::update_layer_height_profile)
    return prof + [top, float(np.clip(top - prof[-2], LMIN, LMAX))], top


def smooth(p):
    sigma = .3 * (radius - 1) + .8
    k = np.exp(-(np.arange(-radius, radius + 1) ** 2) / (2 * sigma ** 2))
    out = p[:4]
    for i in range(4, len(p), 2):
        num = den = 0.
        for j in range(max(i - 2 * radius, 4), min(i + 2 * radius, len(p) - 2) + 1, 2):
            w = k[radius + (j - i) // 2] * np.sqrt(abs(LMAX - p[j + 1]) / (LMAX - LMIN))
            num += w * p[j + 1]; den += w
        out += [p[i], float(np.clip(num / den if den else p[i + 1], LMIN, LMAX))]
    return out


lines = []
for idx, oid in enumerate(order, 1):
    v, f = mesh(comp[oid])
    p, top = profile(v, f, xform[oid])
    hs = np.array(p[5::2])
    print(f"obj {idx} id={oid} altura={top:.2f}mm camadas={len(hs)+1} h min/med/max={hs.min():.3f}/{hs.mean():.3f}/{hs.max():.3f}")
    lines.append(f"object_id={idx}|" + ";".join(f"{x:.6f}" for x in p))

assert len(lines) == len(order)
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
    for it in z.infolist():
        if it.filename in ("Metadata/layer_heights_profile.txt",) or it.filename.endswith(".gcode") or it.filename.endswith(".gcode.md5"):
            continue
        data = z.read(it.filename)
        if it.filename == "Metadata/project_settings.config" and cfg.get("support_style") == "tree_organic":
            cfg["support_style"] = "tree_slim"  # Bambu: camada variável não roda com suporte orgânico
            data = json.dumps(cfg, indent=4)
        out.writestr(it, data)
    out.writestr("Metadata/layer_heights_profile.txt", "\n".join(lines) + "\n")
print(f"qualidade={quality} desvio={dev:.4f} raio={radius} -> {dst}")
