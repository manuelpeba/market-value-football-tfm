from pathlib import Path
from math import ceil
import html
import sys

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
STRATEGY_REPORTS_PATH = ROOT / "reports" / "strategy"
STRATEGY_SRC_PATH = ROOT / "src" / "strategy"

SCORED_UNIVERSE_SIZE = 1_138

st.set_page_config(
    page_title="Scouting IQ - Market Value Intelligence",
    page_icon="⚽",
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
   Compact executive tables
   ========================= */

.comparison-table-wrapper {
    width: 100%;
    overflow-x: auto;
    border-radius: 12px;
}

.comparison-table-wrapper .player-table {
    table-layout: auto;
    font-size: 0.76rem;
}

.comparison-table-wrapper .player-table th,
.comparison-table-wrapper .player-table td {
    padding: 8px 7px;
}

.executive-recommendation-card {
    background: linear-gradient(135deg, #f8fafc 0%, #eef6ff 100%);
    border: 1px solid #dbeafe;
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.055);
    margin-bottom: 18px;
}

.executive-recommendation-title {
    color: #475569;
    font-size: 0.82rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
}

.executive-recommendation-player {
    color: #0f172a;
    font-size: 1.85rem;
    font-weight: 950;
    line-height: 1.05;
}

.executive-recommendation-badge {
    display: inline-block;
    margin-top: 10px;
    padding: 7px 11px;
    border-radius: 999px;
    background: #ef4444;
    color: white;
    font-weight: 900;
    font-size: 0.76rem;
}

.executive-recommendation-reasons {
    color: #334155;
    font-size: 0.90rem;
    margin-top: 12px;
    line-height: 1.5;
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



/* =========================
   Scouting IQ visual refactor
   ========================= */
html, body, [data-testid="stAppViewContainer"] {
    background: #f5f7fb;
}

.block-container {
    padding-top: 0.75rem;
    max-width: 1680px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07172c 0%, #0b2545 45%, #07172c 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.25);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #eaf2ff !important;
}

[data-testid="stSidebar"] .stSlider p,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #dbeafe !important;
}

.scouting-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, #061426 0%, #0b1f3a 48%, #0f2f5f 100%);
    color: white;
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 16px;
    padding: 14px 20px;
    margin: 0 0 16px 0;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
}

.scouting-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 900;
    letter-spacing: 0.03em;
    font-size: 1.12rem;
}

.scouting-brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    color: #0b1f3a;
    font-weight: 900;
}

.scouting-topbar-center {
    flex: 1;
    margin: 0 28px;
    border: 1px solid rgba(226, 232, 240, 0.16);
    background: rgba(15, 23, 42, 0.40);
    border-radius: 10px;
    padding: 9px 14px;
    color: #b6c7df;
    font-size: 0.88rem;
}

.scouting-topbar-right {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #cbd5e1;
    font-size: 0.84rem;
}

.scouting-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #1d4ed8;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    color: white;
}

.scouting-hero-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1.1fr;
    gap: 14px;
    margin-bottom: 18px;
}

.scouting-hero-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.055);
}

.scouting-hero-title {
    font-size: 1.42rem;
    line-height: 1.1;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 6px;
}

.scouting-hero-subtitle {
    color: #64748b;
    font-size: 0.88rem;
    line-height: 1.35;
}

.scouting-score-value {
    font-size: 3.0rem;
    font-weight: 950;
    line-height: 0.98;
    color: #0f172a;
}

.scouting-score-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 7px;
}

.scouting-score-bar {
    height: 8px;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e 0%, #eab308 62%, #ef4444 100%);
    margin: 12px 0 8px 0;
}

.scouting-mini-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
}

.scouting-mini-metric {
    border-left: 1px solid #e2e8f0;
    padding-left: 12px;
}

.scouting-mini-label {
    color: #64748b;
    font-size: 0.74rem;
    margin-bottom: 4px;
}

.scouting-mini-value {
    color: #0f172a;
    font-size: 1.18rem;
    font-weight: 900;
}

.metric-card,
.radar-card,
.radar-info-box,
.shap-executive-box,
.executive-recommendation-card {
    border-radius: 14px !important;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.045) !important;
}

.player-table {
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
}

div[data-testid="stTabs"] button {
    font-weight: 750;
    color: #334155;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1d4ed8;
    border-bottom-color: #1d4ed8;
}

.sidebar-footer {
    color: #93a4bd;
    font-size: 0.72rem;
    padding-top: 10px;
    border-top: 1px solid rgba(148,163,184,0.25);
    margin-top: 18px;
}



/* =========================
   Scouting IQ polish fixes
   ========================= */
.scouting-topbar {
    position: sticky;
    top: 0.45rem;
    z-index: 999;
    min-height: 48px;
}

/* Restore readable Streamlit widgets inside dark sidebar */
[data-testid="stSidebar"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] div[data-baseweb="select"] input,
[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] svg,
[data-testid="stSidebar"] div[data-baseweb="input"] *,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
    color: #0f172a !important;
    fill: #0f172a !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 9px !important;
}

[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div {
    color: initial !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(148,163,184,0.28) !important;
}

.pro-section-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.exec-overview-grid {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr 1.25fr;
    gap: 14px;
    margin-bottom: 16px;
}

.exec-player-card,
.exec-score-card,
.exec-kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.exec-player-name {
    font-size: 1.65rem;
    font-weight: 950;
    color: #0f172a;
    margin-bottom: 6px;
}

.exec-player-meta {
    color: #64748b;
    font-size: 0.90rem;
    line-height: 1.45;
}

.exec-score-main {
    font-size: 3.2rem;
    font-weight: 950;
    line-height: 0.98;
    color: #0f172a;
}

.exec-score-sub {
    color: #64748b;
    font-size: 0.78rem;
    text-transform: uppercase;
    font-weight: 850;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.exec-badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 0.76rem;
    margin-top: 8px;
}
.exec-badge-green { background:#dcfce7; color:#166534; }
.exec-badge-yellow { background:#fef3c7; color:#92400e; }
.exec-badge-red { background:#fee2e2; color:#991b1b; }
.exec-badge-blue { background:#dbeafe; color:#1d4ed8; }

.exec-kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.exec-kpi-label {
    color: #64748b;
    font-size: 0.74rem;
    margin-bottom: 4px;
}

.exec-kpi-value {
    color: #0f172a;
    font-size: 1.18rem;
    font-weight: 900;
}

.driver-chip {
    display: inline-block;
    background: #eef6ff;
    color: #1e3a8a;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 0.78rem;
    font-weight: 800;
    margin-right: 6px;
    margin-bottom: 6px;
}

.compact-board-note {
    color:#64748b;
    font-size:0.82rem;
    margin-top: 4px;
}



/* =========================
   Scouting IQ premium UX pass
   ========================= */
.block-container {
    padding-top: 1.65rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    max-width: 1720px !important;
}

/* Top bar: visible, SaaS-like, not clipped by Streamlit chrome */
.scouting-topbar {
    position: relative !important;
    top: auto !important;
    z-index: 20 !important;
    min-height: 62px !important;
    padding: 16px 22px !important;
    margin: 0 0 22px 0 !important;
    border-radius: 18px !important;
    background: linear-gradient(90deg, #071224 0%, #0a1d36 46%, #12396d 100%) !important;
    border: 1px solid rgba(148, 163, 184, 0.32) !important;
    box-shadow: 0 18px 42px rgba(2, 6, 23, 0.22) !important;
}
.scouting-brand { font-size: 1.20rem !important; }
.scouting-brand-mark {
    width: 40px !important;
    height: 40px !important;
    box-shadow: inset 0 0 0 1px rgba(15,23,42,.08), 0 4px 12px rgba(15,23,42,.18);
}
.scouting-topbar-center {
    min-height: 24px !important;
    background: rgba(255,255,255,0.075) !important;
    border: 1px solid rgba(226, 232, 240, 0.20) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.06) !important;
    color: #d7e5f7 !important;
}
.scouting-topbar-right { color:#e2e8f0 !important; }

/* Replace heavy blue blocks with neutral product cards */
.info-box {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 4px solid #2563eb !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    color: #334155 !important;
    font-weight: 500 !important;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045) !important;
    margin: 12px 0 20px 0 !important;
}
.info-box b { color:#0f172a !important; }
.info-box hr { border-color:#e2e8f0 !important; opacity:1 !important; }

/* More air between context, hero cards and KPI blocks */
.scouting-hero-grid {
    margin-top: 14px !important;
    margin-bottom: 28px !important;
    gap: 18px !important;
}
.metric-card, .scouting-hero-card, .exec-player-card, .exec-score-card, .exec-kpi-card,
.radar-card, .compact-top5-card, .pro-section-card, .executive-recommendation-card {
    border: 1px solid #e3e8ef !important;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.055) !important;
}
.metric-card:hover, .scouting-hero-card:hover, .compact-top5-card:hover, .exec-player-card:hover, .exec-score-card:hover, .exec-kpi-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.075) !important;
    transition: all .15s ease;
}

/* Sidebar filters: keep dark chrome, but make widgets readable and modern */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06152a 0%, #0a2344 50%, #06152a 100%) !important;
}
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stRadio {
    margin-bottom: 0.65rem !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background: #f8fafc !important;
    border: 1px solid #d7dee9 !important;
    border-radius: 10px !important;
    min-height: 40px !important;
    box-shadow: 0 2px 8px rgba(2, 6, 23, 0.18) !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #1e293b !important;
    color: #1e293b !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #dbeafe !important;
}
/* Streamlit expanders: modern disclosure cards */
div[data-testid="stExpander"] {
    border: 1px solid #dce3ee !important;
    border-radius: 14px !important;
    background: #ffffff !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.035) !important;
    margin: 14px 0 18px 0 !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] details > summary {
    padding: 12px 16px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
}
div[data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid #e2e8f0 !important;
}
div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] {
    color: #334155 !important;
}

/* Tables: cleaner Wyscout-like board */
.player-table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    background: #ffffff !important;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045) !important;
}
.player-table th {
    background: #f8fafc !important;
    color: #475569 !important;
    font-size: 0.74rem !important;
    text-transform: none !important;
    letter-spacing: .01em !important;
    padding: 11px 10px !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
.player-table td {
    padding: 11px 10px !important;
    border-bottom: 1px solid #edf2f7 !important;
    color: #172033 !important;
    background: #ffffff !important;
}
.player-table tr:hover td { background: #f8fbff !important; }
.comparison-table-wrapper { margin-top: 10px !important; }

/* Streamlit dataframe containers */
div[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04) !important;
}

/* Compact Top 5 cards */
.compact-top5-grid {
    display: grid !important;
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
    gap: 14px !important;
    margin: 14px 0 22px 0 !important;
}
.compact-top5-card {
    background:#ffffff !important;
    border:1px solid #e2e8f0 !important;
    border-radius:14px !important;
    padding:13px 14px !important;
    min-height:86px !important;
}

/* Tight fixes for score-methodology expander */
.executive-recommendation-card + div[data-testid="stExpander"],
.pro-section-card + div[data-testid="stExpander"] {
    margin-top: 16px !important;
}

/* Section titles: slightly more product-like */
h1, h2, h3 { color:#1f2937 !important; }
hr { border-color:#dbe2ea !important; }



/* =========================
   Final Scouting IQ UX pass
   ========================= */
.block-container {
    padding-top: 1.2rem !important;
    max-width: 1660px !important;
}
.scouting-topbar {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    min-height: 58px !important;
    padding: 13px 18px !important;
    margin-bottom: 10px !important;
    background: linear-gradient(90deg, #071426 0%, #0c2445 54%, #12396d 100%) !important;
}
.scouting-topbar-center { display: none !important; }
.scouting-topbar-right span {
    font-size: .78rem !important;
    color: #dbeafe !important;
    opacity: .95;
}
/* global search input directly below the topbar */
div[data-testid="stTextInput"] label {
    color: #334155 !important;
    font-weight: 800 !important;
}
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    color: #0f172a !important;
    box-shadow: 0 8px 20px rgba(15,23,42,.045) !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.12), 0 8px 20px rgba(15,23,42,.055) !important;
}
.context-strip {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: 0 8px 22px rgba(15,23,42,.045);
    margin: 14px 0 22px 0;
}
.context-strip-title {
    font-size: .78rem;
    font-weight: 900;
    text-transform: uppercase;
    color: #475569;
    letter-spacing: .04em;
    margin-bottom: 8px;
}
.context-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border: 1px solid #dbeafe;
    background: #eff6ff;
    color: #1e3a8a;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: .78rem;
    font-weight: 800;
    margin-right: 6px;
    margin-bottom: 6px;
}
.context-chip-neutral {
    border-color: #e2e8f0;
    background: #f8fafc;
    color: #334155;
}
.scouting-hero-grid {
    margin-top: 6px !important;
    margin-bottom: 30px !important;
}
.metric-card, .scouting-hero-card, .exec-player-card, .exec-score-card, .exec-kpi-card, .radar-card, .compact-top5-card, .pro-section-card {
    background: #ffffff !important;
    border: 1px solid #e5eaf1 !important;
    box-shadow: 0 8px 22px rgba(15,23,42,.045) !important;
}
.radar-info-box {
    background: #ffffff !important;
    border: 1px solid #e5eaf1 !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 20px rgba(15,23,42,.035) !important;
}
/* cleaner expanders */
div[data-testid="stExpander"] {
    border-radius: 14px !important;
    border: 1px solid #dbe3ee !important;
    box-shadow: 0 6px 18px rgba(15,23,42,.035) !important;
    margin: 12px 0 16px 0 !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 850 !important;
    color: #0f172a !important;
}
/* Tables */
.player-table {
    font-size: .78rem !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
.player-table th {
    background: #f8fafc !important;
    color: #475569 !important;
    font-size: .72rem !important;
    font-weight: 900 !important;
    padding: 10px 9px !important;
}
.player-table td {
    padding: 10px 9px !important;
    color: #0f172a !important;
}
.player-table tr:hover td { background: #f8fbff !important; }
div[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 8px 22px rgba(15,23,42,.04) !important;
}
/* Sidebar select readability */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #0f172a !important;
    color: #0f172a !important;
    opacity: 1 !important;
}
/* Section rhythm */
h2, h3 { letter-spacing: -0.02em; }



/* =========================
   Scouting IQ i18n + modern decision UX
   ========================= */
.sort-help-box {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:14px;
    padding:12px 14px;
    color:#334155;
    box-shadow:0 8px 20px rgba(15,23,42,.035);
    font-size:.88rem;
}
.opportunity-layout {
    display:grid;
    grid-template-columns: minmax(0, 1.8fr) minmax(320px, .8fr);
    gap:18px;
    align-items:start;
}
.panel-card {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:16px 18px;
    box-shadow:0 12px 28px rgba(15,23,42,.055);
    margin-bottom:16px;
}
.panel-title {
    font-size:1.02rem;
    font-weight:950;
    color:#0f172a;
    margin-bottom:4px;
}
.panel-subtitle {
    font-size:.82rem;
    color:#64748b;
    line-height:1.35;
}
.top5-list-card {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:16px 18px;
    box-shadow:0 12px 28px rgba(15,23,42,.055);
}
.top5-row {
    display:grid;
    grid-template-columns:32px minmax(0,1fr) 64px;
    gap:10px;
    align-items:center;
    padding:10px 0;
    border-bottom:1px solid #edf2f7;
}
.top5-row:last-child { border-bottom:0; }
.top5-rank {
    width:28px;height:28px;border-radius:8px;background:#eff6ff;color:#1d4ed8;
    display:flex;align-items:center;justify-content:center;font-weight:950;font-size:.82rem;
}
.top5-name { font-weight:950;color:#0f172a;line-height:1.15;font-size:.88rem; }
.top5-meta { color:#64748b;font-size:.74rem;line-height:1.25;margin-top:2px; }
.top5-score { text-align:right;font-weight:950;color:#166534;font-size:1.02rem; }
.radar-modern-grid {
    display:grid;
    grid-template-columns: minmax(0, 1.4fr) minmax(330px, .85fr);
    gap:20px;
    align-items:start;
}
.radar-chart-card {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:10px 12px;
    box-shadow:0 12px 28px rgba(15,23,42,.045);
}
.modern-help-expander div[data-testid="stExpander"] {
    margin-top:10px !important;
}
[data-testid="stSidebar"] div[data-baseweb="popover"] * { color:#0f172a !important; }
[data-testid="stSidebar"] div[role="listbox"] * { color:#0f172a !important; -webkit-text-fill-color:#0f172a !important; }
[data-testid="stSidebar"] div[data-baseweb="select"] input { color:#0f172a !important; -webkit-text-fill-color:#0f172a !important; }
[data-testid="stSidebar"] .stRadio p { color:#dbeafe !important; }
/* Reduce visual noise in Plotly containers */
div[data-testid="stPlotlyChart"] {
    border-radius:16px;
    overflow:hidden;
}
/* More readable multiselect chips */
span[data-baseweb="tag"] {
    border-radius:8px !important;
    font-weight:800 !important;
}


/* Visible slider ranges in dark sidebar */
[data-testid="stSidebar"] .slider-range-hint {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin: -0.35rem 0 0.85rem 0;
    padding: 5px 8px;
    border-radius: 8px;
    background: rgba(219, 234, 254, 0.10);
    border: 1px solid rgba(191, 219, 254, 0.16);
    font-size: 0.72rem;
    line-height: 1.15;
}
[data-testid="stSidebar"] .slider-range-hint span {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}



/* =========================
   Patch: sidebar help, sliders and matrix layout
   ========================= */
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"] {
    display: none !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [aria-hidden="true"] {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
}
[data-testid="stSidebar"] div[data-testid="stPopover"] button {
    background: rgba(219,234,254,.10) !important;
    border: 1px solid rgba(191,219,254,.22) !important;
    color: #eaf2ff !important;
    border-radius: 10px !important;
    width: 100% !important;
    justify-content: flex-start !important;
}
.matrix-shell {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:14px 16px 4px 16px;
    box-shadow:0 12px 28px rgba(15,23,42,.055);
    margin-top:14px;
}
.top5-horizontal-card {
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:16px 18px;
    box-shadow:0 12px 28px rgba(15,23,42,.050);
    margin:18px 0 12px 0;
}
.top5-horizontal-grid {
    display:grid;
    grid-template-columns:repeat(5, minmax(0, 1fr));
    gap:12px;
    margin-top:12px;
}
.top5-horizontal-item {
    border:1px solid #e5eaf1;
    border-radius:14px;
    padding:12px 12px;
    background:linear-gradient(180deg,#ffffff 0%,#f8fafc 100%);
    min-height:94px;
}
.top5-horizontal-rank {
    width:26px;height:26px;border-radius:8px;background:#eff6ff;color:#1d4ed8;
    display:flex;align-items:center;justify-content:center;font-weight:950;font-size:.80rem;
    margin-bottom:8px;
}
.top5-horizontal-name { font-weight:950;color:#0f172a;line-height:1.16;font-size:.90rem; }
.top5-horizontal-meta { color:#64748b;font-size:.74rem;line-height:1.28;margin-top:4px; }
.top5-horizontal-score { color:#166534;font-size:1.05rem;font-weight:950;margin-top:8px; }
@media (max-width: 1200px) {
    .top5-horizontal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}



/* =========================
   Final fixes: popovers, sliders, full-width matrix
   ========================= */
div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
div[data-baseweb="popover"] div {
    background-color: #ffffff !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [aria-hidden="true"] {
    display: none !important;
    visibility: hidden !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
}
.matrix-shell {
    width: 100% !important;
    background:#ffffff !important;
    border:1px solid #e2e8f0 !important;
    border-radius:20px !important;
    padding:12px 14px 0 14px !important;
    box-shadow:0 16px 34px rgba(15,23,42,.060) !important;
    margin-top:16px !important;
    margin-bottom:18px !important;
}
.top5-horizontal-card {
    background:#ffffff !important;
    border:1px solid #e2e8f0 !important;
    border-radius:18px !important;
    padding:16px 18px !important;
    box-shadow:0 12px 28px rgba(15,23,42,.050) !important;
    margin:18px 0 16px 0 !important;
}
.top5-horizontal-grid {
    display:grid !important;
    grid-template-columns:repeat(5, minmax(0, 1fr)) !important;
    gap:12px !important;
    margin-top:12px !important;
}
.top5-horizontal-item {
    border:1px solid #e5eaf1 !important;
    border-radius:14px !important;
    padding:12px !important;
    background:linear-gradient(180deg,#ffffff 0%,#f8fafc 100%) !important;
    min-height:96px !important;
}
.top5-horizontal-rank {
    width:26px;height:26px;border-radius:8px;background:#eff6ff;color:#1d4ed8;
    display:flex;align-items:center;justify-content:center;font-weight:950;font-size:.80rem;margin-bottom:8px;
}
.top5-horizontal-name { font-weight:950;color:#0f172a;line-height:1.16;font-size:.90rem; }
.top5-horizontal-meta { color:#64748b;font-size:.74rem;line-height:1.28;margin-top:4px; }
.top5-horizontal-score { color:#166534;font-size:1.05rem;font-weight:950;margin-top:8px; }
@media (max-width: 1200px) { .top5-horizontal-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; } }


/* =========================
   Release hotfix: i18n, slider tick labels and matrix annotations
   ========================= */
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMax"],
[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [aria-hidden="true"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    margin-top: 0.35rem !important;
    margin-bottom: 1.05rem !important;
    background: rgba(219, 234, 254, 0.13) !important;
    border-color: rgba(191, 219, 254, 0.26) !important;
}
.matrix-shell { display: none !important; }


/* =========================
   Final UX fix: hide native Streamlit slider ticks/tooltip values
   We already expose clean ranges through .slider-range-hint.
   ========================= */
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [aria-hidden="true"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [aria-hidden="true"] *,
[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] > div:nth-child(n+2) div[style*="position: absolute"],
[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] > div:nth-child(n+2) span {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    background: transparent !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    margin-top: 0.15rem !important;
    margin-bottom: 1.15rem !important;
}

/* Hotfix: hide native BaseWeb slider value/tick labels; custom range hints remain visible. */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"],
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"] *,
[data-testid="stSidebar"] .stSlider div[role="presentation"] span,
[data-testid="stSidebar"] .stSlider div[role="presentation"] div[style*="position: absolute"] span {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    background: transparent !important;
}

/* =========================
   Definitive hotfix: hide native BaseWeb slider popover/tick labels.
   The dashboard uses .slider-range-hint as the only visible range indicator.
   ========================= */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"],
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"] *,
[data-testid="stSidebar"] .stSlider div[role="presentation"] > div:not(:first-child),
[data-testid="stSidebar"] .stSlider div[style*="transform: translate"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    background: transparent !important;
    pointer-events: none !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="background-color: rgb(255"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="background: rgb(255"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="#ff5b5b"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="#ef4444"] {
    background: transparent !important;
    box-shadow: none !important;
}


/* =========================
   Final visible filter hints and clean search suggestions
   ========================= */
[data-testid="stSidebar"] .slider-range-hint,
[data-testid="stSidebar"] .slider-range-hint * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    min-height: 28px !important;
    margin: 0.25rem 0 1.05rem 0 !important;
    padding: 6px 8px !important;
    border-radius: 8px !important;
    background: rgba(219, 234, 254, 0.16) !important;
    border: 1px solid rgba(191, 219, 254, 0.32) !important;
    font-size: 0.72rem !important;
    line-height: 1.15 !important;
}
[data-testid="stSidebar"] .slider-range-hint span {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.search-suggestion-caption {
    color:#64748b;
    font-size:.78rem;
    margin:.15rem 0 .2rem 0;
}


/* =========================
   Sprint 11 final hotfix: persistent slider ranges and clickable search filter
   ========================= */
[data-testid="stSidebar"] .slider-minmax-hint,
[data-testid="stSidebar"] .slider-minmax-hint * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
    background: transparent !important;
    pointer-events: auto !important;
}
[data-testid="stSidebar"] .slider-minmax-hint {
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin: -0.15rem 0 0.25rem 0 !important;
    padding: 0 1px !important;
    font-size: 0.74rem !important;
    line-height: 1.1 !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .slider-range-hint,
[data-testid="stSidebar"] .slider-range-hint * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    min-height: 30px !important;
    margin: 0.20rem 0 1.10rem 0 !important;
    padding: 6px 8px !important;
    border-radius: 8px !important;
    background: rgba(219, 234, 254, 0.16) !important;
    border: 1px solid rgba(191, 219, 254, 0.34) !important;
    font-size: 0.72rem !important;
    line-height: 1.15 !important;
}
[data-testid="stSidebar"] .slider-range-hint span {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.clear-search-chip button {
    border-radius: 999px !important;
    border: 1px solid #dbeafe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    font-weight: 850 !important;
    padding: 0.25rem 0.65rem !important;
    min-height: 30px !important;
}



/* Sprint 11 v3 final: remove native slider tick/value labels; keep only custom range box. */
[data-testid="stSidebar"] .stSlider .slider-minmax-hint {
    display: none !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[aria-hidden="true"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[aria-hidden="true"] *,
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="transform: translate"]:not([style*="width"]),
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[style*="top: 100%"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] span[style*="position: absolute"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    background: transparent !important;
    pointer-events: none !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    margin-top: 0.35rem !important;
}
/* Keep search suggestions attached to the search input. */
div[data-testid="stTextInput"] + div[data-testid="stSelectbox"] {
    margin-top: -0.35rem !important;
}


/* =========================
   Sprint 11 v4 final: native search autocomplete and clean slider labels
   ========================= */
/* Hide BaseWeb/Streamlit slider hover tooltips and native tick labels. */
[data-testid="stSidebar"] [role="tooltip"],
[data-testid="stSidebar"] [data-baseweb="tooltip"],
[data-testid="stSidebar"] .stSlider [data-baseweb="tooltip"],
[data-testid="stSidebar"] .stSlider [role="tooltip"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"],
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"] * {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
/* Custom visible slider range: plain text below the track, no extra box/module. */
[data-testid="stSidebar"] .slider-range-hint,
[data-testid="stSidebar"] .slider-range-hint * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    justify-content: space-between !important;
    width: 100% !important;
    margin: -0.05rem 0 1.0rem 0 !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    font-size: 0.73rem !important;
    line-height: 1.15 !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .slider-range-hint span,
[data-testid="stSidebar"] .slider-range-hint b {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
/* The search filter chip is an inline link inside the active filter row. */
.context-chip-clear {
    text-decoration: none !important;
    cursor: pointer !important;
    color: #1e3a8a !important;
}
.context-chip-clear:hover {
    background: #dbeafe !important;
    border-color: #bfdbfe !important;
}
/* Native selectbox is now the search box; its dropdown is attached to the input. */
div[data-testid="stSelectbox"] div[data-baseweb="popover"] {
    z-index: 10000 !important;
}

</style>
""",
    unsafe_allow_html=True,
)




# =============================================================================
# Final UX stabilization patch: sidebar labels, sliders and clickable search clear
# =============================================================================
st.markdown(
    """
<style>
/* Clear, modern global search */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border-radius: 14px !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    min-height: 46px !important;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.055) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.12), 0 10px 24px rgba(15,23,42,.065) !important;
}
/* Sidebar slider titles and permanent range boxes */
.sidebar-slider-title {
    color: #ffffff !important;
    font-size: 0.88rem;
    font-weight: 850;
    margin: 1.05rem 0 0.15rem 0;
}
[data-testid="stSidebar"] .slider-range-hint {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 8px !important;
    margin: 0.35rem 0 0.95rem 0 !important;
    padding: 8px 10px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, 0.14) !important;
    border: 1px solid rgba(191, 219, 254, 0.28) !important;
    font-size: 0.74rem !important;
    line-height: 1.2 !important;
}
[data-testid="stSidebar"] .slider-range-hint span,
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* Hide native BaseWeb hover value balloons/tick labels; our range box is the canonical reference */
[data-testid="stSidebar"] [data-testid="stTickBar"],
[data-testid="stSidebar"] [data-testid="stThumbValue"],
[data-testid="stSidebar"] div[data-baseweb="slider"] [aria-hidden="true"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="ThumbValue"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="TickBar"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="tick"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="Tick"] {
    display: none !important;
    visibility: hidden !important;
}
/* Keep slider track/thumb visible after hiding labels */
[data-testid="stSidebar"] div[data-baseweb="slider"] [role="slider"] {
    display: block !important;
    visibility: visible !important;
}
/* Product glossary and clear-search controls */
.clear-search-button button {
    border-radius: 999px !important;
    border: 1px solid #dbeafe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    font-weight: 850 !important;
    padding: 0.35rem 0.75rem !important;
}
.clear-search-button button:hover {
    background: #dbeafe !important;
    border-color: #bfdbfe !important;
}
.context-chip-clear {
    cursor: default !important;
    text-decoration: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)




# =============================================================================
# Sprint 11 UX closure patch: search, sidebar helpers and filter chips
# =============================================================================
st.markdown(
    """
<style>
/* Premium global search block */
.global-search-shell {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #dbe7f5;
    border-radius: 18px;
    padding: 14px 16px 12px 16px;
    box-shadow: 0 12px 30px rgba(15,23,42,.065);
    margin: 0 0 16px 0;
}
.global-search-title {
    display:flex;
    align-items:center;
    gap:8px;
    font-size:.78rem;
    font-weight:950;
    letter-spacing:.08em;
    text-transform:uppercase;
    color:#1e3a8a;
    margin-bottom:4px;
}
.global-search-caption {
    color:#64748b;
    font-size:.82rem;
    margin-bottom:8px;
}
/* Main selectbox used as autocomplete search */
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #b7c8dd !important;
    min-height: 50px !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.060) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 12px 28px rgba(15,23,42,.075) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] label {
    font-weight: 900 !important;
    color: #1e293b !important;
}
/* Sidebar help controls: avoid blank white expander and align with product style */
[data-testid="stSidebar"] div[data-testid="stPopover"] button {
    background: rgba(219,234,254,.11) !important;
    border: 1px solid rgba(191,219,254,.30) !important;
    color: #eaf2ff !important;
    border-radius: 12px !important;
    width: 100% !important;
    justify-content: flex-start !important;
    min-height: 42px !important;
    font-weight: 850 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05) !important;
}
[data-testid="stSidebar"] div[data-testid="stPopover"] button:hover {
    background: rgba(219,234,254,.18) !important;
    border-color: rgba(191,219,254,.45) !important;
}
/* Slider title + range above the track */
.sidebar-slider-title {
    color: #ffffff !important;
    font-size: 0.86rem !important;
    font-weight: 900 !important;
    margin: 1.00rem 0 0.20rem 0 !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 8px !important;
    margin: 0 0 0.18rem 0 !important;
    padding: 7px 9px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, 0.14) !important;
    border: 1px solid rgba(191, 219, 254, 0.30) !important;
    font-size: 0.72rem !important;
    line-height: 1.15 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04) !important;
}
[data-testid="stSidebar"] .slider-range-hint span,
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* Hide native hover/tick values: custom range box is canonical */
[data-testid="stSidebar"] [data-testid="stTickBar"],
[data-testid="stSidebar"] [data-testid="stThumbValue"],
[data-testid="stSidebar"] div[data-baseweb="slider"] [aria-hidden="true"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="ThumbValue"],
[data-testid="stSidebar"] div[data-baseweb="slider"] div[class*="Tick"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
[data-testid="stSidebar"] .stSlider {
    margin-bottom: .70rem !important;
}
/* Clickable active-search chip */
.context-chip-link {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border: 1px solid #bfdbfe;
    background: #eff6ff;
    color: #1e3a8a !important;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: .78rem;
    font-weight: 900;
    margin-right: 6px;
    margin-bottom: 6px;
    text-decoration: none !important;
}
.context-chip-link:hover {
    background: #dbeafe;
    border-color: #93c5fd;
}
</style>
""",
    unsafe_allow_html=True,
)




# =============================================================================
# Final deterministic sidebar slider state override
# =============================================================================
st.markdown(
    """
<style>
[data-testid="stSidebar"] .sidebar-slider-current-state,
[data-testid="stSidebar"] .sidebar-slider-current-state * {
    visibility: visible !important;
    opacity: 1 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] .sidebar-slider-current-state {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0.15rem 0 0.35rem 0 !important;
    padding: 7px 9px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, 0.14) !important;
    border: 1px solid rgba(191, 219, 254, 0.30) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04) !important;
    font-size: 0.72rem !important;
    line-height: 1.15 !important;
}
[data-testid="stSidebar"] .sidebar-slider-current-state span {
    font-size: 0.68rem !important;
    font-weight: 850 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
[data-testid="stSidebar"] .sidebar-slider-current-state b {
    font-size: 0.82rem !important;
    font-weight: 950 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 numeric sidebar filters: no native slider hover labels
# =============================================================================
st.markdown(
    """
<style>
/* Numeric sidebar filters replace st.slider for the executive filter panel. */
[data-testid="stSidebar"] .sidebar-filter-value-badge {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 0 0.35rem 0 !important;
    padding: 7px 10px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, 0.16) !important;
    border: 1px solid rgba(191, 219, 254, 0.36) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045) !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge span {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
    font-size: .70rem !important;
    font-weight: 950 !important;
    text-transform: uppercase !important;
    letter-spacing: .055em !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: .86rem !important;
    font-weight: 950 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: .85rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    border-radius: 10px !important;
    font-weight: 850 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    color: #0f172a !important;
    background: #f8fafc !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 UX refinement: compact header, collapsed guide, search and numeric filters
# =============================================================================
st.markdown(
    """
<style>
/* Reduce excessive whitespace above the product header. */
.block-container {
    padding-top: 0.55rem !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 10px !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 2.25rem !important;
}

/* Make the collapsed guide look intentional rather than fully expanded onboarding. */
div[data-testid="stExpander"] {
    margin: 0 0 14px 0 !important;
}
div[data-testid="stExpander"] details:not([open]) > summary {
    border-bottom: 0 !important;
}

/* Stronger, product-like global search card and writable select input. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
    border: 1px solid #c8d9ee !important;
    border-radius: 18px !important;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.075) !important;
    padding: 14px 16px 16px 16px !important;
    margin-bottom: 18px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-title {
    font-size: 0.90rem !important;
    color: #0b2f5f !important;
    letter-spacing: 0.085em !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    min-height: 56px !important;
    border: 2px solid #93b5da !important;
    background: #ffffff !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.065) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14), 0 14px 32px rgba(15, 23, 42, 0.090) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] input {
    font-size: 1.00rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

/* Numeric sidebar controls: visible stepper buttons and cleaner input body. */
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-top: 0.20rem !important;
    margin-bottom: 0.88rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-weight: 900 !important;
    min-height: 38px !important;
    border-radius: 10px 0 0 10px !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #eaf2ff !important;
    color: #0f2f5f !important;
    -webkit-text-fill-color: #0f2f5f !important;
    border-left: 1px solid #c7d7ea !important;
    min-width: 30px !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button svg {
    color: #0f2f5f !important;
    fill: #0f2f5f !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button:hover {
    background: #dbeafe !important;
}
.sidebar-filter-value {
    margin-bottom: 0.20rem !important;
}

/* Clear search: visible, modern and separated from the context strip without looking like a raw Streamlit default. */
.search-clear-row {
    display: block !important;
    margin: -0.35rem 0 1.10rem 0 !important;
}
.search-clear-row + div[data-testid="stButton"] button,
div[data-testid="stButton"] button[kind="secondary"] {
    border-radius: 999px !important;
}
div[data-testid="stButton"] button:has(p) {
    font-weight: 850 !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 final visual polish: compact header, search emphasis, filter badges
# =============================================================================
st.markdown(
    """
<style>
/* Pull the product header closer to the top of the viewport. */
.block-container {
    padding-top: 0.15rem !important;
}
header[data-testid="stHeader"] {
    height: 1.35rem !important;
    min-height: 1.35rem !important;
    background: transparent !important;
}
.scouting-topbar {
    margin-top: 0.05rem !important;
    margin-bottom: 8px !important;
}

/* Make the search module read as the primary interaction. */
.global-search-shell,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-left: 4px solid #2563eb !important;
    border-radius: 18px !important;
    box-shadow: 0 14px 34px rgba(37, 99, 235, 0.10), 0 10px 24px rgba(15, 23, 42, 0.055) !important;
}
.global-search-title, .final-search-title {
    color: #0b2f5f !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #93c5fd !important;
    border-radius: 16px !important;
    min-height: 54px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.85), 0 8px 22px rgba(37,99,235,.08) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 12px 28px rgba(37,99,235,.11) !important;
}

/* Sidebar numeric filter state: selected value + allowed range in one compact badge. */
[data-testid="stSidebar"] .sidebar-filter-value-badge {
    display: grid !important;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
    gap: 8px !important;
    align-items: center !important;
    padding: 8px 9px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, 0.14) !important;
    border: 1px solid rgba(191, 219, 254, 0.34) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.06) !important;
    margin: 0.18rem 0 0.30rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-filter-badge-item {
    display: flex !important;
    flex-direction: column !important;
    gap: 2px !important;
    min-width: 0 !important;
}
[data-testid="stSidebar"] .sidebar-filter-badge-item:last-child {
    align-items: flex-end !important;
    text-align: right !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge span {
    color: #b9d4f5 !important;
    -webkit-text-fill-color: #b9d4f5 !important;
    font-size: 0.66rem !important;
    font-weight: 950 !important;
    letter-spacing: .055em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 0.82rem !important;
    font-weight: 950 !important;
    white-space: nowrap !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: 0.95rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    border-radius: 10px 0 0 10px !important;
    font-weight: 900 !important;
    min-height: 40px !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    background: #eff6ff !important;
    color: #0f2f5f !important;
    -webkit-text-fill-color: #0f2f5f !important;
    border-left: 1px solid #c7d8ee !important;
    font-weight: 950 !important;
}

/* Clear-search action: closer to context card and more product-like. */
.search-clear-row {
    margin: -0.70rem 0 0.95rem 1.05rem !important;
}
.search-clear-row + div[data-testid="stButton"] {
    margin-top: -0.70rem !important;
    margin-bottom: 0.95rem !important;
}
.search-clear-row + div[data-testid="stButton"] button,
.clear-search-button button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    padding: 0.38rem 0.82rem !important;
    min-height: 34px !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.10) !important;
}
.search-clear-row + div[data-testid="stButton"] button:hover,
.clear-search-button button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# UX polish v2: spacing, Google-like search, compact guide and numeric filters
# =============================================================================
st.markdown(
    """
<style>
/* Reduce only the excessive Streamlit chrome above the product header. */
header[data-testid="stHeader"] {
    height: 0.35rem !important;
    min-height: 0.35rem !important;
    background: transparent !important;
}
.block-container {
    padding-top: 0.45rem !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 14px !important;
}

/* Quick guide: calmer collapsed product card, with breathing room after the header. */
div[data-testid="stExpander"] {
    margin-top: 10px !important;
    margin-bottom: 24px !important;
    border-radius: 16px !important;
    border: 1px solid #dbe3ee !important;
    background: #ffffff !important;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] details > summary {
    min-height: 46px !important;
    padding: 11px 16px !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
    color: #0f2f5f !important;
    font-weight: 900 !important;
    letter-spacing: 0.01em !important;
}
div[data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid #e5edf7 !important;
}
.quick-guide-intro {
    color: #64748b !important;
    font-size: 0.84rem !important;
    margin: 4px 0 12px 0 !important;
}

/* Search module: white, prominent and closer to a Google-like input. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-left: 4px solid #2563eb !important;
    border-radius: 20px !important;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.085), 0 8px 18px rgba(15, 23, 42, 0.045) !important;
    padding: 16px 18px 18px 18px !important;
    margin-bottom: 18px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-title {
    color: #0b2f5f !important;
    font-size: 0.90rem !important;
    font-weight: 950 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-caption {
    color: #475569 !important;
    font-size: 0.86rem !important;
    margin-bottom: 10px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #93c5fd !important;
    border-radius: 999px !important;
    min-height: 52px !important;
    box-shadow: 0 5px 16px rgba(37, 99, 235, 0.10) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.13), 0 8px 20px rgba(37, 99, 235, 0.12) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] input,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] span {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-weight: 750 !important;
}

/* Sidebar numeric filters: clearer distance between state badge and editable input. */
[data-testid="stSidebar"] .sidebar-filter-value-badge {
    margin: 0.20rem 0 0.56rem 0 !important;
    padding: 9px 10px !important;
    gap: 12px !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge--range {
    margin-bottom: 0.70rem !important;
}
[data-testid="stSidebar"] .sidebar-filter-badge-item b {
    line-height: 1.25 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-top: 0 !important;
    margin-bottom: 1.10rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    background: #eaf2ff !important;
    color: #0b2f5f !important;
    -webkit-text-fill-color: #0b2f5f !important;
    font-weight: 950 !important;
    opacity: 1 !important;
}

/* Clear-search: closer to context strip and less dead vertical space. */
.context-strip-v2 {
    margin-bottom: 0.20rem !important;
}
.search-clear-row {
    display: block !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.search-clear-row + div[data-testid="stButton"] {
    margin-top: -0.10rem !important;
    margin-bottom: 0.90rem !important;
    margin-left: 0.75rem !important;
}
.search-clear-row + div[data-testid="stButton"] button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    padding: 0.34rem 0.82rem !important;
    min-height: 32px !important;
    box-shadow: 0 5px 14px rgba(37, 99, 235, 0.10) !important;
}
.search-clear-row + div[data-testid="stButton"] button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 final product coherence patch: scouting universe + football lookup
# =============================================================================
st.markdown(
    """
<style>
/* Restore Streamlit toolbar while keeping the product header near the top. */
header[data-testid="stHeader"] {
    height: 2.15rem !important;
    min-height: 2.15rem !important;
    background: transparent !important;
}
.block-container {
    padding-top: 0.65rem !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 16px !important;
}

/* Search becomes the primary interaction: white card, clear blue hierarchy and larger input. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title),
div[data-testid="stElementContainer"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #d5e3f6 !important;
    border-left: 5px solid #2563eb !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 44px rgba(15, 23, 42, .075) !important;
    padding: 18px 20px 20px 20px !important;
    margin: 0 0 22px 0 !important;
}
.final-search-title {
    color: #0b2f5f !important;
    font-size: 1.03rem !important;
    font-weight: 950 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    margin-bottom: 7px !important;
}
.final-search-caption {
    color: #475569 !important;
    font-size: .92rem !important;
    line-height: 1.35 !important;
    margin-bottom: 10px !important;
}
.final-search-microcopy {
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
    border-radius: 999px !important;
    padding: 6px 11px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    font-size: .76rem !important;
    margin-bottom: 12px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #2563eb !important;
    border-radius: 18px !important;
    min-height: 64px !important;
    box-shadow: 0 10px 28px rgba(37, 99, 235, .13) !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] input,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] span,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] div {
    font-size: 1.02rem !important;
    line-height: 1.25 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 14px 34px rgba(37,99,235,.16) !important;
}

/* Sidebar: keep the value badge compact, add air between badge and numeric control. */
[data-testid="stSidebar"] .sidebar-slider-title {
    margin: 1.25rem 0 .42rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge,
[data-testid="stSidebar"] .sidebar-slider-state-modern,
[data-testid="stSidebar"] .sidebar-slider-current-state {
    padding: 8px 10px !important;
    margin-bottom: .68rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: 1.32rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    min-height: 42px !important;
    font-weight: 850 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    min-width: 36px !important;
}

/* Guide and actions: attached to context, but not floating as an orphan block. */
.quick-guide-action-row {
    margin-top: -0.90rem !important;
    margin-bottom: .95rem !important;
}
.search-clear-row {
    margin-top: -0.90rem !important;
    margin-bottom: .95rem !important;
}
.search-clear-row + div[data-testid="stButton"] button {
    border-radius: 999px !important;
    border: 1px solid #93c5fd !important;
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%) !important;
    color: #1e3a8a !important;
    font-weight: 950 !important;
    box-shadow: 0 8px 18px rgba(37,99,235,.12) !important;
}

/* Product narrative card for players found outside the Scouting Universe. */
.outside-scouting-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #bfdbfe;
    border-left: 5px solid #2563eb;
    border-radius: 18px;
    box-shadow: 0 12px 30px rgba(15,23,42,.060);
    padding: 16px 18px;
    margin: -8px 0 18px 0;
}
.outside-scouting-eyebrow {
    color:#1d4ed8;
    font-size:.74rem;
    font-weight:950;
    letter-spacing:.08em;
    text-transform:uppercase;
    margin-bottom:5px;
}
.outside-scouting-title {
    color:#0f172a;
    font-size:1.02rem;
    font-weight:950;
    margin-bottom:6px;
}
.outside-scouting-player {
    color:#0f172a;
    font-size:1.28rem;
    font-weight:950;
    line-height:1.1;
}
.outside-scouting-meta, .outside-scouting-text {
    color:#475569;
    font-size:.88rem;
    line-height:1.4;
    margin-top:6px;
}
.outside-scouting-cta {
    display:inline-flex;
    margin-top:10px;
    border:1px solid #bfdbfe;
    background:#eff6ff;
    color:#1e3a8a;
    border-radius:999px;
    padding:6px 10px;
    font-size:.78rem;
    font-weight:900;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 13.5 UX polish v3: compact sidebar, richer guide, KPI info and football lookup cards
# =============================================================================
st.markdown(
    """
<style>
/* Sidebar: keep language selector in one line and reduce vertical density. */
[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 6px !important;
    align-items: center !important;
}
[data-testid="stSidebar"] .stRadio label {
    min-height: 30px !important;
    padding: 3px 9px !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] .stRadio label p {
    font-size: .78rem !important;
    font-weight: 850 !important;
    white-space: nowrap !important;
}
.sidebar-inline-label {
    font-size: .74rem !important;
    line-height: 30px !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] hr {
    margin: .85rem 0 !important;
}
[data-testid="stSidebar"] h3 {
    font-size: .75rem !important;
    letter-spacing: .08em !important;
    margin: .45rem 0 .42rem 0 !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    font-size: .70rem !important;
    line-height: 1.25 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: .72rem !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge,
[data-testid="stSidebar"] .sidebar-filter-state,
[data-testid="stSidebar"] .sidebar-slider-state-modern,
[data-testid="stSidebar"] .sidebar-slider-current-state {
    padding: 5px 7px !important;
    margin-bottom: .36rem !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    min-height: 34px !important;
}

/* Command row: make the two cards visually compact and aligned. */
.final-search-shell,
.context-strip-v2.compact-context-panel {
    min-height: 178px !important;
    height: auto !important;
}
.final-search-shell {
    padding: 16px 17px 14px 17px !important;
}
.final-search-title { font-size: .88rem !important; }
.final-search-caption { font-size: .80rem !important; line-height: 1.35 !important; }
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    min-height: 50px !important;
}
.compact-context-panel .context-current-value { font-size: 1.55rem !important; }
.compact-context-panel .context-chip-row {
    max-height: 42px !important;
    overflow: hidden !important;
}
.context-action-row { margin-top: 7px !important; }

/* Quick Guide: compact card with a left rail that clearly signals disclosure. */
.quick-guide-inline {
    position: relative !important;
    max-width: 100% !important;
    border-radius: 13px !important;
    border: 1px solid #bfdbfe !important;
    background: #ffffff !important;
    box-shadow: 0 6px 18px rgba(15, 23, 42, .040) !important;
    overflow: hidden !important;
}
.quick-guide-inline::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #2563eb, #60a5fa);
}
.quick-guide-inline summary {
    min-height: 34px !important;
    padding: 8px 12px 8px 16px !important;
    font-size: .80rem !important;
    font-weight: 950 !important;
    color: #0b2f5f !important;
}
.quick-guide-inline summary::after {
    content: "⌄";
    margin-left: auto;
    color: #2563eb;
    font-weight: 950;
}
.quick-guide-inline[open] summary::after { content: "⌃"; }
.quick-guide-inline-body {
    padding: 10px 12px 12px 16px !important;
    font-size: .78rem !important;
    line-height: 1.35 !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
}
.quick-guide-tabs { margin-bottom: 8px !important; gap: 6px !important; }
.quick-guide-tabs span { padding: 4px 8px !important; font-size: .70rem !important; }
.quick-guide-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
}
.quick-guide-grid div {
    border: 1px solid #e2e8f0;
    background: #ffffff;
    border-radius: 10px;
    padding: 8px 9px;
}
.quick-guide-grid b { display:block; color:#0f172a; margin-bottom:3px; }
.quick-guide-grid small { display:block; color:#475569; font-size:.72rem; line-height:1.35; }
@media (max-width: 1250px) { .quick-guide-grid { grid-template-columns: 1fr !important; } }

/* Executive Overview: more vertical air between card rows and quick-action cards. */
.home-hero { margin-bottom: 24px !important; }
.metric-card {
    margin-bottom: 14px !important;
}
.quick-action-grid {
    margin-top: 18px !important;
    margin-bottom: 24px !important;
    gap: 18px !important;
}
.quick-action-card {
    padding: 16px 18px !important;
    min-height: 82px !important;
}

/* KPI info: real in-card disclosure instead of decorative info icon only. */
.metric-label-with-info {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
}
.metric-info-details {
    position: relative !important;
    display: inline-block !important;
}
.metric-info-details summary {
    list-style: none !important;
    width: 18px !important;
    height: 18px !important;
    border-radius: 999px !important;
    background: #3b82f6 !important;
    color: #ffffff !important;
    font-size: 11px !important;
    font-weight: 950 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}
.metric-info-details summary::-webkit-details-marker { display:none !important; }
.metric-info-details div {
    position: absolute !important;
    right: 0 !important;
    top: 24px !important;
    z-index: 50 !important;
    min-width: 260px !important;
    max-width: 320px !important;
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 12px !important;
    padding: 10px 12px !important;
    color: #334155 !important;
    font-size: .76rem !important;
    line-height: 1.38 !important;
    box-shadow: 0 16px 34px rgba(15,23,42,.14) !important;
}

/* Football Intelligence Layer: compact executive card, not plain text. */
.outside-scouting-card-v3 {
    padding: 16px 18px !important;
    border-radius: 18px !important;
    border: 1px solid #bfdbfe !important;
    border-left: 5px solid #2563eb !important;
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
}
.outside-scouting-main {
    display: grid;
    grid-template-columns: minmax(0, .9fr) minmax(360px, 1.1fr);
    gap: 18px;
    align-items: start;
}
.outside-scouting-metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
}
.outside-scouting-metrics div {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 10px 11px;
    box-shadow: 0 8px 20px rgba(15,23,42,.035);
}
.outside-scouting-metrics span {
    display: block;
    color: #64748b;
    font-size: .70rem;
    font-weight: 850;
    margin-bottom: 4px;
}
.outside-scouting-metrics b {
    display: block;
    color: #0f172a;
    font-size: 1.05rem;
    font-weight: 950;
    line-height: 1.05;
}
.outside-scouting-metrics small {
    display: block;
    color: #166534;
    font-size: .70rem;
    font-weight: 850;
    margin-top: 4px;
}
.outside-scouting-text {
    margin-top: 12px !important;
    font-size: .83rem !important;
    line-height: 1.42 !important;
}
@media (max-width: 1300px) {
    .outside-scouting-main { grid-template-columns: 1fr !important; }
    .outside-scouting-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 13.5 UX polish v4: sidebar vertical navigation, overview spacing and overlays
# =============================================================================
st.markdown(
    """
<style>
/* Sidebar: the language selector stays inline, but navigation/presets never flow horizontally. */
[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
}
[data-testid="stSidebar"] .sidebar-nav-stack {
    display: flex !important;
    flex-direction: column !important;
    gap: 7px !important;
    margin: 0.15rem 0 0.35rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-nav-stack + div,
[data-testid="stSidebar"] .sidebar-nav-stack ~ div {
    max-width: 100% !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button {
    justify-content: flex-start !important;
    min-height: 32px !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 900 !important;
    padding: 0.35rem 0.72rem !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(90deg, #1d4ed8 0%, #153b70 100%) !important;
    border: 1px solid #60a5fa !important;
    color: #ffffff !important;
    box-shadow: 0 8px 18px rgba(37,99,235,.18) !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(219, 234, 254, 0.075) !important;
    border: 1px solid rgba(191, 219, 254, 0.20) !important;
    color: #eaf2ff !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: rgba(219, 234, 254, 0.15) !important;
    border-color: rgba(191, 219, 254, 0.36) !important;
}
[data-testid="stSidebar"] h3 {
    display: block !important;
    clear: both !important;
    width: 100% !important;
    white-space: nowrap !important;
}
[data-testid="stSidebar"] .stSelectbox {
    width: 100% !important;
}
[data-testid="stSidebar"] .stSelectbox label p {
    font-size: .78rem !important;
    font-weight: 900 !important;
}

/* Executive Overview: homogeneous vertical rhythm between KPI, findings and quick actions. */
.overview-row-gap { height: 22px !important; }
.overview-row-gap-small { height: 18px !important; }
.home-hero { margin-bottom: 26px !important; }
.metric-card, .scouting-hero-card, .quick-action-card {
    overflow: visible !important;
}
.metric-card {
    min-height: 88px !important;
    margin-bottom: 0 !important;
}
.scouting-hero-card {
    min-height: 146px !important;
}
.quick-action-grid {
    margin-top: 0 !important;
    margin-bottom: 26px !important;
    gap: 20px !important;
}
.quick-action-card {
    min-height: 92px !important;
}

/* Info disclosures must float above lower cards instead of being clipped. */
.metric-card-info, .metric-label-with-info, .metric-info-details {
    overflow: visible !important;
}
.metric-card-info {
    position: relative !important;
    z-index: 20 !important;
}
.metric-card-info:has(.metric-info-details[open]) {
    z-index: 9998 !important;
}
.metric-info-details[open] {
    z-index: 9999 !important;
}
.metric-info-details div {
    z-index: 9999 !important;
    top: 26px !important;
    box-shadow: 0 20px 44px rgba(15,23,42,.22) !important;
}

/* Quick Guide: no overlap with chips or page content when expanded. */
.compact-context-panel {
    overflow: visible !important;
    min-height: 0 !important;
}
.compact-context-panel .context-chip-row {
    max-height: none !important;
    overflow: visible !important;
}
.quick-guide-inline {
    position: relative !important;
    z-index: 30 !important;
    margin-top: 8px !important;
}
.quick-guide-inline[open] {
    z-index: 999 !important;
    margin-bottom: 12px !important;
}
.quick-guide-inline-body {
    position: relative !important;
    z-index: 1000 !important;
}

/* Main content width safety: prevent accidental horizontal layout in sidebar sections. */
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: .55rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 13.5 UX polish v5: guide, sidebar help and context overflow fix
# =============================================================================
st.markdown(
    """
<style>
/* Sidebar filters: concise explanatory disclosure instead of a long static caption. */
[data-testid="stSidebar"] .sidebar-filter-helper-label {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
    font-weight: 750 !important;
    margin: 0 0 .15rem 0 !important;
}
[data-testid="stSidebar"] div[data-testid="stPopover"] button {
    min-height: 26px !important;
    height: 26px !important;
    width: 28px !important;
    padding: 0 !important;
    justify-content: center !important;
    border-radius: 999px !important;
    font-weight: 950 !important;
    background: rgba(219,234,254,.13) !important;
    border: 1px solid rgba(191,219,254,.32) !important;
}
[data-testid="stSidebar"] .stSelectbox { margin-top: .15rem !important; }
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    min-height: 40px !important;
    box-shadow: 0 8px 18px rgba(2,6,23,.16) !important;
}

/* Context panel must grow when a search chip is added and the guide is opened. */
.context-strip-v2.compact-context-panel,
.compact-context-panel {
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
    padding-bottom: 14px !important;
}
.compact-context-panel .context-chip-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    max-height: none !important;
    overflow: visible !important;
    margin-top: 10px !important;
    margin-bottom: 10px !important;
}
.context-action-row {
    display: block !important;
    clear: both !important;
    width: 100% !important;
    margin-top: 8px !important;
    position: relative !important;
    z-index: 10 !important;
}
.quick-guide-inline {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    position: relative !important;
    overflow: visible !important;
    margin-top: 8px !important;
    margin-bottom: 0 !important;
}
.quick-guide-inline[open] {
    margin-bottom: 16px !important;
    z-index: 1000 !important;
}
.quick-guide-inline summary {
    display: flex !important;
    align-items: center !important;
    min-height: 38px !important;
    padding: 9px 14px 9px 18px !important;
    border-radius: 13px !important;
}
.quick-guide-inline-body {
    padding: 12px 14px 14px 18px !important;
    position: relative !important;
    z-index: 1001 !important;
}
.quick-guide-layout {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 10px !important;
    margin-bottom: 10px !important;
}
.quick-guide-card,
.quick-guide-glossary {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 10px 11px !important;
    box-shadow: 0 6px 16px rgba(15,23,42,.035) !important;
}
.quick-guide-card span,
.quick-guide-glossary > span {
    display: block !important;
    color: #2563eb !important;
    font-size: .68rem !important;
    font-weight: 950 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}
.quick-guide-card b {
    display: block !important;
    color: #0f172a !important;
    font-size: .84rem !important;
    margin-bottom: 4px !important;
}
.quick-guide-card small {
    display: block !important;
    color: #475569 !important;
    font-size: .74rem !important;
    line-height: 1.35 !important;
}
.quick-guide-glossary {
    display: grid !important;
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 8px !important;
}
.quick-guide-glossary > span {
    grid-column: 1 / -1 !important;
}
.quick-guide-glossary div {
    border: 1px solid #edf2f7 !important;
    border-radius: 10px !important;
    padding: 8px 9px !important;
    background: #f8fbff !important;
}
.quick-guide-glossary b {
    display: block !important;
    color: #0f172a !important;
    font-size: .76rem !important;
    margin-bottom: 3px !important;
}
.quick-guide-glossary small {
    display: block !important;
    color: #64748b !important;
    font-size: .70rem !important;
    line-height: 1.30 !important;
}
@media (max-width: 1280px) {
    .quick-guide-layout { grid-template-columns: 1fr !important; }
    .quick-guide-glossary { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 13.5 UX polish v6: guide moved to search row and compact sidebar filters
# =============================================================================
st.markdown(
    """
<style>
/* Search helper row: examples and guide live together, so the context panel cannot overlap. */
.search-helper-row {
    display: flex !important;
    align-items: flex-start !important;
    gap: 10px !important;
    flex-wrap: wrap !important;
    margin-top: 10px !important;
}
.search-helper-row .final-search-examples {
    margin: 0 !important;
    white-space: nowrap !important;
}
.search-quick-guide {
    width: fit-content !important;
    min-width: 170px !important;
    max-width: 100% !important;
    margin: 0 !important;
}
.search-quick-guide summary {
    min-height: 32px !important;
    padding: 7px 12px 7px 16px !important;
    white-space: nowrap !important;
}
.search-quick-guide[open] {
    width: 100% !important;
    margin-top: 4px !important;
    z-index: 1001 !important;
}
.search-quick-guide .quick-guide-inline-body {
    position: relative !important;
    z-index: 1002 !important;
}

/* Context panel no longer owns Quick Guide: keep it compact and avoid hidden chip text. */
.context-action-row { display: none !important; }
.compact-context-panel .context-chip-row {
    max-height: none !important;
    overflow: visible !important;
    margin-bottom: 0 !important;
}
.context-strip-v2.compact-context-panel {
    padding-bottom: 16px !important;
}

/* Sidebar filters: title + native HTML disclosure, no white popover field. */
[data-testid="stSidebar"] .sidebar-filter-disclosure {
    margin: 0.05rem 0 0.10rem 0 !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
}
[data-testid="stSidebar"] .sidebar-filter-disclosure summary {
    list-style: none !important;
    cursor: pointer !important;
    color: #93c5fd !important;
    -webkit-text-fill-color: #93c5fd !important;
    font-size: .76rem !important;
    line-height: 1.2 !important;
    font-weight: 950 !important;
    letter-spacing: .09em !important;
    text-transform: uppercase !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
}
[data-testid="stSidebar"] .sidebar-filter-disclosure summary::-webkit-details-marker { display: none !important; }
[data-testid="stSidebar"] .sidebar-filter-disclosure[open] summary {
    margin-bottom: 8px !important;
}
[data-testid="stSidebar"] .sidebar-filter-disclosure div {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
    background: rgba(219, 234, 254, 0.08) !important;
    border: 1px solid rgba(191, 219, 254, 0.22) !important;
    border-radius: 11px !important;
    padding: 9px 10px !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

/* Preset selector: clearer separation between label and dropdown. */
[data-testid="stSidebar"] .stSelectbox label {
    margin-bottom: 7px !important;
}
[data-testid="stSidebar"] .stSelectbox label p {
    line-height: 1.25 !important;
}
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    margin-top: 3px !important;
}
[data-testid="stSidebar"] .sidebar-preset-card {
    margin-top: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 14 final UX patch: strategy metric tooltips and clean portfolio map
# =============================================================================
st.markdown(
    """
<style>
.strategy-info-details {
    position: relative !important;
    display: inline-block !important;
    margin-left: 6px !important;
    vertical-align: 1px !important;
}
.strategy-info-details summary {
    list-style: none !important;
    width: 18px !important;
    height: 18px !important;
    border-radius: 999px !important;
    background: #3b82f6 !important;
    color: #ffffff !important;
    font-size: 11px !important;
    font-weight: 950 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    user-select: none !important;
}
.strategy-info-details summary::-webkit-details-marker { display: none !important; }
.strategy-info-details div {
    position: absolute !important;
    right: 0 !important;
    top: 24px !important;
    z-index: 9999 !important;
    min-width: 260px !important;
    max-width: 320px !important;
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 12px !important;
    padding: 10px 12px !important;
    color: #334155 !important;
    font-size: .76rem !important;
    line-height: 1.38 !important;
    box-shadow: 0 20px 44px rgba(15,23,42,.22) !important;
}
.metric-card:has(.strategy-info-details[open]) {
    position: relative !important;
    z-index: 9998 !important;
    overflow: visible !important;
}
.strategy-glossary-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    padding: 2px 2px 12px 2px;
    margin-bottom: 6px;
}
.strategy-glossary-item {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #f8fbff;
    padding: 11px 12px 12px 12px;
    min-height: 82px;
    box-sizing: border-box;
}
.strategy-glossary-item b {
    display: block;
    color: #0f172a;
    font-size: 0.82rem;
    margin-bottom: 5px;
}
.strategy-glossary-item span {
    display: block;
    color: #475569;
    font-size: 0.76rem;
    line-height: 1.38;
}
div[data-testid="stExpander"]:has(.strategy-glossary-grid) {
    overflow: visible !important;
    padding-bottom: 8px !important;
}

.strategy-glossary-details {
    width: 100%;
    background: #ffffff;
    border: 1px solid #dbe3ee;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(15,23,42,.035);
    margin: 12px 0 16px 0;
    overflow: hidden;
}
.strategy-glossary-details summary {
    list-style: none;
    min-height: 46px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 11px 16px;
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    color: #0f172a;
    font-weight: 850;
    cursor: pointer;
    user-select: none;
}
.strategy-glossary-details summary::-webkit-details-marker {
    display: none;
}
.strategy-glossary-details summary::before {
    content: "›";
    color: #0f172a;
    font-size: 1.1rem;
    font-weight: 950;
    line-height: 1;
    margin-right: 4px;
}
.strategy-glossary-details[open] summary::before {
    transform: rotate(90deg);
}
.strategy-glossary-details summary,
.strategy-glossary-details summary * {
    background-color: transparent !important;
}
.strategy-glossary-details[open] summary {
    border-bottom: 1px solid #e5edf7;
}
@media (max-width: 1200px) {
    .strategy-glossary-grid { grid-template-columns: 1fr !important; }
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


def load_transfer_strategy_optimizer():
    """Load the Sprint 14 transfer portfolio optimizer from src/strategy.

    The import is intentionally lazy so the dashboard can still render a clear
    error message if the strategy module or PuLP dependency is missing.
    """
    if str(STRATEGY_SRC_PATH) not in sys.path:
        sys.path.append(str(STRATEGY_SRC_PATH))

    from optimize_transfer_portfolio import optimize_portfolio

    return optimize_portfolio


def optimize_transfer_portfolio_with_style(
    budget: float,
    positions_needed: list[str],
    scenario: str = "balanced",
    max_signings: int = 5,
    min_budget_utilization: float = 0.70,
    portfolio_style: str = "balanced_portfolio",
) -> pd.DataFrame:
    """Optimize a transfer portfolio with optional concentration constraints.

    This dashboard-side wrapper keeps Sprint 14C self-contained: it preserves the
    existing ILP formulation and adds a portfolio-style layer to avoid overly
    concentrated outputs such as several micro-bets plus one very expensive asset.
    """
    try:
        import pulp
    except ModuleNotFoundError:
        # Fallback for environments where PuLP is not available but the project
        # optimizer exists. The external optimizer may not support style constraints.
        optimize_portfolio = load_transfer_strategy_optimizer()
        return optimize_portfolio(
            budget=budget,
            positions_needed=positions_needed,
            scenario=scenario,
            max_signings=max_signings,
            min_budget_utilization=min_budget_utilization,
        )

    input_file = STRATEGY_REPORTS_PATH / "transfer_portfolio_dataset.csv"
    if not input_file.exists():
        raise FileNotFoundError(
            f"Portfolio dataset not found: {input_file}. Run src/strategy/build_transfer_portfolio_dataset.py first."
        )

    scenario_config = {
        "conservative": {
            "min_confidence": 75,
            "max_avg_risk_proxy": 25,
            "value_weight": 0.75,
            "roi_weight": 0.25,
        },
        "balanced": {
            "min_confidence": 60,
            "max_avg_risk_proxy": 40,
            "value_weight": 0.65,
            "roi_weight": 0.35,
        },
        "aggressive": {
            "min_confidence": 45,
            "max_avg_risk_proxy": 60,
            "value_weight": 0.50,
            "roi_weight": 0.50,
        },
    }

    style_config = {
        # Pure value hunting. Keeps the previous formulation for comparison.
        "value_hunting": {
            "max_player_budget_share": None,
            "max_player_portfolio_cost_share": None,
            "min_mid_tier_signings": 0,
        },
        # Balanced portfolio. Avoids the 4 cheap bets + 1 budget filler pattern.
        "balanced_portfolio": {
            "max_player_budget_share": 0.45,
            "max_player_portfolio_cost_share": 0.60,
            "min_mid_tier_signings": 2,
        },
        # Allows one larger strategic asset, but still prevents full concentration.
        "star_prospects": {
            "max_player_budget_share": 0.65,
            "max_player_portfolio_cost_share": 0.75,
            "min_mid_tier_signings": 1,
        },
    }

    if scenario not in scenario_config:
        raise ValueError(f"Invalid scenario: {scenario}")
    if portfolio_style not in style_config:
        raise ValueError(f"Invalid portfolio style: {portfolio_style}")

    def _minmax(series: pd.Series) -> pd.Series:
        s = pd.to_numeric(series, errors="coerce")
        if s.dropna().empty:
            return pd.Series(0.0, index=s.index)
        if s.max() == s.min():
            return pd.Series(50.0, index=s.index)
        return 100 * (s - s.min()) / (s.max() - s.min())

    df = pd.read_csv(input_file)

    if "expected_roi" not in df.columns:
        df["expected_roi"] = np.where(
            pd.to_numeric(df["market_value_eur"], errors="coerce") > 0,
            pd.to_numeric(df["expected_upside"], errors="coerce") / pd.to_numeric(df["market_value_eur"], errors="coerce"),
            np.nan,
        )

    if "matching_confidence_norm" not in df.columns:
        df["matching_confidence_norm"] = pd.to_numeric(df["matching_confidence"], errors="coerce").clip(0, 1) * 100

    numeric_cols = [
        "portfolio_cost",
        "portfolio_value_score",
        "expected_upside",
        "expected_roi",
        "matching_confidence_norm",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    candidates = df[df["is_eligible_portfolio"] == True].copy()
    candidates = candidates[candidates["portfolio_cost"] <= budget].copy()

    if positions_needed:
        candidates = candidates[candidates["position_group"].isin(positions_needed)].copy()

    config = scenario_config[scenario]
    style = style_config[portfolio_style]

    candidates = candidates[candidates["matching_confidence_norm"] >= config["min_confidence"]].copy()
    candidates["risk_proxy"] = 100 - candidates["matching_confidence_norm"]
    candidates["roi_score_norm"] = _minmax(candidates["expected_roi"])
    candidates["optimization_score"] = (
        config["value_weight"] * candidates["portfolio_value_score"]
        + config["roi_weight"] * candidates["roi_score_norm"]
    )

    candidates = candidates.dropna(
        subset=[
            "portfolio_cost",
            "portfolio_value_score",
            "optimization_score",
            "expected_upside",
            "expected_roi",
            "risk_proxy",
        ]
    ).reset_index(drop=True)

    if candidates.empty:
        raise ValueError("No eligible candidates found under current constraints.")

    model = pulp.LpProblem("transfer_portfolio_optimization_with_style", pulp.LpMaximize)
    x = {i: pulp.LpVariable(f"x_{i}", cat="Binary") for i in candidates.index}

    selected_count = pulp.lpSum(x[i] for i in candidates.index)
    selected_cost = pulp.lpSum(candidates.loc[i, "portfolio_cost"] * x[i] for i in candidates.index)

    model += pulp.lpSum(candidates.loc[i, "optimization_score"] * x[i] for i in candidates.index)

    model += selected_cost <= budget
    model += selected_cost >= budget * min_budget_utilization
    model += selected_count <= max_signings
    model += selected_count >= 1

    model += pulp.lpSum(candidates.loc[i, "risk_proxy"] * x[i] for i in candidates.index) <= config[
        "max_avg_risk_proxy"
    ] * selected_count

    unique_positions = list(dict.fromkeys(positions_needed))
    if unique_positions and max_signings >= len(unique_positions):
        for pos in unique_positions:
            available_pos = candidates[candidates["position_group"] == pos]
            if not available_pos.empty:
                model += pulp.lpSum(x[i] for i in available_pos.index) >= 1

    max_budget_share = style["max_player_budget_share"]
    if max_budget_share is not None:
        for i in candidates.index:
            model += candidates.loc[i, "portfolio_cost"] * x[i] <= budget * max_budget_share

    max_portfolio_cost_share = style["max_player_portfolio_cost_share"]
    if max_portfolio_cost_share is not None:
        for i in candidates.index:
            model += candidates.loc[i, "portfolio_cost"] * x[i] <= max_portfolio_cost_share * selected_cost

    min_mid_tier_signings = int(style["min_mid_tier_signings"])
    if min_mid_tier_signings > 0 and max_signings >= min_mid_tier_signings:
        # Require a minimum number of players above a modest cost floor. This is
        # a practical proxy for avoiding portfolios made almost entirely of very
        # low-cost punts.
        mid_tier_floor = max(1_500_000, budget * 0.05)
        mid_tier_candidates = candidates[candidates["portfolio_cost"] >= mid_tier_floor]
        if len(mid_tier_candidates) >= min_mid_tier_signings:
            model += pulp.lpSum(x[i] for i in mid_tier_candidates.index) >= min_mid_tier_signings

    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)
    status = pulp.LpStatus[model.status]

    # If the selected style is too restrictive for a specific input combination,
    # fall back to a feasible value-hunting solution instead of breaking the UI.
    if status != "Optimal" and portfolio_style != "value_hunting":
        return optimize_transfer_portfolio_with_style(
            budget=budget,
            positions_needed=positions_needed,
            scenario=scenario,
            max_signings=max_signings,
            min_budget_utilization=min_budget_utilization,
            portfolio_style="value_hunting",
        )

    if status != "Optimal":
        raise ValueError(f"No optimal solution found. Solver status: {status}")

    selected_idx = [i for i in candidates.index if pulp.value(x[i]) == 1]
    portfolio = candidates.loc[selected_idx].copy()
    portfolio["scenario"] = scenario
    portfolio["budget"] = budget
    portfolio["max_signings"] = max_signings
    portfolio["solver_status"] = status
    portfolio["portfolio_style"] = portfolio_style
    portfolio["budget_utilization"] = portfolio["portfolio_cost"].sum() / budget
    portfolio["player_budget_share"] = portfolio["portfolio_cost"] / budget
    portfolio["player_portfolio_cost_share"] = portfolio["portfolio_cost"] / portfolio["portfolio_cost"].sum()

    return portfolio.sort_values("optimization_score", ascending=False)


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
    raw_label = translate_tier(value)
    label = V(raw_label) if "V" in globals() else raw_label
    if raw_label == "Alta prioridad":
        return f'<span class="badge-red">{html.escape(V(label))}</span>'
    if raw_label == "Objetivo scouting":
        return f'<span class="badge-yellow">{html.escape(V(label))}</span>'
    return f'<span class="badge-gray">{html.escape(V(label))}</span>'


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



def format_signed_money_short(value):
    """Format signed monetary deltas compactly for executive tables."""
    try:
        numeric_value = float(value)
        sign = "+" if numeric_value > 0 else ""
        return f"{sign}{format_money_short(numeric_value)}"
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


def get_first_valid_numeric(row, columns, default=np.nan):
    """Return the first valid numeric value found in a row across candidate columns."""
    for col in columns:
        try:
            if col in row.index:
                value = pd.to_numeric(pd.Series([row[col]]), errors="coerce").iloc[0]
                if pd.notna(value):
                    return float(value)
        except Exception:
            continue
    return default


def format_age_metadata(row, lang: str = "ES") -> str:
    """Format age metadata safely for scouting cards.

    The Football Intelligence lookup can come from broader processed panels where
    age may be stored under a non-standard name or may be unavailable. This helper
    avoids rendering "nan años" and restores age when an alternate age column is
    present.
    """
    age_value = get_first_valid_numeric(
        row,
        [
            "age",
            "player_age",
            "age_years",
            "age_at_season",
            "age_latest",
            "tm_age",
            "transfermarkt_age",
        ],
    )
    if pd.notna(age_value):
        suffix = "years" if lang == "EN" else "años"
        return f"{age_value:.1f} {suffix}"
    return ""


def safe_get(row, col, default="N/A"):
    try:
        value = row[col]
        if pd.isna(value):
            return default
        return value
    except Exception:
        return default


# -----------------------------------------------------------------------------
# Lightweight i18n helpers
# -----------------------------------------------------------------------------
# Default language is defined before any global constants use T(). The sidebar
# selector later overwrites LANG, but functions call T()/UI() at render time.
LANG = globals().get("LANG", "ES")

TEXT = {
    "ES": {
        "search_label": "Buscar jugador, club, liga o posición",
        "search_placeholder": "Ej.: Amorim, Strasbourg, Ligue 1, MID...",
        "filters_title": "FILTROS",
        "filters_caption": "Define criterios de elegibilidad antes de revisar ranking, matriz y perfiles.",
        "preset": "Preset de scouting",
        "selected_preset": "Preset seleccionado",
        "max_age": "Edad máxima",
        "min_minutes": "Minutos mínimos",
        "min_confidence": "Confidence Score mínimo",
        "league": "League" if LANG == "EN" else "Liga",
        "position": "Position" if LANG == "EN" else "Posición",
        "tier": "Tier de oportunidad",
        "opportunity_range": "Rango de Opportunity Score",
        "max_value": "Valor máximo (€M)",
        "min_roi": "ROI 3Y mínimo",
        "max_risk": "Risk Score máximo",
        "all_f": "Todas",
        "all_m": "Todos",
        "sort_by": "Ordenar por",
        "how_filters": "Cómo interpretar filtros, rangos y ordenación",
        "matrix_title": "Opportunity vs Risk Matrix",
        "matrix_caption": "Identifica objetivos prioritarios equilibrando potencial de mercado y riesgo estimado.",
        "methodology": "Ver metodología",
        "top5_title": "Top 5 oportunidades ajustadas por riesgo",
        "top5_caption": "Prioridad inicial para revisión de vídeo y contraste cualitativo.",
        "ranking_title": "Recruitment Ranking",
        "ranking_caption": "Vista ejecutiva compacta. La auditoría completa queda disponible en CSV y módulos detallados.",
    },
    "EN": {
        "search_label": "Search player, club, league or position",
        "search_placeholder": "e.g. Amorim, Strasbourg, Ligue 1, MID...",
        "filters_title": "FILTERS",
        "filters_caption": "Define eligibility criteria before reviewing rankings, matrix and profiles.",
        "preset": "Scouting preset",
        "selected_preset": "Selected preset",
        "max_age": "Maximum age",
        "min_minutes": "Minimum minutes",
        "min_confidence": "Minimum Confidence Score",
        "league": "League",
        "position": "Position",
        "tier": "Opportunity tier",
        "opportunity_range": "Opportunity Score range",
        "max_value": "Maximum value (€M)",
        "min_roi": "Minimum 3Y ROI",
        "max_risk": "Maximum Risk Score",
        "all_f": "All",
        "all_m": "All",
        "sort_by": "Sort by",
        "how_filters": "How to read filters, ranges and sorting",
        "matrix_title": "Opportunity vs Risk Matrix",
        "matrix_caption": "Identify priority targets by balancing market upside and estimated risk.",
        "methodology": "Show methodology",
        "top5_title": "Top 5 risk-adjusted opportunities",
        "top5_caption": "Initial priority list for video review and qualitative validation.",
        "ranking_title": "Recruitment Ranking",
        "ranking_caption": "Compact executive board. Full audit variables remain available in CSV and detailed modules.",
    },
}


def T(key: str) -> str:
    """Translate a fixed UI key using the active dashboard language."""
    language = globals().get("LANG", "ES")
    return TEXT.get(language, TEXT["ES"]).get(key, key)


SORT_LABELS = {
    "executive_decision_score_v2": {"ES": "Decision Score", "EN": "Decision Score"},
    "future_asset_score": {"ES": "Future Asset", "EN": "Future Asset"},
    "asset_roi_3y_pct": {"ES": "ROI 3Y", "EN": "ROI 3Y"},
    "risk_adjusted_opportunity_league": {"ES": "Context Fit", "EN": "Context Fit"},
    "risk_score": {"ES": "Risk Score", "EN": "Risk Score"},
    "projected_market_value_3y_eur": {"ES": "Valor proyectado 3Y", "EN": "Projected Value 3Y"},
    "opportunity_score": {"ES": "Market Opportunity", "EN": "Market Opportunity"},
}


def sort_label(col: str) -> str:
    language = globals().get("LANG", "ES")
    return SORT_LABELS.get(col, {}).get(language, col.replace("_", " ").title())


def UI(text: object) -> str:
    """Translate common free-text labels at render time.

    Keep this function deliberately simple: no recursive calls inside the
    dictionary, because it is used in early helper functions and in EN mode.
    """
    value = str(text)
    if globals().get("LANG", "ES") != "EN":
        return value
    translations = {
        "FILTROS": "FILTERS",
        "Define criterios de elegibilidad antes de revisar ranking, matriz y perfiles.": "Define eligibility criteria before reviewing rankings, matrix and profiles.",
        "Contexto activo": "Active context",
        "Universo modelado": "Modelled universe",
        "Shortlist ejecutiva": "Executive shortlist",
        "Candidatos actuales": "Current candidates",
        "jugadores precandidatos": "pre-candidates",
        "cobertura competitiva": "competitive coverage",
        "calidad del ranking": "ranking quality",
        "simulación conservadora": "conservative simulation",
        "de la shortlist": "of shortlist",
        "Ligas representadas": "Leagues represented",
        "Objetivos prioritarios": "Priority targets",
        "Apuestas de crecimiento": "Growth bets",
        "Bajo impacto": "Low impact",
        "Riesgo elevado": "High risk",
        "requiere validación adicional": "requires additional validation",
        "alto potencial · bajo riesgo": "high upside · low risk",
        "alto potencial · mayor incertidumbre": "high upside · higher uncertainty",
        "potencial limitado · menor riesgo": "limited upside · lower risk",
        "Mejor objetivo": "Best target",
        "Mejor oportunidad": "Best opportunity",
        "jugadores encontrados": "players found",
        "Actualizado con filtros activos": "Updated with active filters",
        "Edad": "Age",
        "Minutos": "Minutes",
        "Valor": "Value",
        "Valor 3Y": "3Y Value",
        "Acción": "Action",
        "Jugador": "Player",
        "Posición": "Position",
        "Liga": "League",
        "Club": "Club",
        "Selecciona entre 2 y 4 jugadores": "Select 2 to 4 players",
        "Misma posición": "Same position",
        "Toda la muestra": "Full sample",
        "Comparar contra": "Compare against",
        "Seleccionar jugador": "Select player",
        "Tarjetas de scouting": "Scouting cards",
        "Lectura scouting": "Scouting readout",
        "Selected player": "Selected player",
        "Reference player": "Reference player",
        "Player profile": "Player profile",
        "Radar scouting": "Radar scouting",
        "percentiles del jugador frente a su benchmark posicional para detectar fortalezas, debilidades y perfil dominante.": "player percentiles against the positional benchmark to identify strengths, weaknesses and dominant profile.",
        "Seleccionar jugador": "Select player",
        "Comparar contra": "Compare against",
        "Misma posición": "Same position",
        "Toda la muestra": "Full sample",
        "Benchmark": "Benchmark",
        "Posición": "Position",
        "Muestra": "Sample",
        "Edad media": "Average age",
        "Minutos medios": "Average minutes",
        "Tarjetas de scouting": "Scouting cards",
        "Lectura scouting": "Scouting readout",
        "Valor": "Value",
        "Valor jugador": "Player value",
        "Sin dato": "No data",
        "Muy alto": "Very high",
        "Alto": "High",
        "Promedio": "Average",
        "Bajo": "Low",
        "Mostrando": "Showing",
        "jugadores": "players",
        "Tier liga": "League tier",
        "Fase": "Stage",
        "Decision Drivers": "Decision Drivers",
        "Market Opportunity": "Market Opportunity",
        "Métrica": "Metric",
        "Percentil": "Percentile",

        "Mejor reemplazo": "Best replacement",
        "Similitud": "Similarity",
        "Adaptación": "Adaptation",
        "Riesgo": "Risk",
        "Jugador referencia": "Reference player",
        "Perfil más similar": "Most similar profile",
        "Similitud media": "Average similarity",
        "Mejor decisión global": "Best global decision",
        "Mayor valor proyectado": "Highest projected value",
        "Mejor ROI": "Best ROI",
        "Menor riesgo": "Lowest risk",
        "Activo menor riesgo": "Lowest-risk asset",
        "para": "for",
        "candidatos listos para validación": "candidates ready for validation",
        "seguimiento presencial": "live scouting follow-up",
        "prioridad de vídeo": "video priority",
        "seguimiento bajo": "low-priority tracking",
        "Top Future Asset": "Top Future Asset",
        "Best ROI": "Best ROI",
        "Score": "Score",
        "Líder Opportunity": "Opportunity leader",
        "Mejor Growth": "Best growth",
        "Mayor Confidence": "Highest confidence",
        "Menor Risk": "Lowest risk",
        "Mayor señal de oportunidad": "Highest opportunity signal",
        "Mayor potencial relativo": "Highest relative potential",
        "Señal más robusta": "Most robust signal",
        "Perfil menos incierto": "Least uncertain profile",
        "potencial económico-deportivo": "economic-sporting upside",
        "eficiencia de inversión": "investment efficiency",
        "proyección heurística": "heuristic projection",
        "prioridad máxima": "top priority",
        "candidatos accionables": "actionable candidates",
        "seguimiento activo": "active tracking",
        "monitorización pasiva": "passive monitoring",
        "Best global decision": "Best global decision",
        "Highest projected value": "Highest projected value",
        "Lowest risk": "Lowest risk",
        "top priority": "top priority",
        "actionable candidates": "actionable candidates",
        "active tracking": "active tracking",
        "passive monitoring": "passive monitoring",
    }
    return translations.get(value, value)

def render_metric_card(label, value, show_info_icon=False):
    label = TXT(label) if 'TXT' in globals() else label
    info_icon = " <span class='info-icon'>i</span>" if show_info_icon else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(UI(label))}{info_icon}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card_with_caption(label, value, caption=None, show_info_icon=False):
    info_icon = " <span class='info-icon'>i</span>" if show_info_icon else ""
    caption_html = (
        f"<div class='helper-caption'>{html.escape(UI(caption))}</div>"
        if caption
        else ""
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(UI(label))}{info_icon}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )





def render_strategy_metric_card(label, value, caption=None, tooltip=None):
    """Render Sprint 14 KPI card with click-to-open info disclosure."""
    tooltip_html = (
        "<details class='strategy-info-details'>"
        "<summary>i</summary>"
        f"<div>{html.escape(str(tooltip))}</div>"
        "</details>"
        if tooltip
        else ""
    )
    caption_html = (
        f"<div class='helper-caption'>{html.escape(str(caption))}</div>"
        if caption
        else ""
    )
    st.markdown(
        f"""
        <div class="metric-card metric-card-info">
            <div class="metric-label metric-label-with-info"><span>{html.escape(str(label))}</span>{tooltip_html}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_player_profile_header(row: pd.Series, name_col: str | None = None, title: str | None = None) -> None:
    """Render a compact Wyscout-style player identity header."""
    if row is None or len(row) == 0:
        return
    resolved_name_col = name_col or "player_name_fbref"
    player_name = str(safe_get(row, resolved_name_col, get_player_name(row)))
    position = str(safe_get(row, "position_group", "N/A"))
    club = str(safe_get(row, "club", "N/A"))
    league = league_display_name(safe_get(row, "league", "N/A"))
    age = format_score(safe_get(row, "age", np.nan))
    value = format_money_short(safe_get(row, "market_value_eur", np.nan))
    risk = format_score(safe_get(row, "risk_score", np.nan))
    header_title_map = {
        "Selected player": {"ES": "Jugador seleccionado", "EN": "Selected player"},
        "Reference player": {"ES": "Jugador referencia", "EN": "Reference player"},
        "Player profile": {"ES": "Perfil del jugador", "EN": "Player profile"},
    }
    if title:
        title_label = header_title_map.get(str(title), {}).get(LANG, UI(title))
        title_html = f"<div class='metric-label'>{html.escape(title_label)}</div>"
    else:
        title_html = ""
    st.markdown(
        f"""
        <div class="radar-info-box" style="padding:10px 14px;">
            {title_html}
            <b>{html.escape(player_name)}</b>
            <span style="color:#64748b;"> · {html.escape(position)} · {html.escape(club)} · {html.escape(league)} · {age} {"years" if globals().get("LANG") == "EN" else "años"} · {html.escape(value)} · Risk {risk}</span>
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

    The ranking CSV is intentionally narrow. The radar layer needs player-performance
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

def load_football_lookup_dataset() -> pd.DataFrame:
    """Load the broadest available current player-season dataset for global lookup.

    This intentionally prefers full processed panels over modeling/radar datasets,
    because modeling datasets may already be restricted to the actionable scouting
    age/minutes universe. The lookup layer must allow senior players to be found
    without altering the Scouting Universe, rankings or recommendations.
    """
    lookup_candidates = [
        "player_season_panel.parquet",
        "player_season_modeling.parquet",
        "player_season_modeling_advanced.parquet",
        "player_season_modeling_growth.parquet",
        "player_season_modeling_indices.parquet",
    ]
    for filename in lookup_candidates:
        candidate_df = load_parquet(PROCESSED_PATH / filename)
        if not candidate_df.empty:
            return candidate_df.copy()
    return pd.DataFrame()


def build_football_universe_dataset(scored_df: pd.DataFrame) -> pd.DataFrame:
    """Build a broader football universe from processed player-season data.

    The Scouting Universe remains the methodological recommendation layer. The
    Football Intelligence Layer is only used for informational lookup over the
    widest available player set while preserving scouting scores only where they
    exist.
    """
    lookup_source = load_football_lookup_dataset()
    if lookup_source.empty:
        football_df = scored_df.copy()
    else:
        football_df = lookup_source.copy()

    if "player_name_fbref" not in football_df.columns and "player_name" in football_df.columns:
        football_df = football_df.rename(columns={"player_name": "player_name_fbref"})
    if "player_name" not in football_df.columns and "player_name_fbref" in football_df.columns:
        football_df["player_name"] = football_df["player_name_fbref"]

    # Canonicalise age for broader Football Intelligence lookup datasets. Some
    # processed panels store age under alternative names, while the scouting
    # model expects a standard `age` column for display and filtering.
    age_aliases = [
        "player_age",
        "age_years",
        "age_at_season",
        "age_latest",
        "tm_age",
        "transfermarkt_age",
    ]
    if "age" not in football_df.columns:
        for alias in age_aliases:
            if alias in football_df.columns:
                football_df["age"] = pd.to_numeric(football_df[alias], errors="coerce")
                break
    elif football_df["age"].isna().all():
        for alias in age_aliases:
            if alias in football_df.columns:
                football_df["age"] = pd.to_numeric(football_df[alias], errors="coerce")
                break

    if "league" in football_df.columns:
        football_df["league"] = football_df["league"].replace({"Liga Portugal": "Primeira Liga"})

    # Football Intelligence is an informational lookup layer, but it must not
    # surface stale historical club-season rows as if they were current. Keep
    # the latest available season before de-duplicating players. This prevents
    # old entries such as former clubs from appearing in the global search when
    # a newer player-season panel exists.
    if "season" in football_df.columns:
        season_series = football_df["season"].dropna().astype(str)
        if not season_series.empty:
            latest_season = sorted(season_series.unique())[-1]
            football_df = football_df[football_df["season"].astype(str) == latest_season].copy()

    # Prefer the most recent player-season row when a processed panel contains
    # several rows per player in the latest season.
    name_col = get_player_name_column(football_df)
    if name_col is not None:
        sort_cols = []
        if "season" in football_df.columns:
            sort_cols.append("season")
        if "minutes_played" in football_df.columns:
            sort_cols.append("minutes_played")
        if sort_cols:
            ascending = [False] * len(sort_cols)
            football_df = football_df.sort_values(sort_cols, ascending=ascending)
        # One search result per player. Club and league are displayed as metadata
        # from the selected latest-season row, not as additional identity keys.
        football_df = football_df.drop_duplicates(subset=[name_col]).copy()

    score_cols = [
        "age",
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
        "future_asset_score",
        "asset_roi_3y_pct",
        "projected_market_value_3y_eur",
        "asset_upside_3y_eur",
        "projected_value_multiplier_3y",
        "executive_decision_score_v2",
        "opportunity_tier",
        "opportunity_tier_label",
        "recommendation_action",
        "undervalued_flag",
    ]
    merge_keys_options = [
        ["player_name_fbref", "season", "club"],
        ["player_name_fbref", "club"],
        ["player_name_tm", "season", "club"],
        ["player_name_tm", "club"],
        ["player_name_fbref"],
        ["player_name_tm"],
    ]
    enriched = football_df.copy()
    for candidate_keys in merge_keys_options:
        merge_keys = [col for col in candidate_keys if col in enriched.columns and col in scored_df.columns]
        if not merge_keys:
            continue
        cols_to_merge = merge_keys + [col for col in score_cols if col in scored_df.columns and col not in merge_keys]
        if len(cols_to_merge) <= len(merge_keys):
            continue
        right = scored_df[cols_to_merge].copy().drop_duplicates(subset=merge_keys)
        merged = enriched.merge(right, on=merge_keys, how="left", suffixes=("", "_scouting"))
        for col in score_cols:
            scouting_col = f"{col}_scouting"
            if scouting_col in merged.columns:
                if col in merged.columns:
                    merged[col] = merged[col].combine_first(merged[scouting_col])
                else:
                    merged[col] = merged[scouting_col]
                merged = merged.drop(columns=[scouting_col])
        enriched = merged
        break

    for col in numeric_cols:
        if col in enriched.columns:
            enriched[col] = pd.to_numeric(enriched[col], errors="coerce")

    required_defaults = {
        "market_value_eur": np.nan,
        "predicted_market_value_eur": np.nan,
        "market_value_gap_eur": np.nan,
        "market_value_gap_pct": np.nan,
        "opportunity_score": np.nan,
        "growth_score": np.nan,
        "confidence_score": np.nan,
        "risk_score": np.nan,
        "asset_roi_3y_pct": np.nan,
        "projected_market_value_3y_eur": np.nan,
        "asset_upside_3y_eur": np.nan,
        "projected_value_multiplier_3y": np.nan,
        "executive_decision_score_v2": np.nan,
    }
    for col, default in required_defaults.items():
        if col not in enriched.columns:
            enriched[col] = default

    if "opportunity_tier_label" not in enriched.columns:
        enriched["opportunity_tier_label"] = np.where(
            enriched["opportunity_score"].notna(), "Exploratorio", "Fuera del universo scoreado"
        )
    else:
        enriched["opportunity_tier_label"] = enriched["opportunity_tier_label"].fillna("Fuera del universo scoreado")

    enriched["is_scouting_universe"] = enriched["opportunity_score"].notna()
    enriched["universe_status"] = np.where(
        enriched["is_scouting_universe"],
        "Scouting opportunity universe",
        "Football intelligence only",
    )

    # Add transparent asset-management projections for the wider football layer.
    # Existing scouting values are preserved; missing values are filled only for
    # informational profiles outside the recommendation universe.
    try:
        projected_enriched = add_projected_market_value_features(enriched.copy())
        for col in [
            "projected_market_value_3y_eur",
            "asset_upside_3y_eur",
            "projected_value_multiplier_3y",
            "asset_roi_3y_pct",
            "future_asset_score",
        ]:
            if col in projected_enriched.columns:
                if col in enriched.columns:
                    enriched[col] = enriched[col].combine_first(projected_enriched[col])
                else:
                    enriched[col] = projected_enriched[col]
    except Exception:
        pass

    # Keep filters usable for non-scored players. These defaults do not create a
    # recommendation; they simply prevent missing scores from breaking discovery.
    enriched["confidence_score"] = pd.to_numeric(enriched["confidence_score"], errors="coerce").fillna(0)
    enriched["opportunity_score"] = pd.to_numeric(enriched["opportunity_score"], errors="coerce").fillna(0)
    enriched["risk_score"] = pd.to_numeric(enriched["risk_score"], errors="coerce").fillna(100)
    enriched["asset_roi_3y_pct"] = pd.to_numeric(enriched["asset_roi_3y_pct"], errors="coerce").fillna(0)
    enriched["executive_decision_score_v2"] = pd.to_numeric(enriched["executive_decision_score_v2"], errors="coerce").fillna(0)

    return enriched.reset_index(drop=True)


def get_available_radar_metrics(position_group: object, source_df: pd.DataFrame) -> list[tuple[str, str]]:
    """Return only position-specific football metrics available in the current data."""
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
        return UI("Sin dato")
    if percentile >= 90:
        return "Elite"
    if percentile >= 75:
        return UI("Muy alto")
    if percentile >= 60:
        return UI("Alto")
    if percentile >= 40:
        return UI("Promedio")
    return UI("Bajo")


def format_radar_metric_value(value) -> str:
    numeric_value = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric_value):
        return "Value unavailable" if globals().get("LANG") == "EN" else "Valor no disponible"
    label = "Player value" if globals().get("LANG") == "EN" else "Valor jugador"
    if abs(float(numeric_value)) >= 100:
        return f"{label}: {float(numeric_value):,.0f}"
    return f"{label}: {float(numeric_value):.2f}"


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
    closed_theta = radar_df["label"].map(metric_display_name).tolist() + [metric_display_name(radar_df["label"].iloc[0])]

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
        height=430,
        margin=dict(l=14, r=14, t=28, b=18),
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
                        <div class="radar-card-title">{html.escape(metric_display_name(row['label']))}</div>
                        <div class="radar-card-percentile">P{float(row['percentile']):.0f}</div>
                        <div class="radar-card-label">{html.escape(str(row['rating']))}</div>
                        <div class="radar-card-value">{html.escape(format_radar_metric_value(row['value']).replace('Valor jugador: ', 'Valor: ').replace('Player value: ', 'Value: '))}</div>
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
        f"<b>{'Reference universe' if LANG == 'EN' else 'Benchmark'}:</b> {html.escape(UI(str(benchmark_mode)).lower())}",
        f"<b>{UI('Posición')}:</b> {html.escape(str(player_position))}",
        f"<b>{UI('Muestra')}:</b> {n_players:,} {UI('jugadores')}",
    ]

    if pd.notna(avg_age):
        parts.append(f"<b>{UI('Edad media')}:</b> {avg_age:.1f} {'years' if globals().get('LANG') == 'EN' else 'años'}")

    if pd.notna(avg_minutes):
        parts.append(f"<b>{UI('Minutos medios')}:</b> {avg_minutes:,.0f}")

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
        f"""
<div class="radar-info-box">
<b>{UI('Radar scouting')}:</b> {UI('percentiles del jugador frente a su benchmark posicional para detectar fortalezas, debilidades y perfil dominante.')}</div>
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
            UI("Seleccionar jugador"),
            player_options,
            key="radar_selected_player",
        )
    with controls[1]:
        benchmark_mode = st.radio(
            UI("Comparar contra"),
            [UI("Misma posición"), UI("Toda la muestra")],
            horizontal=True,
            key="radar_benchmark_mode",
        )

    player_row = selector_df[selector_df[player_name_col].astype(str) == selected_radar_player].iloc[0]
    render_player_profile_header(player_row, player_name_col, "Selected player")
    player_position = normalize_position_group(safe_get(player_row, "position_group", "UNK"))

    benchmark_df = shortlist_df.copy()
    if benchmark_mode in {"Misma posición", "Same position"} and "position_group" in benchmark_df.columns:
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
            "No hay suficientes métricas disponibles para construir benchmarking posicional real. "
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
        st.subheader("🧾 " + UI("Tarjetas de scouting"))
        render_scouting_cards(radar_df)

        if missing_metrics:
            st.caption(
                "Métricas sin dato para este benchmark: " + ", ".join(sorted(set(missing_metrics)))
            )

    top_attributes = radar_df.sort_values("percentile", ascending=False).head(4)
    explanation = " · ".join(
        f"{metric_display_name(row['label'])} P{float(row['percentile']):.1f} ({row['rating']})"
        for _, row in top_attributes.iterrows()
    )
    st.markdown(
        (f"**Scouting readout:** {html.escape(str(selected_radar_player))} stands out mainly in {explanation}." if globals().get("LANG") == "EN" else f"**Lectura scouting:** {html.escape(str(selected_radar_player))} destaca principalmente en {explanation}.")
    )




# =============================================================================
# Comparative Scouting Intelligence helpers
# =============================================================================

COMPARISON_FEATURE_PRIORITY = [
    "minutes_played",
    "goals_per90",
    "assists_per90",
    "g_a_per90",
    "tackles_per90",
    "interceptions_per90",
    "blocks_per90",
    "growth_score",
    "confidence_score",
    "opportunity_score",
    "risk_score",
    "risk_adjusted_opportunity_score",
]

COMPARISON_TABLE_COLUMNS = [
    # Executive on-screen table. Auxiliary percentile/context columns remain
    # available in the CSV export, but are intentionally hidden from the
    # dashboard table to avoid horizontal overflow and improve decision readability.
    ("player_name_fbref", "Jugador"),
    ("club", "Club"),
    ("league", "Liga"),
    ("league_quality_tier", "Tier liga"),
    ("position_group", "Posición"),
    ("market_value_eur", "Valor"),
    ("projected_market_value_3y_eur", "Valor 3Y"),
    ("asset_roi_3y_pct", "ROI 3Y"),
    ("future_asset_score", "Future Asset"),
    ("executive_decision_score_v2", "Decision Score"),
    ("decision_stage", "Fase"),
    ("recommended_action", "Action" if LANG == "EN" else "Acción"),
    ("decision_drivers", "Decision Drivers"),
    ("opportunity_score", "Market Opportunity"),
    ("risk_adjusted_opportunity_league", "Context Fit"),
    ("risk_score", "Risk Score"),
]

# Full analytical columns exported in CSV for auditability.
COMPARISON_CSV_COLUMNS = [
    "player_name_fbref",
    "club",
    "league",
    "league_strength_index",
    "league_quality_tier",
    "position_group",
    "age",
    "minutes_played",
    "market_value_eur",
    "projected_market_value_3y_eur",
    "projected_value_multiplier_3y",
    "asset_upside_3y_eur",
    "asset_roi_3y_pct",
    "roi_score",
    "projected_value_score",
    "future_asset_score",
    "future_asset_tier",
    "executive_decision_score_v2",
    "decision_stage",
    "recommended_action",
    "decision_drivers",
    "replacement_fit_light",
    "opportunity_score",
    "context_opportunity_score",
    "league_adjusted_opportunity_score",
    "risk_score",
    "context_adjusted_risk_score",
    "risk_adjusted_opportunity_score",
    "risk_adjusted_opportunity_league",
    "growth_score",
    "confidence_score",
    "opportunity_percentile",
    "risk_percentile",
    "growth_percentile",
    "executive_recommendation",
]


# League Strength Adjustment
# -------------------------------------------------------------
# Lightweight contextual layer. These values are intentionally kept as a
# transparent configuration dictionary rather than as model inputs. They adjust
# scouting interpretation without changing the trained valuation model.
LEAGUE_STRENGTH_INDEX = {
    "Premier League": 100,
    "LaLiga": 96,
    "La Liga": 96,
    "Bundesliga": 94,
    "Serie A": 93,
    "Ligue 1": 89,
    "Eredivisie": 84,
    "Liga Portugal": 83,
    "Primeira Liga": 83,
    "Belgian Pro League": 80,
    "Jupiler Pro League": 80,
}

DEFAULT_LEAGUE_STRENGTH = 85


def get_league_strength(league: object) -> float:
    """Return a transparent competitive-context index for a league."""
    league_name = str(league).strip()
    if league_name in LEAGUE_STRENGTH_INDEX:
        return float(LEAGUE_STRENGTH_INDEX[league_name])

    normalized = league_name.lower()
    for key, value in LEAGUE_STRENGTH_INDEX.items():
        if key.lower() == normalized:
            return float(value)
    return float(DEFAULT_LEAGUE_STRENGTH)


def classify_league_quality(strength: object) -> str:
    """Translate league strength into an executive scouting tier."""
    value = pd.to_numeric(pd.Series([strength]), errors="coerce").iloc[0]
    if pd.isna(value):
        return "Sin clasificar"
    if value >= 96:
        return "Élite"
    if value >= 92:
        return "Muy alto"
    if value >= 88:
        return "Alto"
    if value >= 82:
        return "Competitivo"
    return "Emergente"




def classify_adaptation_risk(value: object) -> str:
    """Executive label for transition risk between competitive contexts."""
    numeric = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(numeric):
        return "Sin dato"
    if numeric < 4:
        return "Bajo"
    if numeric < 9:
        return "Medio"
    return "Alto"

def add_league_strength_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add contextual league-strength features to scouting outputs.

    These variables are not used to train the valuation model. They are
    post-model decision-support features designed to make candidates from
    different competitions more comparable for a sporting department.
    """
    if df.empty or "league" not in df.columns:
        return df.copy()

    result = df.copy()
    result["league_strength_index"] = result["league"].apply(get_league_strength)
    result["league_quality_tier"] = result["league_strength_index"].apply(classify_league_quality)

    # Keep the original Opportunity Score untouched and
    # add a separate contextual score. This avoids hiding the model signal while
    # making cross-league comparisons more transparent.
    result["league_strength_factor"] = (0.70 + 0.30 * result["league_strength_index"] / 100).clip(0.70, 1.00)

    if "opportunity_score" in result.columns:
        opportunity = pd.to_numeric(result["opportunity_score"], errors="coerce")
        result["league_adjusted_opportunity_score"] = (opportunity * result["league_strength_factor"]).clip(0, 100)
        result["context_opportunity_score"] = (
            0.75 * opportunity + 0.25 * result["league_strength_index"]
        ).clip(0, 100)

    if "risk_score" in result.columns:
        # External-validity uncertainty: lower-strength leagues receive only a
        # mild contextual risk uplift. This is not model leakage; it is a
        # post-model decision-support adjustment.
        result["context_adjusted_risk_score"] = (
            pd.to_numeric(result["risk_score"], errors="coerce")
            + np.maximum(0, 90 - result["league_strength_index"]) * 0.18
        ).clip(0, 100)

    if "risk_adjusted_opportunity_score" in result.columns:
        base_adj = pd.to_numeric(result["risk_adjusted_opportunity_score"], errors="coerce")
        context_opp = pd.to_numeric(result.get("context_opportunity_score", base_adj), errors="coerce")
        result["risk_adjusted_opportunity_league"] = (
            0.70 * base_adj + 0.30 * context_opp
        ).clip(0, 100)

    if "market_value_gap_eur" in result.columns:
        result["value_gap_adjusted_league_eur"] = (
            pd.to_numeric(result["market_value_gap_eur"], errors="coerce")
            * result["league_strength_index"] / 100
        )

    return result


# Projected Market Value Engine
# -------------------------------------------------------------
# Post-model business layer. These features do not retrain the valuation model;
# they transform current scouting signals into a simple asset-management view.

def get_age_projection_factor(age: object) -> float:
    """Return age-based upside factor for a 3-year projection horizon."""
    value = pd.to_numeric(pd.Series([age]), errors="coerce").iloc[0]
    if pd.isna(value):
        return 1.00
    if value <= 18.5:
        return 1.35
    if value <= 19.5:
        return 1.28
    if value <= 20.5:
        return 1.20
    if value <= 21.5:
        return 1.12
    if value <= 22.5:
        return 1.06
    if value <= 23.5:
        return 1.02
    return 0.96


def classify_future_asset_tier(score: object) -> str:
    """Executive label for asset appreciation potential."""
    value = pd.to_numeric(pd.Series([score]), errors="coerce").iloc[0]
    if pd.isna(value):
        return "Sin dato"
    if value >= 85:
        return "Activo estratégico"
    if value >= 70:
        return "Alto potencial"
    if value >= 55:
        return "Potencial medio"
    return "Potencial limitado"


def add_projected_market_value_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add asset-management features.

    The projection is intentionally heuristic and transparent. It combines
    current market value, Growth Score, Opportunity Score, age curve,
    confidence and league context to estimate a 3-year asset potential.
    It should be read as a decision-support scenario, not as a market forecast.
    """
    if df.empty:
        return df.copy()

    result = df.copy()
    if "market_value_eur" not in result.columns:
        return result

    market_value = pd.to_numeric(result["market_value_eur"], errors="coerce")
    growth = pd.to_numeric(result.get("growth_score", 50), errors="coerce").fillna(50).clip(0, 100)
    opportunity = pd.to_numeric(result.get("opportunity_score", 50), errors="coerce").fillna(50).clip(0, 100)
    confidence = pd.to_numeric(result.get("confidence_score", 65), errors="coerce").fillna(65).clip(0, 100)
    risk = pd.to_numeric(result.get("risk_score", 50), errors="coerce").fillna(50).clip(0, 100)

    if "league_strength_index" not in result.columns and "league" in result.columns:
        result["league_strength_index"] = result["league"].apply(get_league_strength)
        result["league_quality_tier"] = result["league_strength_index"].apply(classify_league_quality)

    strength = pd.to_numeric(result.get("league_strength_index", DEFAULT_LEAGUE_STRENGTH), errors="coerce").fillna(DEFAULT_LEAGUE_STRENGTH).clip(70, 100)
    age_factor = result.get("age", pd.Series([21] * len(result), index=result.index)).apply(get_age_projection_factor)

    growth_component = 1.00 + (growth / 100.0) * 1.15
    opportunity_component = 1.00 + np.maximum(0, opportunity - 50) / 100.0 * 0.70
    league_component = 0.92 + (strength / 100.0) * 0.10
    confidence_shrink = 0.60 + (confidence / 100.0) * 0.40
    risk_discount = 1.00 - np.maximum(0, risk - 55) / 100.0 * 0.20

    raw_multiplier = growth_component * opportunity_component * age_factor * league_component * risk_discount
    adjusted_multiplier = 1.00 + (raw_multiplier - 1.00) * confidence_shrink
    adjusted_multiplier = pd.to_numeric(adjusted_multiplier, errors="coerce").clip(1.00, 6.50)

    result["projected_market_value_3y_eur"] = (market_value * adjusted_multiplier).round(0)
    result["projected_value_multiplier_3y"] = adjusted_multiplier.round(2)
    result["asset_upside_3y_eur"] = (result["projected_market_value_3y_eur"] - market_value).round(0)
    result["asset_roi_3y_pct"] = np.where(
        market_value > 0,
        (result["asset_upside_3y_eur"] / market_value * 100).round(1),
        np.nan,
    )

    # Asset Score 2.0
    # ROI captures capital efficiency: for selling/development clubs, multiplying
    # the initial investment can be more attractive than maximising absolute upside.
    # Projected value score is percentile-based within the active scouting universe
    # to avoid letting expensive players dominate the asset score mechanically.
    result["roi_score"] = (
        pd.to_numeric(result["asset_roi_3y_pct"], errors="coerce")
        .clip(lower=0, upper=400)
        / 4.0
    ).clip(0, 100).round(1)

    projected_value = pd.to_numeric(result["projected_market_value_3y_eur"], errors="coerce")
    if projected_value.notna().sum() > 1:
        result["projected_value_score"] = (projected_value.rank(pct=True) * 100).round(1)
    else:
        result["projected_value_score"] = 50.0

    result["future_asset_score"] = (
        0.35 * result["roi_score"]
        + 0.25 * pd.to_numeric(result["projected_value_score"], errors="coerce").fillna(50)
        + 0.20 * opportunity
        + 0.10 * confidence
        + 0.10 * (100 - risk)
    ).clip(0, 100).round(1)
    result["future_asset_tier"] = result["future_asset_score"].apply(classify_future_asset_tier)
    return result


def enrich_scouting_context_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply post-model scouting context and asset features."""
    return add_projected_market_value_features(add_league_strength_features(df))


def get_player_name_column(df: pd.DataFrame) -> str | None:
    """Resolve the most reliable player-name column available in dashboard data."""
    for col in ["player_name_fbref", "player_name_tm", "player_name"]:
        if col in df.columns:
            return col
    return None


def add_comparison_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    """Add percentile columns used by comparison tables."""
    enriched = df.copy()
    percentile_sources = {
        "opportunity_score": "opportunity_percentile",
        "risk_score": "risk_percentile",
        "growth_score": "growth_percentile",
        "confidence_score": "confidence_percentile",
        "risk_adjusted_opportunity_score": "risk_adjusted_opportunity_percentile",
    }

    for source_col, percentile_col in percentile_sources.items():
        if source_col not in enriched.columns:
            continue
        values = pd.to_numeric(enriched[source_col], errors="coerce")
        enriched[percentile_col] = values.rank(pct=True, method="average") * 100

    return enriched


def format_comparison_value(col: str, value) -> str:
    """Format values for the executive comparison table."""
    if col in {"market_value_eur", "predicted_market_value_eur", "market_value_gap_eur", "value_gap_adjusted_league_eur", "projected_market_value_3y_eur", "asset_upside_3y_eur"}:
        return format_money_short(value)
    if col == "asset_roi_3y_pct":
        try:
            return f"{float(value):.0f}%"
        except Exception:
            return "N/A"
    if col in {"opportunity_score", "context_opportunity_score", "league_adjusted_opportunity_score", "risk_score", "context_adjusted_risk_score", "risk_adjusted_opportunity_score", "risk_adjusted_opportunity_league", "growth_score", "confidence_score", "league_strength_index", "adaptation_risk_score", "future_asset_score", "roi_score", "projected_value_score", "projected_value_multiplier_3y"}:
        return format_score(value)
    if col.endswith("_percentile"):
        try:
            return f"P{float(value):.0f}"
        except Exception:
            return "N/A"
    if col == "age":
        try:
            return f"{float(value):.1f}"
        except Exception:
            return "N/A"
    if col == "minutes_played":
        try:
            return f"{int(float(value)):,}"
        except Exception:
            return "N/A"
    if col == "league":
        return html.escape(league_display_name(value))
    if col in {"recommended_action", "replacement_fit", "adaptation_risk_label", "risk_level", "future_asset_tier", "executive_priority", "league_quality_tier"}:
        return html.escape(V(value))
    if col == "decision_drivers":
        return html.escape(driver_display_name(value))
    return html.escape(str(value)) if value is not None else "N/A"


def build_comparison_html_table(comparison_df: pd.DataFrame) -> str:
    """Build a compact HTML table for multi-player shortlist comparison."""
    available_columns = [(c, label) for c, label in COMPARISON_TABLE_COLUMNS if c in comparison_df.columns]
    header = "".join(f"<th>{html.escape(UI(label))}</th>" for _, label in available_columns)
    rows = ""

    for _, row in comparison_df.iterrows():
        cells = []
        for col, _ in available_columns:
            value = safe_get(row, col, "N/A")
            if col in {"executive_recommendation", "recommended_action"}:
                cells.append(f"<td>{recommendation_badge(str(value))}</td>")
            elif col == "risk_score":
                risk_value = get_numeric_value(row, col, np.nan)
                risk_class = "" if pd.isna(risk_value) or risk_value < 70 else " style='font-weight:850;color:#b91c1c;'"
                cells.append(f"<td{risk_class}>{format_comparison_value(col, value)}</td>")
            elif col in {"opportunity_score", "context_opportunity_score", "league_adjusted_opportunity_score", "risk_adjusted_opportunity_score", "risk_adjusted_opportunity_league", "projected_market_value_3y_eur", "asset_roi_3y_pct", "future_asset_score", "executive_decision_score_v2"}:
                cells.append(f"<td style='font-weight:850;'>{format_comparison_value(col, value)}</td>")
            else:
                cells.append(f"<td>{format_comparison_value(col, value)}</td>")
        rows += "<tr>" + "".join(cells) + "</tr>"

    return f"""
    <div class="comparison-table-wrapper">
        <table class="player-table">
            <thead><tr>{header}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """

def build_multi_player_radar_chart(
    selected_rows: pd.DataFrame,
    benchmark_df: pd.DataFrame,
    source_df: pd.DataFrame,
    name_col: str,
) -> go.Figure | None:
    """Build a radar chart that compares 2-4 players on the same percentile scale."""
    if selected_rows.empty or benchmark_df.empty:
        return None

    first_position = normalize_position_group(safe_get(selected_rows.iloc[0], "position_group", "UNK"))
    radar_metrics = get_available_radar_metrics(first_position, source_df)
    if len(radar_metrics) < 3:
        return None

    fig = go.Figure()

    for player_idx, (_, player_row) in enumerate(selected_rows.iterrows()):
        radar_records = []
        for metric, label in radar_metrics:
            if metric not in benchmark_df.columns:
                continue
            percentile = calculate_percentile(benchmark_df[metric], safe_get(player_row, metric, np.nan))
            if percentile is None:
                continue
            radar_records.append({"label": label, "percentile": percentile})

        radar_df = pd.DataFrame(radar_records)
        if radar_df.empty or len(radar_df) < 3:
            continue

        closed_r = radar_df["percentile"].tolist() + [radar_df["percentile"].iloc[0]]
        closed_theta = radar_df["label"].map(metric_display_name).tolist() + [metric_display_name(radar_df["label"].iloc[0])]
        player_name = str(safe_get(player_row, name_col, "Jugador"))

        # Readability fix: only the first selected player is softly filled; the
        # remaining candidates are displayed as stronger outlines. This avoids
        # visual saturation when comparing four similar profiles.
        trace_kwargs = {
            "r": closed_r,
            "theta": closed_theta,
            "name": player_name,
            "mode": "lines+markers",
            "opacity": 0.92,
            "line": dict(width=3),
            "hovertemplate": f"<b>{html.escape(player_name)}</b><br>%{{theta}}<br>Percentil %{{r:.1f}}<extra></extra>",
        }
        if player_idx == 0:
            trace_kwargs.update({"fill": "toself", "opacity": 0.78})
        else:
            trace_kwargs.update({"fill": "none"})

        fig.add_trace(go.Scatterpolar(**trace_kwargs))

    if not fig.data:
        return None

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
            )
        ),
        showlegend=True,
        height=460,
        margin=dict(l=14, r=14, t=28, b=56),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
    )
    return fig


def build_multi_player_percentile_matrix(
    selected_rows: pd.DataFrame,
    benchmark_df: pd.DataFrame,
    source_df: pd.DataFrame,
    name_col: str,
) -> pd.DataFrame:
    """Return one row per player-metric with benchmark percentiles for comparison tables."""
    if selected_rows.empty or benchmark_df.empty:
        return pd.DataFrame()

    first_position = normalize_position_group(safe_get(selected_rows.iloc[0], "position_group", "UNK"))
    radar_metrics = get_available_radar_metrics(first_position, source_df)
    records = []

    for _, player_row in selected_rows.iterrows():
        player_name = str(safe_get(player_row, name_col, "Jugador"))
        for metric, label in radar_metrics:
            if metric not in benchmark_df.columns:
                continue
            percentile = calculate_percentile(benchmark_df[metric], safe_get(player_row, metric, np.nan))
            if percentile is None:
                continue
            records.append(
                {
                    "metric": metric,
                    "Métrica": label,
                    "Jugador": player_name,
                    "Percentil": float(percentile),
                    "Valor": safe_get(player_row, metric, np.nan),
                }
            )

    return pd.DataFrame(records)


def render_multi_player_summary_cards(selected_rows: pd.DataFrame, name_col: str) -> None:
    """Render four compact executive cards for the selected comparison set."""
    if selected_rows.empty:
        return

    def best_player(score_col: str, ascending: bool = False) -> tuple[str, float | None]:
        if score_col not in selected_rows.columns:
            return "N/A", None
        tmp = selected_rows.copy()
        tmp["_score"] = pd.to_numeric(tmp[score_col], errors="coerce")
        tmp = tmp.dropna(subset=["_score"])
        if tmp.empty:
            return "N/A", None
        row = tmp.sort_values("_score", ascending=ascending).iloc[0]
        return str(safe_get(row, name_col, "N/A")), float(row["_score"])

    opportunity_name, opportunity_value = best_player("opportunity_score")
    growth_name, growth_value = best_player("growth_score")
    confidence_name, confidence_value = best_player("confidence_score")
    # Methodological convention: higher Risk Score means higher uncertainty,
    # therefore the safest candidate is the one with the minimum risk_score.
    risk_name, risk_value = best_player("risk_score", ascending=True)

    cards = st.columns(4)
    with cards[0]:
        caption = f"Opportunity Score: {opportunity_value:.1f}" if opportunity_value is not None else "Mayor señal de oportunidad"
        render_metric_card_with_caption("Líder Opportunity", opportunity_name, caption)
    with cards[1]:
        caption = f"Growth Score: {growth_value:.1f}" if growth_value is not None else "Mayor potencial relativo"
        render_metric_card_with_caption("Mejor Growth", growth_name, caption)
    with cards[2]:
        caption = f"Confidence Score: {confidence_value:.1f}" if confidence_value is not None else "Señal más robusta"
        render_metric_card_with_caption("Mayor Confidence", confidence_name, caption)
    with cards[3]:
        caption = f"Risk Score: {risk_value:.1f}" if risk_value is not None else "Perfil menos incierto"
        render_metric_card_with_caption("Menor Risk", risk_name, caption)


def render_metric_winners_table(percentile_matrix: pd.DataFrame) -> pd.DataFrame:
    """Show the player that leads each radar metric within the selected group.

    The analytical dataframe always stores Spanish internal column names
    (Métrica/Jugador/Percentil). We localize only the displayed copy. This avoids
    the EN-mode KeyError caused by selecting a non-existent internal column
    named 'Player'.
    """
    if percentile_matrix.empty:
        return pd.DataFrame()

    winners = (
        percentile_matrix.sort_values("Percentil", ascending=False)
        .drop_duplicates(subset=["Métrica"])
        .copy()
    )

    display_winners = winners[["Métrica", "Jugador", "Percentil"]].copy()
    display_winners["Métrica"] = display_winners["Métrica"].apply(metric_display_name)
    display_winners["Percentil"] = display_winners["Percentil"].map(lambda x: f"P{x:.0f}")

    if globals().get("LANG", "ES") == "EN":
        display_winners = display_winners.rename(
            columns={"Métrica": "Metric", "Jugador": "Player", "Percentil": "Percentile"}
        )
        title = "**Performance Leaders**"
    else:
        title = "**Ganador por métrica**"

    st.markdown(title)
    st.dataframe(
        display_winners,
        use_container_width=True,
        hide_index=True,
    )

    return winners

def build_comparative_conclusion(
    selected_rows: pd.DataFrame,
    metric_winners: pd.DataFrame,
    name_col: str,
) -> str | None:
    """Generate an automatic scouting narrative for the multi-player comparison."""
    if selected_rows.empty:
        return None

    def leader(score_col: str, ascending: bool = False) -> str | None:
        if score_col not in selected_rows.columns:
            return None
        tmp = selected_rows.copy()
        tmp["_score"] = pd.to_numeric(tmp[score_col], errors="coerce")
        tmp = tmp.dropna(subset=["_score"])
        if tmp.empty:
            return None
        row = tmp.sort_values("_score", ascending=ascending).iloc[0]
        return str(safe_get(row, name_col, "N/A"))

    opportunity_leader = leader("opportunity_score")
    growth_leader = leader("growth_score")
    confidence_leader = leader("confidence_score")
    risk_leader = leader("risk_score", ascending=True)

    offensive_labels = ["Goles/90", "Asistencias/90", "G+A/90", "Minutos"]
    offensive_sentence = None
    if metric_winners is not None and not metric_winners.empty:
        offensive_winners = metric_winners[metric_winners["Métrica"].isin(offensive_labels)].copy()
        if not offensive_winners.empty:
            counts = offensive_winners.groupby("Jugador")["Métrica"].agg(list).sort_values(key=lambda s: s.str.len(), ascending=False)
            offensive_leader = counts.index[0]
            led_metrics = counts.iloc[0]
            if len(led_metrics) >= 2:
                metric_text = ", ".join(led_metrics[:-1]) + f" y {led_metrics[-1]}" if len(led_metrics) > 2 else " y ".join(led_metrics)
                if LANG == "EN":
                    metric_text = " and ".join(metric_display_name(m) for m in led_metrics)
                    offensive_sentence = (
                        f"<b>{html.escape(str(offensive_leader))}</b> leads the group's attacking-production profile "
                        f"across {html.escape(metric_text)}."
                    )
                else:
                    offensive_sentence = (
                        f"<b>{html.escape(str(offensive_leader))}</b> domina el perfil de producción ofensiva "
                        f"del grupo, liderando {html.escape(metric_text)}."
                    )
            else:
                metric_label = metric_display_name(led_metrics[0]) if LANG == "EN" else str(led_metrics[0])
                offensive_sentence = (
                    f"<b>{html.escape(str(offensive_leader))}</b> stands out in {html.escape(metric_label)}."
                    if LANG == "EN"
                    else f"<b>{html.escape(str(offensive_leader))}</b> destaca en la métrica ofensiva {html.escape(str(led_metrics[0]))}."
                )

    sentences = []
    if offensive_sentence:
        sentences.append(offensive_sentence)
    if growth_leader:
        sentences.append(
            f"<b>{html.escape(growth_leader)}</b> shows the highest relative growth potential by Growth Score."
            if LANG == "EN"
            else f"<b>{html.escape(growth_leader)}</b> presenta el mayor potencial de crecimiento relativo según Growth Score."
        )
    if confidence_leader and risk_leader and confidence_leader == risk_leader:
        sentences.append(
            f"<b>{html.escape(confidence_leader)}</b> combines the most robust statistical signal with the lowest estimated risk."
            if LANG == "EN"
            else f"<b>{html.escape(confidence_leader)}</b> ofrece la señal estadística más robusta y el menor nivel de riesgo estimado."
        )
    else:
        if confidence_leader:
            sentences.append(
                f"<b>{html.escape(confidence_leader)}</b> offers the most robust signal by Confidence Score."
                if LANG == "EN"
                else f"<b>{html.escape(confidence_leader)}</b> ofrece la señal estadística más robusta según Confidence Score."
            )
        if risk_leader:
            sentences.append(
                f"<b>{html.escape(risk_leader)}</b> has the lowest estimated risk in the group."
                if LANG == "EN"
                else f"<b>{html.escape(risk_leader)}</b> presenta el menor nivel de riesgo estimado del grupo."
            )
    if opportunity_leader:
        sentences.append(
            f"<b>{html.escape(opportunity_leader)}</b> keeps the highest Opportunity Score and is currently the main scouting opportunity among the compared players."
            if LANG == "EN"
            else f"<b>{html.escape(opportunity_leader)}</b> mantiene el Opportunity Score más elevado y representa actualmente la principal oportunidad de scouting entre los jugadores comparados."
        )

    return "<br><br>".join(sentences) if sentences else None

def render_comparative_conclusion(
    selected_rows: pd.DataFrame,
    metric_winners: pd.DataFrame,
    name_col: str,
) -> None:
    conclusion = build_comparative_conclusion(selected_rows, metric_winners, name_col)
    if not conclusion:
        return

    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Scouting Insight"))}</b><br><br>
            {conclusion}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_selected_player_context(selected_rows: pd.DataFrame) -> None:
    """Render compact context for selected players because multiselect chips are intentionally short."""
    if selected_rows.empty or "_s11_detail_label" not in selected_rows.columns:
        return
    context = " · ".join(selected_rows["_s11_detail_label"].astype(str).tolist())
    st.caption(("Selected candidates: " if LANG == "EN" else "Candidatos seleccionados: ") + context)


def render_multi_player_radar_comparison(shortlist_df: pd.DataFrame) -> None:
    """Multi-player positional radar comparison."""
    st.subheader("🕸️ " + ("Radar comparativo de candidatos" if LANG == "ES" else "Candidate Comparison Radar"))
    st.markdown(
        f"""
<div class="radar-info-box">
<b>{html.escape(TXT("Comparación de candidatos"))}:</b> {html.escape(TXT("radar multi-jugador para contrastar fortalezas relativas y encaje deportivo sobre la misma escala percentil."))}
</div>
""",
        unsafe_allow_html=True,
    )

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info("No hay columna de nombre disponible para construir el comparador.")
        return

    selector_df = shortlist_df.dropna(subset=[name_col]).copy()
    if selector_df.empty:
        st.info("No hay jugadores disponibles para el radar comparativo.")
        return

    if "opportunity_score" in selector_df.columns:
        selector_df = selector_df.sort_values("opportunity_score", ascending=False)

    # -------------------------------------------------------------------------
    # UX fix:
    # - The selector must expose position and club.
    # - The default selection must be position-consistent.
    # - Mixed-position comparisons should explain the detected positions.
    # -------------------------------------------------------------------------
    if "position_group" in selector_df.columns:
        selector_df["_s11_position"] = selector_df["position_group"].apply(normalize_position_group)
    else:
        selector_df["_s11_position"] = "UNK"

    selector_df["_s11_player"] = selector_df[name_col].astype(str)
    selector_df["_s11_club"] = selector_df["club"].astype(str) if "club" in selector_df.columns else "Sin club"
    selector_df["_s11_league"] = selector_df["league"].astype(str) if "league" in selector_df.columns else "Sin liga"

    selector_df["_s11_detail_label"] = (
        selector_df["_s11_position"].astype(str)
        + " | "
        + selector_df["_s11_player"].astype(str)
        + " | "
        + selector_df["_s11_club"].astype(str)
        + " | "
        + selector_df["_s11_league"].astype(str)
    )

    # Compact labels keep the selected chips readable. When a player name is
    # duplicated in the shortlist, append club context to avoid ambiguity.
    duplicated_names = selector_df["_s11_player"].duplicated(keep=False)
    selector_df["_s11_selector_label"] = np.where(
        duplicated_names,
        selector_df["_s11_player"].astype(str)
        + " ("
        + selector_df["_s11_position"].astype(str)
        + " · "
        + selector_df["_s11_club"].astype(str)
        + ")",
        selector_df["_s11_player"].astype(str)
        + " ("
        + selector_df["_s11_position"].astype(str)
        + ")",
    )

    # Remove repeated labels while preserving the ranking order.
    selector_df = selector_df.drop_duplicates(subset=["_s11_selector_label"]).copy()

    # Choose the best default positional group by the highest-ranked player that
    # has at least two comparable candidates available. This avoids opening the
    # dashboard with an invalid mixed-position selection.
    default_position = None
    for position in selector_df["_s11_position"].dropna().astype(str).unique().tolist():
        if len(selector_df[selector_df["_s11_position"].astype(str) == position]) >= 2:
            default_position = position
            break

    if default_position is None:
        default_position = str(selector_df["_s11_position"].iloc[0])

    default_df = selector_df[selector_df["_s11_position"].astype(str) == default_position].head(4)
    if len(default_df) < 2:
        default_df = selector_df.head(min(4, len(selector_df)))

    option_labels = selector_df["_s11_selector_label"].tolist()
    default_labels = default_df["_s11_selector_label"].tolist()

    controls = st.columns([1.65, 0.95])
    with controls[0]:
        selected_labels = st.multiselect(
            TXT("Selecciona entre 2 y 4 jugadores"),
            option_labels,
            default=default_labels,
            max_selections=4,
            key="sprint11_multi_player_radar_selector_v2",
            help=(
                "The selected chip is compact. The context row below shows position, club and league for the chosen candidates."
                if LANG == "EN"
                else "La etiqueta seleccionada es compacta. La ficha de contexto inferior muestra posición, club y liga de los candidatos elegidos."
            ),
        )
    with controls[1]:
        benchmark_mode = st.radio(
            "Reference universe" if LANG == "EN" else "Universo de referencia",
            [TXT("Misma posición"), TXT("Toda la muestra")],
            horizontal=True,
            key="sprint11_multi_radar_benchmark",
        )

    if len(selected_labels) < 2:
        st.info(TXT("Selecciona al menos dos jugadores para comparar."))
        return

    selected_rows = selector_df[selector_df["_s11_selector_label"].isin(selected_labels)].copy()
    selected_rows = selected_rows.drop_duplicates(subset=["_s11_selector_label"])
    selected_positions = sorted(selected_rows["_s11_position"].dropna().astype(str).unique().tolist())

    if benchmark_mode in {"Misma posición", "Same position"} and len(selected_positions) > 1:
        positions_text = ", ".join(selected_positions)
        if LANG == "EN":
            st.warning(
                f"Detected positions: {positions_text}. To preserve methodological comparability, "
                "use players from the same position or switch the benchmark to 'Full sample'."
            )
            warning_html = "<b>Recommendation:</b> use the selector in <b>position | player | club | league</b> format and choose candidates from the same position. Example: <b>MID | Player | Club</b>."
        else:
            st.warning(
                f"Posiciones detectadas: {positions_text}. Para mantener comparabilidad metodológica, "
                "usa jugadores de la misma posición o cambia el benchmark a 'Toda la muestra'."
            )
            warning_html = "<b>Recomendación:</b> usa el selector en formato <b>posición | jugador | club | liga</b> y elige candidatos con la misma posición. Ejemplo: <b>MID | Jugador | Club</b>."
        st.markdown(
            f"""
<div class="radar-warning-box">
{warning_html}
</div>
""",
            unsafe_allow_html=True,
        )
        return

    benchmark_df = shortlist_df.copy()
    if benchmark_mode in {"Misma posición", "Same position"} and selected_positions and "position_group" in benchmark_df.columns:
        target_position = selected_positions[0]
        benchmark_df = benchmark_df[
            benchmark_df["position_group"].apply(normalize_position_group).astype(str) == target_position
        ].copy()
    else:
        target_position = "Global"

    # More explicit context than the generic benchmark card.
    n_players = len(benchmark_df)
    avg_age = pd.to_numeric(benchmark_df["age"], errors="coerce").mean() if "age" in benchmark_df.columns else np.nan
    avg_minutes = pd.to_numeric(benchmark_df["minutes_played"], errors="coerce").mean() if "minutes_played" in benchmark_df.columns else np.nan
    selected_positions_text = ", ".join(selected_positions) if selected_positions else "N/A"

    if benchmark_mode in {"Misma posición", "Same position"}:
        context_parts = [
            f"<b>{html.escape('Reference universe' if LANG == 'EN' else 'Benchmark')}:</b> {html.escape(TXT('Misma posición'))}",
            f"<b>{html.escape(TXT('Grupo posicional'))}:</b> {html.escape(str(target_position))}",
            f"<b>{html.escape(TXT('Muestra'))}:</b> {n_players:,} {html.escape(TXT('jugadores'))}",
        ]
    else:
        context_parts = [
            f"<b>{html.escape('Reference universe' if LANG == 'EN' else 'Benchmark')}:</b> {html.escape(TXT('Toda la muestra'))}",
            f"<b>{html.escape('Compared positions' if LANG == 'EN' else 'Posiciones comparadas')}:</b> {html.escape(selected_positions_text)}",
            f"<b>{html.escape(TXT('Muestra'))}:</b> {n_players:,} {html.escape(TXT('jugadores'))}",
        ]
    if pd.notna(avg_age):
        context_parts.append(f"<b>{html.escape(TXT('Edad media'))}:</b> {avg_age:.1f} {'years' if LANG == 'EN' else 'años'}")
    if pd.notna(avg_minutes):
        context_parts.append(f"<b>{html.escape(TXT('Minutos medios'))}:</b> {avg_minutes:,.0f}")

    render_selected_player_context(selected_rows)

    with st.expander("⚙️ " + ("Reference methodology" if LANG == "EN" else "Metodología del benchmark"), expanded=False):
        st.markdown(
            f"""
            <div class="radar-info-box">
                {" · ".join(context_parts)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_multi_player_summary_cards(selected_rows, name_col)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.subheader("📊 " + TXT("Comparación de percentiles"))
    st.caption(TXT("Radar comparativo basado en benchmarking dinámico por posición. Cada eje representa el percentil del jugador frente al universo de referencia seleccionado."))
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    radar_fig = build_multi_player_radar_chart(
        selected_rows=selected_rows,
        benchmark_df=benchmark_df,
        source_df=shortlist_df,
        name_col=name_col,
    )

    if radar_fig is None:
        st.info("No hay suficientes métricas comunes para construir el radar comparativo.")
        return

    left_radar_col, right_radar_col = st.columns([1.45, 0.95], gap="large")
    with left_radar_col:
        st.markdown("<div class='radar-chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(radar_fig, use_container_width=True, config={"displaylogo": False})
        st.markdown("</div>", unsafe_allow_html=True)

    percentile_matrix = build_multi_player_percentile_matrix(
        selected_rows=selected_rows,
        benchmark_df=benchmark_df,
        source_df=shortlist_df,
        name_col=name_col,
    )
    with right_radar_col:
        metric_winners = render_metric_winners_table(percentile_matrix)
        render_comparative_conclusion(selected_rows, metric_winners, name_col)



def get_numeric_value(row: pd.Series, col: str, default: float = np.nan) -> float:
    """Safely read a numeric value from a row."""
    try:
        value = pd.to_numeric(pd.Series([safe_get(row, col, default)]), errors="coerce").iloc[0]
        return float(value) if pd.notna(value) else default
    except Exception:
        return default


def get_display_name(row: pd.Series, name_col: str) -> str:
    return str(safe_get(row, name_col, safe_get(row, "player_name_fbref", "Jugador")))


def classify_candidate_recommendation(row: pd.Series) -> str:
    """Executive recommendation for a candidate comparison table."""
    opportunity = get_numeric_value(row, "opportunity_score", 0)
    risk = get_numeric_value(row, "risk_score", 100)
    adjusted = get_numeric_value(row, "risk_adjusted_opportunity_score", 0)
    confidence = get_numeric_value(row, "confidence_score", 0)

    if adjusted >= 55 and opportunity >= 80 and risk <= 45:
        return "Priorizar"
    if opportunity >= 80 and risk > 65:
        return "Analizar en vídeo"
    if adjusted >= 35 and confidence >= 65:
        return "Seguimiento"
    if risk >= 80:
        return "Descartar por riesgo"
    return "Revisión exploratoria"


def classify_replacement_fit(row: pd.Series) -> str:
    """Executive label for replacement candidates."""
    replacement = get_numeric_value(row, "replacement_score_league_adjusted", get_numeric_value(row, "replacement_score", 0))
    risk = get_numeric_value(row, "risk_score", 100)
    similarity = get_numeric_value(row, "similarity_score_pct", 0)

    if replacement >= 75 and similarity >= 70 and risk <= 55:
        return "Sustituto prioritario"
    if replacement >= 60 and similarity >= 60:
        return "Alternativa viable"
    if risk >= 80:
        return "Riesgo elevado"
    return "Seguimiento"


def recommendation_badge(label: str) -> str:
    """HTML badge for executive recommendation/action labels."""
    raw_label = str(label)
    if raw_label in {"Iniciar contacto", "Due diligence", "Vídeo scouting", "Seguimiento activo", "Monitorización pasiva", "No priorizar", "Analizar en vídeo"}:
        return render_action_badge(raw_label) if "render_action_badge" in globals() else f"<span class='badge-gray'>{html.escape(V(raw_label))}</span>"
    class_name = "badge-gray"
    if raw_label in {"Priorizar", "Sustituto prioritario"}:
        class_name = "badge-red"
    elif raw_label in {"Alternativa viable", "Seguimiento"}:
        class_name = "badge-yellow"
    return f'<span class="{class_name}">{html.escape(V(raw_label))}</span>'



def render_sprint11_context_box(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT(title))}</b><br>
            {html.escape(TXT(text))}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_candidate_decision_cards(df: pd.DataFrame, name_col: str) -> None:
    """Executive cards for candidate decision table."""
    if df.empty:
        return

    def pick(col: str, ascending: bool = False, money: bool = False, pct: bool = False) -> tuple[str, str]:
        if col not in df.columns:
            return "N/A", "Sin dato"
        tmp = df.copy()
        tmp["_v"] = pd.to_numeric(tmp[col], errors="coerce")
        tmp = tmp.dropna(subset=["_v"])
        if tmp.empty:
            return "N/A", "Sin dato"
        row = tmp.sort_values("_v", ascending=ascending).iloc[0]
        if money:
            caption = format_money_short(row["_v"])
        elif pct:
            caption = f"{row['_v']:.0f}%"
        else:
            caption = f"{row['_v']:.1f}"
        return get_display_name(row, name_col), caption

    decision_name, decision_value = pick("executive_decision_score_v2")
    value_name, value_caption = pick("projected_market_value_3y_eur", money=True)
    roi_name, roi_caption = pick("asset_roi_3y_pct", pct=True)
    asset_name, asset_caption = pick("future_asset_score")
    low_risk_name, low_risk_caption = pick("risk_score", ascending=True)

    if LANG == "EN":
        card_specs = [
            ("Best global decision", decision_name, f"Decision Score: {decision_value}"),
            ("Highest projected value", value_name, f"3Y Value: {value_caption}"),
            ("Best ROI", roi_name, f"ROI 3Y: {roi_caption}"),
            ("Top Future Asset", asset_name, f"Future Asset: {asset_caption}"),
            ("Lowest risk", low_risk_name, f"Risk Score: {low_risk_caption}"),
        ]
    else:
        card_specs = [
            ("Mejor decisión global", decision_name, f"Decision Score: {decision_value}"),
            ("Mayor valor proyectado", value_name, f"Valor 3Y: {value_caption}"),
            ("Mejor ROI", roi_name, f"ROI 3Y: {roi_caption}"),
            ("Top Future Asset", asset_name, f"Future Asset: {asset_caption}"),
            ("Menor riesgo", low_risk_name, f"Risk Score: {low_risk_caption}"),
        ]

    cols = st.columns(5)
    for col, (label, value, caption) in zip(cols, card_specs):
        with col:
            render_metric_card_with_caption(label, value, caption)


def render_decision_funnel_cards(df: pd.DataFrame) -> None:
    """Render recruitment funnel counts from decision_stage."""
    if df.empty or "decision_stage" not in df.columns:
        return
    order = ["Elite Target", "Shortlist", "Watchlist", "Monitor"]
    counts = df["decision_stage"].value_counts().reindex(order, fill_value=0)
    cols = st.columns(4)
    captions = (
        {
            "Elite Target": "top priority",
            "Shortlist": "actionable candidates",
            "Watchlist": "active tracking",
            "Monitor": "passive monitoring",
        }
        if LANG == "EN"
        else {
            "Elite Target": "prioridad máxima",
            "Shortlist": "candidatos accionables",
            "Watchlist": "seguimiento activo",
            "Monitor": "monitorización pasiva",
        }
    )
    for col, stage in zip(cols, order):
        with col:
            render_metric_card_with_caption(stage, int(counts[stage]), captions[stage])


def build_candidate_executive_summary(df: pd.DataFrame, name_col: str) -> str | None:
    """Build a short funnel-style executive summary for the active comparison set."""
    if df.empty:
        return None
    best = df.sort_values("executive_decision_score_v2", ascending=False).iloc[0]
    avg_roi = pd.to_numeric(df.get("asset_roi_3y_pct", np.nan), errors="coerce").mean()
    avg_risk = pd.to_numeric(df.get("risk_score", np.nan), errors="coerce").mean()
    elite_count = int((df.get("decision_stage", pd.Series(index=df.index, dtype=object)) == "Elite Target").sum())
    shortlist_count = int((df.get("decision_stage", pd.Series(index=df.index, dtype=object)).isin(["Elite Target", "Shortlist"])).sum())
    best_name = html.escape(get_display_name(best, name_col))
    best_score = get_numeric_value(best, "executive_decision_score_v2", np.nan)
    best_action = html.escape(str(safe_get(best, "recommended_action", "Vídeo scouting")))

    if LANG == "EN":
        best_action = html.escape(action_display_name(safe_get(best, "recommended_action", "Video scouting")))
        return (
            f"<b>{len(df)} candidates compared.</b> {elite_count} Elite Target and {shortlist_count} actionable Shortlist profiles. "
            f"Average expected ROI: <b>{avg_roi:.0f}%</b>; average risk: <b>{avg_risk:.1f}</b>. "
            f"The current best decision is <b>{best_name}</b> with Decision Score <b>{best_score:.1f}</b>; next action: <b>{best_action}</b>."
        )
    return (
        f"<b>{len(df)} candidatos comparados.</b> {elite_count} Elite Target y {shortlist_count} perfiles accionables en Shortlist. "
        f"ROI medio esperado: <b>{avg_roi:.0f}%</b>; riesgo medio: <b>{avg_risk:.1f}</b>. "
        f"La mejor decisión actual es <b>{best_name}</b> con Decision Score <b>{best_score:.1f}</b>; siguiente acción: <b>{best_action}</b>."
    )


def build_candidate_comparison_narrative(df: pd.DataFrame, name_col: str) -> str | None:
    """Automatic executive narrative for candidate comparison."""
    if df.empty:
        return None

    sorted_df = df.copy()
    if "executive_decision_score_v2" in sorted_df.columns:
        sorted_df["_sort"] = pd.to_numeric(sorted_df["executive_decision_score_v2"], errors="coerce")
        sorted_df = sorted_df.sort_values("_sort", ascending=False)
    elif "risk_adjusted_opportunity_league" in sorted_df.columns:
        sorted_df["_sort"] = pd.to_numeric(sorted_df["risk_adjusted_opportunity_league"], errors="coerce")
        sorted_df = sorted_df.sort_values("_sort", ascending=False)
    elif "risk_adjusted_opportunity_score" in sorted_df.columns:
        sorted_df["_sort"] = pd.to_numeric(sorted_df["risk_adjusted_opportunity_score"], errors="coerce")
        sorted_df = sorted_df.sort_values("_sort", ascending=False)
    elif "opportunity_score" in sorted_df.columns:
        sorted_df["_sort"] = pd.to_numeric(sorted_df["opportunity_score"], errors="coerce")
        sorted_df = sorted_df.sort_values("_sort", ascending=False)

    best = sorted_df.iloc[0]
    best_name = get_display_name(best, name_col)
    best_adj = get_numeric_value(best, "risk_adjusted_opportunity_score", np.nan)
    best_context = get_numeric_value(best, "risk_adjusted_opportunity_league", np.nan)
    best_opp = get_numeric_value(best, "opportunity_score", np.nan)
    best_risk = get_numeric_value(best, "risk_score", np.nan)
    best_strength = get_numeric_value(best, "league_strength_index", np.nan)

    low_risk = None
    if "risk_score" in df.columns:
        tmp = df.copy()
        tmp["_risk"] = pd.to_numeric(tmp["risk_score"], errors="coerce")
        tmp = tmp.dropna(subset=["_risk"])
        if not tmp.empty:
            low_risk = tmp.sort_values("_risk", ascending=True).iloc[0]

    if LANG == "EN":
        parts = [
            f"<b>{html.escape(best_name)}</b> appears as the strongest candidate in the comparison because of his combination of Opportunity Score "
            f"({best_opp:.1f}), risk-adjusted Opportunity ({best_adj:.1f}), final Context Fit ({best_context:.1f}) "
            f"and Risk Score ({best_risk:.1f}). His League Strength Index is {best_strength:.1f}."
        ]
        if "asset_roi_3y_pct" in best.index and "future_asset_score" in best.index:
            best_roi = get_numeric_value(best, "asset_roi_3y_pct", np.nan)
            best_asset = get_numeric_value(best, "future_asset_score", np.nan)
            if pd.notna(best_roi) and pd.notna(best_asset):
                parts.append(
                    f"From an asset-management perspective, he has an estimated 3Y ROI of {best_roi:.0f}% and a Future Asset Score of {best_asset:.1f}."
                )
        if low_risk is not None:
            low_risk_name = get_display_name(low_risk, name_col)
            parts.append(
                f"<b>{html.escape(low_risk_name)}</b> is the least uncertain profile in the group and can work as the lower-risk option."
            )
        parts.append(
            "The recommendation should be read as initial analytical prioritization: the ranking reduces the search space, but it does not replace qualitative validation through video, tactical context and scouting follow-up."
        )
        return "<br><br>".join(parts)

    parts = [
        f"<b>{html.escape(best_name)}</b> aparece como el candidato más sólido de la comparativa por su combinación de Opportunity Score "
        f"({best_opp:.1f}), Opportunity ajustada por riesgo ({best_adj:.1f}), Context Fit final ({best_context:.1f}) "
        f"y Risk Score ({best_risk:.1f}). Su League Strength Index es {best_strength:.1f}."
    ]
    if "asset_roi_3y_pct" in best.index and "future_asset_score" in best.index:
        best_roi = get_numeric_value(best, "asset_roi_3y_pct", np.nan)
        best_asset = get_numeric_value(best, "future_asset_score", np.nan)
        if pd.notna(best_roi) and pd.notna(best_asset):
            parts.append(
                f"Desde una óptica de gestión de activos, presenta un ROI 3Y estimado de {best_roi:.0f}% y un Future Asset Score de {best_asset:.1f}."
            )
    if low_risk is not None:
        low_risk_name = get_display_name(low_risk, name_col)
        parts.append(
            f"<b>{html.escape(low_risk_name)}</b> es el perfil menos incierto del grupo, por lo que puede funcionar como opción de menor riesgo relativo."
        )
    parts.append(
        "La recomendación debe interpretarse como priorización analítica inicial: el ranking reduce el espacio de búsqueda, pero no sustituye la validación cualitativa mediante vídeo, contexto táctico y seguimiento del área deportiva."
    )
    return "<br><br>".join(parts)

def add_similarity_deltas(similarity_df: pd.DataFrame, target_row: pd.Series) -> pd.DataFrame:
    """Add deltas against target player for executive interpretation."""
    result = similarity_df.copy()
    delta_cols = {
        "opportunity_score": "delta_opportunity",
        "risk_score": "delta_risk",
        "growth_score": "delta_growth",
        "market_value_eur": "delta_market_value_eur",
        "projected_market_value_3y_eur": "delta_projected_market_value_3y_eur",
        "future_asset_score": "delta_future_asset_score",
        "risk_adjusted_opportunity_score": "delta_risk_adjusted_opportunity",
        "league_strength_index": "delta_league_strength",
    }
    for source_col, delta_col in delta_cols.items():
        if source_col in result.columns and source_col in target_row.index:
            target_value = get_numeric_value(target_row, source_col, np.nan)
            result[delta_col] = pd.to_numeric(result[source_col], errors="coerce") - target_value
    return result


def render_similarity_executive_cards(target_row: pd.Series, best_row: pd.Series, name_col: str, top_df: pd.DataFrame | None = None) -> None:
    """Executive cards for Similar Players."""
    target_name = get_display_name(target_row, name_col)
    best_name = get_display_name(best_row, name_col)
    similarity = get_numeric_value(best_row, "similarity_score_pct", np.nan)
    delta_opp = get_numeric_value(best_row, "delta_opportunity", np.nan)
    delta_risk = get_numeric_value(best_row, "delta_risk", np.nan)

    avg_similarity = None
    if top_df is not None and not top_df.empty and "similarity_score_pct" in top_df.columns:
        avg_similarity = pd.to_numeric(top_df["similarity_score_pct"], errors="coerce").mean()

    cols = st.columns(5)
    with cols[0]:
        ref_context = f"{safe_get(target_row, 'position_group', '')} · Strength {format_score(safe_get(target_row, 'league_strength_index', 'N/A'))}"
        render_metric_card_with_caption("Jugador referencia", target_name, ref_context)
    with cols[1]:
        render_metric_card_with_caption("Perfil más similar", best_name, f"Similarity: {similarity:.1f}")
    with cols[2]:
        sign = "+" if pd.notna(delta_opp) and delta_opp >= 0 else ""
        render_metric_card_with_caption("Δ Opportunity", f"{sign}{delta_opp:.1f}", V("vs jugador referencia"))
    with cols[3]:
        sign = "+" if pd.notna(delta_risk) and delta_risk >= 0 else ""
        render_metric_card_with_caption("Δ Risk", f"{sign}{delta_risk:.1f}", V("menor es mejor"))
    with cols[4]:
        avg_text = f"{avg_similarity:.1f}" if avg_similarity is not None and pd.notna(avg_similarity) else "N/A"
        render_metric_card_with_caption("Similitud media", avg_text, V("Top perfiles"))


def build_similarity_narrative(target_player: str, best_row: pd.Series, name_col: str) -> str:
    best_name = get_display_name(best_row, name_col)
    similarity = get_numeric_value(best_row, "similarity_score_pct", np.nan)
    delta_opp = get_numeric_value(best_row, "delta_opportunity", np.nan)
    delta_risk = get_numeric_value(best_row, "delta_risk", np.nan)
    delta_growth = get_numeric_value(best_row, "delta_growth", np.nan)
    delta_strength = get_numeric_value(best_row, "delta_league_strength", np.nan)

    if LANG == "EN":
        risk_text = "lower risk" if pd.notna(delta_risk) and delta_risk < 0 else "higher risk"
        opp_text = "more opportunity" if pd.notna(delta_opp) and delta_opp > 0 else "less opportunity"
        return (
            f"<b>{html.escape(best_name)}</b> is the closest profile to <b>{html.escape(str(target_player))}</b>, "
            f"with a similarity of {similarity:.1f}%. Versus the reference player, he shows {opp_text} "
            f"(Δ Opportunity {delta_opp:+.1f}), {risk_text} (Δ Risk {delta_risk:+.1f}), a Growth differential of {delta_growth:+.1f} "
            f"and a league-context differential of {delta_strength:+.1f}."
        )

    risk_text = "menor riesgo" if pd.notna(delta_risk) and delta_risk < 0 else "mayor riesgo"
    opp_text = "más oportunidad" if pd.notna(delta_opp) and delta_opp > 0 else "menos oportunidad"

    return (
        f"<b>{html.escape(best_name)}</b> es el perfil más parecido a <b>{html.escape(str(target_player))}</b>, "
        f"con una similitud del {similarity:.1f}%. Frente al jugador de referencia presenta {opp_text} "
        f"(Δ Opportunity {delta_opp:+.1f}), {risk_text} (Δ Risk {delta_risk:+.1f}), una diferencia de Growth de {delta_growth:+.1f} "
        f"y un diferencial de contexto competitivo de liga de {delta_strength:+.1f}."
    )

def render_replacement_executive_cards(target_player: str, replacement_df: pd.DataFrame, name_col: str) -> None:
    if replacement_df.empty:
        return
    best = replacement_df.iloc[0]
    best_name = get_display_name(best, name_col)
    similarity = get_numeric_value(best, "similarity_score_pct", np.nan)
    replacement = get_numeric_value(best, "replacement_score_league_adjusted", get_numeric_value(best, "replacement_score", np.nan))
    risk = get_numeric_value(best, "risk_score", np.nan)

    # If market values are available, estimate difference against selected target if present in delta column.
    saving_caption = TXT("No disponible")
    if "delta_market_value_eur" in best.index:
        delta_market = get_numeric_value(best, "delta_market_value_eur", np.nan)
        if pd.notna(delta_market):
            saving_caption = (format_money_short(-delta_market) + " " + V("de ahorro")) if delta_market < 0 else (format_money_short(delta_market) + " " + V("más caro"))

    cols = st.columns(4)
    with cols[0]:
        render_metric_card_with_caption("Mejor reemplazo", best_name, f"{V('para')} {target_player}")
    with cols[1]:
        render_metric_card_with_caption("Similitud", f"{similarity:.1f}", V("parecido deportivo"))
    with cols[2]:
        render_metric_card_with_caption("Adaptación", f"{replacement:.1f}", V("fit competitivo"))
    with cols[3]:
        render_metric_card_with_caption("Riesgo", f"{risk:.1f}", saving_caption)


def build_replacement_narrative(target_player: str, replacement_df: pd.DataFrame, name_col: str) -> str | None:
    if replacement_df.empty:
        return None
    best = replacement_df.iloc[0]
    best_name = get_display_name(best, name_col)
    similarity = get_numeric_value(best, "similarity_score_pct", np.nan)
    opportunity = get_numeric_value(best, "opportunity_score", np.nan)
    risk = get_numeric_value(best, "risk_score", np.nan)
    fit = get_numeric_value(best, "replacement_score_league_adjusted", get_numeric_value(best, "replacement_score", np.nan))
    strength = get_numeric_value(best, "league_strength_index", np.nan)

    second_sentence = ""
    if len(replacement_df) > 1:
        alt = replacement_df.iloc[1]
        alt_name = get_display_name(alt, name_col)
        alt_opp = get_numeric_value(alt, "opportunity_score", np.nan)
        alt_risk = get_numeric_value(alt, "risk_score", np.nan)
        if LANG == "EN":
            second_sentence = (
                f"<br><br><b>{html.escape(alt_name)}</b> appears as a secondary alternative, "
                f"with Opportunity {alt_opp:.1f} and Risk {alt_risk:.1f}."
            )
        else:
            second_sentence = (
                f"<br><br><b>{html.escape(alt_name)}</b> aparece como alternativa secundaria, "
                f"con Opportunity {alt_opp:.1f} y Risk {alt_risk:.1f}."
            )

    if LANG == "EN":
        return (
            f"<b>{html.escape(best_name)}</b> appears as the best potential replacement for <b>{html.escape(str(target_player))}</b> "
            f"because he combines high similarity ({similarity:.1f}), Opportunity Score {opportunity:.1f}, Risk Score {risk:.1f} "
            f"and contextual replacement fit {fit:.1f}. His League Strength Index is {strength:.1f}; the contextual adjustment is interpreted as adaptation risk, not as a substitute for the original Opportunity Score."
            f"{second_sentence}"
        )

    return (
        f"<b>{html.escape(best_name)}</b> aparece como el mejor sustituto potencial para <b>{html.escape(str(target_player))}</b> "
        f"por combinar similitud elevada ({similarity:.1f}), Opportunity Score {opportunity:.1f}, Risk Score {risk:.1f} "
        f"y Fit contextual de sustitución {fit:.1f}. Su League Strength Index es {strength:.1f}; el ajuste contextual se interpreta como riesgo de adaptación, no como sustituto del Opportunity Score original."
        f"{second_sentence}"
    )

def render_shortlist_comparison_table(shortlist_df: pd.DataFrame) -> None:
    """Executive candidate decision table."""
    st.subheader("📋 " + ("Tablero de reclutamiento" if LANG == "ES" else "Recruitment Board"))
    st.caption(TXT("Comparativa ejecutiva de candidatos filtrados. El CSV conserva las variables auxiliares para auditoría metodológica."))

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info("No hay columna de nombre disponible para construir la tabla comparativa.")
        return

    comparison_source = add_comparison_percentiles(add_executive_decision_features(shortlist_df))
    comparison_source = comparison_source.sort_values("executive_decision_score_v2", ascending=False)

    options = comparison_source[name_col].astype(str).drop_duplicates().tolist()
    default_options = options[: min(5, len(options))]

    selected_players = st.multiselect(
        TXT("Selecciona candidatos para comparar"),
        options,
        default=default_options,
        max_selections=8,
        key="candidate_decision_table_selector",
    )

    if not selected_players:
        st.info(TXT("Selecciona al menos un jugador para construir la tabla comparativa."))
        return

    comparison_df = comparison_source[comparison_source[name_col].astype(str).isin(selected_players)].copy()
    comparison_df = comparison_df.drop_duplicates(subset=[name_col])

    default_sort_options = [
        c for c in [
            "executive_decision_score_v2",
            "future_asset_score",
            "asset_roi_3y_pct",
            "risk_adjusted_opportunity_league",
            "risk_score",
            "projected_market_value_3y_eur",
        ] if c in comparison_df.columns
    ]
    sort_col = st.selectbox(
        T("sort_by"),
        default_sort_options,
        key="candidate_decision_sort_col",
        format_func=sort_label,
        help="ES: el orden controla la prioridad visual de candidatos. EN: sorting controls the displayed recruitment priority.",
    )
    ascending = sort_col == "risk_score"
    with st.expander(T("how_filters"), expanded=False):
        if LANG == "EN":
            st.markdown("""
        - **Decision Score:** final executive decision ranking.
        - **Future Asset:** attractiveness as a three-year sporting asset.
        - **ROI 3Y:** relative investment efficiency.
        - **Context Fit:** opportunity adjusted by competitive context and risk.
        - **Risk Score:** estimated uncertainty; lower is better.
        - **Projected 3Y Value:** absolute economic potential, not necessarily better efficiency.
        """)
        else:
            st.markdown("""
        - **Decision Score:** ranking final de decisión ejecutiva.
        - **Future Asset:** atractivo como activo deportivo a tres años.
        - **ROI 3Y:** eficiencia relativa de inversión.
        - **Context Fit:** oportunidad ajustada por contexto competitivo y riesgo.
        - **Risk Score:** incertidumbre estimada; menor es mejor.
        - **Valor proyectado 3Y:** potencial económico absoluto, no necesariamente mejor eficiencia.
        """)
    comparison_df = comparison_df.sort_values(sort_col, ascending=ascending)

    summary = build_candidate_executive_summary(comparison_df, name_col)
    if summary:
        st.markdown(
            f"""
            <div class="radar-info-box">
                <b>Executive Summary</b><br><br>
                {summary}
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_decision_funnel_cards(comparison_df)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    render_candidate_decision_cards(comparison_df, name_col)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown(build_comparison_html_table(comparison_df), unsafe_allow_html=True)

    narrative = build_candidate_comparison_narrative(comparison_df, name_col)
    if narrative:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="radar-info-box">
                <b>{html.escape(TXT("Lectura ejecutiva"))}</b><br><br>
                {narrative}
            </div>
            """,
            unsafe_allow_html=True,
        )

    csv_columns = [col for col in COMPARISON_CSV_COLUMNS if col in comparison_df.columns]
    csv = comparison_df[csv_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        TXT("Descargar comparación CSV"),
        data=csv,
        file_name="candidate_decision_table.csv",
        mime="text/csv",
        key="download_candidate_decision_table",
    )


def get_similarity_feature_columns(df: pd.DataFrame) -> list[str]:
    """Select robust numeric features for player similarity without training new models."""
    return [
        col
        for col in COMPARISON_FEATURE_PRIORITY
        if col in df.columns and pd.to_numeric(df[col], errors="coerce").notna().sum() >= 3
    ]


def calculate_similarity_table(
    df: pd.DataFrame,
    target_player: str,
    name_col: str,
    restrict_same_position: bool = True,
) -> pd.DataFrame:
    """Compute cosine similarity between a target player and comparable candidates."""
    if df.empty or name_col not in df.columns:
        return pd.DataFrame()

    source = df.dropna(subset=[name_col]).copy()
    source = source.drop_duplicates(subset=[name_col])
    target_rows = source[source[name_col].astype(str) == str(target_player)]
    if target_rows.empty:
        return pd.DataFrame()

    target_row = target_rows.iloc[0]
    target_position = normalize_position_group(safe_get(target_row, "position_group", "UNK"))

    if restrict_same_position and "position_group" in source.columns:
        source = source[source["position_group"].apply(normalize_position_group) == target_position].copy()

    feature_cols = get_similarity_feature_columns(source)
    if len(feature_cols) < 3:
        return pd.DataFrame()

    matrix = source[feature_cols].apply(pd.to_numeric, errors="coerce")
    matrix = matrix.fillna(matrix.median(numeric_only=True))
    std = matrix.std(ddof=0).replace(0, 1)
    scaled = (matrix - matrix.mean()) / std
    scaled = scaled.fillna(0)

    target_idx = source[source[name_col].astype(str) == str(target_player)].index
    if target_idx.empty:
        return pd.DataFrame()

    target_vector = scaled.loc[target_idx[0]].to_numpy(dtype=float)
    candidate_matrix = scaled.to_numpy(dtype=float)
    target_norm = np.linalg.norm(target_vector)
    candidate_norms = np.linalg.norm(candidate_matrix, axis=1)
    denominator = candidate_norms * target_norm
    denominator = np.where(denominator == 0, np.nan, denominator)
    cosine_values = np.dot(candidate_matrix, target_vector) / denominator

    result = source.copy()
    result["similarity_score"] = np.nan_to_num(cosine_values, nan=0.0)
    result["similarity_score_pct"] = ((result["similarity_score"] + 1) / 2 * 100).clip(0, 100)
    result = result[result[name_col].astype(str) != str(target_player)].copy()
    result["similarity_rank"] = result["similarity_score_pct"].rank(ascending=False, method="first").astype(int)
    result["similarity_features_used"] = ", ".join(feature_cols)

    return result.sort_values("similarity_score_pct", ascending=False)


def render_similarity_engine(shortlist_df: pd.DataFrame) -> None:
    """Similarity Engine with executive interpretation."""
    st.subheader("🧬 " + ("Jugadores similares" if LANG == "ES" else "Similar Players"))
    st.caption(TXT("Identifica perfiles comparables al jugador de referencia y resume los principales trade-offs deportivos, económicos y de riesgo."))

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info(TXT("No hay columna de nombre disponible para calcular similitud."))
        return

    selector_df = enrich_scouting_context_features(shortlist_df.dropna(subset=[name_col]).copy())
    if "opportunity_score" in selector_df.columns:
        selector_df = selector_df.sort_values("opportunity_score", ascending=False)

    options = selector_df[name_col].astype(str).drop_duplicates().tolist()
    if not options:
        st.info(TXT("No hay jugadores disponibles para el motor de similitud."))
        return

    controls = st.columns([1.4, 0.8, 0.8])
    with controls[0]:
        target_player = st.selectbox(TXT("Jugador de referencia"), options, key="sprint11_similarity_target")
    with controls[1]:
        restrict_same_position = st.checkbox(UI("Misma posición"), value=True, key="sprint11_similarity_same_position")
    with controls[2]:
        top_n = st.slider("Top N", 5, 20, 10, key="sprint11_similarity_top_n")

    target_rows = selector_df[selector_df[name_col].astype(str) == str(target_player)]
    if target_rows.empty:
        st.info(TXT("No se encuentra el jugador de referencia seleccionado."))
        return
    target_row = target_rows.iloc[0]
    render_player_profile_header(target_row, name_col, "Reference player")

    similarity_df = calculate_similarity_table(
        df=selector_df,
        target_player=target_player,
        name_col=name_col,
        restrict_same_position=restrict_same_position,
    )

    if similarity_df.empty:
        st.info(TXT("No hay suficientes variables numéricas para calcular similitud de forma robusta."))
        return

    similarity_df = add_similarity_deltas(similarity_df, target_row)
    best = similarity_df.iloc[0]
    render_similarity_executive_cards(target_row, best, name_col, similarity_df.head(top_n))
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # Executive compact view: keep only decision-relevant fields on screen.
    # Full variables remain available in the underlying dataframe for audit/export if needed.
    similarity_view = similarity_df.head(top_n).copy()
    if "projected_market_value_3y_eur" in similarity_view.columns:
        similarity_view["projected_value_3y_display"] = similarity_view["projected_market_value_3y_eur"].apply(format_money_short)
    if "delta_projected_market_value_3y_eur" in similarity_view.columns:
        similarity_view["delta_projected_value_3y_display"] = similarity_view["delta_projected_market_value_3y_eur"].apply(
            lambda value: format_signed_money_short(value)
        )
    if "delta_market_value_eur" in similarity_view.columns:
        similarity_view["delta_market_value_display"] = similarity_view["delta_market_value_eur"].apply(
            lambda value: format_signed_money_short(value)
        )

    display_cols = [
        name_col,
        "club",
        "league",
        "league_quality_tier",
        "position_group",
        "similarity_score_pct",
        "delta_opportunity",
        "delta_risk",
        "delta_growth",
        "delta_league_strength",
        "projected_value_3y_display",
        "asset_roi_3y_pct",
        "future_asset_score",
        "opportunity_score",
        "risk_score",
    ]
    display_cols = [col for col in display_cols if col in similarity_view.columns]

    st.dataframe(
        localize_display_df(similarity_view)[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            name_col: st.column_config.TextColumn("Player" if LANG == "EN" else "Jugador"),
            "club": st.column_config.TextColumn("Club"),
            "league": st.column_config.TextColumn(T("league")),
            "league_quality_tier": st.column_config.TextColumn("League tier" if LANG == "EN" else "Tier liga"),
            "position_group": st.column_config.TextColumn(T("position")),
            "similarity_score_pct": st.column_config.ProgressColumn("Similarity", min_value=0, max_value=100, format="%.1f"),
            "delta_opportunity": st.column_config.NumberColumn("Δ Opp.", format="%+.1f"),
            "delta_risk": st.column_config.NumberColumn("Δ Risk", format="%+.1f"),
            "delta_growth": st.column_config.NumberColumn("Δ Growth", format="%+.1f"),
            "delta_league_strength": st.column_config.NumberColumn("Δ Strength", format="%+.1f"),
            "projected_value_3y_display": st.column_config.TextColumn("3Y Value" if LANG == "EN" else "Valor 3Y"),
            "asset_roi_3y_pct": st.column_config.NumberColumn("ROI 3Y", format="%.0f%%"),
            "future_asset_score": st.column_config.ProgressColumn("Future Asset", min_value=0, max_value=100, format="%.1f"),
            "opportunity_score": st.column_config.ProgressColumn("Opportunity", min_value=0, max_value=100, format="%.1f"),
            "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f"),
        },
    )

    narrative = build_similarity_narrative(target_player, best, name_col)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Lectura de similitud"))}</b><br><br>
            {narrative}
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_similarity = similarity_df.head(top_n).copy()
    avg_similarity = pd.to_numeric(top_similarity.get("similarity_score_pct", np.nan), errors="coerce").mean()
    avg_market_value = pd.to_numeric(top_similarity.get("market_value_eur", np.nan), errors="coerce").mean()
    stronger_context_count = int((pd.to_numeric(top_similarity.get("delta_league_strength", 0), errors="coerce") > 0).sum())
    similarity_summary = (
        f"The average similarity of the Top {len(top_similarity)} is <b>{avg_similarity:.1f}</b>. "
        f"<b>{stronger_context_count}</b> profiles come from a stronger competitive context than the reference player. "
        f"The average market value of similar profiles is <b>{html.escape(format_money_short(avg_market_value))}</b>."
        if LANG == "EN"
        else
        f"La similitud media del Top {len(top_similarity)} es <b>{avg_similarity:.1f}</b>. "
        f"<b>{stronger_context_count}</b> perfiles proceden de un contexto competitivo superior al jugador de referencia. "
        f"El valor de mercado medio de los perfiles similares es <b>{html.escape(format_money_short(avg_market_value))}</b>."
    )
    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Similarity Insight"))}</b><br><br>
            {similarity_summary}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(TXT("Variables utilizadas") + ": " + str(similarity_df["similarity_features_used"].iloc[0]))

def build_replacement_candidates(similarity_df: pd.DataFrame) -> pd.DataFrame:
    """Combine similarity, opportunity and risk into a replacement score."""
    if similarity_df.empty:
        return similarity_df

    result = add_comparison_percentiles(similarity_df).copy()
    opportunity = pd.to_numeric(result.get("opportunity_percentile", 50), errors="coerce").fillna(50)
    risk_percentile = pd.to_numeric(result.get("risk_percentile", 50), errors="coerce").fillna(50)
    similarity = pd.to_numeric(result.get("similarity_score_pct", 0), errors="coerce").fillna(0)

    result["risk_attractiveness"] = 100 - risk_percentile
    asset_score = pd.to_numeric(result.get("future_asset_score", opportunity), errors="coerce").fillna(opportunity)
    result["replacement_score"] = (0.42 * similarity + 0.25 * opportunity + 0.20 * result["risk_attractiveness"] + 0.13 * asset_score).clip(0, 100)

    # Adaptation risk is calculated against the reference player's competitive
    # context. A candidate coming from a materially weaker league than the
    # reference carries higher external-validity risk. Candidates from equal or
    # stronger contexts are not penalised.
    if "delta_league_strength" in result.columns:
        result["adaptation_risk_score"] = np.maximum(
            0, -pd.to_numeric(result["delta_league_strength"], errors="coerce").fillna(0)
        ).clip(0, 30)
    else:
        result["adaptation_risk_score"] = 0.0

    result["adaptation_risk_label"] = result["adaptation_risk_score"].apply(classify_adaptation_risk)
    result["replacement_context_fit"] = (
        result["replacement_score"] - 0.35 * result["adaptation_risk_score"]
    ).clip(0, 100)

    # Backwards-compatible alias used by existing cards/config.
    result["replacement_score_league_adjusted"] = result["replacement_context_fit"]
    sort_col = "replacement_context_fit"
    result["replacement_rank"] = result[sort_col].rank(ascending=False, method="first").astype(int)
    return result.sort_values(sort_col, ascending=False)


def render_replacement_analysis(shortlist_df: pd.DataFrame) -> None:
    """Potential replacements based on similarity and risk-adjusted opportunity."""
    st.subheader("🔁 " + ("Buscador de reemplazos" if LANG == "ES" else "Replacement Finder"))
    st.caption(TXT("Identificación automática de reemplazos según perfil deportivo, contexto competitivo, riesgo y potencial de activo."))

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info(TXT("No hay columna de nombre disponible para analizar sustitutos."))
        return

    selector_df = enrich_scouting_context_features(shortlist_df.dropna(subset=[name_col]).copy())
    if "opportunity_score" in selector_df.columns:
        selector_df = selector_df.sort_values("opportunity_score", ascending=False)

    options = selector_df[name_col].astype(str).drop_duplicates().tolist()
    controls = st.columns([1.4, 0.8])
    with controls[0]:
        target_player = st.selectbox(TXT("Jugador a sustituir / comparar"), options, key="sprint11_replacement_target")
    with controls[1]:
        top_n = st.slider(TXT("Número de sustitutos"), 5, 20, 10, key="sprint11_replacement_top_n")

    target_rows = selector_df[selector_df[name_col].astype(str) == str(target_player)]
    if target_rows.empty:
        st.info(TXT("No se encuentra el jugador seleccionado."))
        return
    target_row = target_rows.iloc[0]
    render_player_profile_header(target_row, name_col, "Reference player")

    similarity_df = calculate_similarity_table(
        df=selector_df,
        target_player=target_player,
        name_col=name_col,
        restrict_same_position=True,
    )
    similarity_df = add_similarity_deltas(similarity_df, target_row)
    replacement_df = build_replacement_candidates(similarity_df)

    if replacement_df.empty:
        st.info(TXT("No hay suficientes candidatos comparables para construir la lista de sustitutos."))
        return

    replacement_df["replacement_fit"] = replacement_df.apply(classify_replacement_fit, axis=1)
    render_replacement_executive_cards(target_player, replacement_df, name_col)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # Executive compact view for dashboard consumption. Full replacement_df is kept for CSV export.
    replacement_view = replacement_df.head(top_n).copy()
    if "projected_market_value_3y_eur" in replacement_view.columns:
        replacement_view["projected_value_3y_display"] = replacement_view["projected_market_value_3y_eur"].apply(format_money_short)
    if "asset_upside_3y_eur" in replacement_view.columns:
        replacement_view["asset_upside_3y_display"] = replacement_view["asset_upside_3y_eur"].apply(format_money_short)
    if "delta_market_value_eur" in replacement_view.columns:
        replacement_view["delta_market_value_display"] = replacement_view["delta_market_value_eur"].apply(
            lambda value: format_signed_money_short(value)
        )

    display_cols = [
        "replacement_rank",
        name_col,
        "club",
        "league",
        "league_quality_tier",
        "position_group",
        "replacement_context_fit",
        "similarity_score_pct",
        "adaptation_risk_label",
        "opportunity_score",
        "risk_score",
        "future_asset_score",
        "asset_roi_3y_pct",
        "projected_value_3y_display",
        "asset_upside_3y_display",
        "replacement_fit",
    ]
    display_cols = [col for col in display_cols if col in replacement_view.columns]

    st.dataframe(
        localize_display_df(replacement_view)[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "replacement_rank": st.column_config.NumberColumn("Rank", format="%d"),
            name_col: st.column_config.TextColumn("Player" if LANG == "EN" else "Jugador"),
            "club": st.column_config.TextColumn("Club"),
            "league": st.column_config.TextColumn(T("league")),
            "league_quality_tier": st.column_config.TextColumn("League tier" if LANG == "EN" else "Tier liga"),
            "position_group": st.column_config.TextColumn(T("position")),
            "replacement_context_fit": st.column_config.ProgressColumn("Context fit" if LANG == "EN" else "Fit contexto", min_value=0, max_value=100, format="%.1f"),
            "similarity_score_pct": st.column_config.ProgressColumn("Similarity", min_value=0, max_value=100, format="%.1f"),
            "adaptation_risk_label": st.column_config.TextColumn("Adaptation" if LANG == "EN" else "Adaptación"),
            "opportunity_score": st.column_config.ProgressColumn("Opportunity", min_value=0, max_value=100, format="%.1f"),
            "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f"),
            "asset_roi_3y_pct": st.column_config.NumberColumn("ROI 3Y", format="%.0f%%"),
            "future_asset_score": st.column_config.ProgressColumn("Future Asset", min_value=0, max_value=100, format="%.1f"),
            "projected_value_3y_display": st.column_config.TextColumn("3Y Value" if LANG == "EN" else "Valor 3Y"),
            "asset_upside_3y_display": st.column_config.TextColumn("3Y Upside" if LANG == "EN" else "Upside 3Y"),
            "replacement_fit": st.column_config.TextColumn("Replacement fit" if LANG == "EN" else "Fit de sustitución"),
        },
    )

    narrative = build_replacement_narrative(target_player, replacement_df, name_col)
    if narrative:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="radar-info-box">
                <b>{html.escape(TXT("Replacement Insight"))}</b><br><br>
                {narrative}
            </div>
            """,
            unsafe_allow_html=True,
        )

    csv = replacement_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        TXT("Descargar sustitutos CSV"),
        data=csv,
        file_name="replacement_candidates.csv",
        mime="text/csv",
        key="sprint11_download_replacement_candidates",
    )


def classify_decision_stage(score: object) -> str:
    """Translate Executive Decision Score into a recruitment funnel stage."""
    value = pd.to_numeric(pd.Series([score]), errors="coerce").iloc[0]
    if pd.isna(value):
        return "Monitor"
    if value >= 80:
        return "Elite Target"
    if value >= 70:
        return "Shortlist"
    if value >= 60:
        return "Watchlist"
    return "Monitor"


def classify_executive_action(row: pd.Series) -> str:
    """Translate Executive Decision Score into the next operational action."""
    score = get_numeric_value(row, "executive_decision_score_v2", get_numeric_value(row, "executive_decision_score", 0))
    risk = get_numeric_value(row, "risk_score", 100)
    confidence = get_numeric_value(row, "confidence_score", 0)
    adaptation = get_numeric_value(row, "adaptation_risk_score", 0)

    if score >= 82 and risk <= 55 and confidence >= 70 and adaptation <= 8:
        return "Iniciar contacto"
    if score >= 76 and (risk > 55 or adaptation > 8):
        return "Due diligence"
    if score >= 68:
        return "Vídeo scouting"
    if score >= 58:
        return "Seguimiento activo"
    return "Monitorización pasiva"


def classify_executive_priority_v2(row: pd.Series) -> str:
    """Priority label for the Executive Decision Engine."""
    stage = str(safe_get(row, "decision_stage", "Monitor"))
    if stage == "Elite Target":
        return "Prioridad máxima"
    if stage == "Shortlist":
        return "Prioridad alta"
    if stage == "Watchlist":
        return "Prioridad media"
    return "Monitorizar"


def build_decision_drivers(row: pd.Series) -> str:
    """Generate compact automatic decision drivers for executive tables."""
    drivers = []
    roi = get_numeric_value(row, "asset_roi_3y_pct", np.nan)
    future_asset = get_numeric_value(row, "future_asset_score", np.nan)
    projected_value = get_numeric_value(row, "projected_value_score", np.nan)
    opportunity_context = get_numeric_value(row, "risk_adjusted_opportunity_league", np.nan)
    confidence = get_numeric_value(row, "confidence_score", np.nan)
    risk = get_numeric_value(row, "risk_score", np.nan)
    adaptation = get_numeric_value(row, "adaptation_risk_score", 0)
    replacement_fit = get_numeric_value(row, "replacement_fit_light", np.nan)

    positive = []
    caution = []

    if pd.notna(roi) and roi >= 200:
        positive.append("ROI alto")
    if pd.notna(future_asset) and future_asset >= 70:
        positive.append("activo atractivo")
    if pd.notna(projected_value) and projected_value >= 75:
        positive.append("valor futuro elevado")
    if pd.notna(opportunity_context) and opportunity_context >= 60:
        positive.append("context fit sólido")
    if pd.notna(confidence) and confidence >= 80:
        positive.append("confianza alta")
    if pd.notna(replacement_fit) and replacement_fit >= 75:
        positive.append("fit de plantilla")

    if pd.notna(risk) and risk >= 70:
        caution.append("Riesgo elevado")
    elif pd.notna(risk) and risk <= 45:
        positive.append("riesgo bajo")
    if pd.notna(adaptation) and adaptation >= 9:
        caution.append("adaptación incierta")
    if pd.notna(confidence) and confidence < 65:
        caution.append("confianza limitada")

    drivers = positive[:2]
    if caution:
        drivers.append(caution[0])
    if not drivers:
        drivers = ["perfil equilibrado"]
    return " + ".join(drivers)


def add_light_replacement_fit(df: pd.DataFrame) -> pd.Series:
    """Approximate replacement/squad-fit potential for global executive ranking.

    This is intentionally lightweight: the target-specific Replacement Finder remains
    the source for detailed substitute analysis. Here the score prevents the global
    decision engine from ignoring profile robustness when no target player is selected.
    """
    if df.empty:
        return pd.Series(dtype=float, index=df.index)

    age = pd.to_numeric(df.get("age", 21), errors="coerce").fillna(21)
    confidence = pd.to_numeric(df.get("confidence_score", 65), errors="coerce").fillna(65).clip(0, 100)
    minutes = pd.to_numeric(df.get("minutes_played", 0), errors="coerce").fillna(0)
    strength = pd.to_numeric(df.get("league_strength_index", DEFAULT_LEAGUE_STRENGTH), errors="coerce").fillna(DEFAULT_LEAGUE_STRENGTH).clip(70, 100)

    age_fit = np.select(
        [age <= 19.5, age <= 21.5, age <= 23.5, age > 23.5],
        [92, 88, 78, 62],
        default=75,
    )
    minutes_fit = (minutes / 2200 * 100).clip(0, 100)
    context_fit = strength

    return pd.Series(
        (0.35 * confidence + 0.30 * age_fit + 0.20 * minutes_fit + 0.15 * context_fit).clip(0, 100).round(1),
        index=df.index,
    )


def add_executive_decision_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add final executive decision features used by rankings, tables and pipeline.

    These variables are designed as decision-support outputs and will be natural
    inputs for a later Portfolio Optimization layer: score, stage, action and drivers.
    """
    if df.empty:
        return df.copy()

    result = enrich_scouting_context_features(df).copy()

    opportunity = pd.to_numeric(result.get("opportunity_score", 50), errors="coerce").fillna(50).clip(0, 100)
    context = pd.to_numeric(
        result.get("risk_adjusted_opportunity_league", result.get("risk_adjusted_opportunity_score", opportunity)),
        errors="coerce",
    ).fillna(opportunity).clip(0, 100)
    future_asset = pd.to_numeric(result.get("future_asset_score", opportunity), errors="coerce").fillna(opportunity).clip(0, 100)
    roi = pd.to_numeric(result.get("roi_score", 50), errors="coerce").fillna(50).clip(0, 100)
    risk = pd.to_numeric(result.get("risk_score", 50), errors="coerce").fillna(50).clip(0, 100)
    confidence = pd.to_numeric(result.get("confidence_score", 65), errors="coerce").fillna(65).clip(0, 100)

    if "replacement_context_fit" in result.columns:
        replacement_fit = pd.to_numeric(result["replacement_context_fit"], errors="coerce").fillna(65).clip(0, 100)
    elif "replacement_score_league_adjusted" in result.columns:
        replacement_fit = pd.to_numeric(result["replacement_score_league_adjusted"], errors="coerce").fillna(65).clip(0, 100)
    else:
        replacement_fit = add_light_replacement_fit(result)
        result["replacement_fit_light"] = replacement_fit

    adaptation_risk = pd.to_numeric(
        result.get("adaptation_risk_score", pd.Series(0, index=result.index)),
        errors="coerce",
    ).fillna(0).clip(0, 30)
    adaptation_score = (100 - adaptation_risk * (100 / 30)).clip(0, 100)

    result["executive_context_opportunity_component"] = context.round(1)
    result["executive_future_asset_component"] = future_asset.round(1)
    result["executive_roi_component"] = roi.round(1)
    result["executive_replacement_fit_component"] = replacement_fit.round(1)
    result["executive_adaptation_component"] = adaptation_score.round(1)
    result["executive_confidence_component"] = confidence.round(1)
    result["executive_risk_component"] = (100 - risk).round(1)

    result["executive_decision_score_v2"] = (
        0.30 * future_asset
        + 0.18 * context
        + 0.15 * confidence
        + 0.14 * roi
        + 0.11 * (100 - risk)
        + 0.07 * replacement_fit
        + 0.05 * adaptation_score
    ).clip(0, 100).round(1)

    result["executive_decision_score"] = result["executive_decision_score_v2"]
    result["decision_stage"] = result["executive_decision_score_v2"].apply(classify_decision_stage)
    result["recommended_action"] = result.apply(classify_executive_action, axis=1)
    result["executive_priority"] = result.apply(classify_executive_priority_v2, axis=1)
    result["decision_drivers"] = result.apply(build_decision_drivers, axis=1)
    return result


def build_executive_recommendation_rationale(row: pd.Series) -> str:
    """Generate an executive rationale from score components."""
    player = html.escape(str(safe_get(row, "player_display_name", get_player_name(row))))
    score = get_numeric_value(row, "executive_decision_score_v2", get_numeric_value(row, "executive_decision_score", np.nan))
    future_asset = get_numeric_value(row, "future_asset_score", np.nan)
    roi_pct = get_numeric_value(row, "asset_roi_3y_pct", np.nan)
    risk = get_numeric_value(row, "risk_score", np.nan)
    confidence = get_numeric_value(row, "confidence_score", np.nan)
    context = get_numeric_value(row, "risk_adjusted_opportunity_league", get_numeric_value(row, "risk_adjusted_opportunity_score", np.nan))
    adaptation = get_numeric_value(row, "adaptation_risk_score", 0)
    stage = html.escape(str(safe_get(row, "decision_stage", "Shortlist")))
    raw_action = str(safe_get(row, "recommended_action", "Vídeo scouting"))
    action = html.escape(action_display_name(raw_action))
    drivers = html.escape(driver_display_name(str(safe_get(row, "decision_drivers", "perfil equilibrado"))))

    if LANG == "EN":
        reasons = [
            f"<b>{player}</b> is the best global decision in the panel with an <b>Executive Decision Score</b> of {score:.1f}. The assigned stage is <b>{stage}</b> and the recommended next action is <b>{action.lower()}</b>.",
            f"The main drivers are: <b>{drivers}</b>.",
            f"The recommendation combines asset potential ({future_asset:.1f}), estimated 3Y ROI ({roi_pct:.0f}%), context fit ({context:.1f}), risk ({risk:.1f}) and analytical confidence ({confidence:.1f}).",
        ]
        if pd.notna(adaptation) and adaptation > 0:
            reasons.append(f"Competitive adaptation risk is included as a contextual penalty ({adaptation:.1f}), preventing the ranking from relying only on economic upside.")
        else:
            reasons.append("No relevant competitive-adaptation penalty is detected in the aggregate recommendation.")
        reasons.append("The output organizes the sporting department workflow: it narrows the search universe, but still requires qualitative validation, tactical fit, contractual availability and economic due diligence before progressing.")
        return "<br><br>".join(reasons)

    reasons = [
        f"<b>{player}</b> es la mejor decisión global del panel con un <b>Executive Decision Score</b> de {score:.1f}. La fase asignada es <b>{stage}</b> y la siguiente acción recomendada es <b>{action.lower()}</b>.",
        f"Los drivers principales son: <b>{drivers}</b>.",
        f"La recomendación combina potencial de activo ({future_asset:.1f}), ROI 3Y estimado ({roi_pct:.0f}%), context fit ({context:.1f}), riesgo ({risk:.1f}) y confianza analítica ({confidence:.1f}).",
    ]

    if pd.notna(adaptation) and adaptation > 0:
        reasons.append(
            f"El riesgo de adaptación competitivo se incorpora como penalización contextual ({adaptation:.1f}), evitando que el ranking dependa solo del upside económico."
        )
    else:
        reasons.append(
            "No se detecta una penalización relevante por adaptación competitiva en la recomendación agregada."
        )

    reasons.append(
        "La salida ordena el trabajo del área deportiva: reduce el universo de búsqueda, pero requiere contraste cualitativo, encaje táctico, disponibilidad contractual y validación económica antes de avanzar."
    )
    return "<br><br>".join(reasons)


def get_executive_decision_table(shortlist_df: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    """Build the final recruitment ranking for a sporting director."""
    if shortlist_df.empty:
        return pd.DataFrame()

    df = add_executive_decision_features(shortlist_df)
    name_col = get_player_name_column(df)
    if name_col is None:
        return pd.DataFrame()

    df = df.sort_values("executive_decision_score_v2", ascending=False).copy()
    if top_n is not None:
        df = df.head(top_n).copy()
    df["executive_rank"] = range(1, len(df) + 1)
    df["player_display_name"] = df[name_col].astype(str)
    return df


def render_executive_recommendation_engine(shortlist_df: pd.DataFrame) -> None:
    """Executive product layer: compact SaaS-style decision overview and recruitment ranking."""
    decision_df = get_executive_decision_table(shortlist_df, top_n=8)
    if decision_df.empty:
        return

    best = decision_df.iloc[0]
    best_name = str(safe_get(best, "player_display_name", get_player_name(best)))
    decision_score = get_numeric_value(best, "executive_decision_score_v2", np.nan)
    future_asset = get_numeric_value(best, "future_asset_score", np.nan)
    roi_pct = get_numeric_value(best, "asset_roi_3y_pct", np.nan)
    projected_value = safe_get(best, "projected_market_value_3y_eur", np.nan)
    risk = get_numeric_value(best, "risk_score", np.nan)
    confidence = get_numeric_value(best, "confidence_score", np.nan)
    opportunity = get_numeric_value(best, "opportunity_score", np.nan)
    context = get_numeric_value(best, "risk_adjusted_opportunity_league", get_numeric_value(best, "risk_adjusted_opportunity_score", np.nan))
    action = str(safe_get(best, "recommended_action", "Vídeo scouting"))
    priority = str(safe_get(best, "executive_priority", "Prioridad alta"))
    stage = str(safe_get(best, "decision_stage", "Shortlist"))
    drivers = str(safe_get(best, "decision_drivers", "perfil equilibrado"))
    rationale = build_executive_recommendation_rationale(best)

    badge_class = "exec-badge-blue"
    if action in {"Iniciar contacto", "Due diligence"}:
        badge_class = "exec-badge-red"
    elif action in {"Vídeo scouting", "Seguimiento activo"}:
        badge_class = "exec-badge-yellow"
    if risk <= 40 and decision_score >= 75:
        badge_class = "exec-badge-green"

    driver_chips = "".join(
        f"<span class='driver-chip'>{html.escape(part.strip())}</span>"
        for part in driver_display_name(drivers).split("+")
        if part.strip()
    )

    st.subheader("🏆 " + TXT("Executive Overview"))
    st.caption(TXT("Resumen de decisión actualizado con los filtros activos."))
    st.markdown(
        f"""
        <div class="exec-overview-grid">
            <div class="exec-player-card">
                <div class="exec-score-sub">{html.escape(TXT("Best global decision"))}</div>
                <div class="exec-player-name">{html.escape(best_name)}</div>
                <div class="exec-player-meta">
                    {html.escape(str(safe_get(best, 'position_group', 'N/A')))} · {html.escape(str(safe_get(best, 'club', 'N/A')))} · {html.escape(league_display_name(safe_get(best, 'league', 'N/A')))}<br>
                    {format_score(safe_get(best, 'age', np.nan))} {html.escape(TXT('años'))} · {html.escape(TXT('Valor actual'))} {html.escape(format_money_short(safe_get(best, 'market_value_eur', np.nan)))} · {html.escape(TXT('Valor 3Y'))} {html.escape(format_money_short(projected_value))}
                </div>
                <span class="exec-badge {badge_class}">{html.escape(action_display_name(action))}</span>
                <span class="exec-badge exec-badge-blue">{html.escape(stage)}</span>
            </div>
            <div class="exec-score-card">
                <div class="exec-score-sub">Executive Decision Score</div>
                <div class="exec-score-main">{decision_score:.1f}<span style="font-size:1rem;color:#64748b;"> /100</span></div>
                <div class="scouting-score-bar"></div>
                <div class="exec-player-meta"><b>{html.escape(V(priority))}</b></div>
            </div>
            <div class="exec-kpi-card">
                <div class="exec-kpi-grid">
                    <div><div class="exec-kpi-label">Future Asset</div><div class="exec-kpi-value">{future_asset:.1f}</div></div>
                    <div><div class="exec-kpi-label">ROI 3Y</div><div class="exec-kpi-value">{roi_pct:.0f}%</div></div>
                    <div><div class="exec-kpi-label">Opportunity</div><div class="exec-kpi-value">{opportunity:.1f}</div></div>
                    <div><div class="exec-kpi-label">Context Fit</div><div class="exec-kpi-value">{context:.1f}</div></div>
                    <div><div class="exec-kpi-label">Risk</div><div class="exec-kpi-value">{risk:.1f}</div></div>
                    <div><div class="exec-kpi-label">Confidence</div><div class="exec-kpi-value">{confidence:.1f}</div></div>
                </div>
            </div>
        </div>
        <div class="pro-section-card">
            <div style="font-weight:900;color:#0f172a;margin-bottom:8px;">{html.escape(TXT("Decision drivers"))}</div>
            {driver_chips}
            <div class="compact-board-note">{html.escape(TXT("Siguiente acción recomendada"))}: <b>{html.escape(action_display_name(action))}</b>. {html.escape(TXT("La decisión combina potencial de activo, ROI, context fit, riesgo y confianza analítica."))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="score-methodology-spacer"></div>', unsafe_allow_html=True)
    with st.expander(TXT("Ver explicación completa y metodología de scores"), expanded=False):
        st.markdown(rationale, unsafe_allow_html=True)
        st.markdown(
            ("**Executive formula:** Future Asset 30% · Context Fit 18% · Confidence 15% · ROI 14% · Risk 11% · Replacement Fit 7% · Adaptation Risk 5%." if LANG == "EN" else "**Fórmula ejecutiva:** Future Asset 30% · Context Fit 18% · Confidence 15% · ROI 14% · Risk 11% · Replacement Fit 7% · Adaptation Risk 5%.")
        )

    ranking_view = decision_df.copy()
    ranking_view["valor_actual"] = ranking_view["market_value_eur"].apply(format_money_short) if "market_value_eur" in ranking_view.columns else "N/A"
    ranking_view["valor_3y"] = ranking_view["projected_market_value_3y_eur"].apply(format_money_short) if "projected_market_value_3y_eur" in ranking_view.columns else "N/A"

    display_cols = [
        "executive_rank",
        "player_display_name",
        "position_group",
        "age",
        "club",
        "league",
        "valor_actual",
        "future_asset_score",
        "asset_roi_3y_pct",
        "risk_score",
        "executive_decision_score_v2",
        "recommended_action",
        "decision_drivers",
    ]
    display_cols = [c for c in display_cols if c in ranking_view.columns]

    st.subheader("📌 " + ("Tablero de reclutamiento" if LANG == "ES" else "Recruitment Board"))
    st.caption(TXT("Vista compacta para priorizar revisión. El CSV y las tablas detalladas conservan las variables auxiliares."))
    st.dataframe(
        localize_display_df(ranking_view)[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "executive_rank": st.column_config.NumberColumn("#", format="%d", width="small"),
            "player_display_name": st.column_config.TextColumn("Player" if LANG == "EN" else "Jugador"),
            "position_group": st.column_config.TextColumn("Pos.", width="small"),
            "age": st.column_config.NumberColumn("Age" if LANG == "EN" else "Edad", format="%.1f", width="small"),
            "club": st.column_config.TextColumn("Club"),
            "league": st.column_config.TextColumn(T("league")),
            "valor_actual": st.column_config.TextColumn("Value" if LANG == "EN" else "Value" if LANG == "EN" else "Valor", width="small"),
            "future_asset_score": st.column_config.ProgressColumn("Future Asset", min_value=0, max_value=100, format="%.1f"),
            "asset_roi_3y_pct": st.column_config.NumberColumn("ROI 3Y", format="%.0f%%", width="small"),
            "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f"),
            "executive_decision_score_v2": st.column_config.ProgressColumn("Decision Score", min_value=0, max_value=100, format="%.1f"),
            "recommended_action": st.column_config.TextColumn("Action" if LANG == "EN" else "Acción"),
            "decision_drivers": st.column_config.TextColumn("Main drivers" if LANG == "EN" else "Drivers principales"),
        },
    )

def render_asset_intelligence(shortlist_df: pd.DataFrame) -> None:
    """Asset-management view for projected value and ROI."""
    st.subheader("💰 " + ("Análisis de inversión" if LANG == "ES" else "Investment Analysis"))
    st.caption(TXT("Evalúa los candidatos como activos deportivos: valor actual, valor proyectado, upside, ROI y balance riesgo-retorno."))

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info("No hay columna de nombre disponible para construir Investment Analysis.")
        return

    asset_df = enrich_scouting_context_features(shortlist_df).copy()
    asset_df = asset_df.sort_values("future_asset_score", ascending=False).head(15)

    if asset_df.empty:
        st.info("No hay suficientes datos para construir la vista de activos.")
        return

    best_asset = asset_df.iloc[0]
    best_roi = asset_df.sort_values("asset_roi_3y_pct", ascending=False).iloc[0]
    best_value = asset_df.sort_values("projected_market_value_3y_eur", ascending=False).iloc[0]
    best_low_risk = asset_df.sort_values("risk_score", ascending=True).iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card_with_caption("Top Future Asset", get_display_name(best_asset, name_col), f"Score: {get_numeric_value(best_asset, 'future_asset_score', np.nan):.1f}")
    with c2:
        render_metric_card_with_caption("Best ROI", get_display_name(best_roi, name_col), f"ROI 3Y: {get_numeric_value(best_roi, 'asset_roi_3y_pct', np.nan):.0f}%")
    with c3:
        render_metric_card_with_caption("Mayor valor proyectado", get_display_name(best_value, name_col), format_money_short(safe_get(best_value, "projected_market_value_3y_eur", np.nan)))
    with c4:
        render_metric_card_with_caption("Activo menor riesgo", get_display_name(best_low_risk, name_col), f"Risk: {get_numeric_value(best_low_risk, 'risk_score', np.nan):.1f}")

    view = asset_df.copy()
    view["valor_actual"] = view["market_value_eur"].apply(format_money_short)
    view["valor_3y"] = view["projected_market_value_3y_eur"].apply(format_money_short)
    view["upside_3y"] = view["asset_upside_3y_eur"].apply(format_money_short)
    display_cols = [name_col, "club", "league", "league_quality_tier", "valor_actual", "valor_3y", "upside_3y", "asset_roi_3y_pct", "future_asset_score", "opportunity_score", "risk_score"]
    display_cols = [c for c in display_cols if c in view.columns]

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.dataframe(
        localize_display_df(view)[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            name_col: st.column_config.TextColumn("Player" if LANG == "EN" else "Jugador"),
            "club": st.column_config.TextColumn("Club"),
            "league": st.column_config.TextColumn(T("league")),
            "league_quality_tier": st.column_config.TextColumn("League tier" if LANG == "EN" else "Tier liga"),
            "valor_actual": st.column_config.TextColumn("Value" if LANG == "EN" else "Valor"),
            "valor_3y": st.column_config.TextColumn("3Y Value" if LANG == "EN" else "Valor 3Y"),
            "upside_3y": st.column_config.TextColumn("Upside 3Y"),
            "asset_roi_3y_pct": st.column_config.NumberColumn("ROI 3Y", format="%.0f%%"),
            "future_asset_score": st.column_config.ProgressColumn("Future Asset", min_value=0, max_value=100, format="%.1f"),
            "opportunity_score": st.column_config.ProgressColumn("Opportunity", min_value=0, max_value=100, format="%.1f"),
            "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f"),
        },
    )

    investment_text = (
        f"<b>{html.escape(get_display_name(best_asset, name_col))}</b> appears as the most balanced asset by Future Asset Score. "
        f"<b>{html.escape(get_display_name(best_roi, name_col))}</b> maximizes investment efficiency through 3Y ROI. "
        f"<b>{html.escape(get_display_name(best_value, name_col))}</b> carries the highest absolute projected value over three years."
        if LANG == "EN"
        else
        f"<b>{html.escape(get_display_name(best_asset, name_col))}</b> aparece como el activo más equilibrado por Future Asset Score. "
        f"<b>{html.escape(get_display_name(best_roi, name_col))}</b> maximiza eficiencia de inversión vía ROI 3Y. "
        f"<b>{html.escape(get_display_name(best_value, name_col))}</b> concentra el mayor valor proyectado absoluto a tres años."
    )
    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Investment Insight"))}</b><br><br>
            {investment_text}
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_driver_analysis(shortlist_df: pd.DataFrame) -> None:
    """Simplified model-driver view for sporting decision makers.

    This tab translates SHAP-style model explainability into scouting language:
    which factors push the recommendation up and which factors require caution.
    """
    st.subheader("🔍 " + ("Drivers del modelo" if LANG == "ES" else "Model Drivers"))
    st.caption(TXT("Factores principales que explican por qué el sistema prioriza o penaliza un jugador."))

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    name_col = get_player_name_column(shortlist_df)
    if name_col is None:
        st.info("No hay columna de nombre disponible para construir Model Drivers.")
        return

    driver_df = enrich_scouting_context_features(shortlist_df.dropna(subset=[name_col]).copy())
    decision_df = get_executive_decision_table(driver_df, top_n=min(12, len(driver_df)))

    if not decision_df.empty and "player_display_name" in decision_df.columns:
        options = decision_df["player_display_name"].astype(str).drop_duplicates().tolist()
    else:
        if "future_asset_score" in driver_df.columns:
            driver_df = driver_df.sort_values("future_asset_score", ascending=False)
        options = driver_df[name_col].astype(str).drop_duplicates().tolist()

    if not options:
        st.info(TXT("No hay jugadores disponibles para Model Drivers."))
        return

    selected_player = st.selectbox(
        TXT("Jugador a explicar"),
        options,
        index=0,
        key="driver_analysis_player",
    )

    player_rows = driver_df[driver_df[name_col].astype(str) == str(selected_player)]
    if player_rows.empty and "player_name_fbref" in driver_df.columns:
        player_rows = driver_df[driver_df["player_name_fbref"].astype(str) == str(selected_player)]

    if player_rows.empty:
        st.info(TXT("No se encuentra el jugador seleccionado."))
        return

    player_row = player_rows.iloc[0]
    render_player_profile_header(player_row, name_col, "Player profile")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card_with_caption(
            "Future Asset",
            format_score(safe_get(player_row, "future_asset_score", np.nan)),
            "potencial económico-deportivo",
        )
    with c2:
        roi_value = get_numeric_value(player_row, "asset_roi_3y_pct", np.nan)
        roi_text = f"{roi_value:.0f}%" if pd.notna(roi_value) else "N/A"
        render_metric_card_with_caption("ROI 3Y", roi_text, "eficiencia de inversión")
    with c3:
        render_metric_card_with_caption(
            "Risk Score",
            format_score(safe_get(player_row, "risk_score", np.nan)),
            "menor es mejor",
        )
    with c4:
        render_metric_card_with_caption(
            "3Y Value" if LANG == "EN" else "Valor 3Y",
            format_money_short(safe_get(player_row, "projected_market_value_3y_eur", np.nan)),
            "proyección heurística",
        )

    shap_values = make_shap_proxy(player_row)
    positive = shap_values[shap_values["impact"] > 0].sort_values("impact", ascending=False).head(4)
    negative = shap_values[shap_values["impact"] < 0].sort_values("impact").head(4)

    col_pos, col_neg = st.columns(2, gap="large")
    with col_pos:
        st.markdown("#### " + TXT("Factores que impulsan la recomendación"))
        if positive.empty:
            st.caption("No se detectan contribuciones positivas destacadas.")
        else:
            pos_view = positive.rename(columns={"feature": "Factor", "impact": "Impacto"}).copy()
            pos_view["Factor"] = pos_view["Factor"].apply(V)
            st.dataframe(
                localize_display_df(pos_view),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Factor": st.column_config.TextColumn(TXT("Factor")),
                    "Impacto": st.column_config.NumberColumn(TXT("Impacto"), format="+%.2f"),
                },
            )

    with col_neg:
        st.markdown("#### " + TXT("Factores que requieren cautela"))
        if negative.empty:
            st.caption("No se detectan contribuciones negativas destacadas.")
        else:
            neg_view = negative.rename(columns={"feature": "Factor", "impact": "Impacto"}).copy()
            neg_view["Factor"] = neg_view["Factor"].apply(V)
            st.dataframe(
                localize_display_df(neg_view),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Factor": st.column_config.TextColumn(TXT("Factor")),
                    "Impacto": st.column_config.NumberColumn(TXT("Impacto"), format="%.2f"),
                },
            )

    positive_text = ", ".join(V(x) for x in positive["feature"].astype(str).tolist()) if not positive.empty else TXT("sin factores positivos destacados")
    negative_text = ", ".join(V(x) for x in negative["feature"].astype(str).tolist()) if not negative.empty else TXT("sin limitadores relevantes")

    if LANG == "EN":
        executive_text = (
            f"<b>{html.escape(str(selected_player))}</b> is recommended mainly because of {html.escape(positive_text)}. "
            f"The main elements to validate before moving him to an advanced stage are {html.escape(negative_text)}. "
            f"{html.escape(TXT('Esta lectura resume la trazabilidad del modelo en lenguaje operativo, sin presentar SHAP como causalidad deportiva.'))}"
        )
    else:
        executive_text = (
            f"<b>{html.escape(str(selected_player))}</b> aparece recomendado principalmente por {html.escape(positive_text)}. "
            f"Los principales elementos a validar antes de elevarlo a fase avanzada son {html.escape(negative_text)}. "
            f"Esta lectura resume la trazabilidad del modelo en lenguaje operativo, sin presentar SHAP como causalidad deportiva."
        )

    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Lectura ejecutiva"))}</b><br><br>
            {executive_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recruitment_pipeline(shortlist_df: pd.DataFrame) -> None:
    """Simulated recruitment pipeline for product-level decision support.

    The dashboard does not persist workflow status yet; this view assigns an
    initial recommended stage from the executive decision score, risk and
    confidence to mimic a real recruitment board.
    """
    st.subheader("🗂️ " + TXT("Recruitment Pipeline"))
    render_sprint11_context_box(
        TXT("Objetivo"),
        TXT("convertir el ranking analítico en un flujo operativo de scouting. La fase asignada es una simulación inicial sin persistencia, pensada para priorizar revisión de vídeo, scouting en directo y due diligence.")
    )

    decision_df = get_executive_decision_table(shortlist_df, top_n=20)
    if decision_df.empty:
        st.info("Not enough data to build the recruitment pipeline." if LANG == "EN" else "No hay datos suficientes para construir el pipeline de reclutamiento.")
        return

    pipeline_df = decision_df.copy()
    action_to_stage = {
        "Iniciar contacto": "Due Diligence",
        "Due diligence": "Due Diligence",
        "Vídeo scouting": "Video Review",
        "Seguimiento activo": "Scouting",
        "Monitorización pasiva": "Monitor",
    }
    pipeline_df["pipeline_stage"] = pipeline_df.get("recommended_action", "Monitorizar").map(action_to_stage).fillna("Monitor")
    pipeline_df["next_action"] = pipeline_df["pipeline_stage"].map(
        {
            "Due Diligence": "Validar contrato, agente, salario y disponibilidad",
            "Live Scouting": "Asignar seguimiento presencial",
            "Video Review": "Revisión completa de vídeo",
            "Scouting": "Informe scout inicial",
            "Discovery": "Mantener en radar",
            "Monitor": "No priorizar de momento",
        }
    ).apply(V)

    stage_order = ["Due Diligence", "Live Scouting", "Video Review", "Scouting", "Discovery", "Monitor"]
    stage_counts = pipeline_df["pipeline_stage"].value_counts().reindex(stage_order, fill_value=0)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_metric_card_with_caption("Due Diligence", int(stage_counts["Due Diligence"]), "candidatos listos para validación")
    with k2:
        render_metric_card_with_caption("Live Scouting", int(stage_counts["Live Scouting"]), "seguimiento presencial")
    with k3:
        render_metric_card_with_caption("Video Review", int(stage_counts["Video Review"]), "prioridad de vídeo")
    with k4:
        render_metric_card_with_caption("Discovery / Monitor", int(stage_counts["Discovery"] + stage_counts["Monitor"]), "seguimiento bajo")

    view = pipeline_df.copy()
    if "market_value_eur" in view.columns:
        view["valor_actual"] = view["market_value_eur"].apply(format_money_short)
    if "projected_market_value_3y_eur" in view.columns:
        view["valor_3y"] = view["projected_market_value_3y_eur"].apply(format_money_short)

    display_cols = [
        "executive_rank",
        "player_display_name",
        "club",
        "league",
        "position_group",
        "pipeline_stage",
        "next_action",
        "executive_decision_score_v2",
        "future_asset_score",
        "asset_roi_3y_pct",
        "risk_score",
        "valor_actual",
        "valor_3y",
    ]
    display_cols = [col for col in display_cols if col in view.columns]

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.dataframe(
        localize_display_df(view)[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "executive_rank": st.column_config.NumberColumn("Rank", format="%d"),
            "player_display_name": st.column_config.TextColumn("Player" if LANG == "EN" else "Jugador"),
            "club": st.column_config.TextColumn("Club"),
            "league": st.column_config.TextColumn(T("league")),
            "position_group": st.column_config.TextColumn(T("position")),
            "pipeline_stage": st.column_config.TextColumn("Stage" if LANG == "EN" else "Fase"),
            "next_action": st.column_config.TextColumn("Next action" if LANG == "EN" else "Siguiente acción"),
            "executive_decision_score_v2": st.column_config.ProgressColumn("Decision Score", min_value=0, max_value=100, format="%.1f"),
            "future_asset_score": st.column_config.ProgressColumn("Future Asset", min_value=0, max_value=100, format="%.1f"),
            "asset_roi_3y_pct": st.column_config.NumberColumn("ROI 3Y", format="%.0f%%"),
            "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f"),
            "valor_actual": st.column_config.TextColumn("Value" if LANG == "EN" else "Valor"),
            "valor_3y": st.column_config.TextColumn("3Y Value" if LANG == "EN" else "Valor 3Y"),
        },
    )

    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>{html.escape(TXT("Nota operativa"))}</b><br><br>
            {html.escape(TXT("Esta vista no sustituye a un CRM deportivo. Funciona como prototipo de priorización: traduce el ranking analítico en una primera asignación de fases para reducir carga de revisión y ordenar el trabajo del área de scouting."))}
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_shortlist_intelligence_dashboard(shortlist_df: pd.DataFrame) -> None:
    """Unified scouting decision-support product section."""
    st.markdown(
        f"""
<div class="recruitment-compact-note">
<b>{html.escape(TXT("Executive Scouting Workspace"))}:</b> {html.escape(TXT("priorización, comparación, reemplazos, perfiles similares, inversión y drivers del modelo en un único flujo de decisión."))}
</div>
""",
        unsafe_allow_html=True,
    )

    if shortlist_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return

    shortlist_df = enrich_scouting_context_features(shortlist_df)

    render_executive_recommendation_engine(shortlist_df)
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Pipeline de reclutamiento" if LANG == "ES" else "Recruitment Pipeline",
        "Comparación de candidatos" if LANG == "ES" else "Candidate Comparison",
        "Buscador de reemplazos" if LANG == "ES" else "Replacement Finder",
        "Jugadores similares" if LANG == "ES" else "Similar Players",
        "Análisis de inversión" if LANG == "ES" else "Investment Analysis",
        "Drivers del modelo" if LANG == "ES" else "Model Drivers",
    ])

    with tab1:
        render_recruitment_pipeline(shortlist_df)
    with tab2:
        render_multi_player_radar_comparison(shortlist_df)
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        render_shortlist_comparison_table(shortlist_df)
    with tab3:
        render_replacement_analysis(shortlist_df)
    with tab4:
        render_similarity_engine(shortlist_df)
    with tab5:
        render_asset_intelligence(shortlist_df)
    with tab6:
        render_driver_analysis(shortlist_df)




def render_opportunity_risk_top5_vertical(chart_source: pd.DataFrame, title: str = "Top 5 oportunidades ajustadas por riesgo", caption: str = "Prioridad inicial para revisión") -> None:
    """Render a clean horizontal Top 5 card for the Opportunity vs Risk matrix."""
    if chart_source.empty or "risk_adjusted_opportunity_score" not in chart_source.columns:
        return

    top = chart_source.copy()
    top["_score"] = pd.to_numeric(top["risk_adjusted_opportunity_score"], errors="coerce")
    top = top.dropna(subset=["_score"]).sort_values("_score", ascending=False).head(5)
    if top.empty:
        return

    items = []
    for idx, (_, row) in enumerate(top.iterrows(), start=1):
        player = html.escape(str(get_player_name(row)))
        club = html.escape(str(safe_get(row, "club", "")))
        league = html.escape(league_display_name(safe_get(row, "league", "")))
        score = get_numeric_value(row, "risk_adjusted_opportunity_score", 0)
        action = html.escape(action_display_name(safe_get(row, "recommended_action", "Review" if globals().get("LANG") == "EN" else "Revisión")))
        items.append(
            f"<div class='top5-horizontal-item'>"
            f"<div class='top5-horizontal-rank'>{idx}</div>"
            f"<div class='top5-horizontal-name'>{player}</div>"
            f"<div class='top5-horizontal-meta'>{club} · {league}<br>{action}</div>"
            f"<div class='top5-horizontal-score'>{score:.1f}</div>"
            f"</div>"
        )

    html_block = (
        "<div class='top5-horizontal-card'>"
        f"<div class='panel-title'>{html.escape(TXT(str(title)))}</div>"
        f"<div class='panel-subtitle'>{html.escape(UI(caption))}</div>"
        "<div class='top5-horizontal-grid'>"
        + "".join(items)
        + "</div></div>"
    )
    st.markdown(html_block, unsafe_allow_html=True)

def build_html_table(page_df: pd.DataFrame):
    """Build a compact recruitment-board table for the main view.

    The main dashboard should behave like an executive board: few columns,
    clear actions and no methodological clutter. Detailed variables remain in
    the specialised modules and CSV exports.
    """
    columns = [
        ("player_name_fbref", "Player" if LANG == "EN" else "Jugador"),
        ("club", "Club"),
        ("league", T("league")),
        ("position_group", "Pos."),
        ("age", "Age" if LANG == "EN" else "Edad"),
        ("market_value_eur", "Value" if LANG == "EN" else "Valor"),
        ("projected_market_value_3y_eur", "Value 3Y" if LANG == "EN" else "Valor 3Y"),
        ("asset_roi_3y_pct", "ROI 3Y"),
        ("executive_decision_score_v2", "Decision"),
        ("opportunity_score", "Opportunity"),
        ("risk_score", "Risk"),
        ("recommended_action", "Action" if LANG == "EN" else "Acción"),
    ]
    columns = [(c, label) for c, label in columns if c in page_df.columns]

    header = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    rows = ""

    for _, r in page_df.iterrows():
        cells = []
        for col, _ in columns:
            val = safe_get(r, col, "")

            if col in {"market_value_eur", "projected_market_value_3y_eur"}:
                val = format_money_short(val)
            elif col == "asset_roi_3y_pct":
                try:
                    val = f"{float(val):.0f}%"
                except Exception:
                    val = "N/A"
            elif col in {"executive_decision_score_v2", "opportunity_score", "risk_score"}:
                val = format_score(val)
            elif col == "age":
                try:
                    val = f"{float(val):.1f}"
                except Exception:
                    val = "N/A"
            elif col == "league":
                val = league_display_name(val)
            elif col == "recommended_action":
                cells.append(f"<td>{recommendation_badge(str(val))}</td>")
                continue

            if col in {"executive_decision_score_v2", "opportunity_score"}:
                cells.append(f"<td style='font-weight:900;'>{html.escape(str(val))}</td>")
            elif col == "risk_score":
                risk_value = pd.to_numeric(pd.Series([val]), errors="coerce").iloc[0]
                style = " style='font-weight:900;color:#b91c1c;'" if pd.notna(risk_value) and float(risk_value) >= 70 else ""
                cells.append(f"<td{style}>{html.escape(str(val))}</td>")
            else:
                cells.append(f"<td>{html.escape(str(val))}</td>")

        rows += "<tr>" + "".join(cells) + "</tr>"

    return f"""
    <div class="comparison-table-wrapper">
        <table class="player-table">
            <thead><tr>{header}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
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
                T("league"),
                T("position"),
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

            top5_items_html = "".join(f"<div>{item}</div>" for item in items)
            st.markdown(
                f"""
                <div class="compact-top5-card">
                    <b>🎯 Top 5 destacados</b>
                    <div class="compact-top5-grid">
                        {top5_items_html}
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
            f"Liga: {league_display_name(safe_get(row, 'league'))}<br>"
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
        f"Liga: {league_display_name(safe_get(row, 'league'))}<br>"
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
        return "Apuesta de crecimiento"
    if opportunity < opportunity_ref and risk <= risk_ref:
        return "Perfil de bajo impacto"
    return "Riesgo elevado"


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
    is_en = globals().get("LANG") == "EN"
    zone_labels = {
        "Objetivo prioritario": "Priority target" if is_en else "Objetivo prioritario",
        "Apuesta de crecimiento": "Growth bet" if is_en else "Apuesta de crecimiento",
        "Perfil de bajo impacto": "Low-impact profile" if is_en else "Perfil de bajo impacto",
        "Riesgo elevado": "High risk" if is_en else "Riesgo elevado",
    }
    axis_x_title = "Risk Score"
    axis_y_title = "Market Opportunity"
    risk_ref_label = "Median risk" if is_en else "Riesgo mediano"
    opportunity_ref_label = "Opportunity threshold" if is_en else "Umbral de oportunidad"

    def assign_zone(row):
        if row["opportunity_score"] >= opportunity_ref and row["risk_score"] <= risk_ref:
            return "Objetivo prioritario"
        if row["opportunity_score"] >= opportunity_ref and row["risk_score"] > risk_ref:
            return "Apuesta de crecimiento"
        if row["opportunity_score"] < opportunity_ref and row["risk_score"] <= risk_ref:
            return "Perfil de bajo impacto"
        return "Riesgo elevado"

    df["risk_zone"] = df.apply(assign_zone, axis=1)

    color_map = {
        "Objetivo prioritario": "#22c55e",
        "Apuesta de crecimiento": "#f97316",
        "Perfil de bajo impacto": "#3b82f6",
        "Riesgo elevado": "#ef4444",
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
        "Apuesta de crecimiento",
        "Perfil de bajo impacto",
        "Riesgo elevado",
    ]:
        zone_df = df[df["risk_zone"] == zone]

        if zone_df.empty:
            continue

        league_label = "League" if globals().get("LANG") == "EN" else "Liga"
        position_label = "Position" if globals().get("LANG") == "EN" else "Posición"

        hover_text = [
            f"<b>{get_player_name(row)}</b><br>"
            f"Club: {safe_get(row, 'club')}<br>"
            f"{league_label}: {league_display_name(safe_get(row, 'league'))}<br>"
            f"{position_label}: {safe_get(row, 'position_group')}<br>"
            f"Opportunity Score: {format_score(safe_get(row, 'opportunity_score'))}<br>"
            f"Risk Score: {format_score(safe_get(row, 'risk_score'))}<br>"
            f"Risk Level: {risk_level_display_name(safe_get(row, 'risk_level'))}<br>"
            f"Risk Adjusted Opportunity: {format_score(safe_get(row, 'risk_adjusted_opportunity_score'))}"
            for _, row in zone_df.iterrows()
        ]

        fig.add_trace(
            go.Scatter(
                x=zone_df["risk_score"],
                y=zone_df["opportunity_score"],
                mode="markers",
                name=zone_labels.get(zone, zone),
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
        line_color="rgba(15,23,42,0.55)",
        line_width=2,
    )

    fig.add_hline(
        y=opportunity_ref,
        line_dash="dash",
        line_color="rgba(15,23,42,0.55)",
        line_width=2,
    )

    fig.add_annotation(
        x=risk_ref,
        y=99.5,
        text=risk_ref_label,
        showarrow=False,
        xanchor="right",
        yanchor="top",
        xshift=-8,
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor="rgba(203,213,225,0.95)",
        borderwidth=1,
        borderpad=4,
        font=dict(size=12, color="#475569"),
    )
    fig.add_annotation(
        x=99,
        y=opportunity_ref,
        text=opportunity_ref_label,
        showarrow=False,
        xanchor="right",
        yanchor="top",
        yshift=-8,
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor="rgba(203,213,225,0.95)",
        borderwidth=1,
        borderpad=4,
        font=dict(size=12, color="#475569"),
    )

    fig.update_layout(
        height=640,
        margin=dict(l=18, r=44, t=42, b=32),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.86)",
            bordercolor="rgba(226,232,240,0.9)",
            borderwidth=1,
        ),
        xaxis_title=axis_x_title,
        yaxis_title=axis_y_title,
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
    strategic_bets = int((quadrants == "Apuesta de crecimiento").sum())
    stable_profiles = int((quadrants == "Perfil de bajo impacto").sum())
    avoid_profiles = int((quadrants == "Riesgo elevado").sum())

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
            "Apuestas de crecimiento",
            strategic_bets,
            "alto potencial · mayor incertidumbre",
        )

    with c3:
        render_metric_card_with_caption(
            "Bajo impacto",
            stable_profiles,
            "potencial limitado · menor riesgo",
        )

    with c4:
        render_metric_card_with_caption(
            "Riesgo elevado",
            avoid_profiles,
            "requiere validación adicional",
        )

    with c5:
        render_metric_card_with_caption(
            "🏆 Mejor objetivo",
            top_player,
            f"Risk-adjusted: {top_value}",
        )

def render_opportunity_risk_insight(chart_source: pd.DataFrame) -> None:
    """Render a concise automatic executive insight below Opportunity vs Risk."""

    required = {"opportunity_score", "risk_score"}
    if chart_source.empty or not required.issubset(chart_source.columns):
        return

    insight_df = chart_source.copy()
    insight_df["opportunity_score"] = pd.to_numeric(insight_df["opportunity_score"], errors="coerce")
    insight_df["risk_score"] = pd.to_numeric(insight_df["risk_score"], errors="coerce")
    if "risk_adjusted_opportunity_score" in insight_df.columns:
        insight_df["risk_adjusted_opportunity_score"] = pd.to_numeric(insight_df["risk_adjusted_opportunity_score"], errors="coerce")
    insight_df = insight_df.dropna(subset=["opportunity_score", "risk_score"])
    if insight_df.empty:
        return

    risk_ref = float(insight_df["risk_score"].median())
    opportunity_ref = float(insight_df["opportunity_score"].quantile(0.60))
    zones = insight_df.apply(lambda row: assign_decision_quadrant(row, opportunity_ref, risk_ref), axis=1)
    priority_count = int((zones == "Objetivo prioritario").sum())
    growth_count = int((zones == "Apuesta de crecimiento").sum())
    high_risk_count = int((zones == "Riesgo elevado").sum())
    moderate_risk_pct = float((insight_df["risk_score"].between(risk_ref - 8, risk_ref + 8)).mean() * 100)

    if "risk_adjusted_opportunity_score" in insight_df.columns and insight_df["risk_adjusted_opportunity_score"].notna().any():
        leader_row = insight_df.loc[insight_df["risk_adjusted_opportunity_score"].idxmax()]
        leader_metric = get_numeric_value(leader_row, "risk_adjusted_opportunity_score", np.nan)
        if globals().get("LANG") == "EN":
            leader_text = f"<b>{html.escape(get_player_name(leader_row))}</b> leads the risk-adjusted opportunity ranking ({leader_metric:.1f})."
        else:
            leader_text = f"<b>{html.escape(get_player_name(leader_row))}</b> lidera la oportunidad ajustada por riesgo ({leader_metric:.1f})."
    else:
        leader_row = insight_df.loc[insight_df["opportunity_score"].idxmax()]
        leader_text = (
            f"<b>{html.escape(get_player_name(leader_row))}</b> leads the group's Market Opportunity."
            if globals().get("LANG") == "EN"
            else f"<b>{html.escape(get_player_name(leader_row))}</b> lidera el Market Opportunity del grupo."
        )

    upside_row = insight_df.loc[insight_df["opportunity_score"].idxmax()]
    upside_player = html.escape(get_player_name(upside_row))
    upside_risk = get_numeric_value(upside_row, "risk_score", np.nan)

    if globals().get("LANG") == "EN":
        body = (
            f"Detected <b>{priority_count}</b> priority targets and <b>{growth_count}</b> growth bets within the filtered shortlist. "
            f"{leader_text}<br><br>"
            f"<b>{upside_player}</b> shows the strongest opportunity signal in the group, with Risk Score {upside_risk:.1f}. "
            f"<b>{moderate_risk_pct:.0f}%</b> of candidates sit in a moderate-risk band around the median. "
            f"The <b>{high_risk_count}</b> high-risk profiles require additional validation before moving forward in the funnel."
        )
    else:
        body = (
            f"Se identifican <b>{priority_count}</b> objetivos prioritarios y <b>{growth_count}</b> apuestas de crecimiento dentro de la shortlist filtrada. "
            f"{leader_text}<br><br>"
            f"<b>{upside_player}</b> presenta la mayor señal de oportunidad del grupo, con Risk Score {upside_risk:.1f}. "
            f"El <b>{moderate_risk_pct:.0f}%</b> de los candidatos se concentra en una banda de riesgo moderado alrededor de la mediana. "
            f"Los <b>{high_risk_count}</b> perfiles de riesgo elevado requieren validación adicional antes de avanzar en el funnel."
        )

    st.markdown(
        f"""
        <div class="radar-info-box">
            <b>Executive Insight</b><br><br>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_opportunity_risk_top5(chart_source: pd.DataFrame) -> None:
    """Render compact Top 5 cards below the Opportunity vs Risk matrix without HTML leakage."""
    if chart_source.empty or "risk_adjusted_opportunity_score" not in chart_source.columns:
        return

    top = chart_source.copy()
    top["_score"] = pd.to_numeric(top["risk_adjusted_opportunity_score"], errors="coerce")
    top = top.dropna(subset=["_score"]).sort_values("_score", ascending=False).head(5)
    if top.empty:
        return

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    cols = st.columns(5, gap="medium")
    for idx, ((_, row), col) in enumerate(zip(top.iterrows(), cols), start=1):
        with col:
            player = html.escape(get_player_name(row))
            club = html.escape(str(safe_get(row, "club", "")))
            league = html.escape(league_display_name(safe_get(row, "league", "")))
            score = get_numeric_value(row, "risk_adjusted_opportunity_score", 0)
            st.markdown(
                f"""
                <div class='compact-top5-card'>
                    <div style='font-size:.76rem;color:#64748b;font-weight:850;'>#{idx}</div>
                    <div style='font-weight:950;color:#0f172a;line-height:1.15;margin-top:2px;'>{player}</div>
                    <div style='color:#64748b;font-size:.76rem;margin-top:4px;'>{club} · {league}</div>
                    <div style='font-size:1.12rem;font-weight:950;color:#166534;margin-top:8px;'>{score:.1f}</div>
                </div>
                """,
                unsafe_allow_html=True,
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
if "league" in df.columns:
    df["league"] = df["league"].replace({"Liga Portugal": "Primeira Liga"})

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

scouting_df = df.copy()
football_df = build_football_universe_dataset(scouting_df)
FOOTBALL_UNIVERSE_SIZE = len(football_df)


# =============================================================================
# Sidebar
# =============================================================================

st.sidebar.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <div style="width:34px;height:34px;border-radius:50%;background:white;color:#0b1f3a;display:flex;align-items:center;justify-content:center;font-weight:900;">IQ</div>
        <div>
            <div style="font-size:1.05rem;font-weight:900;letter-spacing:.04em;">SCOUTING IQ</div>
            <div style="font-size:.72rem;color:#9fb3cc;">by MH Analytics</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
_INITIAL_LANG = st.session_state.get("scouting_iq_language", "ES")
lang_label_col, lang_control_col = st.sidebar.columns([0.24, 0.76], gap="small")
with lang_label_col:
    st.markdown(
        f"<div class='sidebar-inline-label'>{html.escape('Language' if _INITIAL_LANG == 'EN' else 'Idioma')}</div>",
        unsafe_allow_html=True,
    )
with lang_control_col:
    LANG = st.radio(
        "Language" if _INITIAL_LANG == "EN" else "Idioma",
        ["ES", "EN"],
        index=1 if _INITIAL_LANG == "EN" else 0,
        horizontal=True,
        key="scouting_iq_language",
        label_visibility="collapsed",
    )

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {'NAVIGATION' if LANG == 'EN' else 'NAVEGACIÓN'}")
PAGE_OPTIONS = [
    "Executive Overview",
    "Transfer Strategy",
    "Market Opportunities",
    "Player Intelligence",
    "Recruitment Board",
    "Methodology",
]
if "dashboard_navigation_page" not in st.session_state:
    st.session_state.dashboard_navigation_page = PAGE_OPTIONS[0]
if st.session_state.dashboard_navigation_page not in PAGE_OPTIONS:
    st.session_state.dashboard_navigation_page = PAGE_OPTIONS[0]

def _nav_label(page_name: str) -> str:
    labels = {
        "Executive Overview": "Executive",
        "Transfer Strategy": "Strategy",
        "Market Opportunities": "Market",
        "Player Intelligence": "Players",
        "Recruitment Board": "Board",
        "Methodology": "Methodology",
    }
    return labels.get(page_name, page_name)

st.sidebar.markdown("<div class='sidebar-nav-stack'>", unsafe_allow_html=True)
for _page_option in PAGE_OPTIONS:
    _active = st.session_state.dashboard_navigation_page == _page_option
    if st.sidebar.button(
        _nav_label(_page_option),
        key=f"nav_btn_{_page_option.replace(' ', '_').lower()}",
        type="primary" if _active else "secondary",
        use_container_width=True,
    ):
        st.session_state.dashboard_navigation_page = _page_option
        st.rerun()
st.sidebar.markdown("</div>", unsafe_allow_html=True)
dashboard_page = st.session_state.dashboard_navigation_page

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <details class="sidebar-filter-disclosure">
        <summary>{html.escape('FILTERS (?)' if LANG == 'EN' else 'FILTROS (?)')}</summary>
        <div>
            {html.escape('Filters define the active scouting universe before ranking, matrix and player-profile analysis. They do not retrain the model; they only constrain the eligible candidates shown in the dashboard.' if LANG == 'EN' else 'Los filtros definen el universo activo de scouting antes de revisar ranking, matriz y perfiles. No reentrenan el modelo: solo acotan los candidatos elegibles que se muestran en el dashboard.')}
        </div>
    </details>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
# Product logic: the dashboard remains in the actionable Scouting Universe.
# The global search can still detect players from the wider Football Intelligence layer
# and explain why they are outside the recommendation universe.
universe_mode = "Scouting Universe"

TEXT = {
    "ES": {
        "search_label": "Buscar jugador, club, liga o posición",
        "search_placeholder": "Ej.: Amorim, Strasbourg, Ligue 1, MID...",
        "filters_title": "FILTROS",
        "filters_caption": "Define criterios de elegibilidad antes de revisar ranking, matriz y perfiles.",
        "preset": "Preset de scouting",
        "selected_preset": "Preset seleccionado",
        "max_age": "Edad máxima",
        "min_minutes": "Minutos mínimos",
        "min_confidence": "Confidence Score mínimo",
        "league": "League" if LANG == "EN" else "Liga",
        "position": "Position" if LANG == "EN" else "Posición",
        "tier": "Tier de oportunidad",
        "opportunity_range": "Rango de Opportunity Score",
        "max_value": "Valor máximo (€M)",
        "min_roi": "ROI 3Y mínimo",
        "max_risk": "Risk Score máximo",
        "all_f": "Todas",
        "all_m": "Todos",
        "sort_by": "Ordenar por",
        "how_filters": "Cómo interpretar los filtros y el orden",
        "matrix_title": "Opportunity vs Risk Matrix",
        "matrix_caption": "Identifica objetivos prioritarios equilibrando potencial de mercado y riesgo estimado.",
        "methodology": "Ver metodología",
        "top5_title": "Top 5 oportunidades ajustadas por riesgo",
        "top5_caption": "Prioridad inicial para revisión de vídeo y contraste cualitativo.",
        "ranking_title": "Recruitment Ranking",
        "ranking_caption": "Vista ejecutiva compacta. La auditoría completa queda disponible en CSV y módulos detallados.",
    },
    "EN": {
        "search_label": "Search player, club, league or position",
        "search_placeholder": "e.g. Amorim, Strasbourg, Ligue 1, MID...",
        "filters_title": "FILTERS",
        "filters_caption": "Narrow the scouting universe before reviewing rankings, matrix and player profiles.",
        "preset": "Scouting preset",
        "selected_preset": "Selected preset",
        "max_age": "Maximum age",
        "min_minutes": "Minimum minutes",
        "min_confidence": "Minimum Confidence Score",
        "league": "League",
        "position": "Position",
        "tier": "Opportunity tier",
        "opportunity_range": "Opportunity Score range",
        "max_value": "Maximum value (€M)",
        "min_roi": "Minimum ROI 3Y",
        "max_risk": "Maximum Risk Score",
        "all_f": "All",
        "all_m": "All",
        "sort_by": "Sort by",
        "how_filters": "How to read filters and sorting",
        "matrix_title": "Opportunity vs Risk Matrix",
        "matrix_caption": "Identify priority targets by balancing market upside and estimated risk.",
        "methodology": "Show methodology",
        "top5_title": "Top 5 risk-adjusted opportunities",
        "top5_caption": "Initial priority list for video review and qualitative validation.",
        "ranking_title": "Recruitment Ranking",
        "ranking_caption": "Compact executive board. Full audit variables remain available in CSV and detailed modules.",
    },
}

def T(key: str) -> str:
    return TEXT.get(LANG, TEXT["ES"]).get(key, key)

SORT_LABELS = {
    "executive_decision_score_v2": {"ES": "Decision Score", "EN": "Decision Score"},
    "future_asset_score": {"ES": "Future Asset", "EN": "Future Asset"},
    "asset_roi_3y_pct": {"ES": "ROI 3Y", "EN": "ROI 3Y"},
    "risk_adjusted_opportunity_league": {"ES": "Context Fit", "EN": "Context Fit"},
    "risk_score": {"ES": "Risk Score", "EN": "Risk Score"},
    "projected_market_value_3y_eur": {"ES": "Valor proyectado 3Y", "EN": "Projected Value 3Y"},
    "opportunity_score": {"ES": "Market Opportunity", "EN": "Market Opportunity"},
}

def sort_label(col: str) -> str:
    return SORT_LABELS.get(col, {}).get(LANG, col.replace("_", " ").title())


LEAGUE_COUNTRY_LABELS = {
    "LaLiga": {"ES": "LaLiga (España)", "EN": "LaLiga (Spain)"},
    "La Liga": {"ES": "LaLiga (España)", "EN": "LaLiga (Spain)"},
    "Premier League": {"ES": "Premier League (Inglaterra)", "EN": "Premier League (England)"},
    "Bundesliga": {"ES": "Bundesliga (Alemania)", "EN": "Bundesliga (Germany)"},
    "Ligue 1": {"ES": "Ligue 1 (Francia)", "EN": "Ligue 1 (France)"},
    "Serie A": {"ES": "Serie A (Italia)", "EN": "Serie A (Italy)"},
    "Eredivisie": {"ES": "Eredivisie (Países Bajos)", "EN": "Eredivisie (Netherlands)"},
    "Liga Portugal": {"ES": "Primeira Liga (Portugal)", "EN": "Primeira Liga (Portugal)"},
    "Primeira Liga": {"ES": "Primeira Liga (Portugal)", "EN": "Primeira Liga (Portugal)"},
    "Belgian Pro League": {"ES": "Pro League (Bélgica)", "EN": "Pro League (Belgium)"},
    "Jupiler Pro League": {"ES": "Pro League (Bélgica)", "EN": "Pro League (Belgium)"},
}

def league_display_name(league: object) -> str:
    raw = str(league)
    return LEAGUE_COUNTRY_LABELS.get(raw, {}).get(LANG, raw)


# -----------------------------------------------------------------------------
# Display localization helpers for generated values and dataframe cells
# -----------------------------------------------------------------------------
VALUE_TRANSLATIONS = {
    "ES": {
        "Iniciar contacto": "Iniciar contacto",
        "Due diligence": "Due diligence",
        "Vídeo scouting": "Vídeo scouting",
        "Seguimiento activo": "Seguimiento activo",
        "Monitorización pasiva": "Monitorización pasiva",
        "Priorizar": "Priorizar",
        "Sustituto prioritario": "Sustituto prioritario",
        "Analizar en vídeo": "Analizar en vídeo",
        "Alternativa viable": "Alternativa viable",
        "Seguimiento": "Seguimiento",
        "Descartar por riesgo": "Descartar por riesgo",
        "Revisión exploratoria": "Revisión exploratoria",
        "Scouting prioritario": "Scouting prioritario",
        "Seguimiento recomendado": "Seguimiento recomendado",
        "Prioridad máxima": "Prioridad máxima",
        "Prioridad alta": "Prioridad alta",
        "Prioridad media": "Prioridad media",
        "Monitorizar": "Monitorizar",
        "Bajo": "Bajo",
        "Medio": "Medio",
        "Alto": "Alto",
        "Muy alto": "Muy alto",
        "Sin dato": "Sin dato",
        "Sin clasificar": "Sin clasificar",
        "Competitivo": "Competitivo",
        "Emergente": "Emergente",
        "Élite": "Élite",
        "Activo estratégico": "Activo estratégico",
        "Alto potencial": "Alto potencial",
        "Potencial medio": "Potencial medio",
        "Potencial limitado": "Potencial limitado",
        "Alta prioridad": "Alta prioridad",
        "Objetivo scouting": "Objetivo scouting",
        "Bajo riesgo": "Bajo riesgo",
        "Exploratorio": "Exploratorio",
        "candidatos listos para validación": "candidatos listos para validación",
        "seguimiento presencial": "seguimiento presencial",
        "prioridad de vídeo": "prioridad de vídeo",
        "seguimiento bajo": "seguimiento bajo",
        "parecido deportivo": "parecido deportivo",
        "fit competitivo": "fit competitivo",
        "más caro": "más caro",
        "de ahorro": "de ahorro",
        "menor es mejor": "menor es mejor",
        "potencial económico-deportivo": "potencial económico-deportivo",
        "eficiencia de inversión": "eficiencia de inversión",
        "proyección heurística": "proyección heurística",
        "ROI alto": "ROI alto",
        "activo atractivo": "activo atractivo",
        "valor futuro elevado": "valor futuro elevado",
        "context fit sólido": "context fit sólido",
        "confianza alta": "confianza alta",
        "fit de plantilla": "fit de plantilla",
        "riesgo elevado": "riesgo elevado",
        "riesgo bajo": "riesgo bajo",
        "adaptación incierta": "adaptación incierta",
        "confianza limitada": "confianza limitada",
        "perfil equilibrado": "perfil equilibrado",
    },
    "EN": {
        "Iniciar contacto": "Start contact",
        "Due diligence": "Due diligence",
        "Vídeo scouting": "Video scouting",
        "Seguimiento activo": "Active tracking",
        "Monitorización pasiva": "Passive monitoring",
        "Priorizar": "Prioritize",
        "Sustituto prioritario": "Priority replacement",
        "Analizar en vídeo": "Video review",
        "Alternativa viable": "Viable alternative",
        "Seguimiento": "Tracking",
        "Descartar por riesgo": "Reject due to risk",
        "Revisión exploratoria": "Exploratory review",
        "Scouting prioritario": "Priority scouting",
        "Seguimiento recomendado": "Recommended tracking",
        "Prioridad máxima": "Top priority",
        "Prioridad alta": "High priority",
        "Prioridad media": "Medium priority",
        "Monitorizar": "Monitor",
        "Bajo": "Low",
        "Medio": "Medium",
        "Alto": "High",
        "Muy alto": "Very high",
        "Sin dato": "No data",
        "Sin clasificar": "Unclassified",
        "Competitivo": "Competitive",
        "Emergente": "Emerging",
        "Élite": "Elite",
        "Activo estratégico": "Strategic asset",
        "Alto potencial": "High potential",
        "Potencial medio": "Medium potential",
        "Potencial limitado": "Limited potential",
        "Alta prioridad": "High priority",
        "Objetivo scouting": "Scouting target",
        "Bajo riesgo": "Low risk",
        "Exploratorio": "Exploratory",
        "candidatos listos para validación": "candidates ready for validation",
        "seguimiento presencial": "live scouting follow-up",
        "prioridad de vídeo": "video priority",
        "seguimiento bajo": "low-priority tracking",
        "parecido deportivo": "sporting similarity",
        "fit competitivo": "competitive fit",
        "más caro": "more expensive",
        "de ahorro": "saving",
        "menor es mejor": "lower is better",
        "potencial económico-deportivo": "economic-sporting upside",
        "eficiencia de inversión": "investment efficiency",
        "proyección heurística": "heuristic projection",
        "ROI alto": "high ROI",
        "activo atractivo": "attractive asset",
        "valor futuro elevado": "high future value",
        "context fit sólido": "solid context fit",
        "confianza alta": "high confidence",
        "fit de plantilla": "squad fit",
        "riesgo elevado": "high risk",
        "riesgo bajo": "low risk",
        "adaptación incierta": "uncertain adaptation",
        "confianza limitada": "limited confidence",
        "perfil equilibrado": "balanced profile",
    },
}

TEXT_EN_EXTRA = {
    "Executive Scouting Workspace": "Executive Scouting Workspace",
    "priorización, comparación, reemplazos, perfiles similares, inversión y drivers del modelo en un único flujo de decisión.": "prioritization, comparison, replacements, similar profiles, investment and model drivers in a single decision workflow.",
    "Resumen de decisión actualizado con los filtros activos.": "Decision summary updated with active filters.",
    "Best global decision": "Best global decision",
    "Valor actual": "Current value",
    "Valor 3Y": "3Y value",
    "años": "years",
    "Decision drivers": "Decision drivers",
    "Siguiente acción recomendada": "Recommended next action",
    "La decisión combina potencial de activo, ROI, context fit, riesgo y confianza analítica.": "The decision combines asset potential, ROI, context fit, risk and analytical confidence.",
    "Ver explicación completa y metodología de scores": "Show full score explanation and methodology",
    "Vista compacta para priorizar revisión. El CSV y las tablas detalladas conservan las variables auxiliares.": "Compact view to prioritize review. CSV and detailed tables keep auxiliary variables.",
    "Objetivo": "Objective",
    "convertir el ranking analítico en un flujo operativo de scouting. La fase asignada es una simulación inicial sin persistencia, pensada para priorizar revisión de vídeo, scouting en directo y due diligence.": "convert the analytical ranking into an operational scouting workflow. The assigned stage is an initial non-persistent simulation designed to prioritize video review, live scouting and due diligence.",
    "Fase": "Stage",
    "Siguiente acción": "Next action",
    "Validar contrato, agente, salario y disponibilidad": "Validate contract, agent, salary and availability",
    "Asignar seguimiento presencial": "Assign live scouting",
    "Revisión completa de vídeo": "Full video review",
    "Informe scout inicial": "Initial scout report",
    "Mantener en radar": "Keep on radar",
    "No priorizar de momento": "Do not prioritize for now",
        "Video Review": "Video review",
        "Scouting": "Scouting",
        "Monitor": "Monitor",
        "Due Diligence": "Due diligence",
        "Discovery": "Discovery",
    "Nota operativa": "Operational note",
    "Esta vista no sustituye a un CRM deportivo. Funciona como prototipo de priorización: traduce el ranking analítico en una primera asignación de fases para reducir carga de revisión y ordenar el trabajo del área de scouting.": "This view does not replace a sporting CRM. It works as a prioritization prototype: it translates the analytical ranking into an initial stage assignment to reduce review workload and organize scouting work.",
    "Identificación automática de reemplazos según perfil deportivo, contexto competitivo, riesgo y potencial de activo.": "Automatic replacement identification based on sporting profile, competitive context, risk and asset potential.",
    "Jugador a sustituir / comparar": "Player to replace / compare",
    "Número de sustitutos": "Number of replacements",
    "Mejor reemplazo": "Best replacement",
    "Similitud": "Similarity",
    "Adaptación": "Adaptation",
    "Riesgo": "Risk",
    "Fit contexto": "Context fit",
    "Fit de sustitución": "Replacement fit",
    "Descargar sustitutos CSV": "Download replacements CSV",
    "Identifica perfiles comparables al jugador de referencia y resume los principales trade-offs deportivos, económicos y de riesgo.": "Identify profiles comparable to the reference player and summarize the main sporting, economic and risk trade-offs.",
    "Jugador de referencia": "Reference player",
    "Perfil más similar": "Most similar profile",
    "Similitud media": "Average similarity",
    "Top perfiles": "Top profiles",
    "Lectura de similitud": "Similarity readout",
    "Variables utilizadas": "Variables used",
    "Evalúa los candidatos como activos deportivos: valor actual, valor proyectado, upside, ROI y balance riesgo-retorno.": "Assess candidates as sporting assets: current value, projected value, upside, ROI and risk-return balance.",
    "Mayor valor proyectado": "Highest projected value",
    "Activo menor riesgo": "Lowest-risk asset",
    "Factores principales que explican por qué el sistema prioriza o penaliza un jugador.": "Main factors explaining why the system prioritizes or penalizes a player.",
    "Jugador a explicar": "Player to explain",
    "Factores que impulsan la recomendación": "Factors driving the recommendation",
    "Factores que requieren cautela": "Factors requiring caution",
    "Factor": "Factor",
    "Impacto": "Impact",
    "Lectura ejecutiva": "Executive readout",
    "Perfil scouting": "Scouting profile",
    "Lectura analítica": "Analytical readout",
    "Recomendación": "Recommendation",
    "Recomendaciones analíticas": "Analytical recommendations",
    "Valor mercado": "Market value",
    "Valor estimado": "Estimated value",
    "Gap de mercado": "Market gap",
    "Ranking": "Ranking",
    "Club": "Club",
    "Liga": "League",
    "Posición": "Position",
    "Edad": "Age",
    "Temporada": "Season",
    "Minutos en liga": "League minutes",
    "Tier": "Tier",
    "Nivel de riesgo": "Risk level",
    "Comparación de candidatos": "Candidate comparison",
    "radar multi-jugador para contrastar fortalezas relativas y encaje deportivo sobre la misma escala percentil.": "multi-player radar to compare relative strengths and sporting fit on the same percentile scale.",
    "Selecciona entre 2 y 4 jugadores": "Select 2 to 4 players",
    "Candidatos seleccionados": "Selected candidates",
    "Metodología del benchmark": "Benchmark methodology",
    "Líder Opportunity": "Opportunity leader",
    "Mejor Growth": "Best growth",
    "Mayor Confidence": "Highest confidence",
    "Menor Risk": "Lowest risk",
    "Comparación de percentiles": "Percentile comparison",
    "Radar comparativo basado en benchmarking dinámico por posición. Cada eje representa el percentil del jugador frente al universo de referencia seleccionado.": "Comparative radar based on dynamic positional benchmarking. Each axis represents the player's percentile against the selected reference universe.",
    "Comparativa ejecutiva de candidatos filtrados. El CSV conserva las variables auxiliares para auditoría metodológica.": "Executive comparison of filtered candidates. The CSV keeps auxiliary variables for methodological audit.",
    "Selecciona candidatos para comparar": "Select candidates to compare",
    "Descargar comparación CSV": "Download comparison CSV",
}


# Runtime i18n extension for Sprint 11/12 late-rendered modules.
VALUE_TRANSLATIONS.setdefault("EN", {}).update({
    "Minutos jugados": "Minutes played",
    "Goles por 90": "Goals per 90",
    "Asistencias por 90": "Assists per 90",
    "Edad": "Age",
    "Liga": "League",
    "Posición": "Position",
    "Élite": "Elite",
    "Muy alto": "Very high",
    "Competitivo": "Competitive",
    "Bajo": "Low",
    "Medio": "Medium",
    "Alto": "High",
    "Scouting prioritario": "Priority scouting",
    "Seguimiento recomendado": "Recommended tracking",
    "Revisión exploratoria": "Exploratory review",
})
TEXT_EN_EXTRA.update({
    "Comparación de candidatos": "Candidate comparison",
    "radar multi-jugador para contrastar fortalezas relativas y encaje deportivo sobre la misma escala percentil.": "multi-player radar to compare relative strengths and sporting fit on the same percentile scale.",
    "Selecciona entre 2 y 4 jugadores": "Select 2 to 4 players",
    "Misma posición": "Same position",
    "Toda la muestra": "Full sample",
    "Candidatos seleccionados": "Selected candidates",
    "Metodología del benchmark": "Benchmark methodology",
    "Misma posición": "Same position",
    "Grupo posicional": "Position group",
    "Muestra": "Sample",
    "jugadores": "players",
    "Edad media": "Average age",
    "Minutos medios": "Average minutes",
    "Comparación de percentiles": "Percentile comparison",
    "Ganador por métrica": "Performance Leaders",
    "Scouting Insight": "Scouting Insight",
    "Tablero de reclutamiento": "Recruitment Board",
    "Comparativa ejecutiva de candidatos filtrados. El CSV conserva las variables auxiliares para auditoría metodológica.": "Executive comparison of filtered candidates. The CSV keeps auxiliary variables for methodological audit.",
    "Selecciona candidatos para comparar": "Select candidates to compare",
    "Lectura ejecutiva": "Executive readout",
    "Descargar comparación CSV": "Download comparison CSV",
    "Lectura de similitud": "Similarity readout",
    "Similarity Insight": "Similarity Insight",
    "La similitud media del Top": "The average similarity of the Top",
    "perfiles proceden de un contexto competitivo superior al jugador de referencia.": "profiles come from a stronger competitive context than the reference player.",
    "El valor de mercado medio de los perfiles similares es": "The average market value of similar profiles is",
    "Replacement Insight": "Replacement insight",
    "Descargar sustitutos CSV": "Download replacements CSV",
    "Investment Insight": "Investment insight",
    "Factores que impulsan la recomendación": "Recommendation drivers",
    "Factores que requieren cautela": "Caution drivers",
    "No se detectan contribuciones positivas destacadas.": "No major positive contributions detected.",
    "No se detectan contribuciones negativas destacadas.": "No major negative contributions detected.",
    "sin factores positivos destacados": "no major positive factors",
    "sin limitadores relevantes": "no relevant limiting factors",
    "Esta lectura resume la trazabilidad del modelo en lenguaje operativo, sin presentar SHAP como causalidad deportiva.": "This readout summarizes model traceability in operational language, without presenting SHAP as sporting causality.",
    "Perfil del jugador": "Player profile",
    "Jugador seleccionado": "Selected player",
    "Jugador referencia": "Reference player",
    "Analytical recommendations": "Analytical recommendations",
    "Este jugador aparece en la shortlist porque combina una señal de infravaloración con potencial de crecimiento y una fiabilidad analítica suficiente.": "This player appears in the shortlist because he combines an undervaluation signal with growth potential and sufficient analytical reliability.",
    "Gap relativo": "Relative gap",
    "Opp. ajustada": "Adjusted opp.",
    "Valor mercado": "Market value",
    "Valor estimado": "Estimated value",
    "Gap de mercado": "Market gap",
    "Nivel de riesgo": "Risk level",
    "Temporada": "Season",
    "Minutos en liga": "League minutes",
})


TEXT_EN_EXTRA.update({
    "Ver metodología técnica del modelo": "Show technical model methodology",
    "Ver contribución técnica detallada": "Show detailed technical contribution",
    "Este jugador aparece en la shortlist porque combina una señal de infravaloración con potencial de crecimiento y una fiabilidad analítica suficiente.": "This player appears in the shortlist because he combines an undervaluation signal with growth potential and sufficient analytical reliability.",
})

TEXT_EN_EXTRA.update({
    "Comparativa ejecutiva de candidatos filtrados. El CSV conserva las variables auxiliares para auditoría metodológica.": "Executive comparison of filtered candidates. The CSV keeps auxiliary variables for methodological audit.",
    "Selecciona candidatos para comparar": "Select candidates to compare",
    "Cómo interpretar los filtros y el orden": "How to read filters and sorting",
    "Decision Score: ranking final de decisión ejecutiva.": "Decision Score: final executive decision ranking.",
    "Future Asset: atractivo como activo deportivo a tres años.": "Future Asset: attractiveness as a three-year sporting asset.",
    "ROI 3Y: eficiencia relativa de inversión.": "ROI 3Y: relative investment efficiency.",
    "Context Fit: oportunidad ajustada por contexto competitivo y riesgo.": "Context Fit: opportunity adjusted by competitive context and risk.",
    "Risk Score: incertidumbre estimada; menor es mejor.": "Risk Score: estimated uncertainty; lower is better.",
    "Valor proyectado 3Y: potencial económico absoluto, no necesariamente mejor eficiencia.": "Projected 3Y Value: absolute economic potential, not necessarily better efficiency.",
    "candidatos comparados": "candidates compared",
    "perfiles accionables en Shortlist": "actionable Shortlist profiles",
    "ROI medio esperado": "Average expected ROI",
    "riesgo medio": "average risk",
    "La mejor decisión actual es": "The current best decision is",
    "siguiente acción": "next action",
    "Vista compacta para priorizar revisión. El CSV y las tablas detalladas conservan las variables auxiliares.": "Compact view to prioritize review. The CSV and detailed tables keep auxiliary variables.",
    "Revisión completa de vídeo": "Full video review",
    "Informe scout inicial": "Initial scout report",
    "Nota operativa": "Operational note",
    "Esta vista no sustituye a un CRM deportivo. Funciona como prototipo de priorización: traduce el ranking analítico en una primera asignación de fases para reducir carga de revisión y ordenar el trabajo del área de scouting.": "This view does not replace a sports CRM. It works as a prioritization prototype: it translates the analytical ranking into an initial stage assignment to reduce review workload and organize the scouting team's workflow.",
    "Top 5 oportunidades ajustadas por riesgo": "Top 5 risk-adjusted opportunities",
    "Prioridad inicial para revisión": "Initial review priority",
    "Seguimiento activo": "Active tracking",
})
def V(value: object) -> str:
    """Translate generated categorical values for display only."""
    raw = str(value)
    return VALUE_TRANSLATIONS.get(LANG, VALUE_TRANSLATIONS["ES"]).get(raw, raw)


def TXT(value: object) -> str:
    """Translate static UI prose used outside the TEXT dictionary."""
    raw = str(value)
    if LANG != "EN":
        return raw
    return TEXT_EN_EXTRA.get(raw, raw)


def action_display_name(value: object) -> str:
    return V(value)


def risk_level_display_name(value: object) -> str:
    return V(value)


def metric_display_name(value: object) -> str:
    """Translate radar/performance metric labels for display while keeping internal columns stable."""
    raw = str(value)
    if globals().get("LANG", "ES") != "EN":
        return raw
    metric_map = {
        "Minutos": "Minutes",
        "Goles/90": "Goals/90",
        "Asistencias/90": "Assists/90",
        "G+A/90": "G+A/90",
        "Tackles/90": "Tackles/90",
        "Interceptions/90": "Interceptions/90",
        "Blocks/90": "Blocks/90",
        "Growth Score": "Growth Score",
        "Confidence Score": "Confidence Score",
        "Save %": "Save %",
        "Clean Sheets": "Clean Sheets",
    }
    return metric_map.get(raw, raw)


# Extra display translations used by late-rendered modules. Kept outside TXT/UI
# dictionaries so the patch is robust against duplicated earlier dictionary blocks.
TEXT_EN_EXTRA.update({
    "Identifica perfiles comparables al jugador de referencia y resume los principales trade-offs deportivos, económicos y de riesgo.": "Identifies comparable profiles for the reference player and summarizes the main sporting, financial and risk trade-offs.",
    "Identificación automática de reemplazos según perfil deportivo, contexto competitivo, riesgo y potencial de activo.": "Automatic replacement identification based on sporting profile, competitive context, risk and asset upside.",
    "Número de sustitutos": "Number of replacements",
    "Jugador a sustituir / comparar": "Player to replace / compare",
    "Jugador de referencia": "Reference player",
    "No hay jugadores disponibles con los filtros actuales.": "No players available with the current filters.",
    "No hay columna de nombre disponible para analizar sustitutos.": "No player-name column available to analyze replacements.",
    "No hay columna de nombre disponible para calcular similitud.": "No player-name column available to calculate similarity.",
    "No hay jugadores disponibles para el motor de similitud.": "No players available for the similarity engine.",
    "No se encuentra el jugador de referencia seleccionado.": "Selected reference player not found.",
    "No se encuentra el jugador seleccionado.": "Selected player not found.",
    "No hay suficientes variables numéricas para calcular similitud de forma robusta.": "There are not enough numeric variables to calculate similarity robustly.",
    "No hay suficientes candidatos comparables para construir la lista de sustitutos.": "There are not enough comparable candidates to build the replacement list.",
    "Lectura de similitud": "Similarity insight",
    "Similarity Insight": "Similarity insight",
    "La similitud media del Top": "The average similarity of the Top",
    "Variables utilizadas": "Variables used",
    "Descargar sustitutos CSV": "Download replacements CSV",
    "Fit de sustitución": "Replacement fit",
    "Adaptación": "Adaptation",
    "Identificación automática de reemplazos": "Automatic replacement identification",
    "Factores principales que explican por qué el sistema prioriza o penaliza un jugador.": "Main factors explaining why the system prioritizes or penalizes a player.",
    "Jugador a explicar": "Player to explain",
    "No hay jugadores disponibles para Model Drivers.": "No players available for Model Drivers.",
    "Factores que impulsan la recomendación": "Recommendation drivers",
    "Factores que requieren cautela": "Caution drivers",
    "No se detectan contribuciones positivas destacadas.": "No relevant positive contributions detected.",
    "No se detectan contribuciones negativas destacadas.": "No relevant negative contributions detected.",
    "Lectura ejecutiva": "Executive readout",
    "aparece recomendado principalmente por": "is mainly recommended because of",
    "Los principales elementos a validar antes de elevarlo a fase avanzada son": "The main elements to validate before moving to an advanced stage are",
    "Esta lectura resume la trazabilidad del modelo en lenguaje operativo, sin presentar SHAP como causalidad deportiva.": "This readout summarizes model traceability in operational language without presenting SHAP as sporting causality.",
    "Objetivo": "Objective",
    "convertir el ranking analítico en un flujo operativo de scouting. La fase asignada es una simulación inicial sin persistencia, pensada para priorizar revisión de vídeo, scouting en directo y due diligence.": "turn the analytical ranking into an operational scouting workflow. The assigned stage is an initial non-persistent simulation designed to prioritize video review, live scouting and due diligence.",
    "Siguiente acción": "Next action",
    "Nota operativa": "Operational note",
    "Esta vista no sustituye a un CRM deportivo. Funciona como prototipo de priorización: traduce el ranking analítico en una primera asignación de fases para reducir carga de revisión y ordenar el trabajo del área de scouting.": "This view does not replace a sports CRM. It works as a prioritization prototype: it translates the analytical ranking into an initial stage assignment to reduce review workload and organize the scouting team's workflow.",
    "Comparación de candidatos": "Candidate Comparison",
    "Jugadores similares": "Similar Players",
    "Análisis de inversión": "Investment Analysis",
    "Modelo Drivers": "Model Drivers",
    "Informe individual de jugador": "Individual Player Report",
    "Selecciona un jugador": "Select a player",
    "Valor mercado": "Market value",
    "Valor estimado": "Estimated value",
    "Gap de mercado": "Market gap",
    "Ranking": "Ranking",
    "Perfil scouting": "Scouting profile",
    "Lectura analítica": "Analytical readout",
    "Recomendación": "Recommendation",
    "Recomendaciones analíticas": "Analytical recommendations",
    "Este jugador aparece en la shortlist porque combina una señal de infravaloración con potencial de crecimiento y una fiabilidad analítica suficiente.": "This player appears in the shortlist because he combines an undervaluation signal with growth potential and sufficient analytical reliability.",
    "Temporada": "Season",
    "Minutos en liga": "League minutes",
    "Nivel de riesgo": "Risk level",
    "Gap relativo": "Relative gap",
    "Opp. ajustada": "Adjusted opp.",
    "años": "years",
    "Jugador": "Player",
    "Métrica": "Metric",
    "Percentil": "Percentile",
    "Impacto": "Impact",
    "Factor": "Factor",
})

# Bidirectional/generated values and risk/action labels.
VALUE_TRANSLATIONS.setdefault("EN", {}).update({
    "Revisión completa de vídeo": "Full video review",
    "Informe scout inicial": "Initial scout report",
    "Validar contrato, agente, salario y disponibilidad": "Validate contract, agent, salary and availability",
    "Asignar seguimiento presencial": "Assign live scouting follow-up",
    "Mantener en radar": "Keep on radar",
    "No priorizar de momento": "Do not prioritize for now",
    "Low": "Low",
    "Medium": "Medium",
    "High": "High",
    "Bajo": "Low",
    "Medio": "Medium",
    "Alto": "High",
    "Muy alto": "Very high",
    "Prioridad alta": "High priority",
    "Prioridad media": "Medium priority",
    "Prioridad máxima": "Top priority",
    "Video Review": "Video Review",
    "Scouting": "Scouting",
    "Monitor": "Monitor",
    "Due Diligence": "Due Diligence",
    "Discovery": "Discovery",
})


# Final EN value/caption translations for Sprint 11 cards and sidebar filters.
VALUE_TRANSLATIONS.setdefault("EN", {}).update({
    "parecido deportivo": "sporting similarity",
    "fit competitivo": "competitive fit",
    "vs jugador referencia": "vs reference player",
    "Top perfiles": "Top profiles",
    "No disponible": "Not available",
    "para": "for",
    "de ahorro": "saving",
    "más caro": "more expensive",
    "High priority": "High priority",
    "Scouting target": "Scouting target",
    "Low risk": "Low risk",
    "Exploratory": "Exploratory",
})
TEXT_EN_EXTRA.update({
    "Selecciona al menos dos jugadores para comparar.": "Select at least two players to compare.",
    "Metodología del benchmark": "Reference methodology",
    "Grupo posicional": "Position group",
    "Muestra": "Sample",
    "jugadores": "players",
    "Edad media": "Average age",
    "Minutos medios": "Average minutes",
    "calidad del ranking": "ranking quality",
    "simulación conservadora": "conservative simulation",
    "Qué mide": "What it measures",
    "Lectura de negocio": "Business reading",
    "Importante": "Important",
})


TEXT_EN_EXTRA.update({
    "Comparativa ejecutiva de candidatos filtrados. El CSV conserva las variables auxiliares para auditoría metodológica.": "Executive comparison of filtered candidates. The CSV keeps auxiliary variables for methodological audit.",
    "Selecciona al menos un jugador para construir la tabla comparativa.": "Select at least one player to build the comparison table.",
    "No hay columna de nombre disponible para construir la tabla comparativa.": "No player-name column available to build the comparison table.",
    "No hay columna de nombre disponible para construir el comparador.": "No player-name column available to build the comparator.",
    "No hay jugadores disponibles para construir el radar con los filtros actuales.": "No players available to build the radar with the current filters.",
    "No hay suficientes métricas disponibles para construir benchmarking posicional real.": "Not enough metrics available to build a real positional benchmark.",
    "No hay suficientes métricas comunes para construir el radar comparativo.": "Not enough common metrics to build the comparison radar.",
    "Mejor reemplazo": "Best replacement",
    "Similitud": "Similarity",
    "Adaptación": "Adaptation",
    "Riesgo": "Risk",
    "Jugador referencia": "Reference player",
    "Perfil más similar": "Most similar profile",
    "Similitud media": "Average similarity",
    "Top perfiles": "Top profiles",
    "No disponible": "Not available",
    "Mayor Growth": "Best growth",
    "Mayor Confidence": "Highest confidence",
    "Menor Risk": "Lowest risk",
    "Líder Opportunity": "Opportunity leader",
    "Opportunity Score": "Opportunity Score",
    "Growth Score": "Growth Score",
    "Confidence Score": "Confidence Score",
    "Risk Score": "Risk Score",
    "Comparación de percentiles": "Percentile comparison",
    "Ganador por métrica": "Performance leaders",
    "Conclusión comparativa": "Scouting insight",
    "Descargar comparación CSV": "Download comparison CSV",
    "Descargar sustitutos CSV": "Download replacements CSV",
})
VALUE_TRANSLATIONS.setdefault("EN", {}).update({
    "Seguimiento activo": "Active tracking",
    "Monitorización pasiva": "Passive monitoring",
    "Vídeo scouting": "Video scouting",
    "Analizar en vídeo": "Video review",
    "Seguimiento recomendado": "Recommended tracking",
    "Revisión exploratoria": "Exploratory review",
    "Scouting prioritario": "Priority scouting",
    "Alta prioridad": "High priority",
    "Objetivo scouting": "Scouting target",
    "Exploratorio": "Exploratory",
    "Bajo riesgo": "Low risk",
})

def league_quality_display_name(value: object) -> str:
    return V(value)


def tier_display_name(value: object) -> str:
    return V(translate_tier(value))


def driver_display_name(value: object) -> str:
    raw = str(value)
    parts = [part.strip() for part in raw.split("+")]
    return " + ".join(V(part) for part in parts if part)


def localize_display_df(display_df: pd.DataFrame) -> pd.DataFrame:
    """Localize categorical dataframe cells without touching the analytical dataset."""
    result = display_df.copy()
    for col in result.columns:
        if col == "league":
            result[col] = result[col].apply(league_display_name)
        elif col in {"recommended_action", "replacement_fit", "adaptation_risk_label", "risk_level", "future_asset_tier", "executive_priority", "next_action", "pipeline_stage"}:
            result[col] = result[col].apply(V)
        elif col == "league_quality_tier":
            result[col] = result[col].apply(league_quality_display_name)
        elif col == "decision_drivers":
            result[col] = result[col].apply(driver_display_name)
        elif col == "decision_stage":
            # Stage labels are product-stage names and stay stable in both languages.
            result[col] = result[col].astype(str)
    return result

def _fmt_sidebar_number(value, suffix: str = "") -> str:
    """Format sidebar numeric values without unnecessary decimals."""
    try:
        numeric = float(value)
        if numeric.is_integer():
            return f"{int(numeric):,}{suffix}"
        return f"{numeric:g}{suffix}"
    except Exception:
        return f"{value}{suffix}"


def render_slider_range_hint(min_value, max_value, current_value, suffix: str = "") -> None:
    """Render a persistent selected-value hint above each sidebar slider.

    The dashboard no longer relies on native Streamlit/BaseWeb hover labels.
    This compact custom label is rendered before the slider and is independent
    from previous .slider-range-hint CSS patches.
    """
    if isinstance(current_value, tuple):
        selected_text = f"{_fmt_sidebar_number(current_value[0], suffix)} – {_fmt_sidebar_number(current_value[1], suffix)}"
    else:
        selected_text = _fmt_sidebar_number(current_value, suffix)

    selected_label = "Selected" if globals().get("LANG", "ES") == "EN" else "Seleccionado"

    st.markdown(
        f"""
        <div class="sidebar-slider-current-state">
            <span>{html.escape(selected_label)}</span>
            <b>{html.escape(selected_text)}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_filter_value(current_value, suffix: str = "", min_value=None, max_value=None) -> None:
    """Render a compact persistent value badge for numeric sidebar filters."""
    selected_label = "Selected" if globals().get("LANG", "ES") == "EN" else "Seleccionado"
    range_label = "Allowed range" if globals().get("LANG", "ES") == "EN" else "Rango permitido"
    selected_text = _fmt_sidebar_number(current_value, suffix)
    range_html = ""
    if min_value is not None and max_value is not None:
        range_text = f"{_fmt_sidebar_number(min_value, suffix)} – {_fmt_sidebar_number(max_value, suffix)}"
        range_html = f"<div class='sidebar-filter-badge-item'><span>{html.escape(range_label)}</span><b>{html.escape(range_text)}</b></div>"
    st.markdown(
        f"""
        <div class="sidebar-filter-value-badge sidebar-filter-value-badge--two-col">
            <div class="sidebar-filter-badge-item"><span>{html.escape(selected_label)}</span><b>{html.escape(selected_text)}</b></div>
            {range_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_filter_range(selected_min, selected_max, global_min=None, global_max=None, suffix: str = "") -> None:
    """Render selected interval plus the allowed global interval for paired numeric filters."""
    selected_label = "Selected interval" if globals().get("LANG", "ES") == "EN" else "Intervalo seleccionado"
    range_label = "Allowed range" if globals().get("LANG", "ES") == "EN" else "Rango permitido"
    selected_text = f"{_fmt_sidebar_number(selected_min, suffix)} – {_fmt_sidebar_number(selected_max, suffix)}"
    range_html = ""
    if global_min is not None and global_max is not None:
        range_text = f"{_fmt_sidebar_number(global_min, suffix)} – {_fmt_sidebar_number(global_max, suffix)}"
        range_html = f"<div class='sidebar-filter-badge-item'><span>{html.escape(range_label)}</span><b>{html.escape(range_text)}</b></div>"
    st.markdown(
        f"""
        <div class="sidebar-filter-value-badge sidebar-filter-value-badge--two-col sidebar-filter-value-badge--range">
            <div class="sidebar-filter-badge-item"><span>{html.escape(selected_label)}</span><b>{html.escape(selected_text)}</b></div>
            {range_html}
        </div>
        """,
        unsafe_allow_html=True,
    )




# =============================================================================
# Final UX close patch: stronger search, stable clear action and sidebar sliders
# =============================================================================
st.markdown(
    """
<style>
.global-search-shell {
    border: 1px solid #c8d7ec !important;
    border-radius: 18px !important;
    padding: 14px 16px !important;
    margin: 0 0 8px 0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f3f8ff 100%) !important;
    box-shadow: 0 14px 32px rgba(15,23,42,.075) !important;
}
.global-search-title { color:#0f2f5f !important; letter-spacing:.08em !important; }
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] label {
    font-size: .86rem !important;
    color: #0f172a !important;
    font-weight: 900 !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 52px !important;
    border: 1px solid #b7c8dd !important;
    background: #ffffff !important;
    border-radius: 15px !important;
    box-shadow: 0 10px 26px rgba(15,23,42,.065) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.13), 0 12px 28px rgba(15,23,42,.075) !important;
}
.search-clear-row { margin: -12px 0 18px 0 !important; }
[data-testid="stSidebar"] .sidebar-slider-title {
    color: #ffffff !important;
    font-weight: 900 !important;
    margin-top: 1.10rem !important;
    margin-bottom: .30rem !important;
}
[data-testid="stSidebar"] .slider-range-hint {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 0 .32rem 0 !important;
    padding: 7px 9px !important;
    border-radius: 9px !important;
    background: rgba(219,234,254,.16) !important;
    border: 1px solid rgba(191,219,254,.34) !important;
    box-shadow: none !important;
    font-size: .73rem !important;
    line-height: 1.15 !important;
}
[data-testid="stSidebar"] .slider-range-hint span,
[data-testid="stSidebar"] .slider-range-hint b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [role="tooltip"],
[data-testid="stSidebar"] .stSlider [data-baseweb="tooltip"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("""<style>

/* =========================
   Sprint 11 UX closure: definitive search + sidebar filter readability
   ========================= */
.global-search-shell {
    border: 1px solid #b9cbe3 !important;
    border-radius: 20px !important;
    padding: 16px 18px 14px 18px !important;
    margin: 0 0 10px 0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%) !important;
    box-shadow: 0 16px 36px rgba(15, 23, 42, .080) !important;
}
.global-search-title {
    color: #0f2f5f !important;
    font-size: .82rem !important;
    letter-spacing: .09em !important;
    text-transform: uppercase !important;
}
.global-search-caption {
    color: #475569 !important;
    font-size: .86rem !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 54px !important;
    border: 1px solid #aebfd4 !important;
    border-radius: 16px !important;
    background: #ffffff !important;
    box-shadow: 0 12px 28px rgba(15, 23, 42, .070) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, .14), 0 14px 32px rgba(15, 23, 42, .085) !important;
}
.sidebar-filter-group-title {
    color: #93c5fd !important;
    font-size: .72rem !important;
    font-weight: 950 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    margin: 1.05rem 0 .30rem 0 !important;
    padding-top: .55rem !important;
    border-top: 1px solid rgba(148, 163, 184, .22) !important;
}
[data-testid="stSidebar"] .sidebar-slider-title {
    color: #ffffff !important;
    font-size: .86rem !important;
    font-weight: 900 !important;
    margin: .82rem 0 .22rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-slider-state,
[data-testid="stSidebar"] .sidebar-slider-state * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] .sidebar-slider-state {
    justify-content: space-between !important;
    align-items: center !important;
    gap: 8px !important;
    width: 100% !important;
    margin: 0 0 .24rem 0 !important;
    padding: 7px 9px !important;
    border-radius: 10px !important;
    background: rgba(219, 234, 254, .16) !important;
    border: 1px solid rgba(191, 219, 254, .36) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045) !important;
    font-size: .72rem !important;
    line-height: 1.15 !important;
    font-weight: 800 !important;
}
/* Native slider values/ticks are intentionally suppressed: sidebar-slider-state is the single visible source. */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [role="tooltip"],
[data-testid="stSidebar"] .stSlider [data-baseweb="tooltip"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
.search-clear-row button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    min-height: 32px !important;
    padding: .25rem .70rem !important;
}
.search-clear-row button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}

</style>""", unsafe_allow_html=True)



# =============================================================================
# UX closing micro-patch: search prominence and sidebar range readability
# =============================================================================
st.markdown(
    """
<style>
/* Make the bordered search container behave like an obvious product search card. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) {
    border: 1px solid #b8cce6 !important;
    border-radius: 20px !important;
    background: linear-gradient(135deg, #ffffff 0%, #f2f8ff 100%) !important;
    box-shadow: 0 16px 36px rgba(15, 23, 42, .085) !important;
    padding: 4px 6px 10px 6px !important;
    margin-bottom: 16px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) label {
    font-size: .82rem !important;
    font-weight: 950 !important;
    color: #1e293b !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #9fb7d6 !important;
    border-radius: 16px !important;
    min-height: 56px !important;
    box-shadow: 0 10px 26px rgba(15,23,42,.070) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 12px 28px rgba(15,23,42,.085) !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.global-search-title) button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    min-height: 34px !important;
    margin-top: .25rem !important;
}
/* Range box is now rendered after the slider track and must always be readable. */
[data-testid="stSidebar"] .sidebar-slider-state {
    margin: .34rem 0 1.10rem 0 !important;
    padding: 8px 10px !important;
    border-radius: 10px !important;
    background: rgba(219,234,254,.16) !important;
    border: 1px solid rgba(191,219,254,.36) !important;
    color: #ffffff !important;
    display: flex !important;
    justify-content: space-between !important;
    gap: 10px !important;
}
[data-testid="stSidebar"] .sidebar-slider-state span,
[data-testid="stSidebar"] .sidebar-slider-state b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}
/* Aggressive but scoped cleanup of native slider labels that only appear on hover. */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [role="tooltip"],
[data-testid="stSidebar"] .stSlider [data-baseweb="tooltip"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Sprint 11/12 final UX closure patch
# =============================================================================
st.markdown(
    """
<style>
/* Search: single CRM-style entry point, not a generic filter card. */
.final-search-card {
    border: 1px solid #b6cae5;
    border-radius: 22px;
    background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%);
    box-shadow: 0 18px 42px rgba(15, 23, 42, .090);
    padding: 18px 20px 16px 20px;
    margin: 0 0 18px 0;
}
.final-search-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #0f2f5f;
    font-size: .86rem;
    font-weight: 950;
    letter-spacing: .075em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.final-search-caption {
    color: #475569;
    font-size: .88rem;
    line-height: 1.35;
    margin-bottom: 10px;
}
.final-search-card label {
    font-weight: 950 !important;
    color: #0f172a !important;
}
.final-search-card div[data-baseweb="select"] > div {
    min-height: 58px !important;
    border: 2px solid #9fb7d6 !important;
    background: #ffffff !important;
    border-radius: 18px !important;
    box-shadow: 0 12px 28px rgba(15,23,42,.075) !important;
    font-size: 1rem !important;
}
.final-search-card div[data-baseweb="select"] > div:hover,
.final-search-card div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 14px 30px rgba(15,23,42,.090) !important;
}
.final-search-card [data-baseweb="select"] svg {
    opacity: 1 !important;
}
/* Hide old duplicated clear-search button styles if legacy code remains. */
.search-clear-row, .clear-search-button { display: none !important; }

/* Quick guide / scouting setup */
.quick-guide-card {
    background: #ffffff;
    border: 1px solid #dbe3ee;
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 10px 26px rgba(15,23,42,.050);
    margin: 0 0 18px 0;
}
.scouting-setup-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    overflow: hidden;
    font-size: .86rem;
}
.scouting-setup-table th {
    background: #f8fafc;
    color: #334155;
    font-weight: 900;
    padding: 9px 10px;
    text-align: left;
}
.scouting-setup-table td {
    padding: 9px 10px;
    border-top: 1px solid #edf2f7;
    color: #334155;
}
.scouting-concept-chip, .matrix-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border: 1px solid #dbeafe;
    background: #eff6ff;
    color: #1e3a8a;
    border-radius: 999px;
    padding: 7px 11px;
    font-size: .78rem;
    font-weight: 900;
    margin: 0 6px 7px 0;
}
.matrix-chip-green { background:#ecfdf5; border-color:#bbf7d0; color:#166534; }
.matrix-chip-orange { background:#fff7ed; border-color:#fed7aa; color:#9a3412; }
.matrix-chip-blue { background:#eff6ff; border-color:#bfdbfe; color:#1d4ed8; }
.matrix-chip-red { background:#fef2f2; border-color:#fecaca; color:#991b1b; }

/* Sidebar preset and value-first sliders */
.sidebar-preset-card {
    background: rgba(219,234,254,.12);
    border: 1px solid rgba(191,219,254,.28);
    border-radius: 14px;
    padding: 12px 13px;
    margin: .70rem 0 1.15rem 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}
.sidebar-preset-eyebrow {
    color: #bfdbfe !important;
    -webkit-text-fill-color: #bfdbfe !important;
    font-size: .72rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 5px;
}
.sidebar-preset-title {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 1.02rem;
    font-weight: 950;
    line-height: 1.15;
    margin-bottom: 5px;
}
.sidebar-preset-text {
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
    font-size: .82rem;
    line-height: 1.38;
}
[data-testid="stSidebar"] .sidebar-slider-title {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: .89rem !important;
    font-weight: 950 !important;
    margin: 1.10rem 0 .32rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-slider-state-modern {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(219,234,254,.13) !important;
    border: 1px solid rgba(191,219,254,.34) !important;
    border-radius: 13px !important;
    padding: 9px 10px !important;
    margin: 0 0 .35rem 0 !important;
    color: #ffffff !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04) !important;
}
[data-testid="stSidebar"] .sidebar-slider-current {
    display: flex !important;
    align-items: baseline !important;
    justify-content: space-between !important;
    gap: 10px !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .sidebar-slider-current span,
[data-testid="stSidebar"] .sidebar-slider-range span {
    color: #bfdbfe !important;
    -webkit-text-fill-color: #bfdbfe !important;
    font-size: .70rem !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: .04em !important;
}
[data-testid="stSidebar"] .sidebar-slider-current b {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 1.12rem !important;
    font-weight: 950 !important;
}
[data-testid="stSidebar"] .sidebar-slider-range {
    display: flex !important;
    justify-content: space-between !important;
    gap: 10px !important;
}
[data-testid="stSidebar"] .sidebar-slider-range b {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
    font-size: .78rem !important;
    font-weight: 850 !important;
}
/* Keep native slider tick labels and hover balloons suppressed; our card is canonical. */
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] *,
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] *,
[data-testid="stSidebar"] .stSlider [role="tooltip"],
[data-testid="stSidebar"] .stSlider [data-baseweb="tooltip"],
[data-testid="stSidebar"] .stSlider div[aria-hidden="true"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* Context hierarchy: candidates first, model universe second. */
.context-strip-v2 {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 10px 26px rgba(15,23,42,.050);
    margin: 14px 0 24px 0;
}
.context-strip-main {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    gap: 16px;
    margin-bottom: 12px;
}
.context-current-kpi {
    min-width: 210px;
}
.context-current-value {
    font-size: 2.35rem;
    line-height: .95;
    font-weight: 950;
    color: #0f172a;
}
.context-current-label {
    color: #475569;
    font-size: .82rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .04em;
    margin-top: 4px;
}
.context-secondary-kpis {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}
.active-search-chip button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    min-height: 33px !important;
    padding: .25rem .70rem !important;
    margin: 0 0 10px 0 !important;
}
.active-search-chip button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}
.action-badge-green { background:#dcfce7; color:#166534; border:1px solid #bbf7d0; }
.action-badge-yellow { background:#fef3c7; color:#92400e; border:1px solid #fde68a; }
.action-badge-red { background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }
.action-badge-gray { background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; }
.action-badge-green, .action-badge-yellow, .action-badge-red, .action-badge-gray {
    display:inline-flex;align-items:center;border-radius:999px;padding:5px 9px;font-weight:900;font-size:.74rem;white-space:nowrap;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Final integrated UX patch: search card, quick guide card and active chips
# =============================================================================
st.markdown(
    """
<style>
/* Modern Quick Guide card: replaces the default expander look. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.quick-guide-title) {
    border: 1px solid #dbe3ee !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
    box-shadow: 0 10px 26px rgba(15, 23, 42, .050) !important;
    padding: 8px 10px 12px 10px !important;
    margin: 0 0 18px 0 !important;
}
.quick-guide-header { margin-bottom: 8px; }
.quick-guide-title {
    color: #0f2f5f;
    font-size: .90rem;
    font-weight: 950;
    letter-spacing: .02em;
    margin-bottom: 3px;
}
.quick-guide-subtitle {
    color: #64748b;
    font-size: .82rem;
    line-height: 1.35;
    margin-bottom: 9px;
}
.quick-guide-chip-row { display:flex; flex-wrap:wrap; gap:7px; }
.quick-guide-chip-row span {
    display:inline-flex;
    align-items:center;
    border:1px solid #dbeafe;
    background:#eff6ff;
    color:#1e3a8a;
    border-radius:999px;
    padding:5px 9px;
    font-size:.74rem;
    font-weight:900;
}

/* Integrated CRM search card. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    border: 1px solid #b6cae5 !important;
    border-radius: 22px !important;
    background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%) !important;
    box-shadow: 0 18px 42px rgba(15, 23, 42, .090) !important;
    padding: 12px 14px 14px 14px !important;
    margin: 0 0 18px 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-title {
    color:#0f2f5f !important;
    font-size:.88rem !important;
    font-weight:950 !important;
    letter-spacing:.075em !important;
    text-transform:uppercase !important;
    margin-bottom:5px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-caption {
    color:#475569 !important;
    font-size:.88rem !important;
    line-height:1.35 !important;
    margin-bottom:10px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) label {
    font-size:.82rem !important;
    font-weight:950 !important;
    color:#0f172a !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    min-height:58px !important;
    border:2px solid #9fb7d6 !important;
    background:#ffffff !important;
    border-radius:18px !important;
    box-shadow:0 12px 28px rgba(15,23,42,.075) !important;
    font-size:1rem !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color:#2563eb !important;
    box-shadow:0 0 0 4px rgba(37,99,235,.14), 0 14px 30px rgba(15,23,42,.090) !important;
}

/* Active search chip lives only inside Contexto activo. */
.context-chip-row { display:flex; flex-wrap:wrap; gap:0; }
.context-chip-search {
    text-decoration:none !important;
    cursor:pointer !important;
    border-color:#bfdbfe !important;
    background:#eff6ff !important;
    color:#1e3a8a !important;
    font-weight:950 !important;
}
.context-chip-search:hover {
    background:#dbeafe !important;
    border-color:#93c5fd !important;
}
.active-search-chip, .clear-search-button { display:none !important; }
</style>
""",
    unsafe_allow_html=True,
)


def render_quick_guide() -> None:
    """Compact contextual guide rendered as a popover near Contexto activo."""
    guide_label = "📖 Quick Guide" if LANG == "EN" else "📖 Guía rápida"
    guide_help = (
        "Open ranking logic, filters and glossary."
        if LANG == "EN"
        else "Abrir lógica del ranking, filtros y glosario."
    )

    with st.popover(guide_label, help=guide_help):
        tab_rank, tab_filters, tab_glossary = st.tabs(
            [
                "Ranking",
                "Filters" if LANG == "EN" else "Filtros",
                "Glossary" if LANG == "EN" else "Glosario",
            ]
        )
        with tab_rank:
            if LANG == "EN":
                st.markdown(
                    """
The ranking is not a market-price prediction table. It is an executive decision layer that combines **Future Asset**, **ROI 3Y**, **Opportunity**, **Risk**, **Context Fit** and **Confidence** to reduce the scouting search space.
                    """
                )
            else:
                st.markdown(
                    """
El ranking no es una tabla de predicción de precio de mercado. Es una capa ejecutiva de decisión que combina **Future Asset**, **ROI 3Y**, **Opportunity**, **Risk**, **Context Fit** y **Confidence** para reducir el espacio de búsqueda del área deportiva.
                    """
                )
        with tab_filters:
            if LANG == "EN":
                st.markdown(
                    """
The sidebar defines the active scouting universe. The most important operational filters are **maximum age**, **minimum minutes** and **minimum confidence**. Numeric controls are used to avoid hover-dependent slider labels.
                    """
                )
            else:
                st.markdown(
                    """
La barra lateral define el universo activo de scouting. Los filtros operativos más importantes son **edad máxima**, **minutos mínimos** y **confianza mínima**. Se usan controles numéricos para evitar etiquetas de slider dependientes del hover.
                    """
                )
        with tab_glossary:
            if LANG == "EN":
                rows = [
                    ("Opportunity", "Sporting-economic upside and undervaluation signal."),
                    ("Risk", "Estimated uncertainty; lower is better."),
                    ("Recommendation", "Analytical interpretation of the candidate profile."),
                    ("Action", "Next operational step for the recruitment team."),
                    ("Decision Score", "Final executive priority score."),
                    ("Tier", "Secondary opportunity classification."),
                ]
            else:
                rows = [
                    ("Opportunity", "Potencial deportivo-económico y señal de infravaloración."),
                    ("Risk", "Riesgo estimado; menor es mejor."),
                    ("Recommendation", "Interpretación analítica del perfil candidato."),
                    ("Action", "Siguiente paso operativo para el área deportiva."),
                    ("Decision Score", "Score ejecutivo final de priorización."),
                    ("Tier", "Clasificación secundaria de oportunidad."),
                ]
            table_rows = "".join(
                f"<tr><td><b>{html.escape(k)}</b></td><td>{html.escape(v)}</td></tr>" for k, v in rows
            )
            st.markdown(
                f"""
<table class="scouting-setup-table">
    <thead><tr><th>{html.escape('Concept' if LANG == 'EN' else 'Concepto')}</th><th>{html.escape('Meaning' if LANG == 'EN' else 'Qué significa')}</th></tr></thead>
    <tbody>{table_rows}</tbody>
</table>
                """,
                unsafe_allow_html=True,
            )


def build_search_options(df: pd.DataFrame) -> tuple[list[str], dict[str, str]]:
    """Build CRM-like search labels while preserving raw values for filtering."""
    labels: list[str] = []
    label_to_raw: dict[str, str] = {}

    def add(label: str, raw: str) -> None:
        if raw is None or str(raw).strip() == "":
            return
        if label not in label_to_raw:
            labels.append(label)
            label_to_raw[label] = str(raw)

    if "league" in df.columns:
        for league in sorted(df["league"].dropna().astype(str).unique().tolist(), key=str.lower):
            add(f"League · {league_display_name(league)}", league)
    if "club" in df.columns:
        for club in sorted(df["club"].dropna().astype(str).unique().tolist(), key=str.lower):
            add(f"Club · {club}", club)
    name_col = get_player_name_column(df)
    if name_col is not None:
        tmp = df.dropna(subset=[name_col]).copy()
        if "executive_decision_score_v2" in tmp.columns:
            tmp = tmp.sort_values("executive_decision_score_v2", ascending=False)
        elif "opportunity_score" in tmp.columns:
            tmp = tmp.sort_values("opportunity_score", ascending=False)
        for _, row in tmp.drop_duplicates(subset=[name_col]).iterrows():
            name = str(row[name_col])
            meta = " · ".join(str(x) for x in [safe_get(row, "club", ""), safe_get(row, "position_group", "")] if str(x).strip())
            add(f"Player · {name}" + (f" ({meta})" if meta else ""), name)
    if "position_group" in df.columns:
        for pos in sorted(df["position_group"].dropna().astype(str).unique().tolist(), key=str.lower):
            add(f"Position · {pos}", pos)
    return labels, label_to_raw


def render_action_badge(label: str) -> str:
    """Modern action badges for the recruitment ranking."""
    raw = str(label)
    display = action_display_name(raw) if "action_display_name" in globals() else V(raw)
    if raw in {"Iniciar contacto", "Due diligence"}:
        cls, icon = "action-badge-green", "🟢"
    elif raw in {"Vídeo scouting", "Seguimiento activo", "Analizar en vídeo"}:
        cls, icon = "action-badge-yellow", "🟡"
    elif raw in {"Monitorización pasiva", "No priorizar", "Descartar por riesgo"}:
        cls, icon = "action-badge-red", "🔴"
    else:
        cls, icon = "action-badge-gray", "⚪"
    return f'<span class="{cls}">{icon} {html.escape(display)}</span>'




# =============================================================================
# Sprint 11 final visual polish v3: hierarchy, spacing and guide placement
# =============================================================================
st.markdown(
    """
<style>
/* Remove excessive Streamlit chrome/blank space above the product header. */
header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
}
[data-testid="stDecoration"] { display: none !important; }
.block-container {
    padding-top: 0.20rem !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 18px !important;
}
.scouting-topbar-right {
    gap: 16px !important;
}
.scouting-topbar-right span {
    font-size: .80rem !important;
    font-weight: 850 !important;
    color: #dbeafe !important;
}

/* Search module: make the card and the writable control visually distinct. */
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #c7d8ee !important;
    border-top: 4px solid #2563eb !important;
    border-left: 1px solid #c7d8ee !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 44px rgba(15, 23, 42, .075), 0 0 0 1px rgba(37,99,235,.035) !important;
    padding: 18px 20px 20px 20px !important;
    margin: 0 0 22px 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-title {
    color: #0b2f5f !important;
    font-size: .96rem !important;
    letter-spacing: .085em !important;
    margin-bottom: 8px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) .final-search-caption {
    color: #52657a !important;
    font-size: .88rem !important;
    margin-bottom: 14px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) label {
    color: #334155 !important;
    font-size: .82rem !important;
    font-weight: 900 !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #2563eb !important;
    border-radius: 999px !important;
    min-height: 58px !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, .11) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 12px 30px rgba(37,99,235,.14) !important;
}

/* Sidebar numeric filters: more separation between value/range card and control. */
[data-testid="stSidebar"] .sidebar-slider-title {
    margin: 1.28rem 0 .45rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge,
[data-testid="stSidebar"] .sidebar-slider-state-modern,
[data-testid="stSidebar"] .sidebar-slider-current-state {
    margin-bottom: .72rem !important;
    padding: 11px 12px !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: 1.15rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    min-height: 42px !important;
    font-size: .92rem !important;
    font-weight: 850 !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    min-width: 36px !important;
}
[data-testid="stSidebar"] .sidebar-filter-group-title {
    margin-top: 1.25rem !important;
    margin-bottom: .70rem !important;
}

/* Keep the clear-search action close to Contexto activo, with less dead air. */
.search-clear-row {
    margin: -1.05rem 0 .70rem 1.05rem !important;
}
.search-clear-row + div[data-testid="stButton"] {
    margin-top: -1.05rem !important;
    margin-bottom: .70rem !important;
}
.search-clear-row + div[data-testid="stButton"] button {
    border-radius: 999px !important;
    border: 1px solid #93c5fd !important;
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%) !important;
    color: #1e3a8a !important;
    font-weight: 950 !important;
    min-height: 34px !important;
    padding: .34rem .86rem !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, .12) !important;
}

/* Quick guide now belongs to Contexto activo: compact, pedagogical, not top-of-page. */
div[data-testid="stExpander"] {
    margin-top: -0.25rem !important;
    margin-bottom: 22px !important;
    border: 1px solid #dbeafe !important;
    border-radius: 16px !important;
    background: #ffffff !important;
    box-shadow: 0 8px 22px rgba(15,23,42,.040) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] details > summary {
    min-height: 44px !important;
    padding: 11px 15px !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
    color: #0f2f5f !important;
    font-weight: 950 !important;
    letter-spacing: .01em !important;
}
div[data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid #e5edf7 !important;
}
div[data-testid="stExpander"] div[data-testid="stTabs"] button {
    border-radius: 999px !important;
    font-weight: 900 !important;
    color: #1e3a8a !important;
}
div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] {
    color: #334155 !important;
    font-size: .88rem !important;
    line-height: 1.45 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# Header + executive filters
# =============================================================================


# =============================================================================
# UX final correction v4: top whitespace, search hierarchy, guide action row
# =============================================================================
st.markdown(
    """
<style>
/* Remove accumulated vertical space from CSS-only markdown blocks. */
div[data-testid="stElementContainer"]:has(style),
div[data-testid="stMarkdownContainer"]:has(> style) {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}
header[data-testid="stHeader"],
[data-testid="stDecoration"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}
section.main > div,
[data-testid="stAppViewContainer"] .main .block-container,
.block-container {
    padding-top: 0.10rem !important;
    margin-top: 0 !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 16px !important;
}

/* Search: product hero card + Google-like white input with blue focus. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title),
div[data-testid="stElementContainer"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-top: 4px solid #2563eb !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 44px rgba(15, 23, 42, .07), 0 8px 24px rgba(37, 99, 235, .07) !important;
}
.final-search-title {
    color: #0b2f5f !important;
    font-size: 1.02rem !important;
    font-weight: 950 !important;
    letter-spacing: .075em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}
.final-search-caption {
    color: #475569 !important;
    font-size: .90rem !important;
    margin-bottom: 6px !important;
}
.final-search-microcopy {
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
    margin: 2px 0 12px 0 !important;
    padding: 5px 9px !important;
    border-radius: 999px !important;
    background: #eff6ff !important;
    border: 1px solid #dbeafe !important;
    color: #1e3a8a !important;
    font-size: .76rem !important;
    font-weight: 850 !important;
}
div[data-testid="stElementContainer"]:has(.final-search-title) + div[data-testid="stElementContainer"] div[data-baseweb="select"] > div,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #2563eb !important;
    border-radius: 999px !important;
    min-height: 58px !important;
    box-shadow: 0 10px 26px rgba(37, 99, 235, .11) !important;
}
div[data-testid="stElementContainer"]:has(.final-search-title) + div[data-testid="stElementContainer"] div[data-baseweb="select"] > div:hover,
div[data-testid="stElementContainer"]:has(.final-search-title) + div[data-testid="stElementContainer"] div[data-baseweb="select"] > div:focus-within,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.14), 0 14px 30px rgba(37,99,235,.13) !important;
}

/* Sidebar filters: compact card, explicit gap between range card and numeric control. */
[data-testid="stSidebar"] .sidebar-slider-title {
    margin: 1.35rem 0 .48rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-filter-value-badge,
[data-testid="stSidebar"] .sidebar-slider-current-state,
[data-testid="stSidebar"] .sidebar-slider-state-modern {
    padding: 8px 10px !important;
    margin: 0 0 .82rem 0 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-top: 0 !important;
    margin-bottom: 1.45rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
    min-height: 39px !important;
}

/* Context actions row: no overlap, no layout jump. */
.search-clear-row,
.quick-guide-action-row {
    margin-top: -0.35rem !important;
    margin-bottom: 1.05rem !important;
}
.search-clear-row + div[data-testid="stButton"] button,
.quick-guide-action-row + div[data-testid="stPopover"] button,
div[data-testid="stPopover"] button[kind="secondary"] {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    min-height: 34px !important;
    padding: .36rem .82rem !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, .08) !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Sprint 11 product polish v5: professional hierarchy and universe selector
# =============================================================================
st.markdown(
    """
<style>
/* Aggressive top whitespace removal for app and print preview. */
html, body, [data-testid="stAppViewContainer"], section.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
[data-testid="stAppViewContainer"] .main .block-container,
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
.scouting-topbar {
    margin-top: 0 !important;
    margin-bottom: 18px !important;
}
/* Search module: white card, blue details, stronger hierarchy. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #bfdbfe !important;
    border-top: 4px solid #2563eb !important;
    border-radius: 22px !important;
    padding: 18px 20px 20px 20px !important;
    box-shadow: 0 20px 50px rgba(15, 23, 42, .075), 0 8px 22px rgba(37, 99, 235, .08) !important;
}
.final-search-title {
    color: #0b2f5f !important;
    font-size: 1.08rem !important;
    font-weight: 950 !important;
    letter-spacing: .085em !important;
}
.final-search-caption {
    color: #475569 !important;
    font-size: .90rem !important;
}
.final-search-microcopy {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    border-radius: 999px !important;
    padding: 5px 10px !important;
    font-weight: 900 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 2px solid #2563eb !important;
    border-radius: 999px !important;
    min-height: 58px !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, .12) !important;
}
/* Sidebar filters: air between status card and numeric control, not inside the card. */
[data-testid="stSidebar"] .sidebar-filter-value-badge {
    padding: 8px 10px !important;
    margin-bottom: 1.02rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: 1.65rem !important;
}
[data-testid="stSidebar"] .sidebar-slider-title {
    margin-top: 1.45rem !important;
}
/* Context actions: compact and aligned. */
.search-clear-row, .quick-guide-action-row {
    margin-top: -0.65rem !important;
    margin-bottom: 1.00rem !important;
}
.search-clear-row + div[data-testid="stButton"] button,
.quick-guide-action-row + div[data-testid="stPopover"] button {
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
    color: #1e3a8a !important;
    font-weight: 950 !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, .10) !important;
}
.universe-status-chip {
    display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:6px 10px;
    background:#f8fafc;border:1px solid #e2e8f0;color:#334155;font-size:.78rem;font-weight:900;
}
.universe-status-chip--football { background:#fff7ed;border-color:#fed7aa;color:#9a3412; }
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Sprint 11 v7 product coherence and visual hierarchy fixes
# =============================================================================
st.markdown(
    """
<style>
/* Keep Streamlit toolbar accessible while preserving compact product spacing. */
header[data-testid="stHeader"] {
    display: flex !important;
    visibility: visible !important;
    height: 2.0rem !important;
    min-height: 2.0rem !important;
    background: transparent !important;
    pointer-events: auto !important;
}
[data-testid="stToolbar"], [data-testid="stToolbar"] * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stAppViewContainer"] .main .block-container,
.block-container {
    padding-top: 0.55rem !important;
    margin-top: 0 !important;
}
.scouting-topbar {
    margin-top: 0.65rem !important;
    margin-bottom: 18px !important;
}

/* Stronger, cleaner global search module. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #d7e5f7 !important;
    border-radius: 20px !important;
    padding: 18px 20px 18px 20px !important;
    box-shadow: 0 14px 34px rgba(15,23,42,.065) !important;
    margin-bottom: 22px !important;
}
.final-search-title {
    color: #0b2f5f !important;
    font-size: 1.02rem !important;
    font-weight: 950 !important;
    letter-spacing: .085em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}
.final-search-caption {
    color: #475569 !important;
    font-size: .90rem !important;
    margin-bottom: 12px !important;
}
.final-search-microcopy {
    display: inline-flex !important;
    width: fit-content !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    border-radius: 999px !important;
    padding: 5px 10px !important;
    font-size: .78rem !important;
    font-weight: 900 !important;
    margin-bottom: 10px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #93c5fd !important;
    border-radius: 16px !important;
    min-height: 58px !important;
    box-shadow: 0 8px 22px rgba(37,99,235,.075) !important;
    align-items: center !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.12), 0 12px 28px rgba(37,99,235,.10) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] span,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] input {
    font-size: 1.02rem !important;
    line-height: 1.3 !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

/* Sidebar: more space between descriptor card and numeric control, not inside the descriptor. */
[data-testid="stSidebar"] .sidebar-filter-value-badge,
[data-testid="stSidebar"] .sidebar-slider-state,
[data-testid="stSidebar"] .sidebar-slider-state-modern,
[data-testid="stSidebar"] .sidebar-slider-current-state {
    padding: 8px 10px !important;
    margin-bottom: .85rem !important;
}
[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
    margin-bottom: 1.45rem !important;
}
[data-testid="stSidebar"] .sidebar-slider-title {
    margin-top: 1.18rem !important;
}

/* Inline contextual actions inside Contexto activo. */
.context-action-row {
    display:flex;
    align-items:center;
    gap:10px;
    flex-wrap:wrap;
    margin-top: 12px;
}
.quick-guide-inline {
    border: 1px solid #bfdbfe;
    background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%);
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    box-shadow: 0 8px 18px rgba(37, 99, 235, .08);
}
.quick-guide-inline summary {
    cursor: pointer;
    list-style: none;
    padding: 8px 12px;
    color: #1e3a8a;
    font-weight: 950;
    font-size: .82rem;
}
.quick-guide-inline summary::-webkit-details-marker { display:none; }
.quick-guide-inline-body {
    padding: 10px 12px 12px 12px;
    border-top: 1px solid #dbeafe;
    background: #ffffff;
    color: #334155;
    font-size: .82rem;
    line-height: 1.4;
    max-width: 760px;
}
.quick-guide-tabs {
    display:flex; gap:6px; flex-wrap:wrap; margin-bottom:8px;
}
.quick-guide-tabs span {
    border:1px solid #dbeafe; background:#eff6ff; color:#1e3a8a; border-radius:999px; padding:4px 8px; font-weight:900; font-size:.76rem;
}
.search-clear-inline {
    display:inline-flex;
}
/* Hide old detached quick-guide popover rows if any remain from previous patches. */
.quick-guide-action-row { display:none !important; }
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 v8 final visual polish: topbar, search, guide and methodology spacing
# =============================================================================
st.markdown(
    """
<style>
/* Give the Streamlit toolbar enough room while keeping the product header near the top. */
header[data-testid="stHeader"] {
    display: flex !important;
    visibility: visible !important;
    height: 2.35rem !important;
    min-height: 2.35rem !important;
    background: transparent !important;
    pointer-events: auto !important;
}
[data-testid="stToolbar"], [data-testid="stToolbar"] * {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stAppViewContainer"] .main .block-container,
.block-container {
    padding-top: 0.85rem !important;
    margin-top: 0 !important;
}
.scouting-topbar {
    margin-top: 1.05rem !important;
    margin-bottom: 18px !important;
}

/* Search module: stronger product hierarchy and Google/CRM-like input. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title),
div[data-testid="stElementContainer"]:has(.final-search-title) {
    background: #ffffff !important;
    border: 1px solid #cfe0f6 !important;
    border-radius: 22px !important;
    padding: 18px 22px 20px 22px !important;
    box-shadow: 0 18px 42px rgba(15, 23, 42, 0.070) !important;
}
.final-search-title {
    display: flex !important;
    align-items: center !important;
    gap: 9px !important;
    color: #08275a !important;
    font-size: 1.06rem !important;
    font-weight: 950 !important;
    letter-spacing: 0.11em !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
}
.final-search-caption {
    color: #42526b !important;
    font-size: 0.91rem !important;
    line-height: 1.35 !important;
    margin-bottom: 10px !important;
}
.final-search-microcopy {
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
    max-width: 100% !important;
    padding: 6px 12px !important;
    border-radius: 999px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    font-size: 0.78rem !important;
    font-weight: 900 !important;
    margin-bottom: 14px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-testid="stSelectbox"] {
    margin-top: 0.15rem !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div {
    min-height: 62px !important;
    padding-left: 18px !important;
    padding-right: 14px !important;
    border: 2px solid #2563eb !important;
    border-radius: 999px !important;
    background: #ffffff !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.10) !important;
    align-items: center !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] > div:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14), 0 12px 30px rgba(37, 99, 235, 0.13) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] *,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] input,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] span {
    font-size: 1.02rem !important;
    line-height: 1.35 !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) div[data-baseweb="select"] svg {
    width: 20px !important;
    height: 20px !important;
    color: #0f2f5f !important;
    fill: #0f2f5f !important;
}

/* Context guide: keep it inside the active context card and make it read as an inline help module. */
.context-action-row {
    margin-top: 14px !important;
    display: flex !important;
    align-items: flex-start !important;
    gap: 12px !important;
}
.quick-guide-inline {
    width: min(540px, 100%) !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 16px !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.070) !important;
    overflow: hidden !important;
}
.quick-guide-inline summary {
    list-style: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 10px 14px !important;
    color: #1e3a8a !important;
    font-weight: 900 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
}
.quick-guide-inline-body {
    border-top: 1px solid #dbeafe !important;
    padding: 12px 14px 14px 14px !important;
    color: #334155 !important;
    font-size: 0.86rem !important;
    line-height: 1.48 !important;
}
.quick-guide-tabs {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin-bottom: 10px !important;
}
.quick-guide-tabs span {
    background: #eff6ff !important;
    color: #1e3a8a !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 999px !important;
    padding: 5px 10px !important;
    font-weight: 900 !important;
    font-size: 0.76rem !important;
}

/* Section spacing: methodology expanders should not touch their preceding cards. */
.score-methodology-spacer,
.model-drivers-expander-spacer {
    height: 16px !important;
    clear: both !important;
}
.pro-section-card {
    margin-bottom: 12px !important;
}
div[data-testid="stExpander"] {
    margin-top: 14px !important;
    margin-bottom: 22px !important;
}

/* Decision-driver blocks: more breathing room inside and between the note and expander. */
.driver-chip {
    margin-bottom: 10px !important;
}
.compact-board-note {
    margin-top: 8px !important;
    line-height: 1.5 !important;
}

/* Sidebar numeric controls: keep current spacing but avoid over-compressed filter groups. */
[data-testid="stSidebar"] .stNumberInput {
    margin-top: 0.30rem !important;
    margin-bottom: 1.25rem !important;
}
[data-testid="stSidebar"] .sidebar-filter-state,
[data-testid="stSidebar"] .sidebar-slider-state-modern {
    margin-bottom: 0.52rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)




# =============================================================================
# Sprint 11 closure hotfix: remove empty search spacer and preserve toolbar
# =============================================================================
st.markdown(
    """
<style>
/* The global search is now rendered without a bordered st.container; this final
   guard hides any empty bordered wrapper left by previous visual passes. */
div[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.final-search-title)):empty,
div[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.final-search-title)):has(> div:empty) {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
}
.scouting-topbar { margin-bottom: 20px !important; }
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 11 final closure patch: search centering, layer badges, stale lookup UX
# =============================================================================
st.markdown(
    """
<style>
/* Final search select centering. Streamlit/BaseWeb renders the selected value in nested flex wrappers. */
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    min-height: 58px !important;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stAppViewContainer"] > .main div[data-baseweb="select"] div[role="combobox"],
[data-testid="stAppViewContainer"] > .main div[data-baseweb="select"] div[role="button"],
[data-testid="stAppViewContainer"] > .main div[data-baseweb="select"] input,
[data-testid="stAppViewContainer"] > .main div[data-baseweb="select"] span {
    min-height: 58px !important;
    height: 58px !important;
    display: flex !important;
    align-items: center !important;
    line-height: 58px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
[data-testid="stAppViewContainer"] > .main div[data-baseweb="select"] svg {
    align-self: center !important;
}
/* Keep global search clean and remove accidental empty bordered wrappers. */
div[data-testid="stVerticalBlockBorderWrapper"]:empty,
div[data-testid="stElementContainer"]:empty {
    display: none !important;
}
.final-search-title {
    margin-bottom: .35rem !important;
}
.final-search-caption {
    margin-bottom: .55rem !important;
}
.final-search-microcopy {
    margin-top: .65rem !important;
}
/* Product layer labels used to explain the dashboard architecture. */
.layer-badge {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 7px 12px;
    border-radius: 999px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1e3a8a;
    font-size: .74rem;
    font-weight: 950;
    letter-spacing: .075em;
    text-transform: uppercase;
    box-shadow: 0 8px 18px rgba(15, 23, 42, .035);
    margin: 6px 0 12px 0;
}
/* Prevent layer badges from looking like default markdown pills. */
div[data-testid="stMarkdownContainer"]:has(.layer-badge) {
    margin-bottom: 0 !important;
}
/* Football Intelligence card should stay compact and separated from context. */
.outside-scouting-card {
    margin-top: 34px !important;
    margin-bottom: 22px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
/* Sprint 11 closure: robust search select vertical alignment. */
div[data-baseweb="select"] > div {
    align-items: center !important;
}
div[data-baseweb="select"] input,
div[data-baseweb="select"] div[role="button"] {
    line-height: 1.35 !important;
}
</style>
""",
    unsafe_allow_html=True,
)



st.markdown(
    """
<style>
/* Sprint 13.5 UX polish v9: keep Quick Guide as a single-line pill beside examples. */
[data-testid="stAppViewContainer"] > .main div[data-testid="stPopover"] {
    margin-top: 0 !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stPopover"] button {
    width: 128px !important;
    min-width: 128px !important;
    max-width: 128px !important;
    min-height: 30px !important;
    height: 30px !important;
    padding: 6px 11px !important;
    border-radius: 999px !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: #1e3a8a !important;
    box-shadow: 0 6px 16px rgba(37,99,235,.08) !important;
    justify-content: center !important;
    align-items: center !important;
    white-space: nowrap !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stPopover"] button p,
[data-testid="stAppViewContainer"] > .main div[data-testid="stPopover"] button span {
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    font-size: .74rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    color: #1e3a8a !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stPopover"] button svg {
    width: 13px !important;
    height: 13px !important;
    color: #2563eb !important;
    fill: #2563eb !important;
}
.final-search-examples {
    min-height: 30px !important;
    display: inline-flex !important;
    align-items: center !important;
}
/* Avoid inherited circular/vertical styling from previous quick-guide patches. */
.search-helper-inline {
    display: flex !important;
    align-items: center !important;
    min-height: 30px !important;
}
</style>
""",
    unsafe_allow_html=True,
)



# =============================================================================
# Sprint 13.5 UX polish v10: deterministic single-line Quick Guide trigger
# =============================================================================
st.markdown(
    """
<style>
/* Keep the Quick Guide trigger in the search helper row as a single-line pill. */
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] {
    margin-top: 0 !important;
    width: auto !important;
    min-width: 138px !important;
    max-width: 160px !important;
}
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button {
    width: 138px !important;
    min-width: 138px !important;
    max-width: 138px !important;
    min-height: 30px !important;
    height: 30px !important;
    padding: 5px 12px !important;
    border-radius: 999px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    box-shadow: 0 6px 16px rgba(37,99,235,.08) !important;
}
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button p,
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button span {
    display: inline !important;
    width: auto !important;
    min-width: max-content !important;
    max-width: none !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    font-size: .74rem !important;
    font-weight: 900 !important;
    color: #1e3a8a !important;
}
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button svg {
    flex: 0 0 auto !important;
    width: 12px !important;
    height: 12px !important;
}
/* Keep examples and guide visually aligned. */
.search-helper-inline,
.final-search-examples {
    min-height: 30px !important;
    height: 30px !important;
    display: inline-flex !important;
    align-items: center !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="scouting-topbar">
        <div class="scouting-brand"><span class="scouting-brand-mark">IQ</span><span>SCOUTING IQ</span></div>
        <div class="scouting-topbar-right"><span>✓ Market Value Engine</span><span>✓ Future Asset</span><span>✓ Risk Layer</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

base_df = add_executive_decision_features(scouting_df.copy())

# Search/context panels are useful in scouting pages, but they create dead space
# in Strategy and Methodology. Keep them out of those pages.
SHOW_COMMAND_PANEL = dashboard_page not in {"Transfer Strategy", "Methodology"}

# Sprint 13.5 v2: compact command row. Search and active context share the first viewport row
# only where the command/search layer is relevant.
if SHOW_COMMAND_PANEL:
    command_left_col, command_right_col = st.columns([0.52, 0.48], gap="medium")
    context_panel_placeholder = command_right_col.empty()
else:
    context_panel_placeholder = st.empty()

# Clear the global search without external navigation.
def clear_global_scouting_search() -> None:
    st.session_state["global_scouting_search"] = None

# CRM-style autocomplete search. Labels show entity type, while filtering keeps the raw value.
# Audit note: player suggestions are built from football_df, not from a hardcoded
# demo dictionary. football_df is constrained to the latest available season in
# build_football_universe_dataset() to avoid stale historical clubs in lookup.
search_options, search_label_to_raw = build_search_options(football_df)

# Search header, input and examples are rendered as a single compact product card.
current_global_search = st.session_state.get("global_scouting_search")
if current_global_search is not None and str(current_global_search) not in search_options:
    # Clear stale selections created before the latest-season Football Intelligence audit.
    st.session_state["global_scouting_search"] = None

if SHOW_COMMAND_PANEL:
    with command_left_col:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="final-search-title">{html.escape('Global scouting search' if LANG == 'EN' else 'Buscador global de scouting')}</div>
                <div class="final-search-caption">{html.escape('Search players, clubs, leagues or positions. Executive ranking remains anchored to the actionable universe.' if LANG == 'EN' else 'Busca jugadores, clubes, ligas o posiciones. El ranking ejecutivo sigue anclado al universo accionable.')}</div>
                """,
                unsafe_allow_html=True,
            )
            global_search_label = st.selectbox(
                "Search" if LANG == "EN" else "Búsqueda global",
                options=search_options,
                index=None,
                placeholder="Search player, club, league or position..." if LANG == "EN" else "Buscar jugador, club, liga o posición...",
                key="global_scouting_search",
                label_visibility="collapsed",
                help=(
                    "Suggestions are grouped by league, club, player and position."
                    if LANG == "EN"
                    else "Las sugerencias aparecen diferenciadas por liga, club, jugador y posición."
                ),
            )
            helper_left, helper_guide, helper_spacer = st.columns([0.42, 0.28, 0.30])
            with helper_left:
                st.markdown(
                    f"""
                    <div class="search-helper-inline">
                        <span class="final-search-examples">{html.escape('Examples: Bundesliga · Bayern · Yan Diomandé · MID' if LANG == 'EN' else 'Ejemplos: Bundesliga · Bayern · Yan Diomandé · MID')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with helper_guide:
                with st.popover("Quick Guide" if LANG == "EN" else "Guía rápida"):
                    st.markdown(
                        f"""
                        <div class="quick-guide-popover-body">
                            <div class="quick-guide-layout">
                                <div class="quick-guide-card">
                                    <span>{html.escape('Workflow' if LANG == 'EN' else 'Flujo')}</span>
                                    <b>{html.escape('From ranking to decision' if LANG == 'EN' else 'Del ranking a la decisión')}</b>
                                    <small>{html.escape('Use Market to detect opportunities, Players to validate profiles, Board to compare candidates and Strategy to optimise the portfolio.' if LANG == 'EN' else 'Usa Market para detectar oportunidades, Players para validar perfiles, Board para comparar candidatos y Strategy para optimizar cartera.')}</small>
                                </div>
                                <div class="quick-guide-card">
                                    <span>{html.escape('Filters' if LANG == 'EN' else 'Filtros')}</span>
                                    <b>{html.escape('Eligibility layer' if LANG == 'EN' else 'Capa de elegibilidad')}</b>
                                    <small>{html.escape('Age, minutes, confidence, opportunity, value, ROI and risk define the active scouting universe.' if LANG == 'EN' else 'Edad, minutos, confianza, oportunidad, valor, ROI y riesgo definen el universo activo de scouting.')}</small>
                                </div>
                            </div>
                            <div class="quick-guide-glossary">
                                <span>{html.escape('Glossary' if LANG == 'EN' else 'Glosario')}</span>
                                <div><b>Opportunity</b><small>{html.escape('market inefficiency and upside signal' if LANG == 'EN' else 'señal de ineficiencia y upside de mercado')}</small></div>
                                <div><b>Risk</b><small>{html.escape('estimated uncertainty; lower is better' if LANG == 'EN' else 'incertidumbre estimada; menor es mejor')}</small></div>
                                <div><b>ROI 3Y</b><small>{html.escape('expected three-year asset return' if LANG == 'EN' else 'retorno esperado del activo a tres años')}</small></div>
                                <div><b>Decision Score</b><small>{html.escape('final executive priority indicator' if LANG == 'EN' else 'indicador final de prioridad ejecutiva')}</small></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
else:
    global_search_label = None

global_search_query = "" if global_search_label is None else search_label_to_raw.get(str(global_search_label), str(global_search_label))
global_search_display = "" if global_search_label is None else str(global_search_label)


# Search can target the wider football dataset, but only Scouting Universe results
# are allowed to drive ranking, shortlist, Opportunity/Risk matrix and executive cards.
search_entity_type = ""
if global_search_display.startswith("Player ·"):
    search_entity_type = "player"
elif global_search_display.startswith("League ·"):
    search_entity_type = "league"
elif global_search_display.startswith("Club ·"):
    search_entity_type = "club"
elif global_search_display.startswith("Position ·"):
    search_entity_type = "position"

search_norm = str(global_search_query).strip().casefold()
scouting_name_col = get_player_name_column(scouting_df)
football_name_col = get_player_name_column(football_df)
search_matches_scouting_universe = False
search_is_outside_scouting_player = False
outside_football_profile = pd.DataFrame()

if search_norm and search_entity_type == "player":
    if scouting_name_col is not None and scouting_name_col in scouting_df.columns:
        scouting_names_norm = scouting_df[scouting_name_col].dropna().astype(str).str.strip().str.casefold()
        search_matches_scouting_universe = bool((scouting_names_norm == search_norm).any())
    if not search_matches_scouting_universe and football_name_col is not None and football_name_col in football_df.columns:
        outside_mask = football_df[football_name_col].fillna("").astype(str).str.strip().str.casefold() == search_norm
        outside_football_profile = football_df[outside_mask].head(1).copy()
        search_is_outside_scouting_player = not outside_football_profile.empty

PRESETS = {
    "full_exploration": {
        "label": {"ES": "Exploración completa", "EN": "Full exploration"},
        "max_age": 30,
        "min_minutes": 0,
        "min_confidence": 0,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].min())),
        "description": {
            "ES": "Visualiza toda la shortlist ejecutiva sin restricciones operativas adicionales.",
            "EN": "Shows the full executive shortlist without additional operating restrictions.",
        },
    },
    "actionable_profiles": {
        "label": {"ES": "Perfiles accionables", "EN": "Actionable profiles"},
        "max_age": 23,
        "min_minutes": 900,
        "min_confidence": 70,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].min())),
        "description": {
            "ES": "Filtro operativo recomendado: jóvenes con minutos suficientes y señal fiable.",
            "EN": "Recommended operating filter: young players with enough minutes and a reliable signal.",
        },
    },
    "elite_youngsters": {
        "label": {"ES": "Jóvenes élite", "EN": "Elite youngsters"},
        "max_age": 21,
        "min_minutes": 900,
        "min_confidence": 70,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].quantile(0.75))),
        "description": {
            "ES": "Jugadores muy jóvenes con alta señal de oportunidad.",
            "EN": "Very young players with a strong opportunity signal.",
        },
    },
    "high_upside": {
        "label": {"ES": "Alto upside", "EN": "High upside"},
        "max_age": 23,
        "min_minutes": 500,
        "min_confidence": 60,
        "min_opportunity": float(np.floor(base_df["opportunity_score"].quantile(0.85))),
        "description": {
            "ES": "Perfiles con mayor potencial relativo, aceptando algo más de riesgo.",
            "EN": "Profiles with higher relative upside, accepting slightly more risk.",
        },
    },
}

def preset_label(key: str) -> str:
    return PRESETS[key]["label"].get(LANG, PRESETS[key]["label"]["ES"])

preset_key = st.sidebar.selectbox(
    T("preset"),
    options=list(PRESETS.keys()),
    index=1,
    key="scouting_preset_key",
    format_func=preset_label,
)
preset = PRESETS[preset_key]
if universe_mode == "Football Universe":
    preset = dict(preset)
    preset["max_age"] = 35
    preset["min_minutes"] = 0
    preset["min_confidence"] = 0
    preset["min_opportunity"] = 0
selected_preset_label = T("selected_preset")
preset_description = preset["description"].get(LANG, preset["description"]["ES"])
st.sidebar.markdown(
    f"""
    <div class="sidebar-preset-card">
        <div class="sidebar-preset-eyebrow">🎯 {html.escape('Active preset' if LANG == 'EN' else 'Preset activo')}</div>
        <div class="sidebar-preset-title">{html.escape(preset_label(preset_key))}</div>
        <div class="sidebar-preset-text">{html.escape(preset_description)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
preset_name = f"{preset_key}_{universe_mode.replace(' ', '_').lower()}"

st.sidebar.markdown(
    f"<div class='sidebar-filter-group-title'>{html.escape('Sporting profile' if LANG == 'EN' else 'Perfil deportivo')}</div>",
    unsafe_allow_html=True,
)

filter_row_1 = [st.sidebar, st.sidebar, st.sidebar]
filter_row_2 = [st.sidebar, st.sidebar, st.sidebar, st.sidebar]
filter_row_3 = [st.sidebar, st.sidebar, st.sidebar]

with filter_row_1[0]:
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('max_age'))}</div>", unsafe_allow_html=True)
    max_age_key = f"max_age_{preset_name}"
    age_min_limit = 16 if universe_mode == "Football Universe" else 18
    age_max_limit = 35 if universe_mode == "Football Universe" else 30
    max_age_default = int(preset["max_age"])
    max_age_preview = int(st.session_state.get(max_age_key, max_age_default))
    render_sidebar_filter_value(max_age_preview, " years" if LANG == "EN" else " años", age_min_limit, age_max_limit)
    max_age = st.number_input(
        T("max_age"),
        min_value=age_min_limit,
        max_value=age_max_limit,
        value=max_age_default,
        step=1,
        key=max_age_key,
        label_visibility="collapsed",
    )
with filter_row_1[1]:
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('min_minutes'))}</div>", unsafe_allow_html=True)
    min_minutes_key = f"min_minutes_{preset_name}"
    min_minutes_default = int(preset["min_minutes"])
    min_minutes_preview = int(st.session_state.get(min_minutes_key, min_minutes_default))
    render_sidebar_filter_value(min_minutes_preview, "", 0, 3000)
    min_minutes = st.number_input(
        T("min_minutes"),
        min_value=0,
        max_value=3000,
        value=min_minutes_default,
        step=100,
        key=min_minutes_key,
        label_visibility="collapsed",
    )
with filter_row_1[2]:
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('min_confidence'))}</div>", unsafe_allow_html=True)
    min_confidence_key = f"min_confidence_{preset_name}"
    min_confidence_default = int(preset["min_confidence"])
    min_confidence_preview = int(st.session_state.get(min_confidence_key, min_confidence_default))
    render_sidebar_filter_value(min_confidence_preview, "", 0, 100)
    min_confidence = st.number_input(
        T("min_confidence"),
        min_value=0,
        max_value=100,
        value=min_confidence_default,
        step=5,
        key=min_confidence_key,
        label_visibility="collapsed",
    )

st.sidebar.markdown(
    f"<div class='sidebar-filter-group-title'>{html.escape('Competitive context' if LANG == 'EN' else 'Contexto competitivo')}</div>",
    unsafe_allow_html=True,
)

with filter_row_2[0]:
    raw_leagues = sorted(base_df["league"].dropna().astype(str).unique().tolist())
    league_display_to_raw = {league_display_name(league): league for league in raw_leagues}
    league_options = [T("all_f")] + list(league_display_to_raw.keys())
    selected_league_display = st.selectbox(T("league"), league_options, key=f"league_{preset_name}")
    selected_league = league_display_to_raw.get(selected_league_display, selected_league_display)
with filter_row_2[1]:
    position_options = [T("all_f")] + sorted(base_df["position_group"].dropna().astype(str).unique().tolist())
    selected_position = st.selectbox(T("position"), position_options, key=f"position_{preset_name}")
with filter_row_2[2]:
    raw_tiers = sorted(base_df["opportunity_tier_label"].dropna().astype(str).unique().tolist())
    tier_display_to_raw = {tier_display_name(tier): tier for tier in raw_tiers}
    tier_options = [T("all_m")] + list(tier_display_to_raw.keys())
    selected_tier_display = st.selectbox(T("tier"), tier_options, key=f"tier_{preset_name}")
    selected_tier = tier_display_to_raw.get(selected_tier_display, selected_tier_display)
with filter_row_2[3]:
    global_min_os = float(np.floor(base_df["opportunity_score"].min()))
    global_max_os = float(np.ceil(base_df["opportunity_score"].max()))
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('opportunity_range'))}</div>", unsafe_allow_html=True)
    os_min_key = f"opportunity_min_{preset_name}"
    os_max_key = f"opportunity_max_{preset_name}"
    os_min_default = float(preset["min_opportunity"])
    os_max_default = global_max_os
    os_min_preview = float(st.session_state.get(os_min_key, os_min_default))
    os_max_preview = float(st.session_state.get(os_max_key, os_max_default))
    render_sidebar_filter_range(os_min_preview, os_max_preview, global_min_os, global_max_os)
    os_cols = st.columns(2, gap="medium")
    with os_cols[0]:
        os_min_value = st.number_input(
            "Min",
            min_value=global_min_os,
            max_value=global_max_os,
            value=os_min_default,
            step=1.0,
            key=os_min_key,
            label_visibility="collapsed",
        )
    with os_cols[1]:
        os_max_value = st.number_input(
            "Max",
            min_value=global_min_os,
            max_value=global_max_os,
            value=os_max_default,
            step=1.0,
            key=os_max_key,
            label_visibility="collapsed",
        )
    os_low, os_high = sorted((float(os_min_value), float(os_max_value)))
    os_range = (os_low, os_high)

st.sidebar.markdown(
    f"<div class='sidebar-filter-group-title'>{html.escape('Market and risk' if LANG == 'EN' else 'Mercado y riesgo')}</div>",
    unsafe_allow_html=True,
)

with filter_row_3[0]:
    global_max_value_m = float(np.ceil(pd.to_numeric(base_df.get("market_value_eur", 0), errors="coerce").max() / 1_000_000))
    max_value_limit_m = max(1.0, global_max_value_m)
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('max_value'))}</div>", unsafe_allow_html=True)
    max_value_key = f"max_value_{preset_name}"
    max_value_preview = float(st.session_state.get(max_value_key, max_value_limit_m))
    render_sidebar_filter_value(max_value_preview, "M", 0.5, max_value_limit_m)
    max_market_value_m = st.number_input(
        T("max_value"),
        min_value=0.5,
        max_value=max_value_limit_m,
        value=max_value_limit_m,
        step=0.5,
        key=max_value_key,
        label_visibility="collapsed",
    )
with filter_row_3[1]:
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('min_roi'))}</div>", unsafe_allow_html=True)
    min_roi_key = f"min_roi_{preset_name}"
    min_roi_preview = int(st.session_state.get(min_roi_key, 0))
    render_sidebar_filter_value(min_roi_preview, "%", 0, 400)
    min_roi = st.number_input(
        T("min_roi"),
        min_value=0,
        max_value=400,
        value=0,
        step=25,
        key=min_roi_key,
        label_visibility="collapsed",
    )
with filter_row_3[2]:
    st.markdown(f"<div class='sidebar-slider-title'>{html.escape(T('max_risk'))}</div>", unsafe_allow_html=True)
    max_risk_key = f"max_risk_{preset_name}"
    max_risk_preview = int(st.session_state.get(max_risk_key, 100))
    render_sidebar_filter_value(max_risk_preview, "", 0, 100)
    max_risk_filter = st.number_input(
        T("max_risk"),
        min_value=0,
        max_value=100,
        value=100,
        step=5,
        key=max_risk_key,
        label_visibility="collapsed",
    )

filtered_df = base_df.copy()
age_filter = pd.to_numeric(filtered_df.get("age", np.nan), errors="coerce") <= max_age
minutes_filter = pd.to_numeric(filtered_df.get("minutes_played", 0), errors="coerce").fillna(0) >= min_minutes
confidence_filter = pd.to_numeric(filtered_df.get("confidence_score", 0), errors="coerce").fillna(0) >= min_confidence
opportunity_filter = pd.to_numeric(filtered_df.get("opportunity_score", 0), errors="coerce").fillna(0).between(os_range[0], os_range[1])
value_filter = pd.to_numeric(filtered_df.get("market_value_eur", 0), errors="coerce").fillna(0) <= max_market_value_m * 1_000_000
roi_filter = pd.to_numeric(filtered_df.get("asset_roi_3y_pct", 0), errors="coerce").fillna(0) >= min_roi
risk_filter = pd.to_numeric(filtered_df.get("risk_score", 100), errors="coerce").fillna(100) <= max_risk_filter
filtered_df = filtered_df[
    age_filter
    & minutes_filter
    & confidence_filter
    & opportunity_filter
    & value_filter
    & roi_filter
    & risk_filter
].copy()

if selected_league != T("all_f"):
    filtered_df = filtered_df[filtered_df["league"].astype(str) == selected_league]
if selected_position != T("all_f"):
    filtered_df = filtered_df[filtered_df["position_group"].astype(str) == selected_position]
if selected_tier != T("all_m"):
    filtered_df = filtered_df[filtered_df["opportunity_tier_label"].astype(str) == selected_tier]

search_query_clean = str(global_search_query).strip().lower()
if search_query_clean and not search_is_outside_scouting_player and not (search_entity_type == "player"):
    searchable_cols = [
        col for col in ["player_name_fbref", "player_name_tm", "player_name", "club", "league", "position_group"]
        if col in filtered_df.columns
    ]
    if searchable_cols:
        search_mask = filtered_df[searchable_cols].astype(str).apply(
            lambda row: search_query_clean in " ".join(row.values).lower(),
            axis=1,
        )
        filtered_df = filtered_df[search_mask].copy()

# If a selected player exists in the model universe but falls outside the active filters,
# preserve the scouting ranking and explain the exclusion instead of collapsing the dashboard.
search_is_outside_active_filters = False
outside_active_profile = pd.DataFrame()
if search_query_clean and search_entity_type == "player" and not search_is_outside_scouting_player:
    player_col = get_player_name_column(base_df)
    if player_col is not None and player_col in base_df.columns:
        base_player_mask = base_df[player_col].fillna("").astype(str).str.strip().str.casefold() == search_norm
        active_player_mask = filtered_df[player_col].fillna("").astype(str).str.strip().str.casefold() == search_norm if player_col in filtered_df.columns else pd.Series(False, index=filtered_df.index)
        if bool(base_player_mask.any()) and not bool(active_player_mask.any()):
            search_is_outside_active_filters = True
            outside_active_profile = base_df[base_player_mask].head(1).copy()

# If the selected player is inside the active criteria, focus the dashboard on that profile.
if search_query_clean and search_entity_type == "player" and not search_is_outside_scouting_player and not search_is_outside_active_filters:
    player_col = get_player_name_column(filtered_df)
    if player_col is not None and player_col in filtered_df.columns:
        active_player_mask = filtered_df[player_col].fillna("").astype(str).str.strip().str.casefold() == search_norm
        if bool(active_player_mask.any()):
            filtered_df = filtered_df[active_player_mask].copy()

filtered_df = filtered_df.sort_values("executive_decision_score_v2" if "executive_decision_score_v2" in filtered_df.columns else "opportunity_score", ascending=False).reset_index(drop=True)

shortlist_universe = len(base_df)
filtered_universe = len(filtered_df)
filtered_pct_shortlist = filtered_universe / shortlist_universe if shortlist_universe > 0 else 0

st.sidebar.markdown(
    f"""
    <div class="sidebar-footer">
        <b>{filtered_universe:,}</b> {html.escape(UI("jugadores encontrados"))}<br>
        {html.escape("Football Universe" if universe_mode == "Football Universe" else UI("Universo modelado"))}: {len(base_df):,}<br>
        {html.escape(UI("Actualizado con filtros activos"))}
    </div>
    """,
    unsafe_allow_html=True,
)

if LANG == "EN":
    active_filters = [
        f"Age ≤ {max_age}",
        f"Minutes ≥ {min_minutes:,}",
        f"Confidence ≥ {min_confidence}",
        f"Opportunity {os_range[0]:.0f}–{os_range[1]:.0f}",
        f"Value ≤ €{max_market_value_m:.1f}M",
        f"ROI 3Y ≥ {min_roi}%",
        f"Risk ≤ {max_risk_filter}",
    ]
else:
    active_filters = [
        f"Edad ≤ {max_age}",
        f"Minutos ≥ {min_minutes:,}",
        f"Confidence ≥ {min_confidence}",
        f"Opportunity {os_range[0]:.0f}–{os_range[1]:.0f}",
        f"Valor ≤ €{max_market_value_m:.1f}M",
        f"ROI 3Y ≥ {min_roi}%",
        f"Risk ≤ {max_risk_filter}",
    ]
search_matches_selected_league = (
    selected_league != T("all_f")
    and search_query_clean
    and str(global_search_query).strip().casefold() == str(selected_league).strip().casefold()
)

if selected_league != T("all_f") and not search_matches_selected_league:
    active_filters.append(f"{T('league')}: {league_display_name(selected_league)}")
if selected_position != T("all_f"):
    active_filters.append(f"{T('position')}: {selected_position}")
if selected_tier != T("all_m"):
    active_filters.append(f"{T('tier')}: {tier_display_name(selected_tier)}")

# Search is shown as a visual chip. Clearing uses a Streamlit callback,
# avoiding external navigation, query params and session_state mutation after widget instantiation.
context_chip_items = []
if search_query_clean:
    search_chip_label = str(global_search_query)
    search_chip_prefix = "Search"
    if search_is_outside_scouting_player:
        search_chip_prefix = "Info"
        search_chip_label = ("Informative profile: " if LANG == "EN" else "Perfil informativo: ") + search_chip_label
    context_chip_items.append(
        f"<span class='context-chip context-chip-search'>{search_chip_prefix} {html.escape(search_chip_label)}</span>"
    )
for item in active_filters:
    item_text = str(item)
    context_chip_items.append(
        f"<span class='context-chip context-chip-neutral'>{html.escape(item_text)}</span>"
    )
context_chips = "".join(context_chip_items)
if SHOW_COMMAND_PANEL:
    with context_panel_placeholder.container():
        st.markdown(
            f"""
<div class="context-strip-v2 compact-context-panel">
    <div class="context-strip-title">{html.escape(UI("Contexto activo"))}</div>
    <div class="context-strip-main">
        <div class="context-current-kpi">
            <div class="context-current-value">{filtered_universe:,}</div>
            <div class="context-current-label">{html.escape(UI("Candidatos actuales"))}</div>
        </div>
        <div class="context-secondary-kpis">
            <span class="context-chip">{html.escape(UI("Universo modelado"))} · {len(base_df):,}</span>
            <span class="context-chip">{html.escape(UI("Shortlist ejecutiva"))} · {shortlist_universe:,}</span>
            <span class="context-chip context-chip-neutral">{filtered_pct_shortlist:.0%} {html.escape(UI("de la shortlist"))}</span>
        </div>
    </div>
    <div class="context-chip-row">{context_chips}</div>
</div>
""",
            unsafe_allow_html=True,
        )


if SHOW_COMMAND_PANEL and search_is_outside_scouting_player and not outside_football_profile.empty:
    outside_row = outside_football_profile.iloc[0]
    outside_name = html.escape(str(get_player_name(outside_row)))
    outside_club = html.escape(str(safe_get(outside_row, "club", "N/A")))
    outside_league = html.escape(league_display_name(safe_get(outside_row, "league", "N/A")))
    outside_position = html.escape(str(safe_get(outside_row, "position_group", "N/A")))
    outside_age_text = format_age_metadata(outside_row, LANG)
    outside_value = format_money_short(safe_get(outside_row, "market_value_eur", np.nan))
    outside_projected_value = format_money_short(safe_get(outside_row, "projected_market_value_3y_eur", np.nan))
    outside_upside_3y = format_signed_money_short(safe_get(outside_row, "asset_upside_3y_eur", np.nan))
    outside_roi_3y = get_numeric_value(outside_row, "asset_roi_3y_pct", np.nan)
    outside_future_asset = get_numeric_value(outside_row, "future_asset_score", np.nan)
    outside_metrics = []
    if outside_projected_value != "N/A":
        outside_metrics.append(("Projected 3Y value" if LANG == "EN" else "Valor proyectado 3Y", outside_projected_value, ""))
    if outside_upside_3y != "N/A":
        outside_metrics.append(("3Y upside" if LANG == "EN" else "Upside 3Y", outside_upside_3y, ""))
    if pd.notna(outside_roi_3y):
        roi_caption = outside_upside_3y if outside_upside_3y != "N/A" else ""
        outside_metrics.append(("ROI 3Y", f"{outside_roi_3y:.0f}%", roi_caption))
    if pd.notna(outside_future_asset):
        outside_metrics.append(("Future Asset", f"{outside_future_asset:.1f} / 100", ""))
    outside_metrics_html = ""
    if outside_metrics:
        outside_metrics_html = "<div class='outside-scouting-metrics'>" + "".join(
            f"<div><span>{html.escape(label)}</span><b>{html.escape(value)}</b>{('<small>' + html.escape(caption) + '</small>') if caption else ''}</div>" for label, value, caption in outside_metrics[:4]
        ) + "</div>"
    outside_title = "Player found outside the scouting universe" if LANG == "EN" else "Jugador encontrado fuera del universo de scouting"
    outside_text = (
        "The system has historical football information for this player, but he is not part of the opportunity universe defined for this version. Ranking, shortlist, Opportunity/Risk matrix and executive recommendations remain based on the Scouting Universe."
        if LANG == "EN"
        else "El sistema dispone de información histórica de este jugador, pero no forma parte del universo de oportunidades definido para esta versión. Ranking, shortlist, matriz Opportunity/Risk y recomendaciones ejecutivas se mantienen sobre el Scouting Universe."
    )
    st.markdown(
        f"""
<div class="outside-scouting-card outside-scouting-card-v3">
    <div class="outside-scouting-main">
        <div>
            <div class="outside-scouting-eyebrow">Football Intelligence Layer</div>
            <div class="outside-scouting-title">{outside_title}</div>
            <div class="outside-scouting-player">{outside_name}</div>
            <div class="outside-scouting-meta">{" · ".join([part for part in [outside_position, outside_club, outside_league, outside_age_text, outside_value] if str(part).strip() and str(part).strip() != "N/A"])}</div>
        </div>
        {outside_metrics_html}
    </div>
    <div class="outside-scouting-text">{html.escape(outside_text)}</div>
    <div class="outside-scouting-cta">{'Informative profile' if LANG == 'EN' else 'Perfil informativo'} · {'ranking unchanged' if LANG == 'EN' else 'ranking sin alterar'}</div>
</div>
""",
        unsafe_allow_html=True,
    )


if SHOW_COMMAND_PANEL and search_is_outside_active_filters and not outside_active_profile.empty:
    outside_row = outside_active_profile.iloc[0]
    outside_name = html.escape(str(get_player_name(outside_row)))
    outside_club = html.escape(str(safe_get(outside_row, "club", "N/A")))
    outside_league = html.escape(league_display_name(safe_get(outside_row, "league", "N/A")))
    outside_position = html.escape(str(safe_get(outside_row, "position_group", "N/A")))
    outside_age_text = format_age_metadata(outside_row, LANG)
    outside_value = format_money_short(safe_get(outside_row, "market_value_eur", np.nan))
    title = "Player outside active scouting criteria" if LANG == "EN" else "Jugador fuera de los criterios activos de scouting"
    text_msg = (
        "The player exists in the analytical model universe, but does not enter the current active preset or filter set. The executive ranking, shortlist and Opportunity/Risk matrix remain based on the active Scouting Universe."
        if LANG == "EN"
        else "El jugador existe en el universo analítico del modelo, pero no entra en el preset o conjunto de filtros activo. El ranking ejecutivo, la shortlist y la matriz Opportunity/Risk se mantienen sobre el Scouting Universe activo."
    )
    st.markdown(
        f"""
<div class="outside-scouting-card">
    <div class="outside-scouting-eyebrow">Scouting Universe · Eligibility Layer</div>
    <div class="outside-scouting-title">{title}</div>
    <div class="outside-scouting-player">{outside_name}</div>
    <div class="outside-scouting-meta">{" · ".join([part for part in [outside_position, outside_club, outside_league, outside_age_text, outside_value] if str(part).strip() and str(part).strip() != "N/A"])}</div>
    <div class="outside-scouting-text">{html.escape(text_msg)}</div>
    <div class="outside-scouting-cta">{'Review filters or preset' if LANG == 'EN' else 'Revisar filtros o preset'} · {'outside active criteria' if LANG == 'EN' else 'fuera de criterios activos'}</div>
</div>
""",
        unsafe_allow_html=True,
    )

# Contextual actions: clear search without detached guide duplication.
if SHOW_COMMAND_PANEL and search_query_clean:
    clear_col, _spacer_col = st.columns([0.16, 0.84])
    with clear_col:
        st.markdown('<div class="search-clear-row">', unsafe_allow_html=True)
        st.button(
            "Clear search" if LANG == "EN" else "Limpiar búsqueda",
            key="clear_global_scouting_search_button",
            on_click=clear_global_scouting_search,
        )
        st.markdown('</div>', unsafe_allow_html=True)


st.markdown('\n<style>\n.pro-section-card .compact-board-note { margin-top: 14px !important; }\n.pro-section-card + div[data-testid="stExpander"] { margin-top: 14px !important; }\n</style>\n', unsafe_allow_html=True)

# =============================================================================
# Sprint 13.5 UX Architecture Refactor: multipanel product navigation
# =============================================================================

st.markdown(
    """
<style>
/* Sprint 13.5: product hierarchy, compact global controls and premium module pages. */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.48rem !important;
}
[data-testid="stSidebar"] .stRadio label {
    border-radius: 10px !important;
    padding: 4px 8px !important;
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(191,219,254,0.08) !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(37,99,235,0.23) !important;
    border-color: rgba(147,197,253,0.38) !important;
    box-shadow: inset 3px 0 0 #ef4444 !important;
}
[data-testid="stSidebar"] h3 {
    font-size: .74rem !important;
    letter-spacing: .09em !important;
    text-transform: uppercase !important;
    color: #93b4d8 !important;
    margin-bottom: .6rem !important;
}
.final-search-shell {
    display: grid !important;
    grid-template-columns: minmax(260px, .42fr) minmax(420px, .58fr) !important;
    gap: 18px !important;
    align-items: center !important;
    background: #ffffff !important;
    border: 1px solid #d8e7fa !important;
    border-radius: 18px !important;
    padding: 14px 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 10px 26px rgba(15,23,42,.045) !important;
}
.final-search-shell .final-search-title {
    margin: 0 0 3px 0 !important;
    font-size: .88rem !important;
    letter-spacing: .08em !important;
    color: #08275a !important;
    font-weight: 950 !important;
    text-transform: uppercase !important;
}
.final-search-shell .final-search-caption {
    margin: 0 !important;
    color: #64748b !important;
    font-size: .80rem !important;
    line-height: 1.32 !important;
}
.final-search-examples {
    margin: 4px 0 12px 0 !important;
    padding: 5px 10px !important;
    font-size: .74rem !important;
}
.context-strip-v2 {
    padding: 10px 12px !important;
    margin: 10px 0 18px 0 !important;
    border-radius: 14px !important;
}
.context-strip-main {
    gap: 14px !important;
    align-items: center !important;
}
.context-current-value {
    font-size: 1.85rem !important;
}
.context-current-label {
    font-size: .72rem !important;
}
.context-chip {
    padding: 5px 8px !important;
    font-size: .72rem !important;
}
.context-action-row {
    margin-top: 8px !important;
}
.quick-guide-inline {
    max-width: 520px !important;
}
.product-page-hero {
    background: linear-gradient(135deg, #ffffff 0%, #f7fbff 100%);
    border: 1px solid #dbeafe;
    border-left: 5px solid #2563eb;
    border-radius: 20px;
    padding: 18px 20px;
    margin: 0 0 18px 0;
    box-shadow: 0 14px 34px rgba(15,23,42,.055);
}
.product-page-eyebrow {
    color: #1d4ed8;
    font-size: .72rem;
    font-weight: 950;
    letter-spacing: .095em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.product-page-title {
    color: #0f172a;
    font-size: 1.68rem;
    line-height: 1.05;
    font-weight: 950;
    margin-bottom: 7px;
}
.product-page-subtitle {
    color: #64748b;
    font-size: .92rem;
    line-height: 1.42;
}
.home-hero {
    display: grid;
    grid-template-columns: 1.35fr .9fr;
    gap: 16px;
    align-items: stretch;
    background: linear-gradient(135deg, #06152a 0%, #0b2a55 58%, #134b8f 100%);
    border: 1px solid rgba(191,219,254,.28);
    border-radius: 22px;
    padding: 22px 24px;
    box-shadow: 0 22px 48px rgba(2,6,23,.18);
    margin-bottom: 18px;
    color: white;
}
.home-hero-title {
    font-size: 2.05rem;
    line-height: 1.04;
    font-weight: 950;
    letter-spacing: -.035em;
    margin-bottom: 8px;
}
.home-hero-subtitle {
    color: #dbeafe;
    font-size: .96rem;
    line-height: 1.45;
    max-width: 780px;
}
.home-hero-kpis {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 10px;
}
.home-hero-kpi {
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(226,232,240,.18);
    border-radius: 14px;
    padding: 12px 13px;
}
.home-hero-kpi span {
    display: block;
    color: #bfdbfe;
    font-size: .70rem;
    text-transform: uppercase;
    letter-spacing: .06em;
    font-weight: 900;
    margin-bottom: 5px;
}
.home-hero-kpi b {
    display: block;
    color: #ffffff;
    font-size: 1.45rem;
    font-weight: 950;
    line-height: 1;
}
.quick-action-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 14px;
    margin: 10px 0 18px 0;
}
.quick-action-card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-left: 4px solid #2563eb;
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 10px 24px rgba(15,23,42,.045);
}
.quick-action-title {
    color:#0f172a;
    font-size:.98rem;
    font-weight:950;
    margin-bottom:4px;
}
.quick-action-text {
    color:#64748b;
    font-size:.80rem;
    line-height:1.35;
}
.strategy-banner {
    background: linear-gradient(135deg, #06152a 0%, #0b2a55 62%, #1d4ed8 100%);
    color: #ffffff;
    border-radius: 22px;
    padding: 24px 26px;
    box-shadow: 0 24px 52px rgba(2,6,23,.20);
    margin-bottom: 18px;
    border: 1px solid rgba(191,219,254,.30);
}
.strategy-eyebrow {
    color:#bfdbfe;
    text-transform:uppercase;
    letter-spacing:.095em;
    font-size:.72rem;
    font-weight:950;
    margin-bottom:7px;
}
.strategy-title {
    font-size:1.85rem;
    font-weight:950;
    line-height:1.08;
    margin-bottom:8px;
}
.strategy-copy {
    color:#dbeafe;
    font-size:.93rem;
    line-height:1.43;
    max-width:860px;
}
.strategy-disabled-note {
    background:#ffffff;
    border:1px solid #dbeafe;
    border-radius:16px;
    padding:14px 16px;
    color:#334155;
    box-shadow:0 10px 24px rgba(15,23,42,.045);
}
.methodology-grid {
    display:grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap:12px;
    margin-bottom:14px;
}
.methodology-grid-3 {
    display:grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap:12px;
    margin-bottom:14px;
}
@media (max-width: 1200px) {
    .home-hero, .final-search-shell { grid-template-columns: 1fr !important; }
    .home-hero-kpis, .quick-action-grid, .methodology-grid, .methodology-grid-3 { grid-template-columns: 1fr !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<style>
/* Sprint 13.5 v2 polish: professional sidebar, compact command row and cleaner home cards. */
.sidebar-inline-label {
    color:#dbeafe;
    font-size:.80rem;
    font-weight:900;
    line-height:34px;
}
[data-testid="stSidebar"] [role="radiogroup"] { gap:.35rem !important; }
[data-testid="stSidebar"] .stRadio label {
    min-height: 31px !important;
    padding: 4px 10px !important;
    border-radius: 9px !important;
}
[data-testid="stSidebar"] .stRadio label p {
    font-size:.86rem !important;
    font-weight:850 !important;
}
[data-testid="stSidebar"] h3 {
    margin-top:.55rem !important;
    margin-bottom:.45rem !important;
}
[data-testid="stSidebar"] .sidebar-filter-group-title,
[data-testid="stSidebar"] .sidebar-slider-title {
    font-size:.76rem !important;
}
.final-search-examples {
    display:inline-flex !important;
    width:fit-content !important;
    margin-top: 9px !important;
}
.compact-context-panel {
    margin: 0 0 16px 0 !important;
    min-height: 202px !important;
    padding: 14px 15px !important;
}
.compact-context-panel .context-strip-main {
    display:grid !important;
    grid-template-columns: .28fr .72fr !important;
}
.compact-context-panel .context-chip-row {
    margin-top: 8px !important;
    max-height: 54px !important;
    overflow: hidden !important;
}
.compact-context-panel .quick-guide-inline { max-width: 100% !important; }
.home-hero {
    gap: 20px !important;
    margin-top: 2px !important;
}
.home-hero-kpis { gap: 14px !important; }
.home-hero-kpi {
    padding: 16px 16px !important;
    min-height: 96px !important;
}
.metric-card { margin-bottom: 8px !important; }
.product-page-title { font-size: 1.52rem !important; }
.layer-badge {
    display:inline-flex;
    align-items:center;
    width:fit-content;
    border:1px solid #bfdbfe;
    background:#eff6ff;
    color:#1e3a8a;
    border-radius:999px;
    padding:6px 11px;
    font-size:.72rem;
    font-weight:950;
    letter-spacing:.075em;
    text-transform:uppercase;
    margin: 0 0 14px 0;
}
.recruitment-compact-note {
    background:#ffffff;
    border:1px solid #dbeafe;
    border-radius:16px;
    padding:12px 14px;
    box-shadow:0 8px 20px rgba(15,23,42,.035);
    color:#334155;
    margin-bottom:14px;
}
@media (max-width: 1300px) {
    .compact-context-panel { min-height: auto !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


def render_product_page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div class="product-page-hero">
    <div class="product-page-eyebrow">{html.escape(eyebrow)}</div>
    <div class="product-page-title">{html.escape(title)}</div>
    <div class="product-page-subtitle">{html.escape(subtitle)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_layer_badge(label: str) -> None:
    """Render a compact layer label used to segment product modules."""
    st.markdown(f"<div class='layer-badge'>{html.escape(str(label))}</div>", unsafe_allow_html=True)


def build_ranked_table_df(source_df: pd.DataFrame) -> pd.DataFrame:
    table = source_df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)
    if not table.empty:
        table["dashboard_tier"] = table["opportunity_tier_label"]
        table.loc[table.head(5).index, "dashboard_tier"] = "Alta prioridad"
    else:
        table["dashboard_tier"] = []
    return table


def get_metric_leader(source_df: pd.DataFrame, col: str, ascending: bool = False) -> pd.Series | None:
    if source_df.empty or col not in source_df.columns:
        return None
    tmp = source_df.copy()
    tmp["_leader_value"] = pd.to_numeric(tmp[col], errors="coerce")
    tmp = tmp.dropna(subset=["_leader_value"])
    if tmp.empty:
        return None
    return tmp.sort_values("_leader_value", ascending=ascending).iloc[0]


def render_findings_cards(source_df: pd.DataFrame) -> None:
    if source_df.empty:
        return
    specs = [
        ("MEJOR OPORTUNIDAD", "Best opportunity", get_metric_leader(source_df, "executive_decision_score_v2"), "Decision", "executive_decision_score_v2"),
        ("MEJOR ACTIVO DE VALOR", "Best value asset", get_metric_leader(source_df, "future_asset_score"), "Future Asset", "future_asset_score"),
        ("OPORTUNIDAD DE MENOR RIESGO", "Lowest-risk opportunity", get_metric_leader(source_df, "risk_score", ascending=True), "Risk", "risk_score"),
        ("MAYOR POTENCIAL DE CRECIMIENTO", "Highest growth potential", get_metric_leader(source_df, "growth_score"), "Growth", "growth_score"),
    ]
    cols = st.columns(4)
    for col_obj, (label_es, label_en, row, metric_label, metric_col) in zip(cols, specs):
        with col_obj:
            if row is None:
                render_metric_card_with_caption(label_en if LANG == "EN" else label_es, "N/A", "")
                continue
            name = get_player_name(row)
            meta = f"{safe_get(row, 'position_group', 'N/A')} · {safe_get(row, 'club', 'N/A')} · {league_display_name(safe_get(row, 'league', 'N/A'))}"
            value = get_numeric_value(row, metric_col, np.nan)
            st.markdown(
                f"""
<div class="scouting-hero-card" style="min-height:132px;">
    <div class="metric-label">{html.escape(label_en if LANG == 'EN' else label_es)}</div>
    <div style="font-size:1.05rem;font-weight:950;color:#0f172a;line-height:1.16;">{html.escape(str(name))}</div>
    <div style="color:#64748b;font-size:.76rem;line-height:1.25;margin-top:5px;">{html.escape(str(meta))}</div>
    <div style="display:flex;justify-content:space-between;align-items:end;border-top:1px solid #edf2f7;margin-top:12px;padding-top:9px;">
        <span style="color:#64748b;font-size:.74rem;font-weight:800;">{html.escape(metric_label)}</span>
        <b style="color:#166534;font-size:1.02rem;">{value:.1f}</b>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )



def render_info_kpi_card(label: str, value: str, caption: str, info_text: str) -> None:
    """Render a compact KPI card with a native HTML details info control."""
    st.markdown(
        f"""
<div class="metric-card metric-card-info">
    <div class="metric-label metric-label-with-info">
        <span>{html.escape(str(label))}</span>
        <details class="metric-info-details">
            <summary>i</summary>
            <div>{html.escape(str(info_text))}</div>
        </details>
    </div>
    <div class="metric-value">{html.escape(str(value))}</div>
    <div class="helper-caption">{html.escape(str(caption))}</div>
</div>
""",
        unsafe_allow_html=True,
    )

def render_executive_overview_page(source_df: pd.DataFrame) -> None:
    precision_value = "N/A"
    if not precision.empty and "precision_at_k" in precision.columns:
        precision_value = f"{precision['precision_at_k'].max():.0%}"
    roi_value = "N/A"
    if not roi.empty and "positive_roi_rate" in roi.columns:
        roi_value = f"{roi['positive_roi_rate'].iloc[0]:.0%}"
    leagues = source_df["league"].nunique() if "league" in source_df.columns else "N/A"
    st.markdown(
        f"""
<div class="home-hero">
    <div>
        <div class="product-page-eyebrow" style="color:#bfdbfe;">Executive Overview</div>
        <div class="home-hero-title">Football Recruitment Intelligence Platform</div>
        <div class="home-hero-subtitle">{html.escape('Compact executive landing for market opportunities, risk-adjusted targets and the strategic scouting workflow.' if LANG == 'EN' else 'Landing ejecutiva compacta para oportunidades de mercado, targets ajustados por riesgo y flujo estratégico de scouting.')}</div>
    </div>
    <div class="home-hero-kpis">
        <div class="home-hero-kpi"><span>{html.escape('Current candidates' if LANG == 'EN' else 'Candidatos actuales')}</span><b>{len(source_df):,}</b></div>
        <div class="home-hero-kpi"><span>{html.escape('Leagues' if LANG == 'EN' else 'Ligas')}</span><b>{leagues}</b></div>
        <div class="home-hero-kpi"><span>Precision@K</span><b>{precision_value}</b></div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        render_metric_card_with_caption(UI("Candidatos actuales"), f"{len(source_df):,}", f"{filtered_pct_shortlist:.0%} {UI('de la shortlist')}")
    with k2:
        render_metric_card_with_caption(UI("Shortlist ejecutiva"), f"{shortlist_universe:,}", UI("jugadores precandidatos"))
    with k3:
        render_metric_card_with_caption(UI("Ligas representadas"), leagues, UI("cobertura competitiva"))
    with k4:
        render_info_kpi_card(
            "Precision@K",
            precision_value,
            UI("calidad del ranking"),
            "Proporción de recomendaciones correctas dentro del Top-K del ranking. En el dashboard se usa como métrica de calidad ejecutiva del orden de candidatos." if LANG == "ES" else "Share of correct recommendations within the Top-K ranking. Used as an executive quality metric for candidate ordering.",
        )
    with k5:
        render_info_kpi_card(
            "Positive ROI Rate",
            roi_value,
            UI("simulación conservadora"),
            "Porcentaje de candidatos que muestran revalorización positiva bajo la simulación histórica de ROI. No equivale a beneficio garantizado ni a precio real de transferencia." if LANG == "ES" else "Share of candidates with positive revaluation under the historical ROI simulation. It is not a guaranteed profit or real transfer fee.",
        )
    st.markdown("<div class='overview-row-gap'></div>", unsafe_allow_html=True)
    render_findings_cards(source_df)
    st.markdown("<div class='overview-row-gap overview-row-gap-small'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="quick-action-grid">
    <div class="quick-action-card"><div class="quick-action-title">Transfer Strategy</div><div class="quick-action-text">{html.escape('Sprint 14 portfolio optimization layer.' if LANG == 'EN' else 'Capa de optimización de carteras del Sprint 14.')}</div></div>
    <div class="quick-action-card"><div class="quick-action-title">Market Opportunities</div><div class="quick-action-text">{html.escape('Review ranking, Top 5 and risk-adjusted market opportunities.' if LANG == 'EN' else 'Revisar ranking, Top 5 y oportunidades ajustadas por riesgo.')}</div></div>
    <div class="quick-action-card"><div class="quick-action-title">Recruitment Board</div><div class="quick-action-text">{html.escape('Compare, replace and prioritize candidates.' if LANG == 'EN' else 'Comparar, reemplazar y priorizar candidatos.')}</div></div>
</div>
""",
        unsafe_allow_html=True,
    )
    render_opportunity_risk_top5_vertical(source_df, "Top 5 opportunities" if LANG == "EN" else "Top 5 oportunidades", "Initial executive review priority" if LANG == "EN" else "Prioridad inicial para revisión ejecutiva")


def render_transfer_strategy_placeholder() -> None:
    """Render Sprint 14C Transfer Strategy Engine.

    The section exposes the ILP portfolio optimizer implemented in src/strategy.
    It turns player-level opportunity signals into an optimized transfer portfolio
    under budget, positional, risk/scenario and squad-size constraints.
    """
    render_product_page_header(
        "Strategic Recruitment Engine",
        "⭐ Transfer Strategy Engine",
        (
            "Optimize a transfer portfolio under budget, position, risk and squad-size constraints."
            if LANG == "EN"
            else "Optimiza una cartera de fichajes bajo restricciones de presupuesto, posición, riesgo y tamaño de plantilla."
        ),
    )

    st.markdown(
        f"""
<div class="strategy-banner">
    <div class="strategy-eyebrow">{html.escape('Sprint 14 · Portfolio Optimization Layer' if LANG == 'EN' else 'Sprint 14 · Capa de optimización de cartera')}</div>
    <div class="strategy-title">{html.escape('From player ranking to portfolio decision.' if LANG == 'EN' else 'Del ranking de jugadores a la decisión de cartera.')}</div>
    <div class="strategy-copy">{html.escape('This module formulates transfer planning as a Binary Integer Programming problem: select the best combination of players subject to budget, positional coverage, risk and maximum-signing constraints.' if LANG == 'EN' else 'Este módulo formula la planificación de fichajes como un problema de Programación Entera Binaria: seleccionar la mejor combinación de jugadores sujeta a presupuesto, cobertura posicional, riesgo y número máximo de incorporaciones.')}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.expander(
        "🧠 " + ("Optimization methodology" if LANG == "EN" else "Metodología de optimización"),
        expanded=False,
    ):
        if LANG == "EN":
            st.markdown(
                """
                The engine uses the Sprint 14 portfolio dataset and solves a 0-1 selection problem.

                **Decision variable:** `x_i = 1` if player `i` is selected, `0` otherwise.

                **Objective:** maximize portfolio optimization score.

                **Main constraints:** budget ceiling, minimum budget utilization, maximum signings, average risk threshold, positional coverage and portfolio concentration depending on the selected style.
                """
            )
        else:
            st.markdown(
                """
                El motor utiliza el dataset de cartera del Sprint 14 y resuelve un problema de selección 0-1.

                **Variable de decisión:** `x_i = 1` si el jugador `i` es seleccionado, `0` en caso contrario.

                **Objetivo:** maximizar el score de optimización de la cartera.

                **Restricciones principales:** presupuesto máximo, utilización mínima del presupuesto, número máximo de fichajes, umbral medio de riesgo, cobertura posicional y concentración de cartera según el estilo seleccionado.
                """
            )

    controls_top = st.columns([1.00, 1.00, 1.00, 1.15, 1.00, 1.00], gap="large")

    with controls_top[0]:
        budget_m = st.slider(
            "Budget (€M)" if LANG == "EN" else "Presupuesto (€M)",
            min_value=5,
            max_value=100,
            value=30,
            step=5,
            key="transfer_strategy_budget_m",
        )

    with controls_top[1]:
        scenario_labels = {
            "conservative": "Conservative" if LANG == "EN" else "Conservador",
            "balanced": "Balanced" if LANG == "EN" else "Equilibrado",
            "aggressive": "Aggressive" if LANG == "EN" else "Agresivo",
        }
        scenario_display = st.selectbox(
            "Scenario" if LANG == "EN" else "Escenario",
            list(scenario_labels.values()),
            index=1,
            key="transfer_strategy_scenario_display",
        )
        scenario = {v: k for k, v in scenario_labels.items()}[scenario_display]

    with controls_top[2]:
        risk_profile_labels = {
            "low": "Low" if LANG == "EN" else "Bajo",
            "medium": "Medium" if LANG == "EN" else "Medio",
            "high": "High" if LANG == "EN" else "Alto",
        }
        risk_profile_display = st.selectbox(
            "Risk Profile" if LANG == "EN" else "Perfil de riesgo",
            list(risk_profile_labels.values()),
            index={"conservative": 0, "balanced": 1, "aggressive": 2}.get(scenario, 1),
            key="transfer_strategy_risk_profile_display",
            help=(
                "Used as an executive label. The optimization thresholds are driven by the selected scenario."
                if LANG == "EN"
                else "Se usa como etiqueta ejecutiva. Los umbrales de optimización los determina el escenario seleccionado."
            ),
        )
        risk_profile = {v: k for k, v in risk_profile_labels.items()}[risk_profile_display]

    with controls_top[3]:
        portfolio_style_labels = {
            "value_hunting": "Value Opportunities",
            "balanced_portfolio": "Balanced Squad Building",
            "star_prospects": "Star + Prospects",
        }
        portfolio_style_display = st.selectbox(
            "Portfolio Style" if LANG == "EN" else "Estilo cartera",
            list(portfolio_style_labels.values()),
            index=1,
            key="transfer_strategy_portfolio_style_display",
            help=(
                "Controls concentration and squad-building logic. Balanced Squad Building prevents one player from absorbing too much of the budget."
                if LANG == "EN"
                else "Controla la concentración y la lógica de construcción de plantilla. Balanced Squad Building evita que un jugador absorba demasiado presupuesto."
            ),
        )
        portfolio_style = {v: k for k, v in portfolio_style_labels.items()}[portfolio_style_display]

    with controls_top[4]:
        max_signings = st.slider(
            "Max Signings" if LANG == "EN" else "Máx. fichajes",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
            key="transfer_strategy_max_signings",
        )

    with controls_top[5]:
        min_budget_utilization = st.slider(
            "Min Budget Use" if LANG == "EN" else "Uso mín. presupuesto",
            min_value=0.50,
            max_value=0.95,
            value=0.70,
            step=0.05,
            key="transfer_strategy_min_budget_utilization",
            help=(
                "Minimum percentage of budget that the optimized portfolio must spend."
                if LANG == "EN"
                else "Porcentaje mínimo del presupuesto que debe consumir la cartera optimizada."
            ),
        )

    positions_needed = st.multiselect(
        "Positions Needed" if LANG == "EN" else "Posiciones necesarias",
        ["DEF", "MID", "ATT"],
        default=["DEF", "MID", "ATT"],
        key="transfer_strategy_positions_needed",
    )

    st.caption(
        (
            "Risk Profile is displayed as an executive interpretation layer. Portfolio Style controls concentration and balance."
            if LANG == "EN"
            else "El Perfil de riesgo se muestra como capa ejecutiva de interpretación. El Estilo de cartera controla concentración y equilibrio."
        )
    )

    if LANG == "EN":
        glossary_items = [
            ("Expected Upside", "Estimated aggregate value gap versus current market value."),
            ("Expected ROI", "Expected upside divided by total portfolio cost."),
            ("Portfolio Score", "Composite value indicator based on inefficiency, upside, confidence and age potential."),
            ("Average Confidence", "Average reliability of the analytical signal used by the optimizer."),
            ("Risk Proxy", "Inverse confidence indicator used as a practical uncertainty proxy."),
            ("Max Concentration", "Weight of the most expensive selected player over total portfolio cost."),
        ]
        glossary_title = "📚 Quick glossary"
    else:
        glossary_items = [
            ("Upside esperado", "Gap de valor agregado estimado frente al valor de mercado actual."),
            ("ROI esperado", "Upside esperado dividido por el coste total de la cartera."),
            ("Score cartera", "Indicador compuesto de ineficiencia, upside, confianza y potencial por edad."),
            ("Confianza media", "Fiabilidad media de la señal analítica utilizada por el optimizador."),
            ("Proxy riesgo", "Indicador inverso de confianza usado como proxy operativo de incertidumbre."),
            ("Concentración máxima", "Peso del jugador más caro sobre el coste total de la cartera."),
        ]
        glossary_title = "📚 Glosario rápido"

    glossary_html = "".join(
        f"<div class='strategy-glossary-item'><b>{html.escape(title)}</b><span>{html.escape(desc)}</span></div>"
        for title, desc in glossary_items
    )

    st.markdown(
        f"""
<details class="strategy-glossary-details">
    <summary>{html.escape(glossary_title)}</summary>
    <div class="strategy-glossary-grid">{glossary_html}</div>
</details>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="radar-info-box" style="margin-top:-4px; margin-bottom:12px;">
<b>{html.escape('Active constraints' if LANG == 'EN' else 'Restricciones activas')}:</b>
{html.escape(f'Budget €{budget_m}M · Scenario {scenario_display} · Risk {risk_profile_display} · Style {portfolio_style_display} · Max signings {max_signings} · Min budget use {min_budget_utilization:.0%}')}
<br><span style="color:#64748b;">{html.escape('Portfolio recalculates automatically when inputs change.' if LANG == 'EN' else 'La cartera se recalcula automáticamente al cambiar los parámetros.')}</span>
</div>
""",
        unsafe_allow_html=True,
    )

    try:
        portfolio = optimize_transfer_portfolio_with_style(
            budget=budget_m * 1_000_000,
            positions_needed=positions_needed,
            scenario=scenario,
            max_signings=max_signings,
            min_budget_utilization=min_budget_utilization,
            portfolio_style=portfolio_style,
        )

        if portfolio.empty:
            st.warning(
                "No feasible portfolio was returned by the optimizer."
                if LANG == "EN"
                else "El optimizador no ha devuelto una cartera factible."
            )
            return

        total_cost = float(portfolio["portfolio_cost"].sum())
        expected_upside = float(portfolio["expected_upside"].sum())
        expected_roi = expected_upside / total_cost if total_cost > 0 else np.nan
        budget_utilization = total_cost / (budget_m * 1_000_000)
        avg_portfolio_score = float(portfolio["portfolio_value_score"].mean())
        avg_confidence = float(portfolio["matching_confidence_norm"].mean()) if "matching_confidence_norm" in portfolio.columns else np.nan
        avg_risk_proxy = float(portfolio["risk_proxy"].mean()) if "risk_proxy" in portfolio.columns else np.nan
        max_player_share = float((portfolio["portfolio_cost"] / total_cost).max()) if total_cost > 0 else np.nan

        st.success(
            "Optimal transfer portfolio generated."
            if LANG == "EN"
            else "Cartera óptima de fichajes generada."
        )

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            render_metric_card_with_caption(
                "Total Cost" if LANG == "EN" else "Coste total",
                f"€{total_cost / 1_000_000:.1f}M",
                "Selected portfolio cost" if LANG == "EN" else "Coste de la cartera seleccionada",
            )
        with kpi2:
            render_metric_card_with_caption(
                "Budget Utilization" if LANG == "EN" else "Uso presupuesto",
                f"{budget_utilization:.1%}",
                "Budget consumed" if LANG == "EN" else "Presupuesto consumido",
            )
        with kpi3:
            render_strategy_metric_card(
                "Expected Upside" if LANG == "EN" else "Upside esperado",
                f"€{expected_upside / 1_000_000:.1f}M",
                "Aggregated expected value gap" if LANG == "EN" else "Gap esperado agregado",
                "Estimated aggregate value gap versus current market value." if LANG == "EN" else "Gap de valor agregado estimado frente al valor de mercado actual.",
            )
        with kpi4:
            render_strategy_metric_card(
                "Expected ROI" if LANG == "EN" else "ROI esperado",
                f"{expected_roi:.1%}" if pd.notna(expected_roi) else "N/A",
                "Upside / total cost" if LANG == "EN" else "Upside / coste total",
                "Expected upside divided by total portfolio cost." if LANG == "EN" else "Upside esperado dividido por el coste total de la cartera.",
            )
        with kpi5:
            render_strategy_metric_card(
                "Avg Portfolio Score" if LANG == "EN" else "Score medio cartera",
                f"{avg_portfolio_score:.1f}",
                "Mean portfolio value score" if LANG == "EN" else "Score medio de valor de cartera",
                "Composite value indicator based on inefficiency, upside, confidence and age potential." if LANG == "EN" else "Indicador compuesto de ineficiencia, upside, confianza y potencial por edad.",
            )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        if pd.notna(avg_confidence) and pd.notna(avg_risk_proxy):
            c1, c2, c3 = st.columns(3)
            with c1:
                render_strategy_metric_card(
                    "Average Confidence" if LANG == "EN" else "Confianza media",
                    f"{avg_confidence:.1f}",
                    "Mean matching confidence" if LANG == "EN" else "Confianza media del matching",
                    "Average reliability of the analytical signal used by the optimizer." if LANG == "EN" else "Fiabilidad media de la señal analítica utilizada por el optimizador.",
                )
            with c2:
                render_strategy_metric_card(
                    "Average Risk Proxy" if LANG == "EN" else "Proxy riesgo medio",
                    f"{avg_risk_proxy:.1f}",
                    "100 - confidence" if LANG == "EN" else "100 - confianza",
                    "Inverse confidence indicator used as a practical uncertainty proxy." if LANG == "EN" else "Indicador inverso de confianza usado como proxy operativo de incertidumbre.",
                )
            with c3:
                render_strategy_metric_card(
                    "Max Player Share" if LANG == "EN" else "Concentración máxima",
                    f"{max_player_share:.1%}" if pd.notna(max_player_share) else "N/A",
                    "Largest player / portfolio cost" if LANG == "EN" else "Mayor jugador / coste cartera",
                    "Weight of the most expensive selected player over total portfolio cost." if LANG == "EN" else "Peso del jugador más caro sobre el coste total de la cartera.",
                )

        st.subheader("📋 " + ("Recommended Portfolio" if LANG == "EN" else "Cartera recomendada"))

        display_cols = [
            "player_name_fbref",
            "club",
            "league",
            "position_group",
            "age",
            "market_value_eur",
            "player_portfolio_cost_share",
            "expected_upside",
            "expected_roi",
            "portfolio_value_score",
            "optimization_score",
        ]
        available_cols = [col for col in display_cols if col in portfolio.columns]
        display = portfolio[available_cols].copy()

        rename_map = {
            "player_name_fbref": "Player" if LANG == "EN" else "Jugador",
            "club": "Club",
            "league": "League" if LANG == "EN" else "Liga",
            "position_group": "Position" if LANG == "EN" else "Posición",
            "age": "Age" if LANG == "EN" else "Edad",
            "market_value_eur": "Market Value" if LANG == "EN" else "Valor mercado",
            "player_portfolio_cost_share": "Portfolio Share" if LANG == "EN" else "Peso cartera",
            "expected_upside": "Expected Upside" if LANG == "EN" else "Upside esperado",
            "expected_roi": "Expected ROI" if LANG == "EN" else "ROI esperado",
            "portfolio_value_score": "Portfolio Score" if LANG == "EN" else "Score cartera",
            "optimization_score": "Optimization Score" if LANG == "EN" else "Score optimización",
        }
        display = display.rename(columns=rename_map)

        money_cols = [
            col
            for col in ["Market Value", "Valor mercado", "Expected Upside", "Upside esperado"]
            if col in display.columns
        ]
        for col in money_cols:
            display[col] = display[col].apply(format_money_short)

        roi_cols = [col for col in ["Expected ROI", "ROI esperado"] if col in display.columns]
        for col in roi_cols:
            display[col] = pd.to_numeric(display[col], errors="coerce").map(
                lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
            )

        share_cols = [col for col in ["Portfolio Share", "Peso cartera"] if col in display.columns]
        for col in share_cols:
            display[col] = pd.to_numeric(display[col], errors="coerce").map(
                lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
            )


        age_cols = [col for col in ["Age", "Edad"] if col in display.columns]
        for col in age_cols:
            display[col] = pd.to_numeric(display[col], errors="coerce").map(
                lambda x: f"{x:.1f}" if pd.notna(x) else "N/A"
            )

        score_cols = [
            col
            for col in ["Portfolio Score", "Score cartera", "Optimization Score", "Score optimización"]
            if col in display.columns
        ]
        for col in score_cols:
            display[col] = pd.to_numeric(display[col], errors="coerce").map(
                lambda x: f"{x:.1f}" if pd.notna(x) else "N/A"
            )

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
        )

        if {"portfolio_cost", "expected_upside", "portfolio_value_score", "position_group"}.issubset(portfolio.columns):
            st.subheader("📈 " + ("Portfolio Map" if LANG == "EN" else "Mapa de cartera"))
            st.caption(
                "Hover each bubble to inspect player, club, cost, upside, ROI and portfolio score."
                if LANG == "EN"
                else "Pasa el ratón por cada burbuja para consultar jugador, club, coste, upside, ROI y score de cartera."
            )
            fig = go.Figure()
            for position_group, group_df in portfolio.groupby("position_group"):
                fig.add_trace(
                    go.Scatter(
                        x=group_df["portfolio_cost"] / 1_000_000,
                        y=group_df["expected_upside"] / 1_000_000,
                        mode="markers",
                        customdata=np.stack(
                            [
                                group_df["player_name_fbref"].astype(str),
                                group_df["club"].astype(str) if "club" in group_df.columns else pd.Series(["N/A"] * len(group_df), index=group_df.index),
                                group_df["position_group"].astype(str),
                                pd.to_numeric(group_df["age"], errors="coerce") if "age" in group_df.columns else pd.Series([np.nan] * len(group_df), index=group_df.index),
                                pd.to_numeric(group_df["expected_roi"], errors="coerce") if "expected_roi" in group_df.columns else pd.Series([np.nan] * len(group_df), index=group_df.index),
                                pd.to_numeric(group_df["portfolio_value_score"], errors="coerce") if "portfolio_value_score" in group_df.columns else pd.Series([np.nan] * len(group_df), index=group_df.index),
                            ],
                            axis=-1,
                        ),
                        marker=dict(
                            size=(pd.to_numeric(group_df["portfolio_value_score"], errors="coerce").fillna(50) / 4).clip(13, 30),
                            opacity=0.85,
                            line=dict(color="white", width=2),
                        ),
                        name=str(position_group),
                        hovertemplate=(
                            "<b>%{customdata[0]}</b><br>"
                            + ("Club" if LANG == "EN" else "Club")
                            + ": %{customdata[1]}<br>"
                            + ("Position" if LANG == "EN" else "Posición")
                            + ": %{customdata[2]}<br>"
                            + ("Age" if LANG == "EN" else "Edad")
                            + ": %{customdata[3]:.1f}<br>"
                            + ("Cost" if LANG == "EN" else "Coste")
                            + ": €%{x:.1f}M<br>"
                            + ("Upside" if LANG == "EN" else "Upside")
                            + ": €%{y:.1f}M<br>"
                            + ("ROI" if LANG == "EN" else "ROI")
                            + ": %{customdata[4]:.1%}<br>"
                            + ("Portfolio Score" if LANG == "EN" else "Score cartera")
                            + ": %{customdata[5]:.1f}<extra></extra>"
                        ),
                    )
                )
            fig.update_layout(
                xaxis_title="Cost (€M)" if LANG == "EN" else "Coste (€M)",
                yaxis_title="Expected Upside (€M)" if LANG == "EN" else "Upside esperado (€M)",
                height=540,
                paper_bgcolor="white",
                plot_bgcolor="white",
                margin=dict(l=70, r=90, t=42, b=70),
                legend_title="Position" if LANG == "EN" else "Posición",
            )
            fig.update_xaxes(
                rangemode="tozero",
                automargin=True,
                showgrid=True,
                zeroline=False,
            )
            fig.update_yaxes(
                rangemode="tozero",
                automargin=True,
                showgrid=True,
                zeroline=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    except ModuleNotFoundError as exc:
        st.error(
            (
                "The strategy optimizer module or one of its dependencies is missing. "
                "Check that `src/strategy/optimize_transfer_portfolio.py` exists and that PuLP is installed."
            )
            if LANG == "EN"
            else (
                "Falta el módulo del optimizador estratégico o alguna dependencia. "
                "Comprueba que existe `src/strategy/optimize_transfer_portfolio.py` y que PuLP está instalado."
            )
        )
        st.exception(exc)
    except Exception as exc:
        st.error(
            "No feasible portfolio found with the selected constraints."
            if LANG == "EN"
            else "No se ha encontrado una cartera factible con las restricciones seleccionadas."
        )
        st.exception(exc)

def render_market_opportunities_page(source_df: pd.DataFrame) -> None:
    render_product_page_header(
        "Market Opportunities",
        "Market Opportunities",
        T("matrix_caption"),
    )
    render_layer_badge("EXECUTIVE SCOUTING LAYER")
    st.markdown(f"## 🎯 {T('matrix_title')}", unsafe_allow_html=True)
    st.caption(T("matrix_caption"))
    fig = build_opportunity_risk_matrix(source_df)
    if fig is None:
        st.info("Not enough data to build the Opportunity vs Risk matrix with current filters." if LANG == "EN" else "No hay datos suficientes para generar la matriz Opportunity vs Risk con los filtros actuales.")
    else:
        st.markdown(
            f"""
            <div style="margin: 4px 0 12px 0;">
                <span class="matrix-chip matrix-chip-green">🟢 {html.escape('Immediate priority' if LANG == 'EN' else 'Prioridad inmediata')}</span>
                <span class="matrix-chip matrix-chip-orange">🟠 {html.escape('Growth bet' if LANG == 'EN' else 'Crecimiento')}</span>
                <span class="matrix-chip matrix-chip-blue">🔵 {html.escape('Low impact' if LANG == 'EN' else 'Bajo impacto')}</span>
                <span class="matrix-chip matrix-chip-red">🔴 {html.escape('High risk' if LANG == 'EN' else 'Riesgo elevado')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander(T("methodology"), expanded=False):
            st.markdown("""
- **X-axis:** Risk Score.
- **Y-axis:** Market Opportunity.
- **Bubble size:** risk-adjusted opportunity.
- **Dashed lines:** dynamic thresholds calculated on the filtered sample.
- **Quadrants:** priority target, growth bet, low-impact profile and high-risk profile.
            """ if LANG == "EN" else """
- **Eje X:** Risk Score.
- **Eje Y:** Market Opportunity.
- **Tamaño de burbuja:** oportunidad ajustada por riesgo.
- **Líneas discontinuas:** umbrales dinámicos calculados sobre la muestra filtrada.
- **Cuadrantes:** objetivo prioritario, apuesta de crecimiento, perfil de bajo impacto y riesgo elevado.
            """)
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "modeBarButtonsToRemove": ["zoom", "pan", "select", "lasso2d", "autoScale", "resetScale"]})
        render_opportunity_risk_top5_vertical(source_df, T("top5_title"), T("top5_caption"))
        render_opportunity_risk_insight(source_df)
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    render_layer_badge("OPERATIONAL SCOUTING LAYER")
    st.header(f"📋 {T('ranking_title')}")
    st.caption(T("ranking_caption"))
    table = build_ranked_table_df(source_df)
    render_paginated_recruitment_ranking(table)


def render_paginated_recruitment_ranking(table_df: pd.DataFrame) -> None:
    PAGE_SIZE = 5
    total_rows = len(table_df)
    total_pages = max(1, ceil(total_rows / PAGE_SIZE))
    if "players_page" not in st.session_state:
        st.session_state.players_page = 1
    st.session_state.players_page = min(st.session_state.players_page, total_pages)
    start_idx = (st.session_state.players_page - 1) * PAGE_SIZE
    page_df = table_df.iloc[start_idx:start_idx + PAGE_SIZE].copy()
    st.markdown(build_html_table(page_df), unsafe_allow_html=True)
    pag_left, pag_right = st.columns([2, 1])
    with pag_left:
        st.caption((f"Showing {len(page_df)} of {total_rows} players" if LANG == "EN" else f"Mostrando {len(page_df)} de {total_rows} jugadores"))
    with pag_right:
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("‹", disabled=st.session_state.players_page <= 1, key="market_page_prev"):
                st.session_state.players_page -= 1
                st.rerun()
        with c2:
            st.markdown(f"**{st.session_state.players_page} / {total_pages}**")
        with c3:
            if st.button("›", disabled=st.session_state.players_page >= total_pages, key="market_page_next"):
                st.session_state.players_page += 1
                st.rerun()


def render_individual_player_report(table_df: pd.DataFrame) -> None:
    st.header("👤 " + TXT("Informe individual de jugador"))
    if table_df.empty:
        st.info(TXT("No hay jugadores disponibles con los filtros actuales."))
        return
    name_col = get_player_name_column(table_df) or "player_name_fbref"
    player_names = table_df[name_col].fillna("Jugador").astype(str).tolist()
    selected_player = st.selectbox(TXT("Selecciona un jugador"), player_names, key="player_intelligence_report_selector")
    player_df = table_df[table_df[name_col].astype(str) == str(selected_player)].iloc[0]
    m1, m2, m3, m4, m5, m6 = st.columns([1.1, 1.1, 1.1, 1.15, 1.05, 0.95])
    with m1:
        render_metric_card(TXT("Valor mercado"), format_money_tm(safe_get(player_df, "market_value_eur")))
    with m2:
        render_metric_card(TXT("Valor estimado"), format_money_tm(safe_get(player_df, "predicted_market_value_eur")))
    with m3:
        render_metric_card(TXT("Gap de mercado"), format_money_tm(safe_get(player_df, "market_value_gap_eur")))
    with m4:
        render_metric_card("Opportunity", f"{format_score(safe_get(player_df, 'opportunity_score'))} / 100")
    with m5:
        render_metric_card("Risk Score", f"{format_score(safe_get(player_df, 'risk_score'))} / 100")
    with m6:
        rank = int(table_df.index[table_df[name_col].astype(str) == str(selected_player)][0]) + 1
        render_metric_card(TXT("Ranking"), f"#{rank} / {len(table_df)}")
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    profile_col, reading_col = st.columns([1, 1])
    with profile_col:
        with st.container(border=True):
            st.subheader("📋 " + TXT("Perfil scouting"))
            profile_table = f"""
            <table class="profile-table">
                <tr><td>{html.escape(TXT('Club'))}:</td><td>{html.escape(str(safe_get(player_df, 'club')))}</td></tr>
                <tr><td>{html.escape(TXT('Liga'))}:</td><td>{html.escape(league_display_name(safe_get(player_df, 'league')))}</td></tr>
                <tr><td>{html.escape(TXT('Posición'))}:</td><td>{html.escape(str(safe_get(player_df, 'position_group')))}</td></tr>
                <tr><td>{html.escape(TXT('Edad'))}:</td><td>{format_score(safe_get(player_df, 'age'))}</td></tr>
                <tr><td>{html.escape(TXT('Temporada'))}:</td><td>{html.escape(str(safe_get(player_df, 'season')))}</td></tr>
                <tr><td>{html.escape(TXT('Minutos en liga'))}:</td><td>{int(float(safe_get(player_df, 'minutes_played', 0))):,}</td></tr>
                <tr><td>{html.escape(TXT('Tier'))}:</td><td>{tier_badge(safe_get(player_df, 'dashboard_tier'))}</td></tr>
                <tr><td>{html.escape(TXT('Nivel de riesgo'))}:</td><td>{html.escape(risk_level_display_name(safe_get(player_df, 'risk_level')))}</td></tr>
            </table>
            """
            st.markdown(profile_table, unsafe_allow_html=True)
    with reading_col:
        with st.container(border=True):
            st.subheader("🧠 " + TXT("Lectura analítica"))
            recommendation = build_recommendation(player_df)
            st.markdown(f"**{html.escape(TXT('Recomendación'))}:** <span class='recommendation'>{html.escape(V(recommendation))}</span> <span class='info-icon'>i</span>", unsafe_allow_html=True)
            st.markdown(TXT("Este jugador aparece en la shortlist porque combina una señal de infravaloración con potencial de crecimiento y una fiabilidad analítica suficiente."))
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
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
    st.markdown("### 🔍 Model Drivers")
    with st.expander(TXT("Ver metodología técnica del modelo"), expanded=False):
        st.markdown("""
**Model Drivers / SHAP proxy** explains how each variable contributes to the player's estimated valuation. Positive bars push the estimated value upward; negative bars reduce the estimated value. SHAP explains model logic and should not be read as direct sporting causality.
""" if LANG == "EN" else """
**Model Drivers / SHAP proxy** explica cómo contribuye cada variable a la valoración estimada del jugador. Las contribuciones positivas elevan el valor estimado; las negativas lo reducen. SHAP explica la lógica interna del modelo y no debe interpretarse como causalidad deportiva directa.
""")
    st.markdown(
        f"""
<div class="shap-executive-box">
{('<b>Executive readout:</b> the chart shows the main factors explaining the selected player estimated value. This layer adds traceability and helps defend the recommendation.' if LANG == 'EN' else '<b>Lectura ejecutiva:</b> el gráfico muestra los principales factores que explican la estimación de valor del jugador seleccionado. Esta capa aporta trazabilidad y ayuda a defender la recomendación.')}
</div>
""",
        unsafe_allow_html=True,
    )
    shap_values = make_shap_proxy(player_df)
    if LANG == "EN":
        shap_values = shap_values.copy()
        shap_values["feature"] = shap_values["feature"].apply(V)
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
    fig_shap.update_layout(height=340, margin=dict(l=10, r=30, t=20, b=35), xaxis_title=("SHAP contribution on estimated log-value" if LANG == "EN" else "Contribución SHAP sobre log-valor estimado"), yaxis_title="", plot_bgcolor="white", paper_bgcolor="white")
    fig_shap.update_xaxes(showgrid=True, gridcolor="#e5e7eb", zeroline=True)
    fig_shap.update_yaxes(showgrid=False)
    with st.expander(TXT("Ver contribución técnica detallada"), expanded=False):
        st.plotly_chart(fig_shap, use_container_width=True)


def render_player_intelligence_page(source_df: pd.DataFrame) -> None:
    render_product_page_header("Player Intelligence", "Player Intelligence", "Radar, positional benchmark, individual profile and model drivers." if LANG == "EN" else "Radar, benchmark posicional, perfil individual y drivers del modelo.")
    render_layer_badge("PLAYER ANALYSIS LAYER")
    table = build_ranked_table_df(source_df)
    render_player_radar_benchmarking(table)
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    render_individual_player_report(table)


def render_recruitment_board_page(source_df: pd.DataFrame) -> None:
    render_product_page_header("Recruitment Board", "Recruitment Board", "Candidate comparison, replacements, similar profiles, investment analysis and model drivers." if LANG == "EN" else "Comparación de candidatos, reemplazos, perfiles similares, análisis de inversión y drivers del modelo.")
    table = build_ranked_table_df(source_df)
    render_shortlist_intelligence_dashboard(table)


def render_methodology_page(source_df: pd.DataFrame) -> None:
    render_product_page_header("Methodology", "Methodology", "Data, modeling, validation and business evaluation." if LANG == "EN" else "Datos, modelización, validación y evaluación de negocio.")
    st.markdown('<div class="methodology-grid">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card_with_caption("Dataset", f"{len(source_df):,}", "modeled player-season candidates" if LANG == "EN" else "candidatos jugador-temporada modelados")
    with m2:
        render_metric_card_with_caption("Coverage", f"{source_df['league'].nunique() if 'league' in source_df.columns else 'N/A'}", "European leagues" if LANG == "EN" else "ligas europeas")
    with m3:
        render_metric_card_with_caption("Model", "XGBoost", "production ML estimator" if LANG == "EN" else "estimador ML productivo")
    with m4:
        render_metric_card_with_caption("Validation", "Temporal", "out-of-sample scouting logic" if LANG == "EN" else "lógica out-of-sample para scouting")
    st.markdown('</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card_with_caption("Growth OLS", "R² 0.5258", "Interpretable benchmark" if LANG == "EN" else "Benchmark interpretable")
    with c2:
        render_metric_card_with_caption("Tuned XGBoost", "R² 0.5414", "Production model" if LANG == "EN" else "Modelo productivo")
    with c3:
        render_metric_card_with_caption("Precision@K", "90%", "Ranking evaluation" if LANG == "EN" else "Evaluación de ranking")
    with st.expander("CRISP-DM / Del Dato al Conocimiento", expanded=False):
        st.markdown("""
Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment

The dashboard separates historical evaluation, operational exploitation, Player Intelligence, Recruitment Intelligence and Decision Support. This architecture avoids mixing academic validation with executive recommendation and prepares Sprint 14: strategic transfer optimization.
""" if LANG == "EN" else """
Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment

El dashboard separa evaluación histórica, explotación operativa, Player Intelligence, Recruitment Intelligence y Decision Support System. Esta arquitectura evita mezclar validación académica con recomendación ejecutiva y prepara la evolución hacia Sprint 14: optimización estratégica de fichajes.
""")
    with st.expander("Scoring architecture", expanded=False):
        st.markdown("""
Predictions  
↓  
Inefficiency Score  
↓  
Growth Score  
↓  
Confidence Score  
↓  
Opportunity Score  
↓  
Risk Score  
↓  
Executive Decision Score
""")


if filtered_df.empty:
    st.warning("No players match the current filters." if LANG == "EN" else "No hay jugadores que cumplan los filtros actuales.")
else:
    if dashboard_page == "Executive Overview":
        render_executive_overview_page(filtered_df)
    elif dashboard_page == "Transfer Strategy":
        render_transfer_strategy_placeholder()
    elif dashboard_page == "Market Opportunities":
        render_market_opportunities_page(filtered_df)
    elif dashboard_page == "Player Intelligence":
        render_player_intelligence_page(filtered_df)
    elif dashboard_page == "Recruitment Board":
        render_recruitment_board_page(filtered_df)
    elif dashboard_page == "Methodology":
        render_methodology_page(filtered_df)


# =============================================================================
# Sprint 11 final closure patch: search centering, footer restore and compact ending
# =============================================================================
st.markdown(
    """
<style>
/* Final top rhythm: no blank rounded spacer above search, no excessive page-end whitespace. */
[data-testid="stAppViewContainer"] .main .block-container,
.block-container {
    padding-bottom: 0.85rem !important;
}
.scouting-topbar {
    margin-top: 0.88rem !important;
    margin-bottom: 18px !important;
}

/* New single search header shell. */
.final-search-shell {
    background: #ffffff !important;
    border: 1px solid #d7e6fb !important;
    border-radius: 22px !important;
    padding: 18px 22px 16px 22px !important;
    box-shadow: 0 14px 32px rgba(15, 23, 42, 0.055) !important;
    margin: 0 0 14px 0 !important;
}
.final-search-shell .final-search-title {
    display: flex !important;
    align-items: center !important;
    gap: 9px !important;
    margin: 0 0 7px 0 !important;
    color: #08275a !important;
    font-size: 1.03rem !important;
    font-weight: 950 !important;
    letter-spacing: 0.11em !important;
    text-transform: uppercase !important;
}
.final-search-shell .final-search-caption {
    margin: 0 !important;
    color: #475569 !important;
    font-size: 0.91rem !important;
    line-height: 1.35 !important;
}
.final-search-examples {
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
    max-width: 100% !important;
    padding: 6px 12px !important;
    margin: 10px 0 18px 0 !important;
    border-radius: 999px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    font-size: 0.78rem !important;
    font-weight: 900 !important;
}
/* Main selectboxes: keep selected value vertically centered. This intentionally covers the dashboard's main selectboxes, not sidebar widgets. */
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    display: flex !important;
    align-items: center !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"],
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="combobox"] > div,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
    display: flex !important;
    align-items: center !important;
    min-height: 42px !important;
    line-height: 1.25 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
/* The first main selectbox is the global search input. */
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"]:first-of-type div[data-baseweb="select"] > div,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:has(input[aria-autocomplete="list"]) {
    min-height: 58px !important;
    height: 58px !important;
    padding: 0 18px !important;
    border: 2px solid #2563eb !important;
    border-radius: 999px !important;
    background: #ffffff !important;
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.10) !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:has(input[aria-autocomplete="list"]) span,
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:has(input[aria-autocomplete="list"]) input {
    min-height: 58px !important;
    font-size: 1.02rem !important;
}
/* Hide accidental empty markdown wrappers if Streamlit leaves one after CSS patches. */
div[data-testid="stMarkdownContainer"]:empty,
div[data-testid="stMarkdownContainer"] p:empty {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}


/* Final robust selectbox centering for the global search selected value. */
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    display: flex !important;
    align-items: center !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
    display: flex !important;
    align-items: center !important;
    min-height: 56px !important;
}
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] [class*="singleValue"],
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] [class*="placeholder"],
[data-testid="stAppViewContainer"] > .main div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    display: flex !important;
    align-items: center !important;
    min-height: 56px !important;
    line-height: 56px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
.scouting-topbar-right span::first-letter {
    color: #bfdbfe !important;
}

/* Footer restored and compact. */
.scouting-iq-footer {
    margin: 42px auto 4px auto !important;
    padding: 18px 0 8px 0 !important;
    border-top: 1px solid #dbe4f0 !important;
    text-align: center !important;
    color: #64748b !important;
    font-size: 0.78rem !important;
}
.scouting-iq-footer b {
    display: block !important;
    margin-bottom: 6px !important;
    color: #0f172a !important;
    font-size: 0.82rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="scouting-iq-footer">
    <b>SCOUTING IQ PLATFORM</b>
    <div>Market Value Intelligence System · Version v1.2.1 · Sprint 14</div>
    <div>Master Thesis · Sports Analytics &amp; Data Science</div>
</div>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Sprint 13.5 UX polish v7: compact guide beside examples and unclipped context chips
# =============================================================================
st.markdown(
    """
<style>
.search-helper-row {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-wrap: nowrap !important;
    margin-top: 10px !important;
    width: 100% !important;
}
.search-helper-row .final-search-examples,
.final-search-examples {
    flex: 0 1 auto !important;
    width: auto !important;
    max-width: calc(100% - 124px) !important;
    min-height: 30px !important;
    margin: 0 !important;
    padding: 6px 10px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-size: .74rem !important;
}
.search-helper-row > .search-quick-guide,
.search-quick-guide.quick-guide-inline,
.quick-guide-inline.search-quick-guide {
    flex: 0 0 116px !important;
    width: 116px !important;
    min-width: 116px !important;
    max-width: 116px !important;
    display: inline-block !important;
    margin: 0 !important;
    position: relative !important;
    z-index: 1200 !important;
}
.search-quick-guide.quick-guide-inline summary,
.quick-guide-inline.search-quick-guide summary {
    min-height: 30px !important;
    height: 30px !important;
    padding: 6px 9px 6px 12px !important;
    font-size: .74rem !important;
    line-height: 1 !important;
    white-space: nowrap !important;
}
.search-quick-guide.quick-guide-inline summary::after,
.quick-guide-inline.search-quick-guide summary::after {
    margin-left: 5px !important;
    font-size: .70rem !important;
}
.search-quick-guide.quick-guide-inline[open],
.quick-guide-inline.search-quick-guide[open] {
    flex-basis: 100% !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-top: 8px !important;
    grid-column: 1 / -1 !important;
}
.search-helper-row:has(.search-quick-guide[open]) {
    flex-wrap: wrap !important;
}
.context-strip-v2.compact-context-panel,
.compact-context-panel {
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
    padding: 15px 17px 18px 17px !important;
    margin-bottom: 18px !important;
}
.compact-context-panel .context-strip-main {
    display: grid !important;
    grid-template-columns: minmax(96px, .28fr) minmax(0, .72fr) !important;
    align-items: start !important;
    gap: 14px !important;
    margin-bottom: 10px !important;
}
.compact-context-panel .context-secondary-kpis {
    display: flex !important;
    flex-wrap: wrap !important;
    align-items: flex-start !important;
    gap: 7px !important;
}
.compact-context-panel .context-chip-row {
    display: flex !important;
    flex-wrap: wrap !important;
    align-items: flex-start !important;
    gap: 7px !important;
    width: 100% !important;
    max-height: none !important;
    height: auto !important;
    overflow: visible !important;
    margin: 10px 0 0 0 !important;
    padding: 0 !important;
}
.compact-context-panel .context-chip,
.context-chip {
    margin: 0 !important;
    white-space: nowrap !important;
    line-height: 1.1 !important;
}
.compact-context-panel .context-current-kpi {
    min-width: 96px !important;
}
.compact-context-panel .context-current-value {
    font-size: 1.95rem !important;
}
.compact-context-panel .context-current-label {
    font-size: .76rem !important;
}
.final-search-shell,
[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    padding-bottom: 14px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# Sprint 13.5 UX polish v8: quick guide as compact popover beside examples
# =============================================================================
st.markdown(
    """
<style>
/* The quick guide is now a compact popover chip next to examples, not an inline expander. */
.search-helper-inline {
    display: flex !important;
    align-items: center !important;
    min-height: 34px !important;
    margin-top: 10px !important;
}
.search-helper-inline .final-search-examples,
.final-search-examples {
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
    max-width: 100% !important;
    min-height: 30px !important;
    padding: 6px 11px !important;
    border-radius: 999px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    font-size: .74rem !important;
    font-weight: 900 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin: 0 !important;
}
/* Main-area popover button styled as the same family as examples. */
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] {
    margin-top: 10px !important;
}
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button {
    min-height: 30px !important;
    height: 30px !important;
    padding: 5px 11px !important;
    border-radius: 999px !important;
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e3a8a !important;
    font-size: .74rem !important;
    font-weight: 900 !important;
    box-shadow: none !important;
}
[data-testid="stAppViewContainer"] .main div[data-testid="stPopover"] button:hover {
    background: #dbeafe !important;
    border-color: #93c5fd !important;
}
.quick-guide-popover-body {
    min-width: 520px !important;
    max-width: 680px !important;
}
.quick-guide-popover-body .quick-guide-layout {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 10px !important;
    margin-bottom: 10px !important;
}
.quick-guide-popover-body .quick-guide-glossary {
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
}
/* Neutralize the old inline-expander behavior if cached CSS still matches. */
.search-quick-guide,
.quick-guide-inline.search-quick-guide {
    display: none !important;
}
/* The search card should not feel clipped at the bottom after the helper row. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.final-search-title) {
    padding-bottom: 20px !important;
}
@media (max-width: 1250px) {
    .quick-guide-popover-body { min-width: 360px !important; }
    .quick-guide-popover-body .quick-guide-layout,
    .quick-guide-popover-body .quick-guide-glossary { grid-template-columns: 1fr !important; }
}
</style>
""",
    unsafe_allow_html=True,
)
