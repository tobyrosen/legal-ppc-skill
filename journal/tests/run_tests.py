#!/usr/bin/env python3
"""Stdlib fallback when pytest is unavailable."""

import sys
import unittest
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root.parent))
    suite = unittest.defaultTestLoader.discover(str(root), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
