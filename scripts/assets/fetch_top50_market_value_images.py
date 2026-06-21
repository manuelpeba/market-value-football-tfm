from pathlib import Path
from io import BytesIO
from datetime import date
import json, re, time, unicodedata
import requests
import pandas as pd
from PIL import Image

ROOT = Path(".")
OUT = ROOT / "app/assets/players"
MANIFEST = ROOT / "app/data/player_images.json"
AUDIT = ROOT / "reports/visual_identity/tm6_9_top50_market_value_fetch_audit.csv"
MISSING_SLUGS = ROOT / "reports/visual_identity/tm6_9_top50_market_value_missing_slugs.txt"

OUT.mkdir(parents=True, exist_ok=True)
AUDIT.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "ScoutingIQ-TFM/1.0 academic visual asset enrichment"}
WIKI_LANGS = ["en", "es", "de", "fr", "it", "nl", "pt"]

def load_targets() -> dict:
    slugs = [
        line.strip()
        for line in MISSING_SLUGS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return {
        slug: {
            "player_name": slug.replace("_", " ").title(),
            "query": slug.replace("_", " "),
            "filename": f"{slug}.webp",
            "aliases": [
                slug.replace("_", " ").title(),
                slug.replace("_", " "),
            ],
        }
        for slug in slugs
    }

TARGETS = load_targets()

def save_webp(url, out_path):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content)).convert("RGB")
    img.thumbnail((512, 512))

    canvas = Image.new("RGB", (512, 512), "#f1f5f9")
    canvas.paste(img, ((512 - img.width)//2, (512 - img.height)//2))
    canvas.save(out_path, "WEBP", quality=88, method=6)

def wikidata_candidates(term):
    params = {
        "action": "wbsearchentities",
        "search": term,
        "language": "en",
        "format": "json",
        "limit": 10,
    }
    r = requests.get("https://www.wikidata.org/w/api.php", params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json().get("search", [])

def wikidata_image(qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    ent = r.json()["entities"][qid]
    p18 = ent.get("claims", {}).get("P18", [])
    if not p18:
        return None, ""
    filename = p18[0]["mainsnak"]["datavalue"]["value"]
    img_url = (
        "https://commons.wikimedia.org/w/index.php"
        "?title=Special:Redirect/file/"
        + requests.utils.quote(filename)
        + "&width=512"
    )
    return img_url, filename

def wikipedia_page_image(term, lang):
    api = f"https://{lang}.wikipedia.org/w/api.php"

    search_params = {
        "action": "opensearch",
        "search": term,
        "limit": 5,
        "namespace": 0,
        "format": "json",
    }
    r = requests.get(api, params=search_params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    titles = r.json()[1]

    for title in titles:
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "piprop": "original",
            "format": "json",
        }
        rr = requests.get(api, params=params, headers=HEADERS, timeout=20)
        rr.raise_for_status()
        pages = rr.json().get("query", {}).get("pages", {})
        for page in pages.values():
            src = page.get("original", {}).get("source")
            if src:
                return src, title
    return None, ""

def find_image(aliases):
    queries = []
    for a in aliases:
        queries.extend([a, f"{a} footballer", f"{a} futbolista", f"{a} soccer player"])
    queries = list(dict.fromkeys(queries))

    for q in queries:
        try:
            for c in wikidata_candidates(q):
                qid = c.get("id")
                if not qid:
                    continue
                url, filename = wikidata_image(qid)
                if url:
                    return url, "wikidata", q, qid, filename
        except Exception:
            pass
        time.sleep(0.15)

    for q in queries:
        for lang in WIKI_LANGS:
            try:
                url, title = wikipedia_page_image(q, lang)
                if url:
                    return url, f"wikipedia_{lang}", q, "", title
            except Exception:
                pass
            time.sleep(0.15)

    return "", "not_found", "", "", ""

def update_manifest():
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        manifest = {
            "version": 3,
            "last_updated": str(date.today()),
            "default_image": "defaults/default_player.webp",
            "players": {},
        }

    manifest["version"] = max(int(manifest.get("version", 3)), 3)
    manifest["last_updated"] = str(date.today())
    manifest.setdefault("default_image", "defaults/default_player.webp")
    manifest.setdefault("players", {})

    for p in OUT.glob("*.webp"):
        manifest["players"][p.stem] = f"players/{p.name}"

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest

def main():
    rows = []

    for slug, cfg in TARGETS.items():
        player = cfg["player_name"]
        dst = OUT / f"{slug}.webp"

        if dst.exists():
            print(f"{player}: already_exists")
            rows.append({
                "slug": slug, "player_name": player, "status": "already_exists",
                "source": "", "query": "", "qid": "", "source_ref": "", "url": "", "error": ""
            })
            continue

        try:
            url, source, query, qid, source_ref = find_image(cfg["aliases"])

            if url:
                save_webp(url, dst)
                print(f"{player}: downloaded ({source})")
                status = "downloaded"
            else:
                print(f"{player}: not_found")
                status = "not_found"

            rows.append({
                "slug": slug, "player_name": player, "status": status,
                "source": source, "query": query, "qid": qid,
                "source_ref": source_ref, "url": url, "error": ""
            })

        except Exception as e:
            print(f"{player}: error {e}")
            rows.append({
                "slug": slug, "player_name": player, "status": "error",
                "source": "", "query": "", "qid": "",
                "source_ref": "", "url": "", "error": str(e)
            })

    manifest = update_manifest()
    pd.DataFrame(rows).to_csv(AUDIT, index=False, encoding="utf-8-sig")

    print()
    print("audit:", AUDIT)
    print("targets:", len(TARGETS))
    print("mapped manifest:", len(manifest["players"]))

if __name__ == "__main__":
    main()
