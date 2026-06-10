# 🧠 Resumen ejecutivo

**Market Value Dynamics and Market Inefficiency Detection in Professional Football** es una plataforma integral de Football Analytics orientada a scouting, recruitment y soporte cuantitativo a la toma de decisiones deportivas.

El objetivo principal del proyecto consiste en identificar ineficiencias de mercado dentro del fútbol profesional mediante la estimación del valor de mercado esperado de jugadores y la detección sistemática de activos potencialmente infravalorados.

La arquitectura desarrollada combina metodologías procedentes de múltiples disciplinas:

* Sports Analytics
* Sports Economics
* Econometría aplicada
* Machine Learning supervisado
* Explainable Artificial Intelligence (XAI)
* Decision Science
* Operations Research
* Portfolio Optimization

La evolución funcional del sistema ha seguido una progresión incremental desde modelos de valoración individuales hasta un entorno completo de apoyo a decisiones deportivas:

```text
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
```

La versión actual incorpora los resultados consolidados de:

```text
Sprint 13A — Multi-League Expansion
Sprint 13A.1 — Coverage Audit & External Validation
Sprint 13B — Advanced Data Expansion
Sprint 14 — Transfer Strategy Engine
Sprint 14.1 — Player Level Layer
```

## Sprint 13A — Multi-League Expansion

Sprint 13A amplió el universo competitivo del proyecto desde siete hasta once ligas europeas, incrementando significativamente la cobertura de observaciones disponibles y permitiendo evaluar explícitamente la capacidad de generalización de la metodología.

Principales resultados:

* 11 ligas europeas integradas.
* 43.591 observaciones FBref procesadas.
* 5.527 observaciones modelables.
* 77 combinaciones liga-temporada.
* Match Rate global del 75,97%.

Esta fase constituyó la primera validación explícita de validez externa del sistema fuera del universo competitivo original.

---

## Sprint 13B — Advanced Data Expansion

Sprint 13B incorporó una nueva capa de métricas avanzadas derivadas de FBref con el objetivo de capturar dimensiones futbolísticas complejas insuficientemente representadas en versiones anteriores.

Variables promovidas a producción:

* finishing_index_v2
* availability_index
* defensive_activity_index

Los resultados obtenidos muestran mejoras consistentes tanto en econometría como en Machine Learning.

Hallazgo principal:

```text
finishing_index_v2
```

se identifica como la variable avanzada con mayor relevancia predictiva agregada.

Este resultado aporta evidencia empírica favorable sobre el valor incremental de métricas avanzadas para la estimación del valor de mercado de futbolistas profesionales.

---

## Sprint 14 — Transfer Strategy Engine

Sprint 14 representa la evolución conceptual más importante del proyecto desde la perspectiva de negocio y soporte a decisiones.

Hasta Sprint 13, el sistema respondía principalmente a la pregunta:

```text
¿Qué jugadores parecen infravalorados?
```

A partir de Sprint 14, el sistema es capaz de responder:

```text
¿Qué combinación de jugadores maximiza el valor esperado bajo restricciones reales de club?
```

Para ello se desarrolla un nuevo motor de optimización basado en Programación Entera Binaria (Binary Integer Programming), capaz de construir carteras óptimas de fichajes considerando simultáneamente:

* presupuesto disponible;
* posiciones necesarias;
* perfil estratégico;
* nivel mínimo de calidad;
* número máximo de incorporaciones;
* restricciones de utilización presupuestaria.

La nueva capa incorpora conceptos procedentes de Operations Research y Portfolio Optimization, ampliando significativamente la contribución académica del proyecto.

---

## Sprint 14.1 — Player Level Layer

Como evolución del Transfer Strategy Engine se incorpora una nueva capa de segmentación de calidad orientada a procesos reales de recruitment.

La plataforma clasifica automáticamente a los jugadores en diferentes niveles competitivos:

* Development Prospect
* Rotation Profile
* First Team Ready
* Key Player Profile
* Elite Target

Esta funcionalidad permite incorporar restricciones explícitas de calidad mínima dentro de los procesos de optimización y mejora la alineación entre recomendaciones analíticas y necesidades deportivas reales de los clubes.

---

## Contribución global del proyecto

La versión actual representa la transición desde un sistema de valoración de mercado hacia una plataforma DSS (Decision Support System) capaz de integrar:

* valoración económica;
* detección de oportunidades;
* evaluación de riesgo;
* scouting cuantitativo;
* recruitment intelligence;
* optimización de carteras de fichajes;
* simulación estratégica.

El resultado es una arquitectura reproducible, interpretable y orientada a negocio que conecta analítica deportiva avanzada con procesos reales de toma de decisiones dentro del fútbol profesional.

# 📊 Estado actual

## Dataset

| Métrica                        |                 Valor |
| ------------------------------ | --------------------: |
| Observaciones FBref procesadas |                43.591 |
| Dataset modelizable final      |                 5.527 |
| Cobertura temporal             | 2019-2020 → 2025-2026 |
| Temporadas                     |                     7 |
| Ligas                          |                    11 |
| Combinaciones liga-temporada   |                    77 |
| Match Rate global              |                75,97% |

---

## Modelización

### Modelos oficiales (v1.2.1)

| Capa             | Modelo oficial     |
| ---------------- | ------------------ |
| Econometría      | Growth OLS v13B    |
| Machine Learning | Tuned XGBoost v13B |

---

### Benchmark econométrico

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

Conclusión:

La incorporación de métricas avanzadas aporta capacidad explicativa incremental dentro de la especificación econométrica sin comprometer la interpretabilidad del modelo.

---

### Modelo Machine Learning productivo

Modelo oficial:

```text
Tuned XGBoost v13B
```

Principales resultados obtenidos durante Sprint 13B:

| Arquitectura         | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

Hallazgo principal:

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables avanzadas, reforzando la robustez metodológica de los resultados.

---

### Variable avanzada más relevante

Los análisis de importancia de variables identifican:

```text
finishing_index_v2
```

como la variable avanzada con mayor relevancia predictiva agregada.

Este resultado constituye el principal hallazgo analítico de Sprint 13B.

---

## Opportunity & Risk Framework

La plataforma incorpora una capa completa de evaluación de oportunidades de mercado basada en la comparación entre valor observado y valor esperado.

Componentes implementados:

* Inefficiency Score
* Growth Score
* Confidence Score
* Opportunity Score
* Risk Score
* Risk-adjusted Opportunity

Esta arquitectura permite priorizar candidatos considerando simultáneamente upside potencial, robustez estadística y nivel de riesgo asociado.

---

## Recruitment Intelligence

La capa de Recruitment Intelligence transforma rankings analíticos en herramientas operativas para departamentos deportivos.

Funcionalidades implementadas:

* Recruitment Board
* Comparative Player Analysis
* Candidate Selection
* Executive Scouting Workflow
* Positional Benchmarking
* Global Search Engine
* Executive Dashboard

---

## Transfer Strategy Engine

### Estado

```text
Sprint 14 — COMPLETADO
Sprint 14.1 — COMPLETADO
```

### Objetivo

Optimizar decisiones de fichaje bajo restricciones reales de club.

Pregunta objetivo:

```text
¿Qué cartera de fichajes maximiza el valor esperado
bajo restricciones deportivas y presupuestarias?
```

---

### Inputs estratégicos

* Budget
* Positions Needed
* Scenario
* Portfolio Style
* Minimum Player Level
* Maximum Signings
* Budget Utilization Constraint

---

### Escenarios implementados

| Escenario    | Objetivo                         |
| ------------ | -------------------------------- |
| Conservative | Prioriza estabilidad y robustez  |
| Balanced     | Equilibrio entre upside y riesgo |
| Aggressive   | Maximización de upside esperado  |

---

### Estilos de cartera

| Estilo                  | Objetivo                                               |
| ----------------------- | ------------------------------------------------------ |
| Value Opportunities     | Maximizar oportunidades de mercado                     |
| Balanced Squad Building | Equilibrio entre concentración y diversificación       |
| Star + Prospects        | Combinación de talento consolidado y desarrollo futuro |

---

### Player Level Layer

Sprint 14.1 incorpora una clasificación jerárquica de calidad deportiva:

| Nivel                | Descripción                          |
| -------------------- | ------------------------------------ |
| Development Prospect | Jugador en desarrollo                |
| Rotation Profile     | Perfil de rotación                   |
| First Team Ready     | Preparado para competir regularmente |
| Key Player Profile   | Jugador diferencial                  |
| Elite Target         | Objetivo estratégico prioritario     |

Esta capa permite incorporar restricciones explícitas de calidad mínima dentro de los procesos de optimización.

---

### Metodología de optimización

El sistema utiliza Programación Entera Binaria (Binary Integer Programming) mediante PuLP para construir carteras óptimas de fichajes.

Restricciones consideradas:

* Presupuesto máximo.
* Utilización mínima del presupuesto.
* Número máximo de incorporaciones.
* Cobertura de posiciones requeridas.
* Nivel mínimo de jugador.
* Restricciones derivadas del estilo de cartera.

La optimización se resuelve en tiempos inferiores a un segundo incluso sobre universos superiores a 600 jugadores elegibles.

---

## Evaluación de negocio

| Métrica       | Valor |
| ------------- | ----: |
| Precision@10  |   90% |
| Precision@20  |   90% |
| Precision@50  |   90% |
| Precision@100 |   85% |

Los resultados continúan respaldando la utilidad operativa del sistema para procesos de scouting, recruitment y construcción de carteras de fichajes.

---

## Estado general del proyecto

```text
Sprint 13A — COMPLETADO
Sprint 13A.1 — COMPLETADO
Sprint 13B — COMPLETADO
Sprint 14 — COMPLETADO
Sprint 14.1 — COMPLETADO

Release v1.2.1 — ACTIVE
```

---

## Estado funcional

```text
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
```

La plataforma ha evolucionado desde un sistema de valoración de mercado hacia un entorno completo de apoyo cuantitativo a decisiones deportivas capaz de integrar scouting, recruitment, evaluación de riesgo y optimización estratégica.

# 📚 Estado CRISP-DM

## Fases completadas

### Business Understanding

* Problema de scouting definido.
* Objetivos de negocio establecidos.
* Marco de ineficiencias de mercado formulado.
* Problema de optimización de fichajes formalizado.
* Restricciones operativas de club modelizadas.

### Data Understanding

* Exploración de fuentes.
* Análisis de calidad.
* Cobertura temporal y competitiva.
* Auditoría multi-liga.
* Evaluación de cobertura por competición.
* Diagnóstico de representatividad del universo analizado.

### Data Preparation

* Matching FBref ↔ Transfermarkt.
* Feature Engineering.
* Construcción del panel longitudinal.
* Control de leakage.
* Expansión multi-liga parametrizada.
* Construcción de métricas avanzadas derivadas de FBref.
* Desarrollo de Composite Football Indices v2.
* Construcción del Portfolio Dataset.

### Modeling

* Econometric Pipeline.
* Machine Learning Pipeline.
* Experiment Tracking.
* Explainability.
* Validación multi-liga.
* Evaluación de métricas avanzadas.
* Comparación Feature Set A vs Feature Set B.
* Transfer Portfolio Optimization.
* Binary Integer Programming.
* Portfolio Construction Engine.

### Evaluation

* Validación temporal.
* Evaluación predictiva.
* Evaluación orientada a negocio.
* Validación externa.
* Evaluación incremental de nuevas variables.
* Comparación transversal multi-modelo.
* Evaluación de escenarios estratégicos.
* Validación de restricciones operativas.

### Deployment

* Dashboard interactivo.
* Recruitment Intelligence.
* Transfer Strategy Engine.
* Portfolio Optimization Layer.
* Decision Support System.
* Modelos productivos v13B.
* Internacionalización EN/ES.

---

## Estado actual

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
```

La metodología ha evolucionado desde un sistema de estimación de valor de mercado hacia una arquitectura DSS completa capaz de integrar predicción, evaluación de oportunidades, análisis de riesgo y optimización estratégica de fichajes.

---

# 🏗️ Arquitectura actual

```text
Raw Sources
↓
Feature Engineering
↓
Advanced Metrics Layer
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

## Componentes implementados

| Componente                    | Estado |
| ----------------------------- | ------ |
| Data Pipelines                | ✅      |
| Matching Pipeline             | ✅      |
| Feature Engineering           | ✅      |
| Advanced Feature Engineering  | ✅      |
| Econometric Pipeline          | ✅      |
| Machine Learning Pipeline     | ✅      |
| MLflow Tracking               | ✅      |
| Explainability                | ✅      |
| Opportunity Score             | ✅      |
| Risk Framework                | ✅      |
| Dashboard DSS                 | ✅      |
| Recruitment Intelligence      | ✅      |
| Internationalization EN/ES    | ✅      |
| Multi-League Expansion        | ✅      |
| External Validity Assessment  | ✅      |
| League Coverage Diagnostics   | ✅      |
| Multi-League Benchmarking     | ✅      |
| Advanced Metrics Integration  | ✅      |
| Composite Football Indices v2 | ✅      |
| Transfer Strategy Engine      | ✅      |
| Portfolio Optimization        | ✅      |
| Scenario Simulation           | ✅      |
| Player Level Layer            | ✅      |

---

# ⚙️ Capacidades implementadas

## Estimación de valor de mercado

La plataforma estima el valor esperado de un jugador utilizando modelos econométricos y algoritmos de Machine Learning entrenados sobre datos históricos procedentes de múltiples competiciones europeas.

La arquitectura combina interpretabilidad econométrica y capacidad predictiva avanzada para capturar los principales determinantes del valor de mercado profesional.

---

## Advanced Football Metrics Layer

Sprint 13B incorpora una nueva capa analítica destinada a capturar dimensiones futbolísticas insuficientemente representadas en versiones anteriores del sistema.

Variables productivas incorporadas:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables amplían la capacidad descriptiva del sistema y fortalecen la señal predictiva disponible para los modelos de valoración.

---

## Opportunity Detection

Identificación automática de jugadores potencialmente infravalorados mediante comparación entre:

```text
Predicted Market Value
vs
Observed Market Value
```

La diferencia entre ambas magnitudes constituye la base del sistema de detección de ineficiencias de mercado.

---

## Risk Assessment

Evaluación del riesgo asociado a cada recomendación mediante:

* Risk Score.
* Risk Category.
* Opportunity vs Risk Matrix.
* Confidence Framework.

Esta capa permite priorizar oportunidades considerando simultáneamente upside potencial y robustez estadística.

---

## Player Intelligence

Transformación de resultados analíticos en información accionable para scouting.

Funcionalidades:

* Player Radar.
* Positional Benchmarking.
* Opportunity Narratives.
* Explainability Layer.
* Comparative Evaluation.

---

## Recruitment Intelligence

Funcionalidades incorporadas durante Sprint 11:

* Recruitment Board.
* Comparative Player Analysis.
* Candidate Selection System.
* Executive Scouting Workflow.
* Global Search Engine.
* Executive UX Layer.

Esta capa transforma rankings analíticos en herramientas operativas para departamentos deportivos.

---

## Transfer Strategy Engine

Sprint 14 incorpora una nueva capa de optimización estratégica orientada a decisiones de fichaje.

Objetivo:

```text
Seleccionar la combinación de jugadores
que maximiza el valor esperado
bajo restricciones reales de club.
```

Inputs principales:

* Budget.
* Positions Needed.
* Scenario.
* Portfolio Style.
* Minimum Player Level.
* Maximum Signings.
* Budget Utilization.

Outputs principales:

* Recommended Portfolio.
* Total Cost.
* Budget Utilization.
* Expected Upside.
* Expected ROI.
* Average Portfolio Score.

---

## Portfolio Optimization

La optimización se implementa mediante Programación Entera Binaria (Binary Integer Programming) utilizando PuLP.

La formulación incorpora:

* restricciones presupuestarias;
* restricciones posicionales;
* restricciones de calidad mínima;
* restricciones de tamaño de cartera;
* restricciones de utilización presupuestaria;
* escenarios estratégicos alternativos.

Esta capa constituye la principal incorporación metodológica de Sprint 14 y representa la transición desde analítica descriptiva hacia Decision Science aplicada al mercado de fichajes.

---

## Decision Support System

La plataforma integra todas las capas anteriores dentro de un entorno único de soporte a decisiones deportivas.

El sistema permite evolucionar desde la identificación de oportunidades individuales hasta la construcción de estrategias completas de captación soportadas por evidencia cuantitativa reproducible.

La incorporación de Portfolio Optimization convierte la plataforma en un DSS capaz de conectar scouting, valoración económica, gestión de riesgo y planificación estratégica de fichajes dentro de una misma arquitectura analítica.
