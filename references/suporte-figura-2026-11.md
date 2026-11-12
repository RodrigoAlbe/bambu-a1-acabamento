# Suporte em figura: pesquisa de 05/11/2026

Pesquisa com fonte, conferida no G-code e no app instalado (Bambu Studio 02.08.02.61).

## Fato (código/perfil)
- O raio do tronco cresce tan(ângulo) × camada por camada; `tree_support_branch_diameter_angle` padrão 5°, faixa 0–15 (TreeSupportCommon.hpp:269, PrintConfig.cpp:5848 @ v02.08.02.61). 5° ≈ +8,7 mm de diâmetro em 50 mm.
- Ponta fixa em 0,8 mm na 2.08; `tree_support_tip_diameter` só na v02.09.01.70 (mín. = largura de linha).
- Orgânico força ≥1 parede; `tree_support_wall_count` -1 = auto.
- Perfil A1 0,08 HQ (conferido no G-code): `support_bottom_z_distance` 0,08, `tree_support_branch_distance` 5, `tree_support_branch_angle` 45, `support_interface_spacing` 0,5, `independent_support_layer_height` 1.
- Branch distance maior e densidade menor = menos contato, remoção mais fácil, overhang pior (help.prusa3d.com/article/organic-supports_480131; OrcaSlicer wiki support_settings_tree).

## Evidência (vídeo/fórum)
- Painted4Combat, 27/10/2024, youtu.be/ZghfP8_L8Pc: minis 0,2/0,08; inclinar 30–45° para olho/sobrancelha não precisar de suporte; suporte manual pintado em escultura; bloqueador em mão e ombro; remover frio, girando/alavancando a interface. Peças mostradas, sem A/B.
- Kennedy DIY, 14/07/2025, youtu.be/yqZUSNsubB8: A/B impresso em peça Lego, camada 0,20: só na mesa, top Z 0,24 (1,2× camada), 3 camadas de interface, espaçamento 0,1, XY 0,38.
- Shayway, 26/08/2023, youtu.be/RxQkp_6fA0s: figura com dentes, 0,12: top Z 0,16, 3 interfaces, espaçamento 0, threshold 15°. Opinião.
- PETG como interface de PLA: fórum positivo na X1C, um usuário de A1 falhou (forum.bambulab.com/t/73640). Sem A/B em rosto.

## Medido no fatiador (Funko de 4 figuras, 10 cm, 05/11)
| variante | tempo | peso | troncos na mesa |
|---|---|---|---|
| sem suporte | 8h20 | 62 g | 0 |
| 5° (padrão) + rosto bloqueado | 12h37 | 85 g | 9 × 5,4 mm |
| 2° + bottom 0,16 | 12h35 | 77 g | 13 × 2,8 mm |
| 0° + bottom 0,16 | 12h18 | 71 g | 2 × 3,6 mm (resto pousa na peça) |
| 2° + bottom 0,16 + rosto inteiro bloqueado (escolhida) | 12h04 | 75 g | 17 × 2,3 mm |

## Desconhecido
- A/B impresso de branch_diameter_angle ou branch_distance em figura: nenhum achado.
- Calor/água quente na remoção; `support_interface_pattern` para figura.
