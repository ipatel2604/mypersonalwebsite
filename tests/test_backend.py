"""backend.py order persistence."""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _fresh_backend(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    import backend
    importlib.reload(backend)
    backend.DB_PATH = tmp_path / "test_orders.db"
    backend.engine = backend.create_engine(f"sqlite:///{backend.DB_PATH}")
    return backend


def test_save_and_get_order(tmp_path, monkeypatch):
    backend = _fresh_backend(tmp_path, monkeypatch)
    order_id = backend.save_order(
        customer_name="Test User",
        customer_phone="9876543210",
        notes="leave at gate",
        items=[{"product": "Regular", "size": "250 g", "price": "₹60", "quantity": 2}],
        total_amount=120.0,
    )
    assert isinstance(order_id, int)

    orders = backend.get_all_orders()
    assert len(orders) == 1
    assert orders[0]["customer_name"] == "Test User"
    assert orders[0]["total_amount"] == 120.0
    assert orders[0]["order_status"] == "new"
    assert orders[0]["items"][0]["product"] == "Regular"


def test_update_order_status(tmp_path, monkeypatch):
    backend = _fresh_backend(tmp_path, monkeypatch)
    order_id = backend.save_order(
        customer_name="Test User",
        customer_phone="9876543210",
        notes="",
        items=[{"product": "Regular", "size": "250 g", "price": "₹60", "quantity": 1}],
        total_amount=60.0,
    )
    backend.update_order_status(order_id, "confirmed")
    orders = backend.get_all_orders()
    assert orders[0]["order_status"] == "confirmed"


def test_using_hosted_database_defaults_false(tmp_path, monkeypatch):
    backend = _fresh_backend(tmp_path, monkeypatch)
    assert backend.using_hosted_database() is False
