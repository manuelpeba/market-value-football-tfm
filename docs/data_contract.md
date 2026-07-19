# TM.8.8–TM.8.10 — DSS Dataset Contract

## Objetivo

Separar estrictamente los contextos temporales del DSS para evitar mezclas entre datos históricos de modelado y snapshot actual.

## Contextos obligatorios

### 1. Season Context

Contexto utilizado por el modelo predictivo.

Campos:

- season
- season_context_club
- season_context_league
- season_context_market_value_eur

Estos campos son históricos y no deben sobrescribirse con snapshot actual.

### 2. Current Snapshot Context

Contexto actual de Transfermarkt.

Campos:

- current_club_snapshot
- current_league_snapshot
- current_market_value_eur_snapshot
- current_valuation_date

Estos campos representan la fotografía actual del jugador.

### 3. Presentation Context

Campos consumidos por Streamlit.

Campos:

- display_club
- display_league
- display_market_value_eur

Regla:

- display_club debe derivar de current_club_snapshot
- display_league debe derivar de current_league_snapshot
- display_market_value_eur debe derivar de current_market_value_eur_snapshot

## Regla de interpretación del gap

Las métricas:

- market_value_gap_eur
- market_value_gap_pct
- expected_upside
- expected_roi
- portfolio_cost

deben declarar el contexto usado.

Si el jugador cambió de club o liga entre el contexto de modelado y el snapshot actual, el gap histórico no puede interpretarse como una valoración actual directa.

## Campos de control obligatorios

- context_changed
- club_context_changed
- league_context_changed
- valuation_context
- gap_interpretation_status

Valores recomendados para gap_interpretation_status:

- VALID_SAME_CONTEXT
- CONTEXT_CHANGED_CAUTION
- INVALID_CURRENT_INTERPRETATION

## Contrato productivo v2.0.0

TM.8.10 convirtió estas reglas en la DataFrame Contract Layer de la release. Además de distinguir los tres contextos, el contrato debe garantizar:

- identidad canónica mediante el Player Registry;
- presencia y tipos compatibles de campos obligatorios;
- ausencia de fabricación silenciosa de `inefficiency_score`;
- uso del `risk_score` procedente de la autoridad de riesgo;
- trazabilidad del snapshot y de su fecha de valoración;
- coherencia entre `current_*` y `display_*` sin sobrescribir `season_*`.

Los consumidores deben fallar de forma explícita ante un contrato inválido o degradar la presentación con un estado documentado; no deben rellenar con ceros una señal analítica ausente.
