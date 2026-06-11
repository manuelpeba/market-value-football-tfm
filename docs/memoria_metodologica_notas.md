# 📖 Memoria Metodológica – Notas de Desarrollo

## Objetivo del documento

Este documento centraliza decisiones metodológicas, hipótesis, experimentos, resultados y conclusiones obtenidas durante el desarrollo de la plataforma:

```text
Market Value Dynamics and Market Inefficiency Detection
in Professional Football
```

Su propósito es servir como base para la redacción de la memoria académica final del TFM y documentar la evolución metodológica completa hasta la release:

```text
v1.2.2 — Transfer Strategy Engine
```

---

# Metodología general

El proyecto sigue una adaptación de CRISP-DM:

1. Comprensión de negocio.
2. Comprensión de datos.
3. Preparación de datos.
4. Modelización.
5. Evaluación.
6. Despliegue.

La ejecución se desarrolló mediante ciclos iterativos de investigación aplicada:

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

Cada sprint representa una hipótesis metodológica explícita evaluada mediante evidencia empírica.

---

# Evolución conceptual del proyecto

La evolución metodológica real del sistema puede resumirse mediante:

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
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

La evolución del proyecto puede interpretarse como una transición progresiva:

```text
Model Prediction
↓
Opportunity Detection
↓
Scouting Intelligence
↓
Recruitment Intelligence
↓
Strategic Decision Support
```

---

# Principio metodológico central

El proyecto no persigue únicamente maximizar precisión predictiva.

La hipótesis metodológica principal puede resumirse mediante:

```text
Un modelo útil para fútbol profesional
no es necesariamente el modelo
con mayor R²,

sino aquel que genera
mejores decisiones deportivas.
```

Por este motivo, la evolución del sistema incorpora progresivamente conceptos procedentes de:

* Econometría aplicada.
* Machine Learning.
* Explainability.
* Sports Economics.
* Football Analytics.
* Recruitment Analytics.
* Decision Science.
* Operations Research.

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

La señal parecía ya capturada por efectos estructurales incluidos dentro de la especificación.

No obstante, estas variables se conservaron por su utilidad posterior dentro de las capas de scouting, benchmarking posicional y visualización.

---

# Sprint 2 — Growth Features

## Hipótesis

El mercado incorpora señales de trayectoria y crecimiento futuro.

## Variables incorporadas

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

La trayectoria histórica constituye una señal crítica para explicar valoraciones futuras.

Este sprint representa el primer salto metodológico relevante del proyecto.

---

# Sprint 3 — Composite Football Indices

## Hipótesis

La agregación de métricas futbolísticas podría mejorar rendimiento predictivo.

## Índices desarrollados

* finishing_index
* playmaking_index
* progression_index
* defensive_index

## Resultados

No se observan mejoras estadísticamente relevantes respecto a Growth OLS.

## Conclusión

Hipótesis parcialmente rechazada.

Los índices muestran mayor utilidad interpretativa que predictiva.

Sin embargo, se conservaron por su contribución a:

* explainability;
* scouting;
* benchmarking;
* reporting ejecutivo.

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

Las configuraciones baseline no fueron capaces de capturar adecuadamente la complejidad del problema.

---

# Sprint 4B — ML Pipeline Mejorado

## Mejoras introducidas

* validación temporal;
* imputación robusta;
* One-Hot Encoding;
* RandomizedSearchCV;
* MLflow;
* preprocessing reproducible.

## Resultados

| Modelo        |   RMSE |    MAE |     R² |
| ------------- | -----: | -----: | -----: |
| Growth OLS    | 0.9046 | 0.7278 | 0.5255 |
| Tuned XGBoost | 0.8753 | 0.7004 | 0.5536 |

## Conclusión

Hipótesis aceptada.

Machine Learning supera consistentemente al benchmark econométrico cuando se acompaña de un pipeline adecuado de validación y optimización.

---

# Sprint 4C — Explainability

## Problema identificado

La mejora predictiva obtenida mediante Machine Learning reduce interpretabilidad.

## Implementación

* SHAP global;
* SHAP local;
* importancia de variables;
* scouting reports.

## Conclusión

La plataforma deja de responder únicamente:

```text
¿Qué jugador parece infravalorado?
```

para responder también:

```text
¿Por qué parece infravalorado?
```

Este sprint constituye un requisito fundamental para la adopción práctica de la metodología por parte de usuarios finales.

# Sprint 5 — Scoring Multicriterio

## Problema identificado

La predicción por sí sola no genera recomendaciones operativas.

Conocer el valor esperado de un jugador no permite decidir automáticamente si merece ser priorizado dentro de un proceso de scouting.

---

## Arquitectura propuesta

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

---

## Fórmula implementada

```python
opportunity_score = (
    0.55 * inefficiency_score_z +
    0.25 * growth_score_z +
    0.20 * confidence_score_z
)
```

---

## Conclusión

La arquitectura evoluciona desde:

```text
Prediction System
```

hacia:

```text
Opportunity Detection System
```

---

# Sprint 6 — Business Evaluation Layer

## Problema identificado

Las métricas predictivas tradicionales no permiten evaluar utilidad práctica.

---

## Objetivo

Evaluar capacidad real del sistema para identificar oportunidades de mercado.

---

## Métricas incorporadas

* Precision@K
* Positive ROI Rate
* ROI Simulation
* Evaluación por liga
* Evaluación por posición

---

## Resultados

|   K | Precision@K |
| --: | ----------: |
|  10 |        0.90 |
|  20 |        0.90 |
|  50 |        0.90 |
| 100 |        0.85 |

---

## Conclusión

Las recomendaciones mantienen elevada calidad incluso ampliando significativamente el universo de candidatos.

Este sprint introduce una visión orientada a negocio complementaria a la evaluación estadística tradicional.

---

# Sprint 8 — Reserved

Sprint reservado.

Las funcionalidades inicialmente previstas fueron absorbidas posteriormente por Sprint 9 para construir una única capa coherente de soporte a decisiones.

---

# Sprint 9 — Decision Support Layer

## Problema identificado

Los rankings seguían siendo insuficientes para usuarios finales.

---

## Objetivo

Transformar resultados analíticos en una herramienta de apoyo a decisiones.

---

## Implementación

### Executive Scouting Layer

* filtros ejecutivos;
* presets de scouting;
* segmentación dinámica;
* exploración interactiva.

### Executive Dashboard

* KPIs;
* matriz Coste vs Upside;
* priorización visual;
* hallazgos ejecutivos.

---

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

# Sprint 10 — Player Intelligence

## Problema identificado

Un ranking no explica completamente el perfil deportivo de un jugador.

---

## Objetivo

Transformar oportunidades analíticas en inteligencia deportiva.

---

## Implementación

### Player Radar

Visualización multidimensional del perfil.

### Positional Benchmarking

Comparación contextualizada frente a jugadores equivalentes.

### Opportunity vs Risk Matrix

Análisis conjunto de potencial y riesgo.

### Scouting Narrative

Interpretación automática del perfil.

---

## Risk Framework

Problema identificado:

```text
Alta oportunidad
≠
Baja incertidumbre
```

Solución:

```text
Risk Score
```

---

## Resultado

Nace formalmente la:

```text
Player Intelligence Layer
```

y se establece la separación metodológica entre:

```text
Historical Evaluation Layer
↓
Current Scouting Layer
```

---

# Sprint 11 — Recruitment Intelligence

## Problema identificado

Los rankings y análisis individuales seguían siendo insuficientes para procesos reales de recruitment.

---

## Objetivo

Transformar inteligencia individual en procesos estructurados de captación.

---

## Implementación

### Recruitment Board

* selección múltiple;
* shortlists dinámicas;
* análisis colectivo.

### Candidate Selection System

* gestión de candidatos;
* comparación simultánea;
* priorización ejecutiva.

### Comparative Player Analysis

Comparación directa mediante:

* Opportunity Score;
* Risk Score;
* Confidence Score;
* Market Value;
* Predicted Value;
* Market Mispricing.

---

## Resultado

La arquitectura evoluciona hacia:

```text
Recruitment Intelligence Layer
```

---

# Sprint 12 — Productization & Internationalization

## Problema identificado

La utilidad práctica seguía dependiendo de conocimientos técnicos relativamente elevados.

---

## Objetivo

Transformar el prototipo analítico en una herramienta DSS utilizable por usuarios finales.

---

## Implementación

### Productization

* reorganización funcional;
* simplificación de navegación;
* mejora de experiencia de usuario.

### Internationalization

Idiomas disponibles:

* Español.
* Inglés.

### Global Search Engine

Búsqueda por:

* jugador;
* club;
* liga;
* posición.

---

## Conclusión

La plataforma deja de comportarse como un prototipo analítico y pasa a funcionar como una aplicación DSS operativa.

---

# Sprint 13A — Multi-League Expansion

## Problema identificado

La metodología había sido validada sobre un universo competitivo relativamente limitado.

Pregunta metodológica:

```text
¿La metodología mantiene su rendimiento
fuera del universo original?
```

---

## Objetivo

Evaluar explícitamente la capacidad de generalización del sistema.

---

## Nuevas ligas incorporadas

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Segunda División de España

---

## Resultados estructurales

| Métrica             |  Valor |
| ------------------- | -----: |
| Ligas               |     11 |
| Temporadas          |      7 |
| Liga-temporada      |     77 |
| Observaciones FBref | 43.591 |
| Dataset modelizable |  5.527 |
| Match Rate global   | 75,97% |

---

## Conclusión

La expansión multi-liga incrementa significativamente la cobertura competitiva y fortalece la validez externa de la metodología.

---

# Sprint 13A.1 — Coverage Audit & External Validation

## Hipótesis

La expansión competitiva no debería deteriorar el rendimiento predictivo.

---

## Resultados

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

---

## Conclusión

Hipótesis aceptada.

La expansión multi-liga mejora simultáneamente:

* cobertura;
* representatividad;
* capacidad predictiva.

Resultado principal:

```text
Tuned XGBoost
RMSE = 0.8525
MAE  = 0.6834
R²   = 0.5664
```

Este experimento constituye la principal evidencia de validez externa de la metodología desarrollada y representa el mejor rendimiento predictivo alcanzado durante el proyecto.


---

# Sprint 13B — Advanced Data Expansion

## Problema identificado

El conjunto de variables deportivas seguía siendo relativamente limitado.

---

## Hipótesis

Las métricas avanzadas derivadas de FBref contienen señal predictiva adicional.

---

## Variables incorporadas

* finishing_index_v2
* availability_index
* defensive_activity_index

---

## Evaluación econométrica

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

---

## Evaluación Machine Learning

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

Resultado productivo final:

```text
Tuned XGBoost v13B

RMSE = 0.9639
MAE  = 0.7777
R²   = 0.4453
```

Las mejoras observadas se calculan respecto al Feature Set A (v13A) utilizando exactamente el mismo diseño experimental, por lo que deben interpretarse como mejoras incrementales internas del experimento Sprint 13B y no como una comparación directa frente a la validación externa multi-liga de Sprint 13A.1.

---

## Hallazgo principal

```text
finishing_index_v2
```

se identifica como la variable avanzada con mayor relevancia predictiva agregada.

---

## Conclusión

Hipótesis aceptada.

Las métricas avanzadas derivadas de FBref aportan capacidad explicativa incremental tanto en econometría como en Machine Learning.

---

# Sprint 14 — Transfer Strategy Engine

## Problema identificado

Hasta Sprint 13 la plataforma respondía principalmente:

```text
¿Qué jugadores parecen infravalorados?
```

Sin embargo, los clubes no fichan jugadores de forma aislada.

Las decisiones reales se producen bajo restricciones simultáneas de:

* presupuesto;
* posiciones necesarias;
* calidad mínima;
* número máximo de incorporaciones;
* perfil estratégico.

---

## Objetivo

Transformar la arquitectura desde:

```text
Player Selection
```

hacia:

```text
Portfolio Selection
```

---

## Implementación

### Transfer Portfolio Dataset

Nueva capa orientada a optimización.

### Binary Integer Programming

Implementación mediante:

```text
PuLP
```

### Restricciones

* presupuesto máximo;
* utilización mínima del presupuesto;
* posiciones requeridas;
* número máximo de fichajes.

### Escenarios

* Conservative
* Balanced
* Aggressive

---

## Conclusión

Sprint 14 introduce formalmente:

* Decision Science;
* Operations Research;
* Portfolio Optimization.

Constituye la principal evolución conceptual del proyecto.

---

# Sprint 14.1 — Player Level Layer

## Problema identificado

```text
Alto ROI
≠
Nivel deportivo suficiente
```

---

## Objetivo

Introducir una capa explícita de segmentación de calidad.

---

## Implementación

### Niveles

* Development Prospect
* Rotation Profile
* First Team Ready
* Key Player Profile
* Elite Target

### Restricción adicional

```text
Minimum Player Level
```

integrada dentro del optimizador.

---

## Resultado

La optimización incorpora simultáneamente:

* valor económico;
* potencial de crecimiento;
* nivel competitivo.

---

## Conclusión

La arquitectura incrementa significativamente su realismo deportivo.

---

# TM.2 — Multi-League DSS Integration

## Problema identificado

Tras Sprint 13A y Sprint 13B, la cobertura de modelización había sido ampliada a once competiciones europeas.

Sin embargo, parte de la capa DSS seguía operando sobre artefactos heredados construidos sobre la versión anterior de siete ligas.

Situación observada:

```text
Modeling Layer
↓
11 ligas

Scoring / Ranking DSS
↓
7 ligas
```

---

## Decisión metodológica

Implementar una capa explícita de reintegración de variables dentro del pipeline de scoring.

Arquitectura resultante:

```text
Predictions
↓
Scoring Feature Reintegration
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Ranking Engine
↓
Transfer Strategy Engine
```

---

## Resultado

Cobertura final:

```text
Modeling Layer
↓
11 ligas

Scoring Layer
↓
11 ligas

Opportunity Layer
↓
11 ligas

Ranking Engine
↓
11 ligas

Transfer Strategy Engine
↓
11 ligas

Decision Support System
↓
11 ligas
```

---

## Conclusión

TM.2 garantiza consistencia metodológica completa entre modelización y DSS sin alterar resultados econométricos, modelos Machine Learning ni lógica de scoring.

---

# Conclusiones metodológicas globales

La evolución metodológica del proyecto puede resumirse mediante:

```text
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
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

---

## Principales hallazgos

### Sprint 2

La trayectoria histórica constituye una señal crítica para explicar valoraciones futuras.

### Sprint 4B

Machine Learning supera consistentemente al benchmark econométrico.

### Sprint 4C

La interpretabilidad resulta imprescindible para adopción operativa.

### Sprint 5

La predicción aislada no genera decisiones accionables.

### Sprint 10

La separación entre evaluación histórica y scouting operativo mejora coherencia metodológica.

### Sprint 13A

La expansión competitiva fortalece simultáneamente cobertura y validez externa.

### Sprint 13B

Las métricas avanzadas derivadas de FBref aportan capacidad explicativa incremental consistente.

### Sprint 14

La optimización de carteras representa una evolución superior a la selección individual de jugadores.

### Sprint 14.1

Las restricciones explícitas de calidad mejoran el realismo deportivo del sistema.

---

# Estado metodológico final

Release actual:

```text
v1.2.2 — Transfer Strategy Engine
```

Estado:

```text
Sprint 13A — COMPLETADO
Sprint 13A.1 — COMPLETADO
Sprint 13B — COMPLETADO
Sprint 14 — COMPLETADO
Sprint 14.1 — COMPLETADO

TM.2 — COMPLETADO
```
Resultado histórico máximo:

```text
Tuned XGBoost
R² = 0.5664
```

Modelo productivo actual:

```text
Tuned XGBoost v13B
R² = 0.4453
```


La arquitectura metodológica desarrollada proporciona una base reproducible, interpretable y académicamente consistente para la identificación de ineficiencias de mercado, el scouting cuantitativo y la optimización estratégica de decisiones de fichaje en fútbol profesional.
