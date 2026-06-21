from pathlib import Path
import json
import re
import unicodedata
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SNAPSHOT_PATH = ROOT / "data/processed/current_player_snapshot.parquet"
MANIFEST_PATH = ROOT / "app/data/player_images.json"
PLAYERS_DIR = ROOT / "app/assets/players"
OUT_PATH = ROOT / "reports/visual_identity/tm6_9_top50_market_value_image_audit.csv"

DSS_LEAGUES = {
    "Premier League",
    "LaLiga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "Eredivisie",
    "Liga Portugal",
    "Belgian Pro League",
    "Austrian Bundesliga",
}

def slugify(name: str) -> str:
    name = str(name).strip().lower()
    name = name.replace("ı", "i").replace("İ", "i")
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return re.sub(r"_+", "_", name).strip("_")

snapshot = pd.read_parquet(SNAPSHOT_PATH)


print("\nSNAPSHOT COLUMNS\n")
print(snapshot.columns.tolist())

NAME_CANDIDATES = [
    "player_name",
    "player_name_fbref",
    "player",
    "name",
    "short_name",
    "full_name",
    "player_name_tm",
    "player_name_transfermarkt",
]

name_col = next(
    (c for c in NAME_CANDIDATES if c in snapshot.columns),
    None
)

if name_col is None:
    raise ValueError(
        f"No player name column found. Columns: {snapshot.columns.tolist()}"
    )

value_col = "current_market_value_eur"
club_col = "current_club"
league_col = "current_league"
position_col = "position"
age_col = "current_age"

df = snapshot.copy()

if league_col:
    df = df[df[league_col].isin(DSS_LEAGUES)].copy()

df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
df = df.dropna(subset=[name_col, value_col])
df = df.sort_values(value_col, ascending=False).drop_duplicates(subset=[name_col], keep="first")
top50 = df.head(50).copy()

manifest = {}
if MANIFEST_PATH.exists():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

rows = []
for i, row in top50.reset_index(drop=True).iterrows():
    player_name = row[name_col]
    slug = slugify(player_name)

    manifest_value = manifest.get(slug)
    manifest_path = None
    manifest_exists = False

    if manifest_value:
        manifest_path = ROOT / manifest_value if not str(manifest_value).startswith("/") else Path(manifest_value)
        manifest_exists = manifest_path.exists()

    physical_candidates = list(PLAYERS_DIR.glob(f"{slug}.*"))
    physical_exists = len(physical_candidates) > 0

    rows.append({
        "rank_market_value": i + 1,
        "player_name": player_name,
        "slug": slug,
        "club": row.get(club_col, "") if club_col else "",
        "league": row.get(league_col, "") if league_col else "",
        "position": row.get(position_col, "") if position_col else "",
        "age": row.get(age_col, "") if age_col else "",
        "market_value_eur": row[value_col],
        "market_value_m": round(row[value_col] / 1_000_000, 1),
        "in_manifest": slug in manifest,
        "manifest_path": manifest_value or "",
        "manifest_file_exists": manifest_exists,
        "physical_file_exists": physical_exists,
        "physical_file": str(physical_candidates[0].relative_to(ROOT)) if physical_candidates else "",
        "image_status": "OK" if manifest_exists or physical_exists else "MISSING",
    })

audit = pd.DataFrame(rows)
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
audit.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")

print("=" * 70)
print("TOP50 MARKET VALUE IMAGE AUDIT")
print("=" * 70)
print(f"players: {len(audit)}")
print(f"with_image: {(audit['image_status'] == 'OK').sum()}")
print(f"missing: {(audit['image_status'] == 'MISSING').sum()}")
print(f"coverage: {100 * (audit['image_status'] == 'OK').mean():.2f}%")
print(f"saved: {OUT_PATH}")
print("=" * 70)

print("\nMISSING:")
print(
    audit.loc[audit["image_status"] == "MISSING",
              ["rank_market_value", "player_name", "club", "league", "market_value_m", "slug"]]
    .to_string(index=False)
)
