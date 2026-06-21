from pathlib import Path
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import time

ROOT = Path(".")
PLAYER_LIST = ROOT / "reports/visual_identity/tm6_9_top60_players.csv"
OUT_DIR = ROOT / "app/assets/players"
AUDIT = ROOT / "reports/visual_identity/tm6_9_top60_player_image_fetch_audit.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "ScoutingIQ-TFM/1.0 academic project image enrichment"
}


ALIASES = {
    "Mario Martín": ["Mario Martin", "Mario Martín Rielves"],
    "Christantus Uche": ["Christantus Uche", "Uche Christantus"],
    "Luca Marianucci": ["Luca Marianucci"],
    "Carlos Romero": ["Carlos Romero Serrano"],
    "Mark O'Mahony": ["Mark O Mahony", "Mark O'Mahony"],
    "Gerard Martín": ["Gerard Martin", "Gerard Martín Langreo"],
    "Erick Nunes": ["Erick Nunes", "Erick Nunes Barbosa dos Santos"],
    "Junior Kadile": ["Junior Kadile"],
    "Hugo Rincón": ["Hugo Rincon", "Hugo Rincón Lumbreras"],
    "Óscar Aranda": ["Oscar Aranda", "Óscar Aranda"],
    "Bas Van den Eynden": ["Bas Van den Eynden", "Bas van den Eynden"],
    "Emilio Kehrer": ["Emilio Kehrer"],
    "Jamie Lawrence": ["Jamie Lawrence", "Jamie Lawrence footballer"],

"Yan Diomande": ["Yan Diomande", "Yan Diomandé"],
    "Adrian Blake": ["Adrian Blake footballer", "Adrian Blake"],
    "Hugo Álvarez": ["Hugo Alvarez", "Hugo Álvarez Antúnez"],
    "Reda Belahyane": ["Reda Belahyane"],
    "Lukas Ullrich": ["Lukas Ullrich footballer", "Lukas Ullrich"],
    "Marwan Al-Sahafi": ["Marwan Al-Sahafi", "Marwan Al Sahafi"],
    "Arthur Atta": ["Arthur Atta"],
    "Brayann Pereira": ["Brayann Pereira"],
    "Melayro Bogarde": ["Melayro Bogarde"],
}


def wiki_search(player_name):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": player_name,
        "language": "en",
        "format": "json",
        "limit": 5,
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json().get("search", [])

def wikidata_entity(qid):
    url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(qid)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()["entities"][qid]

def commons_image_url(filename, width=512):
    return (
        "https://commons.wikimedia.org/w/index.php"
        "?title=Special:Redirect/file/"
        + requests.utils.quote(filename)
        + f"&width={width}"
    )

def get_commons_image_from_entity(entity):
    claims = entity.get("claims", {})
    image_claims = claims.get("P18", [])
    if not image_claims:
        return None
    return image_claims[0]["mainsnak"]["datavalue"]["value"]

def save_webp(url, out_path):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    img = Image.open(BytesIO(r.content)).convert("RGB")
    img.thumbnail((512, 512))

    canvas = Image.new("RGB", (512, 512), "#f1f5f9")
    x = (512 - img.width) // 2
    y = (512 - img.height) // 2
    canvas.paste(img, (x, y))

    canvas.save(out_path, "WEBP", quality=88, method=6)

def main():
    df = pd.read_csv(PLAYER_LIST)
    audit_rows = []

    for _, row in df.iterrows():
        name = str(row["player_name"])
        slug = str(row["slug"])
        out_file = OUT_DIR / f"{slug}.webp"

        status = "not_found"
        qid = ""
        source_image = ""
        error = ""

        try:
            
            search_terms = ALIASES.get(name, [name])
            results = []
            for term in search_terms:
                results.extend(wiki_search(term))


            for candidate in results:
                qid_candidate = candidate.get("id", "")
                label = candidate.get("label", "")
                desc = candidate.get("description", "")

                # Filtro blando: buscamos humanos/futbolistas, pero sin romper si la descripción varía.
                if not qid_candidate:
                    continue

                entity = wikidata_entity(qid_candidate)
                filename = get_commons_image_from_entity(entity)

                if filename:
                    qid = qid_candidate
                    source_image = filename
                    url = commons_image_url(filename)
                    save_webp(url, out_file)
                    status = "downloaded"
                    break

                time.sleep(0.2)

        except Exception as e:
            status = "error"
            error = str(e)

        audit_rows.append({
            "player_name": name,
            "slug": slug,
            "image_file": f"{slug}.webp",
            "status": status,
            "wikidata_qid": qid,
            "source_image": source_image,
            "local_path": str(out_file) if out_file.exists() else "",
            "error": error,
        })

        print(f"{name}: {status}")
        time.sleep(0.5)

    pd.DataFrame(audit_rows).to_csv(AUDIT, index=False, encoding="utf-8-sig")
    print(f"\nAudit saved: {AUDIT}")

if __name__ == "__main__":
    main()
