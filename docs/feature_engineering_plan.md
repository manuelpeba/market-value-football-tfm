````md id="0m9j4v"
# 🧪 Plan de Feature Engineering

<div align="center">

![Feature Engineering](https://img.shields.io/badge/Feature%20Engineering-Advanced-blue)
![Sports Analytics](https://img.shields.io/badge/Sports%20Analytics-Football-success)
![Modeling](https://img.shields.io/badge/Modeling-Econometrics%20%2B%20ML-orange)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)
![Config](https://img.shields.io/badge/Configuration-YAML-purple)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo del documento](#-objetivo-del-documento)
- [⚙️ Filosofía de feature engineering](#️-filosofía-de-feature-engineering)
- [📊 Estado actual del feature set](#-estado-actual-del-feature-set)
- [🏗️ Arquitectura de feature engineering](#️-arquitectura-de-feature-engineering)
- [📦 Fuentes utilizadas](#-fuentes-utilizadas)
- [⚽ Features ofensivas actuales](#-features-ofensivas-actuales)
- [🛡️ Features defensivas actuales](#️-features-defensivas-actuales)
- [⏱️ Features de volumen y contexto](#️-features-de-volumen-y-contexto)
- [📈 Features derivadas actuales](#-features-derivadas-actuales)
- [🎯 Objetivos de mejora del feature set](#-objetivos-de-mejora-del-feature-set)
- [📊 Positional normalization](#-positional-normalization)
- [📈 Percentiles y z-scores](#-percentiles-y-z-scores)
- [🚀 Progression metrics](#-progression-metrics)
- [📉 Growth features](#-growth-features)
- [🛡️ Features defensivas avanzadas](#️-features-defensivas-avanzadas)
- [⚡ Features de progresión y posesión](#-features-de-progresión-y-posesión)
- [📈 Rolling features](#-rolling-features)
- [🏟️ Features contextuales avanzadas](#️-features-contextuales-avanzadas)
- [🧪 Relación con MLflow y tracking](#-relación-con-mlflow-y-tracking)
- [⚙️ Configuración centralizada](#️-configuración-centralizada)
- [🛡️ Prevención de leakage](#️-prevención-de-leakage)
- [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
- [🚀 Roadmap priorizado](#-roadmap-priorizado)
- [🧠 Conclusión](#-conclusión)

---

# 🧠 Objetivo del documento

Este documento describe la estrategia de feature engineering utilizada y prevista dentro del sistema analítico.

El objetivo es:

- documentar features actuales
- justificar decisiones metodológicas
- identificar limitaciones
- priorizar mejoras
- aumentar señal predictiva
- mantener interpretabilidad
- preservar consistencia temporal
- garantizar reproducibilidad

---

# ⚙️ Filosofía de feature engineering

La estrategia de feature engineering sigue un enfoque incremental.

---

## Principio central

Priorizar inicialmente:

```text id="5s2o4q"
baseline interpretable y robusto
```

antes de introducir:

* features altamente complejas
* transformaciones opacas
* ingeniería excesiva
* señales difíciles de justificar

---

## Objetivo metodológico

Construir features que sean:

* coherentes futbolísticamente
* interpretables
* temporalmente válidas
* robustas
* reproducibles
* escalables

---

## Decisión estratégica

Actualmente el principal cuello de botella del sistema es:

```text id="vcx3ua"
la calidad y riqueza del feature set
```

más que el algoritmo utilizado.

---

# 📊 Estado actual del feature set

## Estado general

El sistema dispone actualmente de un baseline sólido de variables:

* ofensivas
* contextuales
* demográficas
* volumen de juego

---

## Limitación principal

Todavía faltan:

* señales longitudinales
* normalización avanzada
* métricas contextuales sofisticadas
* métricas defensivas robustas
* indicadores de progresión

---

## Resultado observado

La mejora moderada de ML respecto a OLS sugiere que:

```text id="n6xgby"
el signal actual todavía es limitado
```

---

# 🏗️ Arquitectura de feature engineering

## Directorios principales

### Pipelines

<pre>
src/data/
src/features/
</pre>

---

### Configuración

<pre>
config/features.yaml
</pre>

---

### Outputs

<pre>
data/processed/
</pre>

---

## Filosofía de arquitectura

Separar:

* extracción
* transformación
* normalización
* modelización
* scoring
* tracking experimental

---

## Relación con MLflow

Las features utilizadas en cada experimento deben registrarse automáticamente mediante:

```text id="tcfumx"
MLflow
```

---

# 📦 Fuentes utilizadas

## FBref

### Información utilizada

* goles
* asistencias
* minutos
* métricas por 90
* acciones ofensivas
* acciones defensivas

---

## Transfermarkt

### Información utilizada

* valor de mercado
* edad
* club
* posición
* histórico temporal

---

## Fuentes previstas futuras

| Fuente              | Estado    |
| ------------------- | --------- |
| Understat           | Pendiente |
| StatsBomb Open Data | Pendiente |

---

# ⚽ Features ofensivas actuales

## Features principales

| Variable      | Tipo                |
| ------------- | ------------------- |
| goals_per90   | Producción ofensiva |
| assists_per90 | Creación            |
| g_a_per90     | Producción agregada |
| shots_per90   | Volumen ofensivo    |

---

## Justificación

Estas métricas:

* son interpretables
* tienen señal futbolística clara
* están relativamente estandarizadas
* permiten baseline sólido

---

## Limitación

No capturan completamente:

* calidad de ocasiones
* progresión
* creación avanzada
* contexto táctico

---

# 🛡️ Features defensivas actuales

## Variables disponibles

| Variable             | Tipo              |
| -------------------- | ----------------- |
| tackles_per90        | Recuperación      |
| interceptions_per90  | Lectura defensiva |
| blocks_per90         | Bloqueos          |
| aerial_duels_won_pct | Juego aéreo       |

---

## Limitaciones actuales

Las métricas defensivas:

* presentan más ruido
* dependen mucho del contexto táctico
* son más difíciles de interpretar aisladamente

---

## Problema principal

El sistema todavía tiene:

```text id="33yt5n"
infra-representación defensiva
```

respecto a perfiles ofensivos.

---

# ⏱️ Features de volumen y contexto

## Variables actuales

| Variable           | Función              |
| ------------------ | -------------------- |
| minutes_played     | Exposición           |
| log_minutes_played | Robustez             |
| starts             | Participación        |
| nineties           | Normalización        |
| age                | Desarrollo           |
| league             | Contexto competitivo |
| season             | Contexto temporal    |
| position_group     | Contexto posicional  |

---

## Justificación

Estas variables permiten controlar:

* exposición competitiva
* diferencias estructurales
* contexto de rendimiento
* edad y progresión

---

# 📈 Features derivadas actuales

## Variables transformadas

| Variable             | Transformación |
| -------------------- | -------------- |
| log_market_value_eur | Log target     |
| log_minutes_played   | Log minutos    |
| g_a_per90            | Suma ofensiva  |

---

## Objetivo

Reducir:

* asimetría
* ruido
* heterocedasticidad

---

## Estado actual

Las transformaciones actuales siguen siendo relativamente simples y priorizan interpretabilidad.

---

# 🎯 Objetivos de mejora del feature set

## Prioridad estratégica

El principal objetivo futuro es:

```text id="u81b0q"
incrementar señal predictiva
```

manteniendo:

* robustez
* interpretabilidad
* validez temporal

---

## Líneas prioritarias

| Área                     | Prioridad |
| ------------------------ | --------- |
| Positional normalization | Alta      |
| Progression metrics      | Alta      |
| Growth features          | Alta      |
| Defensive enrichment     | Alta      |
| Rolling metrics          | Media     |
| Tactical context         | Media     |
| Event data               | Media     |
| Deep representations     | Baja      |

---

# 📊 Positional normalization

## Problema actual

Comparar métricas absolutas entre posiciones introduce sesgos importantes.

Ejemplo:

* un central no debe evaluarse como un delantero
* un mediocentro no produce igual que un extremo

---

## Solución prevista

Normalización por:

* posición
* liga
* temporada

---

## Variables previstas

| Variable            | Descripción       |
| ------------------- | ----------------- |
| goals_per90_pos_z   | Z-score ofensivo  |
| assists_per90_pos_z | Creación relativa |
| shots_per90_pos_z   | Volumen relativo  |
| tackles_per90_pos_z | Defensa relativa  |

---

## Beneficio

Permite capturar:

```text id="1pltt5"
rendimiento relativo dentro del contexto competitivo correcto
```

---

# 📈 Percentiles y z-scores

## Objetivo

Reducir dependencia de métricas absolutas.

---

## Estrategia

Calcular:

* percentiles
* z-scores
* rankings relativos

por:

* posición
* liga
* temporada

---

## Beneficios

Estas transformaciones permiten:

* comparabilidad
* robustez contextual
* mejor señal relativa
* reducción de sesgos estructurales

---

## Variables previstas

| Variable             | Tipo                |
| -------------------- | ------------------- |
| offensive_percentile | Percentil ofensivo  |
| defensive_percentile | Percentil defensivo |
| progression_z        | Progresión relativa |

---

# 🚀 Progression metrics

## Objetivo

Capturar evolución deportiva.

---

## Problema actual

El sistema modela principalmente:

```text id="7ul98l"
estado actual del jugador
```

pero no suficientemente:

```text id="sk0hgi"
trayectoria de evolución
```

---

## Variables previstas

| Variable                 | Descripción         |
| ------------------------ | ------------------- |
| delta_minutes_yoy        | Evolución minutos   |
| delta_goals_per90_yoy    | Evolución ofensiva  |
| delta_assists_per90_yoy  | Evolución creativa  |
| age_adjusted_progression | Progresión relativa |

---

## Beneficio

Estas variables permitirán mejorar:

* Growth Score
* proyección futura
* identificación temprana de talento

---

# 📉 Growth features

## Objetivo

Modelar potencial de revalorización.

---

## Variables previstas

| Variable                 | Descripción             |
| ------------------------ | ----------------------- |
| market_value_growth_prev | Crecimiento histórico   |
| valuation_acceleration   | Aceleración crecimiento |
| growth_consistency       | Estabilidad progresión  |
| breakout_indicator       | Explosión reciente      |

---

## Relación con scouting

Estas features son especialmente relevantes para:

```text id="7m5wfh"
estrategias buy low → sell high
```

---

# 🛡️ Features defensivas avanzadas

## Problema actual

Los perfiles defensivos están parcialmente inframodelados.

---

## Métricas previstas

| Variable                | Descripción         |
| ----------------------- | ------------------- |
| pressures_per90         | Presión             |
| defensive_actions_per90 | Actividad defensiva |
| recoveries_per90        | Recuperaciones      |
| duel_win_pct            | Dominio defensivo   |

---

## Fuentes potenciales

| Fuente    | Estado  |
| --------- | ------- |
| FBref     | Parcial |
| StatsBomb | Futuro  |
| Understat | Parcial |

---

## Objetivo

Reducir sesgo ofensivo del sistema.

---

# ⚡ Features de progresión y posesión

## Variables previstas

| Variable                  | Descripción           |
| ------------------------- | --------------------- |
| progressive_passes_per90  | Progresión pase       |
| progressive_carries_per90 | Progresión conducción |
| carries_into_final_third  | Avance territorial    |
| passes_into_penalty_area  | Creación avanzada     |

---

## Beneficio

Estas métricas permiten capturar:

* progresión
* influencia territorial
* creación indirecta
* impacto no reflejado en goles/asistencias

---

# 📈 Rolling features

## Objetivo

Capturar dinámica temporal reciente.

---

## Variables previstas

| Variable              | Descripción        |
| --------------------- | ------------------ |
| rolling_goals_per90   | Tendencia ofensiva |
| rolling_minutes       | Continuidad        |
| rolling_market_growth | Momentum mercado   |

---

## Riesgo principal

Las rolling features requieren especial control para evitar:

```text id="1c4wsh"
leakage temporal
```

---

# 🏟️ Features contextuales avanzadas

## Variables previstas

| Variable             | Descripción              |
| -------------------- | ------------------------ |
| league_strength      | Nivel competitivo        |
| club_strength        | Contexto colectivo       |
| european_competition | Exposición internacional |
| team_possession_pct  | Contexto táctico         |

---

## Beneficio

Permiten contextualizar mejor:

* rendimiento individual
* entorno competitivo
* dificultad contextual

---

# 🧪 Relación con MLflow y tracking

## Objetivo

Registrar automáticamente:

* features utilizadas
* transformaciones
* grupos de variables
* métricas asociadas
* importancia de variables

---

## Herramienta

```text id="vnzk5g"
MLflow
```

---

## Beneficios

MLflow permite:

* comparar feature sets
* analizar impacto incremental
* reconstruir experimentos
* justificar decisiones metodológicas

---

## Información registrada

### Parámetros

* lista de features
* grupos de features
* normalizaciones activas
* transformaciones utilizadas

---

### Artefactos

* feature importance
* rankings derivados
* predicciones
* diagnósticos

---

# ⚙️ Configuración centralizada

## Directorio

<pre>
config/features.yaml
</pre>

---

## Objetivo

Centralizar:

* features activas
* thresholds
* grupos de variables
* transformaciones
* normalizaciones

---

## Beneficios

La configuración centralizada permite:

* evitar hardcoding
* comparar configuraciones
* reproducir experimentos
* activar/desactivar bloques fácilmente

---

## Ejemplo conceptual

```yaml id="6c6fdm"
feature_groups:
  offensive:
    - goals_per90
    - assists_per90

  progression:
    - progressive_passes_per90
    - progressive_carries_per90
```

---

## Positional normalization experiment

### Objetivo

Evaluar si la normalización relativa por contexto competitivo mejora el rendimiento predictivo.

---

### Variables generadas

#### Z-score contextual

Variables:

- goals_per90_pos_z
- assists_per90_pos_z
- shots_per90_pos_z

Fórmula:

z=(x−μ)/σ

donde:

- x = valor individual
- μ = media del grupo
- σ = desviación estándar del grupo

---

#### Percentiles relativos

Variables:

- goals_position_percentile
- assists_position_percentile

Agrupación utilizada:

```text
[position_group, league]
```

---

### Resultado experimental

No se observaron mejoras predictivas relevantes tras incorporar estas variables.

Las variables permanecen disponibles para futuros modelos ML o análisis exploratorios.

---

# 🛡️ Prevención de leakage

## Principio fundamental

Toda feature debe existir:

```text id="10dxjw"
en el momento real de decisión
```

---

## Variables excluidas

| Variable                   | Motivo             |
| -------------------------- | ------------------ |
| market_value_next_eur      | Información futura |
| future_minutes             | Información futura |
| delta_log_market_value_1y  | Leakage temporal   |
| predicted_market_value_eur | Output derivado    |
| inefficiency_score         | Output derivado    |

---

## Riesgo especial

Las variables longitudinales requieren especial cuidado para no introducir:

* información futura
* contaminación temporal
* optimismo artificial

---

# ⚖️ Trade-offs metodológicos

## Complejidad vs interpretabilidad

Trade-off principal del feature engineering.

---

## Riesgo de exceso de features

Demasiadas variables pueden generar:

* multicolinealidad
* sobreajuste
* pérdida de interpretabilidad
* ruido adicional

---

## Decisión actual

Priorizar:

```text id="4s3oy8"
features robustas y futbolísticamente coherentes
```

---

## Estrategia incremental

La complejidad se incrementará progresivamente según:

* validación experimental
* mejora real de métricas
* estabilidad de rankings
* coherencia metodológica

---

# 🚀 Roadmap priorizado

## Prioridad alta

### 1️⃣ Positional normalization

* z-scores
* percentiles
* rankings relativos

---

### 2️⃣ Progression metrics

* métricas longitudinales
* evolución interanual
* aceleración de desarrollo

---

### 3️⃣ Features defensivas

* recuperación
* presión
* dominio defensivo

---

## Prioridad media

### 4️⃣ Rolling metrics

* tendencias recientes
* momentum
* estabilidad temporal

---

### 5️⃣ Tactical context

* posesión
* strength context
* exposición internacional

---

## Prioridad futura

### 6️⃣ Event-based modeling

* eventos StatsBomb
* secuencias
* acciones avanzadas

---

### 7️⃣ Explainability avanzada

* SHAP
* contribución individual
* explicación de rankings

---

# 🧠 Conclusión

El feature engineering representa actualmente el área con mayor potencial de mejora del sistema analítico.

La arquitectura ya permite:

* integración modular
* tracking experimental
* configuración desacoplada
* validación temporal
* comparación rigurosa de experimentos

La incorporación de:

* normalización contextual
* métricas longitudinales
* señales de progresión
* features defensivas avanzadas

será probablemente el principal factor que determine la evolución futura de la capacidad predictiva y utilidad práctica del sistema de scouting cuantitativo.

La prioridad metodológica no debe centrarse únicamente en añadir más variables, sino en construir:

```text id="d7i7ul"
features con verdadera señal futbolística y validez temporal
```