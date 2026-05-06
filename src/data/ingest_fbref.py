from io import StringIO
from pathlib import Path
import argparse

import pandas as pd
from bs4 import BeautifulSoup, Comment


ROOT = Path(__file__).resolve().parents[2]


def extract_fbref_player_table(html_path: Path) -> pd.DataFrame:
    """
    Extract the player-level standard stats table from a FBref HTML file.

    FBref often stores player tables inside HTML comments, so a direct
    pandas.read_html(html_path) may only return team-level tables.
    """

    html_path = Path(html_path)

    with html_path.open("r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for comment in comments:
        if "stats_standard" not in comment:
            continue

        comment_soup = BeautifulSoup(comment, "lxml")
        table = comment_soup.find("table")

        if table is None:
            continue

        html_io = StringIO(str(table))
        df = pd.read_html(html_io)[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                "_".join(str(part).strip() for part in col if str(part) != "nan")
                for col in df.columns
            ]

        return df

    raise ValueError(f"Player standard stats table not found in: {html_path}")


def ingest_fbref(input_path: str | Path, output_path: str | Path) -> Path:
    """
    Parse one raw FBref HTML file and save the extracted player table as parquet.
    """

    input_path = Path(input_path)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    output_path = Path(output_path)
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    print("Parsing FBref HTML player table...")

    df = extract_fbref_player_table(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    print("FBref ingestion completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Output: {output_path}")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a FBref standard stats HTML file into parquet."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the raw FBref HTML file.",
    )

    parser.add_argument(
        "--output",
        default="data/processed/fbref_features.parquet",
        help="Output parquet path.",
    )

    args = parser.parse_args()

    ingest_fbref(
        input_path=args.input,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
