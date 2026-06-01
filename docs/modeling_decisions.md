# 📊 Decisiones de modelización

<div align="center">

![Econometrics](https://img.shields.io/badge/Econometrics-OLS-green)
![Machine Learning](https://img.shields.io/badge/ML-Tuned%20XGBoost-blue)
![Scoring](https://img.shields.io/badge/Scoring-Engine-success)
![Ranking](https://img.shields.io/badge/Ranking-Automated-success)
![Validation](https://img.shields.io/badge/Validation-Temporal%20%2B%20Business-important)
![Interpretability](https://img.shields.io/badge/Interpretability-SHAP-success)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-blue)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo del documento](#-objetivo-del-documento)
- [⚙️ Filosofía de modelización](#️-filosofía-de-modelización)
- [📈 Decisiones econométricas](#-decisiones-econométricas)
- [🤖 Decisiones Machine Learning](#-decisiones-machine-learning)
- [🔍 Explainability](#-explainability)
- [💡 Decisiones sobre scoring](#-decisiones-sobre-scoring)
- [📊 Ranking Engine](#-ranking-engine)
- [📈 Decisiones de evaluación y negocio](#-decisiones-de-evaluación-y-negocio)
- [🎛️ Sprint 9.1 — Executive Scouting Layer](#️-sprint-91--executive-scouting-layer)
- [💎 Sprint 9.2 — Executive Dashboard & Visual Analytics](#-sprint-92--executive-dashboard--visual-analytics)
- [🎯 Precision@K](#-precisionk)
- [💰 ROI Simulation](#-roi-simulation)
- [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
- [🛡️ Prevención de leakage](#️-prevención-de-leakage)
- [📉 Limitaciones actuales](#-limitaciones-actuales)
- [🚀 Próximas decisiones previstas](#-próximas-decisiones-previstas)
- [🧠 Conclusión](#-conclusión)

---

# 🧠 Objetivo del documento

Este documento recoge las decisiones metodológicas adoptadas durante el desarrollo del sistema analítico y su justificación desde una perspectiva:

- econométrica
- Machine Learning
- explainability
- scoring multicriterio
- ranking systems
- evaluación de negocio
- sports analytics
- scouting cuantitativo
- reproducibilidad

El objetivo no es únicamente documentar qué modelos se han entrenado, sino explicar por qué se han elegido determinadas estrategias de modelización, cómo se han transformado las predicciones en señales de scouting y cómo se evalúa la utilidad real de dichas señales.

---

# ⚙️ Filosofía de modelización

El sistema adopta una arquitectura híbrida:

| Componente | Función |
|---|---|
| Growth OLS | Benchmark econométrico interpretable |
| Tuned XGBoost | Mejor modelo predictivo actual |
| SHAP | Interpretabilidad global y local |
| Scoring Engine | Transformación de predicciones en señales accionables |
| Ranking Engine | Generación automática de shortlists y rankings |
| Evaluation Layer | Validación estadística y de negocio |
| Business Layer | Simulación ROI y análisis de estrategia |
| Dashboard Layer | Visual analytics y soporte a decisiones |

Principio metodológico:

```text
maximizar utilidad de scouting
y no únicamente métricas predictivas
```

La decisión principal es tratar el proyecto como un sistema de soporte a decisiones, no como una competición aislada de modelos. Por tanto, las métricas de error son necesarias, pero no suficientes: deben complementarse con ranking diagnostics, Precision@K y simulación económica.

---

# 📈 Decisiones econométricas

## Modelo seleccionado

El modelo econométrico se plantea sobre el logaritmo del valor de mercado:

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

## Decisiones adoptadas

- uso de `log_market_value_eur` como target principal
- transformación logarítmica para reducir skewness y estabilizar varianza
- incorporación de fixed effects por liga y posición
- uso de HC3 robust covariance
- validación temporal estricta
- mantenimiento de OLS como benchmark interpretable

## Resultado de referencia

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |

## Rol dentro del sistema

```text
OLS = baseline interpretable y referencia econométrica
```

El modelo OLS permite explicar relaciones estructurales del mercado, como primas o descuentos asociados a determinadas ligas, posiciones y niveles de exposición competitiva. Aunque posteriormente el modelo ML tuned supera su rendimiento predictivo, OLS se mantiene como componente fundamental por su valor interpretativo.

---

# 🤖 Decisiones Machine Learning

## Pipeline principal

```text
src/models/machine_learning/train_ml_tuned.py
```

## Modelos evaluados

- Tuned Random Forest
- Tuned XGBoost
- Tuned LightGBM
- HistGradientBoosting

## Diseño experimental

El pipeline ML incorpora:

- validación temporal
- preprocesamiento con `ColumnTransformer`
- imputación de valores faltantes
- escalado de variables numéricas
- codificación categórica
- tuning con `RandomizedSearchCV`
- exportación de predicciones
- persistencia de artefactos
- tracking con MLflow

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Tuned Random Forest | 0.9076 | 0.7315 | 0.5200 |
| Tuned XGBoost | **0.8753** | **0.7004** | **0.5536** |
| Tuned LightGBM | 0.8864 | 0.7162 | 0.5421 |
| HistGradientBoosting | 0.8825 | 0.7118 | 0.5462 |

## Decisión

```text
Tuned XGBoost = modelo predictivo principal actual
```

## Justificación

Tuned XGBoost se adopta como modelo principal porque obtiene el mejor equilibrio entre:

- menor RMSE
- menor MAE
- mayor R²
- capacidad de capturar relaciones no lineales
- compatibilidad con interpretabilidad posterior mediante SHAP
- capacidad de generar predicciones persistibles para scoring

---

# 🔍 Explainability

## Métodos implementados

### Global

- comparación de feature importance
- SHAP global importance
- SHAP summary plots

### Local

- SHAP por jugador
- explicación individual de predicciones
- reportes scouting interpretables

## Decisión

```text
SHAP = mecanismo principal de interpretación del modelo ML
```

## Justificación

SHAP permite conectar el modelo predictivo con el caso de negocio, explicando por qué un jugador aparece como infravalorado y qué variables contribuyen positiva o negativamente a su valoración esperada.

Esto resulta clave para un entorno de scouting profesional, donde una recomendación cuantitativa debe ser defendible ante perfiles no técnicos como dirección deportiva o cuerpo de scouting.

---

# 💡 Decisiones sobre scoring

Sprint 5 introduce la capa de scoring como mecanismo para transformar predicciones en señales accionables.

## Arquitectura conceptual

```text
Predicciones
↓
Inefficiency Score
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Rankings
```

## Scripts implementados

```text
src/models/scoring/

build_inefficiency_score.py
build_growth_score.py
build_confidence_score.py
build_opportunity_score.py
generate_rankings.py
```

---

## Inefficiency Score

Definición conceptual:

```python
predicted_market_value_eur - market_value_eur
```

Rol:

- detectar posible infravaloración
- detectar posible sobrevaloración
- cuantificar gap entre valor esperado y observado

Interpretación:

| Score | Interpretación |
|---|---|
| Positivo | Posible infravaloración |
| Negativo | Posible sobrevaloración |

---

## Growth Score

Variables utilizadas:

- `market_value_growth_prev`
- `delta_log_market_value_prev`
- `breakout_indicator`
- `growth_index`
- `career_year`
- edad relativa

Objetivo:

```text
capturar potencial futuro y trayectoria de desarrollo
```

El Growth Score complementa la infravaloración actual con una dimensión dinámica. Esto evita priorizar únicamente jugadores baratos respecto al modelo, incorporando además señales de revalorización futura.

---

## Confidence Score

Componentes:

- `matching_confidence`
- fiabilidad por minutos jugados
- completitud de features
- estabilidad temporal

Objetivo:

```text
reducir falsos positivos y penalizar recomendaciones poco fiables
```

El Confidence Score reconoce que no todos los jugadores tienen el mismo nivel de fiabilidad analítica. Un perfil con pocos minutos, menor completitud de datos o peor calidad de matching debe recibir una penalización frente a perfiles más robustos.

---

## Opportunity Score

Implementación conceptual:

```python
opportunity_score =
0.55 * inefficiency_score_z
+ 0.25 * growth_score_z
+ 0.20 * confidence_score_z
```

## Justificación de pesos

| Componente | Peso | Justificación |
|---|---:|---|
| Inefficiency Score | 0.55 | Señal principal de infravaloración |
| Growth Score | 0.25 | Potencial futuro de revalorización |
| Confidence Score | 0.20 | Robustez y fiabilidad de la recomendación |

La decisión de dar mayor peso a la ineficiencia responde al objetivo principal del proyecto: detectar discrepancias entre valor esperado y valor observado. Growth y Confidence actúan como moduladores para mejorar utilidad de scouting.

---

# 📊 Ranking Engine

## Pipeline

```text
src/models/scoring/generate_rankings.py
```

## Outputs

```text
reports/rankings/

top_undervalued_global.csv
top_undervalued_by_league.csv
top_undervalued_by_position.csv
top_high_potential.csv
top_low_risk.csv
scouting_shortlist.csv
```

## Resultados actuales

| Métrica | Valor |
|---|---:|
| Observaciones scoreadas | 1,138 |
| Scouting targets | 53 |
| Alta prioridad + target | 376 |

## Decisión

Los rankings no sustituyen el criterio experto, sino que priorizan el universo de análisis. El sistema se interpreta como un filtro cuantitativo para reducir espacio de búsqueda y focalizar el trabajo del departamento de scouting.

---

# 📈 Decisiones de evaluación y negocio

Sprint 6 añade una capa de evaluación orientada a validar si los rankings son útiles desde una perspectiva estadística y de negocio.

## Scripts implementados

```text
src/models/evaluation/

build_ranking_diagnostics.py
build_roi_simulation.py
build_precision_at_k.py
```

## Outputs generados

```text
reports/model_diagnostics/

ranking_summary.csv
ranking_by_league.csv
ranking_by_position.csv
ranking_score_correlations.csv
ranking_tier_summary.csv
```

```text
reports/business/

roi_simulation.csv
roi_global_summary.csv
transfer_strategy_analysis.csv
roi_scouting_shortlist.csv
roi_scouting_shortlist_summary.csv
```

```text
reports/evaluation/

precision_at_k.csv
```

## Decisión metodológica

La evaluación del sistema no se limita a RMSE, MAE y R². Para un sistema de ranking de scouting, se incorporan métricas propias de priorización y negocio:

- Precision@K
- ROI esperado
- ROI ajustado por riesgo
- Positive ROI rate
- distribución por liga
- distribución por posición
- correlaciones entre scores

---

# 🎯 Precision@K

## Objetivo

Medir si los primeros jugadores del ranking concentran perfiles con evolución positiva posterior.

## Resultados actuales

| K | Jugadores | True Positive | Precision@K |
|---:|---:|---:|---:|
| 10 | 10 | 9 | 0.90 |
| 20 | 20 | 18 | 0.90 |
| 50 | 50 | 45 | 0.90 |
| 100 | 100 | 85 | 0.85 |

## Interpretación

El sistema mantiene una precisión elevada incluso ampliando el tamaño del ranking. Esto sugiere que el Opportunity Score no está generando únicamente ruido, sino que ordena perfiles con mayor probabilidad de evolución positiva.

## Advertencia metodológica

La variable de éxito futuro se basa en proxies longitudinales disponibles en el panel. Por tanto, Precision@K debe interpretarse como una validación preliminar de ranking, no como una evaluación causal ni como una validación totalmente independiente del sistema de scoring.

---

# 💰 ROI Simulation

## Objetivo

Estimar la utilidad económica potencial de las recomendaciones generadas.

## Hipótesis inicial

```python
buy_price = market_value_eur
sell_price = predicted_market_value_eur
```

Esta hipótesis fue considerada demasiado optimista.

## Hipótesis conservadora adoptada

Se introduce un factor de realización parcial:

```python
realization_factor = 0.5

assumed_sell_price_eur =
market_value_eur +
(predicted_market_value_eur - market_value_eur) * realization_factor
```

## Justificación

El valor estimado por el modelo no debe interpretarse como precio de venta garantizado. En mercados reales existen:

- costes de transacción
- incertidumbre contractual
- riesgo deportivo
- negociación
- liquidez limitada
- variabilidad del mercado

Por ello se adopta un escenario conservador, asumiendo que solo una parte del upside estimado llega a materializarse.

## Métricas generadas

- `expected_profit_eur`
- `expected_roi_pct`
- `risk_adjusted_profit_eur`
- `risk_adjusted_roi_pct`
- `positive_roi_rate`

## Lectura de negocio

La simulación ROI no busca predecir beneficios reales exactos, sino evaluar sensibilidad, priorización y atractivo relativo de segmentos de mercado, ligas y posiciones.

---


# 🎛️ Sprint 9.1 — Executive Scouting Layer

## Contexto

Tras completar las capas de modelización, scoring y validación de negocio, surgió una necesidad operativa:

```text
Los rankings siguen siendo demasiado extensos
para un proceso real de scouting.
```

Un departamento deportivo no evalúa simultáneamente más de mil jugadores.

Necesita construir shortlists dinámicas según contexto deportivo, presupuesto y estrategia de captación.

---

## Objetivo

Transformar el ranking analítico en una herramienta de scouting interactiva.

---

## Implementación

Se desarrolló una capa ejecutiva basada en filtros dinámicos.

### Presets de scouting

* Exploración completa
* Perfiles accionables
* Jóvenes élite
* Alto upside

### Filtros ejecutivos

* Liga
* Posición
* Edad máxima
* Minutos mínimos
* Opportunity Score
* Confidence Score
* Tier de oportunidad

---

## Resultado

La arquitectura evoluciona desde:

```text
Ranking
↓
Exportación CSV
```

hacia:

```text
Ranking
↓
Scouting Layer
↓
Shortlist dinámica
```

---

## Justificación metodológica

El objetivo no es únicamente identificar jugadores infravalorados.

El objetivo es permitir que diferentes perfiles deportivos puedan construir universos de scouting adaptados a sus necesidades.

---

# 💎 Sprint 9.2 — Executive Dashboard & Visual Analytics

## Contexto

Una vez resuelto el problema de segmentación del universo de jugadores, se abordó la visualización ejecutiva de resultados.

---

## Objetivo

Convertir los rankings y scores en información accionable para dirección deportiva.

---

## Implementación

### Matriz Coste vs Upside

Cada jugador se representa mediante:

```text
Eje X → valor actual
Eje Y → upside estimado
Tamaño → Opportunity Score
Color → prioridad scouting
```

---

### Segmentación estratégica

La matriz divide automáticamente el mercado en:

| Zona                  | Interpretación                 |
| --------------------- | ------------------------------ |
| Comprar / priorizar   | Bajo coste y alto upside       |
| Oportunidades premium | Alto upside con mayor coste    |
| Seguimiento           | Potencial interesante          |
| Menor prioridad       | Menor relación coste-potencial |

---

### Top 5 destacados

Identificación automática de los cinco perfiles más interesantes bajo los filtros activos.

---

### Hallazgos ejecutivos

Síntesis automática basada en:

* candidatos prioritarios
* oportunidades premium
* Opportunity Score medio
* upside agregado identificado
* liga dominante

---

### Tabla priorizada

Visualización ordenada mediante Opportunity Score.

---

## Arquitectura DSS

La arquitectura final evoluciona desde:

```text
Predicción
↓
Scoring
↓
Ranking
```

hacia:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Scouting Layer
↓
Visual Analytics
↓
Decision Support
↓
Scouting
```

---

## Justificación metodológica

La filosofía del proyecto pasa de maximizar precisión predictiva a maximizar utilidad para la toma de decisiones.

Por ello:

```text
Un modelo útil no es el que predice mejor.

Es el que ayuda a tomar mejores decisiones.
```

Sprint 9.2 constituye la primera implementación completa de un DSS (Decision Support System) aplicado al mercado de fichajes europeo.


---

# ⚖️ Trade-offs metodológicos

| Trade-off | Decisión |
|---|---|
| Interpretabilidad vs precisión | Arquitectura híbrida OLS + ML |
| OLS vs ML | OLS como benchmark; XGBoost como modelo predictivo |
| Cobertura vs matching estricto | Priorizar calidad y trazabilidad |
| Complejidad vs reproducibilidad | Modularización y configuración YAML |
| Métrica técnica vs utilidad de negocio | Incorporar Precision@K y ROI simulation |
| Optimismo vs realismo económico | ROI conservador con realization factor |
| Ranking automático vs criterio experto | Sistema como soporte, no sustituto |

---

# 🛡️ Prevención de leakage

## Controles implementados

- validación temporal
- exclusión de variables futuras en entrenamiento
- separación train/test
- separación entre features de modelización y outputs derivados
- persistencia de predicciones fuera del dataset base
- scoring posterior a la generación de predicciones

## Variables excluidas del entrenamiento

- `market_value_next_eur`
- `market_value_growth_1y`
- `delta_log_market_value_1y`
- `predicted_market_value_eur`
- `inefficiency_score`
- `opportunity_score`
- rankings derivados

## Principio general

```text
toda variable utilizada como input debe estar disponible en el momento real de decisión
```

## Nota sobre evaluación

Las variables futuras pueden utilizarse para evaluación posterior, como Precision@K, siempre que no entren en el proceso de entrenamiento ni en la generación original del ranking.

---

# 📉 Limitaciones actuales

## Datos

- no se han integrado todavía xG/xA de Understat
- las métricas defensivas avanzadas siguen limitadas
- no hay variables contractuales ni salariales
- Transfermarkt es proxy de valor, no precio real de transferencia

## Modelización

- posible dependencia del target respecto a reputación y exposición mediática
- muestra reducida tras filtros de calidad
- posible heterogeneidad por posición
- posible sensibilidad a outliers de mercado

## Scoring

- pesos del Opportunity Score definidos por criterio experto
- falta calibración automática de pesos
- Confidence Score aproximado
- ROI simulation depende de supuestos de realización

## Evaluación

- Precision@K usa proxy de crecimiento futuro
- no existe aún validación real contra transferencias ejecutadas
- no se ha realizado backtesting completo por ventana temporal móvil

---

# 🚀 Próximas decisiones previstas

## Prioridad alta

### Explainability avanzada

- integración SHAP en dashboard
- explicación visual de rankings
- drivers positivos y negativos
- interpretación ejecutiva por jugador

---

### Nuevos modelos

- CatBoost
- TabPFN
- comparación con XGBoost

---

### Validación avanzada

- backtesting temporal móvil
- estabilidad longitudinal del ranking
- robustness analysis
- calibración de Opportunity Score

---

## Prioridad media

### Enriquecimiento de datos

- integración Understat
- xG
- xA
- métricas defensivas avanzadas
- métricas de posesión

---

### Modelización específica

- modelos por posición
- modelos por liga
- calibración contextual

---

## Prioridad futura

### API Scoring

- scoring automatizado
- inferencia futura
- actualización periódica

### Monitoring

- data drift
- model drift
- performance tracking


---

# 🧠 Conclusión

El proyecto ha evolucionado desde:

```text
modelo predictivo de valor de mercado
```

hacia:

```text
sistema cuantitativo integral de scouting
```

La arquitectura actual integra de forma coherente múltiples capas analíticas:

* integración multi-fuente FBref + Transfermarkt
* matching reproducible y trazable
* modelización econométrica
* modelización Machine Learning
* explainability mediante SHAP
* scoring multicriterio
* generación automática de rankings
* validación estadística y de negocio
* simulación ROI
* Executive Scouting Layer
* Visual Analytics
* Decision Support System (DSS)

La decisión metodológica central del proyecto consiste en considerar que el valor generado no depende exclusivamente de la capacidad predictiva de un modelo.

En entornos reales de Football Analytics, una predicción aislada tiene utilidad limitada si no puede transformarse en una recomendación interpretable, priorizable y accionable para la toma de decisiones deportivas.

Por ello, la arquitectura fue evolucionando progresivamente:
```text
Sprint 5 convierte el modelo predictivo en un motor de scoring.

Sprint 6 introduce mecanismos de validación estadística y económica orientados a negocio.

Sprint 8 queda reservado tras la redefinición metodológica derivada de la tutoría académica, integrándose posteriormente sus objetivos dentro de una capa más amplia de soporte a decisiones.

Sprint 9.1 transforma el ranking estático en una herramienta interactiva de scouting mediante filtros ejecutivos y construcción dinámica de shortlists.

Sprint 9.2 incorpora una capa completa de Visual Analytics y Decision Support, permitiendo interpretar el mercado de fichajes desde una perspectiva estratégica basada en coste, upside y priorización de oportunidades.
```

La evolución completa del sistema puede resumirse como:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Executive Scouting Layer
↓
Visual Analytics
↓
Decision Support
↓
Scouting
```

El resultado final es una plataforma de Football Analytics orientada a la identificación de jugadores potencialmente infravalorados, capaz de combinar rigor metodológico, interpretabilidad y utilidad práctica para departamentos de scouting y dirección deportiva.

Más allá de la precisión predictiva obtenida por los modelos, la principal contribución del proyecto consiste en demostrar cómo técnicas de econometría, Machine Learning, explainability y analítica deportiva pueden integrarse dentro de un sistema DSS capaz de apoyar procesos reales de captación y evaluación de talento en el mercado de fichajes europeo.
