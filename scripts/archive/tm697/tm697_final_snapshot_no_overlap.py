from pathlib import Path

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_final_snapshot_no_overlap").write_text(s, encoding="utf-8")

css = r'''
<style>
/* TM.6.9.7 FINAL — no overlap in Player Snapshot identity card */
.snapshot-player-photo {
    float: left !important;
    width: 92px !important;
    height: 120px !important;
    min-width: 92px !important;
    max-width: 92px !important;
    margin: 6px 20px 12px 0 !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    position: relative !important;
    z-index: 1 !important;
}

.snapshot-player-photo img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top !important;
    display: block !important;
}

.snapshot-identity-assets,
.pi-identity-assets,
.pi-chip-row {
    margin-left: 112px !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
}

.snapshot-identity-assets + *,
.pi-identity-assets + *,
.pi-chip-row + * {
    margin-left: 112px !important;
}

/* La fila inferior queda debajo de la imagen */
.snapshot-identity-metrics,
.pi-snapshot-metrics {
    clear: both !important;
    margin-top: 14px !important;
}
</style>
'''

if "TM.6.9.7 FINAL — no overlap in Player Snapshot identity card" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK: no-overlap final CSS applied")
