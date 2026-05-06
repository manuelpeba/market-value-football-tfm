# 📘 Modeling Decisions

---

# 📑 Tabla de contenidos

- [🧠 Objetivo de modelización](#-objetivo-de-modelización)
- [⚙️ Unidad de análisis](#️-unidad-de-análisis)
- [🎯 Variable objetivo](#-variable-objetivo)
- [📊 Justificación de la transformación logarítmica](#-justificación-de-la-transformación-logarítmica)
- [📚 Estrategia metodológica](#-estrategia-metodológica)
- [⏳ Estrategia de validación](#-estrategia-de-validación)
- [🏗️ Diseño econométrico](#️-diseño-econométrico)
- [📈 Efectos fijos](#-efectos-fijos)
- [🛡️ Errores robustos HC3](#️-errores-robustos-hc3)
- [⚠️ Decisiones sobre matching](#️-decisiones-sobre-matching)
- [📊 Selección de variables](#-selección-de-variables)
- [🤖 Decisiones sobre Machine Learning](#-decisiones-sobre-machine-learning)
- [⚖️ Interpretabilidad vs capacidad predictiva](#️-interpretabilidad-vs-capacidad-predictiva)
- [💡 Construcción del Inefficiency Score](#-construcción-del-inefficiency-score)
- [📌 Robustness checks](#-robustness-checks)
- [🚀 Próximas mejoras metodológicas](#-próximas-mejoras-metodológicas)

---

# 🧠 Objetivo de modelización

El objetivo principal del sistema es estimar el valor de mercado esperado de futbolistas jóvenes en el mercado europeo a partir de su rendimiento deportivo y contexto competitivo.

El modelo busca detectar:

```text
ineficiencias de mercado
```

mediante la comparación entre:

- valor estimado
- valor observado

---

# ⚙️ Unidad de análisis

La unidad de análisis utilizada es:

```text
Jugador – Temporada
```

Cada observación representa:

- rendimiento deportivo
- contexto competitivo
- situación de mercado

de un jugador en una temporada concreta.

---

# 🎯 Variable objetivo

## Variable principal

```python
log_market_value_eur
```

Fuente:

```text
Transfermarkt
```

---

## Variable secundaria futura

```python
delta_log_market_value_1y
```

Objetivo:

- construir Growth Score
- estimar potencial de revalorización

---

# 📊 Justificación de la transformación logarítmica

El valor de mercado presenta:

- fuerte skewness positiva
- colas largas
- heterocedasticidad

Por tanto, se utiliza:

```python
log_market_value_eur
```

Ventajas:

- mejora estabilidad estadística
- reduce impacto de outliers
- facilita interpretación porcentual
- mejora ajuste del modelo

---

# 📚 Estrategia metodológica

El proyecto combina:

- econometría aplicada
- machine learning supervisado
- feature engineering deportivo

El enfoque principal prioriza:

```text
interpretabilidad
```

sobre complejidad algorítmica extrema.

---

# ⏳ Estrategia de validación

## Decisión adoptada

```text
Temporal out-of-sample validation
```

---

## Split utilizado

| Split | Temporadas |
|---|---|
| Train | 2019-2020 → 2023-2024 |
| Test | 2024-2025 |

---

## Justificación

No se utiliza random split porque:

- introduciría leakage temporal
- rompería coherencia cronológica
- generaría optimismo artificial

La validación temporal reproduce un escenario real de scouting.

---

# 🏗️ Diseño econométrico

## Modelo principal

Regresión OLS con:

- efectos fijos
- errores robustos HC3

---

## Especificación principal

```python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
league FE +
season FE +
position FE
```

---

# 📈 Efectos fijos

## League Fixed Effects

Obligatorios.

Justificación:

- diferencias estructurales entre ligas
- primas reputacionales
- capacidad económica distinta

---

## Season Fixed Effects

Obligatorios.

Justificación:

- inflación del mercado
- shocks macroeconómicos
- cambios estructurales temporales

---

## Position Fixed Effects

Recomendados.

Justificación:

- distinta valoración por rol táctico
- mercados posicionales distintos

---

# 🛡️ Errores robustos HC3

Se utilizan:

```python
HC3 robust standard errors
```

Justificación:

- presencia potencial de heterocedasticidad
- robustez en muestras moderadas
- recomendación estándar en econometría aplicada

---

# ⚠️ Decisiones sobre matching

## Problema principal

FBref y Transfermarkt no comparten identificador común.

---

## Estrategia adoptada

Matching jerárquico:

1. normalización
2. exact matching
3. validación por club
4. fuzzy matching

---

## Decisión metodológica clave

```text
Priorizar cobertura sobre matching ultra estricto
```

---

## Justificación

Un matching demasiado restrictivo:

- destruía tamaño muestral
- reducía capacidad de modelización
- generaba sesgo de selección

---

## Mitigación del riesgo

Se incorporan:

- matching_confidence
- club_score
- robustness checks
- filtros secundarios

---

# 📊 Selección de variables

## Variables deportivas actuales

- goals_per90
- assists_per90
- minutes_played

---

## Variables demográficas

- age
- position_group

---

## Variables contextuales

- league
- season

---

## Variables futuras

Pendiente incorporar:

- progressive_passes_per90
- progressive_carries_per90
- tackles_per90
- interceptions_per90
- xG
- xA

---

# 🤖 Decisiones sobre Machine Learning

## Objetivo

Evaluar si modelos no lineales mejoran capacidad predictiva respecto a OLS.

---

## Modelos implementados

- Random Forest
- HistGradientBoosting
- GradientBoostingRegressor

---

## Resultado principal

ML mejora moderadamente:

- MAE
- RMSE
- R²

pero no sustituye la interpretabilidad del modelo econométrico.

---

# ⚖️ Interpretabilidad vs capacidad predictiva

## Decisión final

```text
OLS = modelo principal
ML = extensión predictiva complementaria
```

---

## Justificación

El objetivo del TFM no es únicamente maximizar R².

También es necesario:

- interpretar resultados
- justificar relaciones económicas
- explicar drivers de mercado
- construir narrativa de scouting

---

# 💡 Construcción del Inefficiency Score

## Definición

```python
inefficiency_score =
valor_estimado - valor_observado
```

---

## Interpretación

| Score | Interpretación |
|---|---|
| Positivo | posible infravaloración |
| Negativo | posible sobrevaloración |

---

# 📌 Robustness checks

Se implementan:

- matching estricto
- validación temporal
- análisis VIF
- comparación OLS vs ML
- estabilidad de rankings

---

# 🚀 Próximas mejoras metodológicas

## Feature engineering avanzado

Pendiente incorporar:

- métricas de progresión
- métricas defensivas
- índices por posición

---

## Growth Score

Objetivo:

```python
delta_log_market_value_1y
```

---

## Dashboard de scouting

Outputs previstos:

- rankings interactivos
- filtros por liga
- filtros por posición
- scouting reports automáticos

---

# 📌 Estado metodológico actual

El sistema ya dispone de:

- pipeline reproducible
- matching robusto
- dataset panel
- modelo econométrico final
- modelos ML supervisados
- validación temporal
- scoring operativo

El proyecto se encuentra en una fase avanzada y metodológicamente sólida para un Trabajo de Fin de Máster en Ciencia de Datos aplicada al fútbol profesional.