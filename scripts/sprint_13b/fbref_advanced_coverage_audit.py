from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw/fbref/sprint_13b/soccerdata")
REPORT_DIR = Path("reports/sprint_13b")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = ["shooting", "playing_time", "misc"]


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten soccerdata MultiIndex columns into snake-like names."""
    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(x) for x in col if str(x) not in ["", "nan", "None"]]).strip()
            for col in df.columns
        ]
    else:
        df.columns = [str(c) for c in df.columns]

    df.columns = (
        pd.Index(df.columns)
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_per_", regex=False)
        .str.replace("%", "_pct", regex=False)
        .str.replace("+", "_plus_", regex=False)
        .str.replace("-", "_minus_", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace("__", "_", regex=False)
        .str.lower()
    )

    return df


def add_index_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Convert soccerdata index metadata into columns."""
    df = df.copy()

    if isinstance(df.index, pd.MultiIndex):
        index_names = [
            name if name is not None else f"index_{i}"
            for i, name in enumerate(df.index.names)
        ]
        df = df.reset_index()
        df.columns = list(index_names) + list(df.columns[len(index_names):])
    else:
        df = df.reset_index()

    return df


rows = []
variable_rows = []

for dataset in DATASETS:
    dataset_dir = RAW_DIR / dataset

    if not dataset_dir.exists():
        rows.append({
            "dataset": dataset,
            "file": "",
            "status": "missing_dataset_dir",
            "rows": 0,
            "columns": 0,
            "error": f"{dataset_dir} does not exist",
        })
        continue

    for path in sorted(dataset_dir.glob("*.parquet")):
        print(f"Auditing {path}")

        try:
            df = pd.read_parquet(path)
            df = add_index_metadata(df)
            df = flatten_columns(df)

            n_rows = len(df)
            n_cols = len(df.columns)

            rows.append({
                "dataset": dataset,
                "file": path.name,
                "status": "ok",
                "rows": n_rows,
                "columns": n_cols,
                "error": "",
            })

            metadata_cols = {
                "league",
                "season",
                "team",
                "player",
                "nation",
                "pos",
                "age",
                "born",
                "url",
            }

            for col in df.columns:
                if col in metadata_cols:
                    continue

                non_null = df[col].notna().sum()
                coverage_pct = non_null / n_rows if n_rows else 0

                numeric_col = pd.to_numeric(df[col], errors="coerce")
                numeric_non_null = numeric_col.notna().sum()

                variable_rows.append({
                    "dataset": dataset,
                    "file": path.name,
                    "variable": col,
                    "rows": n_rows,
                    "non_null": int(non_null),
                    "coverage_pct": round(float(coverage_pct), 4),
                    "numeric_non_null": int(numeric_non_null),
                    "numeric_coverage_pct": round(float(numeric_non_null / n_rows), 4) if n_rows else 0,
                    "min": numeric_col.min(skipna=True),
                    "max": numeric_col.max(skipna=True),
                    "mean": numeric_col.mean(skipna=True),
                    "std": numeric_col.std(skipna=True),
                })

        except Exception as exc:
            rows.append({
                "dataset": dataset,
                "file": path.name,
                "status": "error",
                "rows": 0,
                "columns": 0,
                "error": repr(exc),
            })

file_audit = pd.DataFrame(rows)
variable_audit = pd.DataFrame(variable_rows)

file_audit_path = REPORT_DIR / "fbref_advanced_file_audit.csv"
variable_audit_path = REPORT_DIR / "fbref_advanced_coverage_audit.csv"

file_audit.to_csv(file_audit_path, index=False, encoding="utf-8-sig")
variable_audit.to_csv(variable_audit_path, index=False, encoding="utf-8-sig")

summary = (
    variable_audit
    .groupby(["dataset", "variable"], as_index=False)
    .agg(
        total_rows=("rows", "sum"),
        total_non_null=("non_null", "sum"),
        total_numeric_non_null=("numeric_non_null", "sum"),
        avg_coverage_pct=("coverage_pct", "mean"),
        avg_numeric_coverage_pct=("numeric_coverage_pct", "mean"),
        min_value=("min", "min"),
        max_value=("max", "max"),
        mean_value=("mean", "mean"),
        std_value=("std", "mean"),
        n_files=("file", "nunique"),
    )
)

summary["global_coverage_pct"] = (
    summary["total_non_null"] / summary["total_rows"]
).round(4)

summary["global_numeric_coverage_pct"] = (
    summary["total_numeric_non_null"] / summary["total_rows"]
).round(4)

summary_path = REPORT_DIR / "fbref_advanced_variable_summary.csv"
summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

print("\nSaved:")
print(file_audit_path)
print(variable_audit_path)
print(summary_path)

print("\nFile audit status:")
print(file_audit["status"].value_counts(dropna=False))

print("\nTop variables by global numeric coverage:")
print(
    summary
    .sort_values(["global_numeric_coverage_pct", "dataset", "variable"], ascending=[False, True, True])
    .head(30)
)