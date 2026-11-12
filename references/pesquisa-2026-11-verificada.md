# Veredito — acabamento A1 (verificador único, 04/11/2026)

Placar dos 60: 56 confirmados, 2 plausíveis, 1 refutado (r2#15) e 1 não conferido (r1#14: o Reddit está bloqueado e não tem cópia no Wayback).
O verificador baixou de novo todas as fontes (r2/v/), conferiu os presets do Bambu Studio 02.08.02.61 e o bulbasaur_verde_008.3mf, e deu nota com o Jev (`jev batch --noul`, 60/60 no backend Jev).
O Jev rodou 3 vezes. Da 1ª para a 2ª, a pergunta foi estreitada para "fatos atribuídos à fonte"; na 3ª, a evidência foi ampliada. A nota é da 3ª rodada; as três saídas estão em r2/jev_out.jsonl, jev_out2.jsonl e jev_out3.jsonl.
A nota foi sobrescrita em 11 itens, cada um com justificativa no campo `jev_override`.
Regra para claim composta: se o núcleo atribuído à fonte foi conferido, o achado sai CONFIRMADO, e o pedaço que não deu para conferir fica no campo `nota`.

## Conflitos com a skill

| # | Tema | Lado com fonte melhor | Decisão |
|---|------|-----------------------|---------|
| a | Flow Dynamics: auto × manual | **Skill.** A wiki da Bambu diz que a A1 calibra com sensor de corrente parasita e que o resultado é confiável, exceto com TPU, hotend de terceiros ou bico 0,2. O jitter é de uns 10%. O "desligar o auto depois" não aparece na legenda do LayerLab, e o Factorian só desliga o auto durante o teste no Orca | Manter o auto a cada carretel. O manual fica como teste opcional. Mudou a temperatura, recalibre (wiki) |
| b | Costura back × random | **Empate entre duas fontes da Bambu, sem A/B.** A wiki diz que random cria "zits". O vídeo oficial de 76 s diz que random combina com modelo orgânico ou texturizado | Manter `back` com o rosto virado pra frente da mesa (Loot). Random só em modelo com textura (pelo, escama) |
| c | Top Z distance 0,08 × 0,16 × 0,2 | **Ninguém mediu na A1 com camada 0,08.** O preset da A1 sempre iguala a distância à altura de camada (0,08, 0,12 ou 0,2). O "0,2 → 0,23" do Planet 3DP parte do perfil 0,20. Quem imprime em 0,08 fica acima de 0,1: 0,10 num comentário, piso de 0,11 no fórum, 0,15 no Painted4Combat (A1), 0,16 pela regra 2× do HOHansen | TESTAR 0,12 × 0,16 numa peça. Menor = face apoiada mais lisa e remoção mais difícil |
| d | Ordem das paredes | **Wiki.** Com a parede externa primeiro, ela fica em balanço no overhang. O Factorian avisa que inner-outer-inner com 2 paredes vira outer/inner, e o HQ da A1 tem `wall_loops=2` | Manter `inner wall/outer wall` |
| e | Parede externa lenta | **Nenhum A/B na A1.** No teste da Loot (X1), o perfil lento não mudou nada. O Painted4Combat (A1 Mini) dá só opinião. O fórum citado é de H2D cortando 5000→2500, e o HQ da A1 já usa 2000 | Manter 60 mm/s e 2000. Ir a 20–30 é teste de baixa prioridade |
| f | Ironing | **Wiki.** Num topo curvo, o ironing não tira a linha. No vídeo do 3D Geek, a impressora é Creality, o fatiador é o Creality Print, e o A/B junta camada variável com ironing | Descartar em figura. Manter `no ironing` |

## Aplicar no perfil (processo, valor conferido no 3MF → novo)

- `support_interface_top_layers` = 3 (hoje 2). Fontes: wiki e Planet 3DP.
- `reduce_crossing_wall` = 1 (hoje 0). Fonte: wiki. Conferir no fatiador quanto tempo soma. Não conferido: se `max_travel_detour_distance`=0 significa desvio sem limite.

## Testar antes, numa peça pequena (chave atual → teste)

1. `support_top_z_distance` 0.08 → 0.12 e 0.16 (conflito c).
2. `z_direction_outwall_speed_continuous` 0 → 1. A wiki cita figuras, mas diz que em modelo pequeno a diferença mal se nota.
3. `no_slow_down_for_cooling_on_outwalls` 0 → 1. É chave de filamento, então o `a1_convert.py` teria de gravar nos 4 slots. Risco: topo da cabeça com menos de 8 s de camada.
4. `precise_outer_wall` 0 → 1 (modo dev, nota de versão 2.1.0).
5. Também testar: `seam_slope_type` none → `external` (provavelmente o "Contour" da GUI; mapeamento não conferido) com `override_filament_scarf_seam_setting`=1 e `seam_slope_conditional`=1, que já está ligado; `support_interface_pattern` auto → `rectilinear_interlaced`; `tree_support_branch_diameter` 2 → 1.5; `top_area_threshold` 200% → 300%; `overhang_fan_threshold` 50% → 25%. Calibrar flow ratio (0.98) e fazer torre de temperatura: 205 (wiki, overhang) contra 215–220 (Factorian).

Nomes das chaves e valores de enum (`external`, `rectilinear_interlaced`, `tree_slim`, `inner-outer-inner wall`) conferidos no JSON do sistema, no 3MF e nas strings do binário 02.08.02.61.

## Descartar

- r2#15: "desligar o Flow Dynamics automático". A fonte não diz isso, e a wiki da A1 contradiz.
- r2#8: "Top Z 0,23–0,25". O número vale para camada 0,20, não para 0,08.
- r1#19 (aceleração pela metade): o relato é de H2D a 5000; a A1 já roda a 2000. r2#16 (PA adaptativo): só serve pra Klipper/Orca, e a A1 usa o Flow Dynamics automático.
- r1#14 (seam gap 20%): fonte única, não conferida, e o próprio autor diz que não resolveu.
- r2#20 (ironing): ver conflito f.

## Vira dica na skill (sem mudar o perfil)

- Girar o rosto para a frente antes de fatiar (a costura `back` vai pra trás dele). Inclinar 20–40° pra trás e deixar o rosto vertical.
- Não subir o tempo mínimo de camada: no A/B do Factorian, 150 s piorou.
- Peça única com camada presa em 8 s: imprimir 2 cópias (fórum, A1 mini).
- Arachne só se a pré-visualização perder dedo ou garra. O 10% do HOHansen tem um contraponto no mesmo post: 80% resolveu camada torta. Por isso ficou PLAUSÍVEL.
- Pós-processo (r3): conector Dowel, folga pino/furo entre 0,15 e 0,30 testada antes em cupom, CA gel, lixar as faces antes de colar, primer automotivo de enchimento, lixa de 320–400 até 600.

## Não verificado

Nada foi impresso. Os ganhos dos itens "testar" são das fontes, não medidos na A1 do autor.
Ficaram sem conferir: os 620 votos e o "thin wall sobrepõe paredes" (r1#4), o +4 min/21 h (r1#1), o relato X1C/Orca do precise wall (r1#6) e o arredondamento do top Z para múltiplo da camada.
