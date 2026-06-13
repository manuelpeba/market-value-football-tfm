from __future__ import annotations

from pathlib import Path
import re
import unicodedata
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] if len(Path(__file__).resolve().parents) > 2 else Path.cwd()
# If executed from src/scouting/roles, parents[3] is project root. Fallback handled below.
for p in [Path.cwd(), *Path(__file__).resolve().parents]:
    if (p / 'data').exists():
        ROOT = p
        break

INPUT = ROOT / 'data' / 'external' / 'fbref_top5_2017_2025.csv'
OUT_DIR = ROOT / 'data' / 'processed'
REPORT_DIR = ROOT / 'reports' / 'roles'
OUT = OUT_DIR / 'player_role_features_advanced.parquet'
COVERAGE = REPORT_DIR / 'role_feature_coverage_advanced.csv'
SUMMARY = REPORT_DIR / 'role_feature_dataset_summary.csv'

MIN_MINUTES = 900


def log(msg: str) -> None:
    print(f'[TM.6.2] {msg}')


def normalize_text(x) -> str:
    if pd.isna(x):
        return ''
    s = str(x).strip().lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    return s


def to_numeric_series(s: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(s):
        return pd.to_numeric(s, errors='coerce')
    return pd.to_numeric(
        s.astype(str)
        .str.replace('%', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.replace('\u00a0', '', regex=False)
        .str.strip()
        .replace({'': np.nan, 'nan': np.nan, 'None': np.nan}),
        errors='coerce',
    )


def safe_col(df: pd.DataFrame, name: str, default=np.nan) -> pd.Series:
    if name in df.columns:
        return to_numeric_series(df[name])
    return pd.Series(default, index=df.index, dtype='float64')


def per90(total: pd.Series, n90: pd.Series) -> pd.Series:
    total = pd.to_numeric(total, errors='coerce')
    n90 = pd.to_numeric(n90, errors='coerce')
    return np.where(n90 > 0, total / n90, np.nan)


def infer_role_subgroup(pos: str) -> str:
    """Resolve FBref coarse position labels into role-modelling subgroups.

    Important: the external Kaggle/FBref file often stores hybrid labels such as
    MF,FW or MF,DF. For role discovery, these should remain MID by default;
    otherwise players such as Pedri/Wirtz are pushed into ATT_CF and João Neves/
    Caicedo into DEF_CB. This resolver therefore prioritises midfield whenever
    MF appears in a mixed label, unless a more specific wide/fullback/striker
    token exists.
    """
    raw = '' if pd.isna(pos) else str(pos).upper().strip()
    parts = [p.strip() for p in re.split(r'[,/\- ]+', raw) if p.strip()]
    joined = ' '.join(parts)
    part_set = set(parts)

    if 'GK' in part_set or 'GOALKEEPER' in joined:
        return 'GK'

    # Specific detailed labels, when available. The Kaggle file usually only has
    # DF/MF/FW, but these branches keep the function robust for richer sources.
    if any(p in part_set for p in ['FB', 'WB', 'LB', 'RB', 'LWB', 'RWB']) or any(k in joined for k in ['FULLBACK', 'FULL BACK', 'WINGBACK', 'WING BACK', 'LEFT BACK', 'RIGHT BACK']):
        return 'DEF_FB'

    if any(p in part_set for p in ['LW', 'RW', 'W', 'LM', 'RM']) or any(k in joined for k in ['WINGER', 'LEFT WING', 'RIGHT WING', 'WIDE']):
        return 'ATT_WIDE'

    if any(p in part_set for p in ['ST', 'CF']) or any(k in joined for k in ['STRIKER', 'CENTRE FORWARD', 'CENTER FORWARD']):
        return 'ATT_CF'

    # Coarse FBref hybrid labels: midfield has priority. This is the TM.6.3.1
    # fix for Pedri/Wirtz/João Neves/Caicedo-style misclassification.
    if 'MF' in part_set or 'MID' in part_set or any(k in joined for k in ['MIDFIELDER']):
        return 'MID'

    # Pure forwards and pure defenders after resolving midfield hybrids.
    if 'FW' in part_set or any(k in joined for k in ['FORWARD']):
        return 'ATT_CF'

    if any(p in part_set for p in ['CB', 'DF', 'DEF']) or any(k in joined for k in ['CENTRE BACK', 'CENTER BACK', 'CENTRAL DEFENDER', 'DEFENDER']):
        return 'DEF_CB'

    return 'UNK'


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f'Input not found: {INPUT}')

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    log(f'Reading {INPUT}')
    df = pd.read_csv(INPUT, sep=';', decimal=',', low_memory=False)
    log(f'Raw shape: {df.shape[0]:,} rows x {df.shape[1]:,} cols')

    # Required identity columns
    rename = {
        'player': 'player', 'team': 'team', 'league': 'league', 'season': 'season',
        'pos_': 'pos_', 'age_': 'age_', 'Playing Time_Min': 'minutes', 'Playing Time_90s': 'nineties'
    }
    missing = [c for c in rename if c not in df.columns]
    if missing:
        raise RuntimeError(f'Missing required columns: {missing}')

    out = pd.DataFrame(index=df.index)
    out['player'] = df['player'].astype(str).str.strip()
    out['team'] = df['team'].astype(str).str.strip()
    out['league'] = df['league'].astype(str).str.strip()
    out['season'] = df['season'].astype(str).str.strip()
    out['pos_'] = df['pos_'].astype(str).str.strip()
    out['age_'] = safe_col(df, 'age_')
    out['minutes'] = safe_col(df, 'Playing Time_Min')
    out['nineties'] = safe_col(df, 'Playing Time_90s')
    out['role_subgroup'] = out['pos_'].apply(infer_role_subgroup)
    out['player_key'] = out['player'].map(normalize_text)
    out['team_key'] = out['team'].map(normalize_text)

    # Core advanced features, mostly per90 to avoid role clusters becoming minutes clusters.
    out['goals_p90'] = safe_col(df, 'Per 90 Minutes_Gls')
    out['assists_p90'] = safe_col(df, 'Per 90 Minutes_Ast')
    out['xg_p90'] = safe_col(df, 'Per 90 Minutes_xG')
    out['xag_p90'] = safe_col(df, 'Per 90 Minutes_xAG')
    out['shots_p90'] = safe_col(df, 'Standard_Sh/90')
    out['sot_p90'] = safe_col(df, 'Standard_SoT/90')
    out['shot_distance'] = safe_col(df, 'Standard_Dist')
    out['g_per_shot'] = safe_col(df, 'Standard_G/Sh')
    out['g_per_sot'] = safe_col(df, 'Standard_G/SoT')

    out['key_passes_p90'] = per90(safe_col(df, 'KP_'), out['nineties'])
    out['progressive_passes_p90'] = per90(safe_col(df, 'Progression_PrgP').fillna(safe_col(df, 'PrgP_')), out['nineties'])
    out['progressive_carries_p90'] = per90(safe_col(df, 'Progression_PrgC').fillna(safe_col(df, 'Carries_PrgC')), out['nineties'])
    out['progressive_receipts_p90'] = per90(safe_col(df, 'Progression_PrgR').fillna(safe_col(df, 'Receiving_PrgR')), out['nineties'])
    out['passes_final_third_p90'] = per90(safe_col(df, '1/3_'), out['nineties'])
    out['passes_penalty_area_p90'] = per90(safe_col(df, 'PPA_'), out['nineties'])
    out['crosses_penalty_area_p90'] = per90(safe_col(df, 'CrsPA_'), out['nineties'])
    out['pass_completion_pct'] = safe_col(df, 'Total_Cmp%')
    out['long_pass_completion_pct'] = safe_col(df, 'Long_Cmp%')
    out['through_balls_p90'] = per90(safe_col(df, 'Pass Types_TB'), out['nineties'])
    out['switches_p90'] = per90(safe_col(df, 'Pass Types_Sw'), out['nineties'])

    out['sca_p90'] = safe_col(df, 'SCA_SCA90')
    out['gca_p90'] = safe_col(df, 'GCA_GCA90')
    out['sca_live_p90'] = per90(safe_col(df, 'SCA Types_PassLive'), out['nineties'])
    out['gca_live_p90'] = per90(safe_col(df, 'GCA Types_PassLive'), out['nineties'])
    out['takeons_attempted_p90'] = per90(safe_col(df, 'Take-Ons_Att'), out['nineties'])
    out['takeons_success_p90'] = per90(safe_col(df, 'Take-Ons_Succ'), out['nineties'])
    out['takeons_success_pct'] = safe_col(df, 'Take-Ons_Succ%')
    out['carries_box_p90'] = per90(safe_col(df, 'Carries_CPA'), out['nineties'])
    out['touches_box_p90'] = per90(safe_col(df, 'Touches_Att Pen'), out['nineties'])
    out['touches_att_third_p90'] = per90(safe_col(df, 'Touches_Att 3rd'), out['nineties'])

    out['tackles_p90'] = per90(safe_col(df, 'Tackles_Tkl'), out['nineties'])
    out['tackles_won_p90'] = per90(safe_col(df, 'Tackles_TklW'), out['nineties'])
    out['interceptions_p90'] = per90(safe_col(df, 'Int_'), out['nineties'])
    out['tkl_int_p90'] = per90(safe_col(df, 'Tkl+Int_'), out['nineties'])
    out['blocks_p90'] = per90(safe_col(df, 'Blocks_Blocks'), out['nineties'])
    out['clearances_p90'] = per90(safe_col(df, 'Clr_'), out['nineties'])
    out['aerials_won_p90'] = per90(safe_col(df, 'Aerial Duels_Won'), out['nineties'])
    out['aerials_won_pct'] = safe_col(df, 'Aerial Duels_Won%')
    out['recoveries_p90'] = per90(safe_col(df, 'Performance_Recov'), out['nineties'])
    out['errors_p90'] = per90(safe_col(df, 'Err_'), out['nineties'])

    # Composite role-specific indices for audit and later clustering.
    out['finishing_index_role'] = out[['goals_p90', 'xg_p90', 'shots_p90', 'sot_p90', 'touches_box_p90']].mean(axis=1)
    out['creation_index_role'] = out[['assists_p90', 'xag_p90', 'key_passes_p90', 'sca_p90', 'gca_p90']].mean(axis=1)
    out['progression_index_role'] = out[['progressive_passes_p90', 'progressive_carries_p90', 'passes_final_third_p90', 'progressive_receipts_p90']].mean(axis=1)
    out['defending_index_role'] = out[['tackles_p90', 'interceptions_p90', 'blocks_p90', 'clearances_p90', 'recoveries_p90']].mean(axis=1)
    out['duel_index_role'] = out[['aerials_won_p90', 'aerials_won_pct', 'takeons_success_pct']].mean(axis=1)

    # Filter only useful rows for role modelling.
    before = len(out)
    out = out[out['player_key'].ne('')].copy()
    out = out[out['role_subgroup'].ne('UNK')].copy()
    out = out[out['minutes'].fillna(0) >= MIN_MINUTES].copy()
    log(f'Filtered role feature rows: {len(out):,}/{before:,} with minutes >= {MIN_MINUTES}')
    log('Coverage by subgroup:')
    print(out['role_subgroup'].value_counts(dropna=False).to_string())

    # Save feature coverage report.
    id_cols = {'player','team','league','season','pos_','age_','minutes','nineties','role_subgroup','player_key','team_key'}
    feature_cols = [c for c in out.columns if c not in id_cols]
    coverage_df = pd.DataFrame({
        'feature': feature_cols,
        'non_null_rate': [out[c].notna().mean() for c in feature_cols],
        'non_zero_rate': [out[c].fillna(0).ne(0).mean() if pd.api.types.is_numeric_dtype(out[c]) else np.nan for c in feature_cols],
    }).sort_values('non_null_rate', ascending=False)
    coverage_df.to_csv(COVERAGE, index=False)

    summary_df = (
        out.groupby('role_subgroup')
        .agg(rows=('player', 'size'), players=('player_key', 'nunique'), avg_minutes=('minutes', 'mean'))
        .reset_index()
    )
    summary_df.to_csv(SUMMARY, index=False)

    out.to_parquet(OUT, index=False)
    log(f'Output written: {OUT}')
    log(f'Coverage report: {COVERAGE}')
    log(f'Summary report: {SUMMARY}')


if __name__ == '__main__':
    main()
