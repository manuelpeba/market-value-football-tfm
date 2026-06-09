# 📓 Notebooks Analíticos

<div align="center">

![Notebooks](https://img.shields.io/badge/Notebooks-Research%20Layer-blue)
![Methodology](https://img.shields.io/badge/Methodology-CRISP--DM-orange)
![Econometrics](https://img.shields.io/badge/Econometrics-OLS-success)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost-important)
![Version](https://img.shields.io/badge/Version-v1.2.1-purple)

</div>

---

# 🎯 Objetivo

Los notebooks constituyen la capa de investigación, validación metodológica y generación de evidencia empírica del proyecto.

Su función principal es documentar de forma reproducible el proceso completo de:

* construcción del dataset;
* evaluación de calidad;
* modelización econométrica;
* modelización supervisada;
* validación temporal;
* validación externa;
* evaluación incremental de variables;
* interpretación de resultados.

Los notebooks complementan la arquitectura productiva implementada en:

```text
src/
```

y deben interpretarse como artefactos de investigación y validación académica.

---

# 🧠 Filosofía metodológica

La secuencia sigue la adaptación CRISP-DM utilizada en el proyecto:

```text
Data Understanding
        ↓
Econometric Baseline
        ↓
Econometric Modeling
        ↓
Machine Learning
        ↓
External Validation
        ↓
Advanced Data Expansion
        ↓
Scoring & Decision Support
```

---

# 📚 Estructura actual

```text
notebooks/

├── 01_data_understanding.ipynb
├── 02_econometric_baseline.ipynb
├── 03_econometric_model.ipynb
├── 03_econometric_model_v13a1.ipynb
├── 03_econometric_model_v13b.ipynb
├── 04_supervised_machine_learning.ipynb
├── 04_supervised_machine_learning_v13a1.ipynb
└── Sprint 13B ML Re-estimation
```

---

# 📊 Estado actual

| Notebook                              | Estado       |
| ------------------------------------- | ------------ |
| 01 Data Understanding                 | ✅ Productivo |
| 02 Econometric Baseline               | ✅ Productivo |
| 03 Econometric Model                  | ✅ Productivo |
| 03 Econometric Model v13A.1           | ✅ Cerrado    |
| 03 Econometric Model v13B             | ✅ Cerrado    |
| 04 Supervised Machine Learning        | ✅ Productivo |
| 04 Supervised Machine Learning v13A.1 | ✅ Cerrado    |
| Sprint 13B ML Re-estimation           | ✅ Cerrado    |

---

# 01 — Data Understanding

## Objetivo

Realizar el análisis exploratorio inicial del dataset jugador-temporada y validar la calidad de los datos antes de la modelización.

---

## Contenido

### Calidad de datos

* valores nulos;
* duplicados;
* cobertura temporal;
* cobertura competitiva;
* cobertura por posición.

---

### Análisis descriptivo

* distribución del valor de mercado;
* distribución de edad;
* minutos disputados;
* métricas ofensivas;
* métricas defensivas.

---

### Validaciones

* coherencia temporal;
* análisis de outliers;
* validación de matching;
* representatividad del dataset.

---

## Pregunta de investigación

> ¿El dataset presenta calidad suficiente para modelar valor de mercado de forma robusta?

---

## Contribución

Este notebook constituye la base metodológica sobre la que se construyen todas las fases posteriores.

---

# 02 — Econometric Baseline

## Objetivo

Construir el benchmark econométrico inicial utilizado como referencia para todas las extensiones posteriores.

---

## Especificación base

```text
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
league FE +
position FE
```

---

## Contenido

### Transformaciones

* log_market_value_eur
* log_minutes_played

---

### Econometría

* OLS
* HC3 Robust Standard Errors
* League Fixed Effects
* Position Fixed Effects

---

### Diagnóstico

* R²
* MAE
* RMSE
* análisis de residuos
* VIF

---

## Objetivo metodológico

Establecer una referencia interpretable y académicamente defendible.

---

## Resultado

Este notebook define el punto de partida utilizado para evaluar la aportación incremental de nuevas variables y nuevas arquitecturas.

---

# 03 — Econometric Model

## Objetivo

Extender el baseline mediante variables longitudinales capaces de capturar dinámicas de crecimiento y desarrollo profesional.

---

## Growth Features

* market_value_growth_prev
* delta_log_market_value_prev
* age_squared
* career_year
* breakout_indicator

---

## Contenido

### Comparativa de modelos

* Baseline OLS
* Growth OLS

---

### Evaluación

* comparación de métricas;
* significancia estadística;
* interpretación económica;
* análisis de coeficientes.

---

## Pregunta de investigación

> ¿Las variables longitudinales aportan información incremental relevante para explicar valor de mercado?

---

## Resultado metodológico

La evidencia obtenida justifica la incorporación permanente de variables de crecimiento dentro de la arquitectura del proyecto.

---

## Modelo derivado

```text
Growth OLS
```

que posteriormente evoluciona hacia:

```text
Growth OLS v13B
```

tras la incorporación de nuevas métricas avanzadas.

---

# 03A.1 — Econometric External Validation

## Sprint 13A.1

Objetivo:

Evaluar la robustez del benchmark econométrico tras la expansión multi-liga.

---

## Comparación

```text
7 ligas
vs
11 ligas
```

---

## Evaluaciones realizadas

* estabilidad de coeficientes;
* capacidad explicativa;
* robustez de especificación;
* generalización competitiva.

---

## Contribución

Introducir una capa explícita de validación externa dentro de la metodología econométrica.

---

# 03B — Advanced Data Expansion

## Sprint 13B

Objetivo:

Evaluar si nuevas métricas avanzadas derivadas de FBref aportan capacidad explicativa adicional.

---

## Variables incorporadas

* finishing_index_v2
* availability_index
* defensive_activity_index

---

## Comparación principal

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

---

## Métricas adicionales

Se observan mejoras simultáneas en:

* MAE;
* RMSE;
* AIC;
* BIC.

---

## Hallazgo principal

Las nuevas métricas aportan señal explicativa incremental consistente.

---

## Resultado

```text
Growth OLS v13B
```

queda promovido como benchmark econométrico oficial del proyecto.

# 04 — Supervised Machine Learning

## Objetivo

Evaluar si algoritmos supervisados no lineales son capaces de mejorar la capacidad predictiva respecto al benchmark econométrico.

---

## Hipótesis

> Las relaciones entre rendimiento deportivo y valor de mercado contienen componentes no lineales que pueden ser capturados mediante algoritmos de Machine Learning.

---

## Modelos evaluados

### Baseline

* Random Forest
* Gradient Boosting
* HistGradientBoosting

---

### Modelos avanzados

* LightGBM
* XGBoost

---

## Pipeline

### Preprocesamiento

* imputación;
* encoding categórico;
* escalado cuando procede;
* validación temporal.

---

### Optimización

* RandomizedSearchCV;
* selección de hiperparámetros;
* validación reproducible.

---

### Evaluación

Métricas:

* RMSE;
* MAE;
* R².

---

## Pregunta de investigación

> ¿Los modelos no lineales superan consistentemente al benchmark econométrico?

---

## Resultado

La evidencia obtenida muestra que los algoritmos de boosting superan de forma consistente a los modelos lineales.

---

## Modelo derivado

```text id="s9i7f4"
Tuned XGBoost
```

que posteriormente evoluciona hacia:

```text id="g7l2vq"
Tuned XGBoost v13B
```

tras la expansión multi-liga y la incorporación de métricas avanzadas.

---

# 04A.1 — Machine Learning External Validation

## Sprint 13A.1

Objetivo:

Evaluar la robustez de los modelos de Machine Learning tras ampliar la cobertura competitiva.

---

## Comparación principal

```text id="w8k3ny"
7 ligas
vs
11 ligas
```

---

## Resultado principal

### Tuned XGBoost

| Dataset  |   RMSE |    MAE |     R² |
| -------- | -----: | -----: | -----: |
| 7 ligas  | 0.8892 | 0.7120 | 0.5414 |
| 11 ligas | 0.8525 | 0.6834 | 0.5664 |

---

## Hallazgo

La expansión multi-liga mejora simultáneamente:

* cobertura;
* representatividad;
* capacidad predictiva;
* validez externa.

---

## Contribución

Sprint 13A.1 introduce una capa explícita de evaluación de generalización dentro del proceso de modelización.

---

# 04B — Machine Learning Re-estimation

## Sprint 13B

Objetivo:

Evaluar el impacto de nuevas métricas avanzadas derivadas de FBref sobre el rendimiento de los algoritmos supervisados.

---

## Variables incorporadas

* finishing_index_v2
* availability_index
* defensive_activity_index

---

## Diseño experimental

Comparación:

```text id="r5g8nd"
Feature Set A (v13A)

vs

Feature Set B (v13B)
```

---

## Algoritmos evaluados

* Random Forest
* HistGradientBoosting
* LightGBM
* XGBoost

---

## Resultados

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

---

## Evidencia observada

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

---

## Interpretación

Este comportamiento aporta evidencia favorable porque:

* reduce riesgo de sobreajuste;
* reduce dependencia de una arquitectura específica;
* aumenta la confianza en la calidad de las nuevas variables.

---

## Hallazgo principal

La variable avanzada con mayor relevancia predictiva agregada es:

```text id="u6k1mz"
finishing_index_v2
```

---

## Resultado

```text id="r4n7pk"
Tuned XGBoost v13B
```

queda promovido como modelo productivo oficial.

---

# 🔬 Explainability

## Objetivo

Transformar modelos predictivos complejos en conocimiento interpretable para procesos reales de scouting y recruitment.

---

## Herramientas

### Feature Importance

Permite identificar variables relevantes a nivel global.

---

### SHAP

Permite interpretar:

* importancia global;
* contribución local;
* drivers individuales;
* explicación de recomendaciones.

---

## Preguntas que responde

```text id="c2f4jt"
¿Qué variables explican
el valor de mercado?

¿Por qué este jugador
aparece infravalorado?
```

---

## Sprint 13B

La incorporación de nuevas variables permite evaluar explícitamente su contribución.

Resultado principal:

```text id="v9y2qe"
finishing_index_v2
```

como variable avanzada más relevante.

---

# 🧪 Consideraciones metodológicas

## Unidad de análisis

```text id="j5r1bo"
Jugador – Temporada
```

---

## Cobertura actual

| Métrica            |                 Valor |
| ------------------ | --------------------: |
| Observaciones      |                 5.527 |
| Ligas              |                    11 |
| Temporadas         |                     7 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

---

## Variable objetivo

```python id="t3f4jw"
log_market_value_eur
```

---

## Justificación

La transformación logarítmica:

* reduce asimetría;
* estabiliza varianza;
* mejora interpretabilidad relativa;
* mejora comportamiento econométrico.

---

## Validación temporal

Principio:

```text id="d7n8hs"
Train precede siempre a Test
```

para reproducir escenarios reales de scouting y evitar leakage.

---

# 🎓 Contribución académica

Los notebooks constituyen la principal evidencia empírica utilizada en la memoria del TFM.

Permiten documentar:

* construcción del dataset;
* validación de calidad;
* econometría aplicada;
* Machine Learning supervisado;
* validación temporal;
* validación externa;
* evaluación incremental de features;
* interpretabilidad;
* reproducibilidad experimental.

---

## Contribuciones metodológicas principales

### Sprint 13A

```text id="e8k4zt"
External Validation
```

Demuestra capacidad de generalización fuera del universo competitivo original.

---

### Sprint 13B

```text id="m1t6qr"
Advanced Data Expansion
```

Demuestra que métricas avanzadas derivadas de FBref aportan señal predictiva incremental consistente.

---

# 🔗 Relación con la arquitectura

Los notebooks constituyen la capa de investigación sobre la que posteriormente se construyen:

```text id="h4q7nx"
Scoring
↓
Risk Assessment
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
```

---

# 📌 Estado actual

| Notebook                              | Estado       |
| ------------------------------------- | ------------ |
| 01 Data Understanding                 | ✅ Productivo |
| 02 Econometric Baseline               | ✅ Productivo |
| 03 Econometric Model                  | ✅ Productivo |
| 03 Econometric Model v13A.1           | ✅ Cerrado    |
| 03 Econometric Model v13B             | ✅ Cerrado    |
| 04 Supervised Machine Learning        | ✅ Productivo |
| 04 Supervised Machine Learning v13A.1 | ✅ Cerrado    |
| Sprint 13B ML Re-estimation           | ✅ Cerrado    |

---

# 🛣️ Próxima fase

Sprint 13B queda oficialmente completado.

La hipótesis principal queda validada:

```text id="g8v5nb"
Las métricas avanzadas derivadas de FBref
aportan mejora predictiva consistente
en econometría y Machine Learning.
```

---

## Backlog asociado

```text id="f3p8lh"
TM.2 — Scoring & Ranking Integration v13B
```

Objetivo:

```text id="y9r6jt"
Predictions v13B
↓
Scoring Dataset v13B
↓
Opportunity Framework v13B
↓
Rankings v13B
```

---

## Siguiente desarrollo oficial

```text id="r2m7cw"
Sprint 14
↓
Transfer Strategy Enhancement
```

orientado a transformar inteligencia de scouting en estrategias óptimas de construcción de plantilla.

---

# 🏁 Conclusión

La evolución de los notebooks puede resumirse mediante:

```text id="z5t9dk"
Data Understanding
↓
Econometric Baseline
↓
Growth Modeling
↓
Machine Learning
↓
External Validation
↓
Advanced Data Expansion
↓
Scouting Intelligence
```

La release:

```text id="n4q8xb"
v1.2.1 — Advanced Data Expansion
```

consolida una capa de investigación reproducible, rigurosa y alineada con estándares académicos de Ciencia de Datos, Econometría Aplicada y Football Analytics.

Los notebooks proporcionan la evidencia empírica que sustenta todas las decisiones metodológicas adoptadas y constituyen la base científica sobre la que se construyen las capas operativas de scouting, recruitment y soporte avanzado a decisiones deportivas.
