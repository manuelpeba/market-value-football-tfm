# 📊 Identificación de jugadores infravalorados en el mercado de fichajes europeo

## 🧠 Descripción del proyecto

Este proyecto desarrolla un sistema analítico para mejorar la toma de decisiones en la identificación y adquisición de jugadores en el fútbol europeo.

El objetivo principal es estimar el valor de mercado esperado de los jugadores a partir de su rendimiento deportivo y detectar ineficiencias en el mercado que permitan identificar oportunidades de fichaje (estrategia *buy low, sell high*).

---

## 🎯 Problema de negocio

Los clubes de fútbol toman decisiones de fichaje basadas en:

- Scouting tradicional
- Intuición
- Métricas limitadas

Sin embargo, el mercado presenta ineficiencias debido a:

- Información incompleta
- Sesgos de percepción
- Diferencias entre ligas

👉 Este proyecto busca responder:

**¿Qué jugadores están infravalorados respecto a su rendimiento real?**

---

## 🧩 Enfoque analítico

El sistema combina:

- Econometría (modelo explicativo)
- Machine Learning (extensiones futuras)
- Feature engineering avanzado

Unidad de análisis:

```

Jugador – Temporada

```

---

## 📦 Fuentes de datos

### Transfermarkt

- Valor de mercado
- Edad
- Club
- Historial de traspasos

👉 Uso:
- Variable objetivo (`market_value_eur`)
- Base del Inefficiency Score

---

### FBref

- Métricas de rendimiento por 90 minutos
- Variables ofensivas, defensivas y de posesión

👉 Uso:
- Variables explicativas del modelo

---

## ⚠️ Problema crítico: integración de datos (FBref vs Transfermarkt)

### 🚧 Contexto

Uno de los principales retos del proyecto es la integración de ambas fuentes, ya que:

- ❌ No existe un identificador único común
- ❌ Diferencias en nombres de jugadores (idioma, acentos, formatos)
- ❌ Diferencias en nombres de clubes
- ❌ Desalineación en edad (distintas fechas de captura)
- ❌ Diferencias en granularidad temporal

👉 Este es un problema real en sports analytics y una fuente clave de error si no se trata correctamente.

---

### 🛠️ Solución implementada

Se ha desarrollado un sistema de matching robusto basado en:

#### 1. Normalización de nombres

- Eliminación de acentos
- Lowercase
- Limpieza de strings

#### 2. Matching jerárquico

- Matching exacto (nombre + edad)
- Matching validado por club
- Matching fuzzy (distancia de strings)

#### 3. Validación por edad

- Diferencia máxima permitida: 1.5 años

#### 4. Reducción del espacio de búsqueda

- Filtro por temporada
- Filtro por liga
- Filtro por edad

---

### 📈 Resultados del matching

- Match rate: **88.36%**
- Observaciones emparejadas: **20,836 / 23,580**

Distribución:

- Matching exacto → dominante
- Matching fuzzy → residual

👉 Este componente es uno de los principales aportes técnicos del proyecto.

---

## 🏗️ Pipeline de datos

```

Raw Data
↓
Ingesta (FBref + Transfermarkt)
↓
Feature Engineering
↓
Matching jugador–temporada
↓
Dataset panel
↓
Dataset de modelización

```

---

## 📊 Dataset final

### Panel completo

- Observaciones: 23,580
- Temporadas: 2019-2020 → 2024-2025
- Ligas: 7 principales ligas europeas

---

### Dataset modelizable

- Observaciones: 3,297
- Jugadores: 1,847
- Edad: 18–23 años

---

## 📈 Modelización

### Modelo base

Regresión OLS con:

- Efectos fijos por liga
- Efectos fijos por temporada
- Efectos por posición

### Variable objetivo

```

log_market_value_eur

```

---

## 💡 Inefficiency Score

Se define como:

```

residual = valor_real - valor_estimado

```

Interpretación:

- Positivo → jugador infravalorado
- Negativo → jugador sobrevalorado

---

## 📂 Estructura del proyecto

```bash

src/
data/
ingest_fbref.py
ingest_transfermarkt.py
build_fbref_features.py
build_transfermarkt_features.py
build_player_season_panel.py
build_modeling_dataset.py

data/
raw/
processed/

notebooks/
01_data_understanding.ipynb
02_modeling.ipynb

docs/
data_sources.md
data_quality.md
schema_decisions.md
modeling_decisions.md
project_status.md

```

---

## ▶️ Ejecución

### 1. Construir features FBref

```

python -m src.data.build_fbref_features

```

### 2. Construir features Transfermarkt

```

python -m src.data.build_transfermarkt_features

```

### 3. Construir panel jugador–temporada

```

python -m src.data.build_player_season_panel

```

### 4. Construir dataset de modelización

```

python -m src.data.build_modeling_dataset

```

---

## 📊 Resultados esperados

El sistema permite:

- Estimar valor de mercado esperado
- Detectar ineficiencias
- Generar rankings de jugadores infravalorados

---

## 🚀 Próximos pasos

- Modelización econométrica final
- Validación out-of-sample
- Ranking de jugadores
- Integración con dashboards / scouting tools

---

## 📚 Metodología

Se sigue CRISP-DM adaptado:

```

Business → Data → Preparation → Modeling → Evaluation → Deployment

```

---

## 🧠 Valor del proyecto

Este proyecto aporta:

- Integración robusta de datos heterogéneos
- Modelización interpretable
- Aplicación directa a decisiones de negocio
- Identificación de ineficiencias reales en el mercado

---

## 👤 Autores

- Isabel Muñoz Martín
- Laura González Macho
- Manuel Pérez Bañuls

Trabajo Fin de Máster — Data Science aplicado al fútbol profesional.

Enfoque: scouting cuantitativo, econometría aplicada y machine learning para identificación de ineficiencias de mercado.
