#!/usr/bin/env python3
"""
TM.6.9A — Club Crest Coverage Audit

Audits which club crests are missing for the clubs actually used by the dashboard.

Outputs:
- reports/assets/club_crest_coverage.csv
- reports/assets/missing_club_crests.csv
- reports/assets/club_crest_summary.json
- reports/assets/missing_club_crests_urls_template.csv
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import pandas as pd

IMAGE_EXTS = (".svg", ".png", ".jpg", ".jpeg", ".webp")

CLUB_ASSET_ALIASES = {
    "celta vigo": "celta-de-vigo",
    "celta de vigo": "celta-de-vigo",
    "real club celta de vigo": "celta-de-vigo",
    "getafe": "getafe-cf",
    "getafe cf": "getafe-cf",
    "montpellier": "montpellier-hsc",
    "montpellier hsc": "montpellier-hsc",
    "angers": "angers-sco",
    "angers sco": "angers-sco",
    "holstein kiel": "holstein-kiel",
    "crystal palace": "crystal-palace",
    "crystal palace fc": "crystal-palace",
    "athletic bilbao": "athletic-bilbao",
    "athletic club": "athletic-bilbao",
    "watford": "watford",
    "watford fc": "watford",
    "torino": "torino",
    "torino calcio": "torino",
    "aj auxerre": "aj-auxerre",
    "auxerre": "aj-auxerre",
    "cercle brugge": "cercle-brugge",
    "udinese": "udinese-calcio",
    "udinese calcio": "udinese-calcio",
    "ssc napoli": "ssc-napoli",
    "napoli": "ssc-napoli",
    "real madrid": "real-madrid",
}

DISPLAY_ALIASES = {
    "celta vigo": "Celta Vigo",
    "celta de vigo": "Celta Vigo",
    "getafe cf": "Getafe",
    "getafe": "Getafe",
    "montpellier hsc": "Montpellier",
    "montpellier": "Montpellier",
    "angers": "Angers SCO",
    "angers sco": "Angers SCO",
    "holstein kiel": "Holstein Kiel",
    "crystal palace": "Crystal Palace",
    "crystal palace fc": "Crystal Palace",
    "athletic bilbao": "Athletic Bilbao",
    "athletic club": "Athletic Bilbao",
    "watford fc": "Watford",
    "watford": "Watford",
    "torino calcio": "Torino",
    "torino": "Torino",
    "aj auxerre": "AJ Auxerre",
    "auxerre": "AJ Auxerre",
}

CLUB_COLUMN_HINTS = (
    "club",
    "team",
    "squad",
    "current_club",
    "display_club",
    "season_context_club",
    "current_team",
)

DEFAULT_INPUTS = [
    "reports/dss/global_prospect_universe.csv",
    "reports/tm3_contract_intelligence/contract_intelligence_dataset.csv",
    "reports/strategy/transfer_portfolio_dataset.csv",
    "data/processed/current_player_snapshot.parquet",
    "data/processed/player_season_modeling_v13a.parquet",
    "data/processed/player_season_modeling_v13b_advanced.parquet",
]


def normalize_key(value: object) -> str:
    txt = str(value or "").strip().lower()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    txt = re.sub(r"[^a-z0-9]+", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def slugify(value: object) -> str:
    key = normalize_key(value)
    return re.sub(r"[^a-z0-9]+", "-", key).strip("-") or "club"


def display_name(value: object) -> str:
    raw = str(value or "").strip()
    key = normalize_key(raw)
    if key in DISPLAY_ALIASES:
        return DISPLAY_ALIASES[key]
    # Conservative title casing; avoid over-normalizing unknown official names.
    return raw


def expected_slug(club_display: str) -> str:
    key = normalize_key(club_display)
    return CLUB_ASSET_ALIASES.get(key, slugify(club_display))


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "app").exists() or (candidate / "data").exists() or (candidate / "reports").exists():
            return candidate
    return start


def list_assets(asset_dir: Path) -> dict[str, Path]:
    assets: dict[str, Path] = {}
    if not asset_dir.exists():
        return assets
    for p in asset_dir.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            assets[p.stem.lower()] = p
    return assets


def resolve_asset(club_display: str, assets: dict[str, Path]) -> Path | None:
    candidates = []
    key = normalize_key(club_display)
    alias = CLUB_ASSET_ALIASES.get(key)
    if alias:
        candidates.append(alias)
    candidates.append(slugify(club_display))
    candidates.append(key.replace(" ", "-"))
    for stem in dict.fromkeys(candidates):
        hit = assets.get(stem.lower())
        if hit:
            return hit
    return None


def read_dataset(path: Path) -> pd.DataFrame | None:
    try:
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() in {".parquet", ".pq"}:
            return pd.read_parquet(path)
    except Exception as exc:
        print(f"WARN: could not read {path}: {exc}")
    return None


def club_columns(df: pd.DataFrame) -> list[str]:
    cols = []
    for col in df.columns:
        low = col.lower()
        if any(hint == low or hint in low for hint in CLUB_COLUMN_HINTS):
            if not any(bad in low for bad in ("country", "league", "national", "contract", "score", "id")):
                cols.append(col)
    return cols


def collect_clubs(root: Path, paths: Iterable[str]) -> pd.DataFrame:
    rows = []
    for rel in paths:
        path = root / rel
        if not path.exists():
            continue
        df = read_dataset(path)
        if df is None or df.empty:
            continue
        for col in club_columns(df):
            values = df[col].dropna().astype(str).str.strip()
            values = values[~values.str.lower().isin(["", "nan", "none", "n/a", "na"])]
            counts = values.value_counts()
            for raw, n in counts.items():
                rows.append({
                    "club_raw": raw,
                    "club_display": display_name(raw),
                    "source_file": rel,
                    "source_column": col,
                    "usage_count": int(n),
                })
    if not rows:
        return pd.DataFrame(columns=["club_raw", "club_display", "source_file", "source_column", "usage_count"])
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--asset-dir", default="app/assets/clubs", help="Club crest asset directory")
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS, help="Input datasets to scan")
    args = parser.parse_args()

    root = find_project_root(Path(args.root).resolve())
    asset_dir = root / args.asset_dir
    reports_dir = root / "reports" / "assets"
    reports_dir.mkdir(parents=True, exist_ok=True)

    assets = list_assets(asset_dir)
    clubs = collect_clubs(root, args.inputs)

    if clubs.empty:
        print("No clubs found. Check --inputs or project root.")
        return 1

    grouped = (
        clubs.groupby("club_display", dropna=False)
        .agg(
            club_raw_examples=("club_raw", lambda x: " | ".join(sorted(set(map(str, x)))[:5])),
            source_sections=("source_file", lambda x: " | ".join(sorted(set(map(str, x))))),
            source_columns=("source_column", lambda x: " | ".join(sorted(set(map(str, x))))),
            total_usage=("usage_count", "sum"),
        )
        .reset_index()
    )

    records = []
    for _, r in grouped.iterrows():
        club = str(r["club_display"]).strip()
        slug = expected_slug(club)
        asset = resolve_asset(club, assets)
        records.append({
            "club_display": club,
            "club_raw_examples": r["club_raw_examples"],
            "slug_expected": slug,
            "asset_exists": bool(asset),
            "asset_file": str(asset.relative_to(root)) if asset else "",
            "total_usage": int(r["total_usage"]),
            "source_sections": r["source_sections"],
            "source_columns": r["source_columns"],
        })

    coverage = pd.DataFrame(records).sort_values(["asset_exists", "total_usage", "club_display"], ascending=[True, False, True])
    missing = coverage[~coverage["asset_exists"]].copy()

    coverage_path = reports_dir / "club_crest_coverage.csv"
    missing_path = reports_dir / "missing_club_crests.csv"
    template_path = reports_dir / "missing_club_crests_urls_template.csv"
    summary_path = reports_dir / "club_crest_summary.json"

    coverage.to_csv(coverage_path, index=False)
    missing.to_csv(missing_path, index=False)

    template = missing[["club_display", "slug_expected", "total_usage", "source_sections"]].copy()
    template["crest_url"] = ""
    template["preferred_filename"] = template["slug_expected"] + ".svg"
    template["source"] = "manual"
    template.to_csv(template_path, index=False)

    summary = {
        "clubs_total": int(len(coverage)),
        "clubs_with_asset": int(coverage["asset_exists"].sum()),
        "clubs_missing_asset": int((~coverage["asset_exists"]).sum()),
        "coverage_pct": round(float(coverage["asset_exists"].mean() * 100), 2),
        "asset_dir": str(asset_dir.relative_to(root)) if asset_dir.exists() else str(asset_dir),
        "outputs": {
            "coverage": str(coverage_path.relative_to(root)),
            "missing": str(missing_path.relative_to(root)),
            "manual_url_template": str(template_path.relative_to(root)),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("\nTop missing clubs by usage:")
    if missing.empty:
        print("  ✅ No missing club crests detected.")
    else:
        print(missing[["club_display", "slug_expected", "total_usage"]].head(30).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
