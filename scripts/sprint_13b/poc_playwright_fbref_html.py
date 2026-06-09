from pathlib import Path
import time
import pandas as pd
from playwright.sync_api import sync_playwright


OUT_DIR = Path("data/raw/fbref/sprint_13b/html")
REPORT_DIR = Path("reports/sprint_13b")
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TEST_URLS = [
    {
        "dataset": "shooting",
        "league": "premier_league",
        "season": "2025_2026",
        "url": "https://fbref.com/en/comps/9/shooting/Premier-League-Stats",
        "filename": "fbref_shooting_premier_league_2025_2026.html",
    },
    {
        "dataset": "passing",
        "league": "premier_league",
        "season": "2025_2026",
        "url": "https://fbref.com/en/comps/9/passing/Premier-League-Stats",
        "filename": "fbref_passing_premier_league_2025_2026.html",
    },
    {
        "dataset": "possession",
        "league": "premier_league",
        "season": "2025_2026",
        "url": "https://fbref.com/en/comps/9/possession/Premier-League-Stats",
        "filename": "fbref_possession_premier_league_2025_2026.html",
    },
    {
        "dataset": "gca",
        "league": "premier_league",
        "season": "2025_2026",
        "url": "https://fbref.com/en/comps/9/gca/Premier-League-Stats",
        "filename": "fbref_gca_premier_league_2025_2026.html",
    },
]

rows = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    )

    for item in TEST_URLS:
        dataset_dir = OUT_DIR / item["dataset"]
        dataset_dir.mkdir(parents=True, exist_ok=True)
        out_path = dataset_dir / item["filename"]

        print(f"\nOpening {item['url']}")

        try:
            response = page.goto(
                item["url"],
                wait_until="domcontentloaded",
                timeout=60000,
            )

            time.sleep(8)

            status_code = response.status if response else None
            html = page.content()

            out_path.write_text(html, encoding="utf-8")

            rows.append(
                {
                    **item,
                    "status": "ok",
                    "http_status": status_code,
                    "html_chars": len(html),
                    "output_path": str(out_path),
                    "error": "",
                }
            )

            print(f"Saved {out_path} | status={status_code} | chars={len(html)}")

            time.sleep(20)

        except Exception as exc:
            rows.append(
                {
                    **item,
                    "status": "error",
                    "http_status": None,
                    "html_chars": None,
                    "output_path": "",
                    "error": repr(exc),
                }
            )
            print(f"ERROR: {repr(exc)}")

    browser.close()

audit = pd.DataFrame(rows)
audit_path = REPORT_DIR / "poc_playwright_fbref_html_results.csv"
audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

print("\nSaved:", audit_path)
print(audit)