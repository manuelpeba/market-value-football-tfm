from pathlib import Path
from math import ceil
import html
import textwrap

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]

RANKINGS_PATH = ROOT / "reports" / "rankings"
BUSINESS_PATH = ROOT / "reports" / "business"
EVALUATION_PATH = ROOT / "reports" / "evaluation"

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
    padding-top: 1.15rem;
    padding-bottom: 2rem;
    max-width: 1540px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061b37 0%, #062b57 100%);
}

[data-testid="stSidebar"] * {
    color: white;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    min-height: 86px;
}

.metric-label {
    color: #64748b;
    font-size: 0.84rem;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-size: 1.75rem;
    font-weight: 850;
    color: #0f172a;
}

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
    font-size: 0.92rem;
    margin-bottom: 0.5rem;
}

.helper-caption {
    color: #64748b;
    font-size: 0.80rem;
    margin-top: 5px;
    margin-bottom: 2px;
}

.player-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    background: white;
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    overflow: hidden;
}

.player-table th {
    background: #f8fafc;
    color: #334155;
    font-weight: 800;
    padding: 11px 10px;
    border-bottom: 1px solid #e6eaf0;
    text-align: left;
}

.player-table td {
    padding: 10px;
    border-bottom: 1px solid #edf2f7;
    color: #0f172a;
    vertical-align: middle;
}

.badge-red {
    background: #ef4444;
    color: white;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.76rem;
    display: inline-block;
}

.badge-yellow {
    background: #facc15;
    color: #422006;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.76rem;
    display: inline-block;
}

.badge-gray {
    background: #e5e7eb;
    color: #374151;
    padding: 5px 9px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.76rem;
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

.profile-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
}
.profile-table td {
    padding: 5px 4px;
    vertical-align: top;
    font-size: 0.92rem;
}
.profile-table td:first-child {
    color: #334155;
    font-weight: 800;
    width: 155px;
}

.shap-executive-box {
    border: 1px solid #e6eaf0;
    border-radius: 12px;
    padding: 14px 18px;
    background: #f8fafc;
    margin-bottom: 12px;
    color: #334155;
}

/* separa los popovers de ayuda de la tarjeta superior */
div[data-testid="stPopover"] {
    margin-top: 8px;
}

.bubble-side-card {
    margin-top: 44px;
    padding: 16px 16px 14px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    font-size: 0.84rem;
    color: #0f172a;
}
.bubble-side-title {
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 10px;
    font-size: 0.86rem;
}
.bubble-legend-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 9px 0;
    white-space: nowrap;
}
.legend-dot {
    display: inline-block;
    border-radius: 50%;
    border: 1px solid rgba(15, 23, 42, 0.22);
    flex: 0 0 auto;
}
.legend-red { background: #ef4444; width: 14px; height: 14px; }
.legend-yellow { background: #facc15; width: 14px; height: 14px; }
.legend-gray { background: #9ca3af; width: 14px; height: 14px; }
.legend-size-row {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 8px;
    margin: 10px 0 6px 0;
}
.legend-size-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    color: #334155;
    font-size: 0.74rem;
}
.legend-size-dot {
    display: inline-block;
    border-radius: 50%;
    background: rgba(156, 163, 175, 0.58);
    border: 1px solid rgba(15, 23, 42, 0.22);
}
.legend-size-70 { width: 16px; height: 16px; }
.legend-size-85 { width: 27px; height: 27px; }
.legend-size-100 { width: 42px; height: 42px; }
.legend-divider {
    height: 1px;
    background: #e5e7eb;
    margin: 14px 0 14px 0;
}
.top5-player-row {
    display: grid;
    grid-template-columns: 24px 1fr;
    grid-template-rows: auto auto;
    column-gap: 8px;
    align-items: center;
    line-height: 1.12;
    margin: 8px 0;
}
.top5-rank {
    grid-row: 1 / span 2;
    width: 21px;
    height: 21px;
    border-radius: 50%;
    background: #ef4444;
    color: white;
    font-weight: 900;
    font-size: 0.74rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.18);
}
.top5-player-name {
    color: #0f172a;
    font-weight: 850;
    font-size: 0.80rem;
}
.top5-player-club {
    color: #64748b;
    font-size: 0.70rem;
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


def build_money_slider_options(min_value, max_value, n=72):
    min_value = float(min_value)
    max_value = float(max_value)

    if min_value <= 0 or max_value <= 0 or min_value >= max_value:
        return [min_value, max_value]

    values = np.geomspace(min_value, max_value, n)
    rounded = []
    for value in values:
        if value < 1_000_000:
            rounded.append(round(value / 50_000) * 50_000)
        elif value < 10_000_000:
            rounded.append(round(value / 100_000) * 100_000)
        else:
            rounded.append(round(value / 500_000) * 500_000)

    options = sorted(set([min_value, max_value] + rounded))
    return [v for v in options if min_value <= v <= max_value]


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
            elif col in ["growth_score", "confidence_score", "opportunity_score"]:
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


def size_series_from_scores(scores: pd.Series) -> pd.Series:
    """Escala visual diferencial basada en Opportunity Score para el gráfico principal."""
    scores = pd.to_numeric(scores, errors="coerce").fillna(60).clip(60, 100)
    min_s, max_s = float(scores.min()), float(scores.max())

    if max_s - min_s < 3:
        # Si el Top 15 está muy concentrado, mantenemos jerarquía visual por score
        # sin romper el significado: mayor score sigue siendo mayor burbuja.
        ranks = scores.rank(method="first", ascending=True)
        norm = (ranks - ranks.min()) / max((ranks.max() - ranks.min()), 1)
    else:
        norm = (scores - min_s) / (max_s - min_s)

    return 20 + (norm ** 1.65) * 52


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
    """Leyenda horizontal compacta debajo del gráfico."""

    col_tier, col_size, col_top5 = st.columns([1.1, 1.1, 2.4], gap="large")

    with col_tier:
        with st.container(border=True):
            st.markdown("**Tier de oportunidad**")
            st.markdown("🔴 Alta prioridad")
            st.markdown("🟡 Objetivo scouting")
            st.markdown("⚪ Exploratorio")

    with col_size:
        with st.container(border=True):
            st.markdown("**Opportunity Score**")
            st.markdown("● 70 &nbsp;&nbsp; ⬤ 85 &nbsp;&nbsp; ⬤ 100", unsafe_allow_html=True)
            st.caption("A mayor score, mayor tamaño de burbuja.")

    with col_top5:
        with st.container(border=True):
            st.markdown("**🎯 Top 5 destacados**")

            if top5_players is not None and not top5_players.empty:
                cols = st.columns(5)

                for idx, row in top5_players.reset_index(drop=True).iterrows():
                    with cols[idx]:
                        st.markdown(f"**{idx + 1}. {get_player_name(row)}**")
                        st.caption(str(safe_get(row, "club", "")))
            else:
                st.caption("No hay jugadores destacados con los filtros actuales.")


def build_opportunity_chart(chart_source: pd.DataFrame) -> go.Figure | None:
    """
    Executive bubble chart for the scouting shortlist.

    Design decisions:
    - Only Top 15 filtered players to reduce visual noise.
    - Top 5 are forced to Alta prioridad, highlighted in red.
    - Top 5 have both a number inside the bubble and a boxed callout with arrow.
    - Bubble size is intentionally non-linear to make Opportunity Score visually meaningful.
    """
    required = {"market_value_eur", "market_value_gap_eur", "opportunity_score"}
    if not required.issubset(chart_source.columns):
        return None

    chart_df = chart_source.dropna(subset=list(required)).copy()
    chart_df = chart_df[
        (chart_df["market_value_eur"] > 0)
        & (chart_df["market_value_gap_eur"] > 0)
    ].copy()

    if chart_df.empty:
        return None

    chart_df = chart_df.sort_values("opportunity_score", ascending=False).head(12).copy()
    chart_df["dashboard_tier"] = chart_df.get("opportunity_tier_label", "Exploratorio")

    top5_idx_chart = chart_df.sort_values("opportunity_score", ascending=False).head(5).index
    chart_df.loc[top5_idx_chart, "dashboard_tier"] = "Alta prioridad"

    # Stronger non-linear sizing: clearer differentiation than proportional raw score.
    min_score = float(chart_df["opportunity_score"].min())
    max_score = float(chart_df["opportunity_score"].max())
    score_span = max(max_score - min_score, 1.0)
    scaled = ((chart_df["opportunity_score"] - min_score) / score_span).clip(0, 1)
    chart_df["bubble_size"] = 18 + (scaled ** 1.7) * 54

    color_map = {
        "Alta prioridad": "#ef4444",
        "Objetivo scouting": "#facc15",
        "Exploratorio": "#9ca3af",
        "Bajo riesgo": "#22c55e",
    }

    fig = go.Figure()

    non_top5 = chart_df.drop(index=top5_idx_chart, errors="ignore")
    top5 = chart_df.loc[top5_idx_chart].sort_values("opportunity_score", ascending=False).reset_index(drop=True)

    # Non-top-5: draw first, softer opacity.
    for tier_name in ["Exploratorio", "Objetivo scouting", "Bajo riesgo"]:
        tier_df = non_top5[non_top5["dashboard_tier"] == tier_name]
        if tier_df.empty:
            continue

        hover_text = [
            f"<b>{get_player_name(row)}</b><br>"
            f"Club: {safe_get(row, 'club')}<br>"
            f"Liga: {safe_get(row, 'league')}<br>"
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
                    opacity=0.70,
                    line=dict(width=1.1, color="rgba(15, 23, 42, 0.22)"),
                ),
                showlegend=False,
            )
        )

    # Top 5: draw above the rest with stronger border.
    hover_text_top5 = [
        f"<b>{i + 1}. {get_player_name(row)}</b><br>"
        f"Club: {safe_get(row, 'club')}<br>"
        f"Liga: {safe_get(row, 'league')}<br>"
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
            name="Alta prioridad",
            hovertext=hover_text_top5,
            hoverinfo="text",
            cliponaxis=False,
            marker=dict(
                size=np.maximum(top5["bubble_size"].to_numpy(), 54),
                color="#ef4444",
                opacity=0.88,
                line=dict(width=2.4, color="rgba(15, 23, 42, 0.55)"),
            ),
            showlegend=False,
        )
    )

    # Rank numbers inside Top 5 bubbles: unambiguous association even in dense areas.
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

    # Boxed callouts with leader lines. Offsets are rank-specific to avoid overlap.
    label_offsets = [
        (88, -36),    # 1
        (96, -72),    # 2
        (90, 24),     # 3
        (118, 74),    # 4
        (132, 116),   # 5
    ]

    for i, row in top5.iterrows():
        ax, ay = label_offsets[i] if i < len(label_offsets) else (90, -40)
        fig.add_annotation(
            x=row["market_value_eur"],
            y=row["market_value_gap_eur"],
            text=f"<b>{i + 1}. {get_player_name(row)}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.8,
            arrowcolor="#64748b",
            ax=ax,
            ay=ay,
            xanchor="left",
            yanchor="middle",
            bgcolor="rgba(255,255,255,0.98)",
            bordercolor="#cbd5e1",
            borderwidth=1.2,
            borderpad=5,
            opacity=0.98,
            font=dict(size=11, color="#0f172a"),
        )

    # Axis padding leaves room for callout boxes while keeping the plot compact.
    x_min = max(float(chart_df["market_value_eur"].min()) * 0.70, 50_000)
    x_max = float(chart_df["market_value_eur"].max()) * 1.90
    y_min = max(float(chart_df["market_value_gap_eur"].min()) * 0.62, 50_000)
    y_max = float(chart_df["market_value_gap_eur"].max()) * 1.55

    fig.update_layout(
        height=520,
        margin=dict(l=10, r=16, t=10, b=10),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Valor de mercado actual (€) — escala log",
        yaxis_title="Gap de mercado estimado (€)",
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
        tickvals=[50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000],
        ticktext=["50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M"],
    )

    return fig


# =============================================================================
# Load data
# =============================================================================

shortlist = load_csv(RANKINGS_PATH / "scouting_shortlist.csv")
precision = load_csv(EVALUATION_PATH / "precision_at_k.csv")
roi = load_csv(BUSINESS_PATH / "roi_global_summary.csv")

if shortlist.empty:
    st.warning("No se ha encontrado `reports/rankings/scouting_shortlist.csv`.")
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
    "age",
    "minutes_played",
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
st.sidebar.success("Sprint 7 — Dashboard")
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
st.sidebar.markdown("<br><br><span style='color:#94a3b8;font-size:0.8rem;'>v0.7.0</span>", unsafe_allow_html=True)


# =============================================================================
# Header + actionable filter
# =============================================================================

st.title("🎯 Mercado Ineficiente - Scouting Dashboard")
st.markdown(
    """
Sistema analítico para identificar jugadores infravalorados en el mercado de fichajes europeo mediante
modelos predictivos, scoring multicriterio y validación de negocio.
"""
)
st.markdown(
    """
<div class="info-box">
<span class="info-icon">i</span> Modo scouting operativo: filtra jugadores con edad ≤ 23, minutos ≥ 900 y Confidence Score ≥ 70.
</div>
""",
    unsafe_allow_html=True,
)

top_actionable_filter = st.checkbox(
    "Mostrar solo perfiles accionables",
    value=True,
    help="Aplica filtros mínimos de edad, exposición competitiva y fiabilidad analítica.",
)

if top_actionable_filter and {"age", "minutes_played", "confidence_score"}.issubset(df.columns):
    df = df[
        (df["age"] <= 23)
        & (df["minutes_played"] >= 900)
        & (df["confidence_score"] >= 70)
    ].copy()


# =============================================================================
# KPIs
# =============================================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    render_metric_card("Jugadores en shortlist", f"{len(df):,}")

with k2:
    leagues = df["league"].nunique() if "league" in df.columns else "N/A"
    render_metric_card("Ligas representadas", leagues)

with k3:
    if not precision.empty and "precision_at_k" in precision.columns:
        precision_value = f"{precision['precision_at_k'].max():.2f}"
    else:
        precision_value = "N/A"
    render_metric_card("Precisión del ranking", precision_value, show_info_icon=True)
    with st.popover("ℹ️ Precisión del ranking"):
        st.markdown(
            """
**Qué mide**  
Proporción de aciertos entre los primeros puestos del ranking.

**Lectura de negocio**  
Responde a: *si revisamos el Top K, ¿qué proporción muestra una señal positiva posterior?*

**Uso recomendado**  
Sirve para validar si el ranking concentra buenos candidatos al inicio, que es donde mira primero un equipo de scouting.
"""
        )

with k4:
    if not roi.empty and "positive_roi_rate" in roi.columns:
        roi_value = f"{roi['positive_roi_rate'].iloc[0]:.0%}"
    else:
        roi_value = "N/A"
    render_metric_card("% oportunidades rentables", roi_value, show_info_icon=True)
    with st.popover("ℹ️ % oportunidades rentables"):
        st.markdown(
            """
**Qué mide**  
Proporción de perfiles de la shortlist con ROI positivo en la simulación de negocio.

**Lectura de negocio**  
Indica qué parte del universo filtrado tendría retorno económico positivo bajo las hipótesis del modelo.

**Uso recomendado**  
Debe interpretarse como una aproximación de valor esperado, no como garantía de rentabilidad real.
"""
        )


# =============================================================================
# Main visual block + horizontal scouting filters
# =============================================================================

# The chart container is declared before the filters container so the visual block
# remains above the filters, while the chart is still built with the filtered data.
chart_section = st.container()
filters_section = st.container()
filtered_df = df.copy()

with filters_section:
    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    st.header("🔎 Filtros de scouting")

    filter_row_1 = st.columns(3, gap="large")
    filter_row_2 = st.columns([1.05, 1.05, 1.35, 1.35], gap="large")

    with filter_row_1[0]:
        if "league" in filtered_df.columns:
            leagues = ["Todas"] + sorted(filtered_df["league"].dropna().unique().tolist())
            selected_league = st.selectbox("Liga", leagues)
            if selected_league != "Todas":
                filtered_df = filtered_df[filtered_df["league"] == selected_league]

    with filter_row_1[1]:
        if "position_group" in filtered_df.columns:
            positions = ["Todas"] + sorted(filtered_df["position_group"].dropna().unique().tolist())
            selected_position = st.selectbox("Posición", positions)
            if selected_position != "Todas":
                filtered_df = filtered_df[filtered_df["position_group"] == selected_position]

    with filter_row_1[2]:
        if "opportunity_tier_label" in filtered_df.columns:
            tiers = ["Todos"] + sorted(filtered_df["opportunity_tier_label"].dropna().unique().tolist())
            selected_tier = st.selectbox("Tier de oportunidad", tiers)
            if selected_tier != "Todos":
                filtered_df = filtered_df[filtered_df["opportunity_tier_label"] == selected_tier]

    with filter_row_2[0]:
        if "club" in filtered_df.columns:
            clubs = ["Todos"] + sorted(filtered_df["club"].dropna().unique().tolist())
            selected_club = st.selectbox("Club / equipo", clubs)
            if selected_club != "Todos":
                filtered_df = filtered_df[filtered_df["club"] == selected_club]

    with filter_row_2[1]:
        if "season" in filtered_df.columns:
            seasons = ["Todas"] + sorted(filtered_df["season"].dropna().unique().tolist())
            selected_season = st.selectbox("Temporada analizada", seasons)
            if selected_season != "Todas":
                filtered_df = filtered_df[filtered_df["season"] == selected_season]

    with filter_row_2[2]:
        if "market_value_eur" in filtered_df.columns and not filtered_df.empty:
            min_mv = float(filtered_df["market_value_eur"].min())
            max_mv = float(filtered_df["market_value_eur"].max())
            if min_mv < max_mv:
                mv_options = build_money_slider_options(min_mv, max_mv)
                mv_range = st.select_slider(
                    "Rango de valor de mercado actual (€)",
                    options=mv_options,
                    value=(mv_options[0], mv_options[-1]),
                    format_func=format_money_readable,
                )
            else:
                mv_range = (min_mv, max_mv)
                st.caption(f"Rango de valor de mercado actual: {format_money_readable(min_mv)}")

            st.caption(
                f"Rango seleccionado: {format_money_readable(mv_range[0])} — "
                f"{format_money_readable(mv_range[1])}"
            )
            filtered_df = filtered_df[filtered_df["market_value_eur"].between(mv_range[0], mv_range[1])]

    with filter_row_2[3]:
        if "opportunity_score" in filtered_df.columns and not filtered_df.empty:
            min_os = float(np.floor(filtered_df["opportunity_score"].min()))
            max_os = float(np.ceil(filtered_df["opportunity_score"].max()))
            os_range = st.slider(
                "Rango de Opportunity Score",
                min_value=min_os,
                max_value=max_os,
                value=(min_os, max_os),
            )
            filtered_df = filtered_df[filtered_df["opportunity_score"].between(os_range[0], os_range[1])]

with chart_section:
    st.markdown(
        "## 💎 Coste actual vs upside estimado <span class='info-icon'>i</span>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
Cada burbuja representa un jugador del **Top 12 filtrado**. El tamaño indica el **Opportunity Score**.  
Los **5 mejores jugadores** están destacados en rojo y numerados.
"""
    )

    fig = build_opportunity_chart(filtered_df)

    if fig is None:
        st.info("No hay datos suficientes para generar el gráfico.")
    else:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom",
                    "pan",
                    "select",
                    "lasso2d",
                    "autoScale",
                    "resetScale",
                ],
            },
        )

        top5_legend_df = (
            filtered_df
            .sort_values("opportunity_score", ascending=False)
            .head(5)
            .reset_index(drop=True)
        )

        render_bubble_legend(top5_legend_df)

# =============================================================================
# Paginated table
# =============================================================================

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
# Individual player report
# =============================================================================

st.header("👤 Informe individual de jugador")

if table_df.empty:
    st.info("No hay jugadores disponibles con los filtros actuales.")
    st.stop()

player_names = table_df["player_name_fbref"].fillna("Jugador").tolist()
selected_player = st.selectbox("Selecciona un jugador", player_names)
player_df = table_df[table_df["player_name_fbref"] == selected_player].iloc[0]

m1, m2, m3, m4, m5 = st.columns([1.2, 1.2, 1.2, 1.25, 1.1])
with m1:
    render_metric_card("Valor mercado", format_money_tm(safe_get(player_df, "market_value_eur")))
with m2:
    render_metric_card("Valor estimado", format_money_tm(safe_get(player_df, "predicted_market_value_eur")))
with m3:
    render_metric_card("Gap de mercado", format_money_tm(safe_get(player_df, "market_value_gap_eur")))
with m4:
    render_metric_card("Opportunity Score", f"{format_score(safe_get(player_df, 'opportunity_score'))} / 100")
with m5:
    rank = int(table_df.index[table_df["player_name_fbref"] == selected_player][0]) + 1
    render_metric_card("Ranking", f"#{rank} / {len(table_df)}")

# Espacio visual entre las tarjetas superiores y los bloques de análisis
st.markdown(
    """
    <div style="height:28px;"></div>
    """,
    unsafe_allow_html=True,
)

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

        # Espacio interno para que las métricas no queden pegadas al texto
        st.markdown(
            """
            <div style="height:24px;"></div>
            """,
            unsafe_allow_html=True,
        )

        gap_rel = calculate_gap_relative(player_df)
        gap_text = f"{gap_rel:.1%}" if gap_rel is not None else "N/A"
        s1, s2, s3 = st.columns(3)
        with s1:
            render_metric_card("Gap relativo estimado", gap_text)
        with s2:
            render_metric_card("Growth Score", f"{format_score(safe_get(player_df, 'growth_score'))} / 100")
        with s3:
            render_metric_card("Confidence Score", f"{format_score(safe_get(player_df, 'confidence_score'))} / 100")

        # Aire inferior controlado dentro de la caja de lectura analítica
        st.markdown(
            """
            <div style="height:18px; clear: both;"></div>
            """,
            unsafe_allow_html=True,
        )


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
