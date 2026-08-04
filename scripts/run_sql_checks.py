"""Load checked-in CSV tables to SQLite and execute each statement in analysis/sql_checks.sql."""
from __future__ import annotations
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ["ai_initiative_registry", "control_assessments", "governance_exceptions", "adoption_telemetry", "value_realization"]

def main():
    db = sqlite3.connect(":memory:")
    for table in TABLES:
        with (ROOT / "data" / f"{table}.csv").open() as f:
            rows = list(csv.DictReader(f)); columns = list(rows[0])
        definitions = ", ".join('"' + c + '" TEXT' for c in columns)
        db.execute(f'CREATE TABLE "{table}" ({definitions})')
        db.executemany(f'INSERT INTO "{table}" VALUES ({", ".join("?" for _ in columns)})', [[r[c] for c in columns] for r in rows])
    sql = "\n".join(line for line in (ROOT / "analysis" / "sql_checks.sql").read_text().splitlines() if not line.strip().startswith("--"))
    for check in sql.split(";"):
        statement = check.strip()
        if statement:
            print(statement.splitlines()[0]); print(db.execute(statement).fetchall())

if __name__ == "__main__": main()
