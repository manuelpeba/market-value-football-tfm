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
Sprint TM.2 — Scoring & Ranking Integration
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

## Sprint TM.2 — Scoring & Ranking Integration

Sprint TM.2 resuelve una inconsistencia metodológica detectada tras la expansión multi-liga.

Aunque los modelos productivos ya operaban sobre un universo de once ligas europeas, parte de la capa DSS seguía utilizando artefactos legacy generados sobre la versión previa de siete ligas.

La intervención permitió restaurar la consistencia completa entre:

```text
Modeling Layer
↓
Scoring Layer
↓
Ranking Engine
↓
Transfer Strategy Engine
↓
Decision Support System
```

Principales resultados:

* Integración completa de las 11 ligas en la capa de scoring.
* Integración completa de las 11 ligas en ranking y opportunity detection.
* Integración completa de las 11 ligas en Transfer Strategy Engine.
* Reintegración automática de variables de crecimiento y confianza durante el pipeline de scoring.
* Eliminación de dependencias operativas heredadas de la arquitectura pre-expansión.

Como resultado, la cobertura competitiva del DSS queda alineada con la cobertura de modelización introducida en Sprint 13A, garantizando consistencia metodológica de extremo a extremo.

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

La incorporación de Transfer Strategy Engine, Portfolio Optimization y la integración multi-liga completa del DSS amplían significativamente la contribución académica y profesional del proyecto.

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

## Cobertura operativa DSS

Tras la finalización de Sprint TM.2, la cobertura competitiva de la capa DSS queda alineada con la cobertura de modelización.

| Componente                 | Cobertura |
| -------------------------- | --------: |
| Modeling Dataset           |  11 ligas |
| Scoring Dataset            |  11 ligas |
| Opportunity Dataset        |  11 ligas |
| Transfer Portfolio Dataset |  11 ligas |
| Decision Support System    |  11 ligas |

Ligas soportadas:

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
* Spanish Segunda División

---

## Modelización

### Modelos oficiales (v1.2.2)

| Capa             | Modelo oficial     |
| ---------------- | ------------------ |
| Econometría      | Growth OLS v13B    |
| Machine Learning | Tuned XGBoost v13B |

---

### Referencias de rendimiento

| Resultado                    |  Valor |
| ---------------------------- | -----: |
| R² OLS productivo (v13B)     | 0.4549 |
| R² XGBoost productivo (v13B) | 0.4453 |
| Mejor R² histórico alcanzado | 0.5664 |

El mejor resultado predictivo obtenido durante el proyecto corresponde a Sprint 13A.1 (External Validation), donde Tuned XGBoost alcanzó:

```text
RMSE = 0.8525
MAE  = 0.6834
R²   = 0.5664
```

La versión productiva actual utiliza el dataset consolidado generado tras Sprint 13B y la integración DSS multi-liga de Sprint TM.2.

Nota metodológica:

Los resultados productivos actuales y los resultados históricos de validación externa corresponden a experimentos distintos y no son directamente comparables, al utilizar datasets y configuraciones experimentales diferentes.


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

Resultado sobre conjunto de test temporal (2024-2025):

| Métrica |  Valor |
| ------- | -----: |
| RMSE    | 0.9639 |
| MAE     | 0.7777 |
| R²      | 0.4453 |

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

### Validación externa multi-liga (Sprint 13A.1)

Como parte de la evaluación de validez externa se realizó una reestimación específica sobre el universo ampliado de once ligas europeas.

Mejor resultado obtenido:

| Modelo        |   RMSE |    MAE |     R² |
| ------------- | -----: | -----: | -----: |
| Tuned XGBoost | 0.8525 | 0.6834 | 0.5664 |

Este experimento constituye la principal evidencia de capacidad de generalización de la metodología desarrollada y representa el mejor resultado predictivo alcanzado durante el proyecto.


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

La capa Opportunity Framework opera actualmente sobre un universo multi-liga de 6.208 observaciones elegibles distribuidas en once competiciones europeas.

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
Sprint TM.2 — COMPLETADO
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

La optimización se resuelve sobre un universo multi-liga de 6.208 jugadores elegibles distribuidos en once competiciones europeas.

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
Sprint TM.2 — COMPLETADO

Release v1.2.2 — ACTIVE
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

La plataforma ha evolucionado desde un sistema de valoración de mercado hacia un entorno completo de apoyo cuantitativo a decisiones deportivas capaz de integrar scouting, recruitment, evaluación de riesgo, optimización estratégica y cobertura multi-liga de extremo a extremo.

# 📚 Estado CRISP-DM

| Fase                    | Estado       |
| ----------------------- | ------------ |
| Business Understanding  | ✅ Completada |
| Data Understanding      | ✅ Completada |
| Data Preparation        | ✅ Completada |
| Modeling                | ✅ Completada |
| Evaluation              | ✅ Completada |
| Deployment              | ✅ Completada |
| DSS Integration         | ✅ Completada |
| Transfer Strategy Layer | ✅ Completada |

El proyecto se encuentra actualmente en una fase avanzada de consolidación metodológica y evolución funcional.

La arquitectura DSS principal se considera cerrada y operativa.

---

# 🎯 Objetivo académico alcanzado

El objetivo original del TFM consistía en desarrollar un sistema capaz de:

```text
Estimar el valor de mercado esperado de futbolistas
e identificar oportunidades de mercado potencialmente
infravaloradas.
```

Este objetivo ha sido alcanzado mediante:

* Modelización econométrica.
* Modelización Machine Learning.
* Opportunity Detection.
* Risk Assessment.
* Recruitment Intelligence.
* Transfer Strategy Engine.
* Portfolio Optimization.

La solución desarrollada supera el alcance inicialmente previsto al incorporar una capa explícita de apoyo a decisiones deportivas basada en optimización matemática.

---

# 🏆 Principales contribuciones del proyecto

## 1. Framework de valoración de mercado

Desarrollo de modelos explicativos y predictivos para estimar el valor de mercado esperado de futbolistas profesionales.

---

## 2. Detección sistemática de ineficiencias

Implementación de un Opportunity Framework basado en:

```text
Valor observado
vs
Valor esperado
```

capaz de identificar activos potencialmente infravalorados.

---

## 3. Integración de métricas avanzadas

Incorporación de nuevas variables derivadas de FBref que mejoran simultáneamente:

* econometría;
* machine learning;
* interpretabilidad del sistema.

Hallazgo principal:

```text
finishing_index_v2
```

como variable avanzada más relevante.

---

## 4. Validación multi-liga

Expansión desde siete hasta once competiciones europeas.

Cobertura final:

* 11 ligas.
* 77 league-seasons.
* 43.591 observaciones procesadas.
* 5.527 observaciones modelables.

La expansión permite evaluar explícitamente la capacidad de generalización del sistema fuera de las cinco grandes ligas.

---

## 5. Consistencia DSS de extremo a extremo

Sprint TM.2 garantiza la propagación completa de la expansión multi-liga a todas las capas operativas.

Cobertura final:

```text
Modeling Layer
↓
Scoring Layer
↓
Opportunity Layer
↓
Ranking Engine
↓
Transfer Strategy Engine
↓
Decision Support System
```

Resultado:

```text
11 ligas integradas de extremo a extremo
```

sin dependencias operativas heredadas de versiones anteriores.

---

## 6. Transfer Strategy Engine

Implementación de una capa de optimización basada en Programación Entera Binaria.

Capacidad:

```text
Seleccionar carteras óptimas de fichajes
bajo restricciones reales de club.
```

Esta contribución amplía significativamente el alcance académico y profesional del proyecto.

---

# 🚀 Roadmap futuro

Las siguientes líneas de trabajo se consideran evoluciones naturales del sistema una vez completada la arquitectura DSS principal.

## Prioridad alta

### Contrato restante

Incorporar información contractual para mejorar la estimación del valor de mercado esperado.

Variables potenciales:

* años restantes de contrato;
* expiración contractual;
* proximidad a free agency.

Impacto esperado:

```text
Alto
```

---

### UEFA Club Coefficient

Incorporar fortaleza competitiva internacional de los clubes.

Variables potenciales:

* coeficiente UEFA;
* participaciones europeas;
* rendimiento continental.

Impacto esperado:

```text
Alto
```

---

### CatBoost

Evaluación comparativa frente al stack actual.

Objetivo:

```text
Validar si existe mejora incremental
respecto a Tuned XGBoost.
```

Impacto esperado:

```text
Medio-Alto
```

---

### TabPFN

Benchmark experimental recomendado durante el programa de máster.

Objetivo:

```text
Comparar arquitecturas fundacionales
para datos tabulares frente a enfoques
de boosting tradicionales.
```

Impacto esperado:

```text
Exploratorio
```

---

## Prioridad media

### Selecciones nacionales

Incorporar experiencia internacional absoluta.

Variables potenciales:

* internacionalidades;
* minutos internacionales;
* torneos disputados.

---

### Participación europea

Medir exposición competitiva a nivel continental.

Variables potenciales:

* Champions League;
* Europa League;
* Conference League.

---

### Club Development Index

Medir la capacidad histórica de desarrollo y revalorización de talento de cada club.

Impacto esperado:

```text
Medio
```

---

## Prioridad baja

### Disponibilidad histórica

Incorporar información retrospectiva de disponibilidad deportiva.

Variables potenciales:

* partidos perdidos;
* disponibilidad histórica;
* continuidad competitiva.

Impacto esperado:

```text
Moderado
```

---

# 🔬 Líneas de investigación futuras

Algunas extensiones exceden el alcance natural del proyecto actual y constituyen líneas de investigación independientes.

## Injury Prediction

Objetivo:

```text
Estimar riesgo futuro de lesión
mediante modelización específica.
```

Posibles fuentes:

* disponibilidad histórica;
* carga competitiva;
* minutos acumulados;
* historial médico.

Esta línea se considera un proyecto complementario independiente y potencialmente una futura capa de Health Intelligence.

---

# 📈 Estado final

```text
Release actual:
v1.2.2
```

Cobertura:

```text
11 ligas
77 league-seasons
43.591 observaciones
5.527 observaciones modelables
```

Arquitectura:

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

Estado global:

```text
Arquitectura DSS completada
Validación multi-liga completada
Transfer Strategy Engine completado
TM.2 completado

Mejor resultado histórico:
R² = 0.5664 (Sprint 13A.1)

Modelo productivo actual:
Tuned XGBoost v13B
R² = 0.4453

Proyecto preparado para defensa académica
y evolución hacia plataforma profesional.
```
