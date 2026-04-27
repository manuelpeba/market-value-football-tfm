from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "scouting.duckdb"

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(DB_PATH)

    con.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE SCHEMA IF NOT EXISTS staging;
    CREATE SCHEMA IF NOT EXISTS mart;
    """)

    con.close()
    print(f"Database created at: {DB_PATH}")

if __name__ == "__main__":
    main()
