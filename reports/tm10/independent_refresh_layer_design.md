# TM.10.0-B — Transfermarkt Independent Refresh Layer Design

## Objetivo

Diseñar una capa independiente para actualizar los valores actuales de mercado de Transfermarkt sin depender de Kaggle como mecanismo de actualización operativa.

Esta capa permitirá mantener la frescura del DSS incluso cuando Kaggle presente retrasos, degradación de calidad o regresiones en cobertura temporal.

---

## Contexto

Durante TM.10.0-A se realizó una auditoría comparativa entre la fuente oficial actualmente utilizada por el proyecto y la última actualización disponible de Kaggle.

### Resultado de la auditoría

| Fuente                                   |   Filas | Jugadores | Fecha máxima |
| ---------------------------------------- | ------: | --------: | ------------ |
| transfermarkt_features_v13a.parquet      | 616.377 |    39.361 | 2026-03-30   |
| player_valuations.csv (update_2025_2026) | 507.815 |    31.507 | 2026-02-27   |

### Conclusión

La nueva versión disponible en Kaggle presenta:

* Menor cobertura temporal.
* Menor número de jugadores.
* Menor número de observaciones históricas.
* Pérdida de frescura respecto a la fuente actualmente integrada.

Por tanto:

**Kaggle deja de considerarse una fuente fiable para actualizaciones operativas del DSS.**

---

## Principio Arquitectónico

El sistema queda dividido en dos capas claramente diferenciadas.

### Capa 1 — Histórico Reproducible

Responsabilidad:

* Construcción del panel histórico.
* Econometría.
* Machine Learning.
* Reproducibilidad académica.
* Validación experimental.

Fuente principal:

```text
transfermarkt_features_v13a.parquet
```

Esta capa NO debe modificarse durante las actualizaciones operativas.

---

### Capa 2 — Current Snapshot Operativo

Responsabilidad:

* Actualización de valores actuales.
* Club actual.
* Liga actual.
* Fecha de valoración más reciente.
* Inteligencia operativa del DSS.

Archivo objetivo:

```text
data/processed/transfermarkt_current_snapshot_2026_06.parquet
```

Esta capa puede actualizarse periódicamente sin afectar a los modelos entrenados.

---

## Regla Metodológica

La actualización operativa NO debe:

* Reentrenar modelos.
* Alterar el panel histórico.
* Modificar datasets de entrenamiento.
* Cambiar métricas académicas reportadas en la memoria.

Únicamente debe actualizar:

```text
current_player_snapshot.parquet
global_prospect_universe.csv
contract_intelligence_dataset.csv
transfer_portfolio_dataset.csv
```

---

## Dataset Objetivo

### Archivo

```text
data/processed/transfermarkt_current_snapshot_2026_06.parquet
```

### Campos mínimos requeridos

| Campo                     | Descripción                       |
| ------------------------- | --------------------------------- |
| player_id_tm              | Identificador único Transfermarkt |
| player_name               | Nombre del jugador                |
| current_club              | Club actual                       |
| current_league            | Liga actual                       |
| current_market_value_eur  | Valor actual                      |
| current_valuation_date    | Fecha de valoración               |
| previous_market_value_eur | Valor anterior                    |
| previous_valuation_date   | Fecha valoración anterior         |
| market_value_delta_eur    | Variación absoluta                |
| market_value_delta_pct    | Variación porcentual              |
| source_type               | Tipo de fuente                    |
| snapshot_version          | Versión snapshot                  |
| snapshot_date             | Fecha construcción                |

---

## Fuentes Candidatas

### Opción A — Export estructurado

Ventajas:

* Alta calidad.
* Fácil trazabilidad.
* Reproducible.

Riesgo:

* Dependencia de disponibilidad externa.

---

### Opción B — API no oficial

Ventajas:

* Automatizable.
* Escalable.

Riesgo:

* Posibles cambios de contrato.
* Dependencia de terceros.

---

### Opción C — Snapshot manual validado

Ventajas:

* Muy controlado.
* Adecuado para TFM.

Riesgo:

* Menor automatización.

---

### Opción D — Scraping puntual

Ventajas:

* Máxima independencia.

Riesgo:

* Fragilidad técnica.
* Mantenimiento elevado.
* Riesgo legal superior.

---

## Pipeline Propuesto

### Fase 1 — Acquisition

Entrada:

```text
current_snapshot_raw.csv
```

---

### Fase 2 — Normalization

Objetivos:

* Estandarizar nombres.
* Estandarizar tipos.
* Validar identificadores.

---

### Fase 3 — Validation

Comprobaciones:

* player_id_tm válido.
* market_value positivo.
* fecha válida.
* club válido.

---

### Fase 4 — Duplicate Resolution

Reglas:

* Un registro por player_id_tm.
* Prioridad a valoración más reciente.

---

### Fase 5 — Historical Join

Objetivos:

Recuperar:

```text
previous_market_value_eur
previous_valuation_date
```

a partir del histórico existente.

---

### Fase 6 — Dynamics Calculation

Calcular:

```text
market_value_delta_eur
market_value_delta_pct
```

---

### Fase 7 — Health Check

Generar:

```text
snapshot_health_report.json
```

---

### Fase 8 — Overlay

Actualizar:

```text
current_player_snapshot.parquet
global_prospect_universe.csv
contract_intelligence_dataset.csv
transfer_portfolio_dataset.csv
```

---

## Controles de Calidad

| Control                 |   Objetivo |
| ----------------------- | ---------: |
| Cobertura DSS           |      ≥ 90% |
| Duplicados player_id_tm |          0 |
| Market value nulo       |          0 |
| Fecha máxima snapshot   | Junio 2026 |
| Homónimos críticos      |          0 |
| Freshness               |      GREEN |
| Valores negativos       |          0 |

---

## Estados de Salud

### GREEN

Snapshot válido para producción.

Condiciones:

* Cobertura suficiente.
* Sin errores críticos.
* Actualización reciente.

---

### YELLOW

Snapshot utilizable con limitaciones documentadas.

---

### RED

Snapshot no apto para integración DSS.

---

## Casos de Uso DSS

La nueva capa permitirá incorporar métricas actualmente inexistentes.

### Market Value Momentum

Variación reciente del valor de mercado.

---

### Revaluation Alert

Jugadores con incrementos significativos.

Ejemplo:

```text
+40%
+60%
+120%
```

---

### Devaluation Alert

Jugadores con caídas pronunciadas.

Ejemplo:

```text
-25%
-40%
```

---

### Buy-Low Opportunities

Activos con caída reciente de valoración.

---

### Overheated Assets

Activos que podrían encontrarse sobrevalorados tras una actualización reciente.

---

### Opportunity Score Recalibration

Recalibración automática de oportunidades tras cada actualización de mercado.

---

## Integración con el DSS

La capa de actualización debe ser completamente desacoplada del pipeline de modelado.

```text
Market Value Models
          │
          ▼
Historical Dataset

Transfermarkt Refresh Layer
          │
          ▼
Current Snapshot

Current Snapshot
          │
          ▼
DSS Intelligence Layer
```

---

## Entregables TM.10.0-B

### Documentación

```text
reports/tm10/independent_refresh_layer_design.md
```

### Builder

```text
src/tm10/build_independent_current_snapshot.py
```

### Health Check

```text
src/tm10/run_snapshot_health_check.py
```

### Overlay

```text
src/dss/apply_current_market_value_overlay.py
```

---

## Próximo Sprint

TM.10.0-C — Independent Current Snapshot Builder

Objetivo:

Implementar el constructor de snapshots capaz de generar:

```text
transfermarkt_current_snapshot_YYYY_MM.parquet
```

a partir de cualquier fuente externa normalizada sin depender de Kaggle.
