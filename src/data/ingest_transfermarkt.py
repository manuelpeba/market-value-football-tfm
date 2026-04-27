from pathlib import Path
import argparse
import pandas as pd

from src.data.validate_schema import load_and_validate_transfermarkt


ROOT = Path(__file__).resolve().parents[2]


def ingest_transfermarkt(input_path: str) -> Path:
    input_path = ROOT / input_path

    df = load_and_validate_transfermarkt(input_path)

    output_dir = ROOT / "data" / "interim" / "transfermarkt"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "transfermarkt_player_market_values.parquet"

    df.to_parquet(output_path, index=False)

    print("Transfermarkt ingestion completed")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Output: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Path to raw Transfermarkt CSV file, relative to project root",
    )
    args = parser.parse_args()

    ingest_transfermarkt(args.input)


if __name__ == "__main__":
    main()
