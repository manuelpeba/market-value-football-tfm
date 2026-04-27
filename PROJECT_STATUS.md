# Project Status

## Fecha
Inicio del proyecto y construcción del pipeline inicial de datos. 27/04/2026

## Objetivo actual
Construir la base técnica y metodológica del dataset inicial del TFM antes de descargar o limpiar datos reales, definiendo una estructura reproducible para un panel jugador-temporada.

## Estructura inicial del proyecto
Se ha creado una estructura de repositorio orientada a reproducibilidad:

- `data/raw/`: datos originales sin modificar.
- `data/interim/`: datos validados o transformados parcialmente.
- `data/processed/`: datasets preparados para análisis/modelado.
- `src/data/`: scripts reutilizables de ingestión, validación, profiling, calidad y feature engineering.
- `config/`: configuración del proyecto.
- `reports/tables/`: salidas tabulares de análisis descriptivo.
- `docs/`: documentación metodológica y decisiones de diseño.

## Dataset objetivo
Se ha definido como unidad de análisis principal:

- `player_id`
- `season`

Cada fila representa un jugador en una temporada concreta.

## Pipeline inicial construido

### 1. Validación de esquema
Archivo:

- `src/data/validate_schema.py`

Función:
- Validar que el dataset de Transfermarkt contiene las columnas mínimas necesarias:
  - `player_name`
  - `season`
  - `age`
  - `position`
  - `club`
  - `league`
  - `market_value_eur`

### 2. Ingestión de Transfermarkt
Archivo:

- `src/data/ingest_transfermarkt.py`

Función:
- Leer un CSV bruto desde `data/raw/transfermarkt/`.
- Validar el esquema mínimo.
- Guardar el resultado en formato Parquet dentro de `data/interim/transfermarkt/`.

Comando probado:

```bash
python -m src.data.ingest_transfermarkt --input data/raw/transfermarkt/sample_transfermarkt.csv
```

Resultado:

* 3 filas.
* 7 columnas.
* Dataset generado correctamente en `data/interim/transfermarkt/transfermarkt_player_market_values.parquet`.

### 3. Profiling automático

Archivo:

* `src/data/profile_dataset.py`

Función:

* Generar un resumen descriptivo automático del dataset:

  * tipos de datos
  * nulos
  * porcentaje de nulos
  * cardinalidad
  * valores de ejemplo

Comando probado:

```bash
python -m src.data.profile_dataset --input data/interim/transfermarkt/transfermarkt_player_market_values.parquet --output reports/tables/transfermarkt_profile.csv
```

Resultado:

* Dataset con 3 filas y 7 columnas.
* Sin nulos.
* Tipos detectados correctamente.

### 4. Quality checks iniciales

Archivo:

* `src/data/quality_checks_transfermarkt.py`

Función:

* Detectar duplicados por `player_name + season`.
* Detectar valores de mercado inválidos.
* Detectar edades fuera de rango.
* Detectar valores nulos.

Comando probado:

```bash
python -m src.data.quality_checks_transfermarkt --input data/interim/transfermarkt/transfermarkt_player_market_values.parquet
```

Resultado:

* Duplicados: 0.
* Valores de mercado inválidos: 0.
* Edades inválidas: 0.
* Nulos: 0.

### 5. Feature engineering inicial

Archivo:

* `src/data/build_transfermarkt_features.py`

Función:

* Crear primeras variables derivadas:

  * `player_id`
  * `season_start_year`
  * `position_group`
  * `log_market_value_eur`

Estas variables son necesarias para avanzar hacia el dataset de modelización.

## Decisiones metodológicas tomadas

1. La unidad de análisis será jugador-temporada.
2. El valor de mercado se modelará preferentemente en escala logarítmica.
3. Se mantendrá separación estricta entre datos brutos, intermedios y procesados.
4. `player_name` no se considera identificador fiable; se requiere `player_id`.
5. La variable `season` se mantendrá como string, pero se creará `season_start_year` para análisis temporal.
6. La posición detallada se agrupará en `position_group`: GK, DEF, MID, ATT.
7. Transfermarkt será la fuente principal para el target de valor de mercado.
8. FBref será la fuente principal futura para variables explicativas de rendimiento.

## Próximo paso

Construir el pipeline de ingestión de FBref y diseñar el proceso de matching entre Transfermarkt y FBref, que será una de las partes críticas del proyecto.
EOF
