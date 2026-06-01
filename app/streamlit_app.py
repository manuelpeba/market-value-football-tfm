from pathlib import Path
from math import ceil
import html

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]

RANKINGS_PATH = ROOT / "reports" / "rankings"
BUSINESS_PATH = ROOT / "reports" / "business"
EVALUATION_PATH = ROOT / "reports" / "evaluation"

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

    fig.add_vline(x=cost_ref, line_dash="dash", line_color="rgba(15, 23, 42, 0.45)", line_width=1.2, annotation_text="Coste mediano", annotation_position="top")
    fig.add_hline(y=upside_ref, line_dash="dash", line_color="rgba(15, 23, 42, 0.45)", line_width=1.2, annotation_text="Upside mediano", annotation_position="right")

    quadrant_annotations = [
        (0.18, 0.90, "<b>🟢 Comprar / priorizar</b>", "#22c55e", "#166534"),
        (0.78, 0.90, "<b>🔵 Oportunidades premium</b>", "#3b82f6", "#1d4ed8"),
        (0.18, 0.18, "<b>🟡 Seguimiento</b>", "#facc15", "#854d0e"),
        (0.78, 0.18, "<b>🔴 Menor prioridad</b>", "#ef4444", "#991b1b"),
    ]
    for x, y, text, border, color in quadrant_annotations:
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=x,
            y=y,
            text=text,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor=border,
            borderwidth=1,
            borderpad=5,
            font=dict(size=13, color=color),
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
st.sidebar.success("Sprint 9 — Dashboard productizado")
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
st.sidebar.markdown("<br><br><span style='color:#94a3b8;font-size:0.8rem;'>v0.9.0-dashboard-product</span>", unsafe_allow_html=True)


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
<span class="info-icon">i</span> Modo ejecutivo: primero acota el universo de scouting; después interpreta KPIs, coste vs upside y ranking.
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
st.markdown("## 💎 Coste actual vs upside estimado", unsafe_allow_html=True)
st.markdown(
    """
Cada burbuja representa un jugador del **Top 20 filtrado**.  
La matriz divide el mercado en cuatro zonas estratégicas según **coste actual** y **upside estimado**.  
El tamaño representa el **Opportunity Score** y los números identifican el **Top 5** del ranking actual.
"""
)

fig = build_opportunity_chart(filtered_df)
if fig is None:
    st.info("No hay datos suficientes para generar el gráfico con los filtros actuales.")
else:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": ["zoom", "pan", "select", "lasso2d", "autoScale", "resetScale"],
        },
    )

    top5_legend_df = filtered_df.sort_values("opportunity_score", ascending=False).head(5).reset_index(drop=True)
    render_bubble_legend(top5_legend_df)
    render_chart_executive_summary(filtered_df)


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
        s1, s2, s3 = st.columns(3)
        with s1:
            render_metric_card("Gap relativo estimado", gap_text)
        with s2:
            render_metric_card("Growth Score", f"{format_score(safe_get(player_df, 'growth_score'))} / 100")
        with s3:
            render_metric_card("Confidence Score", f"{format_score(safe_get(player_df, 'confidence_score'))} / 100")
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
