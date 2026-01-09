"""
NASA GCN Kafka Configuration

Credentials are loaded from:
1. Spark configuration (for Databricks pipelines via bundle variables)
2. Environment variables (from .env file for local development)
"""
import os
from pathlib import Path

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


def _get_credential(name: str) -> str:
    """Get credential from Spark config or environment variable."""
    # Try Spark configuration first (for Databricks pipelines)
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()
        if spark:
            value = spark.conf.get(name, "")
            if value:
                return value
    except Exception:
        pass
    
    # Fall back to environment variable
    return os.getenv(name, "")


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
        import warnings
        warnings.warn(
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
        "startingOffsets": "latest",
    }
    
    # Use subscribePattern for flexible matching
    if GCN_INCLUDE_HEARTBEAT:
        options["subscribePattern"] = f"gcn\\.heartbeat|{GCN_COMBINED_PATTERN}"
    else:
        options["subscribePattern"] = GCN_COMBINED_PATTERN
    
    return options
