# Project Status

## Fecha
28-04-2026 - Construcción del pipeline completo de ingestión e integración inicial de datos (Transfermarkt + FBref)

---

## Objetivo actual

Desarrollar un sistema reproducible de construcción del dataset jugador-temporada, integrando múltiples fuentes de datos y estableciendo las bases para el modelado del valor de mercado.

---

## Estado del proyecto

El proyecto ha evolucionado desde la definición de la estructura y el schema objetivo hacia la construcción de un pipeline funcional completo que permite:

- Ingestar datos desde múltiples fuentes
- Validar su estructura
- Analizar su calidad
- Generar variables derivadas
- Integrar datasets en un panel jugador-temporada

---

# 🧱 1. Pipeline de datos construido

## 1.1 Ingestión de Transfermarkt

Archivo:

- `src/data/ingest_transfermarkt.py`

Funcionalidad:

- Lectura de datos brutos desde `data/raw/transfermarkt/`
- Validación de esquema mínimo
- Conversión a formato Parquet
- Almacenamiento en `data/interim/transfermarkt/`

Variables clave:

- `player_name`
- `season`
- `age`
- `position`
- `club`
- `league`
- `market_value_eur`

Rol en el sistema:

- Fuente principal del target (valor de mercado)

---

## 1.2 Profiling de datos

Archivo:

- `src/data/profile_dataset.py`

Funcionalidad:

- Generación automática de informe descriptivo:
  - Tipos de variables
  - Valores nulos
  - Cardinalidad
  - Ejemplos de valores

Output:

- `reports/tables/transfermarkt_profile.csv`

Conclusión:

- Dataset estructuralmente válido
- Sin valores nulos en la muestra inicial

---

## 1.3 Control de calidad de datos

Archivo:

- `src/data/quality_checks_transfermarkt.py`

Checks implementados:

- Duplicados por `player_name + season`
- Valores de mercado inválidos (≤ 0)
- Edades fuera de rango
- Valores nulos

Resultado:

```text
Duplicates: 0
Invalid market values: 0
Invalid ages: 0
Missing values: 0
```

Interpretación:

* Dataset limpio a nivel estructural
* Aún no evaluado a nivel semántico

---

## 1.4 Feature engineering inicial (Transfermarkt)

Archivo:

* `src/data/build_transfermarkt_features.py`

Variables generadas:

* `player_id` (hash de nombre, solución temporal)
* `season_start_year`
* `position_group` (GK / DEF / MID / ATT)
* `log_market_value_eur`

Decisiones clave:

* Transformación logarítmica del valor de mercado para reducir asimetría
* Reducción de dimensionalidad de posición
* Creación de identificador interno de jugador

Output:

* `data/processed/transfermarkt_features.parquet`

---

# 📊 2. Ingestión de FBref

## 2.1 Ingestión de datos de rendimiento

Archivo:

* `src/data/ingest_fbref.py`

Funcionalidad:

* Lectura de datos desde `data/raw/fbref/`
* Validación de esquema
* Conversión a Parquet

Variables clave:

* `minutes_played`
* `goals_per90`
* `assists_per90`
* `shots_per90`
* `progressive_passes_per90`
* `progressive_carries_per90`
* `tackles_per90`
* `interceptions_per90`

Rol en el sistema:

* Fuente principal de variables explicativas

Output:

* `data/interim/fbref/fbref_player_standard.parquet`

---

# 🔗 3. Integración de datasets (Matching v0)

## 3.1 Construcción del player-season panel

Archivo:

* `src/data/build_player_season_panel.py`

Funcionalidad:

* Integración de Transfermarkt y FBref
* Creación de dataset final a nivel jugador-temporada

Claves utilizadas para el join:

```text
normalized_name + season + age
```

Preprocesamiento:

* Normalización de nombres (`lowercase + sin tildes`)
* Homogeneización de columnas

---

## 3.2 Variables generadas

* `matching_status`
* `matching_confidence`

Valores posibles:

```text
matched
unmatched_transfermarkt
unmatched_fbref
```

---

## 3.3 Resultados

```text
Rows: 3
Columns: 26
```

Distribución:

```text
matched: 3
unmatched_transfermarkt: 0
unmatched_fbref: 0
```

Interpretación:

* Matching perfecto en dataset de prueba (100%)
* Validación del pipeline completo de integración

Output:

* `data/processed/player_season_panel.parquet`

---

# ⚠️ 4. Limitaciones del matching v0

El enfoque actual presenta limitaciones importantes:

## Problemas potenciales:

* Variaciones en nombres (acentos, abreviaturas)
* Jugadores con nombres idénticos
* Diferencias entre fuentes
* Cambios de club dentro de la temporada
* Inconsistencias en edad

## Conclusión:

El matching implementado es una **baseline funcional**, pero no escalable a datos reales.

---

# 🧠 5. Decisiones metodológicas clave

1. La unidad de análisis es jugador-temporada
2. Transfermarkt define el target del modelo
3. FBref define las variables explicativas
4. Se separan claramente las fases:

   * raw → ingestión
   * interim → validación
   * processed → modelado
5. Se introduce el concepto de:

   * `matching_confidence`
6. Se prioriza trazabilidad y reproducibilidad del pipeline

---

# 🚀 6. Estado actual del proyecto

Se ha completado el primer ciclo completo de CRISP-DM:

✔ Comprensión de datos
✔ Preparación inicial de datos
✔ Integración multi-fuente

El proyecto ya dispone de un:

```text
Dataset integrado jugador-temporada listo para análisis
```

---

# 🎯 7. Próximos pasos

## Corto plazo

* Mejorar el matching (fuzzy matching + scoring)
* Incorporar Understat (xG, xA)
* Ampliar cobertura de datos

## Medio plazo

* Feature engineering avanzado:

  * índices de rendimiento
  * normalización por posición y liga
* Construcción del modelo de valor de mercado

## Largo plazo

* Modelo de crecimiento (Growth Score)
* Construcción del Inefficiency Score
* Generación de rankings de jugadores

---

## Conclusión

Se ha establecido una base técnica sólida y reproducible que permite evolucionar el sistema hacia fases más avanzadas de modelado y análisis, manteniendo coherencia metodológica y alineación con los objetivos de negocio del proyecto.
