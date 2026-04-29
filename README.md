# ⚽ Market Value Dynamics & Inefficiency in European Football Transfers

Sistema de analítica avanzada para identificar jugadores infravalorados en el mercado de fichajes europeo mediante econometría y machine learning.

---

## 🎯 Problema de negocio

El mercado de fichajes en el fútbol profesional presenta ineficiencias derivadas de:

- Asimetrías de información
- Sesgos en la evaluación del talento
- Diferencias estructurales entre ligas

Esto genera oportunidades de inversión para clubes capaces de detectar discrepancias entre:

```text
Valor de mercado observado vs Valor real del jugador
```

---

## 🧠 Solución propuesta

Se desarrolla un sistema analítico que permite:

* Estimar el valor de mercado esperado de un jugador
* Predecir su evolución futura
* Detectar oportunidades de fichaje

### 🎯 Outputs clave

* **Inefficiency Score** → jugadores infravalorados
* **Growth Score** → potencial de revalorización
* **Confidence Score** → fiabilidad de la estimación

---

## 📊 Unidad de análisis

```text
Jugador – Temporada (player-season)
```

Dataset estructurado como panel longitudinal, adecuado para:

* Modelos econométricos
* Machine Learning supervisado
* Análisis de evolución temporal

---

## 📊 Fuentes de datos

### Transfermarkt

* Valor de mercado (target)
* Edad, club, posición
* Historial de fichajes

### FBref

* Métricas de rendimiento por 90 minutos
* Variables ofensivas, defensivas y de posesión

### (Próximamente)

* Understat → xG, xA
* StatsBomb → eventos avanzados

---

## ⚙️ Arquitectura del proyecto

```
data/
  raw/        → datos originales
  interim/    → datos validados
  processed/  → dataset final para modelado

src/
  data/       → ingestión y validación
  features/   → feature engineering
  models/     → modelos (en desarrollo)

notebooks/
  → análisis exploratorio (EDA)

docs/
  → decisiones metodológicas
```

---

## 🔄 Pipeline de datos

### 1. Ingestión

* Transfermarkt
* FBref

### 2. Validación

* Esquema
* Calidad de datos (nulos, duplicados)

### 3. Integración

* Matching multi-fuente (player-season)

### 4. Feature engineering

#### Normalización contextual (clave)

```text
z-score por:
- posición
- liga
```

#### Índices construidos

* finishing_index
* playmaking_index
* progression_index
* defensive_index

---

## 📈 Estado del proyecto

### ✅ Completado

* Pipeline de datos reproducible
* Integración multi-fuente
* Feature engineering avanzado
* Dataset listo para modelado
* EDA inicial

### ⚠️ Limitaciones actuales

* Dataset de prueba reducido
* Matching simplificado (v0)
* Falta de métricas avanzadas (xG, eventos)

---

## 🚀 Próximos pasos

### Corto plazo

* Modelo baseline (regresión)
* Evaluación de variables

### Medio plazo

* Modelos ML (Random Forest, XGBoost)
* Variables no lineales

### Largo plazo

* Growth model
* Inefficiency Score
* Ranking final de jugadores

---

## 📦 Versionado

### v0.1-data-pipeline

Primer snapshot estable del sistema:

* Pipeline de datos completo
* Feature engineering implementado
* Dataset listo para modelado

---

## 🧪 Reproducibilidad

Ejemplo de ejecución:

```bash
python -m src.data.ingest_transfermarkt
python -m src.data.ingest_fbref
python -m src.data.build_player_season_panel
python -m src.features.build_performance_features
```

---

## 🧠 Enfoque metodológico

El proyecto sigue una adaptación de **CRISP-DM**:

1. Comprensión de negocio
2. Comprensión de datos
3. Preparación de datos
4. Modelado
5. Evaluación
6. Despliegue

---

## 👤 Autores

Isabel Muñoz Martín
Laura González Macho
Manuel Pérez Bañuls

TFM - Data Science aplicado al fútbol
Enfoque: scouting cuantitativo + econometría + machine learning

