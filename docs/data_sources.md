# Fuentes de datos

Este documento describe las fuentes de datos utilizadas en el TFM, su función dentro del sistema analítico, las decisiones metodológicas adoptadas y los principales riesgos asociados.

El objetivo del proyecto es construir un panel jugador-temporada que permita estimar el valor de mercado esperado de futbolistas profesionales e identificar posibles ineficiencias en el mercado de fichajes europeo.

---

## 1. Resumen de fuentes

| Fuente | Tipo de información | Uso en el proyecto | Estado |
|---|---|---|---|
| Transfermarkt / Kaggle Player Scores | Mercado, edad, club, posición, histórico de valor | Target y contexto de mercado | Integrada |
| FBref | Rendimiento deportivo por jugador y temporada | Variables explicativas | Integrada |
| Understat | xG, xA y métricas ofensivas avanzadas | Enriquecimiento futuro | Pendiente |
| StatsBomb Open Data | Eventos avanzados | Extensión opcional | Pendiente |

---

## 2. Transfermarkt / Kaggle Player Scores

### 2.1 Descripción

Transfermarkt es la fuente principal para la dimensión de mercado del proyecto. En lugar de realizar scraping directo de Transfermarkt, se utiliza el dataset estructurado de Kaggle:

```text
davidcariboo/player-scores
```

Esta decisión mejora la reproducibilidad del proyecto y reduce la fragilidad técnica asociada al scraping directo.

---

### 2.2 Uso en el proyecto

Transfermarkt se utiliza para obtener:

- valor de mercado histórico
- edad
- club
- posición
- nacionalidad
- identificador de jugador cuando está disponible
- información temporal de valoración

Variables principales generadas:

```text
market_value_eur
log_market_value_eur
market_value_prev_eur
market_value_next_eur
market_value_growth_1y
delta_log_market_value_1y
```

---

### 2.3 Construcción de features Transfermarkt

Script principal:

```text
src/data/build_transfermarkt_features.py
```

Proceso:

1. Carga de `player_valuations.csv`.
2. Carga de `players.csv`.
3. Conversión de fechas a formato temporal.
4. Asignación de cada valoración a una temporada deportiva.
5. Agregación a nivel jugador-temporada.
6. Selección del último valor disponible dentro de cada temporada.
7. Enriquecimiento con información maestra del jugador.
8. Cálculo de `log_market_value_eur`.
9. Generación de variables dinámicas.
10. Normalización de nombres para facilitar el matching con FBref.

Output:

```text
data/processed/transfermarkt_features.parquet
```

Resumen actual:

```text
Rows Transfermarkt: 300,435
```

---

### 2.4 Justificación metodológica

El valor de mercado de Transfermarkt se utiliza como proxy del valor observado de mercado. Aunque no representa necesariamente el precio real de una transferencia, es una referencia ampliamente utilizada y permite construir una variable objetivo homogénea y disponible de forma histórica.

Ventajas:

- Cobertura amplia.
- Histórico de valoraciones.
- Información de contexto del jugador.
- Adecuado para modelización jugador-temporada.
- Reproducible mediante dataset estructurado.

Limitaciones:

- Es una estimación, no un precio de transacción.
- Puede incorporar sesgos de reputación, club, liga, nacionalidad y exposición mediática.
- Puede reaccionar de forma no inmediata al rendimiento deportivo.
- Puede incluir expectativas futuras no observadas en las variables deportivas.

---

## 3. FBref

### 3.1 Descripción

FBref es la fuente principal de rendimiento deportivo. Aporta métricas estandarizadas por jugador, temporada y competición, incluyendo variables ofensivas, defensivas y de progresión.

---

### 3.2 Uso en el proyecto

FBref se utiliza para construir las variables explicativas del modelo.

Variables principales:

```text
minutes_played
goals_per90
assists_per90
shots_per90
progressive_passes_per90
progressive_carries_per90
tackles_per90
interceptions_per90
```

También aporta:

```text
player_name
season
league
club
position_group
```

Resumen actual:

```text
Rows FBref: 11,780
Leagues: Big 5 + Liga Portugal + Eredivisie
Seasons: 2020-2021 a 2023-2024
```

---

### 3.3 Uso en modelización

En el modelo econométrico final se utilizan las siguientes variables FBref:

```text
minutes_played
goals_per90
assists_per90
```

Estas variables se seleccionan por:

- interpretabilidad
- disponibilidad suficiente
- relación directa con valor de mercado
- menor riesgo de multicolinealidad frente a variables agregadas

---

### 3.4 Riesgos y limitaciones

Riesgos:

- Cambios de formato en tablas fuente.
- Diferencias en nombres de jugadores respecto a Transfermarkt.
- Diferencias en nombres de clubes.
- Cobertura variable según liga y temporada.
- Posibles duplicidades en jugadores con varios clubes en una temporada.

Mitigación:

- Normalización de nombres.
- Validación por temporada.
- Validación por edad.
- Validación por club.
- Fuzzy matching controlado.

---

## 4. Integración Transfermarkt–FBref

### 4.1 Problema

Transfermarkt y FBref no comparten un identificador único común. Esto obliga a construir un proceso de matching probabilístico y validado.

El problema es especialmente relevante en casos de:

- jugadores homónimos
- nombres abreviados
- acentos y caracteres especiales
- cambios de club
- diferencias de edad entre fuentes
- traducciones o variantes en nombres de clubes

Ejemplos problemáticos detectados:

```text
Antony
João Pedro
Diego López
```

---

### 4.2 Script de integración

Archivo:

```text
src/data/build_player_season_panel.py
```

Criterios de matching:

- nombre normalizado
- temporada
- edad
- club
- similitud fuzzy

Parámetros actuales:

```text
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

---

### 4.3 Resultados actuales del matching

```text
FBref rows: 11,780
Transfermarkt rows: 300,435
Panel rows: 11,780
Match rate: 52.47%
```

Distribución:

```text
exact_age_club_validated: 6,107
fuzzy_age_club_validated: 74
unmatched / NaN: 5,599
```

Output:

```text
data/processed/player_season_panel.parquet
```

---

### 4.4 Variables de trazabilidad del matching

| Variable | Descripción |
|---|---|
| `matching_method` | Método mediante el cual se validó el cruce |
| `matching_confidence` | Confianza del matching |
| `age_diff` | Diferencia de edad entre fuentes |
| `club_score` | Score de similitud entre clubes |

Estas variables se utilizan posteriormente para construir el `Confidence Score`.

---

## 5. Dataset final de modelización

Archivo generado:

```text
data/processed/player_season_modeling.parquet
```

Script:

```text
src/data/build_modeling_dataset.py
```

Resultado actual:

```text
Rows: 6,181
Players: 3,024
```

Uso:

- EDA.
- Baseline econométrico.
- Modelo OLS final.
- Construcción de Inefficiency Score.

---

## 6. Understat

### 6.1 Descripción

Understat proporciona métricas avanzadas de calidad ofensiva, especialmente expected goals y expected assists.

Variables previstas:

```text
xg_per90
xa_per90
```

---

### 6.2 Uso previsto

Understat se incorporará en fases posteriores para mejorar la medición de rendimiento ofensivo real, reduciendo la dependencia de goles y asistencias observadas.

Valor esperado:

- Mejor captación de calidad de ocasiones.
- Menor ruido que goles observados.
- Mejor evaluación de jugadores con buen rendimiento subyacente pero bajo output.

---

### 6.3 Estado actual

```text
Pendiente de integración
```

Motivo:

La prioridad actual ha sido construir un pipeline reproducible Transfermarkt-FBref, validar el matching y generar un primer modelo econométrico interpretable.

---

## 7. StatsBomb Open Data

### 7.1 Descripción

StatsBomb Open Data ofrece datos de eventos avanzados, pero con cobertura limitada en términos de competiciones y temporadas.

---

### 7.2 Uso potencial

Variables y conceptos potenciales:

- presión
- acciones defensivas
- secuencias ofensivas
- pases bajo presión
- calidad de recepción
- eventos espaciales

---

### 7.3 Decisión metodológica

StatsBomb no se utiliza como fuente core del dataset final porque su cobertura no es homogénea para las ligas y temporadas objetivo.

Uso recomendado:

```text
Extensión en submuestras o análisis complementario, no fuente principal.
```

---

## 8. Decisión sobre scraping directo de Transfermarkt

Se descarta el scraping directo complejo de Transfermarkt como fuente principal por los siguientes motivos:

- Fragilidad ante cambios HTML.
- Mayor coste de mantenimiento.
- Riesgo de bloqueos.
- Menor reproducibilidad.
- Mayor complejidad para replicación académica.

Se prioriza el dataset estructurado de Kaggle por:

- reproducibilidad
- trazabilidad
- facilidad de descarga
- estabilidad
- adecuación al alcance del TFM

No obstante, se mantiene como línea futura el scraping específico para actualización puntual de jugadores, ligas o temporadas concretas.

---

## 9. Relación entre fuentes y variables del modelo

| Componente | Fuente principal | Variables |
|---|---|---|
| Target | Transfermarkt | `market_value_eur`, `log_market_value_eur` |
| Rendimiento básico | FBref | `minutes_played`, `goals_per90`, `assists_per90` |
| Contexto competitivo | FBref | `league`, `season`, `club`, `position_group` |
| Matching | Interna | `matching_method`, `age_diff`, `club_score` |
| Calidad ofensiva avanzada | Understat | `xg_per90`, `xa_per90` |
| Eventos avanzados | StatsBomb | pendiente |

---

## 10. Limitaciones de datos actuales

- Match rate Transfermarkt-FBref del 52.47%.
- Pérdida de observaciones al filtrar registros modelizables.
- Ausencia de identificador común universal.
- Falta de variables contractuales.
- Falta de información salarial.
- Falta de lesiones e internacionalidades.
- Understat aún no integrado.
- Transfermarkt mide valor estimado, no precio real de transferencia.

---

## 11. Riesgos metodológicos

### 11.1 Variable objetivo

El valor de mercado puede reflejar:

- rendimiento
- potencial
- reputación
- club
- liga
- contrato
- agente
- narrativa mediática
- expectativas futuras

Por tanto, el modelo no identifica ineficiencias puras, sino desviaciones entre valor observado y valor esperado condicional a las variables incluidas.

---

### 11.2 Matching

Errores de matching pueden contaminar el target o las variables explicativas.

Mitigación:

- Validación por edad.
- Validación por club.
- Fuzzy matching restrictivo.
- Registro explícito de método de matching.
- Uso de `Confidence Score`.

---

### 11.3 Cobertura

El dataset cubre bien las principales ligas europeas seleccionadas, pero puede infrarrepresentar jugadores con baja disponibilidad de minutos, cambios de club complejos o nombres ambiguos.

---

## 12. Próximos pasos sobre fuentes

### Corto plazo

- Revisar unmatched cases para mejorar cobertura.
- Guardar tablas de calidad de matching.
- Documentar ejemplos de matching correcto e incorrecto.

### Medio plazo

- Integrar Understat.
- Incorporar xG y xA al modelo.
- Añadir métricas avanzadas adicionales de FBref.

### Largo plazo

- Evaluar fuentes contractuales.
- Evaluar fuentes de lesiones.
- Evaluar internacionalidades.
- Construir Growth Score con valor futuro.

---

## 13. Estado actual

El sistema ya dispone de una base de datos integrada y modelizable que permite estimar el valor de mercado esperado y construir rankings iniciales de oportunidades.

La prioridad inmediata ya no es únicamente la recopilación de datos, sino la mejora del poder predictivo, la validación temporal y la ampliación de variables explicativas.
