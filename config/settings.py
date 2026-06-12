from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SQLITE_DIR = DATA_DIR / "sqlite"

SQLITE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{SQLITE_DIR}/execumind.db"