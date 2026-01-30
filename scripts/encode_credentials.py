#!/usr/bin/env python3
"""
Helper script to encode NASA GCN credentials to Base64.

This script helps you securely encode your credentials for use with
the Databricks Community Edition, which does not support Databricks Secrets.

Usage:
    python scripts/encode_credentials.py

The script will:
1. Prompt you to enter your credentials (input is hidden)
2. Encode them to Base64
3. Display the encoded values to paste in your .env file

Security Note:
    Base64 encoding is obfuscation, NOT encryption. It provides basic
    protection against accidental exposure in logs and screenshots, but
    should not be considered secure for production environments.

    For production, use:
    - Databricks Secrets (requires paid workspace)
    - AWS Secrets Manager / Azure Key Vault
    - HashiCorp Vault
"""

import base64
import getpass
import sys
from pathlib import Path


def encode_to_base64(text: str) -> str:
    """Encode a string to Base64."""
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def decode_from_base64(encoded_text: str) -> str:
    """Decode a Base64 string (for verification)."""
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"[DECODE ERROR: {e}]"


def main():
    """Main function to encode credentials."""
    print("=" * 70)
    print("NASA GCN Credentials Base64 Encoder")
    print("=" * 70)
    print()
    print("This script will encode your NASA GCN credentials to Base64.")
    print("Your input will be hidden for security.")
    print()
    print("⚠️  SECURITY NOTICE:")
    print("   Base64 is obfuscation, NOT encryption!")
    print("   Only use this for Databricks Community Edition.")
    print("   For production, use proper secret management (Databricks Secrets).")
    print()
    print("-" * 70)
    print()

    try:
        # Get credentials from user (hidden input)
        client_id = getpass.getpass("Enter your GCN_CLIENT_ID: ")
        if not client_id:
            print("❌ Error: Client ID cannot be empty")
            sys.exit(1)

        client_secret = getpass.getpass("Enter your GCN_CLIENT_SECRET: ")
        if not client_secret:
            print("❌ Error: Client Secret cannot be empty")
            sys.exit(1)

        print()
        print("-" * 70)
        print()

        # Encode to Base64
        encoded_id = encode_to_base64(client_id)
        encoded_secret = encode_to_base64(client_secret)

        # Display results
        print("✅ Credentials encoded successfully!")
        print()
        print("=" * 70)
        print("COPY THE FOLLOWING TO YOUR .env FILE:")
        print("=" * 70)
        print()
        print(f"GCN_CLIENT_ID_B64={encoded_id}")
        print(f"GCN_CLIENT_SECRET_B64={encoded_secret}")
        print()
        print("=" * 70)
        print()

        # Verification
        print("🔍 Verification (decoded values - check they match your input):")
        print(f"   Client ID: {decode_from_base64(encoded_id)[:10]}...{decode_from_base64(encoded_id)[-4:]}")
        print(f"   Client Secret: {decode_from_base64(encoded_secret)[:10]}...{decode_from_base64(encoded_secret)[-4:]}")
        print()

        # Instructions
        print("📝 Next steps:")
        print("   1. Copy the encoded values above")
        print("   2. Create/edit your .env file:")
        print(f"      cp .env.example .env")
        print("   3. Paste the encoded values in .env")
        print("   4. Remove or comment out plain-text credentials")
        print()
        print("🔒 Remember:")
        print("   - NEVER commit .env file to git (it's in .gitignore)")
        print("   - Base64 is NOT secure encryption")
        print("   - For production, use Databricks Secrets (paid workspace)")
        print()

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
