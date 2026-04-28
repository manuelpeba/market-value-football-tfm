from pathlib import Path
import argparse
import pandas as pd
from unidecode import unidecode


ROOT = Path(__file__).resolve().parents[2]


def normalize_name(name: str) -> str:
    return unidecode(str(name)).lower().strip()


def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(ROOT / path)


def build_panel(transfermarkt_path: str, fbref_path: str, output_path: str) -> Path:
    tm = load_parquet(transfermarkt_path)
    fb = load_parquet(fbref_path)

    tm = tm.copy()
    fb = fb.copy()

    tm["normalized_name"] = tm["player_name"].apply(normalize_name)
    fb["normalized_name"] = fb["player_name"].apply(normalize_name)

    panel = tm.merge(
        fb,
        how="left",
        on=["normalized_name", "season", "age"],
        suffixes=("_tm", "_fbref"),
        indicator=True,
    )

    panel["matching_status"] = panel["_merge"].map({
        "both": "matched",
        "left_only": "unmatched_transfermarkt",
        "right_only": "unmatched_fbref",
    })

    panel["matching_confidence"] = panel["_merge"].map({
        "both": 1.0,
        "left_only": 0.0,
        "right_only": 0.0,
    })

    panel = panel.drop(columns=["_merge"])

    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(output, index=False)

    print("Player-season panel built")
    print(f"Rows: {len(panel):,}")
    print(f"Columns: {len(panel.columns):,}")
    print(panel["matching_status"].value_counts(dropna=False))
    print(f"Output: {output}")

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfermarkt", required=True)
    parser.add_argument("--fbref", required=True)
    parser.add_argument(
        "--output",
        default="data/processed/player_season_panel.parquet",
    )
    args = parser.parse_args()

    build_panel(args.transfermarkt, args.fbref, args.output)


if __name__ == "__main__":
    main()
