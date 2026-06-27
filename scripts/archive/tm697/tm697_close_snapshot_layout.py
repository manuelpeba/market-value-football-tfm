from pathlib import Path

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_close_snapshot_layout").write_text(s, encoding="utf-8")

css = r'''
<style>
/* TM.6.9.7 — Sprint closure: Player Snapshot image layout */
.snapshot-identity-card,
.player-snapshot-identity-card,
.pi-snapshot-identity-card {
    overflow: hidden !important;
}

.snapshot-identity-row,
.player-snapshot-identity-row,
.pi-snapshot-identity-row {
    display: grid !important;
    grid-template-columns: 118px minmax(0, 1fr) !important;
    column-gap: 20px !important;
    align-items: start !important;
}

.snapshot-player-photo,
.pi-player-photo {
    width: 112px !important;
    height: 144px !important;
    min-width: 112px !important;
    max-width: 112px !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    margin: 0 !important;
    position: relative !important;
    z-index: 1 !important;
}

.snapshot-player-photo img,
.pi-player-photo img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top !important;
    display: block !important;
}

.snapshot-identity-content,
.player-snapshot-identity-content,
.pi-snapshot-identity-content {
    min-width: 0 !important;
    position: relative !important;
    z-index: 2 !important;
    padding-left: 6px !important;
}

.snapshot-identity-assets,
.pi-identity-assets,
.pi-chip-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
    max-width: 100% !important;
}

/* Evita que el bloque inferior invada la zona de imagen */
.snapshot-identity-metrics,
.pi-snapshot-metrics {
    clear: both !important;
    margin-top: 14px !important;
}
</style>
'''

if "TM.6.9.7 — Sprint closure: Player Snapshot image layout" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK: snapshot layout closure CSS applied")
