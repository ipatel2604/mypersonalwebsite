"""payments.py, notifications.py, and sheets_sync.py must no-op gracefully
when unconfigured, never raise, and never block checkout."""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def test_payments_not_configured_without_keys(monkeypatch):
    monkeypatch.delenv("RAZORPAY_KEY_ID", raising=False)
    monkeypatch.delenv("RAZORPAY_KEY_SECRET", raising=False)
    import payments
    importlib.reload(payments)
    assert payments.is_configured() is False
    assert payments.create_payment_link(1, 100.0, "Test", "9876543210") is None


def test_notifications_not_configured_without_smtp(monkeypatch):
    monkeypatch.delenv("SMTP_HOST", raising=False)
    monkeypatch.delenv("SMTP_USER", raising=False)
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    import notifications
    importlib.reload(notifications)
    assert notifications.is_configured() is False
    sent = notifications.send_order_confirmation(
        "customer@example.com", "Assam Tea Company", 1,
        [{"product": "Regular", "size": "250 g", "price": "₹60", "quantity": 1}],
        60.0,
    )
    assert sent is False


def test_notifications_skips_when_no_email_even_if_configured(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "secret")
    import notifications
    importlib.reload(notifications)
    sent = notifications.send_order_confirmation(
        "", "Assam Tea Company", 1, [], 0.0
    )
    assert sent is False


def test_sheets_sync_not_configured_without_credentials(monkeypatch):
    monkeypatch.delenv("GOOGLE_SHEET_ID", raising=False)
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_FILE", raising=False)
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raising=False)
    import sheets_sync
    importlib.reload(sheets_sync)
    assert sheets_sync.is_configured() is False
    synced = sheets_sync.append_order(
        1, "Test User", "9876543210",
        [{"product": "Regular", "size": "250 g", "price": "₹60", "quantity": 1}],
        60.0, "",
    )
    assert synced is False
