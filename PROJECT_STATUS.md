# Project Status

## Fecha
28-04-2026 - Pipeline completo + Feature Engineering + EDA

---

## Objetivo actual

Desarrollar un sistema reproducible de construcción del dataset jugador-temporada, integrando múltiples fuentes de datos y estableciendo las bases para el modelado del valor de mercado.

---

## Estado del proyecto

El proyecto ha evolucionado desde la definición del esquema objetivo hacia la construcción de un sistema completo de preparación de datos que permite:

- Ingestar datos desde múltiples fuentes
- Validar su estructura
- Analizar su calidad
- Generar variables derivadas
- Integrar datasets en un panel jugador-temporada
- Construir variables explicativas orientadas a modelado
- Validar el dataset mediante análisis exploratorio (EDA)

---

# 🧱 1. Pipeline de datos construido

## 1.1 Ingestión de Transfermarkt

Archivo:
- `src/data/ingest_transfermarkt.py`

Funcionalidad:
- Lectura de datos brutos
- Validación de esquema
- Conversión a Parquet

Rol:
- Fuente del target (`market_value_eur`)

---

## 1.2 Profiling de datos

Archivo:
- `src/data/profile_dataset.py`

Funcionalidad:
- Análisis descriptivo automático
- Detección de nulos, tipos y cardinalidad

---

## 1.3 Control de calidad

Archivo:
- `src/data/quality_checks_transfermarkt.py`

Checks:
- Duplicados
- Valores inválidos
- Nulos

Resultado:
- Dataset limpio a nivel estructural

---

## 1.4 Feature engineering inicial (Transfermarkt)

Archivo:
- `src/data/build_transfermarkt_features.py`

Variables:
- `player_id`
- `season_start_year`
- `position_group`
- `log_market_value_eur`

---

# 📊 2. Ingestión de FBref

Archivo:
- `src/data/ingest_fbref.py`

Variables:
- Métricas por 90 minutos
- Variables ofensivas, defensivas y de progresión

Rol:
- Fuente principal de variables explicativas

---

# 🔗 3. Integración de datos (Matching v0)

Archivo:
- `src/data/build_player_season_panel.py`

Join:
```text
normalized_name + season + age
```

Variables:

* `matching_status`
* `matching_confidence`

Resultado:

* Matching 100% en dataset de prueba

Output:

* `player_season_panel.parquet`

---

# 📦 4. Feature engineering avanzado

## 4.1 Script principal

Archivo:

* `src/features/build_performance_features.py`

---

## 4.2 Normalización contextual

Se aplica:

```text
z-score por:
- position_group
- league
```

Objetivo:

* Comparabilidad entre jugadores
* Eliminación de sesgos por contexto

---

## 4.3 Variables generadas

### Variables normalizadas

* `z_goals_per90`
* `z_assists_per90`
* `z_shots_per90`
* `z_progressive_passes_per90`
* `z_progressive_carries_per90`
* `z_tackles_per90`
* `z_interceptions_per90`

---

### Índices de rendimiento

* `finishing_index`
* `playmaking_index`
* `progression_index`
* `defensive_index`

---

### Variables de control

* `minutes_bucket`
* `is_low_minutes`

---

## 4.4 Output final

```text
data/processed/player_season_features.parquet
```

---

## 4.5 Observación importante

En el dataset de prueba:

```text
std ≈ 0 en índices
```

Interpretación:

* Limitación del tamaño de muestra
* Comportamiento esperado, no error metodológico

---

# 📊 5. Análisis exploratorio (EDA)

## 5.1 Notebook

Archivo:

* `notebooks/01_data_understanding.ipynb`

---

## 5.2 Objetivo

* Validar dataset integrado
* Analizar calidad de datos
* Explorar distribución de variables
* Verificar coherencia del feature engineering

---

## 5.3 Resultados principales

### Calidad de datos

* Sin valores nulos
* Sin duplicados
* Dataset consistente

---

### Matching

* `matching_status = matched`
* `matching_confidence = 1.0`

---

### Target

* Alta dispersión en `market_value_eur`
* Transformación log adecuada

---

### Variables de rendimiento

* Variabilidad entre perfiles
* Necesidad de normalización confirmada

---

### Índices

* Valores constantes debido a muestra pequeña

---

## 5.4 Conclusión EDA

* Pipeline validado
* Dataset coherente
* Base lista para modelado

Limitación:

* Dataset de prueba no permite inferencia real

---

# ⚠️ 6. Limitaciones actuales

* Tamaño reducido del dataset
* Matching simplificado (v0)
* Falta de variables avanzadas (xG, eventos)
* Sin ajuste por fuerza de liga
* Baja variabilidad en features derivadas

---

# 🧠 7. Decisiones metodológicas clave

1. Unidad de análisis: jugador-temporada
2. Uso de logaritmo en variable objetivo
3. Separación estricta de capas de datos
4. Normalización por contexto competitivo
5. Construcción de índices interpretables
6. Introducción de métricas de calidad de matching

---

# 🚀 8. Estado actual del proyecto

El proyecto ha completado:

✔ Data ingestion
✔ Data validation
✔ Data integration
✔ Feature engineering
✔ Data understanding (EDA)

El sistema dispone de un:

```text
Dataset listo para modelado econométrico
```

---

# 📈 9. Próximo paso

Construcción de modelo baseline:

```text
log_market_value ~ performance + controls
```

Objetivo:

* Estimar valor esperado
* Detectar ineficiencias de mercado

---

# 🎯 10. Próximos pasos

## Corto plazo

* Modelo baseline
* Evaluación de variables
* Mejora del matching

## Medio plazo

* Variables categóricas (liga, posición)
* Modelos no lineales
* Understat (xG, xA)

## Largo plazo

* Growth model
* Inefficiency Score
* Ranking de jugadores

---

## Conclusión

Se ha construido una base técnica sólida, reproducible y alineada con el objetivo del proyecto, permitiendo avanzar hacia la fase de modelado con un dataset estructurado, validado y enriquecido mediante variables de rendimiento contextualizadas.
