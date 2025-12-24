"""
CLI interface for the context generator.

Usage:
    python -m context_generator <path> [options]
    context-generator <path> [options]
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env file if it exists
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

try:
    from .generator import ClaudeMdGenerator
    from .executions.llm_client import LLMClient
except ImportError:
    # Fallback for running as __main__
    from context_generator.generator import ClaudeMdGenerator
    from context_generator.executions.llm_client import LLMClient


def setup_logging(verbose: bool = False):
    """Configure logging for CLI output."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="context-generator",
        description="Generate CLAUDE.md files for progressive context loading in AI/LLM workflows.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate CLAUDE.md files using static analysis only (offline mode)
  context-generator ./src --offline

  # Generate with LLM enhancement via OpenRouter
  context-generator ./src --model openrouter/anthropic/claude-3-haiku

  # Generate with local Ollama model
  context-generator ./src --model ollama/llama3

  # Preview without writing files
  context-generator ./src --dry-run --offline

  # Limit to folders with at least 3 files, max depth 5
  context-generator ./src --min-files 3 --depth 5 --offline
"""
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Root path to scan for source files"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=os.environ.get("CONTEXT_GENERATOR_MODEL", "offline"),
        help="LLM model to use. Format: 'provider/model'. Examples: 'openrouter/anthropic/claude-3-haiku', 'ollama/llama3'. Default: offline"
    )
    
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run in offline mode (no LLM calls, static analysis only)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )
    
    parser.add_argument(
        "--depth",
        type=int,
        default=10,
        help="Maximum folder depth to scan (default: 10)"
    )
    
    parser.add_argument(
        "--min-files",
        type=int,
        default=1,
        help="Minimum files in folder to generate CLAUDE.md (default: 1)"
    )
    
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="*",
        default=[],
        help="Additional patterns to exclude (gitignore format)"
    )
    
    parser.add_argument(
        "--layers",
        type=str,
        choices=["1", "2", "3", "4", "all", "none"],
        default="all",
        help="Which layers to generate: 1-4 for individual layers, 'all' for all 4 layers, 'none' to disable. Default: all"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    root_path = args.path.resolve()
    if not root_path.exists():
        logger.error(f"Path does not exist: {root_path}")
        return 1
    
    if not root_path.is_dir():
        logger.error(f"Path is not a directory: {root_path}")
        return 1
    
    offline = args.offline or args.model.lower() == "offline"
    
    llm_client = None
    if not offline:
        try:
            llm_client = LLMClient.from_model_string(args.model)
            if not llm_client.is_available():
                logger.warning(f"LLM model {args.model} not available, falling back to offline mode")
                offline = True
                llm_client = None
        except ValueError as e:
            logger.error(f"Invalid model string: {e}")
            return 1
    
    logger.info(f"Context Generator v0.1.0")
    logger.info(f"Root path: {root_path}")
    logger.info(f"Mode: {'offline (static analysis)' if offline else f'LLM-enhanced ({args.model})'}")
    logger.info(f"Layers: {args.layers}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("")
    
    try:
        generator = ClaudeMdGenerator(
            root_path=root_path,
            llm_client=llm_client,
            offline=offline
        )
        
        # Configure layer generation
        if args.layers == "none":
            generator.enable_layers = False
        else:
            generator.enable_layers = True
        
        results = generator.generate_all(
            min_files=args.min_files,
            max_depth=args.depth,
            dry_run=args.dry_run
        )
        
        logger.info("")
        logger.info(f"Processed {len(results)} folders")
        
        if args.dry_run:
            logger.info("(dry-run mode - no files were written)")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
