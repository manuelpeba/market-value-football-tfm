# Diseño del dataset y decisiones de modelado

## 1. Introducción

El presente documento describe las decisiones estructurales adoptadas en el diseño del dataset final, incluyendo la definición de la unidad de análisis, la selección de variables, la integración de fuentes y los trade-offs metodológicos.

Estas decisiones son críticas para garantizar la coherencia analítica del sistema y la validez de los modelos econométricos posteriores.

---

## 2. Unidad de análisis

La unidad de análisis del proyecto se define a nivel:

```

Jugador – Temporada

```

Cada fila representa el rendimiento deportivo, el contexto competitivo y el valor de mercado de un jugador en una temporada específica.

### Justificación

Esta elección responde a varias razones:

- El valor de mercado es una variable dinámica dependiente del rendimiento reciente
- Las fuentes de datos (Transfermarkt, FBref) están estructuradas por temporada
- Permite aplicar técnicas de econometría de panel
- Facilita la incorporación de efectos fijos (liga, temporada, posición)

---

## 3. Clave primaria e identificadores

### Clave primaria

La clave primaria del dataset se define como:

- `player_id`
- `season`

Esto garantiza unicidad a nivel jugador–temporada.

---

### Identificador de jugador

Se construye un identificador interno (`player_id`) debido a la ausencia de un identificador común entre fuentes.

Además, se almacenan identificadores externos:

- `fbref_id`
- `transfermarkt_id`

### Justificación

- Evita dependencia de una fuente concreta
- Permite trazabilidad y reproducibilidad
- Facilita futuras ampliaciones del dataset

---

## 4. Variable objetivo (target)

### Target principal

La variable objetivo del modelo es:

```

log_market_value_eur

```

Derivada de:

- `market_value_eur`

### Justificación

- El valor de mercado presenta una distribución altamente sesgada
- La transformación logarítmica:
  - Reduce la asimetría
  - Mejora la linealidad del modelo
  - Permite interpretación en términos relativos (%)

---

### Target secundario (dinámico)

Se define una variable de crecimiento:

```

delta_log_market_value_1y

```

Construida como:

- Diferencia del log del valor de mercado entre t y t+1

### Uso

- Modelización del crecimiento del jugador
- Construcción del Growth Score

---

## 5. Variables explicativas

Las variables se agrupan en tres bloques:

### 5.1 Variables de rendimiento

- `goals_per90`
- `assists_per90`
- `g_a_per90`
- Métricas derivadas de minutos jugados

### 5.2 Variables demográficas

- `age`
- `position`
- `position_group`

### 5.3 Variables contextuales

- `league`
- `club`
- `season`

---

## 6. Transformaciones clave

### 6.1 Variables por 90 minutos

Motivación:

- Permitir comparabilidad entre jugadores con diferente volumen de minutos
- Reducir sesgos por tiempo de juego

---

### 6.2 Transformación logarítmica

Aplicada a:

- `market_value_eur`

Motivación:

- Reducir skewness
- Mejorar estabilidad del modelo
- Evitar influencia desproporcionada de outliers

---

### 6.3 Agrupación de posiciones

Se definen cuatro grupos:

- GK (portero)
- DEF (defensa)
- MID (centrocampista)
- ATT (ataque)

Motivación:

- Reducir dimensionalidad
- Mejorar interpretabilidad
- Permitir efectos fijos por posición

---

## 7. Integración de datos (matching)

### Problema

Las fuentes utilizadas no comparten un identificador único, lo que genera:

- Ambigüedad en la unión de datos
- Riesgo de errores de matching
- Pérdida de observaciones

---

### Solución implementada

Se diseña un sistema de matching robusto basado en:

#### 1. Normalización de nombres

- Lowercase
- Eliminación de acentos
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

### Resultados

- Match rate: 88.36%
- Observaciones emparejadas: 20,836

---

## 8. Reglas de inclusión del dataset

Se incluyen únicamente observaciones que cumplen:

- Matching válido entre fuentes
- Edad entre 18 y 23 años
- Minutos jugados por encima de un umbral mínimo
- Valor de mercado disponible

---

## 9. Dataset final de modelización

Tras aplicar filtros:

- Observaciones: 3,297
- Jugadores: 1,847
- Temporadas: 2019-2020 a 2024-2025

---

## 10. Trade-offs metodológicos

Durante el diseño del dataset se han asumido los siguientes trade-offs:

### Cobertura vs precisión

- Se prioriza mantener volumen de datos
- Se controla el ruido mediante:
  - validaciones
  - variables de calidad de matching

---

### Complejidad vs interpretabilidad

- Se selecciona un modelo interpretable (OLS)
- Se limita la complejidad del feature engineering inicial

---

### Robustez vs coste computacional

- Se reduce el espacio de búsqueda en matching
- Se optimiza el pipeline sin sacrificar calidad

---

## 11. Riesgos identificados

- Matching incorrecto entre fuentes
- Cambios de club dentro de temporada
- Diferencias en naming entre datasets
- Sesgo estructural por liga
- Sesgo mediático en valor de mercado

---

## 12. Conclusión

El diseño del dataset está orientado a maximizar:

- Coherencia analítica
- Robustez metodológica
- Interpretabilidad de los resultados

Estas decisiones permiten construir un sistema sólido para la estimación del valor de mercado y la identificación de ineficiencias en el mercado de fichajes.


