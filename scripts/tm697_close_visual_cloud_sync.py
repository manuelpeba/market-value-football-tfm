from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_close_visual_cloud_sync").write_text(s, encoding="utf-8")

# 1) Búsqueda global: usar football_df también para typeahead.
s = s.replace(
    "candidate_results = rank_global_command_search(base_df, query_value_state, search_options, search_label_to_raw, max_results=5)",
    "candidate_results = rank_global_command_search(football_df, query_value_state, search_options, search_label_to_raw, max_results=5)"
)

# 2) Player Snapshot: quitar Contexto para no duplicar competición y liberar ancho.
s = s.replace(
'''                    <div><span>{html.escape(lbl_age)}</span><b>{html.escape(age_display)} {html.escape(age_suffix)}</b></div>
                    <div><span>{html.escape(lbl_position)}</span><b>{html.escape(position_badge)}</b></div>
                    <div><span>{html.escape(lbl_context)}</span><b>{html.escape(league)}</b></div>''',
'''                    <div><span>{html.escape(lbl_age)}</span><b>{html.escape(age_display)} {html.escape(age_suffix)}</b></div>
                    <div><span>{html.escape(lbl_position)}</span><b>{html.escape(position_badge)}</b></div>''',
1
)

# 3) Role DNA: hacer clicables los botones de intención.
old = '''    st.markdown(
        f"<div class='role-dna-filter-shell'><div class='role-dna-filter-title'>{html.escape(title)}</div><div class='role-dna-filter-subtitle'>{html.escape(subtitle)}</div><div class='role-dna-filter-intents'>{chips_html}</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(available), gap="small")'''

new = '''    st.markdown(
        f"<div class='role-dna-filter-shell'><div class='role-dna-filter-title'>{html.escape(title)}</div><div class='role-dna-filter-subtitle'>{html.escape(subtitle)}</div>",
        unsafe_allow_html=True,
    )

    intent_rules = [
        ("🛡 Construcción desde atrás" if LANG == "ES" else "🛡 Build-up from deep", {"ball_progression_index": 60, "passing_security_index": 55}),
        ("🎨 Creación ofensiva" if LANG == "ES" else "🎨 Offensive creation", {"chance_creation_index": 60, "ball_progression_index": 50}),
        ("⚙ Seguridad en posesión" if LANG == "ES" else "⚙ Possession security", {"passing_security_index": 65}),
        ("🏃 Disponibilidad competitiva" if LANG == "ES" else "🏃 Competitive availability", {"availability_index_role": 65}),
    ]
    btn_cols = st.columns(len(intent_rules), gap="small")
    for bidx, (label, rules) in enumerate(intent_rules):
        with btn_cols[bidx]:
            if st.button(label, key=f"{key_prefix}_intent_{bidx}", use_container_width=True):
                for c in ROLE_DNA_FILTER_COLUMNS:
                    st.session_state[f"{key_prefix}_{c}_min_filter"] = int(rules.get(c, 0))

    st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(len(available), gap="small")'''

if old not in s:
    print("WARN: no se encontró bloque exacto Role DNA clickable")
else:
    s = s.replace(old, new, 1)

# 4) Role DNA number_input: leer valor desde session_state.
s = s.replace(
'''                value=0,
                step=5,
                key=f"{key_prefix}_{col}_min_filter",''',
'''                value=int(st.session_state.get(f"{key_prefix}_{col}_min_filter", 0)),
                step=5,
                key=f"{key_prefix}_{col}_min_filter",''',
1
)

# 5) CSS final snapshot: 2 columnas en meta grid + cards role buttons consistentes.
css = r'''
<style>
/* TM.6.9.7 CLOSE — Cloud visual sync */
.snapshot-identity-layout .snapshot-meta-grid,
.snapshot-card.snapshot-card-identity .snapshot-meta-grid {
    grid-template-columns: 0.8fr 1.2fr !important;
    gap: 18px !important;
}
.snapshot-identity-layout .snapshot-meta-grid div,
.snapshot-identity-layout .snapshot-meta-grid b,
.snapshot-card.snapshot-card-identity .snapshot-meta-grid div,
.snapshot-card.snapshot-card-identity .snapshot-meta-grid b {
    min-width: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
.role-dna-filter-shell + div[data-testid="stHorizontalBlock"] button {
    border-radius: 14px !important;
    border: 1px solid #bfdbfe !important;
    background: #ffffff !important;
    color: #0f2f5f !important;
    font-weight: 900 !important;
    min-height: 46px !important;
}
.role-dna-filter-shell + div[data-testid="stHorizontalBlock"] button:hover {
    background: #eff6ff !important;
    border-color: #2563eb !important;
}
</style>
'''
if "TM.6.9.7 CLOSE — Cloud visual sync" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK TM.6.9.7 Cloud sync closure")
