---
name: bambu-a1-acabamento
description: Prepara um modelo (MakerWorld, 3MF ou STL) para imprimir na Bambu Lab A1 0.4 com AMS lite com o melhor acabamento possível. Baixa o 3MF pelo Safari logado, converte o perfil de outra impressora (P1S, X1C, P2S) para a A1, escolhe a altura de camada medindo (0,08 uniforme × 0,12 × camada adaptativa), corta o desperdício de purga e une placas. Fatia pelo CLI do Bambu, confere o G-code e abre no Bambu Studio. Use sempre que o usuário mandar um link do MakerWorld ou Printables, pedir pra imprimir "da melhor forma", "bem liso", "profissional" ou "parecendo resina", perguntar de camada adaptativa ou variável, linha de camada, marca no topo da peça, costura, suporte, purga ou desperdício do AMS, ou pedir pra deixar tudo de uma cor ou numa placa só. Também cobre o checklist antes de apertar Imprimir (slot, Flow Dynamics, filamento úmido) e o acabamento depois (pintura, fosco).
---

# Acabamento profissional na Bambu A1

Objetivo: arquivo pronto, aberto no Bambu Studio, com tempo e peso medidos no fatiador. Quem aperta Imprimir é sempre o usuário, nunca mande imprimir.

Equipamento do autor (troque pelo seu): Bambu Lab A1, bico 0,4, AMS lite, mesa **BIQU CryoGrip Pro Frostbite** (desde 04/11/2026; antes era Textured PEI). Na Frostbite, o `a1_convert.py` já grava o tipo "Cool Plate" com PLA a 40 °C (desde 08/11: com 30 uma figura soltou), viagem 400 mm/s e aceleração 3000. Pela wiki da BIQU: PLA 30 °C (mínimo), PETG 50 °C, só PLA/PETG/ABS, e limpeza só com água e sabão, sem álcool. Se a A1 reclamar da mesa, desligue a detecção de placa nas configurações da impressora. Se ainda soltar, 45 °C. Os filamentos não são da Bambu: use Generic PLA @BBL A1. Cores em casa: preto (fosco), branco, vermelho, amarelo e verde (brilhante). Pergunte qual slot usar, porque o slot 1 já travou ao puxar filamento.

## Fluxo

1. **Baixar.** `scripts/makerworld.sh info <designId>` lista os perfis com tempo e peso. Compare as versões "NO AMS" e AMS: a AMS de um boneco pequeno costuma ser 80–90% purga (Bulbasaur: 24 g sem AMS contra 144 g com AMS). Depois `scripts/makerworld.sh get <instanceId> dl/modelo.3mf`. O curl direto toma bloqueio da Cloudflare; o Safari já está logado.
2. **Olhar o modelo antes de mexer.** Abra o zip: `Metadata/model_settings.config` (objetos, placas, extrusor), `project_settings.config` (impressora, camada, suporte e o que o autor mudou em `different_settings_to_system`) e `Metadata/plate_1.png`. Mantenha as escolhas deliberadas do autor, como `support_on_build_plate_only`.
3. **Converter para a A1.** `python3 scripts/a1_convert.py <camada> dl/modelo.3mf saida.3mf '<cor>' [chave=valor]`. Ele aplica: processo High Quality A1, Generic PLA em todos os slots, suporte tree organic com ângulo 30, gyroid 10% e costura atrás. Rode com `python3` sem `-I`, porque o numpy está no user site.
4. **Escolher a camada medindo.** Veja a seção abaixo; isso decide a qualidade da superfície.
5. **Fatiar e conferir.** `scripts/slice_report.sh saida.3mf` (some `--arrange` se juntou peças numa placa). Confira: `printer_model = Bambu Lab A1`, a camada certa, `seam_position = back`, M620 = 1 se a peça é de uma cor, e nenhum warning além do timelapse.
   Figura com suporte: rode `python3 scripts/pontas.py <fatiado/s.3mf> <fonte.3mf>` e veja onde o suporte encosta (seção abaixo). Rode com `zsh`, não `bash`, o `slice_report.sh`.
6. **Abrir e passar o checklist.** `open -a BambuStudio saida.3mf` e mande o checklist de impressão abaixo.

## Altura de camada: o que aprendemos

Linha de camada aparece onde a superfície é quase horizontal: topo de cabeça, domo, barriga. Numa parede vertical ela quase não aparece. Por isso a escolha depende da forma da peça, e o critério é sempre fatiar as opções e comparar o tempo.

- **Figura orgânica (bicho, chibi, boneco): 0,08 uniforme é o padrão.** Na gecko, a camada adaptativa do autor deixava 0,12–0,15 no topo raso da cabeça e saíram anéis visíveis em PLA brilhante. Com 0,08 na peça toda o resultado ficou "bem melhor". Numa peça toda curva, a adaptativa acaba em ~0,08 quase em toda parte, então não economiza tempo.
- **Camada adaptativa (`scripts/adaptive.py`) só vale com estas três condições:** uma peça só na placa (ou todas iguais), paredes retas ou verticais em boa parte da altura, e suporte que não seja orgânico. O próprio reel que ensinou isso usou uma peça única. No Jolteon (10 peças) a adaptativa deu 8h20–8h33, contra 7h44 em 0,08 uniforme: cada peça ganha alturas próprias e o número de camadas quase dobra.
- **Mesmo com peça única, a adaptativa ganha pouco num bicho redondo.** No Bulbasaur (47 mm), a qualidade 0,5 ficou em ~0,08 em quase tudo: 2h40, igual ao 0,08 uniforme (2h39). A qualidade 0,7 levou 2h22 (−17 min), mas subiu para 0,10–0,15 nas encostas a 45°, justamente a faixa que marcou a gecko. Pra acabamento máximo, não vale.
- **0,12:** use quando o tempo pesa mais e a peça tem pouco topo raso. O Jolteon caía de ~8h40 para ~5h50 nas três placas.
- **Peça grande com topo curvo e laterais retas:** gere a adaptativa e fatie contra o 0,08. Fique com a adaptativa só se ela ganhar tempo sem engrossar o topo.

Detalhes do `adaptive.py` que custaram horas (está tudo tratado no script):
- O CLI do Bambu não calcula a camada adaptativa; o script porta o algoritmo do Prusa/Bambu (qualidade 0–1, suave com raio 5).
- `object_id=N` no `layer_heights_profile.txt` é a posição na ordem dos `<object>` do `3D/3dmodel.model`, não a do `model_settings`.
- O último z do perfil tem que ser exatamente o topo do objeto. Se não for, o slicer descarta o perfil sem avisar e o fatiamento sai idêntico ao uniforme. Sempre confira se o número de camadas mudou.
- Camada variável com `support_style = tree_organic` dá erro de validação. O script troca para `tree_slim`, que sozinho já custa alguns minutos a mais.

## Suporte em figura: onde encosta e quão grosso (Funko de 4 figuras, 05/11)

O galho subir pela frente na tela não quer dizer que toca o rosto: a maioria só segura embaixo do queixo. Meça antes de mexer.
- **Onde encosta:** `scripts/pontas.py` lista onde cada galho termina com peça logo acima, em coordenadas do objeto (y negativo = frente, se o rosto está virado pra frente da mesa). Queixo e nuca podem ficar; no rosto, bloqueie. Não confie só no `contatos.py`: ele conta só a camada de interface, e no Funko de 4 figuras deixou passar ~40 pontas finas no rosto (óculos, olhos, nariz) que o usuário viu na tela.
- **Bloquear o rosto:** `python3 scripts/bloqueia.py in.3mf out.3mf xmin,xmax,ymin,ymax,zmin,zmax ...` pinta bloqueador (`paint_supports="8"`) nos triângulos virados pra baixo dentro de cada caixa. Bloqueie o rosto inteiro de cada figura, da frente (y < −5) e de 1–3 mm acima do queixo pra cima, não ponto a ponto. Fatie de novo e confira com o `pontas.py`. No Funko de 4 figuras: de ~40 contatos no rosto para 2 pontinhos que o bloqueio não tira.
- **Baixar o ângulo não tira suporte do rosto:** nariz e queixo são quase planos. 30° → 20° → 15° cortou tempo (12h46 → 11h57 → 11h25) com os mesmos contatos.
- **Precisa de suporte?** Fatie com `enable_support=0` pra saber o custo (Funko de 4 figuras: 8h20/62 g contra 12h37/85 g). Cabeça de Funko mais larga que o corpo é teto (30 mm embaixo da cabeça do homem): sem suporte, desaba.
- **O tronco engorda por `tree_support_branch_diameter_angle`** (padrão 5°), não pelo `branch_diameter`. `scripts/troncos.py <s.3mf> <z>` mede os troncos numa altura. No Funko de 4 figuras, com o perfil 0,08:
  - 5°: 9 troncos de 5,4 mm na mesa e 24 g de suporte.
  - 2°: 13 troncos de 2,8 mm e 15 g. É o candidato.
  - 0°: só 2 troncos chegam na mesa, de 1,3 mm a 30 mm de altura e 9 g. O resto pousa na peça e pode tombar; não use.
- **Base do suporte a 1 camada da peça:** o 0,08 da A1 vem com `support_bottom_z_distance` 0,08. Onde o tronco pousa no corpo, isso pode ser o que arranca pedaço. 0,16 é o candidato, igual ao top.
- **Letra em relevo também ganha suporte:** a base de cada letra é uma saliência de ~0,6 mm, e o slicer apoia. Bloqueie a área do texto junto com o rosto (imprime sem suporte).
- **Texto errado do Tripo (BKARIL, BRASN...):** confira com render só da geometria antes de fatiar (script local do autor, não incluído). Pra corrigir: um script local (não incluído) ajusta uma superfície lisa na blusa, leva as letras velhas pra ela e cola o texto novo em DIN Alternate Bold engrossada 0,1 mm (traço ≥ 0,85 mm pro bico 0,4). Confira na vista de frente inteira se outra figura tapa o texto.
- **Ainda sem teste impresso:** 2° e bottom 0,16 só foram fatiados. A ponta fica fixa em 0,8 mm na 2.08; `tree_support_tip_diameter` só existe na 2.09 (ponta menor deixa menos marca).
- Outras técnicas, com fonte em `references/suporte-figura-2026-11.md`: inclinar 30–45° pra olho e sobrancelha dispensarem suporte, e remover depois de esfriar, girando, sem puxar (Painted4Combat).
- **Orientar pela vista** (AngelMaker): o suporte vai pra face que ninguém vê. A perna pode ir de cabeça pra baixo, com o suporte dentro da cintura. Capacete e cabeça nunca virados pra cima (o rosto continua pra frente da mesa, como o `pontas.py` espera), porque é no topo que fica o anel. Base e pedras podem sair em 0,20.

## Outros ajustes que funcionaram

- **Uma cor só:** tire os atributos `paint_color` dos triângulos em `3D/Objects/*.model` e ponha todos os objetos no extrusor 1. Isso some com a torre de limpeza e a purga (gecko: de 20,6 g para 2,8 g).
- **Várias placas numa só:** passe todas as instâncias para a placa 1 em `model_settings.config` e fatie com `--arrange` (sem girar, para manter a orientação do autor). Confira `Metadata/top_1.png` pra ver se alguma peça ficou sobreposta. O ganho é pequeno (Jolteon: −55 min), e o risco é perder tudo se falhar.
  - Multicolor em multipart (Zapach): juntar placas de cores diferentes piora (2h45 + 28 min → 4h40). Se juntar, use `print_sequence = by object`, que imprime uma peça inteira de cada vez (→ ~2h). Só funciona se o cabeçote não bater nas peças já prontas.
- **Multicolor com menos purga:** `flush_volumes_matrix[de*n + para]`. Baixe as trocas para o preto (gecko: 608 → 150) e confira no G-code se não manchou.
- **Costura:** `back`, ou pintada à mão numa face escondida. Antes de fatiar, gire a peça para o rosto ficar virado pra frente da mesa; assim a costura vai para a nuca. `random` cria pontinhos; só serve em textura (pelo, escama).
- **Já no `a1_convert.py` (pesquisa verificada de 04/11):** `support_interface_top_layers=3`, que deixa a face apoiada no suporte mais lisa, e `reduce_crossing_wall=1`, que reduz marca de viagem. No Bulbasaur o custo foi zero (2h39 → 2h39).
- **Mantidos de propósito (a fonte apoia a skill):**
  - Flow Dynamics automático a cada carretel: a A1 mede com sensor e a wiki diz que é confiável.
  - Paredes inner/outer. O William Lins (ago/2026, busto, sem A/B) defende outer/inner pra não esbarrar na casca; continua fora, porque cede em overhang.
  - Parede externa a 60 mm/s. Imprimir a 50% da velocidade não esconde linha de camada (A/B do NuggetsInclusive, 2026). O 3D Max Builds ganhou ao baixar de 200 para 30, mas a A1 já sai de 60.
  - Sem ironing: não alisa topo curvo.
  - Não subir o tempo mínimo de camada: no A/B do Factorian, 150 s piorou.
- Face plana apoiada na mesa copia a textura da mesa. A Frostbite é lisa (confirmado 04/11), então a face de baixo sai lisa e sem linha de camada: em chaveiro, plaquinha ou base, vire a frente pra baixo.
- **Peça plana ou geométrica (chaveiro plano, placa, dado, base), nunca figura:** frente pra baixo na Frostbite; `wall_sequence=outer wall/inner wall` (parede externa mais regular, mas cede em overhang); ironing em todo topo plano (`ironing_type=top`, "All top surfaces" na GUI; conferir o valor na GUI); primeira camada mais lenta (`initial_layer_speed` 50 e `initial_layer_infill_speed` 105 no HQ da A1 → 20–30). Candidato ainda sem A/B: topo a 20 mm/s e aceleração 800 (item 7 abaixo). Fonte: 3D Max Builds, set/2026, A/B impresso em dado, em outra impressora.
- **Peça única muito pequena** (camada travando em 8 s): imprima 2 cópias para dar tempo de esfriar.
- **Ímã escondido:** faça uma parte negativa do tamanho do ímã, 0,5 mm abaixo do topo. Ponha uma pausa na camada em que o furo ainda está aberto e alterne os polos.
- **Escalar peça com encaixe:** a folga escala junto. Corrija com `xy_contour_compensation` negativo (diferença medida − 0,1 a 0,2) na peça que entra.
- **Detalhe fino sumindo na pré-visualização** (dedo, garra): teste o gerador de parede Arachne. Fora isso, fique no Classic, que trata melhor o overhang.
- **Não fazer:** `--load-settings` no CLI (o merge sai quebrado); escrever presets em `user/<id>/` (precisam de `.info` e o app sobrescreve); fuzzy skin, lixa ou primer em peça articulada (trava as juntas).

## Ainda falta teste impresso na A1 (não aplicar às cegas)

As fontes conferem, mas ninguém mediu isto numa A1 em 0,08. Quando o usuário quiser espremer mais qualidade, faça um A/B numa peça pequena (uma mudança por vez) e julgue a peça impressa, não a pré-visualização:
1. `support_top_z_distance` 0,08 → 0,12 e 0,16. Distância menor deixa a face apoiada mais lisa, mas o suporte sai mais difícil. O "0,23" do Planet 3DP vale para camada 0,20. **Sinal impresso (3D Max Builds, camada 0,08, outra impressora):** com 0,08 o suporte arrancou pedaço da peça, com 0,24 a face cedeu, e 0,16 foi o melhor. O A/B do Charizard (0,08 × 0,16) confirma isso na A1. Alternativa com AMS: só a interface do suporte em PETG com distância 0 (PLA e PETG não grudam), ao custo de muita purga.
2. `z_direction_outwall_speed_continuous` = 1. A wiki cita figuras, mas avisa que em modelo pequeno quase não se nota.
3. `no_slow_down_for_cooling_on_outwalls` = 1. É chave de filamento: grave nos 4 slots. Risco: topo da cabeça esfriar menos.
4. `precise_outer_wall` = 1.
5. **Precisão (KostaWorks, A1 + Frostbite, mesma combinação do autor):** `resolution` 0,012 → 0,002 e `slice_closing_radius` 0,049 → 0,002. No vídeo apareceram argola do nariz, dentes e fios de cabelo que sumiam. Fatiado no Bulbasaur em 04/11: mesmo tempo (2h38m47 × 2h38m53) e mesmo peso, com 66% mais movimentos no G-code (358k → 595k). O ganho é de detalhe minúsculo; teste em peça com rosto ou detalhe fino.
6. Scarf seam (`seam_slope_type=external` + `override_filament_scarf_seam_setting=1`; no dado do 3D Max Builds a costura ficou visivelmente menor), torre de temperatura (205 × 215–220 °C) e flow ratio manual.
7. **Topo mais lento** (3D Printed Mom, reel de 23/09/2026, P2S 0,08 HQ): `top_surface_speed` 150 → 20 e `top_surface_acceleration` 2000 → 800. O HQ 0,08 da A1 sai com os mesmos 150 e 2000. O vídeo só mostra peças prontas, sem A/B. Fatiado na Funko de 4 figuras em 05/11: 12h44 contra 12h46, de graça, porque o resfriamento mínimo já freia a camada pequena. Em peça plana e larga o tempo deve subir; meça antes.
8. **Interface do suporte mais densa** (5 vídeos do grupo de impressão 3D, 07/11, em camada 0,12–0,20, nenhum com A/B): os cinco concordam na direção, mais camadas de interface e interface mais fechada. `support_interface_top_layers` 3 → 4 ou 5. `support_interface_spacing` 0,5 → 0,1 só aparece no Rafael Longo. Três deles usam top Z = camada + 0,04 (0,12 na nossa camada de 0,08). Teste junto com o top Z 0,16 do Charizard. **Medido em 07/11:** com `tree_organic`, superfície curva (queixo) não recebe nenhuma camada de interface; só a face plana recebe. No Funko de 4 figuras Funko foram 61 camadas de interface em ~1170 de suporte. Com `tree_slim` ou `tree_hybrid`, o queixo inteiro recebe. Placa de teste com orgânico 3, orgânico 4 e slim 4: arquivo local (1h23, 8,1 g; da esquerda pra direita A, B, C). **Impresso em 08/11 (PLA branco, top Z 0,16):** as 3 saíram inteiras, mas em nenhuma o suporte sai com a mão; precisa de alicate. A slim (C) deixa a maior base na mesa. Falta comparar a lisura embaixo da cabeça e da aba. **6º vídeo, mesma direção e mais forte** (Ateliê Júpiter, mai/2026, 0,08 HQ no Bambu, sem A/B; enviado em 09/11): interface **8 camadas** com espaçamento **0** (maciça), Z superior e inferior **0,12**, ângulo 15 e `raft_first_layer_expansion` **5 mm** (brim do suporte, contra galho que solta). Dizem que o suporte "sai sozinho". Candidato a variante D da placa de teste; a expansão de 5 mm vale já em suporte que pousa na mesa com galho fino. **Medido em 09/11 (fatiado, ainda sem impressão):** numa figura em pé de 123 mm (príncipe + raposa, árvore híbrida), as pontas encostando na peça caíram de 2.668 para 1.224, o tempo de 11h38 para 11h05 e o peso de 86 para 84 g. Com estilo orgânico subiu para 3.271 pontas, e com "só na mesa" não melhorou. Na casca de 2 mm da lua (galho por dentro da cúpula) piorou: 5h48 → 7h43 e 321 → 6.359 pontas, porque a interface maciça cobre o teto interno. Use em figura, não em casca.

9. **Parede externa com aceleração baixa e interface concêntrica** (William Lins, ago/2026, Creality em 0,12, sem A/B, resultado só mostrado pronto): parede externa e topo a 30 mm/s com aceleração 500; na A1 o HQ 0,08 sai com parede a 60 e `outer_wall_acceleration` 2000. Em peça redonda, `support_interface_pattern` auto → concentric, e ironing só nas superfícies de cima, concêntrico, fluxo 10% e espaçamento 0,15 (ele mostrou, mas não usou). A parede precisa (item 4) é ignorada com a ordem externa → interna. Notas: `references/william-lins-qualidade-resina-2026-08.md`.

**Como fazer o A/B numa impressão só (testado no Charizard, 04/11):**
- Duplique o `<object>` no `3D/3dmodel.model` com id novo e UUIDs trocados, mais um `<item>` deslocado.
- No `model_settings.config`, duplique o `<object>`, o `<model_instance>` e o `<assemble_item>`. Dê nomes "A_..." e "B_..." e ponha a chave testada como `<metadata key="..." value="..."/>` dentro de cada objeto.
- Fatie com `--arrange`. Pela coordenada y do `<item>`, diga qual cópia fica atrás (y maior) e qual na frente.
- Confira no G-code que a diferença existe: por exemplo, a altura do último `; FEATURE: Support` de cada `unique label id`.
- Cuidado: alguns 3MF misturam CRLF; use regex com `\r?\n`.
- Antes, confira se a peça tem a característica que o teste mede. O Charizard deitado só tinha suporte até 1,7 mm.

Tudo com fonte e nota: `references/pesquisa-2026-11-verificada.md` (resumo) e `pesquisa-2026-11-achados.jsonl` (os 60 achados).

## Portão antes de entregar o arquivo (obrigatório; duas falhas em 08/11 passaram por falta disto)

Confira no G-code fatiado, não no perfil. Se algum item falhar, corrija antes de abrir no Bambu:
1. **Base de apoio:** meça a área de contato com a mesa de cada peça. Toda figura ou peça com altura/√área > 1,5 leva brim `outer_only` de 8 mm com gap 0. Brim só em parte das peças não basta: na placa 4 da luminária, uma figura sem brim soltou.
2. **Mesa:** Frostbite com PLA a **40 °C** (`cool_plate_temp` e `_initial_layer`). Os 30 °C da BIQU são o mínimo; donos relatam peça pequena soltando a ~33 °C.
3. **Movimento (guia da Bambu para o A1, peça alta ou estreita):** `travel_speed` ≤ 400, `travel_acceleration` e `default_acceleration` ≤ 3000. O 0,08 HQ vem com 700, 10000 e 4000, e a mesa que se mexe derruba a peça.
4. **Ponte com furo:** teto impresso sobre vão (soquete de cabeça pra baixo, tampa) com furo no meio vira macarrão. Feche o furo com uma película de 0,4 mm e fure depois.
6. **Conferir no G-code que o APP gera, não só no CLI** (08/11: a lua saiu com som, mesa 65 °C e viagem 700 mesmo com o 3MF certo). O Bambu Studio só mantém do `project_settings` as chaves listadas em `different_settings_to_system` ([0] processo, [1..n] filamentos, [-1] impressora); o resto volta ao preset do sistema. E o tipo de mesa vem da escolha do app, não do `curr_bed_type`. Liste as chaves alteradas, ponha 40 °C em todo `*_plate_temp`, e depois de "Fatiar mesa" no app leia `/private/var/folders/*/*/T/bamboo_model/<data>/<hora>#<pid>#*/Metadata/.<pid>.0.gcode`: `^M1006` = 0, `M190 S40`, `travel_speed` 400.
5. **Suporte de árvore isolado:** galho sozinho na mesa solta. Confira na pré-visualização se a peça depende de galhos finos pra ficar em pé; se depender, reoriente ou use brim no suporte.

Fontes: [guia de colapso no A1 (cópia do guia Bambu)](https://sparklab.unbc.ca/?p=672), [wiki BIQU CryoGrip Pro](https://neo.bttwiki.com/en/docs/accessories-docs/build-plate/cyrogrippro/), [fórum Bambu: suporte de árvore isolado solta](https://forum.bambulab.com/t/bamboo-lab-a1-support-issue-please-help-me/214841).

## Luminária (peça que a luz atravessa): como o MakerWorld imprime (09/11)

Lido pela API pública (`api.bambulab.com/v1/search-service/select/design2?keyword=...` e `/design-service/design/<id>`):
- Moon Lamp 731351 (43 mil impressões): 0,2 com **0,08 só nos 2 cm de cima e de baixo** (camada variável manual, onde a cúpula fica plana), 4–7 paredes, 15%, Arachne, **sem suporte**, PLA fosco ou mármore.
- Outras luas: 0,2 com 2 paredes e **100% de preenchimento**, ou 5 paredes e 100%. A casca maciça vira litofania: a cratera aparece pela espessura, e não há vazio interno fazendo sombra.
- Lua de parede de 50 cm: peças deitadas na mesa, camada variável, sem suporte, pintada com spray claro.
- Diferença da nossa lua do Pequeno Príncipe (casca de 1,2 mm, 0%, suporte por dentro): eles desenham a casca para fechar sem suporte e mais grossa. Suporte por dentro deixa sombra com a luz acesa.

## Checklist antes de imprimir (mande ao usuário)

1. Escolher o slot da cor no diálogo de impressão (perguntar se o slot 1 ainda trava).
2. Deixar Flow Dynamics Calibration marcado, principalmente em carretel novo.
3. Filamento seco: estalo, vapor ou fio com bolha no bico = úmido. Seque a 50 °C por 8 h. Ar-condicionado ligado não molha o filamento; o problema é quando desliga.
4. Impressão longa (>6 h) numa placa só: se falhar, perde tudo.

## Depois de imprimir

- O maior ganho de superfície é filamento fosco ou mármore. Branco brilhante é a pior combinação para esconder linhas.
- Fuzzy skin esconde linha, mas deixa aspecto áspero: só pra textura proposital (pelo, pedra), nunca rosto ou peça articulada.
- **Bico 0,2 (upgrade de hardware):** o 3D Printed Mom diz que é o maior ganho em detalhe fino (letra, rosto pequeno), mais do que qualquer ajuste. O Bambu já traz perfis da A1 para 0,2 (`0.08mm High Quality @BBL A1 0.2 nozzle`). Custa tempo (linha mais fina) e entope mais fácil. Não testado na A1 do usuário, que só tem o 0,4.
- Não vale: polir com lixa até 5000 (3 dias e ficou com cara de plástico arranhado), vapor de acetona (não alisa PLA), PETG-CF sem bico de aço endurecido (a fibra de carbono gasta o bico de aço inox).
- Pintura de figura (primer → pré-sombra → pele no aerógrafo → olho → verniz fosco e depois brilhante só no olho e na boca): `references/pintura-e-dicas.md`.
- **Figura em várias peças:**
  - Corte no vinco natural (pescoço, cinto, sob um detalhe saliente), nunca no rosto ou num domo liso.
  - Use conector Dowel do corte do Bambu, com folga de 0,15–0,30 por lado. Teste antes num pino só.
  - Lixe as faces e cole com CA em gel (o ativador em spray cura na hora, bom pra capa e peça suspensa), limpando o excesso antes de curar. Epóxi líquido falha em PLA liso. A AngelMaker usa Durepox (massa epóxi) pra unir e preencher a emenda de perna e base, e lixa depois; não testado aqui.
- **Detalhe que faltou no arquivo** (dente, vinco): marque antes no modelo (Meshmixer); se só viu depois, risque com Dremel. Furo e emenda: massa de EVA (William Lins).
- **Fiapo (stringing):** passe rápido a chama de um isqueiro e raspe o resto com a unha.
- **Tinta metálica:** primer preto embaixo (o metal ganha contraste) e verniz fosco nunca por cima, porque apaga o brilho (AngelMaker).
- **Alternativa ao primer:** resina UV passada com pincel em camada fina e curada na luz UV esconde linha melhor que o spray, mas é tóxica (luva, máscara, ventilação) e não se limpa com papel (gruda e estraga). Use spray em rosto e áreas grandes, e resina no corpo (KostaWorks).
- **Pra pintar:** primer de enchimento automotivo (o spray de miniatura não preenche a linha de camada), depois lixa 320–400 até 600. Silk é a pior base pra pintura.
- **Verniz turvo:** vem de umidade, demão grossa ou frio. Conserta com uma demão fina de verniz brilhante e depois refosca.
- Os 23 vídeos do grupo de impressão 3D (01–07/11, nota por vídeo e o que repete a skill): `references/videos-grupo-2026-11-07.md`.
- Pesquisa verificada sobre acabamento (o que vale e o que não vale): `references/acabamento-pesquisa.md` (gecko, 02/11) e `references/pesquisa-2026-11-verificada.md` (04/11).

## Formato da resposta

Primeira linha com o resultado (arquivo, tempo, peso), no máximo 5 itens e uma pergunta no fim. Números sempre do fatiador, nunca estimados de cabeça.
