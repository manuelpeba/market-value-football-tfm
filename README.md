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
![Version](https://img.shields.io/badge/version-v1.1.0-blue)

---

## Historial de releases

| Release | Contenido principal |
|----------|----------|
| v0.1.0 | Data Pipeline |
| v0.2.0 | Econometric Baseline |
| v0.3.0 | MLflow |
| v0.4.0 | Machine Learning |
| v0.5.0 | Explainability |
| v0.6.0 | Scoring Engine |
| v0.7.0 | Dashboard |
| v0.8.0 | Dashboard Productizado |
| v1.0.0 | Scouting Intelligence Platform |
| v1.1.0 | Strategic Recruitment & Decision Support System |

---

## 📑 Tabla de contenidos

- [🧠 Resumen ejecutivo](#-resumen-ejecutivo)
- [📌 Resultados clave](#-resultados-clave)
- [🎯 Problema de negocio](#-problema-de-negocio)
- [🎯 Objetivos del proyecto](#-objetivos-del-proyecto)
- [🏆 Contribuciones del proyecto](#-contribuciones-del-proyecto)
- [🏗️ Arquitectura global](#️-arquitectura-global)
- [📚 Metodología](#-metodología)
- [📦 Datos y preparación](#-datos-y-preparación)
- [📈 Modelización](#-modelización)
- [📊 Evaluación y resultados](#-evaluación-y-resultados)
- [🖥️ Evolución hacia un DSS](#️-evolución-hacia-un-dss)
- [⚽ Valor para departamentos deportivos](#-valor-para-departamentos-deportivos)
- [✅ Estado actual del proyecto](#-estado-actual-del-proyecto)
- [⚠️ Limitaciones](#️-limitaciones)
- [🛣️ Roadmap](#️-roadmap)
- [📂 Estructura del proyecto](#-estructura-del-proyecto)
- [🔁 Reproducibilidad](#-reproducibilidad)
- [▶️ Ejecución reproducible](#️-ejecución-reproducible)
- [📚 Referencias](#-referencias)
- [👨‍🎓 Autoría](#-autoría)
- [🏁 Conclusión](#-conclusión)

---

## 🧠 Resumen ejecutivo

Este Trabajo Fin de Máster desarrolla una plataforma integral de Football Analytics orientada a la identificación de jugadores infravalorados en el mercado europeo de fichajes.

El proyecto combina técnicas de:

- Econometría aplicada.
- Machine Learning supervisado.
- Explainable AI.
- Scoring multicriterio.
- Visual Analytics.
- Decision Support Systems.

El objetivo es transformar grandes volúmenes de datos futbolísticos y de mercado en recomendaciones accionables para departamentos de scouting, recruitment y dirección deportiva.

La plataforma desarrollada permite:

- Estimar el valor de mercado esperado de jugadores profesionales.
- Detectar ineficiencias de mercado.
- Identificar oportunidades potenciales de fichaje.
- Cuantificar el riesgo asociado a cada recomendación.
- Construir shortlists de scouting.
- Comparar candidatos de forma simultánea.
- Apoyar procesos de toma de decisiones mediante un sistema DSS interactivo.
- Optimizar carteras de fichajes bajo restricciones de presupuesto y riesgo.
- Simular estrategias de recruitment alternativas mediante escenarios.

La versión actual corresponde a:

```text
v1.1.0 — Strategic Recruitment & Decision Support System
```

y representa la evolución del proyecto desde un sistema predictivo de valoración de jugadores hacia una plataforma integral de soporte a decisiones para scouting profesional.

---

## 📌 Resultados clave

| Indicador | Valor |
|------------|------------:|
| Match Rate FBref ↔ Transfermarkt | 88% |
| Jugadores analizados | 2.136 |
| Observaciones modelables | 3.916 |
| R² modelo productivo (XGBoost) | 0.5414 |
| Precision@10 | 90% |
| Estado actual | DSS para scouting y recruitment |

---

## 🎯 Problema de negocio

La toma de decisiones en el mercado de fichajes se caracteriza por:

- Información incompleta.
- Elevada incertidumbre.
- Recursos limitados.
- Sesgos cognitivos.
- Asimetrías informativas.

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

- Aplicación de CRISP-DM al ámbito del fútbol profesional.
- Integración de econometría y Machine Learning dentro de un mismo marco metodológico.
- Validación temporal estricta para aproximar escenarios reales de uso.
- Evaluación orientada a negocio mediante métricas de scouting.
- Estudio aplicado de ineficiencias de mercado en fútbol europeo.

### Contribuciones técnicas

- Matching multi-fuente FBref ↔ Transfermarkt.
- Arquitectura modular reproducible.
- Experiment tracking mediante MLflow.
- Explainability basada en SHAP.
- Opportunity Score.
- Risk Framework.
- Decision Support System interactivo.

### Contribuciones de negocio

- Opportunity Detection.
- Risk Assessment.
- Recruitment Intelligence.
- Candidate Comparison.
- Recruitment Board.
- Transfer Strategy Engine.
- Portfolio Optimization.
- Decision Support System.

---

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
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Decision Support System
```

Esta evolución refleja la transición desde una investigación centrada exclusivamente en predicción de valor de mercado hacia una plataforma orientada a la toma de decisiones deportivas.

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

- Minutos disputados.
- Goles.
- Asistencias.
- Producción ofensiva.
- Acciones defensivas.
- Progresión y posesión.
- Indicadores avanzados normalizados por 90 minutos.

---

#### Transfermarkt

Fuente principal de información de mercado.

Variables utilizadas:

- Valor de mercado.
- Edad.
- Posición.
- Club.
- Histórico de valor.
- Contexto competitivo.

---

### Cobertura geográfica

La versión actual incorpora siete ligas europeas:

- Premier League
- LaLiga
- Bundesliga
- Serie A
- Ligue 1
- Eredivisie
- Liga Portugal

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

| Métrica | Valor |
|----------|----------:|
| Observaciones integradas | 24.194 |
| Observaciones emparejadas | 21.245 |
| Match Rate | 88% |

La calidad del matching constituye una de las principales contribuciones técnicas del proyecto, ya que permite construir el panel longitudinal utilizado durante toda la investigación.

---

## 📊 Dataset final

Tras los procesos de integración, validación y preparación se construye un panel longitudinal jugador-temporada.

### Panel completo

| Métrica | Valor |
|----------|----------:|
| Observaciones | 24.194 |
| Temporadas | 2019-2020 → 2025-2026 |
| Ligas | 7 |

### Dataset modelizable

La fase de modelización se centra en jugadores jóvenes con potencial de desarrollo y revalorización.

| Métrica | Valor |
|----------|----------:|
| Observaciones | 3.916 |
| Jugadores únicos | 2.136 |
| Rango de edad | 18–23 |

---

## ⚙️ Feature Engineering

El proyecto incorpora múltiples capas de transformación orientadas a capturar rendimiento, experiencia y evolución temporal.

### Variables de crecimiento

Diseñadas para modelar la trayectoria reciente del jugador.

Ejemplos:

- market_value_growth_prev
- delta_log_market_value_prev
- breakout_indicator
- career_year

### Composite Football Indices

Indicadores sintéticos construidos para representar dimensiones futbolísticas complejas.

Ejemplos:

- finishing_index
- playmaking_index
- experience_index
- growth_index

### Transformaciones aplicadas

- Transformaciones logarítmicas.
- Escalado robusto.
- Winsorización.
- Estandarización.

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
Growth OLS
```

Variables utilizadas:

- Edad.
- Experiencia.
- Rendimiento deportivo.
- Variables de crecimiento.
- Indicadores compuestos.

#### Resultados

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Growth OLS | 0.7287 | 0.9053 | 0.5258 |

El modelo explica aproximadamente el 52.6% de la variabilidad observada en los valores de mercado.

---

### Machine Learning

Tras establecer el benchmark econométrico se desarrolla una segunda capa basada en Machine Learning supervisado.

#### Algoritmos evaluados

- Random Forest
- HistGradientBoosting
- LightGBM
- XGBoost

Todos los modelos fueron optimizados mediante búsqueda sistemática de hiperparámetros.

#### Modelo productivo

Tras la evaluación comparativa se selecciona:

```text
Tuned XGBoost
```

como modelo operativo de la plataforma.

#### Resultados

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Tuned XGBoost | 0.7120 | 0.8892 | 0.5414 |

#### Decisión metodológica

```text
Growth OLS
=
Benchmark interpretable

Tuned XGBoost
=
Modelo productivo
```

Esta separación combina rigor académico, interpretabilidad y capacidad predictiva.

---

## 🔬 Experiment Tracking con MLflow

El proyecto incorpora una capa completa de trazabilidad experimental mediante MLflow.

### Información registrada

#### Parámetros

- Hiperparámetros.
- Configuraciones.
- Seeds.

#### Métricas

- MAE.
- RMSE.
- R².
- Métricas de negocio.

#### Artefactos

- Modelos serializados.
- Gráficos.
- Tablas.
- Datasets.

MLflow permite reconstruir completamente cualquier experimento ejecutado durante el desarrollo del proyecto.

---

## 🔍 Explainability

La plataforma incorpora Explainable AI mediante SHAP para reducir la opacidad del modelo productivo.

### Explainability global

Permite responder a la pregunta:

> ¿Qué variables son más importantes para el modelo?

Outputs generados:

- Feature Importance.
- SHAP Importance.
- Summary Plot.

### Explainability local

Permite responder a la pregunta:

> ¿Por qué el modelo estima un valor determinado para este jugador?

Outputs generados:

- Drivers positivos.
- Drivers negativos.
- Explicación individual.

La interpretabilidad constituye un elemento fundamental para facilitar la adopción de modelos analíticos dentro de entornos profesionales de scouting.

---

## 📊 Evaluación y resultados

La evaluación se realiza mediante validación temporal estricta para aproximar escenarios reales de utilización en scouting profesional.

### Esquema temporal

```text
Train:
2019-2020 → 2024-2025

Current Scouting:
2025-2026
```

La temporada 2025-2026 queda reservada para explotación operativa y no participa en el entrenamiento de modelos.

---

### Evaluación técnica

| Modelo | MAE | RMSE | R² |
|----------|----------:|----------:|----------:|
| Growth OLS | 0.7287 | 0.9053 | 0.5258 |
| Tuned XGBoost | 0.7120 | 0.8892 | 0.5414 |

Los resultados muestran una mejora consistente del modelo de Machine Learning respecto al benchmark econométrico.

---

### Evaluación de negocio

La utilidad práctica del sistema se evalúa mediante métricas orientadas a scouting.

#### Precision@K

| K | Precision@K |
|----------:|----------:|
| 10 | 0.90 |
| 20 | 0.90 |
| 50 | 0.90 |
| 100 | 0.85 |

Estas métricas permiten evaluar la capacidad real del sistema para priorizar oportunidades de mercado relevantes.

---

### Conclusiones analíticas

Los resultados obtenidos muestran que:

- El matching multi-fuente alcanza niveles elevados de calidad.
- El modelo XGBoost supera consistentemente al benchmark econométrico.
- Las métricas de negocio validan la utilidad operativa del sistema.
- La combinación de predicción, scoring y explainability permite construir recomendaciones reproducibles para procesos de scouting profesional.

La base analítica desarrollada constituye el fundamento sobre el que posteriormente se construyen las capas de Recruitment Intelligence y Decision Support System incorporadas en las últimas fases del proyecto.

---

## 🖥️ Evolución hacia un DSS

A partir del Sprint 7 el proyecto evoluciona desde un sistema puramente predictivo hacia una plataforma orientada al consumo de resultados por usuarios de negocio.

El objetivo deja de ser únicamente responder a preguntas analíticas y pasa a centrarse en apoyar procesos reales de scouting y recruitment.

La evolución funcional puede resumirse mediante la siguiente secuencia:

```text
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

- Visualización de métricas clave mediante Executive KPIs.
- Ranking interactivo de oportunidades de mercado.
- Exploración dinámica mediante filtros y segmentaciones.
- Acceso individual a perfiles de jugadores.
- Integración de explicaciones analíticas para apoyar la interpretación de resultados.

#### Contribución

El Sprint 7 representa el inicio de la transición desde un proyecto analítico hacia una herramienta de soporte a decisiones orientada a scouting profesional.

---

### Sprint 9 — Decision Support Layer

Sprint 9 representa la transición desde un dashboard descriptivo hacia un sistema DSS (Decision Support System).

#### Objetivo

Reducir la distancia entre:

```text
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

- Liga.
- Posición.
- Edad.
- Opportunity Score.
- Confidence Score.

##### Cost vs Upside Matrix

Visualización estratégica para evaluar simultáneamente:

- Coste de adquisición.
- Potencial de revalorización.
- Atractivo de mercado.

##### Shortlisting

Priorización automática de candidatos en función de criterios analíticos configurables.

#### Contribución

Nacimiento de la Decision Support Layer.

---

### Sprint 10 — Player Intelligence Layer

Sprint 10 introduce una nueva capa centrada en la interpretación individual de jugadores y en la incorporación explícita del riesgo dentro del proceso de scouting.

#### Objetivos

- Mejorar la interpretabilidad individual.
- Incorporar benchmarking posicional.
- Formalizar la dimensión riesgo-retorno.
- Separar evaluación histórica y scouting operativo.

---

#### Sprint 10.1 — Player Radar & Positional Benchmarking

##### Player Radar

Visualización multidimensional de rendimiento mediante radares posicionales.

Variables utilizadas:

- Minutos.
- Goles por 90.
- Asistencias por 90.
- G+A por 90.
- Growth Score.
- Confidence Score.

##### Positional Benchmarking

Comparación relativa frente a jugadores de la misma posición.

Permite contextualizar el rendimiento dentro del grupo competitivo relevante.

##### Scouting Narrative

Generación automática de narrativa analítica basada en fortalezas y áreas de mejora.

---

#### Sprint 10.2 — Opportunity Score

Desarrollo de una métrica multicriterio para priorización de oportunidades.

El score combina:

- Mispricing.
- Confidence.
- Performance.
- Edad.
- Valor de mercado.

##### Resultado

Generación de rankings operativos orientados a scouting.

---

#### Sprint 10.3 — Risk Assessment Layer

Incorporación de una dimensión formal de riesgo dentro del sistema.

##### Risk Score

Métrica diseñada para cuantificar la incertidumbre asociada a cada recomendación.

##### Risk Categories

Segmentación automática en:

- Low Risk.
- Medium Risk.
- High Risk.

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

- Selección múltiple de candidatos.
- Construcción dinámica de shortlists.
- Comparación simultánea de jugadores.
- Vista ejecutiva de perfiles filtrados.

---

#### Candidate Selection System

Implementación de un sistema de selección multijugador.

Capacidades:

- Selección simultánea.
- Comparación dinámica.
- Gestión de shortlists temporales.

---

#### Comparative Player Analysis

Comparación directa entre candidatos.

Variables comparadas:

- Opportunity Score.
- Risk Score.
- Confidence Score.
- Market Value.
- Predicted Value.
- Mispricing.

Esta funcionalidad permite evaluar alternativas potenciales dentro de un mismo proceso de captación.

---

#### Executive Scouting Workflow

El flujo metodológico evoluciona desde:

```text
Modelo
↓
Ranking
```

hacia:

```text
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

### UX & Executive Workflow Refinement

El Sprint 11 incorpora una fase adicional de refinamiento orientada a mejorar la experiencia de usuario y la eficiencia operativa del proceso de scouting.

Funcionalidades incorporadas:

- Buscador global de scouting.
- Guía rápida integrada.
- Contexto activo de filtros.
- Mejora de navegación entre módulos.
- Optimización visual del Recruitment Board.
- Simplificación de flujos de comparación.

Contribución:

Reducción de fricción operativa y consolidación del dashboard como herramienta de trabajo para procesos de recruitment.

---

### Sprint 12 — Productization & Internationalization Layer

El Sprint 12 consolida y estandariza las mejoras de experiencia de usuario introducidas durante Sprint 11, ampliándolas mediante una capa de internacionalización y productización orientada a usuarios finales.

#### Objetivos

- Mejorar experiencia de usuario.
- Reducir fricción operativa.
- Incrementar accesibilidad.
- Facilitar adopción internacional.
- Consolidar la plataforma como un sistema DSS orientado a negocio.

---

#### Dashboard Productization

Refactorización de la interfaz para facilitar la interpretación y el consumo de resultados analíticos.

Mejoras incorporadas:

- Diseño orientado a perfiles ejecutivos.
- Navegación estructurada por capas funcionales.
- Jerarquización visual de métricas y recomendaciones.
- Mejora de consistencia visual entre módulos.
- Optimización de flujos de exploración y análisis.

---

#### Global Search Engine

Implementación de un buscador global integrado con capacidad de búsqueda por:

- Jugador.
- Club.
- Liga.
- Posición.

Características:

- Autocompletado.
- Sugerencias dinámicas.
- Filtrado inmediato.
- Integración con el contexto activo del dashboard.

---

#### Executive UX Layer

Incorporación de mejoras orientadas a la eficiencia operativa.

Funcionalidades:

- Guía rápida integrada.
- Chips de filtros activos.
- Contexto de exploración persistente.
- Simplificación de interacciones frecuentes.
- Reducción de clics necesarios para acceder a información relevante.

---

#### Full Internationalization

Dashboard completamente bilingüe.

Idiomas disponibles:

- Español.
- Inglés.

La internacionalización se aplica a:

- Sidebar.
- Métricas.
- Tablas.
- Tooltips.
- Alertas.
- Recruitment Board.
- Transfer Strategy Engine.

---

#### Contribución

La plataforma deja de comportarse como un prototipo analítico y pasa a funcionar como una aplicación DSS orientada a:

- Departamentos de scouting.
- Recruitment teams.
- Directores deportivos.
- Analistas de rendimiento.

Sprint 12 consolida la capa de productización necesaria para transformar resultados analíticos en procesos de decisión utilizables por usuarios de negocio.

---

### Sprint 14 — Transfer Strategy Engine

Sprint 14 introduce una nueva capa de optimización orientada a apoyar decisiones estratégicas de recruitment.

El objetivo deja de ser únicamente identificar oportunidades individuales para responder a una pregunta más cercana a la realidad operativa de un club profesional:

```text
¿Qué combinación de jugadores maximiza el valor esperado
bajo restricciones reales de presupuesto y riesgo?
```

Esta evolución desplaza el proyecto desde el scouting analítico hacia ámbitos propios de Decision Science, Portfolio Optimization y Sports Economics.

---

#### Sprint 14.1 — Portfolio Dataset

Construcción de una capa específica de candidatos para optimización.

Variables incorporadas:

* Portfolio Cost.
* Future Asset Score.
* ROI Score.
* Executive Decision Score.
* Portfolio Scores por perfil de riesgo.

Esta capa transforma las recomendaciones individuales en activos comparables dentro de un proceso de optimización.

---

#### Sprint 14.2 — Optimization Engine

Implementación de un motor de optimización basado en programación lineal entera.

Formulación utilizada:

```text
0-1 Knapsack Optimization
```

Implementación:

```text
PuLP
```

Restricciones incorporadas:

* Presupuesto disponible.
* Posiciones requeridas.
* Número máximo de fichajes.

La función objetivo maximiza un score de cartera ajustado al perfil estratégico seleccionado.

---

#### Sprint 14.3 — Scenario Simulator

Desarrollo de un simulador de escenarios orientado a comparar estrategias alternativas de recruitment.

Escenarios disponibles:

* Conservative.
* Balanced.
* Aggressive.

Cada escenario modifica la ponderación entre:

* Opportunity.
* Risk.
* Confidence.
* Future Asset.
* ROI.

permitiendo analizar diferentes perfiles de inversión deportiva.

---

#### Sprint 14.4 — Strategic Recruitment Engine

Integración completa dentro del dashboard DSS.

Funcionalidades incorporadas:

* Optimización interactiva de carteras.
* Configuración de presupuesto.
* Selección de posiciones objetivo.
* Configuración de perfil de riesgo.
* Comparación simultánea de escenarios.
* KPIs ejecutivos de cartera.
* Explicabilidad mediante Selection Rationale.

---

#### Contribución

Sprint 14 representa el mayor salto metodológico del proyecto.

La evolución funcional puede resumirse mediante:

```text
Opportunity Detection
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

La plataforma deja de limitarse a detectar oportunidades para pasar a recomendar estrategias completas de asignación de recursos dentro del mercado de fichajes.

---

## ⚽ Valor para departamentos deportivos

La plataforma desarrollada permite transformar grandes volúmenes de información futbolística en procesos de decisión accionables.

Aplicaciones potenciales:

- Identificación de jugadores infravalorados.
- Priorización objetiva de targets.
- Construcción de shortlists.
- Comparación de candidatos.
- Reducción del universo de scouting.
- Comparación entre mercados y ligas.
- Detección temprana de talento emergente.
- Evaluación riesgo-retorno de fichajes.
- Apoyo cuantitativo a procesos de recruitment.

La arquitectura propuesta complementa el scouting tradicional mediante evidencia cuantitativa reproducible y explicable.

---

## ✅ Estado actual del proyecto

Actualmente la plataforma incorpora:

- Integración multi-fuente.
- Matching jerárquico.
- Panel longitudinal.
- Econometría aplicada.
- Machine Learning supervisado.
- MLflow.
- Explainable AI.
- Opportunity Score.
- Risk Framework.
- Decision Support Layer.
- Player Intelligence Layer.
- Recruitment Intelligence Layer.
- Internacionalización EN/ES.
- Sistema DSS interactivo.
- Transfer Strategy Engine.
- Portfolio Optimization Layer.
- Scenario Simulator.
- Strategic Recruitment Engine.
- Portfolio Recommendation Engine.

Versión actual:

```text
v1.1.0 — Strategic Recruitment & Decision Support System
```

---

## ⚠️ Limitaciones

### Limitaciones de datos

- Dependencia de Transfermarkt como fuente de valor de mercado.
- Ausencia de identificador universal entre fuentes.
- Cobertura limitada a siete ligas europeas.

### Limitaciones deportivas

- Ausencia de datos de tracking.
- Cobertura parcial de métricas avanzadas.
- Dependencia de estadísticas observables.

### Limitaciones metodológicas

- Cambios estructurales del mercado de fichajes.
- Posible drift temporal.
- Necesidad de recalibración periódica de modelos.

---

## 🛣️ Roadmap

Las siguientes líneas de investigación representan posibles extensiones futuras y no forman parte de la versión evaluada en este Trabajo Fin de Máster.

### Sprint 13 — Multi-League Expansion

Ampliación progresiva de cobertura hacia ligas de desarrollo y exportación de talento.

Posibles incorporaciones:

* Championship.
* Segunda División española.
* Belgian Pro League.
* Austrian Bundesliga.
* Danish Superliga.

Objetivo:

Incrementar la capacidad de detección de ineficiencias de mercado fuera de las principales ligas europeas.

---

### Sprint 15 — Advanced Recruitment Intelligence

Ampliación de las capacidades de comparación y evaluación de candidatos.

Líneas potenciales:

* Benchmarking avanzado.
* Comparación posicional enriquecida.
* Radar multicriterio ampliado.
* Explicabilidad avanzada de recomendaciones.

---

### Sprint 16 — Transfer Replacement Engine

Sistema orientado a la sustitución inteligente de jugadores.

Objetivos:

* Identificación automática de reemplazos.
* Matching de perfiles deportivos.
* Restricciones presupuestarias.
* Compatibilidad táctica y competitiva.

Pregunta objetivo:

```text
¿Qué jugadores pueden sustituir de forma eficiente
a un activo que abandona el club?
```

---

### Investigación futura

* Incorporación de TabPFN.
* Incorporación de CatBoost.
* Nuevas fuentes de datos deportivas.
* Métricas avanzadas de FBref.
* Tracking data.
* Optimización multiobjetivo.
* Simulación económica de carteras de fichajes.

---

## 📂 Estructura del proyecto

``` bash
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

#### 7️⃣ Ejecutar Scoring Engine

```bash
python -m src.models.scoring.build_inefficiency_score
python -m src.models.scoring.build_growth_score
python -m src.models.scoring.build_confidence_score
python -m src.models.scoring.build_opportunity_score
python -m src.models.scoring.generate_rankings
```

---

#### 8️⃣ Ejecutar capa de evaluación

```bash
python -m src.models.evaluation.build_ranking_diagnostics
python -m src.models.evaluation.build_roi_simulation
python -m src.models.evaluation.build_precision_at_k
```

---

#### Resultado final

La ejecución completa genera:

```text
Predicciones
↓
Scoring
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Dashboard DSS
```

garantizando la reproducibilidad integral de los resultados presentados en este Trabajo Fin de Máster.

---

## 📚 Referencias

### Fuentes de datos

- FBref
- Transfermarkt

### Frameworks

- Scikit-Learn
- XGBoost
- LightGBM
- SHAP
- MLflow
- Streamlit
- DuckDB
- Pandas
- Statsmodels
- PuLP

### Metodologías

- CRISP-DM (Chapman et al., 2000)
- Explainable AI mediante SHAP (Lundberg & Lee, 2017)

### Literatura académica relacionada

- Müller et al. (2017). Market Value Analysis in European Football.
- Herm et al. (2014). Determinants of Market Values in Professional Football.
- Peeters (2018). Testing Market Inefficiencies in European Football.
- Franck & Nüesch (2012). Talent and Transfer Markets in Football.
- Breiman (2001). Random Forests.
- Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System.

---

## 👨‍🎓 Autoría

Trabajo Fin de Máster

**Market Value Dynamics and Market Inefficiency Detection in Professional Football**

Autores:

- Laura González Macho
- Isabel Muñoz Martín
- Manuel Pérez Bañuls

Tutor:

- Antonio Pita Lozano

---

## 🎯 Impacto potencial

La plataforma desarrollada permite transformar grandes volúmenes de información futbolística en procesos de decisión accionables para departamentos deportivos.

El sistema no pretende sustituir el scouting tradicional, sino complementarlo mediante evidencia cuantitativa reproducible, interpretable y escalable.

La combinación de modelos predictivos, scoring multicriterio, evaluación de riesgo, inteligencia de recruitment y optimización de carteras permite reducir el universo de análisis inicial y apoyar decisiones estratégicas de fichajes bajo restricciones reales de mercado.

---

## 🏁 Conclusión

El proyecto evoluciona desde un ejercicio de modelización predictiva hacia una plataforma integral de Football Analytics orientada a scouting, recruitment y soporte a decisiones deportivas.

La combinación de:

```text
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
Transfer Strategy Engine
+
Portfolio Optimization
+
Decision Support System
```

permite transformar datos deportivos en recomendaciones accionables para procesos reales de captación de talento.

La evolución metodológica desarrollada a lo largo del proyecto puede resumirse mediante:

```text
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
Portfolio Optimization
↓
Decision Support System
```

La release:

```text
v1.1.0 — Strategic Recruitment & Decision Support System
```

representa la consolidación del proyecto como una plataforma DSS aplicada al mercado europeo de fichajes.

Más allá de la identificación de jugadores infravalorados, la plataforma permite apoyar decisiones estratégicas de recruitment mediante la combinación de valoración de mercado, evaluación de riesgo, análisis comparativo y optimización de carteras de fichajes bajo restricciones reales.

El resultado final es una arquitectura reproducible, interpretable y orientada a negocio que conecta técnicas avanzadas de analítica deportiva con problemas reales de toma de decisiones dentro del fútbol profesional.

