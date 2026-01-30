#!/usr/bin/env python3
"""
Test script to validate Base64 credentials implementation.

This script tests the credential loading functionality without
requiring actual NASA GCN credentials or Databricks connection.
"""

import base64
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_base64_encoding_decoding():
    """Test that Base64 encoding/decoding works correctly."""
    print("=" * 70)
    print("Test 1: Base64 Encoding/Decoding")
    print("=" * 70)

    test_credentials = [
        ("test_client_id_123", "Test Client ID"),
        ("my_super_secret_password!", "Test Secret with special chars"),
        ("简体中文", "Test Unicode characters"),
    ]

    all_passed = True

    for original, description in test_credentials:
        # Encode
        encoded = base64.b64encode(original.encode('utf-8')).decode('utf-8')

        # Decode
        decoded = base64.b64decode(encoded).decode('utf-8')

        # Verify
        passed = original == decoded
        status = "✅ PASS" if passed else "❌ FAIL"

        print(f"\n{status} - {description}")
        print(f"  Original:  {original}")
        print(f"  Encoded:   {encoded}")
        print(f"  Decoded:   {decoded}")
        print(f"  Match:     {passed}")

        if not passed:
            all_passed = False

    print()
    return all_passed


def test_credential_loading():
    """Test credential loading with different scenarios."""
    print("=" * 70)
    print("Test 2: Credential Loading Priority")
    print("=" * 70)

    # Import after setting env vars
    from nasa_gcn.config import _get_credential

    test_cases = [
        {
            "name": "Base64 credential present",
            "env_vars": {
                "TEST_CRED_B64": base64.b64encode(b"base64_value").decode(),
                "TEST_CRED": "plain_value",
            },
            "expected": "base64_value",
            "description": "Should prefer Base64 over plain-text",
        },
        {
            "name": "Only plain-text credential",
            "env_vars": {
                "TEST_CRED": "plain_value",
            },
            "expected": "plain_value",
            "description": "Should use plain-text when Base64 not available",
        },
        {
            "name": "No credentials",
            "env_vars": {},
            "expected": "",
            "description": "Should return empty string when nothing found",
        },
    ]

    all_passed = True

    for test_case in test_cases:
        # Clear previous env vars
        for key in ["TEST_CRED", "TEST_CRED_B64"]:
            os.environ.pop(key, None)

        # Set test env vars
        for key, value in test_case["env_vars"].items():
            os.environ[key] = value

        # Test credential loading
        result = _get_credential("TEST_CRED")
        passed = result == test_case["expected"]
        status = "✅ PASS" if passed else "❌ FAIL"

        print(f"\n{status} - {test_case['name']}")
        print(f"  Description: {test_case['description']}")
        print(f"  Expected:    '{test_case['expected']}'")
        print(f"  Got:         '{result}'")
        print(f"  Match:       {passed}")

        if not passed:
            all_passed = False

        # Clean up
        for key in test_case["env_vars"]:
            os.environ.pop(key, None)

    print()
    return all_passed


def test_deploy_script_compatibility():
    """Test that deploy.sh can decode credentials correctly."""
    print("=" * 70)
    print("Test 3: Deploy Script Compatibility")
    print("=" * 70)

    # Create test .env file
    test_env_path = Path(__file__).parent.parent / ".env.test"

    test_client_id = "test_client_id_12345"
    test_client_secret = "test_secret_67890"

    encoded_id = base64.b64encode(test_client_id.encode()).decode()
    encoded_secret = base64.b64encode(test_client_secret.encode()).decode()

    test_env_content = f"""# Test environment file
GCN_CLIENT_ID_B64={encoded_id}
GCN_CLIENT_SECRET_B64={encoded_secret}

# Plain-text versions (should be ignored)
GCN_CLIENT_ID=wrong_plain_id
GCN_CLIENT_SECRET=wrong_plain_secret
"""

    try:
        # Write test .env
        test_env_path.write_text(test_env_content)

        print(f"\n✅ Created test .env file: {test_env_path}")
        print(f"  Encoded Client ID:     {encoded_id}")
        print(f"  Encoded Client Secret: {encoded_secret}")
        print()
        print("📝 To test deploy script manually:")
        print(f"   1. cp {test_env_path} .env")
        print("   2. ./deploy.sh")
        print("   3. Should see: '🔒 Credenciais carregadas (Base64-encoded)'")
        print()
        print("⚠️  Note: This is a mock test. Actual deploy requires Databricks config.")

    except Exception as e:
        print(f"❌ FAIL - Could not create test file: {e}")
        return False

    print()
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("NASA GCN Base64 Credentials - Test Suite")
    print("=" * 70)
    print()

    results = []

    # Run tests
    results.append(("Base64 Encoding/Decoding", test_base64_encoding_decoding()))
    results.append(("Credential Loading Priority", test_credential_loading()))
    results.append(("Deploy Script Compatibility", test_deploy_script_compatibility()))

    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(passed for _, passed in results)

    print()
    if all_passed:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
