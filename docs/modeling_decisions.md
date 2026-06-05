# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release v1.1.0 — Recruitment Intelligence & Decision Support System.

El objetivo es justificar las decisiones desde una perspectiva:

* Econométrica.
* Machine Learning.
* Explainability.
* Scoring multicriterio.
* Evaluación de negocio.
* Football Analytics.
* Scouting cuantitativo.

---

# 🧠 Filosofía de modelización

El proyecto adopta una arquitectura híbrida donde la precisión predictiva no constituye el objetivo final.

La finalidad última es generar recomendaciones accionables para scouting y recruitment.

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
Recruitment Intelligence
↓
Decision Support System
```

Principio metodológico:

```text
Maximizar utilidad para scouting
y no únicamente métricas predictivas
```

---

# 📈 Decisiones econométricas

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

### Decisiones adoptadas

* Transformación logarítmica de la variable objetivo.
* Efectos fijos por liga.
* Efectos fijos por posición.
* Covarianza robusta HC3.
* Validación temporal estricta.

### Rol metodológico

```text
Benchmark interpretable
```

### Resultado

| Modelo     |    MAE |   RMSE |     R² |
| ---------- | -----: | -----: | -----: |
| Growth OLS | 0.7287 | 0.9053 | 0.5258 |

### Conclusión

OLS permanece como benchmark explicativo del sistema.

---

# 🤖 Decisiones de Machine Learning

## Modelos evaluados

* Random Forest.
* HistGradientBoosting.
* LightGBM.
* XGBoost.

## Diseño experimental

El pipeline incorpora:

* Validación temporal.
* ColumnTransformer.
* Imputación.
* Escalado.
* Codificación categórica.
* RandomizedSearchCV.
* MLflow.

## Resultado final

| Modelo        |        MAE |       RMSE |         R² |
| ------------- | ---------: | ---------: | ---------: |
| Tuned XGBoost | **0.7120** | **0.8892** | **0.5414** |

## Decisión

```text
Tuned XGBoost = modelo productivo
```

### Justificación

* Mejor MAE.
* Mejor RMSE.
* Mejor R².
* Robustez.
* Compatibilidad con SHAP.

---

# 🔍 Explainability

## Decisión principal

```text
SHAP = mecanismo oficial de interpretación
```

### Explainability global

Permite identificar:

* Feature Importance.
* SHAP Importance.
* Summary Plots.

### Explainability local

Permite explicar:

* Drivers positivos.
* Drivers negativos.
* Estimaciones individuales.

### Justificación

Las recomendaciones deben ser defendibles ante usuarios no técnicos.

---

# 🎯 Decisiones sobre scoring

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

Captura desviaciones entre:

```text
Valor esperado
vs
Valor observado
```

---

## Growth Score

Captura:

* Potencial.
* Trayectoria.
* Revalorización futura.

---

## Confidence Score

Captura:

* Calidad del matching.
* Robustez estadística.
* Estabilidad temporal.

---

## Opportunity Score

Implementación conceptual:

```python
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
```

### Decisión

Priorizar infravaloración sin ignorar potencial ni robustez.

---

# ⚠️ Risk Framework

Introducido durante Sprint 10.

Problema identificado:

```text
Alta oportunidad
≠
Recomendación segura
```

Se incorpora:

```text
Risk Score
```

### Objetivo

Cuantificar incertidumbre asociada a cada recomendación.

### Interpretación

| Riesgo | Significado           |
| ------ | --------------------- |
| Bajo   | Perfil estable        |
| Medio  | Riesgo moderado       |
| Alto   | Elevada incertidumbre |

### Resultado

```text
Opportunity Score
+
Risk Score
=
Priorización más realista
```

---

# 📋 Ranking Engine

Objetivo:

Transformar scores en recomendaciones priorizadas.

### Principio metodológico

Los rankings no sustituyen al scout.

Su función es:

```text
Reducir espacio de búsqueda
```

y facilitar procesos posteriores de análisis.

---

# 📊 Decisiones de evaluación

El proyecto adopta una visión más amplia que la evaluación tradicional.

## Métricas utilizadas

### Técnicas

* RMSE.
* MAE.
* R².

### Negocio

* Precision@K.
* Positive ROI Rate.
* Métricas de priorización.

### Principio

```text
Un modelo útil
no es únicamente
el que predice mejor
sino el que genera mejores decisiones
```

---

# 🔄 Historical Evaluation Layer

Objetivo:

Separar evaluación metodológica de explotación operativa.

### Funciones

* Comparación de modelos.
* Validación temporal.
* Backtesting.
* Análisis académico.

### Contribución

```text
Evaluación histórica
≠
Scouting operativo
```

Esta separación constituye una de las decisiones metodológicas más importantes del proyecto.

---

# ⚽ Player Intelligence

Introducida durante Sprint 10.

Problema identificado:

```text
Ranking
≠
Comprensión del perfil del jugador
```

### Solución

* Player Radar.
* Positional Benchmarking.
* Scouting Narrative.

### Resultado

```text
Player Intelligence Layer
```

---

# 🎯 Recruitment Intelligence

Introducida durante Sprint 11.

Problema identificado:

```text
Análisis individual
≠
Proceso real de recruitment
```

### Solución

* Recruitment Board.
* Candidate Selection System.
* Comparative Player Analysis.
* Executive Scouting Workflow.

### Resultado

```text
Recruitment Intelligence Layer
```

---

# 🖥️ Decision Support System

Consolidado durante Sprint 12.

Problema identificado:

```text
Análisis avanzado
≠
Adopción por usuarios finales
```

### Solución

* Advanced Search Engine.
* UX Redesign.
* Search Suggestions.
* Search Chips.
* Internationalization EN/ES.

### Resultado

```text
Decision Support System
```

---

# ⚖️ Trade-offs metodológicos

| Trade-off                         | Decisión             |
| --------------------------------- | -------------------- |
| Interpretabilidad vs precisión    | OLS + XGBoost        |
| Econometría vs ML                 | Arquitectura híbrida |
| Cobertura vs matching estricto    | Priorizar calidad    |
| Complejidad vs reproducibilidad   | Modularización       |
| Métrica técnica vs utilidad       | Precision@K          |
| Ranking automático vs scout       | Sistema de apoyo     |
| Evaluación histórica vs operación | Separación explícita |

---

# 🛡️ Prevención de leakage

Controles implementados:

* Validación temporal.
* Separación train/test.
* Exclusión de variables futuras.
* Scoring posterior a predicción.
* Persistencia independiente.

Principio:

```text
Toda variable utilizada como input
debe existir en el momento real
de la decisión.
```

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt.
* Ausencia de variables salariales.
* Ausencia de variables contractuales.

## Modelización

* Heterogeneidad entre posiciones.
* Posible drift temporal.
* Sensibilidad a cambios estructurales del mercado.

## Evaluación

* Precision@K basada en proxies.
* Ausencia de transferencias observadas.
* Backtesting limitado por disponibilidad histórica.

---

# 🛣️ Próximas líneas de investigación

## Sprint 13 — Multi-League Expansion

Ligas candidatas:

* Championship.
* Segunda División.
* Belgian Pro League.

---

## Sprint 14 — Transfer Strategy Engine

Posibles extensiones:

* Replacement Analysis.
* Portfolio Construction.
* Investment Optimization.
* Transfer Strategy Simulation.

---

# 🏁 Conclusión

La principal evolución metodológica del proyecto consiste en transformar una arquitectura centrada en predicción hacia una arquitectura orientada a decisión.

```text
Predicción
↓
Scoring
↓
Ranking
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
```

La combinación de econometría, Machine Learning, explainability y scoring multicriterio permite convertir modelos predictivos en herramientas operativas para scouting y recruitment profesional.

