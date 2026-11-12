#!/bin/zsh
# Fatia um 3MF com as configurações dele mesmo e imprime o que importa conferir.
# uso: slice_report.sh arquivo.3mf [--arrange]
#   --arrange: o Bambu redistribui as peças na placa (sem girar). Só funciona junto do slice.
set -e
f=${1:A}; out=${f:r}_slice; shift || true
extra=(); [[ "$1" == "--arrange" ]] && extra=(--arrange 1 --orient 0)
rm -rf $out; mkdir -p $out
/Applications/BambuStudio.app/Contents/MacOS/BambuStudio $extra --slice 0 --outputdir $out --export-3mf s.3mf $f > $out/log.txt 2>&1 \
  || { echo "FALHOU:"; grep -iE 'error|invalid' $out/log.txt | tail -5; exit 1; }
for g in $(unzip -Z1 $out/s.3mf | grep -E '^Metadata/plate_[0-9]+\.gcode$'); do
  echo "== $g"
  unzip -p $out/s.3mf $g | grep -E '^; (model printing time|total layer number|printer_model|layer_height|seam_position|support_style|max_z_height)[: ]' | head -8
  unzip -p $out/s.3mf $g | grep -cE '^M620 S[0-9]+A' | sed 's/^/M620 (1 = só a carga inicial; mais = trocas de cor): /'
done
unzip -p $out/s.3mf Metadata/slice_info.config | grep -E 'prediction|weight|warning' | grep -v timelapse
echo "saída: $out/s.3mf"
