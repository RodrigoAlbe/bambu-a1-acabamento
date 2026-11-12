# Vídeos compartilhados num grupo de impressão 3D (01 a 07/11/2026)

Lido em 07/11/2026. O grupo tem 56 mensagens, 36 delas com link: 22 reels do Instagram, 2 vídeos do YouTube e o resto é oferta, modelo ou site.

Nenhum reel mostra A/B impresso em 0,08 numa A1. Tudo que é ajuste de fatiador entra como candidato, não como regra.

## Suporte: 4 reels dão a mesma receita

| Reel | Camada do vídeo | O que muda |
|---|---|---|
| Rafael Longo (De1zid1xeey), receita do prof. Kennedy | 0,20 | tree auto, só na mesa, densidade da 1ª camada 70%, top Z = camada + 0,04, interface top 3, **espaçamento da interface 0,5 → 0,1**, distância XY 0,35 → 0,38 |
| IMPRESSIONADO 3D (DfQlATbRSAu) | 0,20 | tree **hybrid**, top Z = camada + 0,04 (0,24), interface top 2 → 3, espaçamento 2 → 1 |
| Pedro Bernardes (DbTcy5MxvpQ) | 0,20 | top Z 0,25, interface top **4** ("vira uma cama") |
| 3d Printing by Simo (DeRkx0GNYVO), A1 na tela | 0,20 | tree **slim**, interface top 3. Peça plana grande sai lisa por baixo |

A AngelMaker (abaixo) usa o mesmo em 0,12: top Z 0,16, interface top 4–5.

O que já estava na skill: interface top 3 (no `a1_convert.py`) e top Z 0,16 em 0,08 (A/B do Charizard). A regra "camada + 0,04" daria 0,12 em 0,08, então fica entre o 0,08 (arranca pedaço) e o 0,16 (melhor no A/B).
Novo: **interface mais densa** (`support_interface_spacing` 0,1) e XY 0,38. Ninguém mostra isso em figura pequena.

## Superfície lisa (TubaLabs Dfak4__EXf3, ashley_lifestory Ddq8YQCm9dV, printpal DdS745BMP0A e DePyIuyvDeC)

- TubaLabs: ironing 15% no topo plano, parede externa 60 mm/s, costura alinhada na quina ou scarf em peça redonda, camada variável 0,20 → 0,08 nas curvas, filamento fosco. Tudo já está na skill. A camada variável já foi medida e reprovada pra figura curva.
- ashley_lifestory: PLA fosco no lugar de brilhante, e fuzzy skin bem fino em art toy. A skill já diz fosco; fuzzy continua só pra textura proposital.
- printpal: imprimir um teste de calibração e copiar o melhor valor pra `ironing_speed`/`ironing_flow` (ironing) e pra fluxo da superfície de topo (`top_solid_infill_flow_ratio`). Só vale pra topo plano. O arquivo do teste é da Print Pal.

## Costura (Aquele 3d, DesZEUOhbyq)

Alinhada pra peça com quina; atrás pra miniatura com a frente virada pra você; aleatória deixa pontilhado; scarf em vaso e cilindro. Igual à skill.

## Montagem e pós-processamento

- **Ímã escondido** (Clube Das Ferramentas, DcULd1asXQr): parte negativa em cilindro com a medida do ímã (8×8×3 no vídeo), alinhada no topo e descida 0,5 mm pra ficar fechada. Fatia, acha a camada em que o furo ainda está aberto e põe "adicionar pausa" ali. Na pausa, coloca os ímãs (polos invertidos entre as duas peças) e continua.
- **Multipart sem trocar cor** (Zapach Store, DdKkYznRa3o): juntar as placas de cores diferentes numa só aumentou o tempo (2h45 + 28 min viraram 4h40). Com "sequência de impressão: por objeto" a mesma placa caiu pra ~2h, porque cada peça é feita inteira antes da próxima. Limite: o cabeçote não pode bater na peça já impressa (a folga aparece em volta da peça na aba Preparar).
- **Ordem do acabamento** (FOF3D, DfLQhMZTKiS): fiapo com maçarico e estilete → lixa → massa (gesso ou massa de modelar) pra buraco e emenda → primer → tinta. Peça muito áspera: base seladora antes da massa. Primer depois da massa, nunca antes.
- **Escalar peça com encaixe** (Paulo Henrique, DcR9xHtuRsg): ao aumentar a peça, a folga cresce junto (0,2 vira 0,5 a +150%). Corrige com compensação de contorno XY (`xy_contour_compensation`) negativa = diferença medida − 0,1 a 0,2; ou o atalho dele: +1% de escala na peça que encaixa a cada 100% extra. Vale também ao reduzir (teste do Charizard a 65%).
- **Preenchimento lightning** (Clube Das Ferramentas, De2ohNXOuBC): abóbora decorativa de 6h → 3h04 trocando gyroid 15% por lightning, com 3 paredes. Só peça decorativa; teste de resistência antes de produzir em série.

## AngelMaker no YouTube: "action figure de filamento que parece resina" (YXrn5_nWQRE, 22 min)

Ela faz action figure em várias peças, e o método inteiro bate com o que a skill já diz. O que acrescenta:
- **Camada por peça:** 0,12 no personagem e 0,20 na base e nas pedras, que ninguém olha de perto.
- **Velocidade:** topo a 80 mm/s e parede externa mais lenta; o preenchimento pode ir rápido. A A1 em 0,08 já sai com a parede a 60.
- **Orientação antes de tudo:** gire cada peça pensando de onde o personagem vai ser visto, pra o suporte cair na face escondida. A perna do Mandaloriano foi de cabeça pra baixo, com o suporte dentro da cintura, e a perna saiu sem marca. Capacete e rosto vão "olhando pra baixo", nunca virados pra cima: as últimas camadas do topo é que deixam anel.
- **Suporte em 0,12:** top Z 0,16 (de novo, camada + 0,04), bottom Z 0,20, tree hybrid automático, interface top 4–5 e bottom 2.
- **Filamento:** ela prefere silk, porque sai mais liso e às vezes nem pinta. Branco dá resultado ruim pra ela em peça com muito suporte (relato pessoal, sem teste). Isso contraria a skill, que manda fosco pra esconder linha e diz que silk é a pior base pra pintar; fica a regra da skill, já que pintamos.
- **Acabamento:** lixa d'água de 150–200 até 600, molhada. Primer cinza automotivo (ColorArte), ou primer preto líquido quando vai ter tinta metálica (o metal ganha contraste e sombra). O primer mostra os defeitos: volta com massa e lixa e passa outro.
- **Emenda de peça:** Durepox pra unir perna e base; massa pra pequenas correções, que é mais fácil de lixar.
- **Pintura:** preto no corpo todo, pré-sombra com dry brush branco de cima pra baixo e depois as cores.
- **Cola:** cola instantânea em gel com ativador em spray, que endurece na hora (bom pra capa e peça suspensa).
- **Verniz fosco não vai em cima de tinta metálica,** porque apaga o brilho. Passe com pincel só no acrílico fosco; spray (Acrilex Acryl Fix fosco) na base.

