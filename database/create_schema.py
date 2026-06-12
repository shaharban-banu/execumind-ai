import sqlite3
from pathlib import Path

DB_PATH="../data/sqlite/execumind.db"
SCHEMA_PATH="database/schema.sql"

Path("../data/sqlite").mkdir(parents=True,exist_ok=True)

conn=sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH,"r")as f:
    schema=f.read()

conn.executescript(schema)
conn.commit()
conn.close()
print("ExecuMind database created successfully")