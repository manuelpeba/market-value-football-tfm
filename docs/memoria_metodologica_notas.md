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

# Sprint 2 — Resultados experimentales

Hipótesis:

La incorporación de variables temporales y de progresión profesional mejora la capacidad predictiva del modelo.

Resultado:

Hipótesis aceptada.

Comparación:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline | 1.0035 | 0.8130 | 0.4160 |
| Growth | 0.9046 | 0.7278 | 0.5255 |

Interpretación:

Las variables relacionadas con crecimiento y trayectoria aportan información complementaria no capturada por el rendimiento instantáneo.

Conclusión:

El mercado incorpora expectativas futuras y señales de progresión profesional.

El proceso CRISP-DM permitió identificar una mejora significativa mediante ingeniería de variables basada en conocimiento del dominio.

---

# Sprint 3 — Resultados experimentales

Hipótesis:

La agregación de métricas futbolísticas en índices compuestos puede mejorar la capacidad predictiva del modelo.

Resultado:

Hipótesis parcialmente aceptada.

Comparación:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Growth OLS + Indices | 0.9046 | 0.7278 | 0.5255 |

Interpretación:

Los índices no aportan señal predictiva adicional.

Sin embargo, proporcionan una representación más interpretable del rendimiento futbolístico.

Conclusión:

La utilidad principal de estos índices se encuentra en la explicabilidad y soporte a decisiones de scouting más que en la mejora del rendimiento estadístico.

---

# Sprint 4 — Resultados experimentales

Hipótesis:

Los modelos no lineales pueden mejorar la predicción del valor de mercado.

Resultado:

Hipótesis rechazada para la versión baseline.

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Random Forest | 1.0481 | 0.8527 | 0.3599 |
| XGBoost | 1.0943 | 0.8801 | 0.3022 |
| LightGBM | 1.1078 | 0.8936 | 0.2848 |

Interpretación:

La mayor complejidad algorítmica no implica necesariamente mejor capacidad predictiva.

---

# Sprint 4B — Improved ML Pipeline

## Hipótesis

La primera iteración de modelos supervisados no superó al modelo econométrico Growth OLS. Sin embargo, dicho resultado podía estar condicionado por una configuración baseline sin ajuste sistemático de hiperparámetros.

La hipótesis del Sprint 4B fue:

```text
Un pipeline de Machine Learning mejorado, con preprocesamiento robusto y tuning controlado, puede capturar relaciones no lineales entre rendimiento, contexto y valor de mercado que el modelo econométrico no representa completamente.
```

---

## Implementación

Se desarrolló el script:

```text
src/models/machine_learning/train_ml_tuned.py
```

El pipeline incorpora:

* validación temporal
* preprocesamiento separado para variables numéricas y categóricas
* imputación de valores faltantes
* escalado de variables numéricas
* codificación one-hot de variables categóricas
* tuning de hiperparámetros
* logging experimental
* exportación de feature importance

---

## Validación temporal

Se mantuvo una estrategia out-of-sample estrictamente temporal:

```text
Train: temporadas < 2023
Test: temporadas >= 2023
```

Esta decisión es especialmente relevante en fútbol, ya que el objetivo real del sistema consiste en generalizar hacia temporadas futuras y no simplemente interpolar jugadores dentro del mismo periodo histórico.

---

## Modelos entrenados

Los modelos evaluados fueron:

* Tuned Random Forest
* Tuned XGBoost
* Tuned LightGBM
* HistGradientBoosting

---

## Tuning

Se utilizó:

```text
RandomizedSearchCV
n_iter = 12
```

La elección de `RandomizedSearchCV` se justifica porque permite explorar distintas configuraciones de hiperparámetros con un coste computacional razonable.

---

## Resultados

| Modelo               |       RMSE |        MAE |         R² |
| -------------------- | ---------: | ---------: | ---------: |
| Growth OLS           |     0.9046 |     0.7278 |     0.5255 |
| Tuned Random Forest  |     0.9076 |     0.7315 |     0.5200 |
| Tuned XGBoost        | **0.8753** | **0.7004** | **0.5536** |
| Tuned LightGBM       |     0.8864 |     0.7162 |     0.5421 |
| HistGradientBoosting |     0.8825 |     0.7118 |     0.5462 |

---

## Resultado principal

El mejor modelo obtenido fue:

```text
Tuned XGBoost
```

con:

```text
RMSE = 0.8753
MAE = 0.7004
R² = 0.5536
```

---

## Interpretación académica

El resultado muestra que, una vez introducido un pipeline de entrenamiento más robusto, los modelos supervisados sí son capaces de superar al benchmark econométrico.

Esto sugiere que el valor de mercado no depende únicamente de relaciones lineales entre edad, minutos y producción ofensiva, sino también de interacciones y no linealidades que pueden ser parcialmente capturadas por modelos de boosting.

No obstante, la mejora es moderada. Por tanto, el resultado no invalida el enfoque econométrico, sino que refuerza una arquitectura híbrida:

* econometría para interpretación y control estructural
* Machine Learning para mejora predictiva
* explainability para traducción a negocio

---

## Interpretación desde scouting

Desde una perspectiva de scouting cuantitativo, el Sprint 4B representa un avance importante porque permite estimar con mayor precisión el valor esperado de mercado.

Una mejor estimación reduce el ruido del Inefficiency Score y mejora la calidad potencial de los rankings de jugadores infravalorados.

Sin embargo, para que el modelo sea utilizable en un contexto profesional, no basta con mejorar la métrica predictiva. Es necesario explicar por qué un jugador aparece como infravalorado.

Por ello, el siguiente sprint debe centrarse en:

* importancia global de variables
* explicación local por jugador
* SHAP values
* análisis de perfiles favorecidos o penalizados por el modelo

---

## Conclusión metodológica

La hipótesis del Sprint 4B queda aceptada.

El pipeline ML mejorado supera al modelo Growth OLS y establece a XGBoost tuned como mejor modelo predictivo actual.

La principal implicación metodológica es que el proyecto pasa de una fase de comparación baseline a una fase de explicabilidad y validación de negocio.

El siguiente paso natural es Sprint 4C:

```text
Explainability + Feature Importance
```

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