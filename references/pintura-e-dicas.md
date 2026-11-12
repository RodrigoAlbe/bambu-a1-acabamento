# Vídeos de pintura e fatiador compartilhados num grupo de impressão 3D

Lido em 03/11/2026.

## 1. Pintura de figura: "Como Pintar Pele e Olhos" (Made in Heaven Studio, 23 min)
https://www.youtube.com/watch?v=1z_J3M2IU-U. Sem legenda; transcrito com whisper.

Ordem do processo:
1. Acabamento (lixa) → primer → **pré-sombreamento** com aerógrafo (preto nas sombras, branco nas luzes).
2. **Pele primeiro:** aerógrafo com bico 0,2 (Steyla B61), tinta Vallejo, camadas finas. Começa com o tom escuro e passa pro claro. Bochecha: pele + um pouco de magenta.
3. **Retoque no pincel com wet blending:** tinta bem diluída, espalhar e limpar o excesso enquanto ainda está molhada. Muitas camadas finas, esperando secar entre elas: cor clara e escura muda de tom ao secar.
4. **Olho:**
   - contorno e preto;
   - branco diluído no meio, que define pra onde a figura olha;
   - íris do tom escuro pro claro, em linhas finas.
   - Pra checar a simetria, tire foto e dê zoom no celular. Refazer é normal.
5. **Isolar antes do brilho:** passa verniz fosco no que já está pintado. Depois, verniz brilhante (laca) só no olho e na boca, e não envernize mais nada por cima.

Outras dicas do vídeo:
- **Máscara (masking):** fita japonesa amarela (do AliExpress) e "borracha" líquida brasileira da Shopee, que sai sem arrancar tinta.
- **Dry brush** pra relevo; o aerógrafo fica pra superfície lisa.
- **Paleta reduzida:** repita as mesmas misturas em várias partes da peça. Use off-white (branco com um toque de amarelo) em vez de branco puro.
- **Pincel:** fino que forma ponta firme (Keramik Precision) e pouca tinta nele.

## 2. Camada adaptativa no Bambu Studio (reel da Utilizze 3D)
https://www.instagram.com/reel/Dd94XPFh42v/. São 61 s; transcrevi o áudio e olhei os quadros.
- O caminho no Bambu Studio: botão direito na peça → altura de camada variável.
  - **Adaptativo:** um slider entre Qualidade e Velocidade (no vídeo, em 0,20).
  - **Ajuste manual na peça:** o botão esquerdo diminui a camada (mais detalhe), o direito aumenta (mais velocidade).
  - **Suave (raio 5):** deixa a transição gradual, o que reduz a marca mas aumenta um pouco o tempo.
- Na capivara de 60 mm, o resultado foi 2h25 com camada baixa na peça toda e 1h26 com a adaptativa.
- Use camada adaptativa e ajuste à mão só a região curva, suavizando a transição, em vez de baixar a camada da peça toda.
- Teste antes em peça de acabamento visível, principalmente com filamento silk.
- É o mesmo problema do topo da cabeça da gecko. Lá, a camada uniforme de 0,08 resolveu.

### Teste no Jolteon branco (03/11/2026): a adaptativa não compensou
Fatiado com `jolteon/adaptive.py` (porta do algoritmo do Bambu/Prusa, suave raio 5):
- 0,08 uniforme + suporte orgânico: **7h44** (o arquivo atual)
- 0,08 uniforme + tree slim: 8h02
- adaptativa qualidade 0,5: 8h33 (1564 camadas)
- adaptativa qualidade 0,7: 8h20 (1732 camadas)

Por quê: o Bambu não aceita camada variável com suporte orgânico, e com 10 peças na mesma mesa cada uma ganha alturas diferentes, o que quase dobra as trocas de camada. Numa peça curva, a adaptativa também fica quase toda em 0,08. Ela só vale pra peça única com paredes retas.

## 3. Modelos: DecorMaster no Cults3D ("kit natal")
https://cults3d.com/pt/usuarios/DecorMaster/modelos-3d
- 199 designs na coleção "Brinquedo sem AMS": fan-art de anime, Tartarugas Ninja, Mortal Kombat, Mario e Halloween, a R$ 21,63 cada.
- São figuras em várias peças, em 3MF, de uma cor por peça, pra montar e pintar. Servem pra A1 sem trocar cor.
- Não achei a coleção de Natal pela busca. Falta o link exato do "kit natal".

## 4. Printables (printables.com)
Só o link da home, sem modelo específico.

## 5. Ofertas de PETG (02–03/11, já vencidas ou só "pra quem resgatou ontem")
- Masterprint preto, branco e cinza: R$ 48–56 o rolo, cupom de 20% no Mercado Livre.
- PrintPulse: R$ 58,90 com cashback, na Shopee.
- PETG é bom pra peça funcional ou ao ar livre. Pra figura que vai ser pintada, o PLA fosco continua melhor: pega mais detalhe e é mais fácil de lixar.
