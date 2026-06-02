# 📖 Memoria Metodológica – Notas de Desarrollo

## Objetivo del documento

Este documento centraliza decisiones metodológicas, hipótesis, experimentos, resultados y conclusiones obtenidas durante el desarrollo de la plataforma:

```text
Market Value Dynamics and Market Inefficiency Detection
in European Football
```

Su propósito es servir como base para la redacción de la memoria académica final del TFM y documentar la evolución metodológica completa hasta la release v1.0.0 — Scouting Intelligence Platform.

---

# Metodología general

El proyecto sigue una adaptación de CRISP-DM:

1. Comprensión de negocio
2. Comprensión de datos
3. Preparación de datos
4. Modelización
5. Evaluación
6. Despliegue

La ejecución fue iterativa:

```text
Hipótesis
↓
Implementación
↓
Evaluación experimental
↓
Aceptación / rechazo
↓
Aprendizaje
↓
Nueva iteración
```

---

# Evolución conceptual del proyecto

La evolución real del sistema fue:

```text
Predicción de valor de mercado
↓
Evaluación econométrica
↓
Machine Learning
↓
Explainability
↓
Scoring multicriterio
↓
Decision Support System
↓
Current Scouting
↓
Player Intelligence
↓
Scouting Intelligence
```

La release v1.0.0 consolida esta transición.

---

# Sprint 1 — Normalización contextual

## Hipótesis

La normalización por posición y competición podría mejorar la capacidad predictiva.

## Variables añadidas

- goals_per90_pos_z
- assists_per90_pos_z
- goals_position_percentile
- assists_position_percentile

Agrupación:

```text
[position_group, league]
```

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS |1.0035|0.8130|0.4160|
| Advanced OLS |1.0065|0.8166|0.4148|

## Conclusión

Hipótesis rechazada.

La señal parecía ya capturada por efectos estructurales.

---

# Sprint 2 — Growth Features

## Hipótesis

El mercado incorpora señales de trayectoria y crecimiento futuro.

## Variables

- market_value_growth_prev
- delta_log_market_value_prev
- age_squared
- career_year
- breakout_indicator

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS |1.0035|0.8130|0.4160|
| Growth OLS |0.9046|0.7278|0.5255|

## Conclusión

Hipótesis aceptada.

La trayectoria histórica constituye una señal clave para explicar valoraciones futuras.

---

# Sprint 3 — Composite Football Indices

## Hipótesis

La agregación de métricas futbolísticas podría mejorar rendimiento predictivo.

## Índices

- finishing_index
- playmaking_index
- progression_index
- defensive_index

## Resultados

Sin mejora estadísticamente relevante sobre Growth OLS.

## Conclusión

Mayor utilidad interpretativa que predictiva.

Los índices se conservaron como herramienta de scouting y reporting.

---

# Sprint 4 — Machine Learning Baseline

## Hipótesis

Los modelos no lineales podrían superar a OLS.

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Random Forest |1.0481|0.8527|0.3599|
| XGBoost |1.0943|0.8801|0.3022|
| LightGBM |1.1078|0.8936|0.2848|

## Conclusión

Hipótesis rechazada para configuraciones baseline.

---

# Sprint 4B — ML Pipeline Mejorado

## Mejoras introducidas

- validación temporal
- imputación robusta
- One-Hot Encoding
- RandomizedSearchCV
- MLflow
- preprocessing reproducible

## Resultados históricos

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS |0.9046|0.7278|0.5255|
| Tuned XGBoost |0.8753|0.7004|0.5536|

## Conclusión

Hipótesis aceptada.

Machine Learning supera consistentemente al benchmark econométrico.

---

# Sprint 4C — Explainability

## Implementación

- SHAP global
- SHAP local
- importancia de variables
- scouting reports

## Conclusión

El sistema deja de responder:

```text
¿Qué jugador aparece infravalorado?
```

para responder:

```text
¿Por qué aparece infravalorado?
```

---

# Sprint 5 — Scoring Multicriterio

## Problema identificado

La predicción por sí sola no genera recomendaciones operativas.

## Arquitectura

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
Ranking
```

## Fórmula

```python
opportunity_score = (
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
)
```

## Conclusión

El proyecto evoluciona desde predicción hacia priorización.

---

# Sprint 6 — Validación de Negocio

## Objetivo

Evaluar utilidad práctica del sistema.

## Métricas

- Precision@K
- ROI Simulation
- Positive ROI Rate
- Evaluación por liga
- Evaluación por posición

## Resultados

| K | Precision@K |
|---:|---:|
| 10 | 0.90 |
| 20 | 0.90 |
| 50 | 0.90 |
| 100 | 0.85 |

## Conclusión

Las recomendaciones mantienen alta calidad incluso ampliando el universo analizado.

---

# Sprint 8 — Reserved

Sprint reservado.

Las funcionalidades inicialmente previstas fueron absorbidas posteriormente por Sprint 9 para construir una única capa coherente de soporte a decisiones.

---

# Sprint 9.1 — Executive Scouting Layer

## Objetivo

Transformar rankings en una herramienta operativa.

## Implementación

- filtros ejecutivos
- presets de scouting
- segmentación dinámica
- exploración interactiva

## Resultado

Nacimiento de la capa de scouting interactivo.

---

# Sprint 9.2 — Executive Dashboard & Decision Support

## Objetivo

Construir una capa DSS orientada a dirección deportiva.

## Implementación

- matriz Coste vs Upside
- hallazgos ejecutivos
- KPIs
- priorización visual

## Resultado

La arquitectura evoluciona hacia:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Visual Analytics
↓
Decision Support
```

---

# Sprint 10.1 — Player Intelligence Layer

## Problema identificado

Un ranking no explica completamente el perfil deportivo de un jugador.

## Objetivo

Transformar oportunidades analíticas en análisis individuales.

## Implementación

### Player Radar MVP

MID / ATT

- minutos
- goles/90
- asistencias/90
- G+A/90
- Growth Score
- Confidence Score

DEF

- tackles/90
- interceptions/90
- blocks/90

GK

- save %
- clean sheets

### Positional Benchmarking

Comparación frente a:

- misma posición
- universo global

### Scouting Narrative

Interpretación automática del perfil.

## Conclusión

Nace formalmente la:

```text
Player Intelligence Layer
```

---

# Sprint 10.2 — FBref Advanced Audit

## Problema identificado

El radar MVP utiliza únicamente métricas disponibles en el dataset actual.

## Objetivo

Evaluar la viabilidad de enriquecer la señal deportiva.

## Tablas auditadas

- Shooting
- Defense
- Misc
- Playing Time
- Passing
- Possession
- Goal & Shot Creation

## Métricas identificadas

Alta prioridad:

- shots_per90
- shots_on_target_per90
- tackles_won_per90
- interceptions_per90
- blocks_per90
- fouls_drawn_per90
- crosses_per90

## Conclusión

La auditoría valida la viabilidad técnica del futuro:

```text
Advanced Football Radar
```

---

# Sprint 10.3 — Current Scouting Layer & Risk Framework

## Problema identificado

El sistema mezclaba evaluación histórica con recomendaciones actuales.

## Objetivo

Separar validación metodológica de uso operativo.

## Implementación

### Integración temporada 2025-2026

Dataset actualizado:

| Métrica | Valor |
|----------|----------:|
| Observaciones | 3.916 |
| Jugadores únicos | 2.136 |
| Temporadas | 2019-2020 → 2025-2026 |

---

### Reentrenamiento completo

Resultados finales:

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Growth OLS | 0.7287 | 0.9053 | 0.5258 |
| Tuned XGBoost | 0.7120 | 0.8892 | 0.5414 |

---

### Risk Framework

Problema:

```text
Alta oportunidad
≠
baja incertidumbre
```

Se introduce:

```text
Risk Score
```

para cuantificar riesgo asociado a cada oportunidad.

---

### Nueva arquitectura

```text
Historical Evaluation Layer
↓
Current Scouting Layer
↓
Player Intelligence Layer
↓
Decision Support Layer
↓
Scouting Intelligence
```

## Conclusión

Sprint 10.3 constituye la principal aportación metodológica de la release v1.0.0.

---

# Conclusión metodológica global

La evolución completa del proyecto muestra una transición progresiva desde:

```text
Predicción de valor de mercado
```

hacia:

```text
Scouting Intelligence Platform
```

Las principales contribuciones metodológicas son:

- integración multi-fuente FBref + Transfermarkt
- matching jerárquico reproducible
- panel longitudinal jugador-temporada
- comparación econometría vs Machine Learning
- explainability mediante SHAP
- scoring multicriterio
- validación mediante Precision@K
- dashboard ejecutivo
- Decision Support System
- Risk Framework
- Current Scouting Layer
- Player Intelligence Layer

---

## Conclusión principal

La capacidad predictiva es importante, pero no constituye el principal valor generado por el sistema.

El valor emerge de la combinación entre:

```text
Predicción
↓
Interpretabilidad
↓
Scoring
↓
Riesgo
↓
Player Intelligence
↓
Decision Support
```

La principal conclusión metodológica es que la separación explícita entre:

```text
Historical Evaluation Layer
↓
Current Scouting Layer
```

permite mantener rigor académico y, simultáneamente, generar recomendaciones operativas aplicables a contextos reales de scouting profesional.

La release v1.0.0 consolida la evolución del proyecto desde un ejercicio de modelización predictiva hacia una plataforma integral de Football Analytics orientada a identificación, priorización y evaluación de oportunidades de mercado.
