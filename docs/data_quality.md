# 🧪 Calidad de Datos

## Objetivo

Este documento describe los controles de calidad implementados en la versión v1.0.0 — Scouting Intelligence Platform.

Su objetivo es garantizar:

- robustez metodológica
- reproducibilidad
- consistencia temporal
- auditabilidad
- trazabilidad
- prevención de leakage

---

# Filosofía de calidad

Principio central:

```text
Calidad > Cobertura
```

El sistema prioriza:

- precisión del matching
- coherencia temporal
- fiabilidad de las observaciones
- robustez estadística

frente a maximizar artificialmente el tamaño del dataset.

---

# Fuentes analizadas

## FBref

Información deportiva:

- minutos
- goles
- asistencias
- métricas por 90
- estadísticas defensivas

---

## Transfermarkt

Información económica:

- valor de mercado
- edad
- posición
- club
- histórico temporal

---

# Riesgos principales

## Matching incorrecto

Problema:

```text
FBref y Transfermarkt no comparten identificador universal
```

Riesgos:

- nombres inconsistentes
- transliteraciones
- cambios de club
- errores ortográficos

---

## Leakage temporal

Riesgo:

```text
Utilizar información futura
```

---

## Inconsistencias contextuales

Ejemplos:

- posiciones ambiguas
- ligas distintas
- temporadas incompletas

---

## Datos faltantes

Posibles efectos:

- pérdida de cobertura
- sesgo muestral
- menor estabilidad

---

# Calidad del matching

## Estrategia

Pipeline jerárquico:

```text
Normalización
↓
Matching exacto
↓
Validación por club
↓
Matching fuzzy
↓
Validación por edad
```

---

## Variables utilizadas

- player_name_normalized
- age
- club
- season

---

## Algoritmo

```text
RapidFuzz
```

---

## Thresholds

```python
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

---

# Resultados del matching

## Panel completo

| Métrica | Valor |
|----------|----------:|
| Observaciones panel | 24.194 |
| Observaciones emparejadas | 21.245 |
| Match Rate | ≈ 88% |

---

## Decisión metodológica

Principio:

```text
Perder cobertura antes que aceptar matching dudoso
```

Beneficios:

- menor ruido
- menor contaminación
- menor probabilidad de false positives

---

# Controles implementados

## Validación de esquema

Controles:

- columnas obligatorias
- tipos válidos
- nombres consistentes
- claves esperadas

---

## Validación de negocio

Controles:

- market value positivo
- edad válida
- minutos válidos
- temporada válida
- posición válida

---

## Validación temporal

Controles:

- coherencia cronológica
- orden temporal
- temporadas válidas

---

## Validación de matching

Controles:

- edad máxima permitida
- similitud de club
- threshold fuzzy
- trazabilidad del método

---

# Calidad del dataset modelizable

## Dataset final

| Métrica | Valor |
|----------|----------:|
| Observaciones | 3.916 |
| Jugadores únicos | 2.136 |
| Edad | 18–23 |
| Ligas | 7 |
| Temporadas | 2019-2020 → 2025-2026 |

---

## Distribución temporal

| Temporada | Observaciones |
|----------|----------:|
| 2019-2020 | 537 |
| 2020-2021 | 536 |
| 2021-2022 | 544 |
| 2022-2023 | 542 |
| 2023-2024 | 586 |
| 2024-2025 | 552 |
| 2025-2026 | 619 |

---

## Filtros aplicados

- matching válido
- edad válida
- market value disponible
- minutos mínimos
- posición válida

---

# Sprint 10 — Impacto sobre calidad

Sprint 10 introduce cambios relevantes en gobernanza y validación.

---

## Sprint 10.1

Player Intelligence Layer

Nuevos controles:

- consistencia de percentiles
- validación de benchmarks
- coherencia de radar

---

## Sprint 10.2

FBref Advanced Audit

Tablas auditadas:

- Shooting
- Defense
- Misc
- Playing Time
- Passing
- Possession
- Goal & Shot Creation

Resultado:

```text
Evaluación de viabilidad antes de integración
```

Principio aplicado:

```text
Auditar antes de incorporar
```

---

## Sprint 10.3

Current Scouting Layer

Nueva separación:

```text
Historical Evaluation Layer
≠
Current Scouting Layer
```

Beneficios:

- menor contaminación analítica
- mayor validez externa
- mayor claridad metodológica

---

# Prevención de leakage

## Principio

```text
Toda variable debe existir
en el momento real de la decisión.
```

---

## Variables excluidas

- market_value_next_eur
- delta_log_market_value_1y
- predicted_market_value_eur
- inefficiency_score
- opportunity_score
- risk_score
- rankings derivados

---

## Leakage controlado

- temporal leakage
- target leakage
- train-test leakage
- scoring leakage

---

# Calidad temporal

## Estrategia histórica

Validación temporal:

| Split | Temporadas |
|----------|------------|
| Train | 2019-2020 → 2024-2025 |
| Scouting | 2025-2026 |

---

## Justificación

Se evita:

- optimismo artificial
- fuga temporal
- sobreestimación de capacidad predictiva

---

# Controles de arquitectura

Separación explícita:

| Capa | Objetivo |
|--------|----------|
| Raw Data | Fuente original |
| Processed Data | Features |
| Modeling Dataset | Entrenamiento |
| Historical Evaluation | Validación |
| Current Scouting | Operación |
| Player Intelligence | Benchmarking |
| Dashboard | Consumo ejecutivo |

---

# Tracking y auditoría

## MLflow

Información registrada:

### Parámetros

- features
- hiperparámetros
- split temporal

### Métricas

- RMSE
- MAE
- R²

### Artefactos

- modelos
- predicciones
- rankings
- explainability

---

## Beneficios

MLflow permite:

```text
Reconstruir exactamente
qué configuración produjo cada resultado
```

---

# Trade-offs metodológicos

| Trade-off | Decisión |
|----------|-----------|
| Cobertura vs precisión | Priorizar precisión |
| Matching agresivo vs conservador | Conservador |
| Dataset grande vs fiable | Fiable |
| Complejidad vs reproducibilidad | Reproducibilidad |
| Evaluación histórica vs operación | Separación Sprint 10 |

---

# Limitaciones actuales

## Datos

Pendiente:

- xG
- xA
- salarios
- contratos
- eventos avanzados

---

## Matching

Existe siempre:

```text
riesgo residual de matching imperfecto
```

---

## Mercado

Transfermarkt incorpora:

- subjetividad
- ruido contextual
- factores no observables

---

# Roadmap de calidad

## Sprint 11

Advanced Football Radar

Validación prevista:

- shots_per90
- shots_on_target_per90
- tackles_won_per90
- interceptions_per90
- blocks_per90

---

## Sprint 12

Understat

Nuevos controles:

- xG
- xA
- consistencia de eventos

---

## Futuras mejoras

- monitorización automática
- alertas de anomalías
- robustness checks
- rolling validation

---

# Conclusión

La calidad de datos constituye uno de los pilares fundamentales del proyecto.

La arquitectura actual incorpora:

- matching validado
- controles de negocio
- validación temporal
- prevención de leakage
- MLflow
- auditoría FBref
- separación Historical vs Current Scouting

La principal mejora introducida durante Sprint 10 es la separación explícita entre evaluación histórica y scouting operativo, reforzando la robustez metodológica y la validez de las recomendaciones generadas por la plataforma.
