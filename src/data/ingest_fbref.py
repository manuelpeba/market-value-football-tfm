from pathlib import Path
import argparse

from src.data.validate_schema import load_and_validate_fbref


ROOT = Path(__file__).resolve().parents[2]


def ingest_fbref(input_path: str) -> Path:
    input_path = ROOT / input_path

    df = load_and_validate_fbref(input_path)

    output_dir = ROOT / "data" / "interim" / "fbref"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "fbref_player_standard.parquet"
    df.to_parquet(output_path, index=False)

    print("FBref ingestion completed")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Output: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    ingest_fbref(args.input)


if __name__ == "__main__":
    main()
