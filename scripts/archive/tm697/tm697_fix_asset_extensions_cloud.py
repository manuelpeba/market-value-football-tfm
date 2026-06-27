from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_asset_extensions_cloud").write_text(s, encoding="utf-8")

# 1) Añadir soporte AVIF y resolver extensiones reales
s = s.replace(
'''".webp": "image/webp",
        ".svg": "image/svg+xml",''',
'''".webp": "image/webp",
        ".avif": "image/avif",
        ".svg": "image/svg+xml",'''
)

# 2) Asegurar búsqueda de todas las extensiones usadas
s = re.sub(
r'''for rel in \[
        f"players/\{slug\}\.png",
        f"players/\{slug\}\.jpg",
        f"players/\{slug\}\.jpeg",
        f"players/\{slug\}\.webp",
        "defaults/default_player\.webp",
    \]:''',
'''for rel in [
        f"players/{slug}.png",
        f"players/{slug}.jpg",
        f"players/{slug}.jpeg",
        f"players/{slug}.webp",
        f"players/{slug}.avif",
        "defaults/default_player.webp",
    ]:''',
s
)

p.write_text(s, encoding="utf-8")
print("OK: extensiones de imagen ampliadas para Cloud")
