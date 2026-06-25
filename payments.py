"""Optional Razorpay payment-link integration.

Falls back to a manual "we'll call you" flow whenever RAZORPAY_KEY_ID /
RAZORPAY_KEY_SECRET are not configured, so the site works with or without
a payment gateway connected.
"""
import logging
import os

logger = logging.getLogger(__name__)

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")


def is_configured() -> bool:
    return bool(RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET)


def create_payment_link(order_id: int, amount_rupees: float, customer_name: str, customer_phone: str) -> str | None:
    """Create a Razorpay payment link and return its URL, or None if unavailable."""
    if not is_configured():
        return None

    import razorpay

    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    payment_link = client.payment_link.create({
        "amount": int(round(amount_rupees * 100)),
        "currency": "INR",
        "description": f"Assam Tea Company order #{order_id}",
        "customer": {
            "name": customer_name,
            "contact": customer_phone,
        },
        "notify": {"sms": True, "email": False},
        "reference_id": str(order_id),
    })
    return payment_link.get("short_url")
