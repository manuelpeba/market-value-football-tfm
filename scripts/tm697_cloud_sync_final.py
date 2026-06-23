from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_cloud_sync_final").write_text(s, encoding="utf-8")

# 1) Role Intelligence: permitir CSV además de Parquet
s = s.replace(
'''        ROOT / "reports" / "dss" / "player_role_dss.parquet",
        ROOT / "reports" / "tm5_role_intelligence" / "player_role_dss.parquet",
        ROOT / "reports" / "role_intelligence" / "player_role_dss.parquet",''',
'''        ROOT / "reports" / "dss" / "player_role_dss.parquet",
        ROOT / "reports" / "player_role_dss.csv",
        ROOT / "reports" / "player_role_intelligence.csv",
        ROOT / "reports" / "roles" / "player_role_labels.csv",
        ROOT / "reports" / "roles" / "player_role_dna.csv",
        ROOT / "reports" / "tm5_role_intelligence" / "player_role_dss.parquet",
        ROOT / "reports" / "role_intelligence" / "player_role_dss.parquet",'''
)

s = s.replace(
'''    patterns = ["player_role_labels*.parquet", "player_role_dss*.parquet", "*role*dss*.parquet", "*role*intelligence*.parquet"]''',
'''    patterns = ["player_role_labels*.parquet", "player_role_dss*.parquet", "*role*dss*.parquet", "*role*intelligence*.parquet", "player_role_labels*.csv", "player_role_dss*.csv", "*role*dss*.csv", "*role*intelligence*.csv"]'''
)

s = s.replace(
'''    role_df = pd.read_parquet(resolved_path).copy()''',
'''    if resolved_path.suffix.lower() == ".csv":
        role_df = pd.read_csv(resolved_path, low_memory=False).copy()
    else:
        role_df = pd.read_parquet(resolved_path).copy()'''
)

# 2) Football lookup: incluir snapshot actual para jugadores fuera del scouting universe, ej. Lamine Yamal
s = s.replace(
'''    lookup_candidates = [
        "player_season_panel.parquet",
        "player_season_modeling.parquet",''',
'''    lookup_candidates = [
        "current_player_snapshot.parquet",
        "transfermarkt_current_snapshot.parquet",
        "player_season_panel.parquet",
        "player_season_modeling.parquet",'''
)

# 3) Global search: ranking/typeahead debe buscar en football_df, no en base_df
s = re.sub(
    r'candidate_results\s*=\s*rank_global_command_search\(base_df,',
    'candidate_results = rank_global_command_search(football_df,',
    s
)

# 4) Snapshot: eliminar Contexto duplicado
s = s.replace(
'''                    <div><span>{html.escape(lbl_age)}</span><b>{html.escape(age_display)} {html.escape(age_suffix)}</b></div>
                    <div><span>{html.escape(lbl_position)}</span><b>{html.escape(position_badge)}</b></div>
                    <div><span>{html.escape(lbl_context)}</span><b>{html.escape(league)}</b></div>''',
'''                    <div><span>{html.escape(lbl_age)}</span><b>{html.escape(age_display)} {html.escape(age_suffix)}</b></div>
                    <div><span>{html.escape(lbl_position)}</span><b>{html.escape(position_badge)}</b></div>'''
)

# 5) Meta grid a 2 columnas
css = r'''
<style>
/* TM.6.9.7 cloud sync final */
.snapshot-identity-layout .snapshot-meta-grid,
.snapshot-card.snapshot-card-identity .snapshot-meta-grid {
    grid-template-columns: 0.8fr 1.2fr !important;
}
</style>
'''
if "TM.6.9.7 cloud sync final" not in s:
    s += "\n\nst.markdown(" + repr(css) + ", unsafe_allow_html=True)\n"

p.write_text(s, encoding="utf-8")
print("OK cloud sync final")
