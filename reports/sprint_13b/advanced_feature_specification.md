# Sprint 13B — Advanced Feature Specification

## Overview

This document defines the advanced features introduced during Sprint 13B (Advanced Data Expansion).

The objective of these features is to enrich the representation of player performance beyond traditional production metrics and improve the explanatory power of market value models.

The new features are derived from advanced FBref datasets successfully integrated through the SoccerData framework:

- Shooting
- Playing Time
- Miscellaneous

Coverage diagnostics indicate approximately 99% availability across:

- 11 leagues
- 7 seasons
- 43,000+ player-season observations

These features will be incorporated into both:

- Econometric models
- Machine Learning models

for subsequent re-estimation and evaluation.

---

# Design Principles

The feature engineering process follows four principles:

1. Football interpretability
2. Economic relevance
3. Positional comparability
4. Reproducibility

All composite indicators are constructed using position-normalized percentiles.

This approach ensures comparability across positions and prevents systematic bias toward attacking roles.

---

# Feature 1 — Finishing Index v2

## Purpose

Measure offensive threat generation and finishing capability.

Unlike the original finishing index, this version captures both:

- Production
- Shot generation

and therefore provides a broader representation of attacking contribution.

---

## Source Variables

### Existing Variables

- goals

### New Sprint 13B Variables

- shots
- shots_on_target
- shots_per90
- shots_on_target_per90

---

## Normalization

Position-adjusted percentiles:

- goals_position_pct
- shots_position_pct
- shots_on_target_position_pct
- shots_per90_position_pct
- shots_on_target_per90_position_pct

---

## Formula

```text
finishing_index_v2 =
0.40 * goals_position_pct
+
0.20 * shots_position_pct
+
0.20 * shots_on_target_position_pct
+
0.10 * shots_per90_position_pct
+
0.10 * shots_on_target_per90_position_pct
```

---

## Interpretation

High values indicate players who:

- score goals
- generate shots
- consistently threaten the opposition goal

Expected beneficiaries:

- Forwards
- Wingers
- Attacking Midfielders

---

# Feature 2 — Availability Index

## Purpose

Measure competitive availability and coach trust.

The market often rewards players who are consistently selected and capable of sustaining playing time.

Availability represents an important component of player value beyond technical performance.

---

## Source Variables

### Existing Variables

- minutes

### New Sprint 13B Variables

- starts
- complete_matches

---

## Normalization

Position-adjusted percentiles:

- starts_position_pct
- minutes_position_pct
- complete_matches_position_pct

---

## Formula

```text
availability_index =
0.40 * starts_position_pct
+
0.30 * minutes_position_pct
+
0.30 * complete_matches_position_pct
```

---

## Interpretation

High values indicate:

- regular starters
- high availability
- sustained competitive participation

Expected relevance across all positions.

---

# Feature 3 — Defensive Activity Index

## Purpose

Capture defensive contribution.

The current modeling framework is primarily driven by offensive metrics.

This feature introduces a defensive dimension to improve representation of:

- Centre Backs
- Full Backs
- Defensive Midfielders

---

## Source Variables

### New Sprint 13B Variables

- interceptions
- tackles_won

---

## Normalization

Position-adjusted percentiles:

- interceptions_position_pct
- tackles_won_position_pct

---

## Formula

```text
defensive_activity_index =
0.50 * interceptions_position_pct
+
0.50 * tackles_won_position_pct
```

---

## Interpretation

High values indicate players with:

- strong defensive involvement
- active ball recovery profiles
- above-average defensive contribution for their position

Expected to reduce offensive bias in valuation models.

---

# Expected Modeling Impact

## Hypothesis H13B.1

The inclusion of advanced finishing, availability and defensive activity metrics will improve model explanatory power relative to the current specification.

---

## Hypothesis H13B.2

The new features will reduce offensive bias and improve representation of defensive player profiles.

---

# Expected Benefits

## Econometric Models

Potential improvements in:

- Adjusted R²
- Coefficient stability
- Positional fairness

---

## Machine Learning Models

Potential improvements in:

- R²
- RMSE
- MAE

through a richer representation of player performance.

---

# Feature Summary

| Feature | Category | Variables | Range |
|----------|----------|----------|----------|
| finishing_index_v2 | Offensive | Goals, Shots, SoT, Shots/90, SoT/90 | [0,1] |
| availability_index | Reliability | Starts, Minutes, Complete Matches | [0,1] |
| defensive_activity_index | Defensive | Interceptions, Tackles Won | [0,1] |

---

# Sprint Status

Status:

```text
DESIGNED
```

Next phase:

```text
Sprint 13B.3
Feature Engineering Implementation
```

The features defined in this document will be implemented in the feature engineering pipeline and subsequently evaluated through econometric and machine learning re-estimation.