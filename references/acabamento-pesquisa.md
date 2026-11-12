# Acabamento "de loja" na Flexi Gecko: o que vale e o que não vale

Pesquisa de 02/11/2026. Três pesquisadores (fóruns e wiki da Bambu, legendas de vídeos do YouTube, pós-processamento) e um verificador, que leu as fontes primárias e deu nota com o Jev. Dos 17 achados, 6 foram confirmados na fonte e valem para esta peça.

Peça: A1 + AMS lite, bico 0,4, 16 segmentos articulados, 2,8 g, 35 min, PLA genérico verde brilhante.

## O que já está no arquivo (`gecko_acabamento_verde.3mf`)

O verificador conferiu estes valores no 3MF.

- Camada variável de 0,08 a 0,15 mm.
- Costura em Back. Random cria pontinhos (zits), segundo a wiki.
- Classic: uma costura por camada, melhor superfície (wiki).
- Parede externa a 60 mm/s.
- Tempo mínimo de camada de 8 s. O exemplo da wiki é 4 s.
- PLA a 220 °C.
- Sem ironing.
- As 16 ilhas por camada já dão tempo de resfriar. Não precisa pôr cópias extras na mesa.

## Próximos passos, do maior para o menor ganho/custo

1. **Filamento fosco ou mármore.** É o maior ganho, e três vídeos com legenda lida concordam (Teaching Tech, Slant 3D, NuggetsInclusive). Cor clara não ajuda: para a Slant 3D, "branco é a pior cor". Ressalva: o fosco é menos resistente, então teste se as juntas aguentam.
2. **Flow Dynamics automático a cada carretel novo.** A wiki diz que o automático varia uns 10%, e que mudar a temperatura ou o max volumetric speed pede nova calibração. Blob vem da pressão residual. A calibração manual de flow rate só entra depois disso, se ainda houver blob.
3. **Costura pintada à mão numa face escondida**, como a barriga ou a parte de dentro da cauda. O recurso está documentado na wiki. O scarf seam falha em overhang.
4. **Conferir a pré-visualização.** Se sumir dedo ou garra, teste Arachne ou detect thin wall. Isso não foi fatiado aqui.
5. **Secar se aparecer fio ou blob:** 50 °C por 8 h em secador. Pela wiki, a A1 é aberta e não seca filamento. Um relato do fórum diz que secar resolveu blobs na costura.

## Não fazer nesta peça

- Lixa, primer de preenchimento, massa ou epóxi (XTC-3D). Todos engrossam a superfície e tendem a colar as juntas. A Smooth-On cita 0,4 mm como espessura de referência de uma demão.
- Fuzzy skin na peça inteira. Ele desloca a parede externa, e as faces das juntas também são parede externa.
- Solvente. Acetona não age no PLA. THF e DCM agem, mas são tóxicos, não use em casa. O verificador não conferiu essas fontes.
- Soprador demorado. Para fios, uma passada rápida e uma escova dura bastam.

## Não verificado

- A folga das juntas: minha medição no modelo saiu inconsistente.
- Mesa lisa contra texturizada para a barriga: só fontes de loja.
- Bico 0,2: confirma camada de 0,06 mm. O "ganho modesto, 2–4× o tempo" é de fórum.
- Faixa visível nas transições da camada variável: relato isolado.
- Nada disso foi impresso. O risco às juntas é dedução.

## Critério de pronto (numa impressão real)

1. As 16 juntas giram livres.
2. Não há pontinho nem blob na face visível.
3. Nenhum dedo ou garra some.

Notas e fontes: `scratchpad/jev_out.jsonl`, `scratchpad/src/`, `scratchpad/yt/`. São temporárias e somem no reboot.

## Vídeo "10 Ways to Hide Layer Lines" (NuggetsInclusive, jan/2026) — lido em 04/11/2026

Fonte: https://www.youtube.com/watch?v=WxpkxQZmCZ8.
Um modelo só, julgado a olho, impressora não informada. Serve como sinal, não como medida.

- Velocidade a 50%: não muda a linha de camada. Confirma manter o perfil.
- Orientação: face apoiada na mesa pega a textura da mesa. Útil em peça com face plana.
- Fuzzy skin: disfarça, mas o autor não gosta do visual em peça estética.
- Padrão na superfície (cubinhos, hexágonos) disfarça; listras horizontais realçam a linha. Só serve pra quem modela.
- Filamento com carga: mármore e PolyTerra disfarçam; o favorito dele é PETG-CF (exige bico endurecido).
- Lixar até 5000 por 3 dias: ruim. Laser: fora do nosso equipamento. Vapor de acetona: liso e brilhante, mas é para ABS/ASA, não PLA.
- Top 3 dele: 1) lixa + primer + pintura (repetir), 2) material que disfarça + outros materiais, 3) vapor.

## Vídeo "How To Get Smoother 3D Prints" (3D Max Builds, set/2026) — lido em 04/11/2026

Fonte: https://www.youtube.com/watch?v=dXIdHLX_2Rc. A/B impressos em carro, domo e dado, impressora Cobra X. Mesa lisa patrocinada (Mini-P P100).

- Fosco esconde linha (mesma linha, menos reflexo). Orientação: diminuir as áreas grandes quase horizontais (carro em pé).
- Top Z distance com camada 0,08: 0,08 difícil de tirar e danifica, 0,24 cede, **0,16 melhor**. Interface em PETG com Z=0 sai fácil, mas exige muita purga e esfria a camada durante a troca.
- Domo: 0,08 uniforme +41 min; adaptativa (qualidade no máximo) +13 min com o mesmo visual. Bate com a regra da skill: peça única, laterais quase verticais.
- Base lisa: mesa lisa, 1ª camada a 20–30 mm/s, Z offset e flow com cuidado, infill/wall overlap maior, elephant foot.
- Parede externa primeiro: um pouco melhor no dado, mas cede em overhang. Parede externa 200 → 30 mm/s: melhora visível.
- Ironing "All top surfaces" alisa topo plano (dado). Scarf seam reduz a costura.

## Vídeo "My Secret to Making FDM Prints Look Like Resin" (KostaWorks FDM, out/2025) — lido em 04/11/2026

Fonte: https://www.youtube.com/watch?v=qunWIJvMcHY. Mesma combinação do autor: A1 + mesa Frostbite, PLA meta (JAYO/Sunlu).

- Bico 0,4 + camada 0,08 no corpo; bico 0,2 + 0,08 no rosto e no detalhe fino (a A1 troca bico em 10 s). Base em 0,12.
- Ventoinha 100% sempre. Gerador Classic; Arachne só em roupa texturizada.
- Rosto e detalhe na vertical: a linha segue a forma.
- Parede externa mais lenta que a interna (tela: externa 75, interna 150).
- Suporte tree; infill lightning (aviso na tela: mais chance de falha).
- Painel Precision (quadro em 78 s do trecho 200–300 s): slice gap closing radius 0,002, resolution 0,002, arc fitting desligado, elephant foot 0. Fatiado no Bulbasaur (só resolution + closing radius): mesmo tempo, G-code com 66% mais movimentos.
- Pós: lixa 400 → 800/1000 só onde precisa; isqueiro no fiapo; Motip spray putty (primer de enchimento) em 80% das peças; resina UV com pincel no corpo (tóxica, não limpar com papel).
