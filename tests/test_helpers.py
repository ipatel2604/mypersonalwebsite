"""Pure-logic helpers: price parsing, slugify, etc."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import app  # noqa: E402


def test_parse_price_rupee_symbol():
    assert app.parse_price("₹60") == 60.0


def test_parse_price_with_comma():
    assert app.parse_price("₹1,200") == 1200.0


def test_parse_price_non_numeric_returns_none():
    assert app.parse_price("Contact for price") is None
    assert app.parse_price("Contact for bulk price") is None


def test_slugify():
    assert app.slugify("Regular Plus") == "regular-plus"
    assert app.slugify("A/B") == "a-b"
