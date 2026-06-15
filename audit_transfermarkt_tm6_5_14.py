#!/usr/bin/env python3
"""
TM.6.5.14 — Transfermarkt Validation & Data Integrity Audit

Run from project root:
    python audit_transfermarkt_tm6_5_14.py \
      --app streamlit_app_tm6_5_13_product_qa_closure_fix_9_leagues.py \
      --expected-leagues "Premier League,LaLiga,Bundesliga,Serie A,Ligue 1,Eredivisie,Primeira Liga,EFL Championship,Pro League" \
      --out reports/data_quality/tm6_5_14

Optional external validation file:
    --current-reference data/external/current_transfermarkt_reference.csv

Expected optional reference columns:
    player, current_club, current_league, market_value_eur, valuation_date
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd


DEFAULT_EXPECTED_LEAGUES = [
    "Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1",
    "Eredivisie", "Primeira Liga", "EFL Championship", "Pro League",
]

ALIASES = {
    "Liga Portugal": "Primeira Liga",
    "POR-Primeira Liga": "Primeira Liga",
    "Belgian Pro League": "Pro League",
    "Jupiler Pro League": "Pro League",
    "BEL-Pro League": "Pro League",
    "ENG-Premier League": "Premier League",
    "ESP-La Liga": "LaLiga",
    "La Liga": "LaLiga",
    "GER-Bundesliga": "Bundesliga",
    "ITA-Serie A": "Serie A",
    "FRA-Ligue 1": "Ligue 1",
    "NED-Eredivisie": "Eredivisie",
    "ENG-EFL Championship": "EFL Championship",
    "ESP-Segunda División": "Segunda División",
    "AUT-Bundesliga": "Austrian Bundesliga",
}

DATASET_CANDIDATES = {
    "dss_universe": [
        "reports/dss/global_prospect_universe.csv",
        "reports/rankings/global_prospect_universe.csv",
        "reports/rankings/top_undervalued_global.csv",
    ],
    "contract_intelligence": ["reports/tm3_contract_intelligence/contract_intelligence_dataset.csv"],
    "portfolio": ["reports/strategy/transfer_portfolio_dataset.csv"],
    "modeling_productive": [
        "data/processed/player_season_modeling_v13b_productive_candidate.parquet",
        "data/processed/player_season_modeling_v13b_advanced.parquet",
        "data/processed/player_season_modeling_v13a.parquet",
    ],
    "transfermarkt_features": [
        "data/processed/transfermarkt_features_v13a.parquet",
        "data/processed/transfermarkt_features.parquet",
        "data/processed/transfermarkt_features.csv",
    ],
    "role_dss": ["data/processed/player_role_dss.parquet"],
    "position_taxonomy": ["data/processed/player_position_taxonomy.parquet"],
}


@dataclass
class LoadedDataset:
    name: str
    path: Path
    df: pd.DataFrame


def norm_text(x: object) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip().lower()
    try:
        import unicodedata
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    except Exception:
        pass
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize_league(x: object) -> str:
    if pd.isna(x):
        return ""
    raw = str(x).strip()
    return ALIASES.get(raw, raw)


def season_num(x: object) -> float:
    if pd.isna(x):
        return np.nan
    s = str(x)
    # accepts 2526, 2425, 2025-2026, 2025/26, 2025
    if re.fullmatch(r"\d{4}", s):
        return float(s)
    years = re.findall(r"20\d{2}", s)
    if years:
        y = int(years[0])
        return float((y - 2000) * 100 + ((y + 1) - 2000))
    nums = re.findall(r"\d+", s)
    if nums:
        return float(nums[0])
    return np.nan


def read_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, low_memory=False)


def find_project_root(start: Path) -> Path:
    start = start if start.is_dir() else start.parent
    candidates = [start, *start.parents]
    # Prefer a real project root with known project artefacts, not a parent that merely contains /data.
    for c in candidates:
        if (c / "reports").exists() or (c / "streamlit_app.py").exists() or any(c.glob("streamlit_app_tm6*.py")):
            return c
    for c in candidates:
        if (c / "data" / "processed").exists():
            return c
    return start


def load_datasets(root: Path) -> list[LoadedDataset]:
    loaded = []
    for name, rels in DATASET_CANDIDATES.items():
        for rel in rels:
            p = root / rel
            if p.exists():
                try:
                    loaded.append(LoadedDataset(name, p, read_any(p)))
                except Exception as e:
                    print(f"WARN: could not read {p}: {e}", file=sys.stderr)
                break
    return loaded


def extract_dict_from_app(app_path: Path, var_name: str) -> dict:
    if not app_path.exists():
        return {}
    text = app_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"^{var_name}\s*=\s*(\{{.*?^\}})", text, flags=re.M | re.S)
    if not m:
        return {}
    try:
        return ast.literal_eval(m.group(1))
    except Exception:
        return {}


def basic_profile(ds: LoadedDataset, expected_leagues: list[str]) -> dict:
    df = ds.df
    out = {"dataset": ds.name, "path": str(ds.path), "rows": len(df), "cols": len(df.columns)}
    name_col = first_col(df, ["player_name_fbref", "player", "player_name", "name"])
    club_col = first_col(df, ["club", "team", "squad", "current_club", "club_actual"])
    league_col = first_col(df, ["league", "competition", "league_name"])
    season_col = first_col(df, ["season", "season_start_year"])
    out["players_unique"] = int(df[name_col].nunique()) if name_col else np.nan
    out["clubs_unique"] = int(df[club_col].nunique()) if club_col else np.nan
    out["leagues_unique_raw"] = int(df[league_col].nunique()) if league_col else np.nan
    out["seasons_unique"] = int(df[season_col].nunique()) if season_col else np.nan
    if season_col:
        sn = df[season_col].map(season_num)
        out["season_min"] = str(df.loc[sn.idxmin(), season_col]) if sn.notna().any() else ""
        out["season_max"] = str(df.loc[sn.idxmax(), season_col]) if sn.notna().any() else ""
        out["pct_2526"] = round(float((sn == 2526).mean() * 100), 2)
        out["pct_2425"] = round(float((sn == 2425).mean() * 100), 2)
    if league_col:
        leagues = sorted({normalize_league(v) for v in df[league_col].dropna().unique()})
        out["leagues_normalized"] = " | ".join(leagues)
        out["residual_out_of_scope_leagues"] = " | ".join([l for l in leagues if l and l not in expected_leagues])
        out["missing_expected_leagues"] = " | ".join([l for l in expected_leagues if l not in leagues])
    return out


def first_col(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    return next((c for c in candidates if c in df.columns), None)


def market_value_audit(ds: LoadedDataset) -> list[dict]:
    df = ds.df.copy()
    checks = []
    cols = [c for c in [
        "market_value_eur", "predicted_market_value_eur", "predicted_market_value",
        "market_value_gap_eur", "market_value_gap_pct", "inefficiency_score", "opportunity_score",
        "growth_score", "confidence_score", "risk_score"
    ] if c in df.columns]
    for col in cols:
        s = pd.to_numeric(df[col], errors="coerce")
        checks.append({
            "dataset": ds.name, "column": col,
            "rows": len(s), "nan": int(s.isna().sum()), "nan_pct": round(float(s.isna().mean()*100), 2),
            "negative": int((s < 0).sum()), "zero": int((s == 0).sum()),
            "min": float(s.min()) if s.notna().any() else np.nan,
            "p01": float(s.quantile(.01)) if s.notna().any() else np.nan,
            "median": float(s.median()) if s.notna().any() else np.nan,
            "p99": float(s.quantile(.99)) if s.notna().any() else np.nan,
            "max": float(s.max()) if s.notna().any() else np.nan,
        })
    return checks


def duplicate_audit(ds: LoadedDataset) -> pd.DataFrame:
    df = ds.df.copy()
    name = first_col(df, ["player_name_fbref", "player", "player_name", "name"])
    season = first_col(df, ["season", "season_start_year"])
    club = first_col(df, ["club", "team", "squad", "current_club", "club_actual"])
    keys = [c for c in [name, season, club] if c]
    if not keys:
        return pd.DataFrame()
    tmp = df.copy()
    for c in keys:
        tmp[c] = tmp[c].astype(str)
    dup = tmp[tmp.duplicated(keys, keep=False)].copy()
    if dup.empty:
        return pd.DataFrame(columns=["dataset", *keys, "duplicate_count"])
    return dup.groupby(keys).size().reset_index(name="duplicate_count").assign(dataset=ds.name)


def club_consistency_audit(ds: LoadedDataset, current_ref: Optional[pd.DataFrame]) -> pd.DataFrame:
    df = ds.df.copy()
    name = first_col(df, ["player_name_fbref", "player", "player_name", "name"])
    club = first_col(df, ["club", "team", "squad", "current_club", "club_actual"])
    league = first_col(df, ["league", "competition", "league_name"])
    season = first_col(df, ["season", "season_start_year"])
    if not name or not club:
        return pd.DataFrame()
    tmp = df[[c for c in [name, club, league, season] if c]].copy()
    tmp["_player_key"] = tmp[name].map(norm_text)
    if season:
        tmp["_season_num"] = tmp[season].map(season_num)
        latest = tmp.sort_values(["_player_key", "_season_num"]).groupby("_player_key", as_index=False).tail(1)
    else:
        latest = tmp.drop_duplicates("_player_key", keep="last")
    latest = latest.rename(columns={name: "player", club: "club_dashboard", league or "": "league_dashboard", season or "": "season_dashboard"})
    if current_ref is not None and not current_ref.empty and {"player", "current_club"}.issubset(current_ref.columns):
        ref = current_ref.copy()
        ref["_player_key"] = ref["player"].map(norm_text)
        keep = ["_player_key", "current_club"] + [c for c in ["current_league", "market_value_eur", "valuation_date"] if c in ref.columns]
        latest = latest.merge(ref[keep].drop_duplicates("_player_key"), on="_player_key", how="left")
        latest["club_match"] = latest["club_dashboard"].map(norm_text) == latest["current_club"].map(norm_text)
        latest["cause_probable"] = np.where(latest["current_club"].isna(), "Sin referencia externa", np.where(latest["club_match"], "OK", "Snapshot antiguo / merge latest-season / transferencia reciente"))
        return latest[latest["club_match"].eq(False) | latest["current_club"].isna()].copy()
    # Without reference, report players with multiple clubs across seasons as transfer-risk sample.
    multi = tmp.groupby("_player_key").agg(
        player=(name, "last"), clubs=(club, lambda s: " | ".join(pd.Series(s.dropna().astype(str).unique()).head(8))),
        n_clubs=(club, "nunique"), latest_club=(club, "last"), latest_season=(season, "last") if season else (club, "size")
    ).reset_index()
    multi["cause_probable"] = np.where(multi["n_clubs"] > 1, "Jugador con cambio de club en histórico: requiere validación externa", "Sin señal interna")
    return multi[multi["n_clubs"] > 1].sort_values("n_clubs", ascending=False)


def sample_players(ds: LoadedDataset, current_ref: Optional[pd.DataFrame], out_dir: Path) -> None:
    df = ds.df.copy()
    name = first_col(df, ["player_name_fbref", "player", "player_name", "name"])
    club = first_col(df, ["club", "team", "squad", "current_club", "club_actual"])
    league = first_col(df, ["league", "competition", "league_name"])
    season = first_col(df, ["season", "season_start_year"])
    if not name:
        return
    if "opportunity_score" in df.columns:
        top = df.sort_values("opportunity_score", ascending=False).head(20).copy()
    else:
        top = df.head(20).copy()
    rnd = df.sample(min(20, len(df)), random_state=42).copy()
    # transferred proxy = players appearing at multiple clubs
    if club:
        keys = df[name].map(norm_text)
        multi_keys = keys.groupby(keys).filter(lambda s: len(s) > 1).unique()
        transfer = df[keys.isin(multi_keys)].drop_duplicates(name).head(20).copy()
    else:
        transfer = pd.DataFrame()
    for label, part in [("top20", top), ("random20", rnd), ("transfer_proxy20", transfer)]:
        if part.empty:
            continue
        cols = [c for c in [name, club, league, season, "age", "position", "position_group", "market_value_eur", "predicted_market_value_eur", "opportunity_score"] if c in part.columns]
        part[cols].to_csv(out_dir / f"player_profile_validation_sample_{label}.csv", index=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--app", default="streamlit_app_tm6_5_13_product_qa_closure_fix_9_leagues.py")
    ap.add_argument("--expected-leagues", default=",".join(DEFAULT_EXPECTED_LEAGUES))
    ap.add_argument("--current-reference", default=None)
    ap.add_argument("--out", default="reports/data_quality/tm6_5_14")
    args = ap.parse_args()

    root = find_project_root(Path(args.root).resolve())
    out_dir = (root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    expected_leagues = [x.strip() for x in args.expected_leagues.split(",") if x.strip()]

    app_path = root / args.app
    if not app_path.exists() and (root / "streamlit_app.py").exists():
        app_path = root / "streamlit_app.py"

    current_ref = read_any(Path(args.current_reference)) if args.current_reference and Path(args.current_reference).exists() else None
    loaded = load_datasets(root)

    profiles = pd.DataFrame([basic_profile(ds, expected_leagues) for ds in loaded])
    profiles.to_csv(out_dir / "dataset_inventory_and_scope.csv", index=False)

    mv_checks = []
    dup_checks = []
    club_checks = []
    for ds in loaded:
        mv_checks.extend(market_value_audit(ds))
        dups = duplicate_audit(ds)
        if not dups.empty:
            dup_checks.append(dups)
        clubs = club_consistency_audit(ds, current_ref)
        if not clubs.empty:
            clubs.insert(0, "dataset", ds.name)
            club_checks.append(clubs)

    pd.DataFrame(mv_checks).to_csv(out_dir / "market_value_consistency_audit.csv", index=False)
    (pd.concat(dup_checks, ignore_index=True) if dup_checks else pd.DataFrame()).to_csv(out_dir / "duplicate_key_audit.csv", index=False)
    (pd.concat(club_checks, ignore_index=True) if club_checks else pd.DataFrame()).to_csv(out_dir / "club_current_context_audit.csv", index=False)

    if loaded:
        primary = next((d for d in loaded if d.name == "dss_universe"), loaded[0])
        sample_players(primary, current_ref, out_dir)

    overrides = {
        "CURRENT_CLUB_OVERRIDES": extract_dict_from_app(app_path, "CURRENT_CLUB_OVERRIDES"),
        "CURRENT_LEAGUE_OVERRIDES_BY_PLAYER": extract_dict_from_app(app_path, "CURRENT_LEAGUE_OVERRIDES_BY_PLAYER"),
        "LEAGUE_STRENGTH_INDEX": extract_dict_from_app(app_path, "LEAGUE_STRENGTH_INDEX"),
    }
    (out_dir / "streamlit_static_config_audit.json").write_text(json.dumps(overrides, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "root": str(root),
        "app_path": str(app_path),
        "expected_league_count": len(expected_leagues),
        "expected_leagues": expected_leagues,
        "datasets_loaded": [str(d.path.relative_to(root)) for d in loaded],
        "current_reference_used": bool(current_ref is not None),
        "outputs": sorted(p.name for p in out_dir.glob("*")),
    }
    (out_dir / "audit_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
