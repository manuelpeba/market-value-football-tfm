# 📌 Estado del proyecto

![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Modeling](https://img.shields.io/badge/Modeling-OLS%20%2B%20ML-blue)
![Matching](https://img.shields.io/badge/Matching-88.36%25-brightgreen)
![Dataset](https://img.shields.io/badge/Dataset-1%2C138%20scored-orange)
![Tracking](https://img.shields.io/badge/Experiment%20Tracking-MLflow-success)
![Config](https://img.shields.io/badge/Configuration-Centralized-blueviolet)
![Status](https://img.shields.io/badge/Status-Scouting%20Dashboard-success)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![DecisionSupport](https://img.shields.io/badge/Decision%20Support-System-success)
![VisualAnalytics](https://img.shields.io/badge/Visual%20Analytics-Executive-success)
![Version](https://img.shields.io/badge/version-v0.8.0--Executive--Dashboard-blue)
![Explainability](https://img.shields.io/badge/Explainability-SHAP-success)


---


# 📑 Tabla de contenidos

-   [🧠 Resumen ejecutivo](#-resumen-ejecutivo)
-   [📚 Estado CRISP-DM](#-estado-crisp-dm)
-   [🔄 Evolución de arquitectura](#-evolución-de-arquitectura)
-   [🏗️ Arquitectura actual del
    sistema](#️-arquitectura-actual-del-sistema)
-   [⚙️ Configuración centralizada](#️-configuración-centralizada)
-   [🧪 Experiment tracking con
    MLflow](#-experiment-tracking-con-mlflow)
-   [⚠️ Problema crítico del proyecto](#️-problema-crítico-del-proyecto)
-   [🛠️ Sistema de matching
    implementado](#️-sistema-de-matching-implementado)
-   [📈 Resultados del matching](#-resultados-del-matching)
-   [📊 Dataset final de modelización](#-dataset-final-de-modelización)
-   [📈 Estado del pipeline
    econométrico](#-estado-del-pipeline-econométrico)
-   [🤖 Estado del pipeline Machine
    Learning](#-estado-del-pipeline-machine-learning)
-   [💡 Estado del scoring pipeline](#-estado-del-scoring-pipeline)
-   [📊 Estado del evaluation
    pipeline](#-estado-del-evaluation-pipeline)
-   [📤 Outputs generados](#-outputs-generados)
-   [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
-   [🧱 Deuda técnica actual](#-deuda-técnica-actual)
-   [🚀 Próximos pasos](#-próximos-pasos)
-   [🧠 Conclusión](#-conclusión)

---

# 🧠 Resumen ejecutivo

El proyecto desarrolla un sistema analítico modular para identificar
jugadores infravalorados en el mercado de fichajes europeo mediante
modelos econométricos y Machine Learning aplicados al valor de mercado
de futbolistas.

El sistema se basa en:

-   integración robusta de múltiples fuentes
-   feature engineering deportivo
-   econometría aplicada
-   validación temporal out-of-sample
-   analytics engineering
-   scouting cuantitativo
-   experiment tracking reproducible
-   configuración centralizada desacoplada

---

## 📊 Estado actual del sistema

| Métrica | Valor |
|---|---:|
| Observaciones panel | 23,580 |
| Dataset modelizable | 3,297 |
| Jugadores únicos | 1,847 |
| Cobertura temporal | 2019-2020 → 2024-2025 |
| Ligas | 7 |
| Match rate | 88.36% |

---

## ✅ Capacidades actuales

El sistema ya permite:

-   estimar valor de mercado esperado
-   calcular Inefficiency Score
-   generar rankings de scouting
-   generar Opportunity Score multicriterio
-   comparar OLS vs Machine Learning
-   producir predicciones out-of-sample
-   persistir modelos entrenados
-   generar outputs reproducibles
-   registrar experimentos automáticamente con MLflow
-   versionar configuraciones de entrenamiento
-   desacoplar parámetros mediante configuración YAML

---

## 📌 Estado global

El proyecto ya ha superado las fases técnicamente más complejas
relacionadas con:

``` text
integración de fuentes
matching
pipeline reproducible
validación temporal
modelización base
tracking experimental
configuración desacoplada
```

Actualmente el principal cuello de botella ya no es arquitectónico,
sino:

``` text
feature engineering y calidad de señal predictiva
```

---

# 📚 Estado CRISP-DM

## Fase actual

``` text
Evaluation → Decision Support → Visual Analytics
```

---

## ✅ Fases completadas

### Business Understanding

-   definición del problema de scouting
-   definición de objetivos empresariales
-   framing econométrico
-   definición de outputs de negocio

---

### Data Understanding

-   análisis exploratorio
-   análisis de distribuciones
-   estudio de sesgos
-   evaluación de calidad
-   análisis de cobertura

---

### Data Preparation

-   feature engineering inicial
-   normalización
-   matching
-   construcción del panel
-   dataset modelizable
-   control de leakage

---

## 🔄 Fases en curso

### Modeling

-   pipeline econométrico final
-   pipeline ML supervisado
-   scoring automático
-   tracking experimental
-   persistencia de artefactos

---

### Evaluation

-   validación temporal
-   robustness checks
-   estabilidad de rankings
-   análisis comparativo OLS vs ML

---

## ⏳ Próximas fases

### Deployment

Completado parcialmente:

- dashboard interactivo
- visual analytics de scouting
- decision support system

Pendiente:

- API scoring
- scouting reports automáticos
- despliegue productivo

## Sprint 1 --- Positional Normalization (Completed)

### Sprint 1A

Status: Completed

Objetivo:

Implementar normalización contextual por posición y liga.

Variables creadas:

-   goals_per90_pos_z
-   assists_per90_pos_z
-   shots_per90_pos_z
-   goals_position_percentile
-   assists_position_percentile

Agrupación:

``` text
[position_group, league]
```

Implementaciones:

-   pipeline desacoplado
-   logging
-   MLflow tracking
-   generación automática de dataset avanzado

Output:

``` text
data/processed/player_season_modeling_advanced.parquet
```

---

### Sprint 1B

Status: Completed

Objetivo:

Evaluar impacto predictivo sobre el modelo OLS.

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Advanced Positional OLS | 1.0065 | 0.8166 | 0.4148 |

Decisión:

Las nuevas variables no serán incorporadas al modelo econométrico final
debido a ausencia de mejora predictiva.

---

## Sprint 2 --- Temporal Dynamics (Completed)

### Sprint 2A

Status: Completed

Objetivo:

Introducir variables que capturen trayectoria y crecimiento profesional.

Variables implementadas:

-   market_value_growth_prev
-   delta_log_market_value_prev
-   age_squared
-   career_year
-   breakout_indicator

Implementaciones:

-   pipeline desacoplado
-   logging
-   MLflow tracking
-   generación automática de dataset enriquecido

Output:

``` text
data/processed/player_season_modeling_growth.parquet
```

---

### Sprint 2B

Status: Completed

Objetivo:

Evaluar impacto de las variables temporales sobre el modelo OLS.

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |

Resultado:

Incremento significativo del rendimiento predictivo.

Decisión:

Growth OLS se adopta como nueva especificación econométrica candidata.

---

## Sprint 3 --- Composite Football Indices (Completed)

### Sprint 3A

Status: Completed

Objetivo:

Crear indicadores agregados de rendimiento futbolístico.

Variables implementadas:

-   finishing_index
-   playmaking_index
-   growth_index
-   experience_index

Implementaciones:

-   pipeline desacoplado
-   logging
-   MLflow tracking
-   generación automática de dataset enriquecido

Output:

``` text
data/processed/player_season_modeling_indices.parquet
```

---

### Sprint 3B

Status: Completed

Objetivo:

Evaluar el impacto de los índices agregados sobre el modelo
econométrico.

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Growth OLS + Indices | 0.9046 | 0.7278 | 0.5255 |

Resultado:

No se observó mejora predictiva.

Decisión:

Los índices se mantienen para interpretabilidad y análisis de scouting.

---

## Sprint 4 --- Machine Learning Baseline (Completed)

### Sprint 4A

Status: Completed

Objetivo:

Comparar modelos supervisados con el benchmark econométrico.

Modelos:

-   Random Forest
-   XGBoost
-   LightGBM

Split:

``` text
Train: temporadas <2023
Test: temporadas >=2023
```

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Random Forest | 1.0481 | 0.8527 | 0.3599 |
| XGBoost | 1.0943 | 0.8801 | 0.3022 |
| LightGBM | 1.1078 | 0.8936 | 0.2848 |

Conclusión:

El benchmark econométrico mantiene mejor rendimiento predictivo.

---

## Sprint 4B --- Improved ML Pipeline (Completed)

Status: Completed

### Objetivo

Mejorar el pipeline de Machine Learning baseline mediante tuning de
hiperparámetros, preprocesamiento robusto y tracking experimental
completo.

### Implementación

Archivo principal:

``` text
src/models/machine_learning/train_ml_tuned.py
```

### Mejoras introducidas

-   validación temporal `train < 2023 / test >= 2023`
-   preprocesamiento con `ColumnTransformer`
-   imputación con `SimpleImputer`
-   escalado con `StandardScaler`
-   codificación categórica con `OneHotEncoder`
-   tuning mediante `RandomizedSearchCV`
-   registro de experimentos con MLflow
-   exportación de feature importance

### Modelos entrenados

-   Tuned Random Forest
-   Tuned XGBoost
-   Tuned LightGBM
-   HistGradientBoosting

### Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Tuned Random Forest | 0.9076 | 0.7315 | 0.5200 |
| Tuned XGBoost | **0.8753** | **0.7004** | **0.5536** |
| Tuned LightGBM | 0.8864 | 0.7162 | 0.5421 |
| HistGradientBoosting | 0.8825 | 0.7118 | 0.5462 |

### Resultado principal

El modelo con mejor rendimiento actual es:

``` text
Tuned XGBoost
```

con:

``` text
R² = 0.5536
```

### Decisión

El Sprint 4B modifica la lectura metodológica del proyecto:

``` text
ML tuned supera al benchmark econométrico Growth OLS
```

Por tanto:

-   OLS se mantiene como benchmark interpretable.
-   XGBoost tuned pasa a ser el mejor modelo predictivo actual.
-   La siguiente fase debe centrarse en explainability y feature
    importance.

### Implicación metodológica

El resultado valida la utilidad de modelos no lineales siempre que se
combinen con:

-   tuning controlado
-   validación temporal
-   preprocesamiento reproducible
-   tracking experimental
-   control de artefactos

### Próximo sprint

``` text
Sprint 4C — Explainability + Feature Importance
```

Objetivo:

Transformar el mejor modelo predictivo actual en un modelo explicable y
defendible para scouting profesional.

---

## Sprint 4C --- Explainability + Player-Level SHAP (Completed)

Status: Completed

### Objetivo

Incorporar explicabilidad al mejor modelo predictivo y generar informes
interpretables a nivel jugador.

### Implementación

Scripts añadidos:

``` text
src/models/explainability/

build_feature_importance_comparison.py
build_shap_analysis.py
build_player_shap_report.py
```

### Funcionalidades implementadas

-   comparación de feature importance
-   SHAP global
-   SHAP summary plots
-   explicación local por jugador
-   generación automática de informes scouting

### Outputs

``` text
reports/tables/explainability/
reports/figures/explainability/
reports/scouting_reports/
```

### Resultado principal

El sistema ya permite identificar:

-   jugadores infravalorados
-   factores explicativos positivos
-   factores explicativos negativos
-   drivers principales del modelo

### Implicación metodológica

El sistema deja de ser únicamente predictivo y pasa a incorporar
interpretabilidad accionable.

### Próximo sprint

``` text
Sprint 5 — Final Scoring System + Undervalued Player Ranking
```

---

## Sprint 5 --- Final Scoring System + Automated Rankings (Completed)

Status: Completed

### Objetivo

Transformar las predicciones generadas por los modelos en señales accionables para scouting cuantitativo mediante una arquitectura multicriterio.

### Implementación

Módulos añadidos:

```text
src/models/scoring/

build_inefficiency_score.py
build_growth_score.py
build_confidence_score.py
build_opportunity_score.py
generate_rankings.py
```

### Componentes implementados

**Inefficiency Score**

```python
predicted_market_value - observed_market_value
```

**Growth Score**

- growth_index
- breakout_indicator
- market_value_growth_prev
- delta_log_market_value_prev

**Confidence Score**

- matching_confidence
- minutes_reliability
- feature_completeness
- temporal_stability

**Opportunity Score**

```python
0.55 * inefficiency_score_z
+ 0.25 * growth_score_z
+ 0.20 * confidence_score_z
```

### Resultados

| Métrica | Valor |
|---|---:|
| Observaciones scoreadas | 1,138 |
| Scouting targets | 53 |
| High-priority targets | 376 |

### Resultado principal

El sistema deja de producir únicamente predicciones y pasa a generar recomendaciones priorizadas orientadas a soporte de decisiones.

---

## Sprint 6 --- Ranking Validation & Business Evaluation (Completed)

Status: Completed

### Objetivo

Evaluar si los rankings generados aportan valor práctico desde una perspectiva estadística y de negocio.

### Implementación

```text
src/models/evaluation/

build_ranking_diagnostics.py
build_roi_simulation.py
build_precision_at_k.py
```

### Resultados

| K | Precision@K |
|---:|---:|
| 10 | 0.90 |
| 20 | 0.90 |
| 50 | 0.90 |
| 100 | 0.85 |

### Implicación metodológica

La evaluación deja de centrarse únicamente en métricas predictivas (RMSE, MAE, R²) y pasa a incorporar métricas orientadas a utilidad de scouting y decisión deportiva.

### Resultado principal

La arquitectura evoluciona hacia:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Evaluación
↓
Business Layer
```

---

## Sprint 7 --- Scouting Dashboard & Decision Support Layer (Completed)

Status: Completed

### Objetivo

Transformar los resultados analíticos del sistema en una herramienta operativa de apoyo a decisiones de scouting profesional.

### Implementación

```text
dashboard/
streamlit_app.py
```

### Funcionalidades implementadas

#### Executive KPIs

- Precision@K
- % oportunidades rentables
- tamaño de shortlist
- cobertura analítica

#### Bubble Chart Coste vs Upside

- Opportunity Score visual
- tiers de oportunidad
- top oportunidades destacadas
- filtros interactivos

#### Ranking interactivo

- paginación
- filtros dinámicos
- segmentación por liga
- posición
- club
- temporada

#### Informe individual

- valor mercado
- valor estimado
- gap de mercado
- Opportunity Score
- Growth Score
- Confidence Score
- recomendación analítica

#### Explainability integrada

- SHAP individual
- drivers positivos
- drivers negativos
- interpretación de predicciones

### Resultado principal

La arquitectura evoluciona desde:

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
Dashboard
↓
Decisión deportiva
```

### Implicación metodológica

El proyecto deja de ser únicamente un sistema predictivo y pasa a convertirse en una plataforma de Football Analytics orientada a soporte de decisiones.

## Sprint 8 — Reserved

Status: Reserved

### Contexto

Tras la tutoría académica y la redefinición de la hoja de ruta del proyecto, las funcionalidades inicialmente previstas para este sprint fueron absorbidas posteriormente dentro del Sprint 9.

Se decidió no ejecutarlo como sprint independiente para evitar fragmentar artificialmente la evolución de la capa de soporte a decisiones.

### Resultado

El Sprint 8 queda reservado en la numeración histórica del proyecto.

Las funcionalidades inicialmente previstas se integraron posteriormente en:

```text
Sprint 9 — Executive Dashboard & Decision Support Layer
```

---

## Sprint 9 — Executive Dashboard & Decision Support Layer (Completed)

Status: Completed

### Objetivo

Transformar el sistema desde un entorno centrado en predicción y ranking hacia una plataforma de Football Analytics orientada a soporte de decisiones de scouting.

### Alcance

Sprint 9 constituye la primera implementación completa de la capa de:

```text
Decision Support System (DSS)
```

integrando visual analytics, priorización de oportunidades e interpretación ejecutiva de resultados.

---

### Sprint 9.1 — Executive Scouting Filters

#### Objetivo

Incorporar una capa de segmentación avanzada que permita explorar el mercado de jugadores desde una perspectiva operativa de scouting.

#### Funcionalidades implementadas

* presets de scouting
* actualización automática de filtros
* eliminación de acciones manuales de refresco
* universo modelado visible
* shortlist ejecutiva
* métricas de cobertura
* filtros activos visibles

#### Variables de segmentación

* Liga
* Posición
* Edad
* Opportunity Score
* Confidence Score

#### Resultado

El dashboard evoluciona desde un ranking estático hacia una herramienta interactiva de exploración y priorización.

---

### Sprint 9.2 — Visual Analytics & Opportunity Matrix

#### Objetivo

Incorporar visualizaciones orientadas a decisión para facilitar la identificación de oportunidades de mercado.

#### Funcionalidades implementadas

##### 💎 Coste actual vs Upside estimado

Nueva matriz estratégica basada en:

* Valor de mercado actual
* Gap de mercado estimado
* Opportunity Score
* Tier de oportunidad

Cada burbuja representa un jugador donde:

```text
X → coste actual
Y → upside estimado
Tamaño → Opportunity Score
Color → prioridad scouting
```

##### 🎯 Segmentación estratégica

El mercado se divide automáticamente en:

| Zona                  | Interpretación                 |
| --------------------- | ------------------------------ |
| Comprar / priorizar   | Bajo coste y alto upside       |
| Oportunidades premium | Alto upside y mayor coste      |
| Seguimiento           | Monitorización futura          |
| Menor prioridad       | Menor relación coste-potencial |

##### 🏅 Top 5 destacados

Identificación automática de los cinco jugadores con mayor Opportunity Score dentro de los filtros activos.

##### 📊 Hallazgos ejecutivos

Nueva capa de síntesis orientada a dirección deportiva:

* candidatos prioritarios
* oportunidades premium
* score oportunidad medio
* upside agregado identificado
* liga dominante

#### Resultado

La arquitectura evoluciona desde:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Dashboard
```

hacia:

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
↓
Scouting
```

### Impacto metodológico

Sprint 9 representa la transición definitiva desde un sistema predictivo hacia una plataforma de Football Analytics orientada a toma de decisiones.

El proyecto incorpora por primera vez una capa DSS (Decision Support System) capaz de transformar predicciones en recomendaciones accionables para scouting profesional.



# 🔄 Evolución de arquitectura

El proyecto comenzó como un entorno principalmente exploratorio basado
en notebooks.

Posteriormente evolucionó hacia:

``` text
pipeline modular reproducible
```

Actualmente:

-   los notebooks se utilizan para análisis e interpretación
-   la ejecución principal se realiza mediante pipelines desacoplados
-   los modelos y outputs se generan automáticamente
-   los artefactos se persisten
-   la configuración está centralizada
-   los experimentos quedan registrados automáticamente


---


## 📌 Cambio arquitectónico principal

### Antes

``` text
Notebook-centric workflow
```


---


### Ahora

``` text
Modular analytics system
```

Separación clara entre:

-   ingesta
-   feature engineering
-   matching
-   modelización
-   scoring
-   evaluación
-   outputs
-   tracking experimental
-   configuración


---


# 🏗️ Arquitectura actual del sistema

``` mermaid
flowchart TD

A[Raw Sources] --> B[Feature Engineering]
B --> C[Player-Season Matching]
C --> D[Player-Season Panel]
D --> E[Modeling Dataset]

E --> F[Econometric Pipeline]
E --> G[Machine Learning Pipeline]

F --> H[Scoring Engine]
G --> H

H --> I[Ranking Engine]
I --> J[Explainability]
J --> K[Scouting Dashboard]
K --> L[Toma de decisión deportiva]
```


---


## 📂 Arquitectura física

``` text
market-value-football-tfm/

├── artifacts/
├── config/
├── data/
├── docs/
├── mlruns/
├── notebooks/
├── reports/
├── src/
├── tests/
```


---


## 🧩 Componentes principales

| Componente | Estado |
|---|---|
| Data pipelines | ✅ |
| Matching pipeline | ✅ |
| Modeling dataset | ✅ |
| OLS pipeline | ✅ |
| ML pipeline | ✅ |
| Scoring pipeline | ✅ |
| Evaluation pipeline | ✅ |
| Temporal validation | ✅ |
| Model persistence | ✅ |
| Ranking generation | ✅ |
| Explainability | ✅ |
| Scouting Dashboard | ✅ |
| MLflow tracking | ✅ |
| Configuración YAML | ✅ |
| Visual Analytics | ✅ |
| Decision Support Layer | ✅ |


---


# ⚙️ Configuración centralizada

El sistema incorpora actualmente una arquitectura de configuración
centralizada desacoplada del código de negocio.


---


## 📂 Directorio de configuración

``` text
config/

├── config.yaml
├── modeling.yaml
├── matching.yaml
├── features.yaml
├── paths.yaml
└── project.yaml
```


---


## 📌 Objetivos

La configuración centralizada permite:

-   desacoplar parámetros del código
-   mejorar reproducibilidad
-   facilitar experimentación
-   evitar hardcoding
-   centralizar decisiones metodológicas
-   mejorar mantenibilidad


---


## 📌 Parámetros centralizados actuales

### Matching

``` yaml
MAX_AGE_DIFF
MIN_CLUB_SCORE
FUZZY_THRESHOLD
```


---


### Modeling

``` yaml
target
features
fixed_effects
validation_split
```


---


### Feature Engineering

``` yaml
minutes_threshold
age_filters
league_filters
feature_groups
```


---


### Paths

``` yaml
data_paths
artifacts_paths
reports_paths
```


---


## 📌 Beneficios arquitectónicos

La centralización de configuración facilita:

-   trazabilidad experimental
-   cambios rápidos de especificaciones
-   comparación entre ejecuciones
-   escalabilidad futura
-   despliegue reproducible


---


# 🧪 Experiment tracking con MLflow

El proyecto incorpora actualmente tracking experimental mediante:

``` text
MLflow
```


---


## 📌 Objetivos

MLflow permite registrar automáticamente:

-   métricas
-   hiperparámetros
-   configuraciones
-   artefactos
-   modelos
-   outputs experimentales


---


## 📂 Directorio principal

``` text
mlruns/
```


---


## 📌 Información registrada

### Configuración experimental

-   variables utilizadas
-   target
-   fixed effects
-   split temporal
-   thresholds
-   hiperparámetros


---


### Métricas

-   RMSE
-   MAE
-   R²


---


### Artefactos

-   modelos serializados
-   feature importance
-   predicciones
-   outputs CSV
-   rankings


---


## 📌 Beneficios metodológicos

El tracking experimental mejora significativamente:

-   reproducibilidad
-   trazabilidad
-   rigor metodológico
-   comparabilidad entre modelos
-   auditoría analítica
-   documentación del TFM


---


## 📌 Impacto arquitectónico

La incorporación de MLflow transforma el sistema desde:

``` text
pipeline reproducible
```

hacia:

``` text
entorno experimental analítico profesional
```


---


# ⚠️ Problema crítico del proyecto

# Integración FBref ↔ Transfermarkt

El principal reto técnico del proyecto ha sido la integración entre
FBref y Transfermarkt.


---


## 🚧 Problemas estructurales

-   ❌ ausencia de identificador común
-   ❌ nombres inconsistentes
-   ❌ transliteraciones
-   ❌ diferencias de clubes
-   ❌ granularidad temporal distinta
-   ❌ cambios intra-temporada


---


## 📉 Riesgos derivados

Sin matching robusto:

-   false positives
-   false negatives
-   ruido en el modelo
-   rankings incorrectos
-   pérdida de validez del scoring


---


## 📌 Impacto técnico

Este problema consumió aproximadamente:

``` text
40-50% del trabajo técnico total
```


---


# 🛠️ Sistema de matching implementado

Se desarrolló un pipeline jerárquico multi-validación.


---


## 1️⃣ Normalización de nombres

-   lowercase
-   eliminación de acentos
-   limpieza de strings


---


## 2️⃣ Matching exacto

Variables utilizadas:

-   nombre normalizado
-   temporada
-   edad aproximada


---


## 3️⃣ Validación por club

Threshold:

``` python
MIN_CLUB_SCORE = 70
```

---


## 4️⃣ Matching fuzzy

Algoritmo:

``` python
RapidFuzz
```

Threshold:

``` python
FUZZY_THRESHOLD = 92
```

---


## 5️⃣ Validación por edad

``` python
MAX_AGE_DIFF = 1.5
```

---


# 📈 Resultados del matching

## 📊 Resultados globales

| Métrica | Resultado |
|---|---:|
| Match rate | 88.36% |
| Observaciones emparejadas | 20,836 |
| Observaciones totales | 23,580 |


---


## Distribución final

| Método | Resultado |
|---|---|
| exact_age_validated | dominante |
| exact_age_club_validated | relevante |
| fuzzy_age_club_validated | residual |


---


## 📌 Interpretación

El matching exacto domina claramente la muestra final.

El fuzzy matching queda restringido a casos ambiguos específicos,
reduciendo riesgo de false positives.

👉 El sistema prioriza cobertura manteniendo control de calidad.


---


# 📊 Dataset final de modelización

## Resultado tras filtros

| Métrica | Valor |
|---|---:|
| Observaciones | 3,297 |
| Jugadores | 1,847 |
| Ligas | 7 |
| Edad | 18–23 |


---


## Filtros aplicados

-   matching válido
-   edad válida
-   minutos mínimos
-   valor de mercado disponible
-   posición válida


---


## Distribución por posición

| Posición | Observaciones |
|---|---:|
| MID | 1,705 |
| DEF | 1,147 |
| ATT | 351 |
| GK | 94 |


---


## Distribución por liga

| Liga | Observaciones |
|---|---:|
| Ligue 1 | 627 |
| Eredivisie | 557 |
| Serie A | 494 |
| Premier League | 466 |
| Bundesliga | 438 |
| LaLiga | 373 |
| Liga Portugal | 342 |


---


# 📈 Estado del pipeline econométrico

``` text
src/models/econometric/
```


---


## Componentes implementados

| Archivo | Estado |
|---|---|
| specifications.py | ✅ |
| train_ols.py | ✅ |
| run_ols_pipeline.py | ✅ |


---


## Funcionalidades actuales

-   fórmula OLS centralizada
-   HC3 robust covariance
-   league FE
-   season FE
-   position FE
-   scoring automático
-   rankings automáticos
-   export CSV
-   evaluación temporal
-   tracking MLflow
-   logging de métricas


---


## Modelo final

``` python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
league FE +
season FE +
position FE
```


---


## 📊 Resultados out-of-sample

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| OLS simple | 1.0036 | 1.2165 | 0.1472 |
| OLS + League FE | 0.7954 | 0.9896 | 0.4356 |
| OLS final FE | **0.7907** | **0.9823** | **0.4439** |


---


## 📌 Hallazgos principales

### Premier League

-   prima estructural positiva significativa


---


### Eredivisie / Liga Portugal

-   descuentos estructurales relevantes


---


### Variables más relevantes

-   minutos jugados
-   goles por 90
-   asistencias por 90


---


# 🤖 Estado del pipeline Machine Learning

``` text
src/models/machine_learning/
```


---


## Componentes implementados

| Archivo | Estado |
|---|---|
| pipelines.py | ✅ |
| train_ml.py | ✅ |
| run_ml_pipeline.py | ✅ |


---


## Modelos implementados

-   Random Forest
-   HistGradientBoosting
-   GradientBoostingRegressor


---


## Funcionalidades actuales

-   preprocessing pipeline
-   one-hot encoding
-   temporal validation
-   feature importance
-   model persistence
-   export automático
-   tracking MLflow
-   logging de hiperparámetros


---


## 📊 Resultados ML

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| OLS final | 0.7907 | 0.9823 | 0.4439 |
| Random Forest | 0.7704 | 0.9691 | 0.4587 |
| HistGradientBoosting | 0.7723 | 0.9642 | 0.4721 |
| Gradient Boosting | **0.7618** | **0.9515** | **0.4813** |


---


## 📌 Insight principal

La mejora moderada de ML respecto a OLS sugiere que:

``` text
el principal cuello de botella es el signal del dataset
```

y no necesariamente el algoritmo.


---


# 💡 Estado del scoring pipeline

``` text
src/models/scoring/
```

## Componentes implementados

| Archivo | Estado |
|---|---|
| build_inefficiency_score.py | ✅ |
| build_growth_score.py | ✅ |
| build_confidence_score.py | ✅ |
| build_opportunity_score.py | ✅ |
| generate_rankings.py | ✅ |

## Señales implementadas

### Inefficiency Score

``` python
predicted_value - observed_value
```

### Growth Score

Basado en:

-   growth_index
-   market_value_growth_prev
-   delta_log_market_value_prev
-   breakout_indicator

### Confidence Score

``` python
0.35 × matching_confidence
+ 0.35 × minutes_reliability
+ 0.20 × feature_completeness
+ 0.10 × temporal_stability
```

### Opportunity Score

``` python
0.55 × inefficiency_score_z
+ 0.25 × growth_score_z
+ 0.20 × confidence_score_z
```

## Resultados actuales

| Métrica | Valor |
|---|---:|
| Observaciones scoreadas | 1,138 |
| Scouting targets | 53 |
| High priority + targets | 376 |

## Rankings automáticos

-   top_undervalued_global.csv
-   top_undervalued_by_league.csv
-   top_undervalued_by_position.csv
-   top_high_potential.csv
-   top_low_risk.csv
-   scouting_shortlist.csv

# 📊 Estado del evaluation pipeline

``` text
src/models/evaluation/
```


---


## Funcionalidades actuales

-   comparación OLS vs ML
-   métricas centralizadas
-   feature importance
-   reporting reproducible
-   tracking de experimentos


---


## Métricas utilizadas

-   RMSE
-   MAE
-   R²


---


# 📤 Outputs generados

## Reports

``` text
reports/
```


---


## Artifacts

``` text
artifacts/
```


---


## MLflow Tracking

``` text
mlruns/
```

---

## Outputs actuales

-   rankings scouting
-   métricas OLS
-   métricas ML
-   feature importance
-   modelos persistidos
-   predicciones
-   diagnósticos
-   experimentos registrados
-   dashboard interactivo
-   informes individuales
-   visual analytics de scouting
-   executive dashboard
-   bubble chart Coste vs Upside
-   scouting matrix
-   top 5 automático
-   executive insights


---


# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs capacidad predictiva

El proyecto prioriza inicialmente:

``` text
interpretabilidad + robustez
```

frente a maximizar únicamente métricas predictivas.


---


## Justificación

En scouting profesional resulta crítico:

-   explicar rankings
-   justificar decisiones
-   interpretar drivers del valor
-   mantener coherencia futbolística


---


## Arquitectura híbrida

Por ello el sistema combina:

-   econometría interpretable
-   ML predictivo
-   scoring cuantitativo


---


# 🧱 Deuda técnica actual

## Principales limitaciones pendientes

### Feature engineering

Pendiente incorporar:

-   z-scores posicionales
-   progression metrics
-   percentiles
-   métricas defensivas
-   rolling metrics
-   growth indicators


---


### Explainability

Pendiente:

-   SHAP
-   explicaciones individuales
-   estabilidad rankings


---


### Dataset signal

El principal cuello de botella actual es:

``` text
calidad y riqueza del feature set
```


---


# 🚀 Próximos pasos

## Prioridad alta

### Sprint 10 — Advanced Player Intelligence

Objetivo:

Evolucionar el dashboard desde una herramienta de priorización hacia una plataforma de análisis individual de talento.

Funcionalidades previstas:

* radar avanzado de jugador
* comparador jugador vs jugador
* comparador jugador vs percentil de liga
* fortalezas y debilidades automáticas
* exportación PDF de perfiles
* scouting cards descargables

Resultado esperado:

```text
Shortlist
↓
Análisis individual
↓
Scouting report
```

---

### Sprint 11 — Advanced Explainability

Objetivo:

Incrementar la interpretabilidad del sistema para facilitar la defensa metodológica y la adopción por parte de departamentos deportivos.

Funcionalidades previstas:

* SHAP global avanzado
* SHAP por liga
* SHAP por posición
* explicación individual de rankings
* explicación del Opportunity Score
* análisis de estabilidad del ranking

Resultado esperado:

```text
Predicción
↓
Explicación
↓
Justificación deportiva
```

---

### Sprint 12 — Feature Engineering Avanzado

Objetivo:

Incrementar la señal predictiva del dataset mediante variables más cercanas al rendimiento futbolístico real.

Líneas de trabajo:

* progression metrics
* carrying metrics
* passing value metrics
* métricas defensivas avanzadas
* percentiles por posición
* normalización por liga
* rolling performance indicators
* indicadores de consistencia

Resultado esperado:

Incremento de capacidad predictiva tanto en OLS como en Machine Learning.

---

### Sprint 13 — Model Benchmark Expansion

Objetivo:

Evaluar arquitecturas adicionales para validar la robustez del modelo actual.

Modelos candidatos:

* CatBoost
* TabPFN
* XGBoost avanzado
* LightGBM avanzado
* Ensemble Models

Resultado esperado:

Determinar si existen mejoras predictivas significativas sobre el benchmark actual.

---

## Prioridad media

### Exportación profesional de resultados

Objetivo:

Facilitar el uso operativo por parte de analistas y scouts.

Funcionalidades previstas:

* exportación PDF de shortlists
* exportación Excel
* informes automáticos por jugador
* informes automáticos por liga
* snapshots ejecutivos

---

### Business Validation Layer

Objetivo:

Acercar el sistema a escenarios reales de scouting profesional.

Análisis previstos:

* simulación de fichajes históricos
* evaluación ex-post de rankings
* análisis ROI ampliado
* comparación con decisiones reales de mercado
* validación de señales de oportunidad

---

### API de Scoring

Objetivo:

Preparar la arquitectura para despliegues futuros.

Funcionalidades previstas:

* scoring automatizado
* inferencia sobre nuevos jugadores
* actualización periódica de rankings
* integración con fuentes externas

---

## Horizonte de cierre del TFM

Antes de la entrega final se considera prioritario completar:

* Dashboard Ejecutivo (✅)
* Visual Analytics (✅)
* Decision Support Layer (✅)
* Explainability avanzada
* Feature Engineering avanzado
* Business Validation
* Memoria final

---

## Visión final del proyecto

La arquitectura objetivo es:

```text
Fuentes de datos
↓
Feature Engineering
↓
Machine Learning
↓
Scoring
↓
Ranking
↓
Visual Analytics
↓
Decision Support
↓
Scouting Intelligence Platform
```

El objetivo final es disponer de una plataforma de Football Analytics capaz de identificar, priorizar y justificar oportunidades de mercado de forma reproducible y defendible desde una perspectiva deportiva y de negocio.


---


# 🧠 Conclusión

El proyecto ya no representa únicamente un análisis exploratorio
académico, sino un sistema analítico modular y reproducible orientado a
scouting cuantitativo profesional.

Actualmente el sistema ya incorpora:

-   integración multi-fuente robusta
-   matching validado
-   modelización econométrica
-   machine learning supervisado
-   validación temporal
-   scoring automático
-   tracking experimental con MLflow
-   configuración centralizada
-   persistencia de artefactos
-   outputs reproducibles
-   visual analytics ejecutivo
-   dashboard de scouting profesional
-   decision support system

Principales conclusiones derivadas del proyecto:

- el matching constituye uno de los principales aportes técnicos del sistema
- las variables temporales aportan una mejora significativa sobre variables estáticas
- los modelos ML mejoran moderadamente la capacidad predictiva
- explainability es necesaria para transformar predicciones en recomendaciones defendibles
- el scoring multicriterio mejora la utilidad real para scouting
- la evaluación de negocio aproxima el sistema a escenarios profesionales

La principal línea de evolución futura se centra ahora en:

``` text
incrementar la señal predictiva mediante feature engineering avanzado
```

y transformar el sistema en una herramienta de scouting cuantitativo
cada vez más cercana a entornos profesionales reales.


---


