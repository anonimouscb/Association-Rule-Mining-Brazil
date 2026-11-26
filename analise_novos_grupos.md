# Análise dos novos grupos — dados não presentes na pesquisa do DataSenado 2023

Estes cinco cruzamentos não constam nos resultados publicados no PDF da pesquisa nacional. Os dados são extraídos dos microdados de 2023 via análise de regras de associação (FP-Growth, suporte mínimo 1%, confiança mínima 1%).

---

## G_new4 — Conhecimento da Lei Maria da Penha por região (VD_REGIAO × P22)

**Pergunta:** Quanto você conhece sobre a Lei Maria da Penha?
- P22_1 = Muito | P22_2 = Pouco | P22_3 = Nada

**Regiões:** 1=Norte | 2=Nordeste | 3=Sudeste | 4=Sul | 5=Centro-Oeste

### Itemsets frequentes

```
P22_2 (Pouco)          | 14625   — 67,1% da amostra
P22_1 (Muito)          |  5636   — 25,9%
P22_3 (Nada)           |  1378   —  6,3%

VD_REGIAO_2 (Nordeste) |  7255
VD_REGIAO_1 (Norte)    |  5642
VD_REGIAO_3 (Sudeste)  |  3225
VD_REGIAO_5 (C-Oeste)  |  3235
VD_REGIAO_4 (Sul)      |  2430

Nordeste + Pouco        | 4967
Norte    + Pouco        | 3867
Nordeste + Muito        | 1806
Norte    + Muito        | 1352
Sul      + Muito        |  726
C-Oeste  + Muito        |  910
```

### Regras de associação

| Regra (A → B) | Confiança | Lift | Interpretação |
|---|---|---|---|
| **Sul → Muito** | 0.299 (30%) | **1.155 (>1)** | Mulheres do Sul conhecem "muito" a LMP acima do esperado — associação positiva. |
| **C-Oeste → Muito** | 0.281 (28%) | **1.087 (>1)** | Centro-Oeste também apresenta associação positiva com conhecimento elevado. |
| **Norte → Nada** | 0.069 (7%) | **1.093 (>1)** | Norte tem proporção de desconhecimento total acima do esperado. |
| **Sul → Pouco** | 0.639 (64%) | 0.952 (<1) | Sul tem menos "pouco" do que a média — consistente com o maior "muito". |
| **Nordeste → Muito** | 0.249 (25%) | 0.962 (<1) | Nordeste apresenta associação negativa com conhecimento elevado. |
| **Norte → Muito** | 0.240 (24%) | 0.926 (<1) | Norte também abaixo do esperado para "muito". |
| **Muito → Sul** | 0.129 (13%) | **1.155 (>1)** | Entre quem conhece muito, há concentração acima do esperado no Sul. |
| **Muito → C-Oeste** | 0.161 (16%) | **1.087 (>1)** | Centro-Oeste também sobrerrepresentado entre quem conhece muito. |

**Síntese:** O conhecimento aprofundado da Lei Maria da Penha é mais frequente no Sul e no Centro-Oeste, enquanto Norte e Nordeste concentram os menores índices de conhecimento. O desconhecimento total (P22_3) é proporcionalmente mais associado ao Norte.

---

## G_new5 — Percepção de aumento da violência doméstica por faixa etária (VD_IDADE × P13)

**Pergunta:** Nos últimos doze meses, a violência doméstica e familiar contra as mulheres:
- P13_1 = Aumentou | P13_2 = Permaneceu igual | P13_3 = Diminuiu

**Faixas etárias:** 1=16–24 | 2=25–29 | 3=30–34 | 4=35–39 | 5=40–44 | 6=45–49 | 7=50–54 | 8=55–59 | 9=60–64 | 10=65+

### Itemsets frequentes

```
P13_1 (Aumentou)       | 16345  — 75,0% da amostra
P13_2 (Igual)          |  3822  — 17,5%
P13_3 (Diminuiu)       |  1051  —  4,8%

Faixa 1 (16–24) + Aumentou  | 1819  (64,0% da faixa)
Faixa 1 (16–24) + Igual     |  735  (25,9% da faixa)
Faixa 5 (40–44) + Aumentou  | 2163  (77,8% da faixa)
Faixa 9 (60–64) + Aumentou  |  961  (80,6% da faixa)
Faixa 8 (55–59) + Aumentou  | 1257  (79,1% da faixa)
```

### Regras de associação

| Regra (A → B) | Confiança | Lift | Interpretação |
|---|---|---|---|
| **60–64 → Aumentou** | 0.806 (81%) | **1.075 (>1)** | Faixa 60–64 é a que mais associa violência ao aumento — acima do esperado. |
| **55–59 → Aumentou** | 0.791 (79%) | **1.054 (>1)** | Faixa 55–59 também acima da média. |
| **45–49 → Aumentou** | 0.795 (80%) | **1.060 (>1)** | Faixa 45–49 igualmente acima do esperado. |
| **40–44 → Aumentou** | 0.778 (78%) | **1.037 (>1)** | Faixa 40–44 levemente acima da média. |
| **16–24 → Aumentou** | 0.640 (64%) | 0.854 (<1) | Jovens de 16–24 percebem menos o aumento — associação negativa. |
| **25–29 → Aumentou** | 0.710 (71%) | 0.946 (<1) | Faixa 25–29 também abaixo da média. |
| **16–24 → Igual** | 0.259 (26%) | **1.475 (>1)** | Jovens de 16–24 associam-se fortemente à percepção de que a violência "permaneceu igual" — o lift mais alto do grupo. |
| **25–29 → Igual** | 0.217 (22%) | **1.238 (>1)** | Faixa 25–29 também acima do esperado para "permaneceu igual". |

**Síntese:** Mulheres mais velhas (40 anos ou mais) percebem o aumento da violência doméstica com maior intensidade do que a média. Jovens de 16 a 29 anos são as que mais relativizam — associando-se à percepção de que a violência "permaneceu igual" — o que pode refletir menor exposição histórica ao tema ou diferença de referencial temporal.

---

## G_new6 — Busca por assistência de saúde após violência por renda (V14 × P46)

**Pergunta P46:** Por causa da violência mais grave, você buscou algum tipo de assistência de saúde?
- P46_1 = Sim | P46_2 = Não

**Renda familiar (V14):** 1 = até 2 SM | 2 = de 2 a 6 SM | 3 = acima de 6 SM

> Atenção: esta pergunta é filtrada — só responde quem declarou ter sofrido violência (P38=Sim). O universo é menor que o total da pesquisa.

### Itemsets frequentes

```
V14_1 (até 2 SM)       | 12589
V14_2 (2 a 6 SM)       |  5132
V14_3 (acima de 6 SM)  |  2268

P46_2 (Não buscou)     |  5037
P46_1 (Buscou)         |  2362

Não buscou + até 2 SM  | 3250  (64,5% das que não buscaram)
Não buscou + 2 a 6 SM  | 1060
Buscou     + até 2 SM  | 1548  (65,5% das que buscaram)
Buscou     + 2 a 6 SM  |  497
Não buscou + acima 6SM |  406
```

### Regras de associação

| Regra (A → B) | Confiança | Lift | Interpretação |
|---|---|---|---|
| **Buscou → até 2 SM** | 0.655 (66%) | **1.134 (>1)** | Mulheres que buscaram assistência de saúde são desproporcionalmente de baixa renda. |
| **até 2 SM → Buscou** | 0.123 (12%) | **1.134 (>1)** | Mulheres de baixa renda buscam assistência acima do esperado. |
| **até 2 SM → Não buscou** | 0.258 (26%) | **1.117 (>1)** | Mas também são maioria entre as que não buscaram — reflexo do peso demográfico da faixa. |
| **acima 6 SM → Não buscou** | 0.179 (18%) | 0.774 (<1) | Mulheres de alta renda buscam menos assistência de saúde após violência — associação negativa com "não buscou" abaixo do esperado, mas o lift <1 indica que buscam proporcionalmente menos que a média. |
| **2 a 6 SM → Buscou** | 0.097 (10%) | 0.893 (<1) | Renda média associa-se negativamente à busca por assistência. |

**Síntese:** A busca por assistência de saúde após violência é mais frequente entre mulheres de baixa renda (até 2 SM), o que pode indicar maior dependência do sistema público de saúde. Mulheres de renda mais alta buscam menos — possivelmente por subnotificação, acesso a redes privadas não captadas pela pesquisa, ou menor disposição a formalizar o episódio.

---

## G_new7 — Solicitação de medida protetiva por faixa etária (VD_IDADE × P62)

**Pergunta P62:** Alguma vez, você solicitou medida protetiva para sua segurança?
- P62_1 = Sim | P62_2 = Não

> Filtrada para quem sofreu violência (P38=Sim).

### Itemsets frequentes

```
P62_2 (Não solicitou)  | 5156
P62_1 (Solicitou)      | 2244

Faixa 5 (40–44) + Não  |  705   Faixa 5 + Sim  | 367
Faixa 4 (35–39) + Não  |  696   Faixa 4 + Sim  | 349
Faixa 6 (45–49) + Não  |  602   Faixa 6 + Sim  | 292
Faixa 3 (30–34) + Não  |  592   Faixa 3 + Sim  | 301
Faixa 1 (16–24) + Não  |  539   Faixa 1 + Sim  | (abaixo do limiar)
Faixa 10 (65+)  + Não  |  310
```

### Regras de associação

| Regra (A → B) | Confiança | Lift | Interpretação |
|---|---|---|---|
| **Solicitou → 40–44** | 0.164 (16%) | **1.281 (>1)** | Faixa 40–44 é a mais associada à solicitação de medida protetiva. |
| **Solicitou → 35–39** | 0.156 (16%) | **1.280 (>1)** | Faixa 35–39 praticamente empatada — ambas com lift ~1.28. |
| **Solicitou → 45–49** | 0.130 (13%) | **1.258 (>1)** | Faixa 45–49 também acima do esperado. |
| **Solicitou → 30–34** | 0.134 (13%) | **1.143 (>1)** | Faixa 30–34 levemente acima da média. |
| **40–44 → Solicitou** | 0.132 (13%) | **1.281 (>1)** | Confirmação bidirecional: mulheres de 40–44 solicitam mais. |
| **35–39 → Solicitou** | 0.132 (13%) | **1.280 (>1)** | Idem para 35–39. |
| **45–49 → Solicitou** | 0.130 (13%) | **1.258 (>1)** | Idem para 45–49. |
| **16–24 → Não solicitou** | 0.190 (19%) | 0.802 (<1) | Jovens de 16–24 solicitam medida protetiva abaixo do esperado — lift <1. |
| **65+ → Não solicitou** | 0.189 (19%) | 0.799 (<1) | Mulheres de 65+ também subrepresentadas entre as que solicitaram. |
| **60–64 → Não solicitou** | — | — | Faixa 60–64 apresenta associação positiva com não solicitação (lift 1.106). |

**Síntese:** A solicitação de medida protetiva concentra-se nas faixas de 30 a 49 anos, com pico em 35–44. Jovens (16–24) e idosas (60+) solicitam proporcionalmente menos — o que pode refletir, respectivamente, menor conhecimento dos mecanismos legais disponíveis e maior isolamento ou dependência familiar.

---

## G_new8 — Vitimização por região (VD_REGIAO × P38)

**Pergunta P38:** Você já sofreu algum tipo de violência doméstica ou familiar?
- P38_1 = Sim | P38_2 = Não

**Regiões:** 1=Norte | 2=Nordeste | 3=Sudeste | 4=Sul | 5=Centro-Oeste

### Itemsets frequentes

```
P38_2 (Não sofreu)     | 14326  — 65,9% da amostra
P38_1 (Sofreu)         |  7413  — 34,1%

Norte    + Sofreu      | 2117  (37,5% da região)
Norte    + Não sofreu  | 3515  (62,3%)
Nordeste + Sofreu      | 2301  (31,7%)
Nordeste + Não sofreu  | 4938  (68,1%)
Sudeste  + Sofreu      | 1110  (34,4%)
Sul      + Sofreu      |  796  (32,8%)
C-Oeste  + Sofreu      | 1089  (33,7%)
```

### Regras de associação

| Regra (A → B) | Confiança | Lift | Interpretação |
|---|---|---|---|
| **Norte → Sofreu** | 0.375 (38%) | **1.103 (>1)** | Norte tem a maior taxa de vitimização declarada — acima do esperado. |
| **Sofreu → Norte** | 0.286 (29%) | **1.103 (>1)** | Entre as que sofreram violência, Norte está sobrerrepresentado. |
| **Nordeste → Sofreu** | 0.317 (32%) | 0.932 (<1) | Nordeste apresenta vitimização abaixo da média nacional. |
| **Sofreu → Nordeste** | 0.310 (31%) | 0.932 (<1) | Confirmação: Nordeste subrepresentado entre vítimas. |
| **Sul → Sofreu** | 0.328 (33%) | 0.963 (<1) | Sul levemente abaixo da média. |
| **Sudeste → Sofreu** | 0.344 (34%) | **1.012 (>1)** | Sudeste praticamente na média nacional. |
| **C-Oeste → Sofreu** | 0.337 (34%) | 0.989 (<1) | Centro-Oeste ligeiramente abaixo da média. |
| **Nordeste → Não sofreu** | 0.681 (68%) | **1.035 (>1)** | Nordeste concentra proporcionalmente mais respostas negativas. |

**Síntese:** A região Norte apresenta a maior taxa de vitimização declarada (37,5%), com associação positiva acima do esperado. O Nordeste, apesar de ser a região com maior número absoluto de respondentes, apresenta a menor taxa proporcional de vitimização declarada (31,7%) — o que pode refletir tanto diferenças reais quanto subnotificação. Sul e Centro-Oeste ficam próximos à média nacional.

---

## Visão geral dos 5 grupos

| Grupo | Variáveis | Principal achado |
|---|---|---|
| G_new4 | VD_REGIAO × P22 | Sul e Centro-Oeste conhecem mais a LMP; Norte tem maior desconhecimento total |
| G_new5 | VD_IDADE × P13 | Mulheres 40+ percebem mais o aumento da violência; jovens 16–29 relativizam mais |
| G_new6 | V14 × P46 | Baixa renda busca mais assistência de saúde após violência; alta renda busca menos |
| G_new7 | VD_IDADE × P62 | Faixas 35–49 solicitam mais medida protetiva; jovens e idosas solicitam menos |
| G_new8 | VD_REGIAO × P38 | Norte tem maior taxa de vitimização declarada (38%); Nordeste a menor (32%) |
