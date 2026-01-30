import logging
from nasa_gcn import main
from nasa_gcn.utils import get_logger


def test_format_number():
    assert main.format_number(1000) == "1,000"
    assert main.format_number(1000000) == "1,000,000"
    assert main.format_number("Error") == "Error"


def test_get_logger():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) >= 1