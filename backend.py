"""Order storage for the Assam Tea Company site.

Defaults to a local SQLite file (data/orders.db) - zero config, fine for
self-hosting on a VM with persistent disk. If the DATABASE_URL environment
variable is set (e.g. a hosted Postgres on Supabase/Railway/Neon), orders are
stored there instead, which is required if deploying to Streamlit Community
Cloud, where the local filesystem isn't guaranteed to persist across
redeploys.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "orders.db"
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")

_IS_SQLITE = engine.url.get_backend_name() == "sqlite"


def using_hosted_database() -> bool:
    return not _IS_SQLITE


def init_db() -> None:
    id_column = (
        "id INTEGER PRIMARY KEY AUTOINCREMENT"
        if _IS_SQLITE
        else "id SERIAL PRIMARY KEY"
    )
    with engine.begin() as connection:
        connection.execute(text(
            f"""
            CREATE TABLE IF NOT EXISTS orders (
                {id_column},
                created_at TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                notes TEXT,
                items_json TEXT NOT NULL,
                total_amount REAL NOT NULL,
                payment_status TEXT NOT NULL DEFAULT 'pending_manual',
                order_status TEXT NOT NULL DEFAULT 'new'
            )
            """
        ))


def save_order(customer_name: str, customer_phone: str, notes: str, items: list[dict], total_amount: float) -> int:
    init_db()
    insert_sql = """
        INSERT INTO orders (created_at, customer_name, customer_phone, notes, items_json, total_amount)
        VALUES (:created_at, :customer_name, :customer_phone, :notes, :items_json, :total_amount)
    """
    if not _IS_SQLITE:
        insert_sql += " RETURNING id"
    params = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "notes": notes,
        "items_json": json.dumps(items),
        "total_amount": total_amount,
    }
    with engine.begin() as connection:
        result = connection.execute(text(insert_sql), params)
        if _IS_SQLITE:
            return result.lastrowid
        return result.scalar_one()


def get_all_orders() -> list[dict]:
    init_db()
    with engine.connect() as connection:
        rows = connection.execute(
            text("SELECT * FROM orders ORDER BY id DESC")
        ).mappings().all()
    orders = []
    for row in rows:
        order = dict(row)
        order["items"] = json.loads(order["items_json"])
        orders.append(order)
    return orders


def update_order_status(order_id: int, order_status: str) -> None:
    init_db()
    with engine.begin() as connection:
        connection.execute(
            text("UPDATE orders SET order_status = :order_status WHERE id = :order_id"),
            {"order_status": order_status, "order_id": order_id},
        )
