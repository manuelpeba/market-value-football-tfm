from __future__ import annotations

from pathlib import Path
import base64
import html
import mimetypes
import re
import unicodedata

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parents[2]

VISUAL_MANIFEST_PATH = (
    ROOT / "reports" / "visual_identity" / "tm6_9a_top30_visual_mvp_manifest.csv"
)

PLAYERS_ASSETS_DIR = ROOT / "app" / "assets" / "players"
CLUBS_ASSETS_DIR = ROOT / "app" / "assets" / "clubs"
FLAGS_ASSETS_DIR = ROOT / "app" / "assets" / "flags"


COUNTRY_TO_ISO2 = {
    "argentina": "ar",
    "austria": "at",
    "belgium": "be",
    "brazil": "br",
    "croatia": "hr",
    "denmark": "dk",
    "england": "gb-eng",
    "france": "fr",
    "germany": "de",
    "ghana": "gh",
    "italy": "it",
    "ivory coast": "ci",
    "cote d'ivoire": "ci",
    "côte d’ivoire": "ci",
    "netherlands": "nl",
    "nigeria": "ng",
    "norway": "no",
    "portugal": "pt",
    "senegal": "sn",
    "serbia": "rs",
    "spain": "es",
    "switzerland": "ch",
    "turkey": "tr",
    "united states": "us",
    "uruguay": "uy",
}


CLUB_DISPLAY_MAP = {
    "Celta de Vigo": "Celta Vigo",
    "RCD Espanyol Barcelona": "Espanyol",
    "RC Strasbourg Alsace": "Strasbourg",
    "Athletic Club": "Athletic Bilbao",
    "Athletic Bilbao": "Athletic Bilbao",
    "Crystal Palace FC": "Crystal Palace",
    "Crystal Palace": "Crystal Palace",
    "AJ Auxerre": "Auxerre",
    "Angers SCO": "Angers SCO",
    "Getafe CF": "Getafe",
}


@st.cache_data(show_spinner=False)
def load_visual_mvp_manifest() -> pd.DataFrame:
    if not VISUAL_MANIFEST_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(VISUAL_MANIFEST_PATH)


def _safe_text(value, fallback: str = "N/A") -> str:
    if value is None:
        return fallback
    try:
        if pd.isna(value):
            return fallback
    except Exception:
        pass
    value = str(value).strip()
    return value if value else fallback


def _fmt_score(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):.1f}"
    except Exception:
        return "—"


def _score_float(value) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def _fmt_money(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        value = float(value)
        if value >= 1_000_000:
            return f"€{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"€{value / 1_000:.0f}K"
        return f"€{value:,.0f}"
    except Exception:
        return "—"


def _slugify(value) -> str:
    value = _safe_text(value, "").lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _initials(name: str) -> str:
    parts = [p for p in str(name).split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def _asset_data_uri(path: Path | str | None) -> str | None:
    if path is None:
        return None
    path = Path(path)
    if not path.exists() or not path.is_file():
        return None
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "image/png"
    try:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return None


def _find_asset(directory: Path, stem: str | int | float | None, extensions=("png", "svg", "jpg", "jpeg", "webp")) -> Path | None:
    if stem is None:
        return None
    try:
        if pd.isna(stem):
            return None
    except Exception:
        pass
    stem = str(stem).replace(".0", "").strip()
    if not stem:
        return None
    for ext in extensions:
        path = directory / f"{stem}.{ext}"
        if path.exists():
            return path
    return None


def resolve_player_image(player_id_tm) -> str | None:
    path = _find_asset(PLAYERS_ASSETS_DIR, player_id_tm, extensions=("jpg", "jpeg", "png", "webp"))
    return _asset_data_uri(path)


def resolve_club_logo(club: str) -> str | None:
    club = CLUB_DISPLAY_MAP.get(_safe_text(club, ""), _safe_text(club, ""))
    candidates = {_slugify(club)}
    candidates.add(_slugify(club.replace(" FC", "").replace(" CF", "")))
    for candidate in candidates:
        path = _find_asset(CLUBS_ASSETS_DIR, candidate, extensions=("png", "svg", "jpg", "jpeg", "webp"))
        uri = _asset_data_uri(path)
        if uri:
            return uri
    return None


def resolve_flag(country: str) -> str | None:
    country_key = _slugify(country).replace("_", " ")
    iso = COUNTRY_TO_ISO2.get(country_key) or COUNTRY_TO_ISO2.get(country_key.split("/")[0].strip())
    if not iso:
        return None
    path = _find_asset(FLAGS_ASSETS_DIR, iso, extensions=("svg", "png", "jpg", "jpeg", "webp"))
    return _asset_data_uri(path)


def _player_name(row) -> str:
    return _safe_text(
        row.get("player")
        or row.get("player_name_tm")
        or row.get("player_name_fbref")
        or row.get("name"),
        "Unknown player",
    )


def _club(row) -> str:
    raw = _safe_text(
        row.get("display_club")
        or row.get("current_club")
        or row.get("club")
        or row.get("team"),
        "N/A",
    )
    return CLUB_DISPLAY_MAP.get(raw, raw)


def _league(row) -> str:
    return _safe_text(row.get("display_league") or row.get("current_league") or row.get("league"), "N/A")


def _position(row) -> str:
    return _safe_text(row.get("position") or row.get("position_group"), "N/A")


def _country(row) -> str:
    return _safe_text(
        row.get("country_of_citizenship")
        or row.get("nationality")
        or row.get("country")
        or row.get("citizenship"),
        "",
    )


def _tier_label(score: float | None) -> tuple[str, str]:
    if score is None:
        return "Watchlist", "tier-neutral"
    if score >= 90:
        return "High Priority", "tier-elite"
    if score >= 80:
        return "High Priority", "tier-high"
    if score >= 70:
        return "Active Watch", "tier-watch"
    return "Monitor", "tier-neutral"


def render_visual_mvp_cards(df: pd.DataFrame | None = None, limit: int = 10):
    """Render compact Visual MVP cards for the Executive Overview.

    The component is intentionally self-contained through components.html to avoid
    Streamlit Markdown escaping issues and to make the card grid stable in exports.
    """
    if df is None:
        df = load_visual_mvp_manifest()

    if df.empty:
        st.warning("No se ha encontrado el manifest visual TM.6.9a.")
        return

    df = df.head(limit).copy()

    css = """
    <style>
    body {
        margin: 0;
        background: transparent;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .visual-mvp-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        padding: 2px 2px 10px 2px;
        box-sizing: border-box;
    }
    .visual-mvp-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 11px 12px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.050);
        min-height: 142px;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }
    .visual-mvp-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #2563eb, #60a5fa);
    }
    .visual-mvp-head {
        display: grid;
        grid-template-columns: 58px minmax(0, 1fr) auto;
        gap: 10px;
        align-items: center;
    }
    .visual-mvp-photo {
        width: 54px;
        height: 54px;
        border-radius: 14px;
        overflow: hidden;
        background: linear-gradient(135deg, #0b2545, #2563eb);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 950;
        font-size: 1.00rem;
        flex-shrink: 0;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.14);
    }
    .visual-mvp-photo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .visual-mvp-rank {
        color: #2563eb;
        font-size: 0.62rem;
        font-weight: 950;
        letter-spacing: .065em;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .visual-mvp-name-row {
        display: flex;
        align-items: center;
        gap: 6px;
        min-width: 0;
    }
    .visual-mvp-name {
        color: #0f172a;
        font-size: 0.94rem;
        font-weight: 950;
        line-height: 1.08;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .visual-mvp-flag,
    .visual-mvp-club-logo {
        width: 18px;
        height: 18px;
        border-radius: 999px;
        object-fit: cover;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        flex-shrink: 0;
    }
    .visual-mvp-club-logo {
        border-radius: 6px;
        width: 20px;
        height: 20px;
        padding: 1px;
    }
    .visual-mvp-meta {
        color: #64748b;
        font-size: 0.70rem;
        line-height: 1.28;
        margin-top: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .visual-mvp-price {
        text-align: right;
        color: #0f172a;
        font-size: 0.92rem;
        font-weight: 950;
        white-space: nowrap;
    }
    .visual-mvp-price span {
        display: block;
        color: #64748b;
        font-size: 0.58rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .05em;
        margin-bottom: 2px;
    }
    .visual-mvp-kpis {
        display: grid;
        grid-template-columns: 1.1fr .95fr .95fr;
        gap: 7px;
        margin-top: 10px;
    }
    .visual-mvp-kpi {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 11px;
        padding: 7px 8px;
        min-height: 43px;
    }
    .visual-mvp-kpi-label {
        color: #64748b;
        font-size: 0.55rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .04em;
        line-height: 1.05;
    }
    .visual-mvp-kpi-value {
        color: #0f172a;
        font-size: 0.94rem;
        font-weight: 950;
        line-height: 1.0;
        margin-top: 4px;
    }
    .visual-mvp-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-top: 9px;
    }
    .visual-mvp-tier {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 4px 8px;
        font-size: 0.62rem;
        font-weight: 950;
        white-space: nowrap;
    }
    .tier-elite { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .tier-high { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .tier-watch { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .tier-neutral { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
    .visual-mvp-action {
        color: #1e3a8a;
        background: #eff6ff;
        border: 1px solid #dbeafe;
        border-radius: 999px;
        padding: 4px 8px;
        font-size: 0.61rem;
        font-weight: 950;
        white-space: nowrap;
    }
    @media (max-width: 1150px) {
        .visual-mvp-grid { grid-template-columns: 1fr; }
    }
    </style>
    """

    cards = ["<div class='visual-mvp-grid'>"]

    for _, row in df.iterrows():
        player = _player_name(row)
        club = _club(row)
        league = _league(row)
        position = _position(row)
        country = _country(row)
        rank = int(row.get("visual_rank", 0)) if pd.notna(row.get("visual_rank", 0)) else 0
        opportunity = _score_float(row.get("opportunity_score"))
        tier_text, tier_class = _tier_label(opportunity)

        player_img = resolve_player_image(row.get("player_id_tm"))
        club_logo = resolve_club_logo(club)
        flag = resolve_flag(country)

        if player_img:
            photo_html = f"<img src='{player_img}' alt='{html.escape(player)}'>"
        else:
            photo_html = html.escape(_initials(player))

        flag_html = f"<img class='visual-mvp-flag' src='{flag}' alt='{html.escape(country)}'>" if flag else ""
        logo_html = f"<img class='visual-mvp-club-logo' src='{club_logo}' alt='{html.escape(club)}'>" if club_logo else ""

        cards.append(
            f"""
            <div class="visual-mvp-card">
                <div class="visual-mvp-head">
                    <div class="visual-mvp-photo">{photo_html}</div>
                    <div style="min-width:0;">
                        <div class="visual-mvp-rank">Visual MVP #{rank}</div>
                        <div class="visual-mvp-name-row">
                            <div class="visual-mvp-name">{html.escape(player)}</div>
                            {flag_html}
                            {logo_html}
                        </div>
                        <div class="visual-mvp-meta">
                            {html.escape(club)} · {html.escape(league)} · {html.escape(position)}
                        </div>
                    </div>
                    <div class="visual-mvp-price"><span>Value</span>{_fmt_money(row.get("market_value_eur"))}</div>
                </div>

                <div class="visual-mvp-kpis">
                    <div class="visual-mvp-kpi">
                        <div class="visual-mvp-kpi-label">Opportunity</div>
                        <div class="visual-mvp-kpi-value">{_fmt_score(row.get("opportunity_score"))}</div>
                    </div>
                    <div class="visual-mvp-kpi">
                        <div class="visual-mvp-kpi-label">Contract</div>
                        <div class="visual-mvp-kpi-value">{_fmt_score(row.get("contract_opportunity_score"))}</div>
                    </div>
                    <div class="visual-mvp-kpi">
                        <div class="visual-mvp-kpi-label">Recruitment</div>
                        <div class="visual-mvp-kpi-value">{_fmt_score(row.get("recruitment_contract_score"))}</div>
                    </div>
                </div>

                <div class="visual-mvp-footer">
                    <span class="visual-mvp-tier {tier_class}">{html.escape(tier_text)}</span>
                    <span class="visual-mvp-action">Open profile →</span>
                </div>
            </div>
            """
        )

    cards.append("</div>")

    html_block = css + "\n".join(cards)
    rows = (len(df) + 1) // 2
    height = 176 * rows + 18
    components.html(html_block, height=max(height, 520), scrolling=False)
