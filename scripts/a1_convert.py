"""Converte um 3MF de qualquer impressora Bambu para A1 0.4 com perfil de acabamento.

uso: python3 a1_convert.py <camada> <origem.3mf> <saida.3mf> [cor1,cor2,...] [chave=valor ...]
ex.: python3 a1_convert.py 0.08 dl/modelo.3mf modelo_a1.3mf '#00AE42' support_on_build_plate_only=1

O que faz: base = project_settings de um projeto A1 salvo pela GUI (assets/), por cima o
processo "<camada>mm High Quality @BBL A1" resolvido pela cadeia `inherits` dos presets do
sistema, todos os slots = Generic PLA @BBL A1, e os overrides de acabamento abaixo.
Geometria, pintura, placas e perfil de camada do 3MF de origem ficam intactos.
Por que não `--load-settings` do CLI: o merge sai quebrado (camada 0.2, start gcode G28 de outra impressora).
"""
import json, os, sys, zipfile

SYS = os.path.expanduser('~/Library/Application Support/BambuStudio/system/BBL/')
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'a1_base_project_settings.json')
SKIP = {'name', 'inherits', 'from', 'instantiation', 'setting_id', 'compatible_printers',
        'compatible_printers_condition', 'description', 'type', 'filament_id'}
FIL_PREFIX = ('filament_', 'nozzle_temperature', 'hot_plate', 'textured_plate', 'cool_plate', 'eng_plate',
              'supertack', 'fan_', 'slow_down', 'overhang_fan', 'close_fan', 'additional_cooling', 'reduce_fan',
              'full_fan', 'temperature_vitrification', 'required_nozzle_HRC', 'pressure_advance',
              'enable_pressure_advance', 'activate_air', 'during_print_exhaust', 'complete_print_exhaust',
              'chamber_temp', 'default_filament_colour', 'nozzle_temperature_range')
OVERRIDES = {'enable_support': '1', 'support_type': 'tree(auto)', 'support_style': 'tree_organic',
             'support_threshold_angle': '30', 'sparse_infill_pattern': 'gyroid',
             'sparse_infill_density': '10%', 'seam_position': 'back',
             # pesquisa verificada 04/11/2026 (wiki Bambu): face apoiada mais lisa; menos marca de viagem na parede
             'support_interface_top_layers': '3', 'reduce_crossing_wall': '1'}


def preset(kind, name):
    chain = []
    while name:
        d = json.load(open(f'{SYS}{kind}/{name}.json')); chain.append(d); name = d.get('inherits')
    out = {}
    for d in reversed(chain): out.update(d)
    return out


layer, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
cores = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else ['#FFFFFF']
extra = dict(a.split('=', 1) for a in sys.argv[5:])

proc = preset('process', f'{layer}mm High Quality @BBL A1')
d = json.load(open(BASE))
d.update({k: v for k, v in proc.items() if k not in SKIP})
n = len(d['filament_settings_id'])
for k, v in list(d.items()):
    if k.startswith(FIL_PREFIX) and isinstance(v, list) and len(v) == n:
        d[k] = [v[0]] * n  # slot 0 da base = Generic PLA @BBL A1
d['filament_colour'] = (cores * n)[:n]
# Mesa BIQU CryoGrip Pro Frostbite: BIQU diz PLA 30 °C / PETG 50 °C e mapeia a placa como a
# "Low Temperature/Cool Plate" da Bambu. Cool Plate também tira o G29.1 Z-0.02 que a A1 só usa na Textured PEI.
d['curr_bed_type'] = 'Cool Plate'
# 40 °C, não 30: 30 é o mínimo da BIQU e figura pequena soltou da mesa (luminária, 08/11/2026); donos relatam soltar a ~33 °C.
d['cool_plate_temp'] = d['cool_plate_temp_initial_layer'] = ['40'] * n
d['print_settings_id'] = f'{layer}mm High Quality @BBL A1'
# Purga do autor: a da base é de outro projeto (no boneco de neve, preto->branco caía de 650 para 128 e mancharia o branco).
# shortcut: a matriz é a das cores do autor; troca de cor muito mais clara (laranja->amarelo) pede ajuste à mão.
srcd = json.loads(zipfile.ZipFile(src).read('Metadata/project_settings.config'))
if len(srcd.get('flush_volumes_matrix', [])) == n * n:
    d['flush_volumes_matrix'] = srcd['flush_volumes_matrix']
    d['flush_multiplier'] = srcd.get('flush_multiplier', d.get('flush_multiplier'))
over = {**OVERRIDES, **extra}
d.update(over)
# guia da Bambu p/ A1 (mesa que se move derruba peça alta/estreita): viagem <= 400 mm/s, acelerações <= 3000 (08/11/2026)
MOV = {'travel_speed': '400', 'travel_acceleration': '3000', 'default_acceleration': '3000'}
for k, v in MOV.items(): d[k] = [v] if isinstance(d.get(k), list) else v
diff = [k for k in sorted(over) if str(proc.get(k)) != over[k]] + [k for k in MOV if k not in over]
# [processo, filamento 1..n, máquina]; nos filamentos só a temperatura da mesa difere do preset
d['different_settings_to_system'] = [';'.join(diff)] + ['cool_plate_temp;cool_plate_temp_initial_layer'] * n + ['']

zin = zipfile.ZipFile(src)
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    for it in zin.infolist():
        if it.filename.endswith(('.gcode', '.gcode.md5')):
            continue  # G-code antigo é da outra impressora
        data = zin.read(it.filename)
        if it.filename == 'Metadata/project_settings.config':
            data = json.dumps(d, indent=4, ensure_ascii=False).encode()
        z.writestr(it, data)
print(dst, 'overrides fora do preset:', diff)
