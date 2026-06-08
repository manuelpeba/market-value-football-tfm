# 🧪 Data Quality

## Objetivo

Este documento describe la estrategia de calidad de datos implementada en la versión:

```text
v1.2.0 — Multi-League Expansion
```

Su objetivo es garantizar:

* robustez metodológica;
* reproducibilidad;
* consistencia temporal;
* auditabilidad;
* trazabilidad;
* prevención de leakage;
* calidad de matching;
* validez externa;
* capacidad de generalización.

La calidad de datos constituye uno de los pilares fundamentales de la arquitectura analítica desarrollada y un requisito indispensable para la construcción de sistemas de soporte a decisiones basados en evidencia.

---

# 🧠 Filosofía de calidad

Principio central:

```text
Calidad > Cobertura
```

La arquitectura prioriza:

* precisión del matching;
* coherencia temporal;
* fiabilidad de observaciones;
* robustez estadística;
* consistencia metodológica;
* interpretabilidad de resultados.

frente a maximizar artificialmente el tamaño del dataset.

La expansión multi-liga ejecutada durante Sprint 13A se diseñó bajo este mismo principio, manteniendo estándares de calidad equivalentes a los utilizados en las ligas originales del proyecto.

---

# Objetivos de calidad

Los controles implementados persiguen cuatro objetivos principales.

## 1. Integridad

Garantizar que los registros utilizados sean válidos y consistentes.

---

## 2. Consistencia

Garantizar coherencia entre:

* fuentes;
* temporadas;
* clubes;
* jugadores;
* ligas;
* contextos competitivos.

---

## 3. Trazabilidad

Permitir reconstruir el origen de cualquier observación utilizada durante la modelización.

---

## 4. Reproducibilidad

Garantizar que todos los resultados puedan regenerarse mediante pipelines versionados.

---

## 5. Validez externa

Garantizar que la metodología mantenga su comportamiento al incorporar nuevos ecosistemas competitivos.

Este objetivo adquiere especial relevancia durante Sprint 13A, donde la expansión de cobertura se utiliza como mecanismo explícito de validación metodológica.

---

# 🔍 Riesgos principales

## Matching incorrecto

Problema:

FBref y Transfermarkt no comparten identificador universal.

Riesgos potenciales:

* transliteraciones;
* nombres inconsistentes;
* cambios de club;
* errores ortográficos;
* duplicidades.

---

## Leakage temporal

Problema:

Utilización de información futura durante entrenamiento o scoring.

Posibles consecuencias:

* optimismo artificial;
* sobreestimación del rendimiento;
* pérdida de validez operativa.

---

## Inconsistencias contextuales

Ejemplos:

* posiciones ambiguas;
* ligas distintas;
* temporadas incompletas;
* cambios de nomenclatura.

---

## Datos faltantes

Posibles efectos:

* pérdida de cobertura;
* sesgo muestral;
* menor estabilidad estadística.

---

## Degradación de generalización

Problema:

Un modelo puede funcionar correctamente dentro del universo original de entrenamiento pero degradarse al incorporar nuevas competiciones.

Este riesgo constituye una de las motivaciones principales de Sprint 13A.

---

# 📚 Fuentes auditadas

## FBref

Tipo:

```text
Performance Data Source
```

Información utilizada:

* minutos;
* goles;
* asistencias;
* métricas por 90;
* estadísticas defensivas;
* contexto competitivo.

Cobertura actual:

| Métrica                  |  Valor |
| ------------------------ | -----: |
| Observaciones procesadas | 43.591 |
| Ligas                    |     11 |
| Temporadas               |      7 |
| Liga-temporada           |     77 |

---

## Transfermarkt

Tipo:

```text
Market Valuation Source
```

Información utilizada:

* valor de mercado;
* edad;
* posición;
* club;
* histórico temporal.

La combinación FBref + Transfermarkt constituye la base de toda la arquitectura predictiva.

---

# 🔗 Calidad del Matching Pipeline

## Objetivo

Resolver la integración:

```text
FBref ↔ Transfermarkt
```

manteniendo niveles elevados de precisión.

---

## Filosofía

Principio aplicado:

```text
Perder cobertura antes que aceptar matching dudoso
```

---

## Estrategia implementada

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

---

## Variables utilizadas

* player_name_normalized
* age
* club
* season

---

## Tecnología

```text
RapidFuzz
```

---

## Thresholds operativos

```python
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

Estos umbrales fueron definidos para minimizar errores de emparejamiento sin comprometer excesivamente la cobertura disponible.

---

# 🛡️ Controles implementados

## Validación de esquema

Controles:

* columnas obligatorias;
* tipos válidos;
* nombres consistentes;
* claves esperadas.

---

## Validación de negocio

Controles:

* market value positivo;
* edad válida;
* minutos válidos;
* temporada válida;
* posición válida.

---

## Validación temporal

Controles:

* coherencia cronológica;
* orden temporal;
* temporadas válidas.

---

## Validación de matching

Controles:

* diferencia máxima de edad;
* similitud mínima de club;
* threshold fuzzy;
* trazabilidad del método utilizado.

---

# 🚫 Prevención de leakage

## Principio

Toda variable debe existir en el momento real de la decisión.

---

## Leakage controlado

### Temporal Leakage

Uso accidental de información futura.

### Target Leakage

Uso de variables derivadas de la variable objetivo.

### Train-Test Leakage

Contaminación entre conjuntos de entrenamiento y evaluación.

### Scoring Leakage

Uso de información posterior al momento operativo de scouting.

---

## Variables excluidas

* market_value_next_eur
* delta_log_market_value_1y
* predicted_market_value_eur
* inefficiency_score
* opportunity_score
* risk_score
* rankings derivados

Estas variables no participan en la construcción del dataset modelizable.

---

# 📊 Calidad del dataset modelizable

La versión actual incorpora completamente la expansión multi-liga ejecutada durante Sprint 13A.

## Dataset final

| Métrica            |                 Valor |
| ------------------ | --------------------: |
| Observaciones      |                 5.527 |
| Jugadores únicos   |                >2.100 |
| Ligas              |                    11 |
| Temporadas         |                     7 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

El universo modelizable constituye actualmente el mayor dataset utilizado por el proyecto desde su inicio.

---

## Resultados de validación predictiva

La expansión multi-liga permitió evaluar si el incremento de cobertura mantenía la calidad metodológica del sistema.

### Tuned XGBoost

| Dataset  |     R² |
| -------- | -----: |
| 7 ligas  | 0.5414 |
| 11 ligas | 0.5664 |

### Growth OLS Temporal

| Dataset  |     R² |
| -------- | -----: |
| 11 ligas | 0.5496 |

La mejora observada sugiere que la expansión competitiva incorpora señal útil adicional y no introduce deterioro en la calidad del dataset.

---

## Distribución temporal

| Temporada | Observaciones |
| --------- | ------------: |
| 2019-2020 |           537 |
| 2020-2021 |           536 |
| 2021-2022 |           544 |
| 2022-2023 |           542 |
| 2023-2024 |           586 |
| 2024-2025 |           552 |
| 2025-2026 |           811 |

---

## Filtros aplicados

* matching válido;
* edad válida;
* market value disponible;
* minutos mínimos;
* posición válida.

---

# ⏳ Calidad temporal

## Estrategia histórica

Validación temporal estricta:

| Split         | Temporadas            |
| ------------- | --------------------- |
| Train         | 2019-2020 → 2022-2023 |
| Test Temporal | 2023-2024 → 2025-2026 |

---

## Justificación

Esta separación evita:

* fuga temporal;
* optimismo artificial;
* sobreestimación de capacidad predictiva.

Además, aproxima de forma realista el contexto operativo de utilización del sistema.

---

# 🌍 Sprint 13A — Multi-League Quality Layer

## Objetivo

Sprint 13A introduce una nueva capa de control de calidad orientada a evaluar la robustez metodológica del sistema tras ampliar significativamente la cobertura competitiva.

A diferencia de releases anteriores, esta fase permite medir explícitamente:

* calidad de integración;
* calidad de matching;
* estabilidad predictiva;
* validez externa;
* capacidad de generalización.

---

## Cobertura incorporada

Nuevas ligas:

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

---

## Resultado global

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Dataset modelizable            |  5.527 |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Liga-temporada                 |     77 |
| Match Rate global              | 75,97% |

---

## Beneficio metodológico

La expansión multi-liga permite:

* reducir dependencia de ligas principales;
* evaluar generalización del sistema;
* incrementar diversidad competitiva;
* reforzar la validez externa de la metodología;
* mejorar la capacidad predictiva de los modelos.

# 📊 Coverage Diagnostics

## Objetivo

Medir la calidad efectiva de integración tras la expansión multi-liga.

Durante Sprint 13A se incorporó una capa específica de diagnósticos de cobertura orientada a cuantificar:

* cobertura efectiva;
* calidad del matching;
* estabilidad temporal;
* diferencias entre ligas;
* impacto sobre la modelización.

---

## Artefactos generados

```text
reports/data_quality/

sprint_13a_matching_by_league.csv
sprint_13a_matching_by_league_season.csv
sprint_13a_coverage_summary.md
```

Estos artefactos permiten auditar la cobertura alcanzada por cada competición y cada temporada de forma completamente reproducible.

---

## Match Rate global

| Métrica           |  Valor |
| ----------------- | -----: |
| Match Rate global | 75,97% |

---

## Match Rate por liga

| Liga                     | Match Rate |
| ------------------------ | ---------: |
| Bundesliga               |     92,75% |
| Premier League           |     92,62% |
| Serie A                  |     91,10% |
| Eredivisie               |     89,95% |
| Ligue 1                  |     89,70% |
| LaLiga                   |     84,26% |
| Belgian Pro League       |     79,68% |
| Liga Portugal            |     75,10% |
| Austrian Bundesliga      |     56,00% |
| Championship             |     50,36% |
| Spanish Segunda División |     43,03% |

---

## Interpretación

Las principales ligas europeas mantienen niveles elevados de matching, generalmente superiores al 84%.

Las reducciones observadas en determinadas competiciones secundarias se concentran principalmente en contextos donde la cobertura histórica disponible en Transfermarkt-Kaggle es limitada.

Los resultados obtenidos sugieren que la degradación observada en determinadas ligas no procede del algoritmo de matching implementado.

---

## Evidencia indirecta de calidad

La expansión multi-liga genera simultáneamente:

* aumento de cobertura;
* aumento de diversidad competitiva;
* mejora predictiva.

Si el matching incorporase un volumen significativo de errores sistemáticos, cabría esperar un deterioro de los modelos.

Sin embargo:

| Modelo                         |     R² |
| ------------------------------ | -----: |
| Tuned XGBoost (7 ligas)        | 0.5414 |
| Tuned XGBoost (11 ligas)       | 0.5664 |
| Growth OLS Temporal (11 ligas) | 0.5496 |

La mejora simultánea observada constituye evidencia favorable de la calidad del proceso de integración.

---

# 🔍 Coverage Audit

## Objetivo

Determinar el origen de las pérdidas de matching observadas durante Sprint 13A.

Pregunta de investigación:

> ¿Las pérdidas de cobertura proceden del pipeline implementado o de limitaciones inherentes a las fuentes disponibles?

---

## Metodología

Se realizó una auditoría específica sobre observaciones no emparejadas en distintas ligas y temporadas.

El análisis incluyó:

* validación manual de registros;
* comprobación de cobertura histórica;
* análisis temporal;
* inspección de identificadores y nombres.

---

## Caso auditado

### Matt Grimes

Hallazgos:

* FBref contiene temporadas posteriores.
* Transfermarkt-Kaggle detiene la cobertura histórica en determinados periodos.
* El pipeline identifica correctamente el jugador.
* El matching no puede completarse por ausencia de referencia económica equivalente.

---

## Resultado de auditoría

La evidencia acumulada durante Sprint 13A sugiere que una parte significativa de las pérdidas de matching observadas procede de limitaciones de cobertura en Transfermarkt-Kaggle.

No se identifican evidencias de fallo estructural en:

* FBref;
* Matching Pipeline;
* Feature Engineering Pipeline;
* Panel Construction Pipeline.

---

## Implicación metodológica

La principal restricción observada no corresponde a calidad del pipeline sino a disponibilidad de datos.

Este hallazgo justifica la creación del backlog:

```text
TM.1 — Transfermarkt Coverage Audit
```

como futura línea de investigación.

---

# 🏗️ Controles de arquitectura

La calidad del sistema se refuerza mediante una separación explícita de capas analíticas.

| Capa                     | Objetivo             |
| ------------------------ | -------------------- |
| Raw Data                 | Fuente original      |
| Processed Data           | Feature Engineering  |
| Modeling Dataset         | Entrenamiento        |
| Historical Evaluation    | Validación           |
| Current Scouting         | Operación            |
| Player Intelligence      | Benchmarking         |
| Recruitment Intelligence | Selección            |
| Transfer Strategy Engine | Optimización         |
| DSS                      | Soporte a decisiones |

---

## Beneficio principal

Esta arquitectura reduce el riesgo de:

* contaminación analítica;
* reutilización indebida de información futura;
* mezcla de contextos históricos y operativos;
* leakage indirecto.

---

# 🔬 Tracking y auditoría

## MLflow

El proyecto incorpora trazabilidad completa mediante MLflow.

---

### Parámetros

* features utilizadas;
* hiperparámetros;
* configuraciones;
* split temporal;
* versiones de datasets.

---

### Métricas

* MAE;
* RMSE;
* R²;
* métricas de negocio;
* métricas de matching.

---

### Artefactos

* modelos;
* predicciones;
* rankings;
* explainability;
* tablas;
* visualizaciones.

---

## Beneficio principal

MLflow permite reconstruir exactamente qué configuración produjo cada resultado publicado.

Este requisito resulta especialmente relevante en un contexto académico orientado a reproducibilidad científica.

---

# ⚖️ Trade-offs metodológicos

| Trade-off                               | Decisión                  |
| --------------------------------------- | ------------------------- |
| Cobertura vs precisión                  | Priorizar precisión       |
| Matching agresivo vs conservador        | Conservador               |
| Dataset grande vs fiable                | Fiable                    |
| Complejidad vs reproducibilidad         | Reproducibilidad          |
| Cobertura competitiva vs homogeneidad   | Priorizar validez externa |
| Cobertura máxima vs calidad de matching | Priorizar calidad         |

---

# ⚠️ Limitaciones actuales

## Matching residual

Todo proceso de integración multi-fuente sin identificador universal mantiene un riesgo residual de emparejamiento imperfecto.

---

## Cobertura

Las ligas secundarias y determinadas temporadas recientes presentan menor cobertura disponible en Transfermarkt-Kaggle.

---

## Valor de mercado

Transfermarkt incorpora factores no observables directamente en los datos deportivos:

* reputación;
* percepción humana;
* contexto mediático;
* expectativas de mercado.

Por tanto:

```text
Valor de mercado ≠ precio real de transferencia
```

---

## Datos avanzados

Actualmente no se incorporan:

* tracking data;
* salarios;
* contratos;
* datos espaciales;
* event data avanzado.

---

# 🛣️ Roadmap de calidad

## TM.1 — Transfermarkt Coverage Audit

Estado:

```text
Backlog futuro
```

### Objetivo

Determinar si las limitaciones observadas proceden de:

* Transfermarkt-Kaggle;
* Transfermarkt original;
* pipeline de extracción.

---

## Sprint 13B — Advanced Data Expansion

Objetivo:

Incrementar profundidad analítica manteniendo estándares equivalentes de calidad y reproducibilidad.

---

### Nuevas fuentes previstas

#### FBref avanzado

* Shooting
* Passing
* Possession
* Goal & Shot Creation
* Defense
* Playing Time

#### Understat

* xG
* xA
* xGChain
* xGBuildup

---

### Nuevos controles previstos

* consistencia de eventos;
* validación cruzada de métricas;
* auditoría multi-fuente;
* monitorización avanzada de calidad;
* robustness checks.

---

## Mejoras futuras

* monitorización automática;
* alertas de anomalías;
* rolling validation;
* quality dashboards;
* auditorías periódicas de cobertura.

---

# 🏁 Conclusión

La calidad de datos constituye uno de los pilares fundamentales de la arquitectura analítica desarrollada.

La versión:

```text
v1.2.0 — Multi-League Expansion
```

incorpora una capa adicional de control de calidad orientada a evaluar explícitamente la robustez metodológica del sistema fuera del universo competitivo original.

La arquitectura actual integra:

* Matching validado.
* Controles de negocio.
* Validación temporal.
* Prevención de leakage.
* MLflow.
* Coverage Diagnostics.
* Coverage Audit.
* Evaluación de validez externa.
* Auditoría multi-liga.

La principal contribución de Sprint 13A no consiste únicamente en ampliar cobertura.

La evidencia obtenida demuestra que la metodología mantiene e incluso mejora su capacidad predictiva tras incorporar nuevos ecosistemas competitivos.

Los resultados observados:

| Modelo                         |     R² |
| ------------------------------ | -----: |
| Tuned XGBoost (7 ligas)        | 0.5414 |
| Tuned XGBoost (11 ligas)       | 0.5664 |
| Growth OLS Temporal (11 ligas) | 0.5496 |

sugieren que la ampliación competitiva aporta información útil adicional sin comprometer la integridad de los datos ni la estabilidad metodológica.

La calidad de datos deja de ser únicamente un mecanismo de control interno para convertirse en una evidencia empírica de generalización y validez externa del sistema propuesto.

Esta conclusión constituye uno de los principales resultados metodológicos de la versión v1.2.0 y refuerza significativamente la solidez académica del proyecto.
