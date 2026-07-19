# 🧪 Data Quality

## Objetivo

Este documento describe la estrategia de calidad de datos implementada en la versión:

```text
v2.0.0 — DSS Architecture, Data Contracts & Productization
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
* capacidad de generalización;
* calidad de nuevas variables avanzadas.

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

La expansión multi-liga ejecutada durante Sprint 13A y la incorporación de métricas avanzadas durante Sprint 13B se desarrollaron bajo este mismo principio.

---

# Objetivos de calidad

Los controles implementados persiguen cinco objetivos principales.

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

Este objetivo adquiere especial relevancia durante Sprint 13A y Sprint 13B.

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

Un modelo puede funcionar correctamente dentro del universo original de entrenamiento pero degradarse al incorporar nuevas competiciones o nuevas variables.

Este riesgo constituye una de las motivaciones principales de Sprint 13A y Sprint 13B.

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
* contexto competitivo;
* métricas avanzadas utilizadas en Sprint 13B.

---

### Cobertura actual

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

La versión actual incorpora:

```text
Sprint 13A
↓
Multi-League Expansion

Sprint 13B
↓
Advanced Data Expansion
```

---

## Dataset final

| Métrica            |                 Valor |
| ------------------ | --------------------: |
| Observaciones      |                 5.527 |
| Jugadores únicos   |               > 2.100 |
| Ligas              |                    11 |
| Temporadas         |                     7 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

---

## Variables avanzadas incorporadas

Sprint 13B añade:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables fueron sometidas a validación específica antes de su promoción a producción.

---

## Estado actual

Dataset productivo:

```text
player_season_modeling_v13b_productive_candidate.parquet
```

Modelos oficiales:

```text
Growth OLS v13B

Tuned XGBoost v13B
```
# 📈 Resultados de validación predictiva

La calidad de un dataset no debe evaluarse únicamente mediante cobertura o volumen de observaciones.

También debe evaluarse mediante su capacidad para generar modelos robustos, estables y generalizables.

---

## Sprint 13A — External Validation

La expansión multi-liga permitió evaluar si el incremento de cobertura mantenía la calidad metodológica del sistema.

### Tuned XGBoost

| Dataset  |     R² |
| -------- | -----: |
| 7 ligas  | 0.5414 |
| 11 ligas | 0.5664 |

---

### Interpretación

La expansión multi-liga:

* incrementa cobertura;
* incrementa diversidad competitiva;
* mejora capacidad predictiva;
* fortalece validez externa.

La evidencia observada sugiere que las nuevas competiciones incorporan señal útil adicional sin deteriorar la calidad del dataset.

---

# 🔬 Sprint 13B — Advanced Features Validation

## Objetivo

Evaluar si las nuevas métricas avanzadas derivadas de FBref mantienen los estándares de calidad exigidos por la arquitectura.

Pregunta metodológica:

```text id="wzpc1h"
¿Las nuevas variables aportan señal útil
o introducen ruido adicional?
```

---

## Variables evaluadas

* finishing_index_v2
* availability_index
* defensive_activity_index

---

## Evaluación econométrica

Comparación principal:

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="a1r5uk"
ΔR² = +0.0044
```

---

### Métricas complementarias

Se observan mejoras simultáneas en:

* MAE;
* RMSE;
* AIC;
* BIC.

---

## Evaluación Machine Learning

Comparación:

```text id="t3n7a7"
Feature Set A (v13A)

vs

Feature Set B (v13B)
```

Resultados:

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

---

## Evidencia de calidad

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento constituye una evidencia especialmente favorable porque:

* reduce la probabilidad de ruido aleatorio;
* reduce el riesgo de sobreajuste;
* aumenta la confianza en la calidad de las variables incorporadas.

---

## Hallazgo principal

Los análisis de importancia muestran que:

```text id="lkxxsk"
finishing_index_v2
```

es la variable avanzada con mayor relevancia predictiva agregada.

---

## Conclusión

Las nuevas variables superan satisfactoriamente los controles de calidad metodológica y son promovidas a producción.

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

Sprint 13A introduce una capa específica orientada a evaluar la robustez metodológica del sistema tras ampliar significativamente la cobertura competitiva.

A diferencia de releases anteriores, esta fase permite medir explícitamente:

* calidad de integración;
* calidad de matching;
* estabilidad predictiva;
* validez externa;
* capacidad de generalización.

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
* reforzar validez externa;
* mejorar capacidad predictiva.

---

# 📊 Coverage Diagnostics

## Objetivo

Medir la calidad efectiva de integración tras la expansión multi-liga.

Durante Sprint 13A se incorporó una capa específica de diagnósticos orientada a cuantificar:

* cobertura efectiva;
* calidad del matching;
* estabilidad temporal;
* diferencias entre ligas;
* impacto sobre modelización.

---

## Artefactos generados

```text id="0l8p3o"
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

## Interpretación

Las principales ligas europeas mantienen niveles elevados de matching.

Las reducciones observadas en determinadas competiciones secundarias se explican principalmente por limitaciones históricas de cobertura en Transfermarkt-Kaggle y no por degradación del algoritmo de matching.

---

# 🔍 Coverage Audit

## Objetivo

Determinar el origen de las pérdidas de matching observadas durante Sprint 13A.

Pregunta principal:

```text id="wb0s1m"
¿Las pérdidas proceden del pipeline
o de limitaciones de las fuentes?
```

---

## Resultado

La evidencia acumulada sugiere que una parte significativa de las pérdidas observadas procede de limitaciones de cobertura en Transfermarkt-Kaggle.

No se identifican evidencias de fallo estructural en:

* FBref;
* Matching Pipeline;
* Feature Engineering Pipeline;
* Panel Construction Pipeline.

---

## Implicación metodológica

La principal restricción observada no corresponde a calidad del pipeline sino a disponibilidad de datos.

Este hallazgo justifica la existencia del backlog:

```text id="ffv3qx"
TM.1 — Transfermarkt Coverage Audit
```

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
| Nuevas variables vs sobreajuste         | Validación multi-modelo   |

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

```text id="i8kjmx"
Valor de mercado
≠
precio real de transferencia
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

## Integración de scoring

Durante Sprint 13B se identificó una separación estructural entre:

```text id="jlwm7r"
Modeling Pipeline
≠
Scoring Pipeline
```

La integración completa queda documentada como:

```text id="ykyr8z"
TM.2 — Scoring & Ranking Integration v13B
```

sin afectar a la validez metodológica de Sprint 13B.

---

# 🗂️ Roadmap histórico de calidad

> TM.2 fue completado y TM.1 quedó parcialmente cubierto por 13A.1. Para las líneas abiertas véase [project_evolution.md](project_evolution.md#roadmap-vigente).

## TM.1 — Transfermarkt Coverage Audit

Objetivo:

* diagnosticar limitaciones de cobertura;
* estimar techo teórico de matching;
* mejorar integración de datos.

---

## TM.2 — Scoring & Ranking Integration v13B — completado

Objetivo:

```text id="r3qz2v"
Predictions v13B
↓
Scoring Dataset v13B
↓
Opportunity Framework v13B
↓
Rankings v13B
```

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

```text id="vgzwz0"
v2.0.0 — DSS Architecture, Data Contracts & Productization
```

incorpora dos contribuciones metodológicas especialmente relevantes.

### Sprint 13A

* expansión a 11 ligas;
* auditoría de cobertura;
* validación externa;
* evaluación explícita de generalización.

### Sprint 13B

* validación de métricas avanzadas;
* integración de nuevas variables productivas;
* mejora simultánea en econometría y Machine Learning;
* fortalecimiento de la robustez metodológica.

Los resultados obtenidos muestran que:

```text id="xn9hhn"
Sprint 13A
→ fortalece la validez externa

Sprint 13B
→ fortalece la calidad explicativa
```

reforzando simultáneamente la solidez de los datos, la calidad de las variables y la confianza en los resultados obtenidos.

La calidad de datos deja de ser únicamente un mecanismo de control interno para convertirse en una evidencia empírica de robustez, generalización y reproducibilidad de la metodología propuesta.

## Controles incorporados en v2.0.0

La calidad se amplía desde la validación del dataset hasta sus consumidores:

- contratos de DataFrame para season, snapshot y presentation;
- auditoría de unicidad y cobertura del Identity Registry;
- comprobación de fechas y procedencia del snapshot;
- validación de que el riesgo no sea sustituido por ceros o fallbacks locales;
- tests de presentación e identidad sobre el universo DSS;
- controles de rendimiento para evitar reconstrucciones repetidas del contexto global;
- compilación de la aplicación y entrypoints de snapshot antes del cierre de release.

Los resultados de 13A/13B siguen siendo evidencia histórica válida; TM.7–TM.8 añaden calidad operativa y de gobernanza sin reestimar los modelos oficiales.
