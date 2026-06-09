# 📊 Market Value Dynamics and Market Inefficiency Detection in Professional Football

### Identificación de jugadores infravalorados en el mercado de fichajes europeo

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Econometrics-green)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow)
![MLflow](https://img.shields.io/badge/MLflow-enabled-success)
![SHAP](https://img.shields.io/badge/Explainability-SHAP-success)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![Status](https://img.shields.io/badge/Status-Decision%20Support%20System-success)
![Coverage](https://img.shields.io/badge/Coverage-11%20Leagues-success)
![Matching](https://img.shields.io/badge/Matching-75.97%25-yellow)
![Version](https://img.shields.io/badge/version-v1.2.1-blue)

---

## Historial de releases

| Release | Contenido principal                             |
| ------- | ----------------------------------------------- |
| v0.1.0  | Data Pipeline                                   |
| v0.2.0  | Econometric Baseline                            |
| v0.3.0  | MLflow                                          |
| v0.4.0  | Machine Learning                                |
| v0.5.0  | Explainability                                  |
| v0.6.0  | Scoring Engine                                  |
| v0.7.0  | Dashboard                                       |
| v0.8.0  | Dashboard Productizado                          |
| v1.0.0  | Scouting Intelligence Platform                  |
| v1.1.0  | Strategic Recruitment & Decision Support System |
| v1.2.0  | Multi-League Expansion                          |
| v1.2.1  | Advanced Data Expansion                         |

---

## 📑 Tabla de contenidos

* [🧠 Resumen ejecutivo](#-resumen-ejecutivo)
* [📌 Resultados clave](#-resultados-clave)
* [🎯 Problema de negocio](#-problema-de-negocio)
* [🎯 Objetivos del proyecto](#-objetivos-del-proyecto)
* [🏆 Contribuciones del proyecto](#-contribuciones-del-proyecto)
* [🏗️ Arquitectura global](#️-arquitectura-global)
* [📚 Metodología](#-metodología)
* [📦 Datos y preparación](#-datos-y-preparación)
* [📈 Modelización](#-modelización)
* [📊 Evaluación y resultados](#-evaluación-y-resultados)
* [🖥️ Evolución hacia un DSS](#️-evolución-hacia-un-dss)
* [⚽ Valor para departamentos deportivos](#-valor-para-departamentos-deportivos)
* [✅ Estado actual del proyecto](#-estado-actual-del-proyecto)
* [⚠️ Limitaciones](#️-limitaciones)
* [🛣️ Roadmap](#️-roadmap)
* [📂 Estructura del proyecto](#-estructura-del-proyecto)
* [🔁 Reproducibilidad](#-reproducibilidad)
* [▶️ Ejecución reproducible](#️-ejecución-reproducible)
* [📚 Referencias](#-referencias)
* [👨‍🎓 Autoría](#-autoría)
* [🏁 Conclusión](#-conclusión)

---

## 🧠 Resumen ejecutivo

Este Trabajo Fin de Máster desarrolla una plataforma integral de Football Analytics orientada a la identificación de jugadores infravalorados en el mercado europeo de fichajes.

El proyecto combina técnicas de:

* Econometría aplicada.
* Machine Learning supervisado.
* Explainable AI.
* Scoring multicriterio.
* Visual Analytics.
* Decision Support Systems.

El objetivo es transformar grandes volúmenes de datos futbolísticos y de mercado en recomendaciones accionables para departamentos de scouting, recruitment y dirección deportiva.

La plataforma desarrollada permite:

* Estimar el valor de mercado esperado de jugadores profesionales.
* Detectar ineficiencias de mercado.
* Identificar oportunidades potenciales de fichaje.
* Cuantificar el riesgo asociado a cada recomendación.
* Construir shortlists de scouting.
* Comparar candidatos de forma simultánea.
* Apoyar procesos de toma de decisiones mediante un sistema DSS interactivo.
* Optimizar carteras de fichajes bajo restricciones de presupuesto y riesgo.
* Simular estrategias de recruitment alternativas mediante escenarios.

La versión actual corresponde a:

```text
v1.2.1 — Advanced Data Expansion
```

La release v1.2.1 consolida los resultados obtenidos durante Sprint 13A — Multi-League Expansion y Sprint 13B — Advanced Data Expansion.

Sprint 13A amplió la cobertura competitiva del sistema desde siete hasta once ligas europeas e incorporó una evaluación explícita de validez externa mediante expansión multi-liga, auditoría de cobertura y validación temporal multi-competición.

Sobre esta nueva base de datos ampliada, Sprint 13B evaluó el impacto de incorporar métricas avanzadas derivadas de FBref mediante la construcción de nuevas variables sintéticas de rendimiento futbolístico.

Las variables:

* finishing_index_v2
* availability_index
* defensive_activity_index

fueron incorporadas al pipeline de modelización y evaluadas tanto mediante econometría como mediante Machine Learning.

Los resultados obtenidos muestran que las nuevas variables generan mejoras consistentes en todas las arquitecturas analíticas evaluadas, aportando evidencia favorable sobre el valor incremental de las métricas avanzadas para la estimación del valor de mercado.

La release mantiene la arquitectura DSS desarrollada en fases anteriores e incorpora simultáneamente una expansión competitiva, una ampliación del espacio de variables y un reentrenamiento completo de los modelos productivos sobre el mayor universo analítico utilizado por el proyecto hasta la fecha.

---

## 📌 Resultados clave

| Indicador                      |                                           Valor |
| ------------------------------ | ----------------------------------------------: |
| Ligas cubiertas                |                                              11 |
| Temporadas                     |                                               7 |
| Combinaciones liga-temporada   |                                              77 |
| Observaciones FBref procesadas |                                          43.591 |
| Dataset modelizable            |                                           5.527 |
| Match Rate global              |                                          75,97% |
| Nuevas variables avanzadas     |                                               3 |
| ΔR² Econometría Sprint 13B     |                                         +0.0044 |
| ΔR² XGBoost Sprint 13B         |                                         +0.0096 |
| Mejor mejora observada         |                              LightGBM (+0.0291) |
| Modelo econométrico oficial    |                                 Growth OLS v13B |
| Modelo ML oficial              |                              Tuned XGBoost v13B |
| Precision@10                   |                                             90% |
| Estado actual                  | DSS + Multi-League Coverage + Advanced Features |

---

## 🎯 Problema de negocio

La toma de decisiones en el mercado de fichajes se caracteriza por:

* Información incompleta.
* Elevada incertidumbre.
* Recursos limitados.
* Sesgos cognitivos.
* Asimetrías informativas.

Los clubes deben seleccionar un número reducido de objetivos dentro de un universo potencialmente compuesto por miles de futbolistas distribuidos entre múltiples ligas y competiciones.

La pregunta central del proyecto es:

> ¿Qué jugadores presentan un valor de mercado observado inferior al valor que cabría esperar dadas sus características deportivas, edad, experiencia y rendimiento reciente?

Responder a esta cuestión permite detectar potenciales ineficiencias de mercado y apoyar estrategias de captación basadas en creación de valor.

---

## 🎯 Objetivos del proyecto

### Objetivo empresarial

Desarrollar una metodología reproducible capaz de identificar jugadores infravalorados bajo una lógica:

```text
Buy Low
↓
Develop
↓
Sell High
```

con potencial aplicación en departamentos de scouting profesional.

### Objetivos analíticos

1. Construir un dataset longitudinal jugador-temporada mediante integración multi-fuente.

2. Modelizar el valor de mercado esperado mediante técnicas econométricas y de Machine Learning.

3. Comparar capacidad predictiva e interpretabilidad entre ambos enfoques.

4. Diseñar métricas compuestas orientadas a scouting.

5. Implementar una capa de soporte a decisiones basada en rankings, scoring y visual analytics.

6. Transformar resultados analíticos en procesos operativos de scouting y recruitment.

---

## 🏆 Contribuciones del proyecto

### Contribuciones académicas

* Aplicación de CRISP-DM al ámbito del fútbol profesional.
* Integración de econometría y Machine Learning dentro de un mismo marco metodológico.
* Validación temporal estricta para aproximar escenarios reales de uso.
* Evaluación orientada a negocio mediante métricas de scouting.
* Estudio aplicado de ineficiencias de mercado en fútbol europeo.
* Evaluación explícita de validez externa mediante expansión multi-liga.
* Evaluación explícita de capacidad de generalización en contextos competitivos heterogéneos.
* Auditoría sistemática de cobertura multi-fuente.
* Evaluación empírica del valor incremental de métricas avanzadas de rendimiento futbolístico.
* Validación cruzada de nuevas variables mediante enfoques econométricos y de Machine Learning.

### Contribuciones técnicas

* Matching multi-fuente FBref ↔ Transfermarkt.
* Arquitectura modular reproducible.
* Experiment tracking mediante MLflow.
* Explainability basada en SHAP.
* Opportunity Score.
* Risk Framework.
* Decision Support System interactivo.
* Multi-League Expansion.
* League Coverage Diagnostics.
* External Validity Assessment.
* Advanced Feature Engineering.
* FBref Advanced Metrics Integration.
* Composite Football Indices v2.

### Contribuciones de negocio

* Opportunity Detection.
* Risk Assessment.
* Recruitment Intelligence.
* Candidate Comparison.
* Recruitment Board.
* Transfer Strategy Engine.
* Portfolio Optimization.
* Decision Support System.

## 🏗️ Arquitectura global

La arquitectura final se organiza en múltiples capas analíticas especializadas orientadas a transformar datos deportivos en decisiones accionables.

```text
Raw Sources
↓
Feature Engineering
↓
Matching Layer
↓
Player Season Panel
↓
Modeling Dataset
↓
Econometric Model
↓
Machine Learning Model
↓
Opportunity Detection
↓
Risk Assessment
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
External Validation
↓
Decision Support System
```

### Evolución metodológica

La evolución funcional del proyecto puede resumirse mediante la siguiente secuencia:

```text
Econometric Model
↓
Machine Learning
↓
Opportunity Detection
↓
Risk Assessment
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
↓
External Validation
```

Esta evolución refleja la transición desde una investigación centrada exclusivamente en predicción de valor de mercado hacia una plataforma orientada a la toma de decisiones deportivas.

La release v1.2.1 incorpora además una nueva capa de enriquecimiento analítico mediante métricas avanzadas derivadas de FBref.

```text
FBref
↓
Advanced Metrics Layer
↓
Composite Indices v2
↓
Modeling Dataset
↓
Predictive Models
```

Esta ampliación no modifica la arquitectura conceptual del sistema, pero incrementa la riqueza informativa disponible para la estimación del valor de mercado esperado.

---

## 📚 Metodología

El proyecto sigue una adaptación de la metodología CRISP-DM aplicada al contexto del fútbol profesional.

```mermaid
flowchart LR

A[Business Understanding]
--> B[Data Understanding]
--> C[Data Preparation]
--> D[Modeling]
--> E[Evaluation]
--> F[Deployment]
```

### 1. Business Understanding

Definición del problema de negocio y de los objetivos asociados a la identificación de jugadores infravalorados.

### 2. Data Understanding

Análisis exploratorio de las fuentes utilizadas, cobertura de datos, calidad de información y compatibilidad entre sistemas.

### 3. Data Preparation

Procesos de matching, limpieza, normalización, feature engineering y construcción del panel longitudinal.

### 4. Modeling

Desarrollo y comparación de modelos econométricos y de Machine Learning para estimar el valor de mercado esperado.

### 5. Evaluation

Evaluación mediante métricas técnicas y métricas de negocio orientadas a procesos de scouting.

### 6. Deployment

Implementación de los resultados mediante artefactos reproducibles, MLflow y un dashboard interactivo orientado a soporte a decisiones.

---

## 📦 Datos y preparación

### Fuentes de datos

El proyecto integra dos fuentes complementarias de información deportiva y de mercado.

#### FBref

Fuente principal de rendimiento deportivo.

Variables utilizadas:

* Minutos disputados.
* Goles.
* Asistencias.
* Producción ofensiva.
* Acciones defensivas.
* Progresión y posesión.
* Indicadores avanzados normalizados por 90 minutos.

Durante Sprint 13B se incorporó una capa adicional de explotación de métricas avanzadas procedentes de tablas especializadas de FBref, permitiendo construir nuevas variables sintéticas orientadas a capturar dimensiones futbolísticas complejas relacionadas con finalización, disponibilidad competitiva y actividad defensiva.

---

#### Transfermarkt

Fuente principal de información de mercado.

Variables utilizadas:

* Valor de mercado.
* Edad.
* Posición.
* Club.
* Histórico de valor.
* Contexto competitivo.

---

### Cobertura geográfica

La versión actual incorpora once ligas europeas:

* Premier League
* LaLiga
* Bundesliga
* Serie A
* Ligue 1
* Eredivisie
* Liga Portugal
* Championship
* Belgian Pro League
* Austrian Bundesliga
* Segunda División de España

Cobertura temporal:

```text
2019-2020 → 2025-2026

11 ligas
77 combinaciones liga-temporada
```

---

## 🔗 Matching multi-fuente

Uno de los principales retos metodológicos del proyecto fue la ausencia de un identificador universal compartido entre FBref y Transfermarkt.

Para resolver este problema se diseñó un pipeline específico de matching jerárquico capaz de maximizar la calidad de emparejamiento sin comprometer la precisión de los registros.

### Flujo de matching

```text
Normalización
↓
Exact Matching
↓
Club Validation
↓
Fuzzy Matching
↓
Age Validation
```

### Resultados

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Match Rate global              | 75,97% |

La reducción del match rate global respecto a versiones anteriores se explica por la incorporación de ligas secundarias con menor cobertura histórica en Transfermarkt-Kaggle y no por modificaciones del algoritmo de matching.

---

## 📊 Dataset final

Tras los procesos de integración, validación y preparación se construye un panel longitudinal jugador-temporada.

### Panel completo

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Combinaciones liga-temporada   |     77 |

### Dataset modelizable

La fase de modelización se centra en jugadores jóvenes con potencial de desarrollo y revalorización.

| Métrica       | Valor |
| ------------- | ----: |
| Observaciones | 5.527 |
| Ligas         |    11 |
| Temporadas    |     7 |

El dataset productivo actual corresponde a:

```text
player_season_modeling_v13b_productive_candidate.parquet
```

e incorpora las variables avanzadas promovidas tras la validación experimental de Sprint 13B.

---

## ⚙️ Feature Engineering

El proyecto incorpora múltiples capas de transformación orientadas a capturar rendimiento, experiencia y evolución temporal.

### Variables de crecimiento

Diseñadas para modelar la trayectoria reciente del jugador.

Ejemplos:

* market_value_growth_prev
* delta_log_market_value_prev
* breakout_indicator
* career_year

### Composite Football Indices

Indicadores sintéticos construidos para representar dimensiones futbolísticas complejas.

Ejemplos:

* finishing_index
* playmaking_index
* experience_index
* growth_index

### Advanced Football Indices (Sprint 13B)

Como resultado de la fase Advanced Data Expansion se incorporan tres nuevas variables sintéticas:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables agregan información procedente de métricas avanzadas de FBref y representan la principal contribución analítica de Sprint 13B.

Entre ellas, **finishing_index_v2** emerge como la variable avanzada con mayor relevancia predictiva agregada en los modelos evaluados.

### Transformaciones aplicadas

* Transformaciones logarítmicas.
* Escalado robusto.
* Winsorización.
* Estandarización.

Estas transformaciones permiten reducir la influencia de valores extremos y mejorar la estabilidad de los modelos predictivos.

---

## 📈 Modelización

### Modelización econométrica

La primera aproximación metodológica del proyecto se basa en econometría aplicada al fútbol profesional.

Su objetivo es construir un modelo interpretable capaz de estimar el valor de mercado esperado de un jugador.

#### Variable objetivo

```text
log_market_value_eur
```

Se utiliza la transformación logarítmica para reducir asimetrías y estabilizar la varianza observada en los valores de mercado.

#### Benchmark econométrico

Modelo final:

```text
Growth OLS v13B
```

Variables utilizadas:

* Edad.
* Experiencia.
* Rendimiento deportivo.
* Variables de crecimiento.
* Indicadores compuestos.
* Métricas avanzadas Sprint 13B.

#### Resultados

| Modelo          |    MAE |   RMSE |     R² |
| --------------- | -----: | -----: | -----: |
| Growth OLS v13B | Mejora | Mejora | 0.4549 |

#### Evaluación Sprint 13B

Comparación principal:

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

Adicionalmente se observaron mejoras simultáneas en:

* RMSE
* MAE
* AIC
* BIC

#### Conclusión

La evidencia obtenida sugiere que las métricas avanzadas incorporadas durante Sprint 13B aportan capacidad explicativa incremental dentro de la especificación econométrica.

---

### Machine Learning

Tras establecer el benchmark econométrico se desarrolla una segunda capa basada en Machine Learning supervisado.

#### Algoritmos evaluados

* Random Forest
* HistGradientBoosting
* LightGBM
* XGBoost

Todos los modelos fueron optimizados mediante búsqueda sistemática de hiperparámetros.

#### Modelo productivo

Tras la evaluación comparativa se selecciona:

```text
Tuned XGBoost v13B
```

como modelo operativo de la plataforma.

#### Resultados Sprint 13B

Comparación principal:

| Modelo               | R² v13A | R² v13B |     ΔR² |
| -------------------- | ------: | ------: | ------: |
| XGBoost              |  0.4357 |  0.4453 | +0.0096 |
| Random Forest        |       — |       — | +0.0097 |
| HistGradientBoosting |       — |       — | +0.0144 |
| LightGBM             |       — |       — | +0.0291 |

La mejora más elevada se observa en LightGBM, mientras que XGBoost mantiene el mejor equilibrio global entre rendimiento predictivo, estabilidad y capacidad operativa.

#### Hallazgo metodológico

Uno de los resultados más relevantes de Sprint 13B es que todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento reduce significativamente el riesgo de que las conclusiones dependan de una única familia de modelos y aporta robustez adicional a la validación experimental realizada.

#### Decisión metodológica

```text
Growth OLS v13B
=
Benchmark interpretable

Tuned XGBoost v13B
=
Modelo productivo
```

Esta separación combina rigor académico, interpretabilidad y capacidad predictiva.
## 🔬 Experiment Tracking con MLflow

El proyecto incorpora una capa completa de trazabilidad experimental mediante MLflow.

### Información registrada

#### Parámetros

* Hiperparámetros.
* Configuraciones.
* Seeds.

#### Métricas

* MAE.
* RMSE.
* R².
* Métricas de negocio.

#### Artefactos

* Modelos serializados.
* Gráficos.
* Tablas.
* Datasets.

MLflow permite reconstruir completamente cualquier experimento ejecutado durante el desarrollo del proyecto.

Además, la integración de MLflow resulta especialmente relevante a partir de Sprint 13A y Sprint 13B, donde la comparación sistemática entre versiones de datasets, espacios de variables y arquitecturas de modelización requiere un seguimiento riguroso de resultados y configuraciones experimentales.

---

## 🔍 Explainability

La plataforma incorpora Explainable AI mediante SHAP para reducir la opacidad del modelo productivo.

### Explainability global

Permite responder a la pregunta:

> ¿Qué variables son más importantes para el modelo?

Outputs generados:

* Feature Importance.
* SHAP Importance.
* Summary Plot.

### Explainability local

Permite responder a la pregunta:

> ¿Por qué el modelo estima un valor determinado para este jugador?

Outputs generados:

* Drivers positivos.
* Drivers negativos.
* Explicación individual.

La interpretabilidad constituye un elemento fundamental para facilitar la adopción de modelos analíticos dentro de entornos profesionales de scouting.

### Sprint 13B — Explainability de variables avanzadas

La incorporación de nuevas variables derivadas de FBref permitió evaluar su relevancia dentro de los modelos predictivos.

Los análisis de importancia realizados durante Sprint 13B muestran que:

```text id="8yvf6o"
finishing_index_v2
```

se posiciona como la variable avanzada con mayor capacidad explicativa agregada.

Este resultado aporta evidencia adicional de que determinadas métricas avanzadas de rendimiento contienen señal útil para aproximar la valoración económica de futbolistas profesionales.

---

## 📊 Evaluación y resultados

La evaluación se realiza mediante validación temporal estricta para aproximar escenarios reales de utilización en scouting profesional.

### Esquema temporal

```text id="7gl4p8"
Train:
2019-2020 → 2024-2025

Current Scouting:
2025-2026
```

La temporada 2025-2026 queda reservada para explotación operativa y no participa en el entrenamiento de modelos.

---

### Evaluación técnica

#### Modelos oficiales v1.2.1

| Modelo             | Rol                    | Estado  |
| ------------------ | ---------------------- | ------- |
| Growth OLS v13B    | Benchmark econométrico | Oficial |
| Tuned XGBoost v13B | Modelo productivo      | Oficial |

---

### Sprint 13A.1 — External Validation

```text id="j7vg8g"
Pregunta metodológica:

¿La metodología mantiene su comportamiento
al ampliarse el universo competitivo?
```

Resultados:

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

Conclusión:

La expansión multi-liga no solo incrementa cobertura sino que mejora el rendimiento predictivo, reforzando la validez externa de la metodología.

---

### Sprint 13B — Advanced Data Expansion

```text id="7u6m7z"
Pregunta metodológica:

¿Las métricas avanzadas de rendimiento
aportan información adicional para explicar
el valor de mercado de los futbolistas?
```

Hipótesis:

Las métricas avanzadas derivadas de FBref contienen información complementaria capaz de mejorar la estimación del valor de mercado esperado.

---

#### Nuevas variables incorporadas

Sprint 13B introduce tres nuevas variables oficiales:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables fueron construidas a partir de métricas avanzadas de rendimiento deportivo integradas desde FBref.

---

#### Resultados econométricos

Comparación principal:

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="b2xj7w"
ΔR² = +0.0044
```

Adicionalmente se observan mejoras simultáneas en:

* RMSE.
* MAE.
* AIC.
* BIC.

Interpretación:

Las variables avanzadas aportan capacidad explicativa incremental dentro de la especificación econométrica.

---

#### Resultados Machine Learning

Comparación Feature Set A vs Feature Set B.

##### Tuned XGBoost

| R² v13A | R² v13B |     ΔR² |
| ------- | ------: | ------: |
| 0.4357  |  0.4453 | +0.0096 |

##### HistGradientBoosting

```text id="jjlwmq"
ΔR² = +0.0144
```

##### LightGBM

```text id="uzifwd"
ΔR² = +0.0291
```

Mejor mejora observada.

##### Random Forest

```text id="v4y5th"
ΔR² = +0.0097
```

---

#### Hallazgo metodológico principal

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento constituye una evidencia especialmente relevante porque:

* reduce el riesgo de dependencia de una única arquitectura;
* refuerza la robustez de los resultados;
* fortalece la validez metodológica de la hipótesis planteada.

---

#### Conclusión Sprint 13B

La hipótesis queda validada.

Las métricas avanzadas derivadas de FBref aportan señal predictiva adicional tanto en econometría como en Machine Learning.

La evidencia observada sugiere que dimensiones futbolísticas asociadas a finalización, disponibilidad competitiva y actividad defensiva contienen información económicamente relevante para explicar las valoraciones de mercado.

---

### Evaluación de negocio

La utilidad práctica del sistema se evalúa mediante métricas orientadas a scouting.

#### Precision@K

|   K | Precision@K |
| --: | ----------: |
|  10 |        0.90 |
|  20 |        0.90 |
|  50 |        0.90 |
| 100 |        0.85 |

Estas métricas permiten evaluar la capacidad real del sistema para priorizar oportunidades de mercado relevantes.

---

### Conclusiones analíticas

Los resultados obtenidos muestran que:

* El matching multi-fuente alcanza niveles elevados de calidad.
* La expansión multi-liga mejora simultáneamente cobertura y capacidad predictiva.
* Las métricas avanzadas aportan capacidad explicativa incremental.
* El modelo XGBoost supera consistentemente al benchmark econométrico.
* Las métricas de negocio validan la utilidad operativa del sistema.
* La combinación de predicción, scoring y explainability permite construir recomendaciones reproducibles para procesos de scouting profesional.

La base analítica desarrollada constituye el fundamento sobre el que posteriormente se construyen las capas de Recruitment Intelligence y Decision Support System incorporadas en las últimas fases del proyecto.

---

## 🖥️ Evolución hacia un DSS

A partir del Sprint 7 el proyecto evoluciona desde un sistema puramente predictivo hacia una plataforma orientada al consumo de resultados por usuarios de negocio.

El objetivo deja de ser únicamente responder a preguntas analíticas y pasa a centrarse en apoyar procesos reales de scouting y recruitment.

La evolución funcional puede resumirse mediante la siguiente secuencia:

```text id="17ql35"
Predicción
↓
Scoring
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Decision Support System
```

---

### Sprint 7 — Executive Dashboard

Sprint 7 introduce la primera capa de visualización y consumo de resultados analíticos.

Hasta este momento, el proyecto se centraba principalmente en la generación de modelos predictivos y métricas de scouting. Con la incorporación del dashboard, los resultados pasan a estar disponibles mediante una interfaz interactiva orientada a usuarios de negocio.

#### Funcionalidades incorporadas

* Visualización de métricas clave mediante Executive KPIs.
* Ranking interactivo de oportunidades de mercado.
* Exploración dinámica mediante filtros y segmentaciones.
* Acceso individual a perfiles de jugadores.
* Integración de explicaciones analíticas para apoyar la interpretación de resultados.

#### Contribución

El Sprint 7 representa el inicio de la transición desde un proyecto analítico hacia una herramienta de soporte a decisiones orientada a scouting profesional.

---

### Sprint 9 — Decision Support Layer

Sprint 9 representa la transición desde un dashboard descriptivo hacia un sistema DSS (Decision Support System).

#### Objetivo

Reducir la distancia entre:

```text id="x0mmsv"
Predicción
↓
Scoring
↓
Ranking
↓
Decisión deportiva
```

#### Funcionalidades implementadas

##### Executive Scouting Filters

Segmentación dinámica mediante:

* Liga.
* Posición.
* Edad.
* Opportunity Score.
* Confidence Score.

##### Cost vs Upside Matrix

Visualización estratégica para evaluar simultáneamente:

* Coste de adquisición.
* Potencial de revalorización.
* Atractivo de mercado.

##### Shortlisting

Priorización automática de candidatos en función de criterios analíticos configurables.

#### Contribución

Nacimiento de la Decision Support Layer.

---

### Sprint 10 — Player Intelligence Layer

Sprint 10 introduce una nueva capa centrada en la interpretación individual de jugadores y en la incorporación explícita del riesgo dentro del proceso de scouting.

#### Objetivos

* Mejorar la interpretabilidad individual.
* Incorporar benchmarking posicional.
* Formalizar la dimensión riesgo-retorno.
* Separar evaluación histórica y scouting operativo.

---

#### Sprint 10.1 — Player Radar & Positional Benchmarking

##### Player Radar

Visualización multidimensional de rendimiento mediante radares posicionales.

Variables utilizadas:

* Minutos.
* Goles por 90.
* Asistencias por 90.
* G+A por 90.
* Growth Score.
* Confidence Score.

##### Positional Benchmarking

Comparación relativa frente a jugadores de la misma posición.

Permite contextualizar el rendimiento dentro del grupo competitivo relevante.

##### Scouting Narrative

Generación automática de narrativa analítica basada en fortalezas y áreas de mejora.

---

#### Sprint 10.2 — Opportunity Score

Desarrollo de una métrica multicriterio para priorización de oportunidades.

El score combina:

* Mispricing.
* Confidence.
* Performance.
* Edad.
* Valor de mercado.

##### Resultado

Generación de rankings operativos orientados a scouting.

---

#### Sprint 10.3 — Risk Assessment Layer

Incorporación de una dimensión formal de riesgo dentro del sistema.

##### Risk Score

Métrica diseñada para cuantificar la incertidumbre asociada a cada recomendación.

##### Risk Categories

Segmentación automática en:

* Low Risk.
* Medium Risk.
* High Risk.

##### Opportunity vs Risk Matrix

Herramienta visual para evaluar simultáneamente potencial y riesgo.

#### Contribución

Nacimiento de la Player Intelligence Layer y consolidación de la lógica riesgo-retorno dentro del proceso de identificación de oportunidades.

---

### Sprint 11 — Recruitment Intelligence Layer

Sprint 11 transforma el sistema desde una herramienta centrada en rankings hacia una plataforma de análisis comparativo para procesos de recruitment.

#### Objetivo

Reducir el tiempo necesario para evaluar, comparar y priorizar candidatos potenciales.

---

#### Recruitment Board

Nueva sección orientada a procesos reales de scouting.

Permite:

* Selección múltiple de candidatos.
* Construcción dinámica de shortlists.
* Comparación simultánea de jugadores.
* Vista ejecutiva de perfiles filtrados.

---

#### Candidate Selection System

Implementación de un sistema de selección multijugador.

Capacidades:

* Selección simultánea.
* Comparación dinámica.
* Gestión de shortlists temporales.

---

#### Comparative Player Analysis

Comparación directa entre candidatos.

Variables comparadas:

* Opportunity Score.
* Risk Score.
* Confidence Score.
* Market Value.
* Predicted Value.
* Mispricing.

Esta funcionalidad permite evaluar alternativas potenciales dentro de un mismo proceso de captación.

---

#### Executive Scouting Workflow

El flujo metodológico evoluciona desde:

```text id="7l8sqk"
Modelo
↓
Ranking
```

hacia:

```text id="5xll42"
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

---

### UX & Executive Workflow Refinement

El Sprint 11 incorpora una fase adicional de refinamiento orientada a mejorar la experiencia de usuario y la eficiencia operativa del proceso de scouting.

Funcionalidades incorporadas:

* Buscador global de scouting.
* Guía rápida integrada.
* Contexto activo de filtros.
* Mejora de navegación entre módulos.
* Optimización visual del Recruitment Board.
* Simplificación de flujos de comparación.

Contribución:

Reducción de fricción operativa y consolidación del dashboard como herramienta de trabajo para procesos de recruitment.

---

### Sprint 12 — Productization & Internationalization Layer

El Sprint 12 consolida y estandariza las mejoras de experiencia de usuario introducidas durante Sprint 11, ampliándolas mediante una capa de internacionalización y productización orientada a usuarios finales.

#### Objetivos

* Mejorar experiencia de usuario.
* Reducir fricción operativa.
* Incrementar accesibilidad.
* Facilitar adopción internacional.
* Consolidar la plataforma como un sistema DSS orientado a negocio.

---

#### Dashboard Productization

Refactorización de la interfaz para facilitar la interpretación y el consumo de resultados analíticos.

Mejoras incorporadas:

* Diseño orientado a perfiles ejecutivos.
* Navegación estructurada por capas funcionales.
* Jerarquización visual de métricas y recomendaciones.
* Mejora de consistencia visual entre módulos.
* Optimización de flujos de exploración y análisis.

---

#### Global Search Engine

Implementación de un buscador global integrado con capacidad de búsqueda por:

* Jugador.
* Club.
* Liga.
* Posición.

Características:

* Autocompletado.
* Sugerencias dinámicas.
* Filtrado inmediato.
* Integración con el contexto activo del dashboard.

---

#### Executive UX Layer

Incorporación de mejoras orientadas a la eficiencia operativa.

Funcionalidades:

* Guía rápida integrada.
* Chips de filtros activos.
* Contexto de exploración persistente.
* Simplificación de interacciones frecuentes.
* Reducción de clics necesarios para acceder a información relevante.

---

#### Full Internationalization

Dashboard completamente bilingüe.

Idiomas disponibles:

* Español.
* Inglés.

La internacionalización se aplica a:

* Sidebar.
* Métricas.
* Tablas.
* Tooltips.
* Alertas.
* Recruitment Board.
* Transfer Strategy Engine.

---

#### Contribución

La plataforma deja de comportarse como un prototipo analítico y pasa a funcionar como una aplicación DSS orientada a:

* Departamentos de scouting.
* Recruitment teams.
* Directores deportivos.
* Analistas de rendimiento.

Sprint 12 consolida la capa de productización necesaria para transformar resultados analíticos en procesos de decisión utilizables por usuarios de negocio.

---

### Sprint 13A — Multi-League Expansion

Objetivo:

Evaluar la generalización de la metodología a ecosistemas competitivos distintos mediante una ampliación sistemática de cobertura.

Nuevas ligas incorporadas:

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Segunda División de España

Resultados:

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Combinaciones liga-temporada   |     77 |
| Observaciones FBref procesadas | 43.591 |
| Match Rate global              | 75,97% |

Contribución:

* Validación externa de la metodología.
* Expansión multi-liga.
* Auditoría de cobertura.
* Diagnóstico de matching.

---

### Sprint 13A.1 — Coverage Audit & External Validation

Objetivo:

Validar la robustez metodológica del sistema tras la expansión desde siete hasta once ligas europeas.

Funcionalidades incorporadas:

* Coverage Diagnostics.
* Matching by League.
* Matching by League Season.
* Coverage Audit.
* Reentrenamiento completo del pipeline.
* Comparación histórica 7 ligas vs 11 ligas.

Contribución:

* Evaluación explícita de validez externa.
* Auditoría sistemática de cobertura.
* Evidencia empírica de capacidad de generalización.

---

### Sprint 13B — Advanced Data Expansion

Objetivo:

Evaluar el impacto de métricas avanzadas derivadas de FBref sobre la capacidad predictiva de los modelos de valoración de mercado.

#### Variables incorporadas

* finishing_index_v2
* availability_index
* defensive_activity_index

#### Resultados principales

Econometría:

```text id="v6xol6"
R²:
0.4505
→
0.4549

ΔR²:
+0.0044
```

Machine Learning:

```text id="0lztjr"
XGBoost:
+0.0096

HistGradientBoosting:
+0.0144

Random Forest:
+0.0097

LightGBM:
+0.0291
```

#### Hallazgo principal

Todas las arquitecturas mejoran simultáneamente tras incorporar las nuevas variables.

#### Contribución

* Advanced Football Metrics Integration.
* Composite Football Indices v2.
* Advanced Feature Engineering.
* Validación transversal multi-modelo.
* Promoción de nuevas variables productivas.
* Fortalecimiento de la capacidad explicativa del sistema.

#### Resultado metodológico

La hipótesis de Sprint 13B queda validada.

Las métricas avanzadas derivadas de FBref aportan señal predictiva incremental consistente tanto en econometría como en Machine Learning.

Las variables:

* finishing_index_v2
* availability_index
* defensive_activity_index

pasan a formar parte del conjunto oficial de features productivas de la plataforma.

#### Limitación documentada

La integración completa entre la nueva capa de modelización y el pipeline histórico de scoring y rankings se documenta como trabajo futuro independiente.

Esta línea queda registrada en backlog como:

```text id="3ggydk"
TM.2 — Scoring & Ranking Integration v13B
```

sin afectar a las conclusiones metodológicas ni a la validación de la hipótesis principal del sprint.

## ⚽ Valor para departamentos deportivos

La plataforma desarrollada permite transformar grandes volúmenes de información futbolística en procesos de decisión accionables.

Aplicaciones potenciales:

* Identificación de jugadores infravalorados.
* Priorización objetiva de targets.
* Construcción de shortlists.
* Comparación de candidatos.
* Reducción del universo de scouting.
* Comparación entre mercados y ligas.
* Detección temprana de talento emergente.
* Evaluación riesgo-retorno de fichajes.
* Apoyo cuantitativo a procesos de recruitment.

La arquitectura propuesta complementa el scouting tradicional mediante evidencia cuantitativa reproducible y explicable.

---

## ✅ Estado actual del proyecto

Actualmente la plataforma incorpora:

* Integración multi-fuente.
* Matching jerárquico.
* Panel longitudinal.
* Econometría aplicada.
* Machine Learning supervisado.
* MLflow.
* Explainable AI.
* Opportunity Score.
* Risk Framework.
* Decision Support Layer.
* Player Intelligence Layer.
* Recruitment Intelligence Layer.
* Internacionalización EN/ES.
* Sistema DSS interactivo.
* Multi-League Expansion.
* League Coverage Diagnostics.
* External Validity Assessment.
* Advanced Football Metrics Integration.
* Composite Football Indices v2.
* Advanced Feature Engineering.
* External Validation Layer.
* Coverage Diagnostics.
* Multi-League Coverage Audit.

Modelos oficiales:

```text id="a7f8qt"
Growth OLS v13B

Tuned XGBoost v13B
```

Versión actual:

```text id="5wn4h2"
v1.2.1 — Advanced Data Expansion
```

Estado metodológico:

```text id="k5zlrp"
Sprint 13A  → COMPLETADO
Sprint 13B  → COMPLETADO
Sprint 14   → SIGUIENTE FASE
```

---

## ⚠️ Limitaciones

### Limitaciones de datos

* Dependencia de Transfermarkt como fuente de valor de mercado.
* Ausencia de identificador universal entre fuentes.
* Menor cobertura en determinadas ligas secundarias.
* Posibles limitaciones de cobertura en Transfermarkt-Kaggle.

### Limitaciones deportivas

* Ausencia de datos de tracking.
* Cobertura parcial de determinadas métricas avanzadas.
* Dependencia de estadísticas observables.
* Ausencia de información contractual detallada.
* Ausencia de información salarial.

### Limitaciones metodológicas

* Cambios estructurales del mercado de fichajes.
* Posible drift temporal.
* Necesidad de recalibración periódica de modelos.
* Dependencia parcial de variables agregadas construidas a partir de datos observables.

### Limitaciones arquitectónicas identificadas

Durante Sprint 13B se identificó una separación estructural entre:

```text id="k9r0we"
Modeling Pipeline
≠
Scoring Pipeline
```

El pipeline de scoring histórico requiere variables enriquecidas no presentes actualmente en la capa productiva de predicción.

Por este motivo, la integración completa entre:

```text id="gdyf2n"
Predictions v13B
↓
Scoring Dataset v13B
↓
Opportunity Score v13B
↓
Risk Score v13B
↓
Rankings v13B
```

se documenta como trabajo futuro independiente sin impacto sobre la validez de los resultados obtenidos durante Sprint 13B.

---

## 🛣️ Roadmap

Las siguientes líneas de investigación representan extensiones futuras del proyecto y no forman parte de la versión evaluada en este Trabajo Fin de Máster.

Tras la consolidación de la arquitectura DSS y la validación obtenida mediante:

```text id="j7hw22"
Sprint 13A — Multi-League Expansion

Sprint 13B — Advanced Data Expansion
```

las siguientes fases se orientan principalmente a:

* fortalecimiento de capacidades de recruitment;
* optimización estratégica de fichajes;
* integración completa de la capa de scoring;
* mejora de capacidad predictiva;
* ampliación progresiva de cobertura analítica.

---

### TM.1 — Transfermarkt Coverage Audit

Estado:

```text id="j6h1j6"
Backlog
```

Objetivo:

Determinar si las limitaciones de cobertura identificadas durante Sprint 13A proceden principalmente de:

* Transfermarkt-Kaggle.
* Transfermarkt original.
* Pipeline de extracción.
* Disponibilidad histórica de determinadas competiciones.

Resultados esperados:

* Diagnóstico definitivo de cobertura.
* Estimación del techo teórico de matching.
* Identificación de oportunidades de mejora en integración de datos.

---

### TM.2 — Scoring & Ranking Integration v13B

Estado:

```text id="e9g2jv"
Backlog Prioritario
```

Objetivo:

Reconstruir la integración completa entre la nueva capa de modelización v13B y el sistema histórico de scoring.

Flujo objetivo:

```text id="qj8y6u"
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

Justificación:

La integración no afecta a la validación de Sprint 13B pero constituye la evolución natural necesaria para alinear completamente la capa de predicción con la capa DSS.

---

### Sprint 14 — Transfer Strategy Enhancement

Estado:

```text id="sazs7d"
Próxima fase principal
```

Objetivo:

Expandir el sistema desde la identificación de oportunidades individuales hacia la recomendación de estrategias completas de captación.

Pregunta objetivo:

```text id="r97gc9"
¿Qué combinación de jugadores maximiza
el valor esperado bajo restricciones reales
de presupuesto y riesgo?
```

Principales líneas de trabajo:

* Transfer Strategy Engine.
* Portfolio Optimization.
* Scenario Simulation.
* Strategic Recruitment.
* Decision Science aplicada al mercado de fichajes.

Contribución esperada:

Integrar scouting, valoración económica, riesgo y optimización dentro de una misma arquitectura de soporte a decisiones.

---

### Investigación futura

#### Modelización

* Incorporación de TabPFN.
* Incorporación de CatBoost.
* Comparación con modelos fundacionales para datos tabulares.
* Ensemble Learning.

#### Datos

* Nuevas métricas avanzadas FBref.
* Event Data avanzado.
* Tracking Data.
* Información contractual.
* Datos salariales.
* Históricos completos de transferencias.

#### Football Analytics

* Advanced Football Radar.
* Similarity Engine.
* Success Probability Models.
* Career Trajectory Modeling.
* Club Development Intelligence.

#### Sports Economics

* Simulación económica de carteras de fichajes.
* Optimización multiobjetivo.
* Valoración dinámica de activos deportivos.
* Modelización de ROI a largo plazo.

---

### Visión a largo plazo

La evolución natural del proyecto puede resumirse mediante:

```text id="w5b6ii"
Market Value Prediction
↓
Opportunity Detection
↓
Risk Assessment
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
↓
External Validation
↓
Advanced Football Analytics Platform
```

El objetivo final es consolidar una plataforma integral de Football Analytics capaz de combinar valoración económica, análisis deportivo, optimización de fichajes y soporte avanzado a decisiones dentro de entornos profesionales de scouting y recruitment.

---

## 📂 Estructura del proyecto

```bash 
market-value-football-tfm/

├── app/                                   # Aplicación interactiva y capa Decision Support
│   ├── streamlit_app.py                   # Executive Dashboard
│   └── utils/                             # Utilidades específicas del dashboard
│       ├── charts.py                      # Visualizaciones y gráficos interactivos
│       ├── formatters.py                  # Formateo de KPIs, métricas y valores monetarios
│       └── loaders.py                     # Carga de datos y outputs analíticos
│
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
│   ├── 04_supervised_machine_learning.ipynb
│   └── README.md
│
├── reports/                               # Outputs analíticos y reporting
│   ├── business/                          # Métricas de negocio y evaluación de impacto
│   ├── evaluation/                        # Resultados de validación y evaluación de modelos
│   ├── figures/                           # Visualizaciones y figuras exportadas
│   │   ├── dashboard/                     # Capturas del DSS y Scouting Intelligence Platform
│   │   └── explainability/                # SHAP, feature importance y análisis interpretativo
│   ├── model_diagnostics/                 # Diagnósticos econométricos y de Machine Learning
│   ├── portfolio/                         # Outputs del Transfer Strategy Engine
│   │   ├── portfolio_candidates.csv
│   │   ├── portfolio_candidates.parquet
│   │   ├── portfolio_dataset_metadata.json
│   │   ├── portfolio_dataset_summary.csv
│   │   ├── recommended_portfolio.csv
│   │   ├── recommended_portfolio_summary.json
│   │   └── scenarios/
│   │       ├── recommended_portfolio_conservative.csv
│   │       ├── recommended_portfolio_balanced.csv
│   │       ├── recommended_portfolio_aggressive.csv
│   │       ├── recommended_portfolio_conservative_summary.json
│   │       ├── recommended_portfolio_balanced_summary.json
│   │       ├── recommended_portfolio_aggressive_summary.json
│   │       ├── scenario_simulation_summary.csv
│   │       └── scenario_simulation_metadata.json
│   ├── rankings/                          # Rankings de scouting y oportunidades de mercado
│   ├── scouting_reports/                  # Informes individuales de scouting
│   └── tables/                            # Métricas, tablas y resultados exportados
│
├── src/                                   # Lógica principal del sistema
│   ├── data/                              # Ingesta, matching y datasets
│   ├── features/                          # Feature engineering
│   ├── models/
│   │   ├── econometric/                   # Pipeline OLS
│   │   ├── evaluation/                    # Métricas y comparación
│   │   ├── machine_learning/              # Pipelines ML
│   │   └── scoring/                       # Inefficiency scoring
│   ├── strategy/                          # Transfer Strategy Engine
│   │   ├── build_portfolio_dataset.py     # Construcción del universo optimizable
│   │   ├── optimize_transfer_strategy.py  # Optimización 0-1 Knapsack
│   │   └── simulate_transfer_scenarios.py # Simulación de escenarios estratégicos
│   └── utils/                             # Utilidades compartidas
│       ├── config.py                      # Loader centralizado de configuración YAML
│       ├── dataset_versioning.py          # Versionado y hashing de datasets
│       └── experiment_tracking.py         # Integración MLflow
│
├── tests/                                 # Estructura reservada para validaciones automatizadas futuras
│   └── .gitkeep                           # Mantiene la carpeta en Git aunque esté vacía
│
├── .gitignore                             # Reglas de exclusión de Git
├── dataset-metadata.json                  # Metadata versionada del dataset actual
├── environment.yml                        # Entorno Conda
├── PROJECT_STATUS.md                      # Estado operativo del proyecto
├── README.md                              # Documentación principal
├── requirements-lock.txt                  # Dependencias fijadas
└── requirements.txt                       # Dependencias Python
```

---

## 🔁 Reproducibilidad

La reproducibilidad constituye uno de los principios fundamentales del proyecto.

La arquitectura ha sido diseñada para garantizar que cualquier resultado pueda regenerarse a partir de los datos de entrada y de la configuración versionada del sistema.

---

### ▶️ Ejecución reproducible

La ejecución completa del pipeline puede reproducirse siguiendo las etapas descritas a continuación.

---

#### 1️⃣ Construir features FBref

```bash
python -m src.data.build_fbref_features
```

---

#### 2️⃣ Construir features Transfermarkt

```bash
python -m src.data.build_transfermarkt_features
```

---

#### 3️⃣ Construir panel jugador-temporada

```bash
python -m src.data.build_player_season_panel
```

---

#### 4️⃣ Construir dataset modelizable

```bash
python -m src.data.build_modeling_dataset
```

---

#### 5️⃣ Ejecutar pipeline econométrico

```bash
python -m src.models.econometric.run_ols_pipeline
```

---

#### 6️⃣ Ejecutar pipeline Machine Learning

```bash
python -m src.models.machine_learning.run_ml_pipeline
```

---

#### Resultado actual

```text id="u3mdmd"
Predicciones
↓
Inefficiency Detection
↓
Recruitment Intelligence
↓
Decision Support System
```

La integración completa de la capa de scoring permanece documentada como línea de trabajo futura mediante TM.2.

---

## 📚 Referencias

### Fuentes de datos

* FBref
* Transfermarkt

### Frameworks

* Scikit-Learn
* XGBoost
* LightGBM
* SHAP
* MLflow
* Streamlit
* DuckDB
* Pandas
* Statsmodels

### Metodologías

* CRISP-DM (Chapman et al., 2000)
* Explainable AI mediante SHAP (Lundberg & Lee, 2017)

### Literatura académica relacionada

* Müller et al. (2017). Market Value Analysis in European Football.
* Herm et al. (2014). Determinants of Market Values in Professional Football.
* Peeters (2018). Testing Market Inefficiencies in European Football.
* Franck & Nüesch (2012). Talent and Transfer Markets in Football.
* Breiman (2001). Random Forests.
* Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System.

---

## 👨‍🎓 Autoría

Trabajo Fin de Máster

**Market Value Dynamics and Market Inefficiency Detection in Professional Football**

Autores:

* Laura González Macho
* Isabel Muñoz Martín
* Manuel Pérez Bañuls

Tutor:

* Antonio Pita Lozano

---

## 🎯 Impacto potencial

La plataforma desarrollada permite transformar grandes volúmenes de información futbolística en procesos de decisión accionables para departamentos deportivos.

El sistema no pretende sustituir el scouting tradicional, sino complementarlo mediante evidencia cuantitativa reproducible, interpretable y escalable.

La combinación de modelos predictivos, evaluación de ineficiencias, explainability, inteligencia de recruitment y soporte a decisiones permite reducir el universo de análisis inicial y apoyar decisiones estratégicas de captación de talento.

---

## 🏁 Conclusión

El proyecto evoluciona desde un ejercicio de modelización predictiva hacia una plataforma integral de Football Analytics orientada a scouting, recruitment y soporte a decisiones deportivas.

La combinación de:

```text id="4aj3qh"
Econometría
+
Machine Learning
+
Explainable AI
+
Opportunity Detection
+
Risk Assessment
+
Recruitment Intelligence
+
Decision Support System
```

permite transformar datos deportivos en recomendaciones accionables para procesos reales de captación de talento.

La evolución metodológica desarrollada a lo largo del proyecto puede resumirse mediante:

```text id="bc0c5u"
Predicción
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
```

La release v1.2.1 incorpora dos contribuciones metodológicas especialmente relevantes para este Trabajo Fin de Máster.

La primera corresponde a Sprint 13A, donde la expansión desde siete hasta once ligas europeas permitió evaluar explícitamente la capacidad de generalización del sistema en ecosistemas competitivos heterogéneos.

La segunda corresponde a Sprint 13B, donde la incorporación de métricas avanzadas derivadas de FBref permitió demostrar que variables adicionales de rendimiento deportivo aportan capacidad predictiva incremental tanto en econometría como en Machine Learning.

Los resultados obtenidos muestran que:

```text id="rtj9kg"
Sprint 13A
→ mejora la validez externa

Sprint 13B
→ mejora la capacidad explicativa
```

reforzando simultáneamente la solidez metodológica y el valor analítico de la plataforma.

El resultado final es una arquitectura reproducible, interpretable y orientada a negocio que conecta técnicas avanzadas de analítica deportiva con problemas reales de toma de decisiones dentro del fútbol profesional.

La siguiente etapa del proyecto se centrará en Sprint 14 — Transfer Strategy Enhancement, ampliando el sistema desde la identificación de oportunidades hacia la recomendación optimizada de estrategias de fichajes.
