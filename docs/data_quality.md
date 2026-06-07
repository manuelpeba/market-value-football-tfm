# 🧪 Data Quality

## Objetivo

Este documento describe la estrategia de calidad de datos implementada en la release:

v1.2.0 — Multi-League Expansion

Su objetivo es garantizar:

* robustez metodológica;
* reproducibilidad;
* consistencia temporal;
* auditabilidad;
* trazabilidad;
* prevención de leakage;
* calidad de matching;
* validez externa.

La calidad de datos constituye uno de los pilares fundamentales de la arquitectura analítica desarrollada.

---

# 🧠 Filosofía de calidad

Principio central:

Calidad > Cobertura

La arquitectura prioriza:

* precisión del matching;
* coherencia temporal;
* fiabilidad de observaciones;
* robustez estadística;
* consistencia metodológica.

frente a maximizar artificialmente el tamaño del dataset.

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
* jugadores.

---

## 3. Trazabilidad

Permitir reconstruir el origen de cualquier observación utilizada durante la modelización.

---

## 4. Reproducibilidad

Garantizar que todos los resultados puedan regenerarse mediante pipelines versionados.

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

# 📚 Fuentes auditadas

## FBref

Tipo:

Performance Data Source

Información utilizada:

* minutos;
* goles;
* asistencias;
* métricas por 90;
* estadísticas defensivas;
* contexto competitivo.

---

## Transfermarkt

Tipo:

Market Valuation Source

Información utilizada:

* valor de mercado;
* edad;
* posición;
* club;
* histórico temporal.

---

# 🔗 Calidad del Matching Pipeline

## Objetivo

Resolver la integración:

FBref ↔ Transfermarkt

manteniendo niveles elevados de precisión.

---

## Filosofía

Principio aplicado:

Perder cobertura antes que aceptar matching dudoso.

---

## Estrategia implementada

Normalización
↓
Exact Matching
↓
Club Validation
↓
Fuzzy Matching
↓
Age Validation

---

## Variables utilizadas

* player_name_normalized
* age
* club
* season

---

## Tecnología

RapidFuzz

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

---

### Target Leakage

Uso de variables derivadas de la variable objetivo.

---

### Train-Test Leakage

Contaminación entre conjuntos de entrenamiento y evaluación.

---

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

La fase de modelización continúa centrándose en jugadores jóvenes con potencial de desarrollo y revalorización.

## Dataset final

| Métrica            |                 Valor |
| ------------------ | --------------------: |
| Observaciones      |                 3.916 |
| Jugadores únicos   |                 2.138 |
| Edad               |                 18–23 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

El universo modelizable utilizado por los modelos predictivos mantiene actualmente las siete ligas originales del proyecto.

La expansión multi-liga de Sprint 13A se ha implementado sobre la capa de integración y panelización de datos, constituyendo la base para futuras ampliaciones del universo de modelización.

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
| 2025-2026 |           619 |

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

| Split            | Temporadas            |
| ---------------- | --------------------- |
| Train            | 2019-2020 → 2024-2025 |
| Current Scouting | 2025-2026             |

---

## Justificación

Esta separación evita:

* fuga temporal;
* optimismo artificial;
* sobreestimación de capacidad predictiva.

Además, aproxima de forma más realista el contexto operativo de utilización del sistema.

# 🌍 Sprint 13A — Multi-League Quality Layer

## Objetivo

Sprint 13A introduce una nueva capa de control de calidad orientada a evaluar la robustez de la metodología en ecosistemas competitivos distintos.

A diferencia de releases anteriores, esta fase no modifica:

* modelos predictivos;
* scoring multicriterio;
* explainability;
* dashboard;
* Recruitment Intelligence;
* Transfer Strategy Engine.

Su objetivo principal consiste en evaluar la calidad de integración y la validez externa del sistema tras ampliar significativamente la cobertura competitiva.

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
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Combinaciones liga-temporada   |     77 |

---

## Beneficio metodológico

La expansión multi-liga permite:

* reducir dependencia de ligas principales;
* evaluar generalización del sistema;
* incrementar diversidad competitiva;
* reforzar la validez externa de la metodología.

---

# 📊 Coverage Diagnostics

## Objetivo

Medir calidad efectiva de integración tras la expansión multi-liga.

Durante Sprint 13A se incorporó una capa específica de diagnósticos de cobertura.

---

## Artefactos generados

```text id="7m1n0x"
reports/data_quality/

sprint_13a_matching_by_league.csv
sprint_13a_matching_by_league_season.csv
sprint_13a_coverage_summary.md
```

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

Las principales ligas europeas mantienen niveles elevados de matching.

La reducción del match rate global respecto a versiones anteriores se explica principalmente por la incorporación de competiciones secundarias con menor cobertura histórica disponible en Transfermarkt-Kaggle.

La evidencia disponible no apunta a una degradación del algoritmo de matching.

---

# 🔍 Coverage Audit

## Objetivo

Determinar el origen de las pérdidas de matching observadas durante Sprint 13A.

Pregunta de investigación:

> ¿Las pérdidas de cobertura proceden del pipeline implementado o de limitaciones de las fuentes disponibles?

---

## Caso auditado

Matt Grimes

Hallazgos:

* Transfermarkt-Kaggle contiene valoraciones hasta 2023-06-01.
* Última temporada disponible: 2022-2023.
* FBref contiene observaciones posteriores.

---

## Conclusión

La evidencia obtenida durante Sprint 13A sugiere que una parte significativa de las pérdidas de matching observadas en ligas secundarias y temporadas recientes procede de limitaciones de cobertura en Transfermarkt-Kaggle.

No se identifican indicios de fallo estructural en:

* FBref;
* Matching Pipeline;
* Feature Engineering Pipeline.

---

# 🏗️ Controles de arquitectura

La calidad del sistema se refuerza mediante una separación explícita de capas analíticas.

| Capa                     | Objetivo             |
| ------------------------ | -------------------- |
| Raw Data                 | Fuente original      |
| Processed Data           | Features             |
| Modeling Dataset         | Entrenamiento        |
| Historical Evaluation    | Validación           |
| Current Scouting         | Operación            |
| Player Intelligence      | Benchmarking         |
| Recruitment Intelligence | Selección            |
| Transfer Strategy        | Optimización         |
| DSS                      | Soporte a decisiones |

---

## Beneficio

Esta arquitectura reduce el riesgo de:

* contaminación analítica;
* mezcla de contextos;
* reutilización indebida de información futura.

---

# 🔬 Tracking y auditoría

## MLflow

El proyecto incorpora trazabilidad completa mediante MLflow.

---

### Parámetros

* features utilizadas;
* hiperparámetros;
* configuraciones;
* split temporal.

---

### Métricas

* MAE;
* RMSE;
* R²;
* métricas de negocio.

---

### Artefactos

* modelos;
* predicciones;
* rankings;
* explainability;
* visualizaciones.

---

## Beneficio principal

MLflow permite reconstruir exactamente qué configuración produjo cada resultado publicado.

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

Valor de mercado ≠ precio real de transferencia.

---

## Datos avanzados

Actualmente no se incorporan:

* tracking data;
* salarios;
* contratos;
* datos espaciales;
* eventos avanzados.

---

# 🛣️ Roadmap de calidad

## TM.1 — Transfermarkt Coverage Audit

Estado:

Backlog futuro.

---

### Objetivo

Determinar si las limitaciones observadas durante Sprint 13A proceden de:

* Transfermarkt-Kaggle;
* Transfermarkt como fuente original;
* pipeline de extracción.

---

## Sprint 13B — Advanced Data Expansion

Objetivo:

Incrementar profundidad analítica manteniendo estándares de calidad equivalentes.

---

### Nuevas fuentes previstas

#### FBref avanzado

* Shooting
* Passing
* Possession
* Goal & Shot Creation
* Defense

#### Understat

* xG
* xA
* xGChain
* xGBuildup

---

### Nuevos controles previstos

* consistencia de eventos;
* validación cruzada de métricas;
* auditoría de cobertura avanzada;
* monitorización de calidad multi-fuente.

---

## Mejoras futuras

* monitorización automática;
* alertas de anomalías;
* robustness checks;
* rolling validation;
* quality dashboards.

---

# 🏁 Conclusión

La calidad de datos constituye uno de los pilares fundamentales de la arquitectura analítica desarrollada.

La versión:

v1.2.0 — Multi-League Expansion

incorpora una capa adicional de control de calidad orientada a evaluar la robustez metodológica del sistema en múltiples ecosistemas competitivos.

La arquitectura actual integra:

* Matching validado.
* Controles de negocio.
* Validación temporal.
* Prevención de leakage.
* MLflow.
* Coverage Diagnostics.
* Coverage Audit.
* Separación Historical vs Current Scouting.
* Evaluación de validez externa.

La principal contribución de Sprint 13A consiste en demostrar que la metodología mantiene niveles elevados de calidad e integridad incluso tras ampliar la cobertura desde siete hasta once ligas europeas.

La calidad de datos deja de ser únicamente un mecanismo de control interno para convertirse en un elemento central de validación metodológica y generalización del sistema.
