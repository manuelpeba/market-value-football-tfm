# 📖 Memoria Metodológica – Notas de Desarrollo

## Objetivo del documento

Este documento centraliza decisiones metodológicas, hipótesis, experimentos, resultados y conclusiones obtenidas durante el desarrollo de la plataforma:

```text
Market Value Dynamics and Market Inefficiency Detection
in Professional Football
```

Su propósito es servir como base para la redacción de la memoria académica final del TFM y documentar la evolución metodológica completa hasta la release:

```text
v1.2.1 — Advanced Data Expansion
```

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

La evolución metodológica real del sistema fue:

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
Decision Support Layer
↓
Current Scouting Layer
↓
Player Intelligence Layer
↓
Recruitment Intelligence Layer
↓
Decision Support System
↓
External Validation
↓
Advanced Data Expansion
```

La release v1.2.1 consolida esta evolución.

Sprint 13A aporta una validación explícita de la capacidad de generalización del sistema mediante expansión multi-liga.

Sprint 13B aporta una validación explícita del valor incremental de métricas avanzadas derivadas de rendimiento futbolístico.

Ambas contribuciones constituyen los principales avances metodológicos de la fase final del proyecto.

---

# Sprint 1 — Normalización contextual

## Hipótesis

La normalización por posición y competición podría mejorar la capacidad predictiva.

## Variables añadidas

* goals_per90_pos_z
* assists_per90_pos_z
* goals_position_percentile
* assists_position_percentile

Agrupación:

```text
[position_group, league]
```

## Resultados

| Modelo       |   RMSE |    MAE |     R² |
| ------------ | -----: | -----: | -----: |
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Advanced OLS | 1.0065 | 0.8166 | 0.4148 |

## Conclusión

Hipótesis rechazada.

La señal parecía ya capturada por efectos estructurales.

No obstante, estas variables se mantuvieron por su valor interpretativo y posterior reutilización dentro de capas de scouting.

---

# Sprint 2 — Growth Features

## Hipótesis

El mercado incorpora señales de trayectoria y crecimiento futuro.

## Variables

* market_value_growth_prev
* delta_log_market_value_prev
* age_squared
* career_year
* breakout_indicator

## Resultados

| Modelo       |   RMSE |    MAE |     R² |
| ------------ | -----: | -----: | -----: |
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Growth OLS   | 0.9046 | 0.7278 | 0.5255 |

## Conclusión

Hipótesis aceptada.

La trayectoria histórica constituye una señal clave para explicar valoraciones futuras.

Este resultado marca el primer salto metodológico relevante del proyecto.

---

# Sprint 3 — Composite Football Indices

## Hipótesis

La agregación de métricas futbolísticas podría mejorar rendimiento predictivo.

## Índices

* finishing_index
* playmaking_index
* progression_index
* defensive_index

## Resultados

Sin mejora estadísticamente relevante sobre Growth OLS.

## Conclusión

Mayor utilidad interpretativa que predictiva.

Los índices se conservaron por su valor para scouting, explainability y reporting.

---

# Sprint 4 — Machine Learning Baseline

## Hipótesis

Los modelos no lineales podrían superar a OLS.

## Resultados

| Modelo        |   RMSE |    MAE |     R² |
| ------------- | -----: | -----: | -----: |
| Random Forest | 1.0481 | 0.8527 | 0.3599 |
| XGBoost       | 1.0943 | 0.8801 | 0.3022 |
| LightGBM      | 1.1078 | 0.8936 | 0.2848 |

## Conclusión

Hipótesis inicialmente rechazada.

Las configuraciones baseline resultaron insuficientes para capturar la complejidad del problema.

---

# Sprint 4B — ML Pipeline Mejorado

## Mejoras introducidas

* validación temporal
* imputación robusta
* One-Hot Encoding
* RandomizedSearchCV
* MLflow
* preprocessing reproducible

## Resultados históricos

| Modelo        |   RMSE |    MAE |     R² |
| ------------- | -----: | -----: | -----: |
| Growth OLS    | 0.9046 | 0.7278 | 0.5255 |
| Tuned XGBoost | 0.8753 | 0.7004 | 0.5536 |

## Conclusión

Hipótesis aceptada.

Machine Learning supera consistentemente al benchmark econométrico.

---

# Sprint 4C — Explainability

## Implementación

* SHAP global
* SHAP local
* importancia de variables
* scouting reports

## Conclusión

El sistema deja de responder:

```text
¿Qué jugador aparece infravalorado?
```

para responder:

```text
¿Por qué aparece infravalorado?
```

Lo que incrementa notablemente la interpretabilidad y utilidad práctica de los modelos.

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

* Precision@K
* ROI Simulation
* Positive ROI Rate
* Evaluación por liga
* Evaluación por posición

## Resultados

|   K | Precision@K |
| --: | ----------: |
|  10 |        0.90 |
|  20 |        0.90 |
|  50 |        0.90 |
| 100 |        0.85 |

## Conclusión

Las recomendaciones mantienen calidad elevada incluso ampliando el universo de candidatos.

---

# Sprint 8 — Reserved

Sprint reservado.

Las funcionalidades inicialmente previstas fueron absorbidas posteriormente por Sprint 9 para construir una única capa coherente de soporte a decisiones.

---

# Sprint 9.1 — Executive Scouting Layer

## Objetivo

Transformar rankings en una herramienta operativa.

## Implementación

* filtros ejecutivos
* presets de scouting
* segmentación dinámica
* exploración interactiva

## Resultado

Nacimiento de la capa de scouting interactivo.

---

# Sprint 9.2 — Executive Dashboard & Decision Support

## Objetivo

Construir una capa DSS orientada a dirección deportiva.

## Implementación

* matriz Coste vs Upside
* hallazgos ejecutivos
* KPIs
* priorización visual

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

* minutos
* goles/90
* asistencias/90
* G+A/90
* Growth Score
* Confidence Score

DEF

* tackles/90
* interceptions/90
* blocks/90

GK

* save %
* clean sheets

### Positional Benchmarking

Comparación frente a:

* misma posición
* universo global

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

* Shooting
* Defense
* Misc
* Playing Time
* Passing
* Possession
* Goal & Shot Creation

## Conclusión

La auditoría valida la viabilidad técnica del futuro:

```text
Advanced Football Radar
```

y establece las bases metodológicas para Sprint 13B.

---

# Sprint 10.3 — Current Scouting Layer & Risk Framework

## Problema identificado

El sistema mezclaba evaluación histórica con recomendaciones actuales.

## Objetivo

Separar validación metodológica de uso operativo.

## Implementación

### Integración temporada 2025-2026

Dataset actualizado:

| Métrica          |                 Valor |
| ---------------- | --------------------: |
| Observaciones    |                 3.916 |
| Jugadores únicos |                 2.138 |
| Temporadas       | 2019-2020 → 2025-2026 |

### Reentrenamiento completo

Resultados finales v1.0.0:

| Modelo        |    MAE |   RMSE |     R² |
| ------------- | -----: | -----: | -----: |
| Growth OLS    | 0.7287 | 0.9053 | 0.5258 |
| Tuned XGBoost | 0.7120 | 0.8892 | 0.5414 |

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

Sprint 10.3 constituye la principal aportación metodológica de la release v1.0.0 y establece la separación formal entre evaluación académica y explotación operativa.

# Sprint 11 — Recruitment Intelligence Layer

## Problema identificado

Los rankings generados por el sistema permitían identificar oportunidades potenciales, pero seguían siendo insuficientes para apoyar procesos reales de recruitment.

La evaluación individual de candidatos requería múltiples consultas y comparaciones manuales.

## Objetivo

Transformar rankings analíticos en una herramienta operativa de recruitment.

## Implementación

### Recruitment Board

Nueva interfaz orientada a procesos reales de scouting.

Funcionalidades:

* selección múltiple de candidatos;
* construcción dinámica de shortlists;
* comparación simultánea de jugadores;
* análisis ejecutivo de perfiles.

### Candidate Selection System

Sistema diseñado para gestionar candidatos potenciales dentro de un mismo proceso de captación.

Capacidades:

* selección multijugador;
* shortlists temporales;
* comparación dinámica.

### Comparative Player Analysis

Comparación directa entre candidatos mediante:

* Opportunity Score;
* Risk Score;
* Confidence Score;
* Market Value;
* Predicted Value;
* Mispricing.

### Executive Scouting Workflow

Nueva secuencia metodológica:

```text id="z4e3lv"
Modelo
↓
Opportunity Detection
↓
Filtering
↓
Shortlisting
↓
Comparative Analysis
↓
Recruitment Decision
```

## Conclusión

La arquitectura evoluciona desde identificación de oportunidades hacia soporte explícito a procesos de recruitment.

Nace formalmente la:

```text id="gnv3r7"
Recruitment Intelligence Layer
```

---

# Sprint 12 — Productization & Internationalization Layer

## Problema identificado

La utilidad práctica del sistema dependía todavía de conocimientos técnicos relativamente elevados.

## Objetivo

Transformar el prototipo analítico en una aplicación DSS orientada a usuarios finales.

## Implementación

### Dashboard Productization

Mejoras introducidas:

* reorganización funcional;
* jerarquización visual;
* simplificación de navegación;
* optimización de experiencia de usuario.

### Global Search Engine

Capacidad de búsqueda por:

* jugador;
* club;
* liga;
* posición.

### Executive UX Layer

Incorporación de:

* guía rápida integrada;
* contexto activo de filtros;
* reducción de fricción operativa;
* optimización de workflows.

### Internationalization

Idiomas disponibles:

* Español.
* Inglés.

## Conclusión

La plataforma deja de comportarse como un prototipo analítico y pasa a funcionar como una herramienta DSS orientada a procesos reales de scouting y recruitment.

---

# Sprint 13A — Multi-League Expansion

## Problema identificado

La metodología había sido desarrollada y validada inicialmente sobre un universo limitado de competiciones.

Persistía una pregunta metodológica relevante:

```text id="s5kg5t"
¿La metodología mantiene su rendimiento
fuera del universo competitivo original?
```

## Objetivo

Evaluar explícitamente la capacidad de generalización de la metodología mediante expansión competitiva.

## Nuevas ligas incorporadas

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Segunda División de España

## Resultados estructurales

| Métrica             |  Valor |
| ------------------- | -----: |
| Ligas               |     11 |
| Temporadas          |      7 |
| Liga-temporada      |     77 |
| Observaciones FBref | 43.591 |
| Dataset modelizable |  5.527 |
| Match Rate global   | 75,97% |

## Conclusión

La expansión multi-liga incrementa significativamente la cobertura competitiva y establece la base necesaria para una evaluación formal de validez externa.

---

# Sprint 13A.1 — Coverage Audit & External Validation

## Hipótesis

La expansión competitiva no debería deteriorar el rendimiento predictivo de la metodología.

## Diseño experimental

Comparación:

```text id="9t6z6q"
Dataset 7 ligas
vs
Dataset 11 ligas
```

manteniendo la misma arquitectura de modelización.

## Resultados

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

## Resultado observado

La expansión multi-liga mejora simultáneamente:

* cobertura;
* representatividad;
* capacidad predictiva.

## Conclusión

Hipótesis aceptada.

Sprint 13A aporta evidencia favorable de validez externa y constituye una de las contribuciones metodológicas más relevantes del proyecto.

---

# Sprint 13B — Advanced Data Expansion

## Problema identificado

El modelo continuaba utilizando un conjunto relativamente limitado de variables deportivas agregadas.

La auditoría desarrollada durante Sprint 10.2 había identificado la existencia de información potencialmente relevante contenida en tablas avanzadas de FBref.

## Hipótesis

Las métricas avanzadas derivadas de rendimiento futbolístico contienen información adicional capaz de mejorar la estimación del valor de mercado esperado.

## Objetivo

Evaluar empíricamente el impacto de nuevas variables avanzadas derivadas de FBref sobre el rendimiento de modelos econométricos y de Machine Learning.

---

## Variables incorporadas

Sprint 13B introduce tres nuevas variables productivas:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables agregan información avanzada relacionada con:

* capacidad finalizadora;
* disponibilidad competitiva;
* actividad defensiva.

---

## Evaluación econométrica

### Comparación principal

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="1hyc6j"
ΔR² = +0.0044
```

Adicionalmente se observan mejoras simultáneas en:

* RMSE;
* MAE;
* AIC;
* BIC.

## Conclusión

Las nuevas variables aportan capacidad explicativa incremental dentro de la especificación econométrica.

---

## Evaluación Machine Learning

### Comparación

```text id="q8jw0f"
Feature Set A (v13A)

vs

Feature Set B (v13B)
```

### Resultados

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

### Hallazgo principal

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento aporta robustez metodológica adicional y reduce el riesgo de dependencia de una única familia de modelos.

---

## Explainability

Los análisis de importancia de variables realizados durante Sprint 13B muestran que:

```text id="a0x6v6"
finishing_index_v2
```

constituye la variable avanzada con mayor relevancia predictiva agregada.

Este resultado representa el principal hallazgo analítico del sprint.

---

## Promoción productiva

Se consideran promovidos a producción:

### Dataset

```text id="zjry8v"
player_season_modeling_v13b_productive_candidate.parquet
```

### Variables oficiales

* finishing_index_v2
* availability_index
* defensive_activity_index

### Modelos oficiales

```text id="b1x3l2"
Growth OLS v13B

Tuned XGBoost v13B
```

---

## Conclusión

Hipótesis aceptada.

Las métricas avanzadas derivadas de FBref aportan señal predictiva adicional tanto en econometría como en Machine Learning.

Sprint 13B constituye la principal contribución metodológica de la release v1.2.1.

---

# Sprint 13B.6 — Integración Scoring & Rankings

## Problema identificado

Tras completar la nueva capa de modelización se intentó integrar los resultados dentro del pipeline histórico de scoring.

## Arquitectura observada

El pipeline de scoring depende de variables enriquecidas como:

* market_value_growth_prev
* delta_log_market_value_prev
* growth_index
* career_year
* breakout_indicator
* matching_confidence

Sin embargo, el pipeline productivo v13B genera únicamente:

* predicted_log_market_value_ml
* predicted_market_value_ml_eur
* inefficiency_score_ml

## Resultado

Se identifica una separación estructural entre:

```text id="fhlmzi"
Modeling Pipeline
≠
Scoring Pipeline
```

## Evaluación metodológica

La integración completa requeriría construir:

```text id="9rx9cb"
scoring_dataset_v13b
```

mediante combinación explícita entre:

* dataset enriquecido;
* predicciones productivas v13B.

## Decisión

Se decide no ejecutar esta integración dentro de Sprint 13B.

Justificación:

1. No afecta a la validación de la hipótesis principal.
2. No altera resultados econométricos.
3. No altera resultados de Machine Learning.
4. Constituye un trabajo de integración independiente.
5. Presenta menor prioridad estratégica que Sprint 14.

---

# Backlog metodológico

## TM.2 — Scoring & Ranking Integration v13B

### Objetivo

Reconstruir la integración completa entre:

```text id="pzyw1n"
Predictions v13B
↓
Scoring Dataset v13B
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Risk Score
↓
Rankings v13B
↓
Stability Analysis
```

### Estado

```text id="l8sj4g"
Backlog documentado
```

### Observación

TM.2 se documenta como trabajo futuro y no implica la reapertura de Sprint 13B.

---

# Conclusiones metodológicas globales

La evolución metodológica del proyecto puede resumirse mediante la siguiente secuencia:

```text id="mfz1uk"
Predicción
↓
Machine Learning
↓
Explainability
↓
Scoring
↓
Decision Support
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
↓
External Validation
↓
Advanced Data Expansion
```

Los principales hallazgos obtenidos durante el desarrollo son:

### Sprint 2

La trayectoria histórica constituye una señal clave para explicar valoraciones futuras.

### Sprint 4B

Machine Learning supera consistentemente al benchmark econométrico.

### Sprint 4C

La interpretabilidad resulta crítica para adopción operativa.

### Sprint 5

La predicción aislada no genera decisiones accionables.

### Sprint 10.3

La separación entre evaluación histórica y scouting operativo mejora la coherencia metodológica.

### Sprint 13A

La expansión competitiva mejora simultáneamente cobertura y capacidad predictiva.

### Sprint 13B

Las métricas avanzadas derivadas de FBref aportan capacidad explicativa incremental consistente.

---

# Estado metodológico final

Release actual:

```text id="1ygpf5"
v1.2.1 — Advanced Data Expansion
```

Estado:

```text id="ryz9k5"
Sprint 13A — COMPLETADO

Sprint 13B — COMPLETADO

Hipótesis Sprint 13B — VALIDADA

TM.2 — BACKLOG

Sprint 14 — SIGUIENTE FASE
```

La arquitectura metodológica desarrollada proporciona una base sólida, reproducible y académicamente consistente para la identificación de ineficiencias de mercado en fútbol profesional mediante econometría, Machine Learning y analítica deportiva avanzada.
