"""Make the tests directory importable as a plain directory.

Two test modules import a SIBLING module (`import test_native_admission as fixture`). That worked only
when whatever launched pytest had already put `tests/` on sys.path; under a bare `python -m pytest tests`
it fails at collection with ModuleNotFoundError, so those two modules never ran. Inserting the directory
here (conftest is imported before any test module) fixes collection without touching either test's
semantics -- the fixtures and assertions are unchanged.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
