"""
NASA GCN Kafka Configuration

Credentials are loaded from:
1. Spark configuration (for Databricks pipelines via bundle variables)
2. Environment variables (from .env file for local development)

Security Note:
- Credentials can be stored as Base64-encoded values (obfuscation, not encryption)
- Use variables with _B64 suffix (e.g., GCN_CLIENT_ID_B64)
- This provides basic protection against accidental exposure in logs
- For production environments, use Databricks Secrets (requires paid workspace)
"""

import base64
import os
from pathlib import Path

# Import logger with fallback for different environments
try:
    from utils import get_logger
except ImportError:
    from nasa_gcn.utils import get_logger

# Initialize logger
logger = get_logger(__name__)

# Try to load .env file if it exists (for local development)
try:
    from dotenv import load_dotenv

    # Look for .env in the project root
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # dotenv not available (e.g., in Databricks), use environment variables directly
    pass


def _decode_base64_credential(encoded_value: str) -> str:
    """
    Decode a Base64-encoded credential.

    Args:
        encoded_value: Base64-encoded string

    Returns:
        Decoded credential string, or empty string if decoding fails
    """
    try:
        decoded_bytes = base64.b64decode(encoded_value)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        logger.warning(f"Failed to decode Base64 credential: {e}")
        return ""


def _get_credential(name: str) -> str:
    """
    Get credential from Spark config or environment variable.

    Supports both plain-text and Base64-encoded credentials:
    - First tries to load from {name}_B64 and decode
    - Falls back to plain-text {name} variable
    - Searches in Spark config first, then environment variables

    Args:
        name: Credential name (e.g., 'GCN_CLIENT_ID')

    Returns:
        Credential value or empty string if not found
    """
    # Try Base64-encoded version first (more secure)
    encoded_name = f"{name}_B64"

    # Try Spark configuration first (for Databricks pipelines)
    try:
        from pyspark.sql import SparkSession

        spark = SparkSession.getActiveSession()
        if spark:
            # Try Base64 version
            encoded_value = spark.conf.get(encoded_name, "")
            if encoded_value:
                decoded = _decode_base64_credential(encoded_value)
                if decoded:
                    logger.info(f"Loaded {name} from Spark config (Base64-encoded)")
                    return decoded

            # Fall back to plain-text version
            value = spark.conf.get(name, "")
            if value:
                logger.warning(
                    f"Loaded {name} from Spark config in plain-text. "
                    f"Consider using {encoded_name} for better security."
                )
                return value
    except Exception:
        pass

    # Fall back to environment variables
    # Try Base64 version
    encoded_value = os.getenv(encoded_name, "")
    if encoded_value:
        decoded = _decode_base64_credential(encoded_value)
        if decoded:
            logger.info(f"Loaded {name} from environment (Base64-encoded)")
            return decoded

    # Fall back to plain-text version
    plain_value = os.getenv(name, "")
    if plain_value:
        logger.warning(
            f"Loaded {name} from environment in plain-text. "
            f"Consider using {encoded_name} for better security."
        )

    return plain_value


# Kafka broker settings
KAFKA_BOOTSTRAP_SERVERS = "kafka.gcn.nasa.gov:9092"
KAFKA_SECURITY_PROTOCOL = "SASL_SSL"
KAFKA_SASL_MECHANISM = "OAUTHBEARER"

# OAuth settings
OAUTH_TOKEN_ENDPOINT = "https://auth.gcn.nasa.gov/oauth2/token"


def _build_jaas_config(client_id: str, client_secret: str) -> str:
    """Build JAAS configuration string for Kafka OAuth."""
    return (
        "kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required "
        f'clientId="{client_id}" '
        f'clientSecret="{client_secret}";'
    )


# Topic subscription patterns (using regex to match multiple topic types)
GCN_TOPIC_PATTERNS = [
    "gcn\\.classic\\.text\\..*",
    "gcn\\.classic\\.voevent\\..*",
    "gcn\\.classic\\.binary\\..*",
    "gcn\\.notices\\..*",
    "gcn\\.circulars",
    "igwn\\.gwalert",
]

# Combined pattern for all topics
GCN_COMBINED_PATTERN = "|".join(GCN_TOPIC_PATTERNS)

# Include heartbeat for testing
GCN_INCLUDE_HEARTBEAT = True


def get_kafka_options() -> dict:
    """Return Kafka connection options for Spark readStream."""
    # Get credentials at runtime (allows Spark config to be available)
    client_id = _get_credential("GCN_CLIENT_ID")
    client_secret = _get_credential("GCN_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.warning(
            "GCN credentials not found. "
            "Set GCN_CLIENT_ID and GCN_CLIENT_SECRET in .env file or pipeline configuration."
        )

    options = {
        "kafka.bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "kafka.security.protocol": KAFKA_SECURITY_PROTOCOL,
        "kafka.sasl.mechanism": KAFKA_SASL_MECHANISM,
        "kafka.sasl.jaas.config": _build_jaas_config(client_id, client_secret),
        "kafka.sasl.login.callback.handler.class": (
            "kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginCallbackHandler"
        ),
        "kafka.sasl.oauthbearer.token.endpoint.url": OAUTH_TOKEN_ENDPOINT,
        "failOnDataLoss": "false",
        "startingOffsets": "earliest",
    }

    # Use subscribePattern for flexible matching
    if GCN_INCLUDE_HEARTBEAT:
        options["subscribePattern"] = f"gcn\\.heartbeat|{GCN_COMBINED_PATTERN}"
    else:
        options["subscribePattern"] = GCN_COMBINED_PATTERN

    return options
