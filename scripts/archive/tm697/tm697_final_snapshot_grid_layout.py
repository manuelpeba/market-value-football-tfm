from pathlib import Path

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_final_snapshot_grid_layout").write_text(s, encoding="utf-8")

css = r'''
<style>
/* TM.6.9.7 FINAL — Player Snapshot identity grid layout */
.snapshot-card.snapshot-card-identity {
    display: grid !important;
    grid-template-columns: 118px minmax(0, 1fr) !important;
    column-gap: 18px !important;
    align-items: start !important;
    overflow: hidden !important;
    padding: 22px 24px !important;
}

.snapshot-card.snapshot-card-identity > .snapshot-player-photo {
    grid-column: 1 !important;
    grid-row: 1 !important;
    float: none !important;
    width: 108px !important;
    height: 138px !important;
    min-width: 108px !important;
    max-width: 108px !important;
    margin: 18px 0 0 0 !important;
    border-radius: 20px !important;
    position: relative !important;
    z-index: 1 !important;
}

.snapshot-card.snapshot-card-identity > .snapshot-player-photo img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top !important;
    display: block !important;
}

.snapshot-card.snapshot-card-identity > .snapshot-identity-main {
    grid-column: 2 !important;
    grid-row: 1 !important;
    min-width: 0 !important;
    max-width: 100% !important;
    position: relative !important;
    z-index: 2 !important;
}

.snapshot-card.snapshot-card-identity .snapshot-identity-assets {
    margin: 12px 0 12px 0 !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
    justify-content: flex-start !important;
}

.snapshot-card.snapshot-card-identity .snapshot-position-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
    justify-content: flex-start !important;
}

.snapshot-card.snapshot-card-identity .snapshot-meta-grid {
    margin-top: 12px !important;
    display: grid !important;
    grid-template-columns: 0.75fr 1fr 1fr !important;
    gap: 14px !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

.snapshot-card.snapshot-card-identity .snapshot-meta-grid div,
.snapshot-card.snapshot-card-identity .snapshot-meta-grid b {
    min-width: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

/* Neutraliza hacks anteriores */
.snapshot-identity-assets,
.pi-identity-assets,
.pi-chip-row {
    margin-left: 0 !important;
}
.snapshot-identity-assets + *,
.pi-identity-assets + *,
.pi-chip-row + * {
    margin-left: 0 !important;
}
</style>
'''

if "TM.6.9.7 FINAL — Player Snapshot identity grid layout" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK: final grid layout aplicado")
