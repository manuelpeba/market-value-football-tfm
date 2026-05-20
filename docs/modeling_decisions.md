# 📊 Decisiones de modelización

<div align="center">

![Econometrics](https://img.shields.io/badge/Econometrics-OLS-green)
![Machine Learning](https://img.shields.io/badge/ML-Supervised-blue)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Interpretability](https://img.shields.io/badge/Interpretability-High-success)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-blue)
![Configuration](https://img.shields.io/badge/Configuration-YAML-purple)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo del documento](#-objetivo-del-documento)
- [🎯 Objetivo analítico del proyecto](#-objetivo-analítico-del-proyecto)
- [⚙️ Filosofía de modelización](#️-filosofía-de-modelización)
- [📊 Unidad de análisis](#-unidad-de-análisis)
- [🎯 Variable objetivo](#-variable-objetivo)
- [📚 Decisiones econométricas](#-decisiones-econométricas)
- [📈 Transformación logarítmica](#-transformación-logarítmica)
- [🏗️ Selección de features](#️-selección-de-features)
- [🏟️ Efectos fijos](#️-efectos-fijos)
- [🛡️ Robust standard errors](#️-robust-standard-errors)
- [🤖 Decisiones de Machine Learning](#-decisiones-de-machine-learning)
- [⏳ Estrategia de validación temporal](#-estrategia-de-validación-temporal)
- [🧪 Experiment tracking y reproducibilidad](#-experiment-tracking-y-reproducibilidad)
- [⚙️ Configuración centralizada](#️-configuración-centralizada)
- [📊 Métricas de evaluación](#-métricas-de-evaluación)
- [💡 Decisiones sobre scoring](#-decisiones-sobre-scoring)
- [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
- [🛡️ Prevención de leakage](#️-prevención-de-leakage)
- [📉 Limitaciones actuales](#-limitaciones-actuales)
- [🚀 Próximas decisiones previstas](#-próximas-decisiones-previstas)
- [🧠 Conclusión](#-conclusión)

---

# 🧠 Objetivo del documento

Este documento recoge las principales decisiones metodológicas y de modelización adoptadas durante el desarrollo del sistema analítico.

El objetivo es documentar:

- justificaciones técnicas
- trade-offs metodológicos
- decisiones econométricas
- decisiones de Machine Learning
- criterios de validación
- configuración experimental
- controles de reproducibilidad
- limitaciones actuales

La intención no es únicamente describir modelos utilizados, sino justificar por qué determinadas decisiones resultan coherentes desde la perspectiva de:

- sports analytics
- econometría aplicada
- scouting cuantitativo
- analytics engineering
- reproducibilidad experimental

---

# 🎯 Objetivo analítico del proyecto

El proyecto busca estimar el valor de mercado esperado de futbolistas jóvenes utilizando:

- rendimiento deportivo
- contexto competitivo
- características demográficas
- información de mercado

A partir de dicha estimación se construyen métricas orientadas a detectar posibles ineficiencias de mercado.

---

## Pregunta principal

```text
¿Qué jugadores presentan un valor de mercado inferior al esperado según su rendimiento y contexto competitivo?
```

---

# ⚙️ Filosofía de modelización

La estrategia de modelización combina:

* econometría interpretable
* Machine Learning supervisado
* validación temporal
* scoring cuantitativo
* experiment tracking

---

## Decisión principal

El sistema prioriza inicialmente:

```text
interpretabilidad + robustez
```

frente a:

```text
maximización agresiva de métricas predictivas
```

---

## Justificación

En entornos reales de scouting resulta fundamental:

* justificar rankings
* explicar decisiones
* interpretar drivers del valor
* mantener coherencia futbolística
* evitar modelos opacos difíciles de defender

Por ello el proyecto utiliza:

| Enfoque        | Función                       |
| -------------- | ----------------------------- |
| OLS            | Modelo interpretable baseline |
| ML supervisado | Mejora predictiva             |
| Scoring        | Outputs accionables           |

---

# 📊 Unidad de análisis

La unidad de análisis utilizada es:

```text
Jugador – Temporada
```

---

## Justificación

El valor de mercado es una variable dinámica que evoluciona temporalmente en función de:

* rendimiento reciente
* progresión deportiva
* contexto competitivo
* edad
* exposición mediática
* situación contractual

Trabajar a nivel jugador–temporada permite:

* modelar evolución temporal
* integrar múltiples fuentes
* construir panel longitudinal
* aplicar validación temporal
* generar scoring reproducible

---

# 🎯 Variable objetivo

## Variable principal

```python
market_value_eur
```

---

## Variable utilizada en modelización

```python
log_market_value_eur
```

---

## Justificación del target logarítmico

El valor de mercado presenta:

* fuerte asimetría
* heavy tails
* heterocedasticidad
* concentración extrema en élite

La transformación logarítmica permite:

* estabilizar varianza
* reducir impacto de outliers
* mejorar comportamiento estadístico
* facilitar interpretación relativa
* mejorar ajuste econométrico

---

## Decisión: exclusión de variables de normalización contextual en modelo final

Se evaluó la incorporación de variables derivadas de normalización contextual por posición y competición:

Variables:

- goals_per90_pos_z
- assists_per90_pos_z
- goals_position_percentile
- assists_position_percentile

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS | 1.0035 | 0.8130 | 0.4160 |
| Advanced OLS | 1.0065 | 0.8166 | 0.4148 |

Observaciones:

Se detectó una ligera degradación del rendimiento.

Posible explicación:

Las nuevas variables presentan redundancia informativa con:

- league fixed effects
- season fixed effects
- position fixed effects

Decisión:

Las variables no serán utilizadas en el modelo econométrico final, aunque permanecerán implementadas para futuras iteraciones y modelos supervisados.

---

## Decisión: adopción de variables temporales y de crecimiento

Se evaluó la incorporación de variables relacionadas con dinámica temporal.

Variables:

- age_squared
- career_year
- breakout_indicator

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline | 1.0035 | 0.8130 | 0.4160 |
| Growth | 0.9046 | 0.7278 | 0.5255 |

Observaciones:

Se observa una mejora consistente en todas las métricas.

Interpretación:

El valor de mercado parece depender no solo del rendimiento deportivo actual sino también de factores relacionados con evolución y potencial futuro.

Decisión:

Growth OLS pasa a ser el modelo econométrico preferente para siguientes iteraciones.

---

## Decisión: uso de índices compuestos para explicabilidad

Se evaluó la incorporación de índices agregados construidos mediante combinación de variables futbolísticas.

Índices:

- finishing_index
- playmaking_index
- growth_index
- experience_index

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Growth OLS + Indices | 0.9046 | 0.7278 | 0.5255 |

Observaciones:

No se observó mejora cuantitativa.

Posible explicación:

Los índices agregan información ya presente en:

- goals_per90
- assists_per90
- age
- career_year

Decisión:

Los índices no serán incorporados al modelo econométrico final como variables predictoras.

No obstante, permanecerán implementados para tareas de:

- scouting
- interpretación de rankings
- reporting

---

## Decisión: evaluación inicial de modelos supervisados

Se evaluaron modelos supervisados de tipo ensemble y boosting.

Modelos:

- Random Forest
- XGBoost
- LightGBM

Objetivo:

Determinar si relaciones no lineales mejoran la predicción del valor de mercado.

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS | 0.9046 | 0.7278 | 0.5255 |
| Random Forest | 1.0481 | 0.8527 | 0.3599 |
| XGBoost | 1.0943 | 0.8801 | 0.3022 |
| LightGBM | 1.1078 | 0.8936 | 0.2848 |

Conclusión:

No se observó mejora respecto al benchmark econométrico.

Posibles causas:

- ausencia de tuning
- conjunto reducido de variables
- baja dimensionalidad
- ausencia de variables categóricas codificadas
- tamaño limitado del dataset

---

## Decisión: mejora del pipeline ML mediante tuning y preprocesamiento robusto

Tras la evaluación inicial de modelos supervisados, se observó que Random Forest, XGBoost y LightGBM en configuración baseline no superaban al modelo econométrico Growth OLS.

Esto no implicaba necesariamente que los modelos no lineales fueran inadecuados, sino que la primera iteración presentaba limitaciones metodológicas:

- ausencia de tuning sistemático
- preprocesamiento menos robusto
- control limitado de hiperparámetros
- menor trazabilidad experimental
- posible infraoptimización de modelos de boosting

Por ello se implementó una segunda iteración del pipeline ML.

### Implementación

Archivo:

```text
src/models/machine_learning/train_ml_tuned.py
```

### Decisiones técnicas

Se incorporó un pipeline de preprocesamiento basado en:

* `ColumnTransformer`
* `SimpleImputer`
* `StandardScaler`
* `OneHotEncoder`

Esta decisión permite tratar adecuadamente variables numéricas y categóricas dentro de un flujo reproducible, reduciendo riesgo de inconsistencias entre entrenamiento y evaluación.

### Estrategia de tuning

Se utilizó:

```text
RandomizedSearchCV
n_iter = 12
```

La elección de búsqueda aleatoria responde a un trade-off entre:

* exploración razonable del espacio de hiperparámetros
* coste computacional controlado
* reproducibilidad
* suficiencia metodológica para una iteración de TFM

No se optó por una búsqueda exhaustiva porque el objetivo del sprint era validar si el bajo rendimiento inicial de ML se debía a infraoptimización, no maximizar agresivamente la métrica.

### Validación temporal

Se mantuvo la división:

```text
Train: temporadas < 2023
Test: temporadas >= 2023
```

Esta decisión preserva la coherencia metodológica del proyecto y evita leakage temporal.

### Modelos evaluados

* Tuned Random Forest
* Tuned XGBoost
* Tuned LightGBM
* HistGradientBoosting

### Resultados

| Modelo               |       RMSE |        MAE |         R² |
| -------------------- | ---------: | ---------: | ---------: |
| Growth OLS           |     0.9046 |     0.7278 |     0.5255 |
| Tuned Random Forest  |     0.9076 |     0.7315 |     0.5200 |
| Tuned XGBoost        | **0.8753** | **0.7004** | **0.5536** |
| Tuned LightGBM       |     0.8864 |     0.7162 |     0.5421 |
| HistGradientBoosting |     0.8825 |     0.7118 |     0.5462 |

### Interpretación

El ajuste de hiperparámetros y la mejora del pipeline permiten que los modelos supervisados superen al benchmark econométrico.

El mejor resultado corresponde a:

```text
Tuned XGBoost
```

con:

```text
R² = 0.5536
```

Esto supone una mejora relativa aproximada del 5.3% frente al Growth OLS.

### Decisión metodológica

A partir de este sprint, el sistema adopta una arquitectura híbrida:

| Componente                | Rol                              |
| ------------------------- | -------------------------------- |
| Growth OLS                | Benchmark interpretable          |
| Tuned XGBoost             | Mejor modelo predictivo actual   |
| Feature importance / SHAP | Capa de explicabilidad           |
| Scoring pipeline          | Traducción a outputs de scouting |

### Implicación

El resultado justifica avanzar hacia modelos supervisados más complejos, siempre que se acompañen de mecanismos de interpretabilidad.

Por ello, la siguiente decisión metodológica será incorporar explainability mediante:

* feature importance global
* SHAP values
* interpretaciones locales por jugador
* análisis de dependencia de variables

El objetivo no es únicamente mejorar métricas, sino transformar el modelo en una herramienta defendible para scouting profesional.

---

# 📚 Decisiones econométricas

## Modelo baseline seleccionado

```text
Ordinary Least Squares (OLS)
```

---

## Justificación

OLS constituye una decisión coherente debido a:

* interpretabilidad
* robustez
* facilidad de explicación
* estándar académico
* uso frecuente en sports analytics
* capacidad para modelar relaciones marginales

---

## Rol dentro del sistema

OLS actúa como:

```text
baseline interpretable del sistema
```

sobre el cual se comparan modelos más complejos.

---

## Decisión metodológica importante

El objetivo inicial no era maximizar R², sino construir:

* modelo defendible
* relaciones económicamente coherentes
* outputs interpretables
* scoring estable

---

# 📈 Transformación logarítmica

## Variable transformada

```python
log_market_value_eur
```

---

## Razones estadísticas

La distribución original de mercado presenta:

* alta asimetría
* colas largas
* outliers extremos

---

## Beneficios

La transformación logarítmica mejora:

* linealidad
* estabilidad de residuos
* interpretabilidad relativa
* robustez del modelo
* comparabilidad entre jugadores

---

## Interpretación

Los coeficientes pueden interpretarse aproximadamente como:

```text
cambios porcentuales relativos
```

en valor de mercado.

---

# 🏗️ Selección de features

## Filosofía general

El feature set inicial prioriza:

* simplicidad
* interpretabilidad
* coherencia futbolística
* estabilidad estadística

---

## Variables actuales

### Rendimiento ofensivo

* goals_per90
* assists_per90
* g_a_per90

---

### Volumen de juego

* minutes_played
* log_minutes_played
* starts
* nineties

---

### Contexto

* league
* season
* position_group
* age

---

## Decisión importante

Se evitó inicialmente incluir:

* demasiadas métricas correlacionadas
* features altamente derivadas
* variables con leakage temporal
* features difíciles de interpretar

---

## Justificación

El objetivo era construir primero:

```text
baseline estable y defendible
```

antes de aumentar complejidad.

---

# 🏟️ Efectos fijos

## Fixed effects utilizados

### Liga

```text
league FE
```

---

### Temporada

```text
season FE
```

---

### Posición

```text
position FE
```

---

## Justificación

Los efectos fijos permiten controlar heterogeneidad estructural derivada de:

* diferencias económicas entre ligas
* cambios de mercado entre temporadas
* diferencias estructurales entre posiciones

---

## Ejemplos observados

### Premier League

Se detecta prima estructural positiva significativa.

---

### Eredivisie / Liga Portugal

Se observan descuentos estructurales consistentes.

---

## Beneficio metodológico

Los fixed effects permiten que:

```text
las métricas deportivas no absorban diferencias contextuales estructurales
```

---

# 🛡️ Robust standard errors

## Método utilizado

```text
HC3 robust covariance
```

---

## Justificación

Los datos deportivos presentan frecuentemente:

* heterocedasticidad
* varianza no constante
* ruido estructural

---

## Beneficio

HC3 permite:

* inferencia más robusta
* errores estándar más fiables
* mayor rigor econométrico

---

## Decisión metodológica

Se priorizó robustez inferencial sobre simplicidad computacional.

---

# 🤖 Decisiones de Machine Learning

## Objetivo

Evaluar si modelos no lineales mejoran capacidad predictiva respecto a OLS.

---

## Modelos implementados

* RandomForestRegressor
* GradientBoostingRegressor
* HistGradientBoostingRegressor

---

## Justificación de selección

Estos modelos son adecuados para:

* datasets tabulares
* relaciones no lineales
* interacciones implícitas
* tamaño medio de muestra

---

## Decisión importante

No se seleccionaron inicialmente modelos extremadamente complejos porque:

* el dataset todavía es relativamente pequeño
* el principal cuello de botella parece ser el signal
* se priorizó control metodológico

---

## Resultado observado

ML mejora moderadamente respecto a OLS:

| Modelo            |   R² |
| ----------------- | ---: |
| OLS final         | 0.44 |
| Gradient Boosting | 0.48 |

---

## Interpretación

La mejora limitada sugiere que:

```text
la principal limitación actual es el feature set
```

más que el algoritmo.

---

# ⏳ Estrategia de validación temporal

## Decisión crítica

El sistema utiliza:

```text
temporal validation
```

---

## Split utilizado

| Split | Temporadas            |
| ----- | --------------------- |
| Train | 2019-2020 → 2023-2024 |
| Test  | 2024-2025             |

---

## Justificación

El random split:

* rompe coherencia temporal
* introduce leakage
* genera optimismo artificial
* sobreestima capacidad predictiva

---

## Objetivo

Simular escenarios reales de scouting futuro.

---

## Beneficio

La validación temporal aumenta significativamente:

* rigor metodológico
* realismo operacional
* credibilidad de resultados

---

# 🧪 Experiment tracking y reproducibilidad

## Herramienta utilizada

```text
MLflow
```

---

## Objetivo

Registrar automáticamente:

* métricas
* hiperparámetros
* configuraciones
* artefactos
* modelos
* outputs

---

## Información registrada

### Parámetros

* features utilizadas
* target
* fixed effects
* hiperparámetros
* configuración experimental
* split temporal

---

### Métricas

* RMSE
* MAE
* R²

---

### Artefactos

* modelos
* rankings
* predicciones
* feature importance
* diagnósticos

---

## Justificación metodológica

MLflow mejora:

* reproducibilidad
* trazabilidad
* comparación entre experimentos
* auditoría metodológica
* defensa académica

---

## Decisión importante

El tracking experimental permite justificar:

```text
por qué un modelo o configuración fue seleccionado
```

frente a alternativas.

---

# ⚙️ Configuración centralizada

## Objetivo

Separar configuración y lógica funcional.

---

## Directorio

<pre>
config/
</pre>

---

## Archivos principales

| Archivo       | Función               |
| ------------- | --------------------- |
| modeling.yaml | Modelización          |
| features.yaml | Features              |
| matching.yaml | Matching              |
| paths.yaml    | Paths                 |
| project.yaml  | Configuración general |

---

## Beneficios

La configuración centralizada permite:

* evitar hardcoding
* facilitar experimentación
* mantener coherencia
* versionar configuraciones
* mejorar mantenibilidad

---

## Decisión metodológica

La configuración declara parámetros.

La lógica permanece en:

<pre>
src/
</pre>

---

# 📊 Métricas de evaluación

## Métricas utilizadas

| Métrica | Objetivo                     |
| ------- | ---------------------------- |
| RMSE    | Penalización errores grandes |
| MAE     | Error medio interpretable    |
| R²      | Capacidad explicativa        |

---

## Justificación

Se combinan métricas complementarias para evitar:

* dependencia excesiva de una única métrica
* interpretaciones parciales
* optimización artificial

---

## Decisión importante

No se priorizó únicamente maximizar R².

También se evaluó:

* estabilidad
* interpretabilidad
* coherencia futbolística
* robustez temporal

---

# 💡 Decisiones sobre scoring

## Objetivo

Transformar outputs de modelización en señales accionables para scouting.

---

# Métrica principal

```python
inefficiency_score =
valor_estimado - valor_observado
```

---

## Interpretación

| Score    | Significado             |
| -------- | ----------------------- |
| Positivo | Posible infravaloración |
| Negativo | Posible sobrevaloración |

---

## Justificación

El scoring permite traducir outputs estadísticos en:

* rankings
* shortlists
* señales scouting
* oportunidades potenciales

---

## Decisión metodológica

El scoring se construye sobre:

```text
predicciones out-of-sample
```

para evitar optimismo artificial.

---

# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs predicción

Trade-off principal del proyecto.

---

## Decisión adoptada

Priorizar inicialmente:

```text
interpretabilidad + robustez
```

frente a:

```text
modelos extremadamente complejos
```

---

## Justificación

En scouting profesional resulta más útil:

* explicar rankings
* entender drivers
* justificar decisiones

que ganar pequeñas mejoras marginales de R² con modelos opacos.

---

## Flexibilidad futura

La arquitectura actual permite incorporar posteriormente:

* CatBoost
* TabPFN
* SHAP
* modelos específicos por posición

sin rediseñar el sistema.

---

# 🛡️ Prevención de leakage

## Principio general

Todo feature debe existir en el momento temporal de decisión.

---

## Variables excluidas

Ejemplos:

* market_value_next_eur
* delta_log_market_value_1y
* predicted_market_value_eur
* rankings derivados

---

## Tipos de leakage controlados

* leakage temporal
* target leakage
* leakage entre train/test
* leakage derivado de scoring

---

## Decisión importante

Los outputs del modelo:

* no vuelven al dataset base
* no se utilizan como inputs
* permanecen separados en reports/artifacts

---

# 📉 Limitaciones actuales

## Feature engineering

El feature set todavía es limitado respecto a sistemas profesionales.

---

## Métricas avanzadas pendientes

* progression metrics
* percentiles
* z-scores por posición
* métricas defensivas
* rolling metrics
* trajectory features

---

## Dataset size

El dataset modelizable sigue siendo relativamente pequeño para ML avanzado.

---

## Cobertura contextual

Todavía faltan:

* xG
* xA
* métricas de posesión avanzadas
* eventos tipo StatsBomb

---

# 🚀 Próximas decisiones previstas

## Modelización

Posibles próximos modelos:

* CatBoost
* TabPFN
* modelos por posición

---

## Explainability

Pendiente incorporar:

* SHAP global
* SHAP individual
* explicación automática de rankings

---

## Feature engineering

Prioridad principal actual:

```text
incrementar señal predictiva
```

---

## Opportunity Score

Próxima evolución prevista:

```python
Opportunity Score =
inefficiency_score +
growth_score +
confidence_score
```

---

## Validación avanzada

Pendiente:

* robustness checks
* estabilidad rankings
* análisis longitudinal
* sensibilidad por liga

---

# 🧠 Conclusión

La estrategia de modelización adoptada busca equilibrar:

* rigor metodológico
* interpretabilidad
* capacidad predictiva
* coherencia futbolística
* reproducibilidad experimental

El sistema actual combina:

* econometría interpretable
* Machine Learning supervisado
* validación temporal
* scoring cuantitativo
* MLflow tracking
* configuración centralizada

La incorporación de tracking experimental y configuración desacoplada supone un salto importante en madurez metodológica, ya que permite auditar decisiones, comparar ejecuciones y justificar configuraciones de manera reproducible.

El siguiente gran salto de valor del proyecto dependerá principalmente de:

```text
feature engineering avanzado y enriquecimiento del signal predictivo
```

más que de incrementar complejidad algorítmica de forma aislada.
