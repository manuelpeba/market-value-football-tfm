from pathlib import Path
import argparse
import pandas as pd
from unidecode import unidecode
from rapidfuzz import fuzz


ROOT = Path(__file__).resolve().parents[2]


def normalize_name(name: str) -> str:
    """Normalize player names to improve matching across sources."""
    return unidecode(str(name)).lower().strip()


def load_parquet(path: str) -> pd.DataFrame:
    """Load a parquet file from project root."""
    return pd.read_parquet(ROOT / path)


def compute_name_similarity(name_tm: str, name_fbref: str) -> float:
    """Compute fuzzy similarity between normalized player names."""
    return fuzz.token_sort_ratio(str(name_tm), str(name_fbref)) / 100.0


def build_matching_status(row: pd.Series) -> str:
    """Assign matching status based on merge result."""
    if row["_merge"] == "both":
        return "matched"
    if row["_merge"] == "left_only":
        return "unmatched_transfermarkt"
    if row["_merge"] == "right_only":
        return "unmatched_fbref"
    return "unknown"


def build_panel(
    transfermarkt_path: str,
    fbref_path: str,
    output_path: str,
) -> Path:
    tm = load_parquet(transfermarkt_path)
    fb = load_parquet(fbref_path)

    tm = tm.copy()
    fb = fb.copy()

    # Normalize names for exact baseline matching
    tm["normalized_name"] = tm["player_name"].apply(normalize_name)
    fb["normalized_name"] = fb["player_name"].apply(normalize_name)

    panel = tm.merge(
        fb,
        how="outer",
        on=["normalized_name", "season", "age"],
        suffixes=("_tm", "_fbref"),
        indicator=True,
    )

    panel["matching_status"] = panel.apply(build_matching_status, axis=1)

    # Name similarity is 1.0 for exact normalized joins.
    # Kept as explicit variable to support future fuzzy matching v1.
    panel["name_similarity"] = panel.apply(
        lambda row: compute_name_similarity(
            row.get("player_name_tm", ""),
            row.get("player_name_fbref", ""),
        )
        if row["_merge"] == "both"
        else 0.0,
        axis=1,
    )

    # Matching confidence v0:
    # - exact matched records receive similarity-based confidence
    # - unmatched records receive 0
    panel["matching_confidence"] = panel.apply(
        lambda row: row["name_similarity"] if row["_merge"] == "both" else 0.0,
        axis=1,
    )

    panel = panel.drop(columns=["_merge"])

    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(output, index=False)

    print("Player-season panel built")
    print(f"Rows: {len(panel):,}")
    print(f"Columns: {len(panel.columns):,}")
    print("\nMatching status:")
    print(panel["matching_status"].value_counts(dropna=False))
    print("\nMatching confidence:")
    print(panel["matching_confidence"].describe())
    print(f"\nOutput: {output}")

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

    build_panel(
        transfermarkt_path=args.transfermarkt,
        fbref_path=args.fbref,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()