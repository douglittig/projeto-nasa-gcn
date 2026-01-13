# Roadmap: Próximos Passos e Ideias de Evolução

Este documento consolida ideias para evolução do pipeline NASA GCN, incluindo novas tabelas Gold, cruzamentos de dados, e fontes externas para enriquecimento.

---

## 🗄️ Novas Tabelas Gold Propostas

### 1. `gold_grb_catalog`
**Objetivo**: Catálogo consolidado de Gamma-Ray Bursts com metadados enriquecidos.

| Campo | Fonte | Descrição |
|-------|-------|-----------|
| `grb_id` | Notices | Identificador padrão (ex: GRB 260111A) |
| `trigger_time` | Notices | Timestamp do primeiro trigger |
| `detecting_instruments` | Notices | Lista de instrumentos (Swift, Fermi, GECAM, etc.) |
| `best_ra_dec` | Notices | Coordenadas mais precisas disponíveis |
| `localization_error` | Notices | Erro de localização em arcmin/arcsec |
| `duration_t90` | Circulars | Duração T90 (extraída via NLP) |
| `classification` | Circulars | Longo/Curto (extraída via NLP) |
| `redshift` | Circulars | Redshift espectroscópico (se disponível) |
| `host_galaxy` | Circulars | Nome da galáxia hospedeira |
| `has_afterglow` | Circulars | Booleano: contrapartida óptica/X detectada? |
| `circular_count` | Pipeline | Total de circulares sobre o evento |

**Join Strategy**: 
- Agregar `gcn_notices` + `gcn_classic_binary` por `grb_id`
- Left join com `gcn_circulars` agregadas
- Usar regex/NLP para extrair T90, redshift, classificação do corpo dos circulares

---

### 2. `gold_multimessenger_events`
**Objetivo**: Eventos com detecção em múltiplos "mensageiros" (luz, ondas gravitacionais, neutrinos).

| Campo | Fonte | Descrição |
|-------|-------|-----------|
| `event_id` | Derivado | Identificador unificado |
| `messengers` | Derivado | Array: ["gamma", "gw", "nu", "optical"] |
| `gw_superevent_id` | `igwn_gwalert` | ID do evento LIGO/Virgo/KAGRA |
| `grb_id` | Notices | GRB associado (se houver) |
| `neutrino_event_id` | Notices | Alerta IceCube (se houver) |
| `temporal_coincidence` | Calculado | Diferença temporal entre detecções |
| `spatial_coincidence` | Calculado | Sobreposição de regiões de erro |
| `significance` | `igwn_gwalert` | FAR (False Alarm Rate) |
| `classification_probs` | `igwn_gwalert` | Probabilidades BNS/BBH/NSBH |

**Join Strategy**:
- Window join temporal: eventos dentro de ±1000 segundos
- Spatial match: sobreposição de regiões de localização (requer geometria esférica)
- Cross-match com alertas IceCube (`gcn_notices` onde `mission = 'icecube'`)

---

### 3. `gold_followup_timeline`
**Objetivo**: Linha do tempo de observações de follow-up por evento.

| Campo | Fonte | Descrição |
|-------|-------|-----------|
| `event_id` | Derivado | Identificador do evento |
| `circular_id` | `gcn_circulars` | ID da circular |
| `time_since_trigger` | Calculado | Tempo decorrido desde T0 |
| `observing_team` | `gcn_circulars` | Equipe/Telescópio (extraído do submitter) |
| `observation_band` | Circulars | Banda: raio-X, UV, óptico, rádio (NLP) |
| `detection_status` | Circulars | Detecção/Upper-limit (NLP) |
| `magnitude_or_flux` | Circulars | Valor reportado (NLP) |

**Valor**: Permite análises de tempo de resposta da comunidade e eficácia de instrumentos.

---

### 4. `gold_instrument_performance`
**Objetivo**: Métricas agregadas de performance por instrumento/missão.

| Campo | Fonte | Descrição |
|-------|-------|-----------|
| `instrument` | Notices | Nome do instrumento (Swift/BAT, Fermi/GBM, etc.) |
| `period` | Calculado | Mês/Trimestre/Ano |
| `trigger_count` | Notices | Total de triggers |
| `confirmed_grb_count` | Circulars | GRBs confirmados |
| `false_positive_rate` | Calculado | Triggers não-astrofísicos |
| `avg_localization_error` | Notices | Erro médio de localização |
| `median_response_time` | Circulars | Tempo mediano até primeira circular |

---

## 🔗 Fontes Externas para Enriquecimento

### 1. HEASARC (High Energy Astrophysics Science Archive)
**URL**: https://heasarc.gsfc.nasa.gov/

| Catálogo | Descrição | Uso Potencial |
|----------|-----------|---------------|
| **GRBCAT** | Catálogo histórico de GRBs | Enriquecer com dados históricos |
| **Swift Master** | Todas observações Swift | Detalhes de exposição e instrumentos |
| **Fermi GBM Burst** | Parâmetros espectrais de GRBs | T90, fluência, hardness ratio |

**Integração**: API REST via `astroquery.heasarc` ou download de catálogos em FITS/CSV.

```python
from astroquery.heasarc import Heasarc
heasarc = Heasarc()
result = heasarc.query_object("GRB 230101A", mission="grbcat")
```

---

### 2. GraceDB (Gravitational-Wave Candidate Event Database)
**URL**: https://gracedb.ligo.org/

| Dado | Descrição | Uso Potencial |
|------|-----------|---------------|
| **Superevent Details** | Parâmetros detalhados do evento GW | Enriquecer `igwn_gwalert` |
| **Sky Maps** | Mapas de localização em FITS | Análise espacial avançada |
| **EM Bright** | Probabilidade de contrapartida EM | Priorização de follow-up |

**Integração**: API REST pública (JSON).

```python
import requests
response = requests.get("https://gracedb.ligo.org/api/superevents/S190425z/")
data = response.json()
```

---

### 3. SIMBAD (Set of Identifications, Measurements, and Bibliography)
**URL**: http://simbad.cds.unistra.fr/

| Dado | Descrição | Uso Potencial |
|------|-----------|---------------|
| **Object Types** | Classificação de objetos astronômicos | Identificar galáxias hospedeiras |
| **Cross-IDs** | Nomes alternativos de objetos | Desambiguação de eventos |
| **Bibliography** | Referências de artigos | Enriquecer narrativa científica |

**Integração**: TAP/ADQL queries ou `astroquery.simbad`.

---

### 4. TNS (Transient Name Server)
**URL**: https://www.wis-tns.org/

| Dado | Descrição | Uso Potencial |
|------|-----------|---------------|
| **Supernova Classifications** | Classificação espectral de SNe | Identificar contrapartidas ópticas |
| **Transient Coordinates** | Posições precisas de transientes | Cross-match com GRBs |

**Integração**: API REST (requer registro).

---

### 5. NASA Exoplanet Archive
**URL**: https://exoplanetarchive.ipac.caltech.edu/

| Dado | Descrição | Uso Potencial |
|------|-----------|---------------|
| **Host Stars** | Propriedades de estrelas hospedeiras | Contexto para MOA (microlensing) |

---

### 6. Open Astronomy Catalogs (OAC)
**URL**: https://github.com/astrocatalogs

| Catálogo | Descrição | Uso Potencial |
|----------|-----------|---------------|
| **Open Supernova Catalog** | SNe com dados agregados | Cross-match kilonovae |
| **Open TDE Catalog** | Tidal Disruption Events | Eventos MAXI/EP |

---

## 🔀 Cruzamentos de Dados Interessantes

### 1. GRB ↔ Gravitational Waves
**Hipótese**: GRBs curtos são produzidos por fusões de estrelas de nêutrons (detectáveis por LIGO).

**Implementação**:
```sql
SELECT 
    g.grb_id,
    gw.superevent_id,
    ABS(g.trigger_time - gw.trigger_time) AS time_diff_seconds,
    gw.prob_bns
FROM gold_grb_catalog g
JOIN igwn_gwalert gw 
    ON ABS(UNIX_TIMESTAMP(g.trigger_time) - UNIX_TIMESTAMP(gw.trigger_time)) < 10
WHERE g.classification = 'short'
  AND gw.prob_bns > 0.5
```

---

### 2. Neutrino Alerts ↔ Blazar Flares
**Hipótese**: Neutrinos de alta energia podem vir de blazares em flare.

**Implementação**:
- Filtrar `gcn_notices` onde `mission = 'icecube'`
- Cruzar com catálogo de blazares (SIMBAD/Fermi-LAT)
- Verificar circulares mencionando Fermi-LAT/AGILE detections

---

### 3. Einstein Probe ↔ Swift Follow-up
**Hipótese**: Novos transientes detectados pelo Einstein Probe recebem follow-up do Swift.

**Implementação**:
- Filtrar `gcn_notices` onde `mission = 'einstein_probe'`
- Procurar circulares com "Swift ToO" no subject
- Calcular tempo de resposta

---

### 4. GRB Afterglows ↔ Host Galaxy Redshift
**Hipótese**: GRBs com redshift medido permitem estudos cosmológicos.

**Implementação**:
- Extrair redshift de circulares via regex: `z\s*[=~]\s*(\d+\.?\d*)`
- Enriquecer com dados de SIMBAD sobre a galáxia hospedeira
- Calcular distância de luminosidade

---

## 🧪 Experimentos de NLP/ML

### 1. Extração de Entidades (NER)
Treinar modelo para extrair:
- Nomes de instrumentos
- Coordenadas (RA/Dec)
- Magnitudes/Fluxos
- Timestamps
- Classificações (longo/curto, BNS/BBH)

### 2. Classificação de Circulares
Categorizar automaticamente:
- Detecção inicial
- Follow-up observation
- Upper limit
- Retraction
- Request for observations

### 3. Similaridade Semântica
Agrupar eventos relacionados que podem ter nomenclaturas diferentes (ex: EP260110a = GRB 260110B?).

---

## 📊 Métricas de Sucesso

| Métrica | Descrição | Valor Alvo |
|---------|-----------|------------|
| **Taxa de Enriquecimento** | % de eventos com dados externos | > 50% |
| **Latência de Ingestão** | Tempo desde Kafka até Gold | < 5 minutos |
| **Cobertura de Cross-Match** | % de GW events com follow-up | Baseline atual |
| **Precisão de NLP** | Acurácia de extração de redshift | > 90% |

---

## 🗓️ Priorização Sugerida

| Fase | Objetivo | Esforço |
|------|----------|---------|
| **1** | `gold_grb_catalog` básico (sem NLP) | Baixo |
| **2** | Integração HEASARC (GRBCAT) | Médio |
| **3** | `gold_multimessenger_events` | Médio |
| **4** | Extração NLP de redshift/T90 | Alto |
| **5** | Integração GraceDB/SIMBAD | Médio |
| **6** | Dashboard de métricas | Médio |

---

## 📚 Referências

- [GCN Missions](https://gcn.nasa.gov/missions)
- [HEASARC Archive](https://heasarc.gsfc.nasa.gov/docs/archive.html)
- [GraceDB API](https://gracedb.ligo.org/documentation/api.html)
- [SIMBAD TAP](http://simbad.cds.unistra.fr/simbad/sim-tap)
- [NASA Open APIs](https://api.nasa.gov/)
- [Astroquery Documentation](https://astroquery.readthedocs.io/)
