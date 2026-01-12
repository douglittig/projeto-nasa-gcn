# GCN Packet Types Reference

Este documento lista todos os tipos de pacotes GCN (Gamma-ray Coordinates Network) suportados pelo parser binário.

## Referência Oficial
📖 [GCN Socket Packet Definition Document](https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html)

---

## Estrutura do Pacote Binário

Cada pacote GCN tem exatamente **160 bytes** (40 inteiros de 4 bytes, big-endian).

| Slot | Campo | Descrição |
|------|-------|-----------|
| 0 | `pkt_type` | Tipo do pacote (ver tabelas abaixo) |
| 1 | `pkt_sernum` | Número serial do pacote |
| 4 | `trig_num` | ID do trigger |
| 5 | `burst_tjd` | Truncated Julian Day |
| 6 | `burst_sod` | Segundos do dia × 100 |
| 7 | `burst_ra` | RA × 100 ou × 10000 |
| 8 | `burst_dec` | Dec × 100 ou × 10000 |
| 11 | `burst_error` | Erro de posição |
| 18 | `trigger_id` | Flags do trigger |
| 19 | `misc` | Flags diversos |

---

## Tabela de Tipos de Pacotes

### Sistema/Básicos (1-11)
| Tipo | Nome | Status |
|------|------|--------|
| 1 | `BATSE_ORIGINAL` | ❌ Legado |
| 2 | `TEST` | ✅ Ativo |
| 3 | `IMALIVE` | ✅ Ativo |
| 4 | `KILL` | ✅ Ativo |
| 11 | `BATSE_MAXBC` | ❌ Legado |

### IPN - InterPlanetary Network (31-39)
| Tipo | Nome | Status |
|------|------|--------|
| 31 | `IPN_RAW` | ✅ Ativo |
| 32 | `IPN_SEGMENT` | ⚠️ Pendente |
| 39 | `IPN_POSITION` | ✅ Ativo |

### INTEGRAL (51-56)
| Tipo | Nome | Status |
|------|------|--------|
| 51 | `INTEGRAL_POINTDIR` | ✅ Ativo |
| 52 | `INTEGRAL_SPIACS` | ✅ Ativo |
| 53 | `INTEGRAL_WAKEUP` | ✅ Ativo |
| 54 | `INTEGRAL_REFINED` | ✅ Ativo |
| 55 | `INTEGRAL_OFFLINE` | ✅ Ativo |
| 56 | `INTEGRAL_WEAK` | ✅ Ativo |

### SWIFT (60-99, 103, 133, 140-141)
| Tipo | Nome | Status |
|------|------|--------|
| 60 | `SWIFT_BAT_GRB_ALERT` | ✅ Ativo |
| 61 | `SWIFT_BAT_GRB_POSITION` | ✅ Ativo |
| 62 | `SWIFT_BAT_GRB_NACK` | ✅ Ativo |
| 63 | `SWIFT_BAT_GRB_LC` | ✅ Ativo |
| 64 | `SWIFT_BAT_SCALED_MAP` | 🔒 Interno |
| 65 | `SWIFT_FOM_OBSERVE` | ✅ Ativo |
| 66 | `SWIFT_SC_SLEW` | ✅ Ativo |
| 67 | `SWIFT_XRT_POSITION` | ✅ Ativo |
| 68 | `SWIFT_XRT_SPECTRUM` | 🔒 Interno |
| 69 | `SWIFT_XRT_IMAGE` | ✅ Ativo |
| 70 | `SWIFT_XRT_LIGHTCURVE` | 🔒 Interno |
| 71 | `SWIFT_XRT_NACK_POSITION` | ✅ Ativo |
| 72 | `SWIFT_UVOT_IMAGE` | ✅ Ativo |
| 73 | `SWIFT_UVOT_SRC_LIST` | ✅ Ativo |
| 77 | `SWIFT_XRT_PROC_SPECTRUM` | 🔒 Interno |
| 78 | `SWIFT_XRT_PROC_IMAGE` | ✅ Ativo |
| 79 | `SWIFT_UVOT_PROC_IMAGE` | ✅ Ativo |
| 80 | `SWIFT_UVOT_PROC_SRC_LIST` | ✅ Ativo |
| 81 | `SWIFT_UVOT_POSITION` | ✅ Ativo |
| 82 | `SWIFT_BAT_GRB_POS_TEST` | ✅ Teste |
| 83 | `SWIFT_POINTDIR` | ✅ Ativo |
| 84 | `SWIFT_BAT_TRANS` | ✅ Ativo |
| 85 | `SWIFT_XRT_THRESHPIX` | 🔒 Interno |
| 86 | `SWIFT_XRT_THRESHPIX_PROC` | 🔒 Interno |
| 87 | `SWIFT_XRT_SPER` | 🔒 Interno |
| 88 | `SWIFT_XRT_SPER_PROC` | 🔒 Interno |
| 89 | `SWIFT_UVOT_NACK_POSITION` | ✅ Ativo |
| 97 | `SWIFT_BAT_QUICKLOOK_POSITION` | ✅ Ativo |
| 98 | `SWIFT_BAT_SUBTHRESHOLD_POSITION` | ✅ Ativo |
| 99 | `SWIFT_BAT_SLEW_GRB_POSITION` | ✅ Ativo |
| 103 | `SWIFT_ACTUAL_POINTDIR` | ✅ Ativo |
| 133 | `SWIFT_BAT_MONITOR` | ✅ Ativo |
| 140 | `SWIFT_BAT_SUB_SUB_THRESH_POS` | ✅ Ativo |
| 141 | `SWIFT_BAT_KNOWN_SRC_POS` | ✅ Ativo |

### SuperAGILE / AGILE (100-109)
| Tipo | Nome | Status |
|------|------|--------|
| 100 | `SUPERAGILE_GRB_WAKEUP` | ✅ Ativo |
| 101 | `SUPERAGILE_GRB_GROUND` | ✅ Ativo |
| 102 | `SUPERAGILE_GRB_REFINED` | ✅ Ativo |
| 105 | `AGILE_MCAL_ALERT` | ✅ Ativo |
| 107 | `AGILE_POINTDIR` | ✅ Ativo |
| 109 | `SUPERAGILE_GRB_POS_TEST` | ✅ Teste |

### FERMI GBM (110-119, 131)
| Tipo | Nome | Status |
|------|------|--------|
| 110 | `FERMI_GBM_ALERT` | ✅ Ativo |
| 111 | `FERMI_GBM_FLT_POS` | ✅ Ativo |
| 112 | `FERMI_GBM_GND_POS` | ✅ Ativo |
| 114 | `FERMI_GBM_GND_INTERNAL` | 🔒 Interno |
| 115 | `FERMI_GBM_FINAL_POS` | ✅ Ativo |
| 116 | `FERMI_GBM_ALERT_INTERNAL` | 🔒 Interno |
| 117 | `FERMI_GBM_FLT_INTERNAL` | 🔒 Interno |
| 119 | `FERMI_GBM_POS_TEST` | ✅ Teste |
| 131 | `FERMI_GBM_SUBTHRESHOLD` | ✅ Ativo |

### FERMI LAT (120-129, 144, 146)
| Tipo | Nome | Status |
|------|------|--------|
| 120 | `FERMI_LAT_GRB_POS_INI` | 🔒 Interno |
| 121 | `FERMI_LAT_GRB_POS_UPD` | ✅ Ativo |
| 122 | `FERMI_LAT_GRB_POS_DIAG` | 🔒 Interno |
| 123 | `FERMI_LAT_TRANS` | ✅ Ativo |
| 124 | `FERMI_LAT_GRB_POS_TEST` | ✅ Teste |
| 125 | `FERMI_LAT_MONITOR` | ✅ Ativo |
| 126 | `FERMI_SC_SLEW` | ✅ Ativo |
| 127 | `FERMI_LAT_GND` | ✅ Ativo |
| 128 | `FERMI_LAT_OFFLINE` | ✅ Ativo |
| 129 | `FERMI_POINTDIR` | ✅ Ativo |
| 144 | `FERMI_SC_SLEW_INTERNAL` | 🔒 Interno |
| 146 | `FERMI_GBM_FIN_POS_INTERNAL` | 🔒 Interno |

### MAXI (134-136)
| Tipo | Nome | Status |
|------|------|--------|
| 134 | `MAXI_UNKNOWN_SOURCE` | ✅ Ativo |
| 135 | `MAXI_KNOWN_SOURCE` | ✅ Ativo |
| 136 | `MAXI_TEST` | ✅ Teste |

### LVC - LIGO/Virgo/KAGRA (150-154, 163-164)
| Tipo | Nome | Status |
|------|------|--------|
| 150 | `LVC_PRELIMINARY` | ✅ Ativo |
| 151 | `LVC_INITIAL` | ✅ Ativo |
| 152 | `LVC_UPDATE` | ✅ Ativo |
| 153 | `LVC_TEST` | ❌ Descontinuado |
| 154 | `LVC_COUNTERPART` | ✅ Ativo |
| 163 | `LVC_EARLY_WARNING` | ✅ Ativo |
| 164 | `LVC_RETRACTION` | ✅ Ativo |

### AMON / IceCube (157-176)
| Tipo | Nome | Status |
|------|------|--------|
| 157 | `AMON_ICECUBE_COINC` | 🔒 Interno |
| 158 | `AMON_ICECUBE_HESE` | ❌ Substituído por 173/174 |
| 159 | `AMON_ICECUBE_TEST` | ✅ Teste |
| 160 | `CALET_GBM_FLT_LC` | ✅ Ativo |
| 161 | `CALET_GBM_GND_LC` | ✅ Ativo |
| 166 | `AMON_ICECUBE_CLUSTER` | 🔒 Interno |
| 168 | `GWHEN_COINC` | 🔒 Interno |
| 169 | `AMON_ICECUBE_EHE` | ❌ Substituído por 173/174 |
| 170 | `AMON_ANTARES_FERMILAT_COINC` | ❌ Terminado |
| 171 | `HAWC_BURST_MONITOR` | ✅ Ativo |
| 172 | `AMON_NU_EM_COINC` | ✅ Ativo |
| 173 | `ICECUBE_ASTROTRACK_GOLD` | ✅ Ativo |
| 174 | `ICECUBE_ASTROTRACK_BRONZE` | ✅ Ativo |
| 175 | `SK_SUPERNOVA` | ✅ Ativo |
| 176 | `AMON_ICECUBE_CASCADE` | ✅ Ativo |

### GECAM (188-189)
| Tipo | Nome | Status |
|------|------|--------|
| 188 | `GECAM_FLT` | ✅ Ativo |
| 189 | `GECAM_GND` | ✅ Ativo |

### Outros
| Tipo | Nome | Status |
|------|------|--------|
| 130 | `SIMBAD_NED_SEARCH_RESULTS` | ✅ Ativo |
| 137 | `OGLE` | ⚠️ Pendente |
| 139 | `MOA` | ✅ Ativo |
| 145 | `COINCIDENCE` | ✅ Ativo |
| 148 | `SUZAKU_LIGHTCURVE` | ✅ Ativo |
| 149 | `SNEWS` | ✅ Ativo |

---

## Legenda de Status

| Símbolo | Significado |
|---------|-------------|
| ✅ | Ativo - disponível para público |
| 🔒 | Interno - apenas equipe da missão |
| ❌ | Legado/Descontinuado |
| ⚠️ | Pendente - pode ser reativado |

---

## Uso no Pipeline

```python
from nasa_gcn.binary_parser import get_packet_type_name, parse_gcn_binary_packet

# Obter nome do tipo
name = get_packet_type_name(61)  # "SWIFT_BAT_GRB_POSITION"

# Parsear pacote completo
result = parse_gcn_binary_packet(binary_data)
print(result["pkt_type_name"])  # Nome legível
```

---

## Referências

- [GCN Kafka Client](https://gcn.nasa.gov/docs/client)
- [Socket Packet Definition](https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html)
- [GCN Mission Topics](https://gcn.nasa.gov/missions)
