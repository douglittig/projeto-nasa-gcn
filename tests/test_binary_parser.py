"""
Testes para o módulo binary_parser.

Para rodar:
    cd /Users/douglaslittig/Documents/workspace/projeto-nasa-gcn
    uv run pytest tests/test_binary_parser.py -v
"""

import struct
import pytest
from datetime import datetime

from nasa_gcn.binary_parser import (
    parse_gcn_binary_packet,
    tjd_sod_to_datetime,
    centi_to_deg,
    get_packet_type_name,
    TJD_EPOCH,
)


class TestTjdSodToDatetime:
    """Testes para conversão TJD+SOD para datetime."""

    def test_known_date(self):
        """Testa conversão de uma data conhecida."""
        # TJD 10281 = 17 Jul 1996 (exemplo da documentação NASA)
        # TJD = dias desde 1968-05-24
        # 10281 dias = ~28 anos
        result = tjd_sod_to_datetime(10281, 0)
        assert result is not None
        # 1968-05-24 + 10281 dias = 1996-07-17
        assert result.year == 1996
        assert result.month == 7
        assert result.day == 17

    def test_with_seconds(self):
        """Testa conversão com seconds-of-day."""
        # 12:00:00 = 43200 segundos = 4320000 centi-segundos
        result = tjd_sod_to_datetime(10281, 4320000)
        assert result is not None
        assert result.hour == 12
        assert result.minute == 0

    def test_invalid_tjd(self):
        """Retorna None para TJD inválido."""
        assert tjd_sod_to_datetime(0, 0) is None
        assert tjd_sod_to_datetime(-1, 0) is None

    def test_invalid_sod(self):
        """Retorna None para SOD negativo."""
        assert tjd_sod_to_datetime(10281, -1) is None


class TestCentiToDeg:
    """Testes para conversão de centi-graus para graus."""

    def test_scale_100(self):
        """Testa escala padrão (centi-graus)."""
        # 18000 centi-graus = 180.0 graus
        assert centi_to_deg(18000) == 180.0
        assert centi_to_deg(9000) == 90.0
        assert centi_to_deg(0) == 0.0

    def test_scale_10000(self):
        """Testa escala 10000 (0.0001 graus)."""
        # 1800000 = 180.0 graus
        assert centi_to_deg(1800000, scale=10000) == 180.0
        assert centi_to_deg(900000, scale=10000) == 90.0

    def test_negative_values(self):
        """Testa valores negativos (Dec)."""
        assert centi_to_deg(-4500) == -45.0
        assert centi_to_deg(-9000) == -90.0


class TestGetPacketTypeName:
    """Testes para mapeamento de tipos de pacote."""

    def test_known_types(self):
        """Testa tipos conhecidos."""
        assert get_packet_type_name(60) == "SWIFT_BAT_GRB_ALERT"
        assert get_packet_type_name(110) == "FERMI_GBM_ALERT"
        assert get_packet_type_name(150) == "LVC_PRELIMINARY"
        assert get_packet_type_name(3) == "IMALIVE"

    def test_unknown_type(self):
        """Retorna nome genérico para tipo desconhecido."""
        assert get_packet_type_name(999) == "UNKNOWN_TYPE_999"
        assert get_packet_type_name(0) == "UNKNOWN_TYPE_0"


class TestParseGcnBinaryPacket:
    """Testes para parsing de pacotes binários GCN."""

    def _create_test_packet(
        self,
        pkt_type: int = 60,
        pkt_sernum: int = 12345,
        trig_num: int = 67890,
        burst_tjd: int = 20000,
        burst_sod: int = 4320000,  # 12:00:00
        burst_ra: int = 18000,  # 180.0 deg
        burst_dec: int = 4500,  # 45.0 deg
        burst_error: int = 100,  # 1.0 deg
        trigger_id: int = 0,
        misc: int = 0,
    ) -> bytes:
        """Cria um pacote de teste de 160 bytes."""
        # Array de 40 inteiros (inicializado com zeros)
        longs = [0] * 40
        
        # Preencher campos conforme especificação
        longs[0] = pkt_type
        longs[1] = pkt_sernum
        longs[2] = 0  # hop_cnt
        longs[3] = 0  # pkt_sod
        longs[4] = trig_num
        longs[5] = burst_tjd
        longs[6] = burst_sod
        longs[7] = burst_ra
        longs[8] = burst_dec
        longs[11] = burst_error
        longs[18] = trigger_id
        longs[19] = misc
        longs[39] = 10  # newline terminator
        
        # Pack como big-endian
        return struct.pack('>40i', *longs)

    def test_valid_packet(self):
        """Testa parsing de pacote válido."""
        packet = self._create_test_packet()
        result = parse_gcn_binary_packet(packet)
        
        assert result["parse_error"] is None
        assert result["pkt_type"] == 60
        assert result["pkt_type_name"] == "SWIFT_BAT_GRB_ALERT"
        assert result["pkt_sernum"] == 12345
        assert result["trig_num"] == 67890
        assert result["burst_tjd"] == 20000
        assert result["burst_ra_deg"] == 180.0
        assert result["burst_dec_deg"] == 45.0
        assert result["burst_error_deg"] == 1.0

    def test_burst_datetime(self):
        """Testa conversão de datetime."""
        packet = self._create_test_packet(
            burst_tjd=10281,  # 17 Jul 1996
            burst_sod=4320000,  # 12:00:00
        )
        result = parse_gcn_binary_packet(packet)
        
        assert result["burst_datetime"] is not None
        dt = datetime.fromisoformat(result["burst_datetime"])
        assert dt.year == 1996
        assert dt.month == 7
        assert dt.day == 17
        assert dt.hour == 12

    def test_invalid_size(self):
        """Retorna erro para pacote de tamanho errado."""
        result = parse_gcn_binary_packet(b"too short")
        assert result["parse_error"] is not None
        assert "Invalid packet size" in result["parse_error"]

    def test_none_input(self):
        """Retorna erro para input None."""
        result = parse_gcn_binary_packet(None)
        assert result["parse_error"] is not None
        assert "None" in result["parse_error"]

    def test_negative_dec(self):
        """Testa Dec negativo (hemisfério sul)."""
        packet = self._create_test_packet(burst_dec=-4500)  # -45.0 deg
        result = parse_gcn_binary_packet(packet)
        
        assert result["burst_dec_deg"] == -45.0

    def test_scale_detection_10000(self):
        """Testa detecção de escala 10000 para coordenadas de alta precisão."""
        # Ra = 1800000 (180.0 deg em escala 10000)
        # Dec = 450000 (45.0 deg em escala 10000)
        packet = self._create_test_packet(
            burst_ra=1800000,
            burst_dec=450000,
            burst_error=10000,  # 1.0 deg
        )
        result = parse_gcn_binary_packet(packet)
        
        # Deve detectar escala 10000 automaticamente
        assert result["burst_ra_deg"] == 180.0
        assert result["burst_dec_deg"] == 45.0
        assert result["burst_error_deg"] == 1.0

    def test_fermi_packet_type(self):
        """Testa pacote FERMI_GBM_ALERT."""
        packet = self._create_test_packet(pkt_type=110)
        result = parse_gcn_binary_packet(packet)
        
        assert result["pkt_type"] == 110
        assert result["pkt_type_name"] == "FERMI_GBM_ALERT"

    def test_lvc_packet_type(self):
        """Testa pacote LVC (Gravitational Wave)."""
        packet = self._create_test_packet(pkt_type=150)
        result = parse_gcn_binary_packet(packet)
        
        assert result["pkt_type"] == 150
        assert result["pkt_type_name"] == "LVC_PRELIMINARY"
