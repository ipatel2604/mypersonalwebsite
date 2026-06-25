"""Optional order-confirmation email via SMTP.

Falls back to doing nothing whenever SMTP_HOST/SMTP_USER/SMTP_PASSWORD are
not configured, so the site works with or without email notifications wired
up - same pattern as payments.py for Razorpay.
"""
import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587") or "587")
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USER)


def is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD)


def send_order_confirmation(
    customer_email: str,
    company_name: str,
    order_id: int,
    items: list[dict],
    total_amount: float,
) -> bool:
    """Send a confirmation email. Returns True if sent, False if skipped/failed."""
    if not is_configured() or not customer_email:
        return False

    lines = [f"Thank you for your order with {company_name}!", ""]
    lines.append(f"Order reference: #{order_id}")
    lines.append("")
    lines.append("Items:")
    for item in items:
        lines.append(f"- {item['product']} ({item['size']}) x{item['quantity']} @ {item['price']}")
    lines.append("")
    lines.append(f"Order total: Rs. {total_amount:,.0f}")
    lines.append("")
    lines.append("We will contact you by phone to confirm availability, pricing, and delivery or pickup details.")

    message = EmailMessage()
    message["Subject"] = f"{company_name} - Order #{order_id} received"
    message["From"] = FROM_EMAIL
    message["To"] = customer_email
    message.set_content("\n".join(lines))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        return True
    except Exception:
        # A failed confirmation email should never break checkout for the
        # customer - the order is already saved by this point.
        logger.exception("Failed to send order confirmation email for order #%s", order_id)
        return False
