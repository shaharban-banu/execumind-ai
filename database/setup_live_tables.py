"""
Live Tables Setup Script.
 
Creates the four live mirror tables and the simulator
event log in the existing SQLite database.
"""

from datetime import  datetime
from sqlalchemy import inspect,text
from database.database import engine
from database.live_models import (LiveBase,LiveOrder,LiveOrderItem,LivePayment,LiveReview,SimulatorEvent,)
from utils.logger import logger

LIVE_TABLES=[LiveOrder,LiveOrderItem,LiveReview,LivePayment,SimulatorEvent]
TABLE_NAMES=[model.__tablename__ for model in LIVE_TABLES]

def tables_exist() -> dict[str, bool]:
    """
    Check which live tables already exist in the database.
    """
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
 
    return {
        name: name in existing
        for name in TABLE_NAMES
    }
def create_live_tables():
    """
    Create all live mirror tables and simulator_events.
 
    Uses checkfirst=True so existing tables are never
    dropped or modified. Historical data is safe.
    """
    logger.info("Creating live mirror tables")
 
    LiveBase.metadata.create_all(
        bind=engine,
        checkfirst=True          # skip tables that already exist
    )
 
    logger.info("Live tables created successfully")

def verify_live_tables() -> None:
    """
    Verify all expected live tables exist and are empty.
 
    Logs table name and row count for each.
    Raises RuntimeError if any table is missing.
    """
    logger.info("Verifying live tables")
 
    status = tables_exist()
    missing = [name for name, exists in status.items() if not exists]
 
    if missing:
        raise RuntimeError(
            f"Missing live tables after creation: {missing}"
        )
 
    with engine.connect() as conn:
        for name in TABLE_NAMES:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {name}")
            )
            count = result.scalar()
            logger.info("  %-30s  %s rows", name, count)
 
    logger.info("All live tables verified")
 
 
def reset_live_tables() -> None:
    """
    Clear all live mirror tables and reset simulator state.
 
    USE THIS to restart a simulation demo from scratch.
    Deletes all rows from live_orders, live_order_items,
    live_order_reviews, live_order_payments, and
    simulator_events.
 
    Historical tables (orders, reviews, etc.) are
    NEVER touched by this function.
    """
    logger.info("Resetting live tables for fresh simulation")
 
    mirror_tables = [
        "live_order_items",       # clear items before orders (safe for SQLite)
        "live_order_reviews",
        "live_order_payments",
        "live_orders",
        "simulator_events",
    ]
 
    with engine.begin() as conn:
        for table in mirror_tables:
            conn.execute(text(f"DELETE FROM {table}"))
            logger.info("  Cleared: %s", table)
 
        # Log the reset event
        conn.execute(
            text("""
                INSERT INTO simulator_events
                    (event_type, timestamp, orders_inserted,
                     current_speed, anomaly_injected, notes)
                VALUES
                    (:event_type, :timestamp, :orders_inserted,
                     :current_speed, :anomaly_injected, :notes)
            """),
            {
                "event_type": "reset",
                "timestamp": datetime.utcnow().isoformat(),
                "orders_inserted": 0,
                "current_speed": "normal",
                "anomaly_injected": 0,
                "notes": "Simulation reset — all live tables cleared",
            }
        )
 
    logger.info("Live tables reset completed")
 
 
def get_simulation_status() -> dict:
    """
    Return current simulation status.
 
    Used by FastAPI GET /simulator/status endpoint
    to report live state to the React frontend.
 
    Returns:
        dict with keys:
            orders_inserted   int
            latest_event      str
            current_speed     str
            anomaly_injected  bool
            last_updated      str
    """
    with engine.connect() as conn:
 
        # Total rows currently in live_orders
        orders_count = conn.execute(
            text("SELECT COUNT(*) FROM live_orders")
        ).scalar()
 
        # Latest simulator event
        row = conn.execute(
            text("""
                SELECT event_type, timestamp,
                       current_speed, anomaly_injected, notes
                FROM simulator_events
                ORDER BY id DESC
                LIMIT 1
            """)
        ).fetchone()
 
    if row is None:
        return {
            "orders_inserted": 0,
            "latest_event": "not_started",
            "current_speed": "normal",
            "anomaly_injected": False,
            "last_updated": None,
            "notes": "",
        }
 
    return {
        "orders_inserted": orders_count,
        "latest_event": row.event_type,
        "current_speed": row.current_speed,
        "anomaly_injected": bool(row.anomaly_injected),
        "last_updated": row.timestamp,
        "notes": row.notes,
    }
 
 
# --------------------------------------------------
# Entry point
# --------------------------------------------------
 
def main() -> None:
    """
    Run the full live table setup.
 
    Steps:
        1. Check which tables already exist
        2. Create any missing tables
        3. Verify all tables are present
        4. Print status summary
    """
    logger.info("=" * 60)
    logger.info("ExecuMind AI — Live Tables Setup")
    logger.info("=" * 60)
 
    # Step 1 — check current state
    status = tables_exist()
    already_exist = [name for name, exists in status.items() if exists]
    to_create = [name for name, exists in status.items() if not exists]
 
    if already_exist:
        logger.info(
            "Already exist (will skip): %s",
            already_exist
        )
 
    if to_create:
        logger.info(
            "Will create: %s",
            to_create
        )
    else:
        logger.info(
            "All live tables already exist — nothing to create"
        )
 
    # Step 2 — create tables
    create_live_tables()
 
    # Step 3 — verify
    verify_live_tables()
 
    # Step 4 — summary
    logger.info("=" * 60)
    logger.info("Setup complete. Live tables ready for simulator.")
    logger.info(
        "Run reset_live_tables() before each demo to start fresh."
    )
    logger.info("=" * 60)
 
 
if __name__ == "__main__":
    main()