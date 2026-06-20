from pathlib import Path
import pandas as pd
import numpy as np
import re

# ============================
# PATHS
# ============================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "reports" / "visual_identity" / "tm6_9a_top30_visual_mvp_manifest.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "opportunity": ROOT / "reports" / "dss" / "global_prospect_universe.csv",
    "contract": ROOT / "reports" / "tm3_contract_intelligence" / "contract_intelligence_dataset.csv",
    "portfolio": ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv",
}

# ============================
# HELPERS
# ============================

def read_csv(path):
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

def slugify(x):
    x = str(x).lower().strip()
    x = re.sub(r"[^a-z0-9]+", "_", x)
    return x.strip("_")

def topn(df, col, n=5, label=""):
    if df.empty or col not in df.columns:
        return pd.DataFrame()
    out = df.sort_values(col, ascending=False).head(n).copy()
    out["selection_source"] = label or col
    return out

# ============================
# LOAD DATA
# ============================

dfs = {k: read_csv(v) for k, v in SOURCES.items()}

# ============================
# BUILD CANDIDATES POOL
# ============================

candidates = pd.concat([
    topn(dfs["opportunity"], "opportunity_score", 5, "top5_opportunity_score"),
    topn(dfs["opportunity"], "risk_adjusted_opportunity_score", 5, "top5_risk_adjusted_opportunity"),
    topn(dfs["contract"], "contract_opportunity_score", 5, "top5_contract_opportunity"),
    topn(dfs["contract"], "recruitment_contract_score", 5, "top5_recruitment_contract"),
    topn(dfs["portfolio"], "portfolio_score", 5, "top5_portfolio_score"),
    topn(dfs["portfolio"], "strategy_score", 5, "top5_strategy_score"),
], ignore_index=True)

if candidates.empty:
    raise RuntimeError("No candidates generated. Check input datasets.")

# ============================
# VISUAL KEY
# ============================

name_col = next((c for c in ["player", "player_name", "name", "player_name_tm"] if c in candidates.columns), None)
club_col = next((c for c in ["club", "current_club", "team"] if c in candidates.columns), None)

if "player_id_tm" in candidates.columns:
    candidates["_visual_key"] = candidates["player_id_tm"].fillna("").astype(str)
else:
    candidates["_visual_key"] = candidates[name_col].astype(str) + "|" + candidates[club_col].astype(str)

# ============================
# DEDUP AGGREGATION (SAFE)
# ============================

agg = candidates.groupby("_visual_key", as_index=False).agg(
    lambda s: s.dropna().iloc[0] if len(s.dropna()) else np.nan
).copy()

sources = (
    candidates.groupby("_visual_key")["selection_source"]
    .apply(lambda x: " | ".join(sorted(set(x.dropna().astype(str)))))
    .reset_index()
)

manifest = agg.merge(sources, on="_visual_key", how="left")

# ============================
# PRIORITY SCORE
# ============================

score_cols = [
    "opportunity_score",
    "risk_adjusted_opportunity_score",
    "contract_opportunity_score",
    "recruitment_contract_score",
    "portfolio_score",
    "strategy_score",
]

existing_scores = [c for c in score_cols if c in manifest.columns]

manifest["_priority_score"] = manifest[existing_scores].max(axis=1, skipna=True)

# ============================
# CLEAN + DEDUP FINAL
# ============================

if "player_id_tm" in manifest.columns:
    manifest = manifest.drop_duplicates(subset=["player_id_tm"]).copy()
else:
    manifest = manifest.drop_duplicates().copy()

manifest = manifest.sort_values("_priority_score", ascending=False).copy()

# ============================
# TOP 30 CUT
# ============================

manifest = manifest.head(30).reset_index(drop=True)

# ============================
# VISUAL RANK
# ============================

manifest["visual_rank"] = range(1, len(manifest) + 1)

# ============================
# ASSET MAPPING
# ============================

manifest["asset_filename"] = manifest.apply(
    lambda r: f"{r.get('player_id_tm')}.jpg"
    if pd.notna(r.get("player_id_tm"))
    else f"{slugify(r.get(name_col, 'unknown'))}.jpg",
    axis=1
)

manifest["asset_path"] = "app/assets/players/" + manifest["asset_filename"]

manifest["asset_status"] = "pending_manual_download"

manifest["source_url"] = ""
manifest["license_note"] = (
    "Manual curated asset for academic/demo use; "
    "source and licence pending review."
)

# ============================
# FINAL COLUMN ORDER (SAFE)
# ============================

preferred_cols = [
    "visual_rank",
    "player_id_tm",
    name_col,
    club_col,
    "league",
    "position",
    "age",
    "market_value_eur",
    "opportunity_score",
    "risk_adjusted_opportunity_score",
    "contract_opportunity_score",
    "recruitment_contract_score",
    "_priority_score",
    "selection_source",
    "asset_filename",
    "asset_path",
    "asset_status",
]

preferred_cols = [c for c in preferred_cols if c in manifest.columns]

manifest = manifest[preferred_cols + [c for c in manifest.columns if c not in preferred_cols and not c.startswith("_")]]

# ============================
# SAVE
# ============================

manifest.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print(f"Saved: {OUTPUT}")
print(manifest.head(30))
print("\nOK: TM.6.9a Visual MVP Manifest generated (30 players)")