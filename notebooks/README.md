# 📓 Notebooks Analíticos — Sprint 10

## 🎯 Objetivo

Los notebooks de Sprint 10 constituyen la capa analítica y metodológica del TFM. Su finalidad es documentar de forma reproducible el proceso de modelización, validación y generación de evidencia empírica que sustenta el sistema de identificación de jugadores infravalorados.

La secuencia sigue la lógica CRISP-DM adoptada en el proyecto:

```text
Data Understanding
        ↓
Econometric Baseline
        ↓
Econometric Modeling
        ↓
Supervised Machine Learning
        ↓
Scoring & Decision Support
```

Estos notebooks complementan la arquitectura productiva implementada en `src/` y deben interpretarse como artefactos de investigación y validación metodológica, no como pipelines operativos.

---

# 📚 Estructura

```text
notebooks/

├── 01_data_understanding.ipynb
├── 02_econometric_baseline.ipynb
├── 03_econometric_model.ipynb
└── 04_supervised_machine_learning.ipynb
```

---

# 01 — Data Understanding

## Objetivo

Realizar el análisis exploratorio inicial del dataset jugador–temporada y validar la calidad de los datos antes de la modelización.

## Contenido

### Calidad de datos

- valores nulos
- duplicados
- cobertura temporal
- cobertura por liga
- cobertura por posición

### Análisis descriptivo

- distribución del valor de mercado
- distribución de edad
- minutos jugados
- métricas ofensivas
- métricas defensivas

### Validaciones

- coherencia temporal
- análisis de outliers
- evaluación del matching
- análisis de representatividad

## Outputs principales

- estadísticas descriptivas
- tablas resumen
- visualizaciones exploratorias
- conclusiones de calidad de datos

## Pregunta de investigación

> ¿El dataset presenta calidad suficiente para modelar valor de mercado de forma robusta?

---

# 02 — Econometric Baseline

## Objetivo

Construir el benchmark econométrico inicial sobre el que comparar posteriores extensiones y modelos de Machine Learning.

## Especificación

```text
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
league FE +
position FE
```

## Contenido

### Transformaciones

- log_market_value_eur
- log_minutes_played

### Econometría

- OLS
- HC3 robust standard errors
- fixed effects por liga
- fixed effects por posición

### Diagnóstico

- R²
- MAE
- RMSE
- análisis de residuos
- multicolinealidad (VIF)

## Objetivo metodológico

Establecer una referencia interpretable y académicamente defendible.

---

# 03 — Econometric Model

## Objetivo

Extender el baseline mediante variables longitudinales y de trayectoria para capturar dinámicas de crecimiento y potencial de revalorización.

## Variables incorporadas

### Growth Features

- market_value_growth_prev
- delta_log_market_value_prev
- age_squared
- career_year
- breakout_indicator

### Variables contextuales

- experiencia acumulada
- evolución reciente
- trayectoria profesional

## Contenido

### Comparativa de modelos

- Baseline OLS
- Growth OLS

### Evaluación

- comparación de métricas
- significancia estadística
- interpretación económica
- análisis de coeficientes

## Pregunta de investigación

> ¿Las variables de crecimiento aportan información incremental relevante sobre el valor de mercado?

## Resultado esperado

Growth OLS como benchmark econométrico final del proyecto.

---

# 04 — Supervised Machine Learning

## Objetivo

Comparar modelos supervisados frente al benchmark econométrico para evaluar posibles ganancias predictivas.

## Modelos evaluados

### Baseline

- Random Forest
- Gradient Boosting
- HistGradientBoosting

### Modelos avanzados

- XGBoost
- LightGBM

### Pipeline

- imputación
- escalado
- encoding categórico
- validación temporal
- RandomizedSearchCV

## Evaluación

### Métricas

- RMSE
- MAE
- R²

### Comparación

```text
Growth OLS
vs
Tuned ML Models
```

### Interpretabilidad

- feature importance
- drivers principales
- preparación para SHAP

## Pregunta de investigación

> ¿Los modelos no lineales mejoran la capacidad predictiva respecto al benchmark econométrico?

---

# 🔬 Consideraciones metodológicas

## Unidad de análisis

```text
Jugador – Temporada
```

## Validación temporal

```text
Train:
2019-2020 → 2022-2023

Test:
2023-2024

Scoring reciente:
2024-2025
```

La validación temporal evita leakage y reproduce escenarios reales de scouting.

## Variable objetivo

```python
log_market_value_eur
```

Se utiliza transformación logarítmica para:

- reducir asimetría
- estabilizar varianza
- mejorar interpretabilidad relativa

---

# 🎓 Contribución académica

Los notebooks permiten documentar:

- construcción del dataset modelizable
- validación econométrica
- comparación OLS vs ML
- evaluación temporal out-of-sample
- justificación metodológica de decisiones de modelización

Constituyen la principal evidencia empírica utilizada en la memoria del TFM.

---

# 🔗 Relación con Sprint 10

Sprint 10 incorpora una nueva capa de inteligencia deportiva basada en:

- Player Radar
- Positional Benchmarking
- Percentiles por posición
- Comparativas individuales
- Interpretación visual del rendimiento

Los notebooks proporcionan la base analítica sobre la que posteriormente se construyen las capas de:

```text
Scoring
↓
Visual Analytics
↓
Decision Support
↓
Player Intelligence
```

---

# 📌 Estado

| Notebook | Estado |
|-----------|-----------|
| 01 Data Understanding | ✅ Release v1.0 |
| 02 Econometric Baseline | ✅ Release v1.0 |
| 03 Econometric Model | ✅ Release v1.0 |
| 04 Supervised Machine Learning | ✅ Release v1.0 |

