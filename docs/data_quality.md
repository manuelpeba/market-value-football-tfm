````md id="4k1vqp"
# 🧪 Calidad de datos

<div align="center">

![Data Quality](https://img.shields.io/badge/Data%20Quality-Validated-success)
![Matching](https://img.shields.io/badge/Matching-88.36%25-brightgreen)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Architecture](https://img.shields.io/badge/Architecture-Modular-blue)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)
![Config](https://img.shields.io/badge/Configuration-YAML-purple)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo del documento](#-objetivo-del-documento)
- [🏗️ Filosofía de calidad de datos](#️-filosofía-de-calidad-de-datos)
- [📦 Fuentes analizadas](#-fuentes-analizadas)
- [⚠️ Principales riesgos de calidad](#️-principales-riesgos-de-calidad)
- [🔗 Calidad del matching](#-calidad-del-matching)
- [📊 Resultados del matching](#-resultados-del-matching)
- [🧪 Controles de validación implementados](#-controles-de-validación-implementados)
- [📉 Calidad del dataset modelizable](#-calidad-del-dataset-modelizable)
- [🛡️ Prevención de leakage](#️-prevención-de-leakage)
- [📈 Calidad temporal](#-calidad-temporal)
- [📂 Controles de esquema](#-controles-de-esquema)
- [⚙️ Configuración centralizada de validaciones](#️-configuración-centralizada-de-validaciones)
- [🧪 Tracking y auditoría experimental](#-tracking-y-auditoría-experimental)
- [📝 Logging y trazabilidad](#-logging-y-trazabilidad)
- [⚖️ Trade-offs metodológicos](#️-trade-offs-metodológicos)
- [📉 Limitaciones actuales](#-limitaciones-actuales)
- [🚀 Mejoras futuras previstas](#-mejoras-futuras-previstas)
- [🧠 Conclusión](#-conclusión)

---

# 🧠 Objetivo del documento

Este documento describe los controles y decisiones relacionados con la calidad de datos dentro del sistema analítico.

El objetivo es documentar:

- riesgos identificados
- controles implementados
- validaciones de integración
- calidad del matching
- consistencia temporal
- prevención de leakage
- trazabilidad experimental
- controles de reproducibilidad

La calidad de datos constituye un componente crítico del proyecto porque el sistema depende de:

```text
integración multi-fuente sin identificador común
```

---

# 🏗️ Filosofía de calidad de datos

La estrategia de calidad de datos se basa en cinco principios principales:

| Principio              | Objetivo                         |
| ---------------------- | -------------------------------- |
| Validación incremental | Detectar errores tempranos       |
| Reproducibilidad       | Evitar transformaciones manuales |
| Auditabilidad          | Poder rastrear decisiones        |
| Separación de capas    | Evitar contaminación             |
| Consistencia temporal  | Evitar leakage                   |

---

## Principio metodológico central

Se prioriza:

```text id="5kgfgj"
calidad y robustez del dataset
```

frente a:

```text id="3vd8fs"
maximizar artificialmente cobertura
```

---

## Implicación práctica

El sistema prefiere:

* perder observaciones ambiguas
* mantener mayor confianza
* reducir false positives
* preservar coherencia metodológica

---

# 📦 Fuentes analizadas

## FBref

### Tipo de información

* rendimiento deportivo
* métricas por 90
* participación
* estadísticas ofensivas y defensivas

---

## Transfermarkt

### Tipo de información

* valor de mercado
* edad
* club
* posición
* histórico temporal

---

## Problema principal

Las fuentes:

```text id="ghh0jx"
NO comparten identificador universal
```

---

# ⚠️ Principales riesgos de calidad

## 1️⃣ Riesgo de matching incorrecto

Problemas detectados:

* transliteraciones
* nombres inconsistentes
* cambios de club
* variaciones ortográficas
* granularidad distinta

---

## 2️⃣ Leakage temporal

Riesgo de incorporar:

* información futura
* variables derivadas posteriores
* outputs del modelo

---

## 3️⃣ Inconsistencias contextuales

Ejemplos:

* ligas distintas
* posiciones ambiguas
* diferencias de calendario
* cambios intra-temporada

---

## 4️⃣ Datos faltantes

Riesgos:

* baja cobertura
* features incompletas
* temporadas parciales

---

## 5️⃣ Ruido estructural

Problemas derivados de:

* variabilidad deportiva
* mercado subjetivo
* observaciones extremas
* muestras reducidas por posición

---

# 🔗 Calidad del matching

## Problema crítico del proyecto

El matching FBref ↔ Transfermarkt representa el principal reto técnico del sistema.

---

## Objetivo

Construir integración robusta manteniendo:

* precisión
* coherencia temporal
* trazabilidad
* auditabilidad

---

## Estrategia implementada

Pipeline jerárquico:

1. normalización
2. matching exacto
3. validación por club
4. matching fuzzy
5. validación por edad

---

## Variables utilizadas

| Variable               | Uso                   |
| ---------------------- | --------------------- |
| player_name_normalized | Matching principal    |
| age                    | Validación            |
| club                   | Validación contextual |
| season                 | Restricción temporal  |

---

## Algoritmo fuzzy

```text id="khpn5d"
RapidFuzz
```

---

## Thresholds actuales

```python id="r0nt6g"
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

---

## Justificación metodológica

Los thresholds se diseñaron para:

* minimizar false positives
* restringir matching ambiguo
* mantener trazabilidad
* preservar coherencia futbolística

---

# 📊 Resultados del matching

## Resultados globales

| Métrica                   | Resultado |
| ------------------------- | --------: |
| Observaciones totales     |    23,580 |
| Observaciones emparejadas |    20,836 |
| Match rate                |    88.36% |

---

## Distribución de métodos

| Método                   | Interpretación             |
| ------------------------ | -------------------------- |
| exact_age_validated      | Dominante                  |
| exact_age_club_validated | Alta confianza             |
| fuzzy_age_club_validated | Casos ambiguos controlados |

---

## Insight principal

El matching exacto domina claramente el dataset final.

Esto reduce significativamente:

* riesgo de false positives
* contaminación del dataset
* ruido en modelización

---

## Decisión metodológica

El sistema prefiere:

```text id="3l3ffr"
perder cobertura antes que introducir matching dudoso
```

---

# 🧪 Controles de validación implementados

## Validaciones de esquema

### Controles

* columnas críticas existentes
* tipos válidos
* nombres consistentes
* unicidad esperada

---

## Validaciones de negocio

### Controles

* market value positivo
* edad válida
* minutos razonables
* temporada válida
* posición válida

---

## Validaciones temporales

### Controles

* coherencia cronológica
* temporadas válidas
* orden temporal consistente

---

## Validaciones de matching

### Controles

* diferencia máxima de edad
* similitud de club
* confidence score mínimo
* trazabilidad del método

---

## Validaciones de modelización

### Controles

* features completas
* target válido
* categorías válidas
* split temporal correcto

---

# 📉 Calidad del dataset modelizable

## Dataset final

| Métrica          | Valor |
| ---------------- | ----: |
| Observaciones    | 3,297 |
| Jugadores únicos | 1,847 |
| Edad             | 18–23 |
| Ligas            |     7 |

---

## Filtros aplicados

* matching válido
* minutos mínimos
* market value disponible
* edad válida
* posición válida

---

## Justificación

Los filtros buscan construir un dataset:

```text id="6n6d8j"
más pequeño pero más fiable
```

---

## Beneficio

Esto mejora:

* estabilidad del modelo
* interpretabilidad
* robustez
* coherencia futbolística

---

# 🛡️ Prevención de leakage

## Principio fundamental

Toda variable debe existir:

```text id="jcc9om"
en el momento real de decisión
```

---

## Variables explícitamente excluidas

| Variable                   | Motivo             |
| -------------------------- | ------------------ |
| market_value_next_eur      | Información futura |
| delta_log_market_value_1y  | Leakage temporal   |
| predicted_market_value_eur | Output derivado    |
| inefficiency_score         | Output derivado    |
| rankings                   | Output derivado    |

---

## Tipos de leakage controlados

* temporal leakage
* target leakage
* leakage entre train/test
* leakage derivado de scoring

---

## Decisión metodológica

Las variables derivadas del modelo:

```text id="6qohba"
NO vuelven al dataset base
```

---

# 📈 Calidad temporal

## Estrategia de validación

El sistema utiliza:

```text id="10mbsn"
temporal validation
```

---

## Split actual

| Split | Temporadas            |
| ----- | --------------------- |
| Train | 2019-2020 → 2023-2024 |
| Test  | 2024-2025             |

---

## Justificación

El random split:

* rompe coherencia temporal
* introduce optimismo artificial
* sobreestima generalización

---

## Beneficio

La validación temporal mejora:

* realismo
* robustez
* credibilidad metodológica

---

# 📂 Controles de esquema

## Separación entre capas

El sistema separa:

| Elemento       | Directorio        |
| -------------- | ----------------- |
| Raw data       | `data/raw/`       |
| Processed data | `data/processed/` |
| Outputs        | `reports/`        |
| Artifacts      | `artifacts/`      |
| Tracking       | `mlruns/`         |
| Configuración  | `config/`         |
| Logs           | `logs/`           |

---

## Objetivo

Evitar:

* contaminación
* mezcla de responsabilidades
* pérdida de trazabilidad
* leakage accidental

---

## Decisión importante

Los outputs del modelo:

* no forman parte del dataset base
* permanecen separados
* son reproducibles

---

# ⚙️ Configuración centralizada de validaciones

## Directorio

<pre>
config/
</pre>

---

## Archivos relevantes

| Archivo       | Función                  |
| ------------- | ------------------------ |
| matching.yaml | Thresholds matching      |
| modeling.yaml | Split temporal y filtros |
| features.yaml | Features utilizadas      |
| paths.yaml    | Rutas del sistema        |

---

## Beneficios

La configuración centralizada permite:

* evitar hardcoding
* reproducir ejecuciones
* versionar cambios
* comparar experimentos
* mantener coherencia entre pipelines

---

## Relación con calidad

Los thresholds críticos quedan desacoplados del código.

Esto facilita:

* auditoría
* tuning controlado
* análisis de sensibilidad

---

# 🧪 Tracking y auditoría experimental

## Herramienta utilizada

```text id="mzuw0i"
MLflow
```

---

## Objetivo

Registrar:

* métricas
* parámetros
* configuraciones
* artefactos
* outputs

---

## Beneficios para calidad

MLflow mejora:

* trazabilidad
* reproducibilidad
* comparación entre ejecuciones
* auditoría metodológica

---

## Información registrada

### Parámetros

* features
* target
* fixed effects
* hiperparámetros
* split temporal

---

### Métricas

* RMSE
* MAE
* R²

---

### Artefactos

* modelos
* predicciones
* rankings
* feature importance

---

## Decisión metodológica

El tracking experimental permite:

```text id="pd1m8f"
reconstruir qué configuración produjo cada resultado
```

---

# 📝 Logging y trazabilidad

## Directorio

<pre>
logs/
</pre>

---

## Objetivo

Registrar información operativa de ejecución.

---

## Uso previsto

Los logs permiten almacenar:

* errores controlados
* filas procesadas
* warnings
* paths utilizados
* duración de pipelines

---

## Diferencia respecto a MLflow

| Elemento | Función                |
| -------- | ---------------------- |
| logs     | Auditoría operativa    |
| mlruns   | Auditoría experimental |

---

## Beneficio

La combinación de ambos sistemas mejora:

* debugging
* mantenimiento
* trazabilidad
* reproducibilidad

---

# ⚖️ Trade-offs metodológicos

## Cobertura vs precisión

Trade-off principal del matching.

---

## Decisión adoptada

Priorizar:

```text id="yj0tlg"
precisión y confianza
```

frente a:

```text id="okty6r"
máxima cobertura posible
```

---

## Coste

Se pierden observaciones potencialmente válidas.

---

## Beneficio

Se reduce:

* ruido
* false positives
* contaminación del modelo
* rankings erróneos

---

# 📉 Limitaciones actuales

## Cobertura de features

Todavía faltan:

* xG
* xA
* métricas avanzadas defensivas
* eventos tipo StatsBomb

---

## Dataset size

El dataset modelizable sigue siendo relativamente pequeño para:

* modelos altamente complejos
* deep learning
* segmentación extrema

---

## Matching residual

Aunque el sistema es robusto, siempre existe:

```text id="5fwz5k"
riesgo residual de matching imperfecto
```

---

## Calidad de mercado

Transfermarkt incorpora inevitablemente:

* subjetividad
* ruido contextual
* componentes no observables

---

# 🚀 Mejoras futuras previstas

## Validación avanzada

Pendiente incorporar:

* análisis de estabilidad
* robustness checks
* validación cruzada temporal avanzada

---

## Quality scoring

Posible evolución:

```python id="j0fg0g"
confidence_score =
matching_quality +
feature_completeness +
temporal_stability
```

---

## Feature engineering

Próximas mejoras:

* z-scores posicionales
* percentiles
* progression metrics
* rolling metrics

---

## Explainability

Pendiente:

* SHAP
* explicaciones individuales
* estabilidad de rankings

---

## Automatización

Posibles evoluciones:

* validaciones automáticas
* data quality monitoring
* alertas de anomalías

---

# 🧠 Conclusión

La calidad de datos representa uno de los componentes más críticos del sistema analítico desarrollado.

El proyecto prioriza:

* robustez
* consistencia temporal
* trazabilidad
* auditabilidad
* prevención de leakage
* reproducibilidad experimental

La incorporación de:

* matching validado
* configuración centralizada
* MLflow
* logging estructurado

permite construir un entorno mucho más sólido desde el punto de vista metodológico y cercano a prácticas profesionales de analytics engineering y sports analytics.

El principal reto futuro no será únicamente aumentar volumen de datos, sino incrementar:

```text id="2cl0y8"
calidad de señal predictiva manteniendo robustez metodológica
```
