"""Ensure packages import correctly."""

import importlib
import os
import sys
import pytest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

@pytest.mark.parametrize("module", [
    "codes",
    "noise",
    "simulation",
    "decoders",
    "energy",
])
def test_import(module):
    importlib.import_module(module)
