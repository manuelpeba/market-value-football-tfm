# Notas metodológicas para memoria TFM

Este documento centraliza decisiones metodológicas, justificaciones técnicas y consideraciones académicas derivadas del desarrollo del proyecto.

No constituye la versión final de la memoria, sino una recopilación estructurada para facilitar la posterior redacción.

---

# 1. Ingeniería de variables: normalización contextual por posición y liga

## Contexto

Las métricas de rendimiento futbolístico presentan distribuciones distintas según:

- posición
- competición
- estilo de juego de la liga

Por ejemplo, un delantero de Eredivisie suele presentar distribuciones ofensivas distintas respecto a un delantero de Premier League o Serie A.

La comparación directa mediante valores absolutos puede introducir sesgos estructurales.

---

## Problema detectado

Utilizar variables ofensivas brutas:

- goals_per90
- assists_per90
- shots_per90

puede generar:

- sobrevaloración de jugadores ofensivos
- diferencias artificiales entre ligas
- menor comparabilidad entre perfiles

---

## Solución implementada

Se implementó un bloque de normalización contextual basado en agrupaciones:

```text
[position_group, league]
```

Las variables se transformaron mediante:

### Z-score contextual

Fórmula:

z=(x−μ)/σ

donde:

- x = valor individual
- μ = media del grupo
- σ = desviación estándar del grupo

Variables generadas:

- goals_per90_pos_z
- assists_per90_pos_z
- shots_per90_pos_z

---

### Percentiles relativos

Variables generadas:

- goals_position_percentile
- assists_position_percentile

Los percentiles permiten interpretar el posicionamiento relativo del jugador dentro de su contexto competitivo.

Ejemplo:

Un percentile 0.90 indica que el jugador supera al 90% de jugadores equivalentes dentro de su grupo.

---

## Objetivos esperados

La incorporación de estas variables persigue:

- reducir sesgo ofensivo
- mejorar comparabilidad
- capturar contexto competitivo
- incrementar señal predictiva
- mejorar rendimiento de OLS y modelos ML

---

# 2. Justificación metodológica

La utilización de normalización contextual responde a prácticas habituales en Sports Analytics y Scouting cuantitativo.

Los departamentos de análisis rara vez comparan estadísticas absolutas entre ligas debido a diferencias estructurales:

- intensidad competitiva
- ritmo de juego
- estilos tácticos
- nivel medio de rivales

La normalización relativa aproxima mejor el proceso real de scouting profesional.

---

# 3. Arquitectura reproducible

La implementación se realizó mediante un pipeline desacoplado:

```text
src/features/build_advanced_features.py
```

Inputs:

```text
data/processed/player_season_modeling.parquet
```

Outputs:

```text
data/processed/player_season_modeling_advanced.parquet
```

Logs:

```text
logs/build_advanced_features.log
```

---

# 4. Trazabilidad experimental

El pipeline incorpora seguimiento mediante MLflow.

Para cada ejecución se registran:

## Parámetros

- input_path
- output_path
- variables utilizadas
- agrupaciones

## Métricas

- número de observaciones
- número de variables
- variables creadas
- tasas de valores faltantes

## Artefactos

- dataset generado
- logs

---

# 5. Resultados obtenidos en Sprint 1

Dataset inicial:

```text
Filas: 3297
Variables: 54
```

Dataset transformado:

```text
Filas: 3297
Variables: 59
```

Variables añadidas:

- goals_per90_pos_z
- assists_per90_pos_z
- shots_per90_pos_z
- goals_position_percentile
- assists_position_percentile

---

## Observaciones

La variable:

```text
shots_per90_pos_z
```

presentó:

```text
missing_rate = 100%
```

La causa no corresponde a un error de implementación sino a la ausencia de la variable original:

```text
shots_per90
```

en el dataset modelizable actual.

Por tanto:

La variable no será incorporada a modelos econométricos ni de Machine Learning hasta disponer de datos válidos.

---

# 6. Riesgos y limitaciones

La normalización por grupos puede presentar limitaciones:

- grupos con pocos jugadores
- distribuciones muy asimétricas
- sensibilidad a outliers

Posibles mejoras futuras:

- winsorization
- robust scaling
- percentiles suavizados
- rolling normalization temporal

---

# Sprint 1 — Resultados experimentales

Hipótesis:

La normalización contextual por posición y liga podría mejorar la capacidad predictiva del modelo.

Resultado:

Hipótesis rechazada.

Comparación:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline | 1.0035 | 0.8130 | 0.4160 |
| Advanced | 1.0065 | 0.8166 | 0.4148 |

Interpretación:

La información adicional generada parece estar parcialmente capturada por los efectos fijos incluidos en el modelo.

Conclusión:

El proceso CRISP-DM permitió validar y descartar una hipótesis de ingeniería de variables sin evidencia de mejora predictiva.

---

# 7. Preguntas esperables en defensa

¿Por qué no comparar métricas absolutas?

Porque distintas ligas presentan distribuciones estructurales diferentes.

---

¿Por qué agrupar por posición y liga?

Porque ambas variables afectan significativamente al comportamiento estadístico del jugador.

---

¿Por qué utilizar z-score?

Porque permite expresar rendimiento relativo respecto a un grupo comparable.

---

¿Por qué percentiles además de z-score?

Porque facilitan interpretación para perfiles no técnicos y scouting.

---

¿Por qué no incluir shots_per90_pos_z?

Porque actualmente la variable base presenta valores faltantes completos.