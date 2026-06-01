# 📊 Identificación de jugadores infravalorados en el mercado de fichajes europeo


![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Econometrics-green)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow)
![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Status](https://img.shields.io/badge/Status-Scouting%20Platform-success)
![Version](https://img.shields.io/badge/version-v0.8.0--Executive--Dashboard-blue)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![DecisionSupport](https://img.shields.io/badge/Decision%20Support-System-success)
![MLflow](https://img.shields.io/badge/MLflow-enabled-success)
![Scouting](https://img.shields.io/badge/Scouting-Ranking%20Engine-success)
![Explainability](https://img.shields.io/badge/Explainability-SHAP-success)

---

# 🧠 Descripción del proyecto

Este proyecto desarrolla un sistema analítico modular para mejorar la
toma de decisiones en scouting y fichajes dentro del fútbol profesional
europeo.

El objetivo principal es estimar el valor de mercado esperado de
futbolistas jóvenes a partir de su rendimiento deportivo y detectar
ineficiencias de mercado que permitan identificar oportunidades de
fichaje bajo una estrategia:

> **Buy low → Sell high**

El sistema combina:

-   Econometría aplicada
-   Machine Learning supervisado
-   Feature engineering deportivo
-   Integración robusta de fuentes heterogéneas
-   Validación temporal out-of-sample
-   Analytics engineering
-   Scouting cuantitativo

---

# 📑 Tabla de contenidos

-   [🧠 Descripción del proyecto](#-descripción-del-proyecto)
-   [🎯 Problema de negocio](#-problema-de-negocio)
-   [🧩 Objetivos analíticos](#-objetivos-analíticos)
-   [⚙️ Enfoque metodológico](#️-enfoque-metodológico)
-   [🔄 Evolución de arquitectura](#-evolución-de-arquitectura)
-   [🏗️ Analytics Engineering &
    Reproducibility](#️-analytics-engineering--reproducibility)
-   [🧪 Experiment Tracking & Dataset
    Versioning](#-experiment-tracking--dataset-versioning)
-   [📚 Metodología](#-metodología)
-   [⏳ Estrategia de validación
    temporal](#-estrategia-de-validación-temporal)
-   [📦 Fuentes de datos](#-fuentes-de-datos)
-   [⚠️ Problema crítico del proyecto](#️-problema-crítico-del-proyecto)
-   [🛠️ Sistema de matching
    implementado](#️-sistema-de-matching-implementado)
-   [📈 Resultados del matching](#-resultados-del-matching)
-   [🏗️ Arquitectura del pipeline](#️-arquitectura-del-pipeline)
-   [📊 Dataset final](#-dataset-final)
-   [📈 Pipeline econométrico](#-pipeline-econométrico)
-   [🤖 Pipeline Machine Learning](#-pipeline-machine-learning)
-   [🎯 Scouting Scoring Engine](#-scouting-scoring-engine)
-   [📋 Automated Ranking Engine](#-automated-ranking-engine)
-   [💡 Inefficiency Score](#-inefficiency-score)
-   [📤 Business Outputs](#-business-outputs)
-   [📂 Estructura del proyecto](#-estructura-del-proyecto)
-   [▶️ Ejecución reproducible](#️-ejecución-reproducible)
-   [📊 Resultados actuales](#-resultados-actuales)
-   [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
-   [🚀 Próximos pasos](#-próximos-pasos)
-   [🧠 Valor del proyecto](#-valor-del-proyecto)
-   [👤 Autores](#-autores)

---

# 🎯 Problema de negocio

Los clubes toman decisiones de fichaje basándose en:

-   scouting tradicional
-   intuición
-   métricas limitadas
-   análisis parcialmente subjetivos

Sin embargo, el mercado presenta ineficiencias derivadas de:

-   información incompleta
-   sesgos mediáticos
-   diferencias estructurales entre ligas
-   asimetrías de información

👉 Este proyecto busca responder:

## ❓ ¿Qué jugadores están infravalorados respecto a su rendimiento real?

---

# 🧩 Objetivos analíticos

El sistema busca:

-   estimar el valor de mercado esperado
-   detectar jugadores infravalorados
-   construir rankings cuantitativos de scouting
-   analizar diferencias estructurales entre ligas
-   comparar econometría vs machine learning
-   generar outputs interpretables para toma de decisiones

---

# ⚙️ Enfoque metodológico

## Unidad de análisis

``` text
Jugador – Temporada
```

Cada observación representa:

-   rendimiento deportivo
-   contexto competitivo
-   valor de mercado
-   características demográficas

de un jugador en una temporada concreta.

---

# 🔄 Evolución de arquitectura

El proyecto comenzó como un entorno exploratorio basado principalmente
en notebooks y evolucionó hacia una arquitectura modular reproducible
orientada a analytics engineering y modelización escalable.

Actualmente:

-   los notebooks se utilizan para EDA, validación e interpretación
-   la ejecución principal se realiza mediante pipelines modulares
-   los outputs son reproducibles y versionables
-   los modelos pueden persistirse y reutilizarse
-   la validación temporal está centralizada
-   los artefactos de modelización quedan desacoplados del código
    analítico

Esta evolución permitió transformar el proyecto desde un prototipo
exploratorio hacia un sistema analítico estructurado y reproducible.

---

# 🏗️ Analytics Engineering & Reproducibility

El proyecto adopta principios de analytics engineering:

-   separación modular de pipelines
-   outputs reproducibles
-   persistencia de artefactos
-   trazabilidad de transformaciones
-   configuración desacoplada
-   validación temporal centralizada

Separación explícita entre:

``` text
raw data
processed data
modeling data
artifacts
business outputs
```

La arquitectura facilita:

-   mantenibilidad
-   escalabilidad
-   auditoría metodológica
-   replicabilidad académica
-   despliegue futuro

---

# 🧪 Experiment Tracking & Dataset Versioning

El proyecto incorpora un sistema de trazabilidad experimental orientado
a garantizar:

-   reproducibilidad
-   auditoría metodológica
-   comparación entre ejecuciones
-   persistencia de experimentos
-   control de versiones del dataset

---

## MLflow

Se implementó integración completa con:

``` text
MLflow
```

El sistema registra automáticamente:

-   métricas
-   hiperparámetros
-   configuración experimental
-   artifacts generados
-   metadata del dataset
-   timestamps
-   validación temporal utilizada

---

## Información registrada por experimento

Cada ejecución almacena automáticamente:

``` text
model_name
dataset_version
dataset_hash
train_period
test_period
features
metrics
artifacts
execution_timestamp
```

---

## Dataset Versioning

Se implementó versionado lógico del dataset modelizable.

Ejemplo:

``` text
player_season_modeling_v1
player_season_modeling_v2
player_season_modeling_v3
```

Cada versión almacena:

-   hash SHA256
-   número de filas
-   número de columnas
-   pipeline generador
-   fecha de creación

Metadata persistida en:

``` text
artifacts/metadata/
```

---

## Validación temporal reproducible

El pipeline econométrico utiliza:

``` text
strict temporal out-of-sample validation
```

Split actual:

| Split | Temporadas |
|---|---|
| Train | 2019-2020 → 2023-2024 |
| Test | 2024-2025 |

---

## Consideración metodológica importante

Los modelos predictivos temporales no utilizan:

``` text
season fixed effects
```

durante inferencia out-of-sample, ya que la temporada futura no existe
durante entrenamiento y generaría leakage estructural.

Sin embargo:

-   league FE
-   position FE

sí se mantienen para capturar heterogeneidad estructural del mercado.

---

## Artefactos experimentales

Los experimentos generan automáticamente:

``` text
mlruns/
artifacts/
reports/
```

Incluyendo:

-   métricas exportadas
-   rankings
-   metadata
-   outputs de scoring
-   predicciones
-   modelos persistidos

---

# 📚 Metodología

El proyecto sigue una adaptación de:

``` text
CRISP-DM
```

## Estado actual

``` text
Evaluation → Decision Support → Visual Analytics
```

---

# ⏳ Estrategia de validación temporal

El sistema utiliza validación temporal estricta para evitar leakage
temporal y reproducir escenarios reales de scouting.

| Split | Temporadas |
|---|---|
| Train | 2019-2020 → 2023-2024 |
| Test | 2024-2025 |

👉 No se utiliza random split.

## Justificación

El random split:

-   rompe coherencia temporal
-   introduce leakage
-   genera optimismo artificial
-   sobreestima capacidad predictiva

La validación temporal reproduce un entorno real de scouting donde el
modelo debe generalizar hacia temporadas futuras.

---

# 📦 Fuentes de datos

## Transfermarkt / Kaggle Player Scores

### Variables principales

-   valor de mercado
-   edad
-   club
-   posición
-   historial de traspasos

### Uso

-   target principal
-   construcción del Inefficiency Score
-   contexto de mercado

### Dataset utilizado

``` text
Kaggle — davidcariboo/player-scores
```

---

## FBref

### Variables principales

-   estadísticas por 90 minutos
-   métricas ofensivas
-   métricas defensivas
-   métricas de posesión

### Uso

-   variables explicativas
-   feature engineering deportivo

---

## Understat (pendiente)

### Variables previstas

-   xG
-   xA

### Uso previsto

-   métricas ofensivas ajustadas por calidad
-   mejora del signal predictivo

---

# ⚠️ Problema crítico del proyecto

# Integración FBref ↔ Transfermarkt

Uno de los principales retos del proyecto es el matching entre ambas
fuentes.

## Problemas estructurales

-   ❌ no existe identificador único común
-   ❌ nombres inconsistentes
-   ❌ transliteraciones
-   ❌ diferencias de clubes
-   ❌ diferencias de edad
-   ❌ cambios intra-temporada
-   ❌ granularidad distinta

👉 Este problema consumió aproximadamente el 40-50% del trabajo técnico
total.

---

# 🛠️ Sistema de matching implementado

Se desarrolló un pipeline jerárquico robusto.

## 1️⃣ Normalización de nombres

-   lowercase
-   eliminación de acentos
-   limpieza de strings

---

## 2️⃣ Matching exacto

-   nombre
-   temporada
-   edad aproximada

---

## 3️⃣ Validación por club

-   fuzzy matching
-   similarity score

---

## 4️⃣ Matching fuzzy

-   RapidFuzz
-   token sort ratio
-   threshold elevado

---

## 5️⃣ Validación final

``` python
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

---

# 📈 Resultados del matching

| Métrica | Resultado |
|---|---:|
| Match rate | 88.36% |
| Observaciones emparejadas | 20,836 |
| Observaciones totales | 23,580 |

## Distribución

| Método | Resultado |
|---|---|
| exact_age_validated | dominante |
| exact_age_club_validated | relevante |
| fuzzy_age_club_validated | residual |

👉 El matching constituye uno de los principales aportes técnicos del
proyecto.

---

# 🏗️ Arquitectura del pipeline

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

# 📊 Dataset final

## Panel completo

| Métrica | Valor |
|---|---:|
| Observaciones | 23,580 |
| Temporadas | 2019-2020 → 2024-2025 |
| Ligas | 7 |

---

## Dataset modelizable

| Métrica | Valor |
|---|---:|
| Observaciones | 3,297 |
| Jugadores | 1,847 |
| Edad | 18–23 |

---

## Ligas incluidas

-   Premier League
-   LaLiga
-   Bundesliga
-   Serie A
-   Ligue 1
-   Eredivisie
-   Liga Portugal

---

# 📈 Pipeline econométrico

``` text
src/models/econometric/
```

---

## Arquitectura

El pipeline econométrico está completamente modularizado.

### Componentes principales

-   `specifications.py`
-   `train_ols.py`
-   `evaluate_ols.py`
-   `run_ols_pipeline.py`

---

## Funcionalidades

-   fórmula OLS centralizada
-   efectos fijos
-   HC3 robust covariance
-   scoring automático
-   rankings automáticos
-   export de outputs
-   evaluación temporal
-   experiment tracking
-   dataset versioning
-   MLflow logging
-   temporal split reproducible

---

## Modelo econométrico final

Regresión OLS con:

-   league FE
-   position FE
-   HC3 robust standard errors
-   validación temporal estricta out-of-sample

---

## Consideración metodológica

Los season fixed effects se utilizan únicamente en análisis explicativos
e in-sample.

Para validación temporal futura:

``` text
season FE se desactiva
```

para evitar problemas de generalización hacia temporadas no observadas
durante entrenamiento.

---

## Variable objetivo

``` python
log_market_value_eur
```

---

## Especificación principal

``` python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
league FE +
position FE
```

---

## Outputs generados

``` text
reports/tables/
reports/rankings/
reports/model_diagnostics/
```

Outputs:

-   métricas OLS
-   coeficientes
-   rankings infravalorados
-   rankings sobrevalorados
-   residuos
-   tablas VIF

---

# 🤖 Pipeline Machine Learning

``` text
src/models/machine_learning/
```

---

## Modelos implementados

-   Random Forest
-   HistGradientBoosting
-   GradientBoostingRegressor

---

## Funcionalidades

-   preprocessing pipeline
-   one-hot encoding
-   temporal validation
-   feature importance
-   model persistence
-   export automático

---

## Arquitectura ML

El pipeline ML incluye:

-   preprocessing desacoplado
-   entrenamiento modular
-   evaluación centralizada
-   persistencia de modelos

---

## Persistencia de modelos

Los modelos entrenados se almacenan en:

``` text
artifacts/models/
```

Esto permite:

-   reutilización
-   comparación entre ejecuciones
-   scoring posterior
-   reproducibilidad
-   potencial despliegue futuro

---

## Outputs ML

``` text
artifacts/
reports/
```

Outputs:

-   métricas ML
-   feature importance
-   predicciones out-of-sample
-   modelos persistidos

---

# 🎯 Scouting Scoring Engine

Sprint 5 introduce una capa analítica orientada a convertir las
predicciones del modelo en una herramienta de apoyo real para scouting
profesional.

## Arquitectura del scoring

``` text
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
Automated Rankings
```

## Opportunity Score

``` python
opportunity_score =
0.55 × inefficiency_score_z
+ 0.25 × growth_score_z
+ 0.20 × confidence_score_z
```

Resultados actuales:

| Métrica | Valor |
|---|---:|
| Observaciones | 1,138 |
| Scouting targets | 53 |
| Alta prioridad + targets | 376 |

---

# 📋 Automated Ranking Engine

Outputs generados:

``` text
top_undervalued_global.csv
top_undervalued_by_league.csv
top_undervalued_by_position.csv
top_high_potential.csv
top_low_risk.csv
scouting_shortlist.csv
```

# 💡 Inefficiency Score

El sistema estima:

``` python
inefficiency_score =
valor_estimado - valor_observado
```

## Interpretación

| Score | Interpretación |
|---|---|
| Positivo | posible infravaloración |
| Negativo | posible sobrevaloración |

---

# 📤 Business Outputs

``` text
reports/rankings/
```

El sistema genera automáticamente:

-   jugadores infravalorados
-   jugadores sobrevalorados
-   rankings por liga
-   rankings por posición
-   scouting shortlists
-   feature importance
-   diagnostics
-   predicciones

---

# 🖥️ Dashboard de scouting

Sprint 7 incorpora una capa completa de visual analytics y soporte a la decisión construida sobre Streamlit.

## Objetivo

Transformar predicciones, rankings y métricas de negocio en una herramienta operativa utilizable por departamentos de scouting y dirección deportiva.

## Funcionalidades principales

### 📊 Executive KPIs

- Jugadores en shortlist
- Precision@K
- % oportunidades rentables
- Ligas representadas

### 💎 Coste actual vs Upside estimado

Bubble chart interactivo:

- Eje X: valor de mercado actual
- Eje Y: gap de mercado estimado
- Tamaño: Opportunity Score
- Color: tier de oportunidad
- Top oportunidades destacadas

### 📋 Ranking interactivo

- Paginación
- Filtros dinámicos
- Segmentación por liga
- Segmentación por posición
- Segmentación por club
- Segmentación por temporada

### 👤 Informe individual

- Valor actual
- Valor estimado
- Gap de mercado
- Opportunity Score
- Growth Score
- Confidence Score
- Recomendación analítica

### 🔍 Explainability

- SHAP local
- Drivers positivos y negativos
- Interpretación ejecutiva

## Sprint 9 — Executive Dashboard & Decision Support Layer

Sprint 9 consolida la evolución del proyecto desde un sistema de modelización y ranking hacia una plataforma de Football Analytics orientada a soporte de decisiones para scouting profesional.

### Objetivo

Reducir la distancia entre los resultados de los modelos y la toma de decisiones deportivas mediante visual analytics, segmentación avanzada y síntesis ejecutiva.

---

### Sprint 9.1 — Executive Scouting Filters

Se incorpora una capa de exploración dinámica del mercado basada en filtros ejecutivos y presets de scouting.

#### Funcionalidades implementadas

* presets de scouting
* filtros automáticos sin refresco manual
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

Resultado:

El dashboard evoluciona desde un ranking estático hacia una herramienta interactiva de exploración y priorización.

---

### Sprint 9.2 — Visual Analytics & Opportunity Matrix

#### 💎 Coste actual vs Upside estimado

Nueva matriz estratégica basada en:

* Valor de mercado actual
* Gap de mercado estimado
* Opportunity Score
* Tier de oportunidad

Cada jugador se representa mediante una burbuja donde:

* Eje X → coste actual de adquisición
* Eje Y → upside estimado
* Tamaño → Opportunity Score
* Color → prioridad de scouting

#### 📌 Segmentación estratégica

| Zona                  | Interpretación                       |
| --------------------- | ------------------------------------ |
| Comprar / priorizar   | Bajo coste y alto upside             |
| Oportunidades premium | Alto upside con mayor coste          |
| Seguimiento           | Interés moderado para monitorización |
| Menor prioridad       | Menor relación coste-potencial       |

#### 🏅 Top 5 destacados

Identificación automática de los cinco jugadores con mayor Opportunity Score dentro de los filtros activos.

#### 📈 Hallazgos ejecutivos

Indicadores incorporados:

* candidatos prioritarios
* oportunidades premium
* score oportunidad medio
* upside agregado identificado
* liga dominante

### Contribución metodológica

Sprint 9 representa la primera implementación completa de una capa DSS (Decision Support System) aplicada al mercado de fichajes.

El flujo operativo queda definido como:

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
↓
Decisión deportiva
```

### Impacto sobre el proyecto

La plataforma deja de ser únicamente un sistema predictivo para convertirse en una herramienta de priorización de talento y soporte cuantitativo a decisiones deportivas.


# 📂 Estructura del proyecto

``` bash
market-value-football-tfm/

├── artifacts/                             # Artefactos persistidos de modelos y predicciones
│   ├── encoders/                          # Encoders categóricos serializados
│   ├── feature_importance/                # Importancia de variables exportada
│   ├── metadata/                          # Metadata y hashes de datasets versionados
│   ├── models/                            # Modelos entrenados (.joblib)
│   ├── predictions/                       # Predicciones persistidas
│   └── scalers/                           # Transformadores numéricos serializados
│
├── config/                                # Configuración centralizada del sistema
│   ├── config.yaml
│   ├── config_backup.yaml
│   ├── features.yaml                      # Configuración de feature engineering
│   ├── matching.yaml                      # Parámetros de matching
│   ├── modeling.yaml                      # Configuración de modelización
│   ├── paths.yaml                         # Paths del proyecto
│   ├── project.yaml                       # Configuración global
│   ├── scoring.yaml                       # Configuración de scoring y rankings
│   └── validation.yaml                    # Configuración centralizada de validación temporal
│
├── data/
│   ├── external/                          # Datos auxiliares externos
│   ├── interim/                           # Datos parcialmente transformados
│   ├── processed/                         # Datasets finales reutilizables
│   └── raw/                               # Datos originales sin procesar
│
├── docs/                                  # Documentación técnica y metodológica
│   ├── architecture.md                    # Arquitectura completa del sistema
│   ├── data_dictionary.md                 # Diccionario de variables y outputs
│   ├── data_quality.md                    # Evaluación de calidad de datos
│   ├── data_sources.md                    # Fuentes de datos y matching
│   ├── feature_engineering_plan.md        # Roadmap de feature engineering
│   ├── modeling_decisions.md              # Decisiones metodológicas de modelización
│   ├── pipeline_reference.md              # Referencia técnica de pipelines
│   ├── README.md                          # Índice central de documentación
│   └── schema_decisions.md                # Diseño de esquema y arquitectura de datos
│
├── logs/                                  # Logs de ejecución y debugging
│
├── mlruns/                                # Tracking experimental MLflow
│
├── notebooks/                             # Notebooks exploratorios y análisis
│   ├── 01_data_understanding.ipynb
│   ├── 02_econometric_baseline.ipynb
│   ├── 03_econometric_model.ipynb
│   └── 04_supervised_machine_learning.ipynb
│
├── reports/                               # Outputs analíticos y reporting
│   ├── figures/                           # Visualizaciones
│   ├── model_diagnostics/                 # Diagnósticos de modelos
│   ├── rankings/                          # Rankings scouting
│   ├── scouting_reports/                  # Reports automáticos futuros
│   └── tables/                            # Métricas y tablas exportadas
│
├── src/                                   # Lógica principal del sistema
│   ├── data/                              # Ingesta, matching y datasets
│   ├── features/                          # Feature engineering
│   ├── models/
│   │   ├── econometric/                   # Pipeline OLS
│   │   ├── evaluation/                    # Métricas y comparación
│   │   ├── machine_learning/              # Pipelines ML
│   │   └── scoring/                       # Inefficiency scoring
│   └── utils/                             # Utilidades compartidas
│       ├── config.py                      # Loader centralizado de configuración YAML
│       ├── dataset_versioning.py          # Versionado y hashing de datasets
│       └── experiment_tracking.py         # Integración MLflow
│
├── tests/                                 # Tests futuros
│
├── environment.yml                        # Entorno Conda
├── PROJECT_STATUS.md                      # Estado operativo del proyecto
├── README.md                              # Documentación principal
├── requirements-lock.txt                  # Dependencias fijadas
└── requirements.txt                       # Dependencias Python
```

---

# ▶️ Ejecución reproducible

## 1️⃣ Construir features FBref

``` bash
python -m src.data.build_fbref_features
```

---

## 2️⃣ Construir features Transfermarkt

``` bash
python -m src.data.build_transfermarkt_features
```

---

## 3️⃣ Construir panel jugador--temporada

``` bash
python -m src.data.build_player_season_panel
```

---

## 4️⃣ Construir dataset modelizable

``` bash
python -m src.data.build_modeling_dataset
```

---

## 5️⃣ Ejecutar pipeline econométrico

``` bash
python -m src.models.econometric.run_ols_pipeline
```

---

## 6️⃣ Ejecutar pipeline Machine Learning

``` bash
python -m src.models.machine_learning.run_ml_pipeline
```

---


## 7️⃣ Ejecutar Scoring Engine

```bash
python -m src.models.scoring.build_inefficiency_score
python -m src.models.scoring.build_growth_score
python -m src.models.scoring.build_confidence_score
python -m src.models.scoring.build_opportunity_score
python -m src.models.scoring.generate_rankings
```

---

## 8️⃣ Ejecutar capa de evaluación

```bash
python -m src.models.evaluation.build_ranking_diagnostics
python -m src.models.evaluation.build_roi_simulation
python -m src.models.evaluation.build_precision_at_k
```

---

# 📊 Resultados actuales

## Modelo econométrico final

Evaluación realizada mediante validación temporal estricta
out-of-sample.

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| OLS temporal final | 0.7947 | 0.9887 | 0.4366 |

---

## Interpretación metodológica

La degradación mínima respecto a modelos in-sample sugiere que:

``` text
el modelo mantiene capacidad explicativa robusta al generalizar hacia temporadas futuras
```

y que la señal predictiva proviene principalmente de variables
deportivas y contextuales, no de sobreajuste temporal.

---

## Machine Learning

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| OLS final | 0.7907 | 0.9823 | 0.4439 |
| Random Forest | 0.7704 | 0.9691 | 0.4587 |
| HistGradientBoosting | 0.7723 | 0.9680 | 0.4600 |
| Gradient Boosting | **0.7613** | **0.9493** | **0.4807** |

---

## Principales hallazgos

### 📌 La liga importa estructuralmente

-   Premier League → prima positiva
-   Eredivisie / Liga Portugal → descuentos estructurales

---

### 📌 Variables más relevantes

-   minutos jugados
-   goles por 90
-   asistencias por 90

---

### 📌 Insight metodológico clave

El hecho de que ML solo mejore moderadamente respecto a OLS indica que:

``` text
el principal cuello de botella actual es el signal predictivo del dataset
```

no necesariamente el algoritmo.

Esto refuerza la importancia futura de:

-   feature engineering avanzado
-   xG / xA
-   métricas defensivas
-   métricas de progresión

---

## Sprint 1 --- Positional Normalization Experiment

Se implementó un pipeline adicional de ingeniería de variables para
evaluar si una normalización contextual por posición y competición podía
mejorar la capacidad predictiva del modelo econométrico.

### Features añadidas

``` text
goals_per90_pos_z
assists_per90_pos_z
shots_per90_pos_z
goals_position_percentile
assists_position_percentile
```

Agrupación utilizada:

``` text
[position_group, league]
```

Motivación:

-   reducir sesgo ofensivo
-   mejorar comparabilidad entre jugadores
-   capturar diferencias estructurales entre ligas

### Resultados experimentales

| Modelo | RMSE ↓ | MAE ↓ | R² ↑ |
|---|---:|---:|---:|
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Advanced Positional OLS | 1.0065 | 0.8166 | 0.4148 |

Conclusión:

Las nuevas variables no produjeron mejoras significativas y mostraron
una ligera degradación del rendimiento.

Las variables se mantienen implementadas y registradas mediante MLflow,
pero no serán incorporadas al modelo econométrico final.

---

## Sprint 2 --- Temporal Dynamics & Growth Features

Se implementó un segundo bloque de ingeniería de variables centrado en
dinámica temporal y progresión del jugador.

La motivación es que el mercado de fichajes no valora únicamente el
rendimiento actual, sino también señales de crecimiento y trayectoria
profesional.

### Variables añadidas

``` text
market_value_growth_prev
delta_log_market_value_prev
age_squared
career_year
breakout_indicator
```

Descripción:

-   market_value_growth_prev → tendencia reciente de valoración
-   delta_log_market_value_prev → velocidad de crecimiento
-   age_squared → relación no lineal entre edad y valor
-   career_year → experiencia acumulada
-   breakout_indicator → identificación de jóvenes en explosión

### Resultados experimentales

| Modelo | RMSE ↓ | MAE ↓ | R² ↑ |
|---|---:|---:|---:|
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Positional OLS | 1.0065 | 0.8166 | 0.4148 |
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |

Conclusión:

Las variables temporales mejoraron significativamente la capacidad
predictiva del modelo.

El modelo Growth OLS pasa a ser el modelo econométrico preferente para
siguientes iteraciones.

---

## Sprint 3 --- Composite Football Indices

Se implementó un bloque adicional de ingeniería de variables orientado a
construir indicadores agregados de rendimiento futbolístico.

El objetivo no era únicamente mejorar capacidad predictiva sino aumentar
la interpretabilidad del sistema desde una perspectiva de scouting y
toma de decisiones.

### Índices creados

``` text
finishing_index
playmaking_index
growth_index
experience_index
```

Descripción:

-   finishing_index → capacidad ofensiva y finalización
-   playmaking_index → generación ofensiva y creación
-   growth_index → señales de crecimiento reciente
-   experience_index → madurez y experiencia acumulada

### Resultados experimentales

| Modelo | RMSE ↓ | MAE ↓ | R² ↑ |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Growth OLS + Composite Indices | 0.9046 | 0.7278 | 0.5255 |

Conclusión:

Los índices compuestos no aportaron mejora predictiva adicional.

Sin embargo, proporcionan una representación más interpretable del
rendimiento deportivo y se mantienen para tareas de scouting y análisis
descriptivo.

---

## Sprint 4 --- Machine Learning Baseline

Se implementó una primera línea base de modelos supervisados para
comparar el rendimiento predictivo frente al modelo econométrico.

El objetivo fue evaluar si modelos no lineales podían capturar
relaciones complejas entre rendimiento deportivo y valor de mercado.

### Modelos evaluados

-   Random Forest
-   XGBoost
-   LightGBM

### Estrategia de validación

Se utilizó división temporal:

``` text
Train: temporadas < 2023
Test: temporadas ≥ 2023
```

Esta decisión evita leakage temporal y simula un escenario real de
predicción futura.

### Resultados

| Modelo | RMSE ↓ | MAE ↓ | R² ↑ |
|---|---:|---:|---:|
| Growth OLS | **0.9046** | **0.7278** | **0.5255** |
| Random Forest | 1.0481 | 0.8527 | 0.3599 |
| XGBoost | 1.0943 | 0.8801 | 0.3022 |
| LightGBM | 1.1078 | 0.8936 | 0.2848 |

Conclusión:

Los modelos ML baseline no superaron al modelo econométrico actual.

---

## Sprint 4B --- Improved Machine Learning Pipeline

Tras comprobar que los modelos supervisados baseline no superaban al
benchmark econométrico, se implementó una segunda iteración del pipeline
de Machine Learning orientada a mejorar la capacidad predictiva mediante
preprocesamiento robusto, ajuste de hiperparámetros y trazabilidad
experimental.

### Objetivo

Mejorar el rendimiento de los modelos supervisados frente al modelo
Growth OLS mediante:

-   validación temporal estricta
-   pipeline de preprocesamiento reproducible
-   búsqueda aleatoria de hiperparámetros
-   registro experimental con MLflow
-   exportación de importancia de variables

### Implementación

Archivo principal:

``` text
src/models/machine_learning/train_ml_tuned.py
```

### Estrategia de validación

Se mantiene la división temporal:

``` text
Train: temporadas < 2023
Test: temporadas >= 2023
```

Esta decisión evita leakage temporal y reproduce un escenario realista
de scouting, donde el modelo se entrena con información histórica y se
evalúa sobre temporadas posteriores.

### Pipeline de preprocesamiento

Se implementó un pipeline basado en:

-   `ColumnTransformer`
-   `SimpleImputer`
-   `StandardScaler`
-   `OneHotEncoder`

Esto permite tratar de forma separada variables numéricas y categóricas,
reduciendo errores manuales y mejorando la reproducibilidad del
entrenamiento.

### Modelos evaluados

-   Tuned Random Forest
-   Tuned XGBoost
-   Tuned LightGBM
-   HistGradientBoosting

### Tuning

Se utilizó:

``` text
RandomizedSearchCV
n_iter = 12
```

El objetivo no fue realizar una búsqueda exhaustiva, sino obtener una
mejora razonable del rendimiento manteniendo control computacional y
trazabilidad metodológica.

### MLflow

Cada experimento registra:

-   hiperparámetros
-   métricas
-   artefactos
-   modelos entrenados
-   feature importance

### Feature importance

Las importancias de variables se exportan en:

``` text
artifacts/feature_importance/
```

### Resultados

| Modelo | RMSE ↓ | MAE ↓ | R² ↑ |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Tuned Random Forest | 0.9076 | 0.7315 | 0.5200 |
| Tuned XGBoost | **0.8753** | **0.7004** | **0.5536** |
| Tuned LightGBM | 0.8864 | 0.7162 | 0.5421 |
| HistGradientBoosting | 0.8825 | 0.7118 | 0.5462 |

### Conclusión

El pipeline mejorado de Machine Learning supera por primera vez al
modelo econométrico Growth OLS.

El mejor modelo actual es:

``` text
Tuned XGBoost
```

con:

``` text
R² = 0.5536
RMSE = 0.8753
MAE = 0.7004
```

La mejora relativa respecto a Growth OLS es aproximadamente del 5.3% en
R².

Este resultado justifica metodológicamente la transición desde un
enfoque puramente econométrico hacia modelos supervisados más complejos,
manteniendo la econometría como benchmark interpretable y utilizando
Machine Learning como capa predictiva adicional.

No obstante, la mejora sigue siendo moderada, por lo que la siguiente
fase debe centrarse en explicabilidad, feature importance y análisis
SHAP para convertir el modelo en una herramienta interpretable de
scouting cuantitativo.

---

## Sprint 4C --- Explainability + Player-Level SHAP Analysis

Tras obtener un modelo supervisado con mejor rendimiento predictivo que
el benchmark econométrico, el siguiente paso consistió en incorporar
mecanismos de explicabilidad que permitieran interpretar las
predicciones y convertir el sistema en una herramienta útil para
scouting profesional.

### Objetivo

Transformar el mejor modelo predictivo actual en un sistema explicable
mediante:

-   feature importance comparativa
-   SHAP global
-   SHAP local por jugador
-   informes automáticos de scouting

### Implementación

Nuevos módulos:

``` text
src/models/explainability/

├── build_feature_importance_comparison.py
├── build_shap_analysis.py
├── build_player_shap_report.py
```

### Outputs generados

``` text
reports/tables/explainability/

├── feature_importance_comparison_top10.csv
├── shap_global_importance.csv

reports/figures/explainability/

├── feature_importance_comparison_top10.png
├── shap_summary.png

reports/scouting_reports/

├── player_shap_report.csv
```

### Feature importance comparativa

Se construyó una comparación agregada entre:

-   Random Forest
-   Tuned Random Forest
-   Tuned XGBoost
-   Tuned LightGBM
-   Gradient Boosting

El objetivo fue identificar qué variables muestran una señal consistente
independientemente del algoritmo utilizado.

Resultados destacados:

-   experience_index
-   goals_position_percentile
-   log_minutes_played
-   finishing_index
-   playmaking_index

### SHAP Global Importance

La explicación basada en SHAP permitió estimar la contribución real de
cada variable sobre las predicciones individuales.

Top variables observadas:

| Variable | Importancia |
|---|---:|
| matches_played | 1.199 |
| age_fbref | 0.697 |
| minutes_played | 0.682 |
| starts | 0.676 |
| goals | 0.344 |

### Diferencias entre Feature Importance y SHAP

Se observaron diferencias relevantes:

Feature importance clásica:

-   experience_index
-   finishing_index
-   playmaking_index

SHAP:

-   matches_played
-   minutes_played
-   starts
-   goals

Interpretación:

La importancia clásica refleja cuánto utiliza el modelo una variable
durante la construcción de árboles, mientras que SHAP refleja el impacto
efectivo sobre las predicciones.

### SHAP por jugador

Se implementó un reporte individual que genera automáticamente:

-   factores positivos
-   factores negativos
-   valor esperado estimado
-   gap de mercado
-   inefficiency score

Ejemplo:

``` text
Jugador: Yan Diomandé

Factores positivos:

+ goals_per90
+ league_LaLiga
+ assists_per90

Factores negativos:

− log_minutes_played
− league_PremierLeague
```

### Conclusión

Sprint 4C transforma el sistema desde un modelo predictivo hacia una
herramienta de scouting cuantitativo interpretable.

La combinación:

``` text
Machine Learning + SHAP + scoring
```

permite explicar no únicamente qué jugador aparece como infravalorado,
sino también por qué.

---

# 📊 Sprint 6 --- Ranking Validation & Business Evaluation

Sprint 6 incorpora una capa de validación cuantitativa y evaluación de
negocio orientada a medir el valor real del sistema para scouting
profesional.

## Nuevos módulos

``` text
src/models/evaluation/

├── build_ranking_diagnostics.py
├── build_roi_simulation.py
├── build_precision_at_k.py
```

## Outputs generados

``` text
reports/model_diagnostics/
ranking_summary.csv
ranking_by_league.csv
ranking_by_position.csv
ranking_score_correlations.csv
ranking_tier_summary.csv
```

``` text
reports/business/
roi_simulation.csv
roi_global_summary.csv
transfer_strategy_analysis.csv
roi_scouting_shortlist.csv
roi_scouting_shortlist_summary.csv
```

## Precision@K

| K | Precision@K |
|---:|---:|
|10|0.90|
|20|0.90|
|50|0.90|
|100|0.85|

## Objetivo

Convertir el sistema en una herramienta de decisión cuantitativa para
priorización de fichajes.

---

## Sprint 7 --- Scouting Dashboard & Decision Support Layer

### Objetivo

Convertir el sistema desde un proyecto de modelización hacia una plataforma operativa de Football Analytics.

### Arquitectura funcional

```text
Modelos predictivos
↓
Scoring Engine
↓
Ranking Engine
↓
Explainability
↓
Dashboard Scouting
↓
Toma de decisión deportiva
```

### Contribución

El dashboard constituye la primera interfaz integrada del proyecto y conecta la capa analítica con la toma de decisiones de scouting.


# ⚖️ Trade-offs metodológicos

## Cobertura vs precisión

Decisión adoptada:

``` text
Priorizar cobertura muestral
```

---

## Interpretabilidad vs complejidad

Decisión adoptada:

``` text
OLS = modelo principal
ML = extensión predictiva
```

---

## Robustez vs coste computacional

Se optimizó:

-   matching jerárquico
-   reducción del espacio de búsqueda
-   filtrado temporal

---

# 🚀 Próximos pasos

## Prioridad inmediata

- integración Understat
- incorporación de xG y xA
- métricas defensivas avanzadas
- Perfil individual avanzado de jugador
- Radar comparativo de rendimiento
- Comparador entre jugadores
- Exportación PDF de shortlists
- Risk Score
- Simulación de escenarios de fichaje
- Business Validation Panel

---

## Fase posterior

-   dashboard interactivo
-   scouting reports automáticos PDF
-   simulación ROI de fichajes
-   despliegue analítico

# 🧠 Valor del proyecto

El proyecto aporta:

-   integración robusta de datos heterogéneos
-   arquitectura modular reproducible
-   validación temporal realista
-   modelización interpretable
-   comparación econometría vs ML
-   aplicación directa a scouting profesional
-   detección de ineficiencias de mercado
-   experiment tracking reproducible
-   scoring multicriterio para scouting
-   generación automática de rankings accionables
-   dataset versioning
-   analytics engineering aplicado
-   trazabilidad experimental completa
-   dashboard ejecutivo para scouting profesional
-   sistema visual de priorización de fichajes
-   decision support system aplicado al mercado de transferencias
-   visual analytics para departamentos deportivos

El sistema ya constituye una base sólida para:

-   sports analytics
-   scouting cuantitativo
-   econometría aplicada
-   machine learning supervisado
-   toma de decisiones deportivas

---

# 🎯 Contribución académica y técnica

La aportación del proyecto no se limita a la construcción de un modelo predictivo.

Contribuciones principales:

- integración multi-fuente FBref + Transfermarkt mediante matching jerárquico
- construcción de un panel longitudinal jugador–temporada
- diseño de una arquitectura reproducible basada en Analytics Engineering
- comparación rigurosa entre econometría y Machine Learning
- incorporación de explainability mediante SHAP
- transformación de predicciones en señales accionables de scouting
- evaluación mediante métricas estadísticas y métricas de negocio

La arquitectura aproxima un entorno real de Football Analytics profesional:

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
Scouting Intelligence
```

---

# ⚽ Aplicación profesional

La solución reproduce un flujo de trabajo habitual en departamentos de Football Analytics:

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

Aplicaciones:

- Recruitment Analytics
- Market Intelligence
- Scouting cuantitativo
- Player Trading Strategies
- Identificación de ineficiencias de mercado

---

# 👤 Autores

-   Isabel Muñoz Martín
-   Laura González Macho
-   Manuel Pérez Bañuls

Trabajo Fin de Máster --- Data Science aplicado al fútbol profesional.

Enfoque:

-   sports analytics
-   scouting cuantitativo
-   econometría aplicada
-   machine learning
-   analytics engineering
-   identificación de ineficiencias de mercado
