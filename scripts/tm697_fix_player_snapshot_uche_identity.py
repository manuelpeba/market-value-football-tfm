from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_fix_player_snapshot_uche_identity").write_text(s, encoding="utf-8")

block = r'''
# ============================================================
# TM.6.9.7 — Player Snapshot identity hardening
# ============================================================
def _tm697_safe_asset_data_uri(rel_path: str) -> str:
    try:
        import base64
        path = ROOT / "app" / "assets" / rel_path
        if not path.exists():
            return ""
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".avif": "image/avif",
            ".svg": "image/svg+xml",
        }.get(path.suffix.lower(), "image/png")
        return "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    except Exception:
        return ""

def _tm697_slug_player(name: object) -> str:
    import unicodedata, re
    x = unicodedata.normalize("NFKD", str(name or ""))
    x = "".join(c for c in x if not unicodedata.combining(c))
    x = x.lower()
    return re.sub(r"[^a-z0-9]+", "_", x).strip("_")

def _tm697_player_image_uri(player_name: object) -> str:
    slug = _tm697_slug_player(player_name)

    aliases = {
        "javi_rodriguez": "javi_rodriguez",
        "javirodriguez": "javi_rodriguez",
        "christantus_uche": "christantus_uche",
        "christantusuche": "christantus_uche",
        "mario_martin": "mario_martin",
        "saba_goglichidze": "saba_goglichidze",
        "luca_marianucci": "luca_marianucci",
        "rabby_nzingoula": "rabby_nzingoula",
    }

    slug = aliases.get(slug, slug)

    for rel in [
        f"players/{slug}.png",
        f"players/{slug}.jpg",
        f"players/{slug}.jpeg",
        f"players/{slug}.webp",
        f"players/{slug}.avif",
        "defaults/default_player.webp",
    ]:
        uri = _tm697_safe_asset_data_uri(rel)
        if uri:
            return uri
    return ""

def _tm69_player_avatar_html(ctx: dict, player_name: str) -> str:
    """Final active resolver: real player image when available, default silhouette otherwise."""
    uri = _tm697_player_image_uri(player_name)
    if uri:
        return f"<div class='pi-player-photo'><img src='{html.escape(uri)}' alt='{html.escape(str(player_name or 'Player'))}'></div>"
    return ""

_TM697_NATIONALITY_OVERRIDES = {
    "christantus_uche": "Nigeria",
    "christantusuche": "Nigeria",
    "javi_rodriguez": "España",
    "javirodriguez": "España",
}

def _tm697_player_nationality_fallback(player_name: object, current_value: object = "") -> str:
    current = str(current_value or "").strip()
    if current and current.lower() not in {"nan", "none", "null", "n/a", "na"}:
        return current
    slug = _tm697_slug_player(player_name)
    return _TM697_NATIONALITY_OVERRIDES.get(slug, "")
'''

# Eliminar bloques antiguos del mismo resolver para evitar sombras
s = re.sub(
    r'\n# ============================================================\n# TM\.6\.9\.7 — Player Snapshot identity hardening.*?(?=\n# ============================================================|\ndef |\n[A-Z_]+\s*=|\nst\.markdown|\Z)',
    "\n",
    s,
    flags=re.S
)

# Sustituir todas las definiciones activas de avatar
s = re.sub(
    r'def _tm69_player_avatar_html\(ctx: dict, player_name: str\) -> str:\n(?:    .*\n)+?(?=\ndef |\n# |\n[A-Z_]+\s*=|\nst\.markdown|\Z)',
    '''def _tm69_player_avatar_html(ctx: dict, player_name: str) -> str:
    uri = _tm697_player_image_uri(player_name) if "_tm697_player_image_uri" in globals() else ""
    if uri:
        return f"<div class='pi-player-photo'><img src='{html.escape(uri)}' alt='{html.escape(str(player_name or 'Player'))}'></div>"
    return ""
''',
    s,
    flags=re.M
)

# Insertar bloque antes de Player Intelligence para que esté definido antes de render
anchor = "def render_tm69_executive_summary_tab"
if anchor in s and "TM.6.9.7 — Player Snapshot identity hardening" not in s:
    s = s.replace(anchor, block + "\n\n" + anchor, 1)
elif "TM.6.9.7 — Player Snapshot identity hardening" not in s:
    s = block + "\n\n" + s

# Forzar fallback de nacionalidad en cualquier asignación country/nationality típica
s = re.sub(
    r'(country_raw\s*=\s*_tm69_row_nationality\(row,\s*player_raw\))',
    r'\1\n        country_raw = _tm697_player_nationality_fallback(player_raw, country_raw) if "_tm697_player_nationality_fallback" in globals() else country_raw',
    s
)

s = re.sub(
    r'(nationality_raw\s*=\s*_tm69_row_nationality\(row,\s*player_name\))',
    r'\1\n    nationality_raw = _tm697_player_nationality_fallback(player_name, nationality_raw) if "_tm697_player_nationality_fallback" in globals() else nationality_raw',
    s
)

# CSS para que la foto no vuelva a quedar tapada por reglas antiguas
css = r'''
<style>
/* TM.6.9.7 — Player Snapshot Uche identity fix */
.pi-player-photo {
    display: flex !important;
    width: 96px !important;
    height: 124px !important;
    min-width: 96px !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    background: #eef2f7 !important;
    border: 1px solid #dbeafe !important;
    box-shadow: 0 12px 26px rgba(15,23,42,.12) !important;
    align-items: center !important;
    justify-content: center !important;
}
.pi-player-photo img {
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top !important;
}
.pi-visual-stack {
    min-width: 112px !important;
}
</style>
'''
if "TM.6.9.7 — Player Snapshot Uche identity fix" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK: Player Snapshot Uche image + nationality fallback patched")
