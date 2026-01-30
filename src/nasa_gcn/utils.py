"""
Utility functions for NASA GCN Pipeline.
"""

import logging
import sys

from pyspark.sql import Column
from pyspark.sql.functions import col, decode, regexp_replace


def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger with a standard format.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def decode_utf8(col_name: str = "value") -> Column:
    """
    Decodes a binary column (default 'value') to UTF-8 string.
    """
    return decode(col(col_name), "UTF-8")


def clean_json_id(id_col: Column) -> Column:
    """
    Removes brackets and quotes from JSON array strings to extract the first element.
    Ex: '["123"]' -> '123'
    """
    # Remove leading [" or [
    step1 = regexp_replace(id_col, r'^[\["]+', "")
    # Remove trailing "] or ]
    return regexp_replace(step1, r'[\]"]+$', "")
