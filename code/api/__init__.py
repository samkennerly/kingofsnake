"""
Application Programming Interface tools.
"""
from pathlib import Path

from .ergast import ErgastAPI

REPO = Path(__file__).resolve().parent.parent.parent
CACHE = REPO / "data/cache"
