#!/usr/bin/env python3
"""
Shared CLI argument parser for automation scripts.

Provides:
- --dry-run / -d
- --verbose / -v
- --quiet / -q
"""

import argparse

def get_standard_parser(description="Automation script with dry-run and verbosity options."):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--dry-run", action="store_true", help="Simulate execution without writing changes.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress non-error output.")
    return parser
