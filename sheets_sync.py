"""Optional live Google Sheets sync for orders.

Falls back to doing nothing whenever Google credentials aren't configured,
so the site works with or without this wired up - same pattern as
payments.py and notifications.py.

Setup required (one-time, in Google Cloud Console):
1. Create a project, enable the "Google Sheets API".
2. Create a Service Account, generate a JSON key for it.
3. Create a Google Sheet, share it (Editor access) with the service
   account's email address (looks like xxx@xxx.iam.gserviceaccount.com -
   found inside the JSON key file).
4. Set GOOGLE_SHEET_ID (from the sheet's URL) and either
   GOOGLE_SERVICE_ACCOUNT_FILE (path to the downloaded JSON key) or
   GOOGLE_SERVICE_ACCOUNT_JSON (the JSON key's contents, useful for cloud
   secrets where uploading a file isn't convenient).
"""
import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
GOOGLE_SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "")
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
_HEADER_ROW = [
    "Order ID", "Date/Time", "Customer Name", "Phone", "Items",
    "Total (Rs)", "Notes", "Order Status",
]


def is_configured() -> bool:
    return bool(GOOGLE_SHEET_ID and (GOOGLE_SERVICE_ACCOUNT_FILE or GOOGLE_SERVICE_ACCOUNT_JSON))


def _get_worksheet():
    import gspread
    from google.oauth2.service_account import Credentials

    if GOOGLE_SERVICE_ACCOUNT_JSON:
        info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
        creds = Credentials.from_service_account_info(info, scopes=_SCOPES)
    else:
        creds = Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE, scopes=_SCOPES)

    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sheet.sheet1
    if worksheet.row_count == 0 or not worksheet.row_values(1):
        worksheet.append_row(_HEADER_ROW)
    return worksheet


def append_order(
    order_id: int,
    customer_name: str,
    customer_phone: str,
    items: list[dict],
    total_amount: float,
    notes: str,
    order_status: str = "new",
) -> bool:
    """Append a row for this order to the configured Google Sheet.

    Returns True if synced, False if skipped (not configured) or failed.
    A failure here must never block checkout - the order is already saved
    in the database by the time this is called.
    """
    if not is_configured():
        return False

    items_summary = "; ".join(
        f"{item['product']} ({item['size']}) x{item['quantity']} @ {item['price']}"
        for item in items
    )
    row = [
        order_id,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        customer_name,
        customer_phone,
        items_summary,
        f"{total_amount:,.0f}",
        notes,
        order_status,
    ]

    try:
        worksheet = _get_worksheet()
        worksheet.append_row(row)
        return True
    except Exception:
        logger.exception("Failed to sync order #%s to Google Sheet", order_id)
        return False
