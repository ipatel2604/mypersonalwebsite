"""Every page must render without raising an exception."""
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

PAGES = [
    "home",
    "products",
    "about",
    "checkout",
    "contact",
    "privacy_policy",
    "terms",
    "refund_policy",
]


@pytest.mark.parametrize("page", PAGES)
def test_page_renders_without_exception(page, tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    at = AppTest.from_file(str(ROOT / "app.py"))
    at.session_state["current_page"] = page
    at.run()
    assert list(at.exception) == []


def test_checkout_shows_correct_total(monkeypatch):
    monkeypatch.chdir(ROOT)
    at = AppTest.from_file(str(ROOT / "app.py"))
    at.session_state["current_page"] = "checkout"
    at.session_state["bag_items"] = [
        {"product": "Regular", "size": "250 g", "price": "₹60", "quantity": 2},
        {"product": "Sugar", "size": "Standard packet", "price": "Contact for price", "quantity": 1},
    ]
    at.run()
    assert list(at.exception) == []
    text = "\n".join(md.value for md in at.markdown)
    assert "Order total: ₹120" in text
    assert "plus items priced on request" in text


def test_footer_is_present_on_every_page(monkeypatch):
    """Regression test for the footer/visibility bug: the custom footer must
    not collide with Streamlit's chrome-hiding CSS selector."""
    monkeypatch.chdir(ROOT)
    at = AppTest.from_file(str(ROOT / "app.py"))
    at.session_state["current_page"] = "home"
    at.run()
    text = "\n".join(md.value for md in at.markdown)
    assert 'class="footer"' in text
    assert "<footer" not in text, "footer must not use a <footer> tag - it collides with the chrome-hiding CSS rule"


def test_add_to_bag_from_product_detail_clears_query_param_path(monkeypatch):
    """Regression test for the checkout-navigation bug: the add-to-bag
    handler must clear st.query_params so the router doesn't bounce back."""
    monkeypatch.chdir(ROOT)
    source = (ROOT / "app.py").read_text()
    assert "st.query_params.clear()" in source
