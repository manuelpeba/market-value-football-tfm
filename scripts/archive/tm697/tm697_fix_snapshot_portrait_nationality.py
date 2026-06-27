from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_fix_snapshot_portrait_nationality").write_text(s, encoding="utf-8")

# 1) Sustituir helper antiguo _siq_player_portrait_html: antes solo Javi tenía foto
new_helper = r'''
def _siq_asset_to_data_uri_safe(rel_path: str) -> str:
    try:
        import base64
        path = ROOT / "app" / "assets" / rel_path
        if not path.exists():
            return ""
        suffix = path.suffix.lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".avif": "image/avif",
            ".svg": "image/svg+xml",
        }.get(suffix, "image/png")
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


def _siq_slug_player_name(player_name: object) -> str:
    import unicodedata, re
    x = unicodedata.normalize("NFKD", str(player_name or ""))
    x = "".join(c for c in x if not unicodedata.combining(c))
    x = x.lower()
    return re.sub(r"[^a-z0-9]+", "_", x).strip("_")


def _siq_player_portrait_html(player_name: object, css_class: str = "snapshot-player-photo") -> str:
    """Real portrait when local asset exists; default silhouette otherwise."""
    slug = _siq_slug_player_name(player_name)

    aliases = {
        "javirodriguez": "javi_rodriguez",
        "javi_rodriguez": "javi_rodriguez",
        "christantusuche": "christantus_uche",
        "christantus_uche": "christantus_uche",
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
        uri = _siq_asset_to_data_uri_safe(rel)
        if uri:
            alt = html.escape(str(player_name or "Player"))
            return f"<div class='{css_class}'><img src='{html.escape(uri)}' alt='{alt}' loading='lazy'></div>"

    initials = "".join([x[:1] for x in str(player_name or "PI").split()[:2]]).upper() or "PI"
    return f"<div class='{css_class} snapshot-player-fallback'>{html.escape(initials)}</div>"
'''

s = re.sub(
    r'def _siq_asset_to_data_uri_safe\(rel_path: str\) -> str:\n.*?\ndef _siq_player_portrait_html\(player_name: object, css_class: str = "snapshot-player-photo"\) -> str:\n.*?return f"<div class=\'\{css_class\}\'><img src=\'\{html\.escape\(uri\)\}\' alt=\'\{alt\}\' loading=\'lazy\'></div>"\n',
    new_helper + "\n",
    s,
    flags=re.S,
    count=1
)

# 2) Añadir fallback duro de nacionalidad a _tm69_row_nationality
s = s.replace(
'''    key = normalize_search_text(player_name or row_dict.get("player_name_fbref", "") or row_dict.get("player_name_display", ""))
    return _tm69_player_nationality_lookup().get(key, "")''',
'''    key = normalize_search_text(player_name or row_dict.get("player_name_fbref", "") or row_dict.get("player_name_display", ""))
    compact_key = key.replace(" ", "").replace("_", "").replace("-", "")

    nationality_overrides = {
        "christantusuche": "Nigeria",
        "javirodriguez": "España",
        "javi rodriguez": "España",
        "sabagoglichidze": "Georgia",
        "lucamarianucci": "Italia",
        "rabbynzingoula": "Francia",
        "mariomartin": "España",
    }

    if compact_key in nationality_overrides:
        return nationality_overrides[compact_key]

    return _tm69_player_nationality_lookup().get(key, "")''',
    1
)

# 3) CSS específico para que el retrato de Player Snapshot no quede tapado por reglas antiguas
css = r'''
<style>
/* TM.6.9.7 — Player Snapshot portrait + nationality fix */
.snapshot-player-photo {
    display: flex !important;
    width: 118px !important;
    height: 148px !important;
    min-width: 118px !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    background: #eef2f7 !important;
    border: 1px solid #dbeafe !important;
    box-shadow: 0 10px 24px rgba(15,23,42,.08) !important;
    align-items: center !important;
    justify-content: center !important;
}
.snapshot-player-photo img {
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top !important;
}
.snapshot-identity-assets {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
}
</style>
'''
if "TM.6.9.7 — Player Snapshot portrait + nationality fix" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK: Player Snapshot usa imagen local real + fallback nacionalidad")
