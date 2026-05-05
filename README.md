# ⚽ Market Value Dynamics & Inefficiency in European Football Transfers

Sistema de analítica avanzada para identificar jugadores infravalorados en el mercado de fichajes europeo mediante econometría y machine learning.

---

## 🎯 Problema de negocio

El mercado de fichajes en el fútbol profesional presenta ineficiencias derivadas de:

- Asimetrías de información
- Sesgos en la evaluación del talento
- Diferencias estructurales entre ligas
- Diferencias en visibilidad mediática y competitiva entre campeonatos

Esto genera oportunidades de inversión para clubes capaces de detectar discrepancias entre:

```text
Valor de mercado observado vs Valor de mercado esperado
```

---

## 🧠 Solución propuesta

Se desarrolla un sistema analítico que permite:

* Estimar el valor de mercado esperado de un jugador
* Comparar el valor estimado con el valor observado en Transfermarkt
* Identificar jugadores potencialmente infravalorados
* Priorizar oportunidades de scouting e inversión

### Outputs clave

* **Inefficiency Score** → grado de infravaloración estimada
* **Growth Score** → potencial de revalorización futura
* **Confidence Score** → fiabilidad de la estimación y calidad del matching

---

## 📊 Unidad de análisis

```text
Jugador – Temporada (player-season)
```

El dataset se estructura como panel longitudinal, adecuado para:

* Modelos econométricos
* Machine Learning supervisado
* Análisis de evolución temporal del valor de mercado
* Comparación entre jugadores, ligas y posiciones

---

## 📊 Fuentes de datos

### Transfermarkt / Kaggle Player Scores

Fuente utilizada:

```text
davidcariboo/player-scores
```

Uso principal:

* Valor de mercado histórico
* Edad
* Posición
* Club
* Nacionalidad
* Construcción del target `market_value_eur`
* Transformación logarítmica `log_market_value_eur`

Dataset procesado generado:

```text
data/processed/transfermarkt_features.parquet
```

Resumen actual:

```text
Rows: 300,435
Players: 39,361
Seasons: 1999–2025
```

### FBref

Uso principal:

* Métricas de rendimiento por 90 minutos
* Variables ofensivas, defensivas y de progresión
* Base principal de variables explicativas para modelado

Dataset construido:

```text
data/processed/fbref_features.parquet
```

Resumen:

```text
Rows: ~11,800
Players: ~5,000
Seasons: 2020–2023
Leagues: Big 5 + Portugal + Eredivisie
```

### Futuras extensiones

* Understat → xG, xA
* StatsBomb Open Data → eventos avanzados en submuestras

---

## ⚙️ Arquitectura del proyecto

```text
data/
  raw/        → datos originales no versionados
  interim/    → datos intermedios no versionados
  processed/  → datasets procesados no versionados
  outputs/    → outputs analíticos no versionados

src/
  data/       → ingestión, validación e integración
  features/   → feature engineering
  models/     → modelización

scripts/
  → automatización de descarga de datos

notebooks/
  → EDA y modelización exploratoria

docs/
  → documentación metodológica y fuentes de datos

reports/
  → resultados y outputs finales
```

---

## 🔄 Pipeline de datos

### 1. Descarga reproducible de datos

El dataset de Transfermarkt se descarga mediante Kaggle API:

```bash
bash scripts/download_data.sh
```

Esto genera los CSV originales en:

```text
data/raw/transfermarkt/kaggle_player_scores/
```

Los datos raw no se versionan en GitHub por tamaño y reproducibilidad.

---

### 2. Construcción de features Transfermarkt

```bash
python src/data/build_transfermarkt_features.py
```

Este script:

* carga `player_valuations.csv`
* carga `players.csv`
* asigna cada valoración a una temporada deportiva
* agrega el valor de mercado a nivel jugador-temporada
* selecciona el último valor disponible de cada temporada
* calcula `log_market_value_eur`
* genera variables dinámicas de valor de mercado
* normaliza nombres para futuro matching con FBref

Output:

```text
data/processed/transfermarkt_features.parquet
```

---

### 3. Integración con FBref

Siguiente paso del pipeline:

```text
FBref + Transfermarkt → player_season_modeling.parquet
```

El matching se plantea mediante:

* `player_name_norm`
* `season`
* validación auxiliar por edad
* fuzzy matching en casos no exactos
* métricas de calidad:

  * `matching_status`
  * `matching_confidence`

---

### 4. Feature engineering deportivo

Se construyen variables normalizadas y agregadas:

```text
z-score por:
- posición
- liga
```

Índices principales:

* `finishing_index`
* `playmaking_index`
* `progression_index`
* `defensive_index`

---

## 📈 Estado del proyecto

### Completado

* Pipeline FBref construido
* Dataset de rendimiento generado
* Descarga reproducible del dataset Transfermarkt vía Kaggle API
* Construcción de `transfermarkt_features.parquet`
* Target histórico válido a nivel jugador-temporada
* Documentación inicial de fuentes de datos
* Estructura preparada para matching multi-fuente

### En progreso

* Matching robusto Transfermarkt–FBref
* Construcción de `player_season_modeling.parquet`
* Modelo econométrico baseline

### Limitaciones actuales

* Transfermarkt y FBref no comparten identificador único
* El matching requiere normalización y validación probabilística
* El dataset final de modelización aún depende de la calidad del cruce entre fuentes
* Understat y StatsBomb quedan como extensiones futuras

---

## 🚀 Próximos pasos

### Corto plazo

* Construir `build_player_season_panel.py` v2
* Implementar matching exacto + fuzzy matching
* Generar `player_season_modeling.parquet`
* Validar cobertura del join

### Medio plazo

* Modelo econométrico baseline:

  ```text
  log_market_value_eur ~ performance + age + position + league + season
  ```
* Cálculo inicial de residuos
* Definición de `Inefficiency Score`

### Largo plazo

* Modelos ML: Random Forest, XGBoost / LightGBM
* Growth model
* Ranking final de jugadores infravalorados
* Dashboard o informe operativo para scouting

---

## 📦 Versionado

### v0.1-data-pipeline

Primer snapshot estable del sistema:

* Pipeline inicial de datos
* Feature engineering de rendimiento
* EDA inicial

### v0.2-transfermarkt-kaggle-pipeline

Estado actual:

* Descarga reproducible de Transfermarkt desde Kaggle
* Procesamiento histórico de valores de mercado
* Construcción de panel jugador-temporada para Transfermarkt
* Preparación del target para modelización econométrica

---

## 🧪 Reproducibilidad

### 1. Descargar datos

```bash
bash scripts/download_data.sh
```

### 2. Construir features Transfermarkt

```bash
python src/data/build_transfermarkt_features.py
```

### 3. Próximamente

```bash
python src/data/build_player_season_panel.py
python src/features/build_performance_features.py
python src/models/baseline_econometric_model.py
```

---

## 🧠 Enfoque metodológico

El proyecto sigue una adaptación de CRISP-DM:

1. Comprensión de negocio
2. Comprensión de datos
3. Preparación de datos
4. Modelización
5. Evaluación
6. Despliegue
7. Puesta en valor

La decisión de utilizar un dataset estructurado de Transfermarkt vía Kaggle responde a criterios de reproducibilidad, trazabilidad y reducción del riesgo técnico asociado al scraping directo.

---

## 👤 Autores

Isabel Muñoz Martín
Laura González Macho
Manuel Pérez Bañuls

TFM - Data Science aplicado al fútbol
Enfoque: scouting cuantitativo + econometría + machine learning
