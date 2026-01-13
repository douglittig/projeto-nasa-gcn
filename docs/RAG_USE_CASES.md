# Casos de Uso RAG - NASA GCN Pipeline

Este documento descreve perguntas e cenários que um sistema de Retrieval-Augmented Generation (RAG) poderia responder utilizando os dados processados pelo pipeline NASA GCN.

## Visão Geral dos Dados

O pipeline processa dois tipos principais de dados da NASA GCN:

| Tipo | Descrição | Formato |
|------|-----------|---------|
| **Notices** | Alertas automáticos, machine-readable, em tempo real | JSON, Binary, VoEvent XML |
| **Circulars** | Boletins humanos, citáveis, com observações e análises | Texto livre (prosa científica) |

A camada **Gold** (`gcn_events_summarized`) une esses dados, criando um registro único por evento astronômico que combina:
- **Fatos estruturados**: Coordenadas, timestamps, classificações, probabilidades
- **Narrativa científica**: Discussões da comunidade, observações de follow-up, análises

---

## 🔭 Perguntas sobre Eventos Específicos

Perguntas que buscam informações consolidadas sobre um evento astronômico nomeado.

| Categoria | Pergunta Exemplo |
|-----------|------------------|
| **Síntese** | "Quais foram as principais observações sobre o GRB 230101A?" |
| **Contrapartida** | "O evento S190425z teve contrapartida óptica confirmada?" |
| **Localização** | "Quais telescópios reportaram posições refinadas para GRB 260109C?" |
| **Follow-up** | "Quais equipes observaram o afterglow do GRB 251230A?" |
| **Timeline** | "Qual foi a sequência de observações do GRB 260111A nas primeiras 24 horas?" |

---

## 🛰️ Perguntas Multi-Mensageiro

Perguntas que exploram a natureza multi-mensageira da astrofísica moderna (luz, ondas gravitacionais, neutrinos).

| Tipo de Mensageiro | Pergunta |
|--------------------|----------|
| **Ondas Gravitacionais** | "Quais eventos LIGO/Virgo/KAGRA tiveram GRBs associados?" |
| **Neutrinos** | "Houve observações ópticas ou de raios-X do alerta IceCube-260111A?" |
| **Coincidências** | "Quais eventos tiveram detecção simultânea por Swift e Fermi?" |
| **Fusões** | "Quais eventos de fusão de estrelas de nêutrons (BNS) tiveram follow-up eletromagnético?" |

---

## 📊 Perguntas Analíticas e de Tendência

Perguntas que agregam informações de múltiplos eventos para identificar padrões.

| Foco | Pergunta |
|------|----------|
| **Estatísticas** | "Quantos GRBs foram detectados pelo Swift no último mês?" |
| **Instrumentos** | "Quais instrumentos mais frequentemente detectam GRBs longos vs curtos?" |
| **Comunidade** | "Quais são os grupos de pesquisa mais ativos em follow-up óptico?" |
| **Tempo de Resposta** | "Qual o tempo médio entre o trigger do Fermi e a primeira circular de follow-up?" |
| **Cobertura** | "Qual porcentagem dos alertas de GRB recebeu observações de follow-up?" |

---

## 🔬 Perguntas Científicas Profundas

Perguntas que requerem compreensão do contexto científico e síntese de múltiplas fontes.

| Tema | Pergunta |
|------|----------|
| **Classificação** | "O GRB 260105C foi classificado como longo ou curto? Quais evidências suportam isso?" |
| **Redshift** | "Quais eventos tiveram redshift medido espectroscopicamente?" |
| **Kilonova** | "Houve evidência de kilonova para algum evento de fusão de estrelas de nêutrons recente?" |
| **Host Galaxy** | "Qual a galáxia hospedeira do GRB 250101B?" |
| **Energia** | "Quais foram os GRBs mais energéticos detectados este ano?" |
| **Progenitor** | "Quais hipóteses foram levantadas sobre o progenitor do GRB 251230A?" |

---

## 🎯 Perguntas de Alto Valor (Híbridas)

Estas perguntas demonstram o **valor único** do dataset GCN, cruzando dados estruturados (Notices) com narrativa científica (Circulars).

### Exemplo 1: Análise de Contrapartida Eletromagnética

> "Com base nas probabilidades de classificação do LIGO (BNS, BBH, NSBH) e nas observações reportadas pela comunidade, quais eventos de ondas gravitacionais de 2025 tiveram maior probabilidade de produzir uma contrapartida eletromagnética e foram efetivamente observados?"

**Por que é valiosa**: Cruza `prob_bns`, `prob_has_remnant` (Notices) com observações em Circulars.

### Exemplo 2: Coordenação de Follow-up

> "Para o GRB 260111A, quais foram as primeiras detecções em cada banda do espectro (raios-X, UV, óptico, rádio) e em quanto tempo após o trigger inicial?"

**Por que é valiosa**: Requer extração de timestamps e bandas de observação de múltiplos Circulars.

### Exemplo 3: Eficácia de Instrumentos

> "Compare a taxa de sucesso de localização entre o Einstein Probe (EP) e o Swift/BAT para eventos de raios-X transientes no último trimestre."

**Por que é valiosa**: Agrega performance de instrumentos a partir de alertas e confirmações/rejeições em Circulars.

---

## 🏗️ Arquitetura RAG Recomendada

```
┌─────────────────────────────────────────────────────────────┐
│                      Pergunta do Usuário                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Embedding da Pergunta                    │
│               (sentence-transformers / bge-m3)              │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Vector Search                           │
│            (Databricks Vector Search / FAISS)               │
│                                                             │
│   Busca em: gcn_events_summarized.scientific_narrative      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Contexto Recuperado                      │
│                                                             │
│   • event_id: S190425z                                      │
│   • circular_count: 47                                      │
│   • scientific_narrative: "SUBJECT: S190425z..."            │
│   • alert_type: PRELIMINARY                                 │
│   • prob_bns: 0.89                                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         LLM                                 │
│              (GPT-4, Claude, Llama, etc.)                   │
│                                                             │
│   Prompt: "Baseado no contexto, responda: {pergunta}"       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Resposta Gerada                          │
│                                                             │
│   "O evento S190425z, com probabilidade de 89% de ser uma   │
│    fusão de estrelas de nêutrons (BNS), recebeu 47          │
│    circulares de follow-up. As observações do ZTF e do      │
│    Pan-STARRS identificaram candidatos a contrapartida..."  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Referências

- [NASA GCN Documentation](https://gcn.nasa.gov/docs)
- [GCN Notices](https://gcn.nasa.gov/notices)
- [GCN Circulars](https://gcn.nasa.gov/circulars)
- [LIGO/Virgo/KAGRA Public Alerts](https://gracedb.ligo.org/)
