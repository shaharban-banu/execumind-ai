"""
Application configuration.

Loads:
- Project paths
- Database settings
- Dataset configuration
- Canonical schema
- Column mappings
- Capability definitions
"""
from pathlib import Path


#project paths
#----------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SQLITE_DIR = DATA_DIR / "sqlite"

SQLITE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{SQLITE_DIR}/execumind.db"

# --------------------------------------------------
# Table name mapping: historical → live mirror
# --------------------------------------------------
LIVE_TABLE_MAPPING = {
    "orders": "live_orders",
    "order_items": "live_order_items",
    "reviews": "live_reviews",
    "payments": "live_payments",
}
# SQL commands that are never permitted
BLOCKED_SQL_COMMANDS = [
    "drop",
    "delete",
    "truncate",
    "alter",
    "insert",
    "update",
]