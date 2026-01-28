"""
NASA GCN Binary Packet Parser

Este módulo contém funções para decodificar os pacotes binários de 160 bytes
enviados pelo GCN (Gamma-ray Coordinates Network) usando o formato legado
BACODINE.

Referência: https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html

Autores: Projeto NASA GCN Databricks
"""

import struct
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

# ==============================================================================
# MAPEAMENTO DE TIPOS DE PACOTES GCN
# ==============================================================================
# Baseado em: https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html (07 Dec 2021)
# Nota: Muitos tipos são legados/inativos mas incluídos para completude

PACKET_TYPE_NAMES: Dict[int, str] = {
    # Pacotes básicos/sistema
    1: "BATSE_ORIGINAL",  # NO LONGER AVAILABLE (GRO de-orbit)
    2: "TEST",
    3: "IMALIVE",
    4: "KILL",
    # BATSE (NO LONGER AVAILABLE)
    11: "BATSE_MAXBC",
    21: "BRADFORD_TEST",
    22: "BATSE_FINAL",
    24: "BATSE_LOCBURST",
    # ALEXIS (NO LONGER AVAILABLE)
    25: "ALEXIS",
    # RXTE (NO LONGER AVAILABLE / NOT AVAILABLE)
    26: "RXTE_PCA_ALERT",
    27: "RXTE_PCA",
    28: "RXTE_ASM_ALERT",
    29: "RXTE_ASM",
    # COMPTEL (NO LONGER AVAILABLE)
    30: "COMPTEL",
    # IPN
    31: "IPN_RAW",
    32: "IPN_SEGMENT",
    # SAX (NO LONGER AVAILABLE)
    33: "SAX_WFC_ALERT",
    34: "SAX_WFC",
    35: "SAX_NFI_ALERT",
    36: "SAX_NFI",
    # RXTE
    37: "RXTE_ASM_XTRANS",
    38: "SPARE_TESTING",
    39: "IPN_POSITION",
    # HETE (NO LONGER AVAILABLE)
    40: "HETE_S/C_ALERT",
    41: "HETE_S/C_UPDATE",
    42: "HETE_S/C_LAST",
    43: "HETE_GNDANA",
    44: "HETE_TEST",
    # Counterpart e Swift TOO
    45: "GRB_COUNTERPART",
    46: "SWIFT_TOO_FOM_OBSERVE",
    47: "SWIFT_TOO_SC_SLEW",
    48: "DOW_TOD_TEST",
    # INTEGRAL
    51: "INTEGRAL_POINTDIR",
    52: "INTEGRAL_SPIACS",
    53: "INTEGRAL_WAKEUP",
    54: "INTEGRAL_REFINED",
    55: "INTEGRAL_OFFLINE",
    56: "INTEGRAL_WEAK",
    # AAVSO / MILAGRO
    57: "AAVSO",
    58: "MILAGRO",
    59: "KONUS_LIGHTCURVE",
    # =========================================================================
    # SWIFT (60-99, 103, 133, 140, 141)
    # =========================================================================
    60: "SWIFT_BAT_GRB_ALERT",
    61: "SWIFT_BAT_GRB_POSITION",
    62: "SWIFT_BAT_GRB_NACK",
    63: "SWIFT_BAT_GRB_LC",
    64: "SWIFT_BAT_SCALED_MAP",  # NOT PUBLIC, SWIFT TEAM ONLY
    65: "SWIFT_FOM_OBSERVE",
    66: "SWIFT_SC_SLEW",
    67: "SWIFT_XRT_POSITION",
    68: "SWIFT_XRT_SPECTRUM",  # NOT PUBLIC, SWIFT TEAM ONLY
    69: "SWIFT_XRT_IMAGE",
    70: "SWIFT_XRT_LIGHTCURVE",  # NOT PUBLIC, SWIFT TEAM ONLY
    71: "SWIFT_XRT_NACK_POSITION",
    72: "SWIFT_UVOT_IMAGE",
    73: "SWIFT_UVOT_SRC_LIST",
    76: "SWIFT_BAT_GRB_PROC_LC",  # NOT YET AVAILABLE
    77: "SWIFT_XRT_PROC_SPECTRUM",  # NOT PUBLIC, SWIFT TEAM ONLY
    78: "SWIFT_XRT_PROC_IMAGE",
    79: "SWIFT_UVOT_PROC_IMAGE",
    80: "SWIFT_UVOT_PROC_SRC_LIST",
    81: "SWIFT_UVOT_POSITION",
    82: "SWIFT_BAT_GRB_POS_TEST",
    83: "SWIFT_POINTDIR",
    84: "SWIFT_BAT_TRANS",
    85: "SWIFT_XRT_THRESHPIX",  # NOT PUBLIC, SWIFT TEAM ONLY
    86: "SWIFT_XRT_THRESHPIX_PROC",  # NOT PUBLIC, SWIFT TEAM ONLY
    87: "SWIFT_XRT_SPER",  # NOT PUBLIC, SWIFT TEAM ONLY
    88: "SWIFT_XRT_SPER_PROC",  # NOT PUBLIC, SWIFT TEAM ONLY
    89: "SWIFT_UVOT_NACK_POSITION",
    97: "SWIFT_BAT_QUICKLOOK_POSITION",
    98: "SWIFT_BAT_SUBTHRESHOLD_POSITION",
    99: "SWIFT_BAT_SLEW_GRB_POSITION",
    103: "SWIFT_ACTUAL_POINTDIR",
    133: "SWIFT_BAT_MONITOR",
    140: "SWIFT_BAT_SUB_SUB_THRESH_POS",
    141: "SWIFT_BAT_KNOWN_SRC_POS",
    # =========================================================================
    # SuperAGILE / AGILE (100-109)
    # =========================================================================
    100: "SUPERAGILE_GRB_WAKEUP",
    101: "SUPERAGILE_GRB_GROUND",
    102: "SUPERAGILE_GRB_REFINED",
    105: "AGILE_MCAL_ALERT",
    107: "AGILE_POINTDIR",
    109: "SUPERAGILE_GRB_POS_TEST",
    # =========================================================================
    # FERMI GBM (110-119, 131)
    # =========================================================================
    110: "FERMI_GBM_ALERT",
    111: "FERMI_GBM_FLT_POS",
    112: "FERMI_GBM_GND_POS",
    114: "FERMI_GBM_GND_INTERNAL",  # NOT PUBLIC, FERMI TEAM ONLY
    115: "FERMI_GBM_FINAL_POS",
    116: "FERMI_GBM_ALERT_INTERNAL",  # NOT PUBLIC, FERMI TEAM ONLY
    117: "FERMI_GBM_FLT_INTERNAL",  # NOT PUBLIC, FERMI TEAM ONLY
    119: "FERMI_GBM_POS_TEST",
    131: "FERMI_GBM_SUBTHRESHOLD",
    # =========================================================================
    # FERMI LAT (120-129, 144, 146)
    # =========================================================================
    120: "FERMI_LAT_GRB_POS_INI",  # NOT PUBLIC, FERMI TEAM ONLY
    121: "FERMI_LAT_GRB_POS_UPD",
    122: "FERMI_LAT_GRB_POS_DIAG",  # NOT PUBLIC, FERMI TEAM ONLY
    123: "FERMI_LAT_TRANS",
    124: "FERMI_LAT_GRB_POS_TEST",
    125: "FERMI_LAT_MONITOR",
    126: "FERMI_SC_SLEW",
    127: "FERMI_LAT_GND",
    128: "FERMI_LAT_OFFLINE",
    129: "FERMI_POINTDIR",
    144: "FERMI_SC_SLEW_INTERNAL",  # NOT PUBLIC, FERMI TEAM ONLY
    146: "FERMI_GBM_FIN_POS_INTERNAL",  # NOT PUBLIC, FERMI TEAM ONLY
    # =========================================================================
    # MISC (130, 134-137, 139, 145, 148, 149)
    # =========================================================================
    130: "SIMBAD_NED_SEARCH_RESULTS",
    134: "MAXI_UNKNOWN_SOURCE",
    135: "MAXI_KNOWN_SOURCE",
    136: "MAXI_TEST",
    137: "OGLE",
    139: "MOA",
    145: "COINCIDENCE",
    148: "SUZAKU_LIGHTCURVE",
    149: "SNEWS",
    # =========================================================================
    # LVC - LIGO/Virgo/KAGRA Gravitational Waves (150-154, 163, 164)
    # =========================================================================
    150: "LVC_PRELIMINARY",
    151: "LVC_INITIAL",
    152: "LVC_UPDATE",
    153: "LVC_TEST",  # DISCONTINUED BY LVC
    154: "LVC_COUNTERPART",
    163: "LVC_EARLY_WARNING",
    164: "LVC_RETRACTION",
    # =========================================================================
    # AMON / ICECUBE (157-159, 166, 169, 170-176)
    # =========================================================================
    157: "AMON_ICECUBE_COINC",  # NOT YET PUBLIC, AMON TEAM ONLY
    158: "AMON_ICECUBE_HESE",  # REPLACED BY 173/174
    159: "AMON_ICECUBE_TEST",
    160: "CALET_GBM_FLT_LC",
    161: "CALET_GBM_GND_LC",
    166: "AMON_ICECUBE_CLUSTER",  # NOT YET PUBLIC, AMON TEAM ONLY
    168: "GWHEN_COINC",  # NOT YET PUBLIC, GWHEN TEAM ONLY
    169: "AMON_ICECUBE_EHE",  # REPLACED BY 173/174
    170: "AMON_ANTARES_FERMILAT_COINC",  # TERMINATED BY AMON 08sep19
    171: "HAWC_BURST_MONITOR",
    172: "AMON_NU_EM_COINC",
    173: "ICECUBE_ASTROTRACK_GOLD",
    174: "ICECUBE_ASTROTRACK_BRONZE",
    175: "SK_SUPERNOVA",
    176: "AMON_ICECUBE_CASCADE",
    # =========================================================================
    # GECAM (188-189)
    # =========================================================================
    188: "GECAM_FLT",
    189: "GECAM_GND",
}


# TJD (Truncated Julian Day) epoch: 1968-05-24 00:00:00 UTC (MJD 40000)
TJD_EPOCH = datetime(1968, 5, 24, 0, 0, 0)


def get_packet_type_name(pkt_type: int) -> str:
    """
    Retorna o nome legível para um tipo de pacote GCN.

    Args:
        pkt_type: Número do tipo de pacote (0-255)

    Returns:
        Nome do tipo de pacote ou "UNKNOWN_{num}" se não mapeado
    """
    return PACKET_TYPE_NAMES.get(pkt_type, f"UNKNOWN_{pkt_type}")


def tjd_sod_to_datetime(tjd: int, sod_centi: int) -> Optional[datetime]:
    """
    Converte timestamp GCN (TJD + SOD em centi-segundos) para datetime.

    O GCN usa Truncated Julian Day (TJD = JD - 2440000.5) e
    Seconds-of-Day em unidades de centi-segundos (sod * 100).

    Args:
        tjd: Truncated Julian Day (dias desde 1968-05-24)
        sod_centi: Segundos do dia * 100 (centi-segundos)

    Returns:
        datetime ou None se os valores forem inválidos

    Examples:
        >>> tjd_sod_to_datetime(10281, 4320000)  # TJD 10281 = 17 Jul 1996
        datetime.datetime(1996, 7, 17, 12, 0, 0)
    """
    if tjd <= 0 or sod_centi < 0:
        return None

    try:
        sod_seconds = sod_centi / 100.0
        return TJD_EPOCH + timedelta(days=tjd, seconds=sod_seconds)
    except (ValueError, OverflowError):
        return None


def centi_to_deg(value: int, scale: int = 100) -> float:
    """
    Converte valor escalonado (centi-graus ou 10^-4 graus) para graus decimais.

    O GCN usa dois níveis de escala para coordenadas:
    - 100x (centi-graus) para fontes com maior incerteza
    - 10000x (0.0001 graus) para fontes com melhor precisão

    Args:
        value: Valor inteiro escalonado
        scale: Fator de escala (100 ou 10000)

    Returns:
        Valor em graus decimais
    """
    return value / scale


def parse_gcn_binary_packet(binary_data: bytes) -> Dict[str, Any]:
    """
    Decodifica um pacote binário GCN de 160 bytes.

    O pacote GCN consiste em 40 inteiros de 4 bytes (big-endian).
    Esta função extrai os campos mais comuns que são compartilhados
    entre a maioria dos tipos de pacotes.

    Args:
        binary_data: Bytes do pacote GCN (deve ter exatamente 160 bytes)

    Returns:
        Dicionário com os campos parseados:
        - pkt_type: int - Tipo do pacote
        - pkt_type_name: str - Nome legível do tipo
        - pkt_sernum: int - Número serial do pacote
        - trig_num: int - Número do trigger (se aplicável)
        - burst_tjd: int - Truncated Julian Day
        - burst_sod_centi: int - Segundos do dia em centi-segundos
        - burst_datetime: str - ISO timestamp
        - burst_ra_deg: float - RA em graus decimais
        - burst_dec_deg: float - Dec em graus decimais
        - burst_error_deg: float - Erro de posição em graus
        - trigger_id: int - ID/flags do trigger
        - misc: int - Campo misc/flags
        - parse_error: str - Mensagem de erro se parsing falhou

    References:
        https://gcn.gsfc.nasa.gov/sock_pkt_def_doc.html
    """
    result: Dict[str, Any] = {
        "pkt_type": None,
        "pkt_type_name": None,
        "pkt_sernum": None,
        "trig_num": None,
        "burst_tjd": None,
        "burst_sod_centi": None,
        "burst_datetime": None,
        "burst_ra_deg": None,
        "burst_dec_deg": None,
        "burst_error_deg": None,
        "trigger_id": None,
        "misc": None,
        "parse_error": None,
    }

    # Validação de entrada
    if binary_data is None:
        result["parse_error"] = "binary_data is None"
        return result

    if len(binary_data) != 160:
        result["parse_error"] = f"Invalid packet size: {len(binary_data)} bytes (expected 160)"
        return result

    try:
        # Desempacota 40 inteiros de 4 bytes (big-endian, signed)
        longs = struct.unpack(">40i", binary_data)

        # Campos comuns (slots 0-8, 11, 18-19)
        pkt_type = longs[0]
        result["pkt_type"] = pkt_type
        result["pkt_type_name"] = get_packet_type_name(pkt_type)
        result["pkt_sernum"] = longs[1]

        # Trigger number (slot 4) - nem todos os tipos usam
        trig_num = longs[4]
        result["trig_num"] = trig_num if trig_num > 0 else None

        # Timestamp: TJD (slot 5) e SOD em centi-segundos (slot 6)
        burst_tjd = longs[5]
        burst_sod = longs[6]
        result["burst_tjd"] = burst_tjd
        result["burst_sod_centi"] = burst_sod

        if burst_tjd > 0 and burst_sod >= 0:
            burst_dt = tjd_sod_to_datetime(burst_tjd, burst_sod)
            if burst_dt:
                result["burst_datetime"] = burst_dt.isoformat()

        # Coordenadas: RA (slot 7), Dec (slot 8), Error (slot 11)
        burst_ra = longs[7]
        burst_dec = longs[8]
        burst_error = longs[11]

        # Detecção heurística da escala (100 vs 10000)
        # Valores > 36000 ou < 0 indicam escala 10000
        if burst_ra > 36000 or burst_ra < 0 or abs(burst_dec) > 9000:
            scale = 10000
        else:
            scale = 100

        ra_deg = centi_to_deg(burst_ra, scale)
        dec_deg = centi_to_deg(burst_dec, scale)
        err_deg = centi_to_deg(abs(burst_error), scale)

        # Validação de ranges
        if 0 <= ra_deg < 360:
            result["burst_ra_deg"] = ra_deg
        if -90 <= dec_deg <= 90:
            result["burst_dec_deg"] = dec_deg
        result["burst_error_deg"] = err_deg

        # Trigger ID e Misc flags (slots 18-19)
        result["trigger_id"] = longs[18]
        result["misc"] = longs[19]

    except struct.error as e:
        result["parse_error"] = f"Struct unpack error: {e}"
    except Exception as e:
        result["parse_error"] = f"Unexpected error: {e}"

    return result


# Schema para uso com Spark UDF
PARSED_BINARY_SCHEMA = """
    pkt_type INT,
    pkt_type_name STRING,
    pkt_sernum INT,
    trig_num INT,
    burst_tjd INT,
    burst_sod_centi INT,
    burst_datetime STRING,
    burst_ra_deg DOUBLE,
    burst_dec_deg DOUBLE,
    burst_error_deg DOUBLE,
    trigger_id INT,
    misc INT,
    parse_error STRING
"""
