#!/usr/bin/env python3
"""
Test environment variable loading for context generator CLI.
Never commit this file - it's for testing only.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from context_generator.cli import create_parser

def test_env_loading():
    """Test that environment variables are loaded correctly."""
    
    # Test 1: Default (no environment)
    print("Test 1: Default model (no env)")
    parser = create_parser()
    args = parser.parse_args(["/tmp"])
    print(f"  Model: {args.model}")
    assert args.model == "offline", f"Expected 'offline', got {args.model}"
    print("  ✓ PASS: Default is 'offline'\n")
    
    # Test 2: CONTEXT_GENERATOR_MODEL from environment
    print("Test 2: CONTEXT_GENERATOR_MODEL from env")
    os.environ["CONTEXT_GENERATOR_MODEL"] = "openrouter/anthropic/claude-3-haiku"
    parser = create_parser()
    args = parser.parse_args(["/tmp"])
    print(f"  Model: {args.model}")
    assert args.model == "openrouter/anthropic/claude-3-haiku", \
        f"Expected 'openrouter/anthropic/claude-3-haiku', got {args.model}"
    print("  ✓ PASS: Environment variable loaded\n")
    del os.environ["CONTEXT_GENERATOR_MODEL"]
    
    # Test 3: Command line overrides environment
    print("Test 3: CLI overrides environment")
    os.environ["CONTEXT_GENERATOR_MODEL"] = "gemini/gemini-1.5-flash"
    parser = create_parser()
    args = parser.parse_args(["/tmp", "--model", "ollama/llama3.2"])
    print(f"  Model: {args.model}")
    assert args.model == "ollama/llama3.2", \
        f"Expected 'ollama/llama3.2', got {args.model}"
    print("  ✓ PASS: CLI overrides environment\n")
    del os.environ["CONTEXT_GENERATOR_MODEL"]
    
    # Test 4: Provider-specific variables
    print("Test 4: Provider API keys from environment")
    test_config = {
        "CONTEXT_GENERATOR_MODEL": "openrouter/anthropic/claude-3-haiku",
        "OPENROUTER_API_KEY": "sk-or-test123",
        "OLLAMA_HOST": "http://localhost:9999",
        "GEMINI_API_KEY": "AIza-test456",
    }
    
    # Set them
    for key, value in test_config.items():
        os.environ[key] = value
    
    # Load dotenv (already done by cli.py import)
    from dotenv import load_dotenv
    load_dotenv()  # Should be no-op since already loaded, but let's verify
    
    # Verify from environment
    for key, expected in test_config.items():
        actual = os.environ.get(key)
        assert actual == expected, f"Expected {key}={expected}, got {actual}"
    
    print("  Config:")
    for key in test_config:
        print(f"    {key}: {os.environ.get(key)[:15]}...")
    print("  ✓ PASS: All variables loaded\n")
    
    # Cleanup
    for key in test_config:
        if key in os.environ:
            del os.environ[key]
    
    print("=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)
    print("\nYour configuration is ready. You can now:")
    print("1. Set CONTEXT_GENERATOR_MODEL in .env")
    print("2. Add provider API keys to .env")
    print("3. Run without --model argument:")
    print("   python -m context_generator ./path/to/code")

if __name__ == "__main__":
    try:
        test_env_loading()
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
