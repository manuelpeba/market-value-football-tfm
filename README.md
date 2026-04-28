# Market Value Dynamics and Inefficiency in European Football Transfers

TFM - Máster en Data Science

---

## 🎯 Objetivo del proyecto

El objetivo de este proyecto es desarrollar un sistema analítico que permita identificar jugadores infravalorados en el mercado de fichajes europeo, mediante la estimación del valor de mercado esperado y su evolución futura.

El sistema busca apoyar la toma de decisiones en departamentos deportivos, permitiendo:

- Identificar oportunidades de fichaje (buy low)
- Optimizar inversiones en transferencias
- Reducir el riesgo económico en el mercado

---

## 🧠 Enfoque metodológico

El proyecto sigue una adaptación del framework **CRISP-DM**:

1. Comprensión del negocio
2. Comprensión de los datos
3. Preparación de los datos
4. Modelado
5. Evaluación
6. Despliegue (conceptual)

---

## 🧱 Unidad de análisis

```text
Jugador - Temporada (player-season)
```

Cada fila del dataset representa:

* Un jugador
* En una temporada concreta
* Con variables de mercado, rendimiento y contexto

---

## 📊 Fuentes de datos

### Transfermarkt

* Valor de mercado (target)
* Edad, club, posición
* Historial de mercado

### FBref

* Métricas de rendimiento por 90 minutos
* Variables ofensivas, defensivas y de posesión

### (Futuro)

* Understat → xG, xA
* StatsBomb Open Data → eventos avanzados

---

## ⚙️ Arquitectura del proyecto

```text
data/
  raw/        → datos originales
  interim/    → datos validados
  processed/  → datasets listos para modelado

src/
  data/       → ingestión, validación, matching
  features/   → feature engineering
  models/     → modelos econométricos / ML

notebooks/
  → análisis exploratorio (EDA)

reports/
  → outputs tabulares y resultados

docs/
  → decisiones metodológicas
```

---

## 🔄 Pipeline de datos implementado

### 1. Ingestión de datos

Scripts:

* `ingest_transfermarkt.py`
* `ingest_fbref.py`

Funcionalidad:

* Lectura de datos brutos
* Validación de esquema
* Conversión a formato Parquet

---

### 2. Validación y calidad de datos

Scripts:

* `validate_schema.py`
* `quality_checks_transfermarkt.py`
* `profile_dataset.py`

Incluye:

* Validación de columnas
* Detección de nulos
* Duplicados
* Valores inválidos
* Profiling automático

---

### 3. Feature engineering (Transfermarkt)

Script:

* `build_transfermarkt_features.py`

Variables creadas:

* `player_id` (identificador interno)
* `season_start_year`
* `position_group` (GK / DEF / MID / ATT)
* `log_market_value_eur`

---

### 4. Integración de fuentes (Matching v0)

Script:

* `build_player_season_panel.py`

Join basado en:

```text
normalized_name + season + age
```

Output:

```text
player_season_panel.parquet
```

Incluye:

* `matching_status`
* `matching_confidence`

---

### 5. Feature engineering de rendimiento

Script:

* `build_performance_features.py`

Incluye:

#### Normalización (clave del proyecto)

```text
z-score por:
- position_group
- league
```

#### Variables generadas

* `z_goals_per90`
* `z_assists_per90`
* `z_progressive_passes_per90`
* ...

#### Índices de scouting

* `finishing_index`
* `playmaking_index`
* `progression_index`
* `defensive_index`

#### Variables de control

* `minutes_bucket`
* `is_low_minutes`

Output final:

```text
data/processed/player_season_features.parquet
```

---

## 📈 Estado actual del proyecto

Se ha completado:

* ✔ Pipeline completo de datos
* ✔ Integración multi-fuente (Transfermarkt + FBref)
* ✔ Matching inicial (v0)
* ✔ Feature engineering avanzado
* ✔ Dataset listo para modelado
* ✔ Análisis exploratorio inicial (EDA)

---

## 📊 Análisis exploratorio (EDA)

Notebook:

* `notebooks/01_data_understanding.ipynb`

Incluye:

* Validación del dataset
* Distribución del target
* Análisis por posición y liga
* Evaluación de minutos jugados
* Revisión de métricas de rendimiento
* Validación de índices construidos

---

## ⚠️ Limitaciones actuales

* Dataset de prueba reducido
* Matching simplificado (v0)
* Falta de variables avanzadas (xG, eventos)
* Sin ajuste aún por fuerza de liga

---

## 🚀 Próximos pasos

### Corto plazo

* Mejorar matching (fuzzy matching + scoring)
* Incorporar Understat (xG, xA)

### Medio plazo

* Modelo baseline de valor de mercado
* Incorporación de variables categóricas (liga, posición)
* Modelado no lineal (edad²)

### Largo plazo

* Modelo de crecimiento (Growth Score)
* Cálculo del Inefficiency Score
* Ranking de jugadores infravalorados

---

## 🎯 Output esperado

El sistema generará:

```text
Inefficiency Score → jugadores infravalorados
Growth Score → potencial de revalorización
Confidence Score → fiabilidad del modelo
```

---

## 🧪 Reproducibilidad

Ejemplo de ejecución del pipeline:

```bash
python -m src.data.ingest_transfermarkt ...
python -m src.data.ingest_fbref ...
python -m src.data.build_player_season_panel ...
python -m src.features.build_performance_features ...
```

---

## 👤 Autores

Isabel Muñoz Martín
Laura González Macho
Manuel Pérez Bañuls

TFM - Data Science aplicado al fútbol
Enfoque: scouting cuantitativo + econometría + machine learning

