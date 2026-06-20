from pathlib import Path
import re
import time
import unicodedata
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "app" / "assets" / "clubs"
REPORT_DIR = ROOT / "reports" / "visual_identity"
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "ScoutingIQ-TFM/1.0 (academic project; contact: local)"
}

DATA_CANDIDATES = [
    ROOT / "data" / "processed" / "current_player_snapshot.parquet",
    ROOT / "reports" / "dss" / "global_prospect_universe.csv",
    ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv",
]

TARGET_LEAGUES = {
    "Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1",
    "Eredivisie", "Liga Portugal", "Belgian Pro League", "Austrian Bundesliga",
    "LaLiga (España)", "Bundesliga (Alemania)"
}

def slug(value):
    txt = str(value or "").strip()
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    txt = txt.lower()
    txt = re.sub(r"[^a-z0-9]+", "-", txt).strip("-")
    return txt or "asset"

def find_col(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

def load_clubs():
    frames = []
    for path in DATA_CANDIDATES:
        if not path.exists():
            continue
        df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
        club_col = find_col(df, ["current_club", "club", "display_club", "club_name", "squad", "team"])
        league_col = find_col(df, ["league", "competition", "league_display"])
        if not club_col:
            continue
        cols = [club_col] + ([league_col] if league_col else [])
        tmp = df[cols].copy()
        tmp = tmp.rename(columns={club_col: "club", league_col: "league"} if league_col else {club_col: "club"})
        frames.append(tmp)

    clubs = pd.concat(frames, ignore_index=True)
    clubs["club"] = clubs["club"].astype(str).str.strip()
    clubs = clubs[(clubs["club"] != "") & (clubs["club"].str.lower() != "nan")]

    if "league" in clubs.columns:
        clubs["league"] = clubs["league"].astype(str).str.strip()
        prod = clubs[clubs["league"].isin(TARGET_LEAGUES)]
        if not prod.empty:
            clubs = prod

    clubs["slug"] = clubs["club"].map(slug)
    return clubs.drop_duplicates("slug").sort_values("club")

def wikidata_search(club):
    r = requests.get(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbsearchentities",
            "search": club,
            "language": "en",
            "format": "json",
            "limit": 5,
        },
        headers=HEADERS,
        timeout=25,
    )
    r.raise_for_status()
    return [x["id"] for x in r.json().get("search", [])]

def wikidata_logo_filename(qid):
    r = requests.get(
        f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json",
        headers=HEADERS,
        timeout=25,
    )
    r.raise_for_status()
    claims = r.json()["entities"].get(qid, {}).get("claims", {})
    vals = claims.get("P154", [])
    if not vals:
        return None
    return vals[0]["mainsnak"]["datavalue"]["value"]

def extension_from_filename(filename):
    ext = Path(filename).suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        return ext
    return ".png"

def download_commons_file(filename, slug_name):
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + requests.utils.quote(filename)
    ext = extension_from_filename(filename)
    out_path = OUT_DIR / f"{slug_name}{ext}"

    r = requests.get(url, headers=HEADERS, timeout=35, allow_redirects=True)
    r.raise_for_status()

    if len(r.content) < 1000:
        return None, url, "too_small"

    out_path.write_bytes(r.content)
    return out_path, url, "downloaded"

def main():
    clubs = load_clubs()
    print(f"Clubes únicos detectados: {len(clubs)}")

    rows = []

    for _, row in clubs.iterrows():
        club = row["club"]
        s = row["slug"]

        existing = []
        for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
            p = OUT_DIR / f"{s}{ext}"
            if p.exists() and p.stat().st_size > 1000:
                existing.append(p)

        if existing:
            rows.append({"club": club, "slug": s, "status": "exists", "path": str(existing[0]), "source": ""})
            continue

        status = "not_found"
        source = ""
        path = ""

        try:
            qids = wikidata_search(club)
            for qid in qids:
                filename = wikidata_logo_filename(qid)
                if not filename:
                    continue
                out_path, source, status = download_commons_file(filename, s)
                if out_path:
                    path = str(out_path)
                    break
                time.sleep(0.25)

        except Exception as e:
            status = f"error: {type(e).__name__}"

        rows.append({"club": club, "slug": s, "status": status, "path": path, "source": source})
        print(f"{status:18} | {club} -> {s}")
        time.sleep(0.45)

    report = pd.DataFrame(rows)
    out_report = REPORT_DIR / "tm6_9a_club_crests_download_report.csv"
    report.to_csv(out_report, index=False, encoding="utf-8")

    print("\nGuardado:", out_report)
    print(report["status"].value_counts(dropna=False))

if __name__ == "__main__":
    main()
