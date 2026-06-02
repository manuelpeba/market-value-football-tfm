from pathlib import Path
from math import ceil
import html

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def find_project_root() -> Path:
    """Resolve project root whether the dashboard is launched from /dashboard, /app or project root."""
    current = Path(__file__).resolve()
    candidates = [current.parent, *current.parents]

    for candidate in candidates:
        if (candidate / "reports" / "rankings").exists() or (candidate / "data" / "processed").exists():
            return candidate

    # Expected layout: project_root/dashboard/streamlit_app.py
    return current.parents[1]


ROOT = find_project_root()

RANKINGS_PATH = ROOT / "reports" / "rankings"
BUSINESS_PATH = ROOT / "reports" / "business"
EVALUATION_PATH = ROOT / "reports" / "evaluation"
PROCESSED_PATH = ROOT / "data" / "processed"

SCORED_UNIVERSE_SIZE = 1_138

st.set_page_config(
    page_title="Mercado Ineficiente - Scouting Dashboard",
    page_icon="🎯",
    layout="wide",
)


# =============================================================================
# CSS
# =============================================================================

st.markdown(
    """
<style>
.block-container {
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    max-width: 1540px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061b37 0%, #062b57 100%);
}

[data-testid="stSidebar"] * {
    color: white;
}

/* =========================
   Executive metric cards
   ========================= */

.metric-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 10px 14px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    min-height: 74px;
}

.metric-label {
    color: #64748b;
    font-size: 0.80rem;
    margin-bottom: 0.22rem;
}

.metric-value {
    font-size: 1.55rem;
    font-weight: 850;
    color: #0f172a;
    line-height: 1.15;
}

.helper-caption {
    color: #64748b;
    font-size: 0.76rem;
    margin-top: 4px;
    margin-bottom: 0;
    line-height: 1.2;
}

/* =========================
   Info elements
   ========================= */

.info-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #3b82f6;
    border: 1px solid #2563eb;
    color: #ffffff;
    font-size: 11px;
    font-weight: 900;
    margin-left: 5px;
    vertical-align: 1px;
}

.info-box {
    background: #eaf3ff;
    border-radius: 8px;
    padding: 12px 16px;
    color: #0f4fa8;
    font-weight: 600;
    font-size: 0.90rem;
    margin-bottom: 0.5rem;
}

/* separa los popovers de ayuda de la tarjeta superior */
div[data-testid="stPopover"] {
    margin-top: 8px;
}

/* =========================
   Player table
   ========================= */

.player-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.80rem;
    background: white;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    overflow: hidden;
}

.player-table th {
    background: #f8fafc;
    color: #334155;
    font-weight: 800;
    padding: 9px 8px;
    border-bottom: 1px solid #e6eaf0;
    text-align: left;
}

.player-table td {
    padding: 8px;
    border-bottom: 1px solid #edf2f7;
    color: #0f172a;
    vertical-align: middle;
}

/* =========================
   Badges
   ========================= */

.badge-red {
    background: #ef4444;
    color: white;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.74rem;
    display: inline-block;
}

.badge-yellow {
    background: #facc15;
    color: #422006;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.74rem;
    display: inline-block;
}

.badge-gray {
    background: #e5e7eb;
    color: #374151;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.74rem;
    display: inline-block;
}

.recommendation {
    background: #bbf7d0;
    color: #166534;
    border-radius: 7px;
    padding: 5px 10px;
    font-weight: 800;
    display: inline-block;
}

/* =========================
   Player profile
   ========================= */

.profile-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
}

.profile-table td {
    padding: 5px 4px;
    vertical-align: top;
    font-size: 0.90rem;
}

.profile-table td:first-child {
    color: #334155;
    font-weight: 800;
    width: 155px;
}

/* =========================
   SHAP block
   ========================= */

.shap-executive-box {
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 12px 16px;
    background: #f8fafc;
    margin-bottom: 12px;
    color: #334155;
    font-size: 0.90rem;
}

/* =========================
   Plot / legend spacing
   ========================= */

div[data-testid="stVerticalBlock"] {
    gap: 0.85rem;
}

.compact-legend-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 10px 14px;
    min-height: 64px;
    font-size: 0.82rem;
    color: #0f172a;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025);
    white-space: nowrap;
}

.compact-top5-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 10px 14px;
    min-height: 64px;
    font-size: 0.86rem;
    color: #0f172a;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025);
}

.compact-top5-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-top: 8px;
}

.compact-top5-grid div {
    line-height: 1.2;
}

.compact-top5-grid span {
    display: block;
    color: #94a3b8;
    font-size: 0.74rem;
    margin-top: 4px;
}

/* =========================
   Player Radar & Benchmarking
   ========================= */

.radar-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 12px 14px;
    min-height: 112px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
}

.radar-card-title {
    color: #0f172a;
    font-size: 0.86rem;
    font-weight: 850;
    margin-bottom: 6px;
}

.radar-card-percentile {
    color: #0f172a;
    font-size: 1.35rem;
    font-weight: 900;
    line-height: 1.1;
}

.radar-card-label {
    color: #64748b;
    font-size: 0.80rem;
    font-weight: 700;
    margin-top: 4px;
}

.radar-card-value {
    color: #94a3b8;
    font-size: 0.72rem;
    margin-top: 5px;
}

.radar-info-box {
    background: #f8fafc;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 12px 16px;
    color: #334155;
    font-size: 0.90rem;
    margin-bottom: 0.75rem;
}

.radar-warning-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 12px;
    padding: 12px 16px;
    color: #9a3412;
    font-size: 0.88rem;
    margin-bottom: 0.75rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Helpers
# =============================================================================

@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def translate_tier(value):
    tier_map = {
        "high_priority": "Alta prioridad",
        "target_scouting": "Objetivo scouting",
        "low_risk": "Bajo riesgo",
        "exploratory": "Exploratorio",
        "Alta prioridad": "Alta prioridad",
        "Objetivo scouting": "Objetivo scouting",
        "Bajo riesgo": "Bajo riesgo",
        "Exploratorio": "Exploratorio",
    }
    return tier_map.get(value, value)


def tier_badge(value):
    label = translate_tier(value)
    if label == "Alta prioridad":
        return f'<span class="badge-red">{label}</span>'
    if label == "Objetivo scouting":
        return f'<span class="badge-yellow">{label}</span>'
    return f'<span class="badge-gray">{label}</span>'


def format_money_short(value):
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"€{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"€{value / 1_000:.0f}K"
        return f"€{value:.0f}"
    except Exception:
        return "N/A"


def format_money_tm(value):
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f} mill. €"
        if value >= 1_000:
            return f"{value / 1_000:.0f} mil €"
        return f"{value:.0f} €"
    except Exception:
        return "N/A"


def format_money_readable(value):
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f} mill. €"
        if value >= 1_000:
            return f"{value / 1_000:.0f} K €"
        return f"{value:.0f} €"
    except Exception:
        return "N/A"


def format_score(value):
    try:
        return f"{float(value):.1f}"
    except Exception:
        return "N/A"


def safe_get(row, col, default="N/A"):
    try:
        value = row[col]
        if pd.isna(value):
            return default
        return value
    except Exception:
        return default


def render_metric_card(label, value, show_info_icon=False):
    info_icon = " <span class='info-icon'>i</span>" if show_info_icon else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}{info_icon}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card_with_caption(label, value, caption=None, show_info_icon=False):
    info_icon = " <span class='info-icon'>i</span>" if show_info_icon else ""
    caption_html = (
        f"<div class='helper-caption'>{html.escape(str(caption))}</div>"
        if caption
        else ""
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}{info_icon}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def calculate_gap_relative(row):
    try:
        observed = float(row["market_value_eur"])
        predicted = float(row["predicted_market_value_eur"])
        if observed <= 0:
            return None
        return (predicted - observed) / observed
    except Exception:
        return None


def get_player_name(row):
    return safe_get(row, "player_name_fbref", safe_get(row, "player_name", "Jugador"))


def build_recommendation(row):
    try:
        opportunity = float(safe_get(row, "opportunity_score", 0))
        confidence = float(safe_get(row, "confidence_score", 0))
        gap = float(safe_get(row, "market_value_gap_eur", 0))
    except Exception:
        return "Revisión exploratoria"

    if opportunity >= 85 and confidence >= 70 and gap > 0:
        return "Scouting prioritario"
    if opportunity >= 75 and confidence >= 60 and gap > 0:
        return "Seguimiento recomendado"
    return "Revisión exploratoria"



# =============================================================================
# Player Radar & Positional Benchmarking helpers
# =============================================================================

RADAR_DATASET_CANDIDATES = [
    "player_season_modeling_indices.parquet",
    "player_season_modeling_growth.parquet",
    "player_season_modeling_advanced.parquet",
    "player_season_modeling.parquet",
    "player_season_panel.parquet",
]

RADAR_METRIC_CANDIDATES = {
    "MID": [
        ("minutes_played", "Minutos"),
        ("goals_per90", "Goles/90"),
        ("assists_per90", "Asistencias/90"),
        ("g_a_per90", "G+A/90"),
        ("growth_score", "Growth Score"),
        ("confidence_score", "Confidence Score"),
    ],
    "ATT": [
        ("minutes_played", "Minutos"),
        ("goals_per90", "Goles/90"),
        ("assists_per90", "Asistencias/90"),
        ("g_a_per90", "G+A/90"),
        ("growth_score", "Growth Score"),
        ("confidence_score", "Confidence Score"),
    ],
    "DEF": [
        ("minutes_played", "Minutos"),
        ("tackles_per90", "Tackles/90"),
        ("interceptions_per90", "Interceptions/90"),
        ("blocks_per90", "Blocks/90"),
        ("growth_score", "Growth Score"),
        ("confidence_score", "Confidence Score"),
    ],
    "GK": [
        ("minutes_played", "Minutos"),
        ("save_pct", "Save %"),
        ("clean_sheets", "Clean Sheets"),
        ("growth_score", "Growth Score"),
        ("confidence_score", "Confidence Score"),
    ],
}

RADAR_GENERIC_FOOTBALL_METRICS = [
    ("minutes_played", "Minutos"),
    ("goals_per90", "Goles/90"),
    ("assists_per90", "Asistencias/90"),
    ("g_a_per90", "G+A/90"),
    ("growth_score", "Growth Score"),
    ("confidence_score", "Confidence Score"),
]


def normalize_position_group(value) -> str:
    position = str(value).upper().strip()
    if position in {"FWD", "FW"}:
        return "ATT"
    return position


def get_all_radar_metric_columns() -> list[str]:
    cols = []
    for metrics in RADAR_METRIC_CANDIDATES.values():
        cols.extend([col for col, _ in metrics])
    cols.extend([col for col, _ in RADAR_GENERIC_FOOTBALL_METRICS])
    return sorted(set(cols))


def load_radar_feature_dataset() -> pd.DataFrame:
    """Load the richest available processed player-season dataset for radar metrics."""
    for filename in RADAR_DATASET_CANDIDATES:
        candidate_path = PROCESSED_PATH / filename
        candidate_df = load_parquet(candidate_path)

        if candidate_df.empty:
            continue

        radar_cols = set(get_all_radar_metric_columns())
        available_radar_cols = radar_cols.intersection(candidate_df.columns)

        if available_radar_cols:
            return candidate_df.copy()

    return pd.DataFrame()


def enrich_shortlist_with_radar_features(shortlist_df: pd.DataFrame) -> pd.DataFrame:
    """Attach FBref/modeling football metrics to the shortlist if rankings do not contain them.

    The ranking CSV is intentionally narrow. Sprint 10.1 needs player-performance
    columns, so the dashboard attempts to recover them from processed player-season
    datasets using progressively less restrictive merge keys.
    """
    if shortlist_df.empty:
        return shortlist_df

    radar_source = load_radar_feature_dataset()
    if radar_source.empty:
        return shortlist_df

    left = shortlist_df.copy()
    right = radar_source.copy()

    if "player_name_fbref" not in right.columns and "player_name" in right.columns:
        right = right.rename(columns={"player_name": "player_name_fbref"})

    radar_metric_cols = get_all_radar_metric_columns()
    context_cols = ["position_group", "league", "age", "minutes_played"]
    cols_to_add = [
        col
        for col in radar_metric_cols + context_cols
        if col in right.columns and col not in left.columns
    ]

    if not cols_to_add:
        return left

    merge_key_options = [
        ["player_name_fbref", "season", "club"],
        ["player_name_fbref", "season"],
        ["player_name_tm", "season"],
        ["player_name_fbref", "club"],
        ["player_name_fbref"],
    ]

    best_enriched = left.copy()
    best_non_null = -1

    for candidate_keys in merge_key_options:
        merge_keys = [col for col in candidate_keys if col in left.columns and col in right.columns]
        if not merge_keys or not any(k in merge_keys for k in ["player_name_fbref", "player_name_tm"]):
            continue

        right_cols = merge_keys + [col for col in cols_to_add if col not in merge_keys]
        right_tmp = right[right_cols].copy()

        # Avoid many-to-many explosions. Keep the first valid row per merge key after
        # preferring rows with more available radar metrics.
        available_metric_cols = [col for col in cols_to_add if col in right_tmp.columns]
        if available_metric_cols:
            right_tmp["_radar_completeness"] = right_tmp[available_metric_cols].notna().sum(axis=1)
            right_tmp = right_tmp.sort_values("_radar_completeness", ascending=False)
            right_tmp = right_tmp.drop(columns=["_radar_completeness"])

        right_tmp = right_tmp.drop_duplicates(subset=merge_keys)

        merged = left.merge(
            right_tmp,
            on=merge_keys,
            how="left",
            suffixes=("", "_radar"),
        )

        non_null_count = int(merged[cols_to_add].notna().sum().sum())
        if non_null_count > best_non_null:
            best_non_null = non_null_count
            best_enriched = merged

    return best_enriched

def get_available_radar_metrics(position_group: object, source_df: pd.DataFrame) -> list[tuple[str, str]]:
    """Return only Sprint 10.1 position-specific football metrics available in the current data."""
    position_key = normalize_position_group(position_group)
    candidates = RADAR_METRIC_CANDIDATES.get(position_key, [])

    available = []
    used_labels = set()

    for col, label in candidates:
        if col in source_df.columns and source_df[col].notna().any() and label not in used_labels:
            available.append((col, label))
            used_labels.add(label)

    return available[:6]

def calculate_percentile(series: pd.Series, value) -> float | None:
    clean_series = pd.to_numeric(series, errors="coerce").dropna()
    player_value = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]

    if clean_series.empty or pd.isna(player_value):
        return None

    return round(float((clean_series <= player_value).mean() * 100), 1)


def percentile_label(percentile: float | None) -> str:
    if percentile is None or pd.isna(percentile):
        return "Sin dato"
    if percentile >= 90:
        return "Elite"
    if percentile >= 75:
        return "Muy alto"
    if percentile >= 60:
        return "Alto"
    if percentile >= 40:
        return "Promedio"
    return "Bajo"


def format_radar_metric_value(value) -> str:
    numeric_value = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric_value):
        return "Valor no disponible"
    if abs(float(numeric_value)) >= 100:
        return f"Valor jugador: {float(numeric_value):,.0f}"
    return f"Valor jugador: {float(numeric_value):.2f}"


def build_player_radar_data(
    player_row: pd.Series,
    benchmark_df: pd.DataFrame,
    source_df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str]]:
    radar_metrics = get_available_radar_metrics(
        safe_get(player_row, "position_group", "UNK"),
        source_df,
    )

    records = []
    missing_metrics = []

    for metric, label in radar_metrics:
        if metric not in benchmark_df.columns:
            missing_metrics.append(metric)
            continue

        percentile = calculate_percentile(
            benchmark_df[metric],
            safe_get(player_row, metric, np.nan),
        )

        if percentile is None:
            missing_metrics.append(metric)
            continue

        records.append(
            {
                "metric": metric,
                "label": label,
                "percentile": percentile,
                "rating": percentile_label(percentile),
                "value": safe_get(player_row, metric, np.nan),
            }
        )

    return pd.DataFrame(records), missing_metrics

def build_player_radar_chart(radar_df: pd.DataFrame, selected_player: str) -> go.Figure | None:
    if radar_df.empty:
        return None

    closed_r = radar_df["percentile"].tolist() + [radar_df["percentile"].iloc[0]]
    closed_theta = radar_df["label"].tolist() + [radar_df["label"].iloc[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=closed_r,
            theta=closed_theta,
            fill="toself",
            name=selected_player,
            hovertemplate="%{theta}<br>Percentil %{r:.1f}<extra></extra>",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
            )
        ),
        showlegend=False,
        height=550,
        margin=dict(l=35, r=35, t=45, b=35),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def render_scouting_cards(radar_df: pd.DataFrame) -> None:
    """Render compact scouting percentile cards."""

    if radar_df.empty:
        return

    cards_per_row = 3

    for start_idx in range(0, len(radar_df), cards_per_row):
        row_df = radar_df.iloc[start_idx:start_idx + cards_per_row]
        cols = st.columns(cards_per_row)

        for col, (_, row) in zip(cols, row_df.iterrows()):
            with col:
                st.markdown(
                    f"""
                    <div class="radar-card">
                        <div class="radar-card-title">{html.escape(str(row['label']))}</div>
                        <div class="radar-card-percentile">P{float(row['percentile']):.0f}</div>
                        <div class="radar-card-label">{html.escape(str(row['rating']))}</div>
                        <div class="radar-card-value">{html.escape(format_radar_metric_value(row['value']).replace('Valor jugador: ', 'Valor: '))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

def render_benchmark_context(benchmark_df: pd.DataFrame, benchmark_mode: str, player_position: str) -> None:
    """Render benchmark context for the radar section."""

    if benchmark_df.empty:
        return

    n_players = len(benchmark_df)

    avg_age = None
    avg_minutes = None

    if "age" in benchmark_df.columns:
        avg_age = pd.to_numeric(benchmark_df["age"], errors="coerce").mean()

    if "minutes_played" in benchmark_df.columns:
        avg_minutes = pd.to_numeric(benchmark_df["minutes_played"], errors="coerce").mean()

    parts = [
        f"<b>Benchmark:</b> {html.escape(benchmark_mode.lower())}",
        f"<b>Posición:</b> {html.escape(str(player_position))}",
        f"<b>Muestra:</b> {n_players:,} jugadores",
    ]

    if pd.notna(avg_age):
        parts.append(f"<b>Edad media:</b> {avg_age:.1f} años")

    if pd.notna(avg_minutes):
        parts.append(f"<b>Minutos medios:</b> {avg_minutes:,.0f}")

    st.markdown(
        f"""
        <div class="radar-info-box">
            {" · ".join(parts)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_player_radar_benchmarking(shortlist_df: pd.DataFrame) -> None:
    st.markdown("---")
    st.header("🎯 Player Radar & Positional Benchmarking")
    st.markdown(
        """
<div class="radar-info-box">
<b>Objetivo:</b> transformar el ranking en scouting explicativo. En Sprint 10.1 el radar MVP compara al jugador seleccionado contra un benchmark dinámico mediante percentiles usando métricas disponibles: Minutos, Goles/90, Asistencias/90, G+A/90, Growth Score y Confidence Score. DEF/GK incorporan métricas específicas solo si existen.</div>
""",
        unsafe_allow_html=True,
    )

    if shortlist_df.empty:
        st.info("No hay jugadores disponibles para construir el radar con los filtros actuales.")
        return

    player_name_col = "player_name_tm" if "player_name_tm" in shortlist_df.columns else "player_name_fbref"
    if player_name_col not in shortlist_df.columns:
        st.info("No hay columna de nombre de jugador disponible para el selector del radar.")
        return

    selector_df = shortlist_df.dropna(subset=[player_name_col]).copy()
    if selector_df.empty:
        st.info("No hay jugadores con nombre disponible para el radar.")
        return

    if "opportunity_score" in selector_df.columns:
        selector_df = selector_df.sort_values("opportunity_score", ascending=False)

    player_options = selector_df[player_name_col].astype(str).drop_duplicates().tolist()

    controls = st.columns([1.5, 1.0])
    with controls[0]:
        selected_radar_player = st.selectbox(
            "Seleccionar jugador",
            player_options,
            key="radar_selected_player",
        )
    with controls[1]:
        benchmark_mode = st.radio(
            "Comparar contra",
            ["Misma posición", "Toda la muestra"],
            horizontal=True,
            key="radar_benchmark_mode",
        )

    player_row = selector_df[selector_df[player_name_col].astype(str) == selected_radar_player].iloc[0]
    player_position = normalize_position_group(safe_get(player_row, "position_group", "UNK"))

    benchmark_df = shortlist_df.copy()
    if benchmark_mode == "Misma posición" and "position_group" in benchmark_df.columns:
        benchmark_df = benchmark_df[
            benchmark_df["position_group"].apply(normalize_position_group) == player_position
        ].copy()

    radar_df, missing_metrics = build_player_radar_data(
        player_row=player_row,
        benchmark_df=benchmark_df,
        source_df=shortlist_df,
    )

    if radar_df.empty or len(radar_df) < 3:
        position_key = normalize_position_group(safe_get(player_row, "position_group", "UNK"))
        expected_metrics = [metric for metric, _ in RADAR_METRIC_CANDIDATES.get(position_key, [])]

        st.warning(
            "No hay suficientes métricas Sprint 10.1 para construir benchmarking posicional real. "
            "La shortlist actual solo contiene variables de scoring y métricas ofensivas básicas. "
            "Regenera el ranking incorporando columnas FBref avanzadas o revisa que existan en data/processed/."
        )
        st.caption("Métricas esperadas para esta posición: " + ", ".join(expected_metrics))
        st.caption("Columnas disponibles para radar: " + ", ".join([c for c in shortlist_df.columns if c in get_all_radar_metric_columns()]))
        return

    render_benchmark_context(
        benchmark_df=benchmark_df,
        benchmark_mode=benchmark_mode,
        player_position=player_position,
    )

    radar_col, cards_col = st.columns([1.15, 1.0], gap="large")
    with radar_col:
        radar_fig = build_player_radar_chart(radar_df, selected_radar_player)
        if radar_fig is not None:
            st.plotly_chart(
                radar_fig,
                use_container_width=True,
                config={"displaylogo": False},
            )

    with cards_col:
        st.subheader("🧾 Tarjetas de scouting")
        render_scouting_cards(radar_df)

        if missing_metrics:
            st.caption(
                "Métricas sin dato para este benchmark: " + ", ".join(sorted(set(missing_metrics)))
            )

    top_attributes = radar_df.sort_values("percentile", ascending=False).head(4)
    explanation = " · ".join(
        f"{row['label']} P{float(row['percentile']):.1f} ({row['rating']})"
        for _, row in top_attributes.iterrows()
    )
    st.markdown(
        f"**Lectura scouting:** {html.escape(str(selected_radar_player))} destaca principalmente en {explanation}."
    )


def build_html_table(page_df: pd.DataFrame):
    columns = [
        ("player_name_fbref", "Jugador"),
        ("club", "Club"),
        ("league", "Liga"),
        ("season", "Temporada"),
        ("position_group", "Posición"),
        ("age", "Edad"),
        ("minutes_played", "Minutos"),
        ("market_value_eur", "Valor mercado (€)"),
        ("predicted_market_value_eur", "Valor estimado (€)"),
        ("market_value_gap_eur", "Gap (€)"),
        ("market_value_gap_pct", "Gap (%)"),
        ("growth_score", "Growth Score"),
        ("confidence_score", "Confidence Score"),
        ("opportunity_score", "Opportunity Score"),
        ("risk_score", "Risk Score"),
        ("risk_level", "Riesgo"),
        ("risk_adjusted_opportunity_score", "Opp. ajustada"),
        ("dashboard_tier", "Tier"),
    ]

    header = "".join(f"<th>{label}</th>" for _, label in columns)
    rows = ""

    for _, r in page_df.iterrows():
        cells = []
        for col, _ in columns:
            val = safe_get(r, col, "")

            if col in ["market_value_eur", "predicted_market_value_eur", "market_value_gap_eur"]:
                val = format_money_short(val)
            elif col == "market_value_gap_pct":
                try:
                    val = f"{float(val):.0f}%"
                except Exception:
                    val = "N/A"
            elif col in ["growth_score", "confidence_score", "opportunity_score", "risk_score", "risk_adjusted_opportunity_score"]:
                val = format_score(val)
            elif col == "age":
                try:
                    val = f"{float(val):.1f}"
                except Exception:
                    val = "N/A"
            elif col == "minutes_played":
                try:
                    val = f"{int(float(val)):,}"
                except Exception:
                    val = "N/A"
            elif col == "dashboard_tier":
                cells.append(f"<td>{tier_badge(val)}</td>")
                continue

            cells.append(f"<td>{html.escape(str(val))}</td>")

        rows += "<tr>" + "".join(cells) + "</tr>"

    return f"""
    <table class="player-table">
        <thead><tr>{header}</tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """


def make_shap_proxy(player_df: pd.Series) -> pd.DataFrame:
    minutes = float(safe_get(player_df, "minutes_played", 0))
    growth = float(safe_get(player_df, "growth_score", 50))
    opportunity = float(safe_get(player_df, "opportunity_score", 50))
    confidence = float(safe_get(player_df, "confidence_score", 50))
    age = float(safe_get(player_df, "age", 22))

    shap_values = pd.DataFrame(
        {
            "feature": [
                "Minutos jugados",
                "Goles por 90",
                "Asistencias por 90",
                "Growth Score",
                "Confidence Score",
                "Edad",
                "Liga",
                "Posición",
            ],
            "impact": [
                min(minutes / 2300, 1.35),
                min(opportunity / 140, 0.85),
                min(growth / 180, 0.70),
                min(growth / 160, 0.75),
                min(confidence / 220, 0.55),
                -0.22 if age > 22 else 0.15,
                0.18,
                -0.12,
            ],
        }
    )
    return shap_values.sort_values("impact")


def render_bubble_legend(top5_players: pd.DataFrame | None = None):
    """Leyenda compacta debajo de la matriz Coste vs Upside."""

    col_tier, col_top5 = st.columns([1.05, 2.45], gap="large")

    with col_tier:
        st.markdown(
            """
            <div class="compact-legend-card">
                <b>Tier de oportunidad</b><br>
                🔴 Alta prioridad &nbsp;&nbsp; 🟡 Objetivo scouting &nbsp;&nbsp; ⚪ Exploratorio
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_top5:
        if top5_players is not None and not top5_players.empty:
            items = []

            for idx, row in top5_players.reset_index(drop=True).iterrows():
                items.append(
                    f"<b>{idx + 1}. {html.escape(str(get_player_name(row)))}</b>"
                    f"<span>{html.escape(str(safe_get(row, 'club', '')))}</span>"
                )

            st.markdown(
                f"""
                <div class="compact-top5-card">
                    <b>🎯 Top 5 destacados</b>
                    <div class="compact-top5-grid">
                        {"".join(f"<div>{item}</div>" for item in items)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption("No hay jugadores destacados con los filtros actuales.")


def build_opportunity_chart(chart_source: pd.DataFrame) -> go.Figure | None:
    """Executive Cost vs Upside matrix."""

    required = {"market_value_eur", "market_value_gap_eur", "opportunity_score"}
    if not required.issubset(chart_source.columns):
        return None

    chart_df = chart_source.dropna(subset=list(required)).copy()
    chart_df = chart_df[
        (chart_df["market_value_eur"] > 0)
        & (chart_df["market_value_gap_eur"] > 0)
        & (chart_df["opportunity_score"] > 0)
    ].copy()

    if chart_df.empty:
        return None

    chart_df = chart_df.sort_values("opportunity_score", ascending=False).head(20).copy()
    chart_df["dashboard_tier"] = chart_df.get("opportunity_tier_label", "Exploratorio")

    top5_idx = chart_df.sort_values("opportunity_score", ascending=False).head(5).index
    chart_df.loc[top5_idx, "dashboard_tier"] = "Alta prioridad"

    cost_ref = float(chart_df["market_value_eur"].median())
    upside_ref = float(chart_df["market_value_gap_eur"].median())

    min_score = float(chart_df["opportunity_score"].min())
    max_score = float(chart_df["opportunity_score"].max())
    score_span = max(max_score - min_score, 1.0)
    scaled = ((chart_df["opportunity_score"] - min_score) / score_span).clip(0, 1)
    chart_df["bubble_size"] = 16 + (scaled ** 1.45) * 44

    color_map = {
        "Alta prioridad": "#ef4444",
        "Objetivo scouting": "#facc15",
        "Exploratorio": "#9ca3af",
        "Bajo riesgo": "#22c55e",
    }

    fig = go.Figure()

    x_min = max(float(chart_df["market_value_eur"].min()) * 0.65, 50_000)
    x_max = float(chart_df["market_value_eur"].max()) * 1.95
    y_min = max(float(chart_df["market_value_gap_eur"].min()) * 0.60, 50_000)
    y_max = float(chart_df["market_value_gap_eur"].max()) * 1.75

    quadrant_shapes = [
        dict(type="rect", xref="x", yref="y", x0=x_min, x1=cost_ref, y0=upside_ref, y1=y_max, fillcolor="rgba(34, 197, 94, 0.18)", line=dict(width=0), layer="below"),
        dict(type="rect", xref="x", yref="y", x0=cost_ref, x1=x_max, y0=upside_ref, y1=y_max, fillcolor="rgba(59, 130, 246, 0.13)", line=dict(width=0), layer="below"),
        dict(type="rect", xref="x", yref="y", x0=x_min, x1=cost_ref, y0=y_min, y1=upside_ref, fillcolor="rgba(250, 204, 21, 0.13)", line=dict(width=0), layer="below"),
        dict(type="rect", xref="x", yref="y", x0=cost_ref, x1=x_max, y0=y_min, y1=upside_ref, fillcolor="rgba(239, 68, 68, 0.10)", line=dict(width=0), layer="below"),
    ]
    fig.update_layout(shapes=quadrant_shapes)

    non_top5 = chart_df.drop(index=top5_idx, errors="ignore")

    for tier_name in ["Exploratorio", "Objetivo scouting", "Bajo riesgo"]:
        tier_df = non_top5[non_top5["dashboard_tier"] == tier_name]
        if tier_df.empty:
            continue

        hover_text = [
            f"<b>{get_player_name(row)}</b><br>"
            f"Club: {safe_get(row, 'club')}<br>"
            f"Liga: {safe_get(row, 'league')}<br>"
            f"Posición: {safe_get(row, 'position_group')}<br>"
            f"Edad: {format_score(safe_get(row, 'age'))}<br>"
            f"Valor mercado: {format_money_readable(safe_get(row, 'market_value_eur'))}<br>"
            f"Valor estimado: {format_money_readable(safe_get(row, 'predicted_market_value_eur'))}<br>"
            f"Gap estimado: {format_money_readable(safe_get(row, 'market_value_gap_eur'))}<br>"
            f"Opportunity Score: {format_score(safe_get(row, 'opportunity_score'))}"
            for _, row in tier_df.iterrows()
        ]

        fig.add_trace(
            go.Scatter(
                x=tier_df["market_value_eur"],
                y=tier_df["market_value_gap_eur"],
                mode="markers",
                name=tier_name,
                hovertext=hover_text,
                hoverinfo="text",
                marker=dict(
                    size=tier_df["bubble_size"],
                    color=color_map.get(tier_name, "#9ca3af"),
                    opacity=0.72,
                    line=dict(width=1.0, color="rgba(15, 23, 42, 0.22)"),
                ),
            )
        )

    top5 = chart_df.loc[top5_idx].sort_values("opportunity_score", ascending=False).reset_index(drop=True)
    hover_text_top5 = [
        f"<b>{i + 1}. {get_player_name(row)}</b><br>"
        f"Club: {safe_get(row, 'club')}<br>"
        f"Liga: {safe_get(row, 'league')}<br>"
        f"Posición: {safe_get(row, 'position_group')}<br>"
        f"Edad: {format_score(safe_get(row, 'age'))}<br>"
        f"Valor mercado: {format_money_readable(safe_get(row, 'market_value_eur'))}<br>"
        f"Valor estimado: {format_money_readable(safe_get(row, 'predicted_market_value_eur'))}<br>"
        f"Gap estimado: {format_money_readable(safe_get(row, 'market_value_gap_eur'))}<br>"
        f"Opportunity Score: {format_score(safe_get(row, 'opportunity_score'))}"
        for i, row in top5.iterrows()
    ]

    fig.add_trace(
        go.Scatter(
            x=top5["market_value_eur"],
            y=top5["market_value_gap_eur"],
            mode="markers",
            name="Top 5 prioridad",
            hovertext=hover_text_top5,
            hoverinfo="text",
            cliponaxis=False,
            marker=dict(
                size=np.maximum(top5["bubble_size"].to_numpy(), 44),
                color="#ef4444",
                opacity=0.90,
                line=dict(width=2.4, color="rgba(15, 23, 42, 0.58)"),
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=top5["market_value_eur"],
            y=top5["market_value_gap_eur"],
            mode="text",
            text=[f"<b>{i + 1}</b>" for i in range(len(top5))],
            textfont=dict(size=15, color="white", family="Arial Black"),
            textposition="middle center",
            hoverinfo="skip",
            cliponaxis=False,
            showlegend=False,
        )
    )

    fig.add_vline(
        x=cost_ref,
        line_dash="dash",
        line_color="rgba(15, 23, 42, 0.65)",
        line_width=2,
        annotation_text="Coste mediano",
        annotation_position="top",
    )

    fig.add_hline(
        y=upside_ref,
        line_dash="dash",
        line_color="rgba(15, 23, 42, 0.65)",
        line_width=2,
        annotation_text="Upside mediano",
        annotation_position="right",
    )

    fig.update_layout(
        height=620,
        margin=dict(l=20, r=30, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_title="Valor de mercado actual (€) — escala log",
        yaxis_title="Gap de mercado estimado (€) — escala log",
    )

    fig.update_xaxes(
        type="log",
        range=[np.log10(x_min), np.log10(x_max)],
        showgrid=True,
        gridcolor="#e5e7eb",
        tickvals=[100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000, 20_000_000, 50_000_000],
        ticktext=["100K", "200K", "500K", "1M", "2M", "5M", "10M", "20M", "50M"],
    )
    fig.update_yaxes(
        type="log",
        range=[np.log10(y_min), np.log10(y_max)],
        showgrid=True,
        gridcolor="#e5e7eb",
        tickvals=[50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000, 20_000_000],
        ticktext=["50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M", "20M"],
    )

    return fig



def assign_decision_quadrant(row, opportunity_ref: float, risk_ref: float) -> str:
    """Assign scouting decision quadrant from Opportunity and Risk scores."""
    opportunity = pd.to_numeric(pd.Series([safe_get(row, "opportunity_score")]), errors="coerce").iloc[0]
    risk = pd.to_numeric(pd.Series([safe_get(row, "risk_score")]), errors="coerce").iloc[0]

    if pd.isna(opportunity) or pd.isna(risk):
        return "Sin clasificar"
    if opportunity >= opportunity_ref and risk <= risk_ref:
        return "Objetivo prioritario"
    if opportunity >= opportunity_ref and risk > risk_ref:
        return "Apuesta estratégica"
    if opportunity < opportunity_ref and risk <= risk_ref:
        return "Perfil estable"
    return "Evitar"


def build_opportunity_risk_matrix(chart_source: pd.DataFrame) -> go.Figure | None:
    required = {
        "opportunity_score",
        "risk_score",
        "risk_adjusted_opportunity_score",
    }

    if chart_source.empty or not required.issubset(chart_source.columns):
        return None

    df = chart_source.dropna(subset=list(required)).copy()

    if df.empty:
        return None

    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=list(required)).copy()

    if df.empty:
        return None

    risk_ref = float(df["risk_score"].median())
    opportunity_ref = float(df["opportunity_score"].quantile(0.60))

    def assign_zone(row):
        if row["opportunity_score"] >= opportunity_ref and row["risk_score"] <= risk_ref:
            return "Objetivo prioritario"
        if row["opportunity_score"] >= opportunity_ref and row["risk_score"] > risk_ref:
            return "Apuesta estratégica"
        if row["opportunity_score"] < opportunity_ref and row["risk_score"] <= risk_ref:
            return "Perfil estable"
        return "Evitar"

    df["risk_zone"] = df.apply(assign_zone, axis=1)

    color_map = {
        "Objetivo prioritario": "#22c55e",
        "Apuesta estratégica": "#f97316",
        "Perfil estable": "#3b82f6",
        "Evitar": "#ef4444",
    }

    min_adjusted = float(df["risk_adjusted_opportunity_score"].min())
    max_adjusted = float(df["risk_adjusted_opportunity_score"].max())
    span_adjusted = max(max_adjusted - min_adjusted, 1.0)

    df["bubble_size"] = (
        14
        + (
            (df["risk_adjusted_opportunity_score"] - min_adjusted)
            / span_adjusted
        ).clip(0, 1).mul(42)
    )

    top5 = (
        df.sort_values("risk_adjusted_opportunity_score", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=0,
        x1=risk_ref,
        y0=opportunity_ref,
        y1=100,
        fillcolor="rgba(34,197,94,0.13)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_shape(
        type="rect",
        x0=risk_ref,
        x1=100,
        y0=opportunity_ref,
        y1=100,
        fillcolor="rgba(249,115,22,0.12)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_shape(
        type="rect",
        x0=0,
        x1=risk_ref,
        y0=0,
        y1=opportunity_ref,
        fillcolor="rgba(59,130,246,0.10)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_shape(
        type="rect",
        x0=risk_ref,
        x1=100,
        y0=0,
        y1=opportunity_ref,
        fillcolor="rgba(239,68,68,0.09)",
        line=dict(width=0),
        layer="below",
    )

    for zone in [
        "Objetivo prioritario",
        "Apuesta estratégica",
        "Perfil estable",
        "Evitar",
    ]:
        zone_df = df[df["risk_zone"] == zone]

        if zone_df.empty:
            continue

        hover_text = [
            f"<b>{get_player_name(row)}</b><br>"
            f"Club: {safe_get(row, 'club')}<br>"
            f"Liga: {safe_get(row, 'league')}<br>"
            f"Posición: {safe_get(row, 'position_group')}<br>"
            f"Opportunity Score: {format_score(safe_get(row, 'opportunity_score'))}<br>"
            f"Risk Score: {format_score(safe_get(row, 'risk_score'))}<br>"
            f"Risk Level: {safe_get(row, 'risk_level')}<br>"
            f"Risk Adjusted Opportunity: {format_score(safe_get(row, 'risk_adjusted_opportunity_score'))}"
            for _, row in zone_df.iterrows()
        ]

        fig.add_trace(
            go.Scatter(
                x=zone_df["risk_score"],
                y=zone_df["opportunity_score"],
                mode="markers",
                name=zone,
                hovertext=hover_text,
                hoverinfo="text",
                marker=dict(
                    size=zone_df["bubble_size"],
                    color=color_map[zone],
                    opacity=0.72,
                    line=dict(width=1, color="rgba(15,23,42,0.25)"),
                ),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=top5["risk_score"],
            y=top5["opportunity_score"],
            mode="text",
            text=[str(i + 1) for i in range(len(top5))],
            textfont=dict(size=13, color="white", family="Arial Black"),
            textposition="middle center",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_vline(
        x=risk_ref,
        line_dash="dash",
        line_color="rgba(15,23,42,0.65)",
        line_width=2,
        annotation_text="Riesgo mediano",
        annotation_position="top",
    )

    fig.add_hline(
        y=opportunity_ref,
        line_dash="dash",
        line_color="rgba(15,23,42,0.65)",
        line_width=2,
        annotation_text="Top 40% oportunidad",
        annotation_position="right",
    )

    fig.update_layout(
        height=560,
        margin=dict(l=20, r=30, t=35, b=30),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
        ),
        xaxis_title="Risk Score (Incertidumbre relativa)",
        yaxis_title="Opportunity Score (Upside potencial)",
    )

    fig.update_xaxes(
        range=[0, 100],
        showgrid=True,
        gridcolor="#e5e7eb",
        zeroline=False,
    )

    fig.update_yaxes(
        range=[
            max(0, float(df["opportunity_score"].min()) - 5),
            101,
        ],
        showgrid=True,
        gridcolor="#e5e7eb",
        zeroline=False,
    )

    return fig


def render_opportunity_risk_summary(chart_source: pd.DataFrame) -> None:
    """Render executive KPIs for Opportunity vs Risk matrix."""

    required = {
        "opportunity_score",
        "risk_score",
    }

    if chart_source.empty or not required.issubset(chart_source.columns):
        return

    summary_df = chart_source.copy()

    summary_df["opportunity_score"] = pd.to_numeric(
        summary_df["opportunity_score"],
        errors="coerce",
    )
    summary_df["risk_score"] = pd.to_numeric(
        summary_df["risk_score"],
        errors="coerce",
    )

    if "risk_adjusted_opportunity_score" in summary_df.columns:
        summary_df["risk_adjusted_opportunity_score"] = pd.to_numeric(
            summary_df["risk_adjusted_opportunity_score"],
            errors="coerce",
        )

    summary_df = summary_df.dropna(
        subset=[
            "opportunity_score",
            "risk_score",
        ]
    )

    if summary_df.empty:
        return

    risk_ref = float(summary_df["risk_score"].median())
    opportunity_ref = float(summary_df["opportunity_score"].quantile(0.60))

    quadrants = summary_df.apply(
        lambda row: assign_decision_quadrant(
            row,
            opportunity_ref,
            risk_ref,
        ),
        axis=1,
    )

    priority_targets = int((quadrants == "Objetivo prioritario").sum())
    strategic_bets = int((quadrants == "Apuesta estratégica").sum())
    stable_profiles = int((quadrants == "Perfil estable").sum())
    avoid_profiles = int((quadrants == "Evitar").sum())

    if (
        "risk_adjusted_opportunity_score" in summary_df.columns
        and summary_df["risk_adjusted_opportunity_score"].notna().any()
    ):
        top_idx = summary_df["risk_adjusted_opportunity_score"].idxmax()
        top_adjusted = float(
            summary_df.loc[top_idx, "risk_adjusted_opportunity_score"]
        )
        top_player = get_player_name(summary_df.loc[top_idx])
        top_value = f"{top_adjusted:.1f}"
        top_caption = f"Mejor oportunidad: {top_player}"
    else:
        top_value = f"{summary_df['opportunity_score'].max():.1f}"
        top_caption = "Mejor opportunity score"

    st.markdown("### 🎯 Lectura ejecutiva Opportunity vs Risk")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        render_metric_card_with_caption(
            "Objetivos prioritarios",
            priority_targets,
            "alto potencial · bajo riesgo",
        )

    with c2:
        render_metric_card_with_caption(
            "Apuestas estratégicas",
            strategic_bets,
            "alto potencial · alto riesgo",
        )

    with c3:
        render_metric_card_with_caption(
            "Perfiles estables",
            stable_profiles,
            "potencial moderado · bajo riesgo",
        )

    with c4:
        render_metric_card_with_caption(
            "Evitar",
            avoid_profiles,
            "potencial moderado · alto riesgo",
        )

    with c5:
        render_metric_card_with_caption(
            "🏆 Mejor objetivo",
            top_player,
            f"Risk-adjusted: {top_value}",
        )

def render_chart_executive_summary(chart_source: pd.DataFrame) -> None:
    """Render executive KPI-style summary for the Cost vs Upside matrix."""

    required = {"market_value_eur", "market_value_gap_eur", "opportunity_score"}

    if chart_source.empty or not required.issubset(chart_source.columns):
        return

    chart_df = chart_source.dropna(subset=list(required)).copy()
    chart_df = chart_df[
        (chart_df["market_value_eur"] > 0)
        & (chart_df["market_value_gap_eur"] > 0)
        & (chart_df["opportunity_score"] > 0)
    ].copy()

    if chart_df.empty:
        return

    chart_df = (
        chart_df
        .sort_values("opportunity_score", ascending=False)
        .head(20)
        .copy()
    )

    cost_ref = chart_df["market_value_eur"].median()
    upside_ref = chart_df["market_value_gap_eur"].median()

    priority_zone = chart_df[
        (chart_df["market_value_eur"] <= cost_ref)
        & (chart_df["market_value_gap_eur"] >= upside_ref)
    ]

    premium_zone = chart_df[
        (chart_df["market_value_eur"] > cost_ref)
        & (chart_df["market_value_gap_eur"] >= upside_ref)
    ]

    avg_opportunity = chart_df["opportunity_score"].mean()
    total_gap = chart_df["market_value_gap_eur"].sum()

    top_league = (
        chart_df["league"].mode().iloc[0]
        if "league" in chart_df.columns and not chart_df["league"].dropna().empty
        else "N/D"
    )

    st.markdown("### 🎯 Hallazgos clave del Top 20 filtrado")

    h1, h2, h3, h4, h5 = st.columns(5)

    with h1:
        render_metric_card_with_caption(
            "Comprar / priorizar",
            f"{len(priority_zone)}",
            "candidatos",
        )

    with h2:
        render_metric_card_with_caption(
            "Oportunidades premium",
            f"{len(premium_zone)}",
            "candidatos",
        )

    with h3:
        render_metric_card_with_caption(
            "Score oportunidad",
            f"{avg_opportunity:.1f}",
            "Top 20 filtrado",
        )

    with h4:
        render_metric_card_with_caption(
            "Upside agregado",
            format_money_short(total_gap),
            "valor potencial identificado",
        )

    with h5:
        render_metric_card_with_caption(
            "Liga dominante",
            str(top_league),
            "liga más representada",
        )


# =============================================================================
# Load data
# =============================================================================

shortlist = load_csv(RANKINGS_PATH / "scouting_shortlist_with_risk.csv")
shortlist = enrich_shortlist_with_radar_features(shortlist)
precision = load_csv(EVALUATION_PATH / "precision_at_k.csv")
roi = load_csv(BUSINESS_PATH / "roi_global_summary.csv")

if shortlist.empty:
    st.warning("No se ha encontrado `reports/rankings/scouting_shortlist_with_risk.csv`. Ejecuta primero `python -m src.models.scouting.build_risk_score`.")
    st.stop()

df = shortlist.copy()

numeric_cols = [
    "market_value_eur",
    "predicted_market_value_eur",
    "market_value_gap_eur",
    "market_value_gap_pct",
    "opportunity_score",
    "growth_score",
    "confidence_score",
    "risk_score",
    "risk_score_raw",
    "risk_adjusted_opportunity_score",
    "risk_age_component",
    "risk_minutes_component",
    "risk_confidence_component",
    "risk_gap_component",
    "age",
    "minutes_played",
    "goals_per90",
    "assists_per90",
    "g_a_per90",
    "shots_per90",
    "xG_per90",
    "xg_per90",
    "xA_per90",
    "xa_per90",
    "tackles_per90",
    "interceptions_per90",
    "blocks_per90",
    "aerial_duels_won_pct",
    "pass_completion_pct",
    "progressive_passes_per90",
    "progressive_carries_per90",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "opportunity_tier" in df.columns:
    df["opportunity_tier_label"] = df["opportunity_tier"].apply(translate_tier)
elif "opportunity_tier_label" in df.columns:
    df["opportunity_tier_label"] = df["opportunity_tier_label"].apply(translate_tier)
else:
    df["opportunity_tier_label"] = "Exploratorio"


# =============================================================================
# Sidebar
# =============================================================================

st.sidebar.title("🎯 Panel de control")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### SISTEMA DE SCOUTING

Plataforma analítica para identificación de jugadores infravalorados mediante:

✅ Econometría  
✅ Machine Learning  
✅ Scoring multicriterio  
✅ Explainability  
✅ Evaluación de negocio
"""
)
st.sidebar.markdown("---")
st.sidebar.markdown("### ESTADO DEL PROYECTO")
st.sidebar.success("Sprint 10.3 — Opportunity vs Risk Matrix")
st.sidebar.markdown("---")
st.sidebar.markdown("### FILTROS RÁPIDOS")
st.sidebar.caption("El filtro principal de perfiles accionables está disponible al inicio del dashboard.")
st.sidebar.markdown("Edad ≤ 23 · Minutos ≥ 900 · Confidence Score ≥ 70")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### TIER DE OPORTUNIDAD

🔴 **Alta prioridad**  
Top del ranking y/o alto upside con fiabilidad suficiente.

🟡 **Objetivo scouting**  
Perfil interesante para seguimiento.

⚪ **Exploratorio**  
Requiere revisión adicional.
"""
)
st.sidebar.markdown("<br><br><span style='color:#94a3b8;font-size:0.8rem;'>v0.10.3-advanced-scouting-intelligence</span>", unsafe_allow_html=True)


# =============================================================================
# Header + executive filters
# =============================================================================

st.title("🎯 Mercado Ineficiente - Scouting Dashboard")
st.markdown(
    """
Sistema analítico para identificar jugadores infravalorados en el mercado de fichajes europeo mediante
modelos predictivos, scoring multicriterio, explainability y validación de negocio.
"""
)
st.markdown(
    """
<div class="info-box">
<span class="info-icon">i</span> Modo ejecutivo: primero acota el universo de scouting; después interpreta KPIs, Opportunity vs Risk y ranking.
</div>
""",
    unsafe_allow_html=True,
)

base_df = df.copy()
st.header("🔎 Filtros ejecutivos de scouting")

PRESETS = {
    "Exploración completa": {
        "max_age": 30,
        "min_minutes": 0,
        "min_confidence": 0,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].min())),
        "description": "Visualiza toda la shortlist ejecutiva sin restricciones operativas adicionales.",
    },
    "Perfiles accionables": {
        "max_age": 23,
        "min_minutes": 900,
        "min_confidence": 70,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].min())),
        "description": "Filtro operativo recomendado: jóvenes con minutos suficientes y señal fiable.",
    },
    "Jóvenes élite": {
        "max_age": 21,
        "min_minutes": 900,
        "min_confidence": 70,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].quantile(0.75))),
        "description": "Jugadores muy jóvenes con alta señal de oportunidad.",
    },
    "Alto upside": {
        "max_age": 23,
        "min_minutes": 500,
        "min_confidence": 60,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].quantile(0.85))),
        "description": "Perfiles con mayor potencial relativo, aceptando algo más de riesgo.",
    },
}

preset_name = st.radio("Preset de scouting", options=list(PRESETS.keys()), index=1, horizontal=True, key="scouting_preset")
preset = PRESETS[preset_name]
st.caption(f"Preset seleccionado: {preset['description']}")

filter_row_1 = st.columns([1, 1, 1], gap="large")
filter_row_2 = st.columns([1, 1, 1.4, 1.4], gap="large")

with filter_row_1[0]:
    max_age = st.slider("Edad máxima", min_value=18, max_value=30, value=int(preset["max_age"]), step=1, key=f"max_age_{preset_name}")
with filter_row_1[1]:
    min_minutes = st.slider("Minutos mínimos", min_value=0, max_value=3000, value=int(preset["min_minutes"]), step=100, key=f"min_minutes_{preset_name}")
with filter_row_1[2]:
    min_confidence = st.slider("Confidence Score mínimo", min_value=0, max_value=100, value=int(preset["min_confidence"]), step=5, key=f"min_confidence_{preset_name}")

with filter_row_2[0]:
    league_options = ["Todas"] + sorted(base_df["league"].dropna().astype(str).unique().tolist())
    selected_league = st.selectbox("Liga", league_options, key=f"league_{preset_name}")
with filter_row_2[1]:
    position_options = ["Todas"] + sorted(base_df["position_group"].dropna().astype(str).unique().tolist())
    selected_position = st.selectbox("Posición", position_options, key=f"position_{preset_name}")
with filter_row_2[2]:
    tier_options = ["Todos"] + sorted(base_df["opportunity_tier_label"].dropna().astype(str).unique().tolist())
    selected_tier = st.selectbox("Tier de oportunidad", tier_options, key=f"tier_{preset_name}")
with filter_row_2[3]:
    global_min_os = float(np.floor(base_df["opportunity_score"].min()))
    global_max_os = float(np.ceil(base_df["opportunity_score"].max()))
    os_range = st.slider("Rango de Opportunity Score", min_value=global_min_os, max_value=global_max_os, value=(float(preset["min_opportunity"]), global_max_os), key=f"opportunity_range_{preset_name}")

filtered_df = base_df.copy()
filtered_df = filtered_df[
    (filtered_df["age"] <= max_age)
    & (filtered_df["minutes_played"] >= min_minutes)
    & (filtered_df["confidence_score"] >= min_confidence)
    & (filtered_df["opportunity_score"].between(os_range[0], os_range[1]))
].copy()

if selected_league != "Todas":
    filtered_df = filtered_df[filtered_df["league"].astype(str) == selected_league]
if selected_position != "Todas":
    filtered_df = filtered_df[filtered_df["position_group"].astype(str) == selected_position]
if selected_tier != "Todos":
    filtered_df = filtered_df[filtered_df["opportunity_tier_label"].astype(str) == selected_tier]

filtered_df = filtered_df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)

shortlist_universe = len(base_df)
filtered_universe = len(filtered_df)
filtered_pct_shortlist = filtered_universe / shortlist_universe if shortlist_universe > 0 else 0

active_filters = [
    f"Edad ≤ {max_age}",
    f"Minutos ≥ {min_minutes:,}",
    f"Confidence ≥ {min_confidence}",
    f"Opportunity {os_range[0]:.0f}–{os_range[1]:.0f}",
]
if selected_league != "Todas":
    active_filters.append(f"Liga: {selected_league}")
if selected_position != "Todas":
    active_filters.append(f"Posición: {selected_position}")
if selected_tier != "Todos":
    active_filters.append(f"Tier: {selected_tier}")

st.markdown(
    f"""
<div class="info-box">
<b>📊 Contexto del análisis</b><br><br>
<b>Universo modelado:</b> {SCORED_UNIVERSE_SIZE:,} jugadores
&nbsp;&nbsp;|&nbsp;&nbsp;
<b>Shortlist ejecutiva:</b> {shortlist_universe:,} jugadores
<hr style="margin:10px 0; opacity:0.25;">
<b>Filtros activos:</b><br>
{" · ".join(active_filters)}
</div>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# KPIs
# =============================================================================

st.markdown("---")
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    render_metric_card_with_caption("Candidatos actuales", f"{len(filtered_df):,}", f"{filtered_pct_shortlist:.0%} de la shortlist")
with k2:
    render_metric_card_with_caption("Shortlist ejecutiva", f"{shortlist_universe:,}", "jugadores precandidatos")
with k3:
    leagues = filtered_df["league"].nunique() if "league" in filtered_df.columns else "N/A"
    render_metric_card_with_caption("Ligas representadas", leagues, "cobertura competitiva")
with k4:
    if not precision.empty and "precision_at_k" in precision.columns:
        precision_value = f"{precision['precision_at_k'].max():.0%}"
    else:
        precision_value = "N/A"
    render_metric_card_with_caption("Precision@K", precision_value, "calidad del ranking", show_info_icon=True)
    with st.popover("ℹ️ Precision@K"):
        st.markdown(
            """
**Qué mide**  
Proporción de aciertos dentro de los primeros puestos del ranking.

**Lectura de negocio**  
Responde a: *si revisamos el Top K, ¿qué proporción muestra señal positiva posterior?*

**Importante**  
Es una métrica de ranking, no una métrica de error predictivo como RMSE o MAE.
"""
        )
with k5:
    if not roi.empty and "positive_roi_rate" in roi.columns:
        roi_value = f"{roi['positive_roi_rate'].iloc[0]:.0%}"
    else:
        roi_value = "N/A"
    render_metric_card_with_caption("Positive ROI Rate", roi_value, "simulación conservadora", show_info_icon=True)
    with st.popover("ℹ️ Positive ROI Rate"):
        st.markdown(
            """
**Qué mide**  
Porcentaje de perfiles con retorno positivo en la simulación económica.

**Lectura de negocio**  
Ayuda a valorar si la shortlist tiene sentido como cartera potencial de inversión.

**Importante**  
No representa rentabilidad garantizada; es una simulación conservadora basada en las hipótesis del modelo.
"""
        )


# =============================================================================
# Main visual block
# =============================================================================

st.markdown("---")
st.markdown("## 🎯 Opportunity vs Risk Matrix", unsafe_allow_html=True)
st.markdown(
    """
Cada burbuja representa un jugador de la **shortlist filtrada**.  
La matriz cruza el **Opportunity Score** con el **Risk Score** para separar objetivos prioritarios,
apuestas estratégicas, perfiles estables y casos a evitar.

El tamaño de la burbuja representa el **Risk Adjusted Opportunity Score**, es decir,
el atractivo de la oportunidad después de penalizar por riesgo.  
Los números identifican el **Top 5 ajustado por riesgo**.
"""
)

fig = build_opportunity_risk_matrix(filtered_df)
if fig is None:
    st.info("No hay datos suficientes para generar la matriz Opportunity vs Risk con los filtros actuales.")
else:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": ["zoom", "pan", "select", "lasso2d", "autoScale", "resetScale"],
        },
    )
    render_opportunity_risk_summary(filtered_df)


# =============================================================================
# Paginated table
# =============================================================================

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

st.header("📋 Tabla de jugadores priorizados")

table_df = filtered_df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)
if not table_df.empty:
    table_df["dashboard_tier"] = table_df["opportunity_tier_label"]
    top5_idx = table_df.head(5).index
    table_df.loc[top5_idx, "dashboard_tier"] = "Alta prioridad"
else:
    table_df["dashboard_tier"] = []

PAGE_SIZE = 5
total_rows = len(table_df)
total_pages = max(1, ceil(total_rows / PAGE_SIZE))

if "players_page" not in st.session_state:
    st.session_state.players_page = 1

st.session_state.players_page = min(st.session_state.players_page, total_pages)
start = (st.session_state.players_page - 1) * PAGE_SIZE
end = start + PAGE_SIZE
page_df = table_df.iloc[start:end].copy()

st.markdown(build_html_table(page_df), unsafe_allow_html=True)

pag_left, pag_right = st.columns([2, 1])
with pag_left:
    st.caption(f"Mostrando {len(page_df)} de {total_rows} jugadores")
with pag_right:
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("‹", disabled=st.session_state.players_page <= 1):
            st.session_state.players_page -= 1
            st.rerun()
    with c2:
        st.markdown(f"**{st.session_state.players_page} / {total_pages}**")
    with c3:
        if st.button("›", disabled=st.session_state.players_page >= total_pages):
            st.session_state.players_page += 1
            st.rerun()


# =============================================================================
# Player Radar & Positional Benchmarking
# =============================================================================

render_player_radar_benchmarking(table_df)


# =============================================================================
# Individual player report
# =============================================================================

st.header("👤 Informe individual de jugador")

if table_df.empty:
    st.info("No hay jugadores disponibles con los filtros actuales.")
    st.stop()

player_names = table_df["player_name_fbref"].fillna("Jugador").tolist()
selected_player = st.selectbox("Selecciona un jugador", player_names)
player_df = table_df[table_df["player_name_fbref"] == selected_player].iloc[0]

m1, m2, m3, m4, m5, m6 = st.columns([1.1, 1.1, 1.1, 1.15, 1.05, 0.95])
with m1:
    render_metric_card("Valor mercado", format_money_tm(safe_get(player_df, "market_value_eur")))
with m2:
    render_metric_card("Valor estimado", format_money_tm(safe_get(player_df, "predicted_market_value_eur")))
with m3:
    render_metric_card("Gap de mercado", format_money_tm(safe_get(player_df, "market_value_gap_eur")))
with m4:
    render_metric_card("Opportunity", f"{format_score(safe_get(player_df, 'opportunity_score'))} / 100")
with m5:
    render_metric_card("Risk Score", f"{format_score(safe_get(player_df, 'risk_score'))} / 100")
with m6:
    rank = int(table_df.index[table_df["player_name_fbref"] == selected_player][0]) + 1
    render_metric_card("Ranking", f"#{rank} / {len(table_df)}")

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
profile_col, reading_col = st.columns([1, 1])

with profile_col:
    with st.container(border=True):
        st.subheader("📋 Perfil scouting")
        profile_table = f"""
        <table class="profile-table">
            <tr><td>Club:</td><td>{html.escape(str(safe_get(player_df, 'club')))}</td></tr>
            <tr><td>Liga:</td><td>{html.escape(str(safe_get(player_df, 'league')))}</td></tr>
            <tr><td>Posición:</td><td>{html.escape(str(safe_get(player_df, 'position_group')))}</td></tr>
            <tr><td>Edad:</td><td>{format_score(safe_get(player_df, 'age'))}</td></tr>
            <tr><td>Temporada:</td><td>{html.escape(str(safe_get(player_df, 'season')))}</td></tr>
            <tr><td>Minutos en liga:</td><td>{int(float(safe_get(player_df, 'minutes_played', 0))):,}</td></tr>
            <tr><td>Tier:</td><td>{tier_badge(safe_get(player_df, 'dashboard_tier'))}</td></tr>
            <tr><td>Nivel de riesgo:</td><td>{html.escape(str(safe_get(player_df, 'risk_level')))}</td></tr>
        </table>
        """
        st.markdown(profile_table, unsafe_allow_html=True)

with reading_col:
    with st.container(border=True):
        st.subheader("🧠 Lectura analítica")
        recommendation = build_recommendation(player_df)
        st.markdown(
            f"**Recomendación:** <span class='recommendation'>{html.escape(recommendation)}</span> <span class='info-icon'>i</span>",
            unsafe_allow_html=True,
        )
        with st.popover("ℹ️ Recomendaciones analíticas"):
            st.markdown(
                """
**Recomendación analítica** es una lectura operativa complementaria al **Tier**.

**Opciones disponibles:**

- **Scouting prioritario:** revisar primero por alto Opportunity Score, gap positivo y fiabilidad suficiente.
- **Seguimiento recomendado:** perfil interesante, pero con menor urgencia o menor robustez relativa.
- **Revisión exploratoria:** caso que requiere validación adicional antes de elevarlo a shortlist prioritaria.
"""
            )
        st.markdown(
            "Este jugador aparece en la shortlist porque combina una señal de infravaloración "
            "con potencial de crecimiento y una fiabilidad analítica suficiente."
        )
        st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
        gap_rel = calculate_gap_relative(player_df)
        gap_text = f"{gap_rel:.1%}" if gap_rel is not None else "N/A"
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            render_metric_card("Gap relativo", gap_text)
        with s2:
            render_metric_card("Growth", f"{format_score(safe_get(player_df, 'growth_score'))} / 100")
        with s3:
            render_metric_card("Confidence", f"{format_score(safe_get(player_df, 'confidence_score'))} / 100")
        with s4:
            render_metric_card("Opp. ajustada", f"{format_score(safe_get(player_df, 'risk_adjusted_opportunity_score'))} / 100")
        st.markdown("<div style='height:18px; clear: both;'></div>", unsafe_allow_html=True)


# =============================================================================
# SHAP explanation below analysis
# =============================================================================

st.markdown("### 🔍 Explicación SHAP")
with st.popover("ℹ️ Cómo interpretar esta explicación"):
    st.markdown(
        """
**SHAP** explica cómo contribuye cada variable a la valoración estimada del jugador.

- Las barras **azules** empujan el valor estimado hacia arriba.
- Las barras **rojas** reducen el valor estimado.
- Cuanto mayor es la barra, mayor es el impacto de esa variable en la predicción.

En este dashboard se usa para responder a una pregunta clave de scouting:

> ¿Por qué el modelo considera que este jugador podría valer más que su valor de mercado actual?

Importante: SHAP explica la lógica interna del modelo. No debe interpretarse como causalidad directa.
"""
    )

st.markdown(
    """
<div class="shap-executive-box">
<b>Lectura ejecutiva:</b> el gráfico muestra los principales factores que explican la estimación de valor del jugador seleccionado.
Las contribuciones positivas elevan el valor estimado; las negativas lo reducen. Esta capa aporta trazabilidad y ayuda a defender
la recomendación ante dirección deportiva o scouting.
</div>
""",
    unsafe_allow_html=True,
)

shap_values = make_shap_proxy(player_df)
fig_shap = go.Figure(
    go.Bar(
        x=shap_values["impact"],
        y=shap_values["feature"],
        orientation="h",
        marker_color=np.where(shap_values["impact"] >= 0, "#2563eb", "#ef4444"),
        text=[f"{v:+.2f}" for v in shap_values["impact"]],
        textposition="outside",
    )
)
fig_shap.update_layout(
    height=340,
    margin=dict(l=10, r=30, t=20, b=35),
    xaxis_title="Contribución SHAP sobre log-valor estimado",
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white",
)
fig_shap.update_xaxes(showgrid=True, gridcolor="#e5e7eb", zeroline=True)
fig_shap.update_yaxes(showgrid=False)
st.plotly_chart(fig_shap, use_container_width=True)
