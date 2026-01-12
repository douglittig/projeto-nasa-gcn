# GCN Notices - Schema para RAG

Documentação da tabela `gcn_notices` otimizada para pipelines de Retrieval-Augmented Generation (RAG).

---

## Visão Geral

A tabela `gcn_notices` contém alertas do GCN no novo formato JSON, originados de múltiplas missões:
- **IceCube** - Neutrinos de alta energia
- **Super-Kamiokande** - Detecção de supernovas via neutrinos
- **Fermi** - Gamma-ray bursts
- **Swift** - Transientes de raios-X/gama
- **LIGO/Virgo** - Ondas gravitacionais

---

## Schema da Tabela

### Campos Extraídos do JSON

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `mission` | STRING | Missão (do tópico) | `icecube`, `superk` |
| `mission_name` | STRING | Nome completo da missão | `IceCube`, `Super-Kamiokande` |
| `instrument` | STRING | Instrumento utilizado | `IC86` |
| `messenger` | STRING | Tipo de mensageiro | `Neutrino`, `GW`, `Gamma-ray` |
| `notice_id` | STRING | ID único do notice | `SN.097021.000969` |
| `pipeline` | STRING | Pipeline de processamento | `snwatch`, `Bronze Track Alert` |
| `alert_type` | STRING | Tipo do alerta | `initial`, `update`, `retraction` |
| `alert_tense` | STRING | Estado do alerta | `test`, `real` |

### Timestamps

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `trigger_time` | STRING | Momento do trigger (ISO8601) |
| `alert_datetime` | STRING | Momento do alerta (ISO8601) |

### Coordenadas Celestes

| Campo | Tipo | Descrição | Range |
|-------|------|-----------|-------|
| `ra` | DOUBLE | Right Ascension em graus | 0-360 |
| `dec` | DOUBLE | Declination em graus | -90 a +90 |
| `ra_dec_error` | STRING | Erro de posição | `0.5`, `0.7` |
| `containment_probability` | STRING | Probabilidade de conter a fonte | `0.68`, `0.9` |

### Campos Específicos - Neutrinos (IceCube)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `n_events` | STRING | Número de eventos detectados |
| `nu_energy` | STRING | Energia do neutrino (TeV) |
| `p_astro` | STRING | Probabilidade de origem astrofísica |

### Campos Específicos - Supernovas (Super-Kamiokande)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `luminosity_distance` | STRING | Distância luminosa (Mpc) |

### Campos para RAG

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `document_text` | STRING | Texto formatado para embedding |
| `json_length` | INT | Tamanho do JSON (filtro básico) |
| `notice_json` | STRING | JSON original completo |

---

## Formato do `document_text`

O campo `document_text` é formatado para embedding:

```
MISSION: IceCube | MESSENGER: Neutrino | TYPE: update | ID: IceCube-251225A | RA: 297.42 | DEC: 22.47
```

---

## Missões e Tópicos

| Missão | Tópico Kafka | Messenger |
|--------|--------------|-----------|
| IceCube | `gcn.notices.icecube.*` | Neutrino |
| Super-Kamiokande | `gcn.notices.superk.*` | Neutrino |
| Fermi GBM | `gcn.notices.fermi.gbm.*` | Gamma-ray |
| Swift | `gcn.notices.swift.*` | X-ray, Gamma-ray |
| LIGO/Virgo | `gcn.notices.lvc.*` | Gravitational Wave |

---

## Queries de Exemplo

### Listar notices por missão
```sql
SELECT mission_name, messenger, COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_notices
GROUP BY mission_name, messenger
ORDER BY total DESC;
```

### Filtrar alertas reais (não-teste)
```sql
SELECT notice_id, mission_name, alert_type, trigger_time, ra, dec
FROM sandbox.nasa_gcn_dev.gcn_notices
WHERE alert_tense = 'real'
ORDER BY trigger_time DESC
LIMIT 20;
```

### Buscar neutrinos de alta energia
```sql
SELECT notice_id, mission_name, nu_energy, p_astro, ra, dec
FROM sandbox.nasa_gcn_dev.gcn_notices
WHERE messenger = 'Neutrino'
  AND CAST(nu_energy AS DOUBLE) > 100
ORDER BY CAST(nu_energy AS DOUBLE) DESC;
```

### Buscar por coordenadas (cone search)
```sql
SELECT notice_id, mission_name, ra, dec, ra_dec_error
FROM sandbox.nasa_gcn_dev.gcn_notices
WHERE ra BETWEEN 290 AND 310
  AND dec BETWEEN 15 AND 30;
```

---

## Referências

- [GCN Kafka Topics](https://gcn.nasa.gov/docs/client)
- [IceCube Alerts](https://gcn.gsfc.nasa.gov/amon_icecube_gold_bronze_events.html)
- [Super-Kamiokande SNEWS](https://snews.bnl.gov/)
