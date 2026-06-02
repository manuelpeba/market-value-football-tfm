# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release v1.0.0 — Scouting Intelligence Platform.

El objetivo es justificar las decisiones desde una perspectiva:

- econométrica
- machine learning
- explainability
- scoring multicriterio
- evaluación de negocio
- football analytics
- scouting cuantitativo

---

# Filosofía de modelización

El proyecto adopta una arquitectura híbrida donde la precisión predictiva no constituye el objetivo final.

La finalidad última es generar recomendaciones accionables para scouting.

Arquitectura conceptual:

```text
Modelización
↓
Evaluación
↓
Scoring
↓
Ranking
↓
Player Intelligence
↓
Decision Support
↓
Scouting Intelligence
```

Principio metodológico:

```text
maximizar utilidad de scouting
y no únicamente métricas predictivas
```

---

# Decisiones econométricas

## Modelo seleccionado

Modelo:

```python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
growth variables +
league FE +
position FE
```

Decisiones:

- logaritmo del valor de mercado
- efectos fijos por liga
- efectos fijos por posición
- covarianza robusta HC3
- validación temporal

Rol:

```text
Benchmark interpretable
```

Resultados finales:

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Growth OLS | 0.7287 | 0.9053 | 0.5258 |

Conclusión:

OLS permanece como benchmark explicativo del sistema.

---

# Decisiones Machine Learning

## Modelos evaluados

- Tuned Random Forest
- Tuned LightGBM
- HistGradientBoosting
- Tuned XGBoost

## Diseño experimental

El pipeline incorpora:

- validación temporal
- ColumnTransformer
- imputación
- escalado
- codificación categórica
- RandomizedSearchCV
- MLflow

## Resultados finales

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Tuned Random Forest | 0.7486 | 0.9303 | 0.4980 |
| Tuned LightGBM | 0.7307 | 0.9052 | 0.5248 |
| HistGradientBoosting | 0.7292 | 0.9011 | 0.5291 |
| Tuned XGBoost | **0.7120** | **0.8892** | **0.5414** |

Decisión:

```text
Tuned XGBoost = modelo productivo
```

Justificación:

- mejor MAE
- mejor RMSE
- mejor R²
- robustez
- compatibilidad SHAP

---

# Explainability

## Decisión principal

```text
SHAP = mecanismo oficial de interpretación
```

Capacidades:

### Global

- feature importance
- SHAP importance
- summary plots

### Local

- explicación por jugador
- scouting reports
- drivers positivos
- drivers negativos

Justificación:

La recomendación debe ser defendible ante perfiles no técnicos.

---

# Decisiones sobre scoring

Sprint 5 introduce una capa específica para transformar predicciones en señales accionables.

Arquitectura:

```text
Predicción
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
```

---

## Inefficiency Score

Objetivo:

```text
Valor esperado - valor observado
```

Permite detectar:

- infravaloración
- sobrevaloración

---

## Growth Score

Captura:

- potencial
- trayectoria
- revalorización futura

---

## Confidence Score

Captura:

- calidad de matching
- robustez estadística
- estabilidad temporal

---

## Opportunity Score

Implementación conceptual:

```python
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
```

Decisión:

Priorizar infravaloración sin ignorar potencial ni robustez.

---

# Sprint 10 — Risk Framework

Introducido en Sprint 10.3.

Problema identificado:

```text
Opportunity alta
≠
recomendación segura
```

Se incorpora:

```text
Risk Score
```

Objetivo:

Cuantificar incertidumbre asociada a cada oportunidad.

Interpretación:

| Riesgo | Significado |
|----------|-------------|
| Bajo | Perfil estable |
| Medio | Riesgo moderado |
| Alto | Elevada incertidumbre |

Resultado:

```text
Opportunity Score
+
Risk Score
=
priorización más realista
```

---

# Ranking Engine

Objetivo:

Convertir scores en recomendaciones priorizadas.

Outputs:

```text
top_undervalued_global.csv
top_undervalued_by_league.csv
top_undervalued_by_position.csv
top_high_potential.csv
top_low_risk.csv
scouting_shortlist.csv
scouting_shortlist_with_risk.csv
```

Decisión:

Los rankings no sustituyen al scout.

Reducen espacio de búsqueda.

---

# Decisiones de evaluación

El proyecto adopta una visión más amplia que la evaluación tradicional.

Métricas utilizadas:

- RMSE
- MAE
- R²
- Precision@K
- ROI esperado
- ROI ajustado por riesgo
- Positive ROI Rate

Principio:

```text
un modelo útil
no es únicamente
el que predice mejor
sino el que genera mejores decisiones
```

---

# Historical Evaluation Layer

Introducida formalmente en Sprint 10.

Objetivo:

Separar evaluación metodológica de uso operativo.

Funciones:

- comparación de modelos
- validación temporal
- análisis académico
- backtesting

Artefactos:

```text
tuned_xgboost_test_predictions.csv
tuned_xgboost_full_predictions.csv
```

---

# Current Scouting Layer

Introducida en Sprint 10.3.

Objetivo:

Generar recomendaciones operativas sobre la temporada actual.

Artefactos:

```text
tuned_xgboost_predictions.csv
scoring_dataset.csv
scouting_shortlist.csv
scouting_shortlist_with_risk.csv
```

Contribución metodológica:

```text
Evaluación histórica
≠
Scouting operativo
```

Esta separación constituye una de las decisiones más importantes del proyecto.

---

# Sprint 10.1 — Player Intelligence

Problema identificado:

```text
Ranking
≠
comprensión del perfil del jugador
```

Solución:

## Player Radar MVP

Métricas:

- minutos
- goles/90
- asistencias/90
- G+A/90
- Growth Score
- Confidence Score

## Positional Benchmarking

Comparación contra:

- misma posición
- universo completo

## Scouting Narrative

Interpretación automática del perfil.

Resultado:

```text
Player Intelligence Layer
```

---

# Sprint 10.2 — FBref Advanced Audit

Objetivo:

Determinar viabilidad de métricas avanzadas.

Tablas auditadas:

- Shooting
- Defense
- Misc
- Playing Time
- Passing
- Possession
- Goal & Shot Creation

Resultado:

Definición del roadmap para:

```text
Advanced Football Radar
```

---

# Sprint 10.3 — Current Season Scouting Refresh

Decisiones adoptadas:

- integración temporada 2025-2026
- reentrenamiento completo
- Risk Framework
- Current Scouting Layer

Resultado:

Dataset modelizable:

| Métrica | Valor |
|----------|----------:|
| Observaciones | 3.916 |
| Jugadores únicos | 2.136 |
| Temporadas | 2019-2020 → 2025-2026 |

---

# Trade-offs metodológicos

| Trade-off | Decisión |
|----------|-----------|
| Interpretabilidad vs precisión | OLS + XGBoost |
| Econometría vs ML | Arquitectura híbrida |
| Cobertura vs matching estricto | Priorizar calidad |
| Complejidad vs reproducibilidad | Modularización |
| Métrica técnica vs utilidad | Precision@K + ROI |
| Ranking automático vs scout | Sistema de apoyo |
| Evaluación histórica vs operación | Separación explícita Sprint 10 |

---

# Prevención de leakage

Controles:

- validación temporal
- separación train/test
- exclusión de variables futuras
- scoring posterior a predicción
- persistencia independiente

Principio:

```text
Toda variable utilizada como input
debe existir en el momento real
de la decisión.
```

---

# Limitaciones actuales

## Datos

- ausencia de xG/xA Understat
- limitaciones defensivas avanzadas
- ausencia de variables salariales
- ausencia de variables contractuales

## Modelización

- dependencia parcial de Transfermarkt
- heterogeneidad por posición
- sensibilidad a outliers

## Evaluación

- Precision@K basada en proxies
- ausencia de transferencias reales
- ausencia de backtesting rolling completo

---

# Próximas decisiones

## Sprint 11

Advanced Football Radar

- shooting
- defense
- misc
- playing time

## Sprint 12

Data Enrichment

- Understat
- xG
- xA

## Sprint 13

Advanced Modeling

- CatBoost
- TabPFN
- Ensemble Models

---

# Conclusión

La principal evolución metodológica del proyecto se produce durante Sprint 10.

La arquitectura deja de centrarse exclusivamente en:

```text
Predicción
```

y pasa a estructurarse como:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Player Intelligence
↓
Decision Support
↓
Scouting Intelligence
```

La separación entre Historical Evaluation Layer y Current Scouting Layer constituye la decisión metodológica más relevante de la release v1.0.0.

Esta arquitectura aproxima el proyecto a sistemas utilizados en departamentos profesionales de Football Analytics y Scouting.
