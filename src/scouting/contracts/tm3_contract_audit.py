from pathlib import Path
import json
import re
import sys
import pandas as pd

ROOT = Path.cwd()
REPORT_DIR = ROOT / "reports" / "tm3_contract_audit"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

EXACT_CONTRACT_COLUMNS = {
    "contract_expiration_date",
    "contract_until",
    "contract_end",
    "contract_expires",
    "contract_remaining",
    "remaining_contract",
    "expiration_year",
}

SEMANTIC_PATTERNS = [
    re.compile(r"contract", re.I),
    re.compile(r"expir", re.I),
    re.compile(r"expires", re.I),
    re.compile(r"until", re.I),
    re.compile(r"remaining", re.I),
    re.compile(r"free[_\s-]?agent", re.I),
]

DATA_EXTENSIONS = {".csv", ".parquet", ".pkl", ".pickle", ".feather"}
TEXT_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".json", ".txt", ".ipynb"}
EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", "mlruns"}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def read_columns(path: Path):
    try:
        if path.suffix == ".csv":
            return list(pd.read_csv(path, nrows=0).columns)
        if path.suffix == ".parquet":
            return list(pd.read_parquet(path).columns)
        if path.suffix in {".pkl", ".pickle"}:
            obj = pd.read_pickle(path)
            return list(obj.columns) if hasattr(obj, "columns") else []
        if path.suffix == ".feather":
            return list(pd.read_feather(path).columns)
    except Exception as exc:
        return {"__error__": str(exc)}
    return []


def classify_column(col: str) -> str:
    c = col.strip()
    if c in EXACT_CONTRACT_COLUMNS:
        return "exact_candidate"
    if any(p.search(c) for p in SEMANTIC_PATTERNS):
        return "semantic_candidate"
    return "no_match"


def scan_data_files():
    rows = []
    data_files = []
    for path in ROOT.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in DATA_EXTENSIONS:
            continue
        data_files.append(path)
        cols = read_columns(path)
        if isinstance(cols, dict):
            rows.append({
                "file": str(path.relative_to(ROOT)),
                "file_type": path.suffix.lower(),
                "column": "__READ_ERROR__",
                "match_type": "error",
                "error": cols.get("__error__", "unknown"),
            })
            continue
        for col in cols:
            mt = classify_column(str(col))
            if mt != "no_match":
                rows.append({
                    "file": str(path.relative_to(ROOT)),
                    "file_type": path.suffix.lower(),
                    "column": col,
                    "match_type": mt,
                    "error": "",
                })
    return data_files, pd.DataFrame(rows)


def scan_text_files():
    rows = []
    keywords = [*EXACT_CONTRACT_COLUMNS, "contract", "contrato", "contractual", "expiration", "expiración", "expires", "free agent"]
    for path in ROOT.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for kw in keywords:
            count = len(re.findall(re.escape(kw), text, flags=re.I))
            if count:
                rows.append({"file": str(path.relative_to(ROOT)), "keyword": kw, "mentions": count})
    return pd.DataFrame(rows)


def main():
    data_files, data_hits = scan_data_files()
    text_hits = scan_text_files()

    data_hits_path = REPORT_DIR / "contract_column_candidates.csv"
    text_hits_path = REPORT_DIR / "contract_text_mentions.csv"
    coverage_path = REPORT_DIR / "contract_coverage.csv"
    by_league_path = REPORT_DIR / "contract_coverage_by_league.csv"
    report_path = REPORT_DIR / "contract_coverage_report.md"

    data_hits.to_csv(data_hits_path, index=False)
    text_hits.to_csv(text_hits_path, index=False)

    exact_hits = data_hits[data_hits.get("match_type", pd.Series(dtype=str)).eq("exact_candidate")] if not data_hits.empty else pd.DataFrame()
    semantic_hits = data_hits[data_hits.get("match_type", pd.Series(dtype=str)).eq("semantic_candidate")] if not data_hits.empty else pd.DataFrame()

    has_contract_data = not exact_hits.empty or not semantic_hits.empty

    # Coverage is only computable if a real contractual column exists in a tabular artifact.
    coverage = pd.DataFrame([{
        "scope": "tabular_artifacts",
        "files_scanned": len(data_files),
        "exact_contract_columns_found": int(len(exact_hits)),
        "semantic_contract_columns_found": int(len(semantic_hits)),
        "contract_data_available": bool(has_contract_data),
        "coverage_computable": bool(has_contract_data),
    }])
    coverage.to_csv(coverage_path, index=False)

    # Placeholder expected by sprint spec. Real by-league coverage requires contract data + league column.
    pd.DataFrame(columns=["league", "observations", "contract_available", "contract_coverage_pct"]).to_csv(by_league_path, index=False)

    status = "CONTRACT DATA AVAILABLE" if has_contract_data else "DATA AVAILABILITY GAP"
    report = f"""# TM.3 Contract Data Audit\n\n## Status\n\n```text\n{status}\n```\n\n## Audit scope\n\n- Root scanned: `{ROOT}`\n- Tabular files scanned: `{len(data_files)}`\n- Exact contract columns searched:\n\n```text\n{', '.join(sorted(EXACT_CONTRACT_COLUMNS))}\n```\n\n## Results\n\n| Metric | Value |\n|---|---:|\n| Exact contract columns found | {len(exact_hits)} |\n| Semantic contract columns found | {len(semantic_hits)} |\n| Contract coverage computable | {str(has_contract_data)} |\n\n## Interpretation\n\n"""
    if has_contract_data:
        report += "Contract-related columns were detected in tabular artifacts. Next step: compute observation-level, league-level and season-level coverage.\n"
    else:
        report += "No contractual columns were detected in the available tabular artifacts. TM.3 should therefore be documented as a Data Availability Gap and the Contract Intelligence architecture should be prepared without modifying Opportunity Score, Risk Score or existing Recruitment Intelligence modules.\n"

    report += f"""\n## Generated outputs\n\n```text\nreports/tm3_contract_audit/contract_coverage.csv\nreports/tm3_contract_audit/contract_coverage_by_league.csv\nreports/tm3_contract_audit/contract_coverage_report.md\nreports/tm3_contract_audit/contract_column_candidates.csv\nreports/tm3_contract_audit/contract_text_mentions.csv\n```\n"""
    report_path.write_text(report, encoding="utf-8")

    print(report)

if __name__ == "__main__":
    main()
