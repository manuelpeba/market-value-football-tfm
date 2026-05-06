# Project Status

## Fecha
06-05-2026 — Pipeline multi-fuente + matching validado + dataset de modelización + EDA + baseline econométrico + modelo OLS con Fixed Effects + Inefficiency Score

---

## Objetivo actual

Desarrollar un sistema reproducible de analítica avanzada para identificar jugadores potencialmente infravalorados en el mercado de fichajes europeo, integrando datos de mercado y rendimiento deportivo en un panel jugador-temporada y estimando el valor de mercado esperado mediante modelos econométricos interpretables.

El proyecto se encuentra actualmente en la fase de **Modelización** dentro de una adaptación de CRISP-DM, habiendo completado las fases de comprensión de negocio, comprensión de datos, preparación de datos, integración multi-fuente, análisis exploratorio y construcción del primer modelo econométrico final.

---

## 1. Resumen ejecutivo del estado del proyecto

El proyecto ha avanzado desde una fase inicial de diseño metodológico y construcción del pipeline hacia una primera versión funcional del sistema analítico completo.

Actualmente se dispone de:

- Un pipeline reproducible de datos Transfermarkt y FBref.
- Un proceso de matching jugador-temporada con validación por nombre, temporada, edad y club.
- Un dataset integrado `player_season_panel.parquet`.
- Un dataset final de modelización `player_season_modeling.parquet`.
- Un notebook de comprensión de datos `01_data_understanding.ipynb`.
- Un notebook de baseline econométrico `02_econometric_baseline.ipynb`.
- Un notebook econométrico final `03_econometric_model.ipynb`.
- Un primer modelo OLS con efectos fijos por liga, temporada y posición.
- Un sistema inicial de scoring basado en residuos: `Inefficiency Score`, `Confidence Score` y `Opportunity Score`.
- Rankings iniciales de jugadores infravalorados y sobrevalorados.

---

## 2. Objetivo de negocio

El objetivo de negocio del TFM es mejorar la toma de decisiones en scouting y fichajes dentro del fútbol profesional europeo mediante la identificación sistemática de oportunidades de mercado.

La hipótesis central del proyecto es:

```text
Existen jugadores cuyo rendimiento deportivo justifica un valor de mercado superior al observado en Transfermarkt.
```

El sistema analítico busca apoyar decisiones como:

- Identificación de jugadores potencialmente infravalorados.
- Priorización de targets de fichaje.
- Reducción del riesgo económico en decisiones de inversión.
- Comparación objetiva entre jugadores de distintas ligas y posiciones.
- Complemento cuantitativo al scouting tradicional.

---

## 3. Objetivo analítico

El objetivo analítico es estimar el valor de mercado esperado de los jugadores a partir de variables de rendimiento, edad y contexto competitivo, para posteriormente comparar dicha estimación con el valor observado.

La lógica analítica es:

```text
Valor esperado estimado > Valor observado  → Posible infravaloración
Valor esperado estimado < Valor observado  → Posible sobrevaloración
```

El output principal del modelo econométrico es el residuo transformado en un score interpretable:

```text
Inefficiency Score = predicted_log_market_value - observed_log_market_value
```

---

## 4. Metodología

El proyecto sigue una adaptación de CRISP-DM:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment conceptual
7. Puesta en valor

La fase actual corresponde a **Modeling / Evaluation inicial**, con un modelo econométrico interpretable que servirá como baseline robusto antes de avanzar hacia modelos de Machine Learning.

---

## 5. Unidad de análisis

La unidad de análisis es:

```text
Jugador–temporada
```

Esta decisión permite:

- Capturar la evolución temporal de los jugadores.
- Integrar datos de mercado y rendimiento deportivo.
- Construir un panel longitudinal.
- Modelizar dinámicas de valor de mercado.
- Generar rankings comparables por temporada, liga y posición.

---

## 6. Fuentes de datos utilizadas

### 6.1 Transfermarkt / Kaggle Player Scores

Fuente principal de mercado.

Uso:

- `market_value_eur`
- `log_market_value_eur`
- edad
- posición
- club
- temporada
- histórico de valores de mercado

Dataset bruto principal:

```text
davidcariboo/player-scores
```

Dataset procesado:

```text
data/processed/transfermarkt_features.parquet
```

Resumen procesado:

```text
Rows Transfermarkt: 300,435
```

---

### 6.2 FBref

Fuente principal de rendimiento deportivo.

Uso:

- minutos jugados
- goles por 90
- asistencias por 90
- métricas ofensivas
- métricas defensivas
- métricas de progresión
- liga
- club
- temporada

Dataset integrado inicial:

```text
Rows FBref: 11,780
```

---

### 6.3 Understat

Fuente prevista para próximas iteraciones.

Uso futuro:

- `xg_per90`
- `xa_per90`
- métricas de calidad ofensiva

Estado actual:

```text
No incorporada todavía al modelo econométrico final.
```

---

### 6.4 StatsBomb Open Data

Fuente opcional futura.

Uso potencial:

- eventos avanzados
- presión
- secuencias
- acciones defensivas

Estado actual:

```text
No forma parte del dataset core por limitaciones de cobertura.
```

---

## 7. Ligas y temporadas consideradas

### Ligas objetivo

- Premier League
- LaLiga
- Bundesliga
- Serie A
- Ligue 1
- Eredivisie
- Liga Portugal

### Temporadas principales

- 2020-2021
- 2021-2022
- 2022-2023
- 2023-2024

---

## 8. Pipeline de datos implementado

### 8.1 Descarga y procesamiento de Transfermarkt

Archivo principal:

```text
src/data/build_transfermarkt_features.py
```

Funcionalidad:

- Carga de datos históricos de valor de mercado.
- Conversión de fechas a temporadas deportivas.
- Agregación a nivel jugador-temporada.
- Selección del último valor disponible en cada temporada.
- Construcción de `market_value_eur`.
- Transformación logarítmica `log_market_value_eur`.
- Generación de identificadores y campos normalizados.

Output:

```text
data/processed/transfermarkt_features.parquet
```

---

### 8.2 Integración FBref + Transfermarkt

Archivo principal:

```text
src/data/build_player_season_panel.py
```

Objetivo:

Construir un panel jugador-temporada integrando métricas de rendimiento de FBref con valor de mercado de Transfermarkt.

El matching se realiza mediante un enfoque multi-criterio:

- nombre normalizado
- temporada
- edad
- club
- similitud fuzzy controlada

Parámetros principales:

```text
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

Resultados actuales:

```text
FBref rows: 11,780
Transfermarkt rows: 300,435
Panel rows: 11,780
Match rate: 52.47%
```

Distribución del matching:

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

### 8.3 Construcción del dataset de modelización

Archivo principal:

```text
src/data/build_modeling_dataset.py
```

Objetivo:

Filtrar el panel integrado para generar un dataset final apto para modelización econométrica.

Criterios principales:

- Observaciones con valor de mercado conocido.
- Variables esenciales no nulas.
- Registros con matching validado.
- Variables compatibles con el modelo OLS.

Resultado:

```text
Dataset: player_season_modeling.parquet
Rows: 6,181
Players: 3,024
```

Output:

```text
data/processed/player_season_modeling.parquet
```

---

## 9. Problemas encontrados y decisiones técnicas

### 9.1 Matching incorrecto por homónimos

Problema:

Algunos jugadores con nombres iguales o similares generaban cruces incorrectos.

Ejemplos detectados:

- Antony
- João Pedro
- Diego López

Solución implementada:

- Matching por nombre normalizado.
- Validación por temporada.
- Validación por edad.
- Validación por club.
- Fuzzy matching solo bajo umbrales estrictos.
- Variables explícitas de trazabilidad del matching.

---

### 9.2 Problemas de dtype en pandas

Problema:

Asignaciones de texto sobre columnas inicializadas como `float64` generaban errores con `ArrowStringArray`.

Solución:

Inicializar columnas destinadas a contener strings con `dtype=object` antes de asignar valores textuales.

---

### 9.3 Multicolinealidad en variables ofensivas

Problema:

Variables como `goals_per90`, `assists_per90` y agregados tipo `g_a_per90` capturaban información redundante.

Solución:

Eliminar variables agregadas redundantes del modelo final y mantener variables interpretables:

- `goals_per90`
- `assists_per90`
- `minutes_played`
- `age`

---

### 9.4 Interpretación del residuo

Problema:

Inicialmente existía riesgo de confusión entre residuo econométrico e Inefficiency Score.

Decisión final:

```text
residual_observed_minus_predicted = observed_log_market_value - predicted_log_market_value
inefficiency_score = predicted_log_market_value - observed_log_market_value
```

Interpretación:

```text
inefficiency_score > 0 → jugador potencialmente infravalorado
inefficiency_score < 0 → jugador potencialmente sobrevalorado
```

---

## 10. Notebooks implementados

### 10.1 `01_data_understanding.ipynb`

Objetivo:

Comprensión inicial del dataset integrado.

Incluye:

- carga del dataset
- dimensiones
- tipos de datos
- missing values
- análisis del target
- distribución del valor de mercado
- análisis por liga
- análisis por posición
- validación inicial de coherencia

Estado:

```text
Completado
```

---

### 10.2 `02_econometric_baseline.ipynb`

Objetivo:

Construir un primer baseline econométrico sobre `log_market_value_eur`.

Incluye:

- selección inicial de variables
- modelo OLS básico
- interpretación preliminar
- identificación de problemas de multicolinealidad
- primeras pruebas de ranking de infravaloración

Estado:

```text
Completado
```

---

### 10.3 `03_econometric_model.ipynb`

Objetivo:

Construir el modelo econométrico final interpretable con fixed effects y errores robustos.

Incluye:

- introducción metodológica
- preparación de datos
- selección de variables
- encoding de efectos fijos
- OLS con HC3 robust standard errors
- evaluación del modelo
- diagnóstico de multicolinealidad
- análisis de residuos
- construcción del Inefficiency Score
- construcción del Confidence Score
- construcción del Opportunity Score
- ranking de infravalorados
- ranking de sobrevalorados
- conclusiones académicas y de negocio

Estado:

```text
Completado
```

---

## 11. Modelo econométrico final

### 11.1 Especificación

Variable dependiente:

```text
log_market_value_eur
```

Variables explicativas base:

```text
minutes_played
goals_per90
assists_per90
age
```

Fixed Effects:

```text
league FE
season FE
position_group FE
```

Implementación:

```text
pd.get_dummies(..., drop_first=True)
```

Estimador:

```text
OLS
```

Errores estándar:

```text
HC3 robust standard errors
```

---

### 11.2 Resultados del modelo

Muestra final usada en el modelo:

```text
N_obs: 1,012
N_features: 17
```

Métricas:

```text
MAE_log: 0.6363
RMSE_log: 0.7964
R2: 0.6481
Adjusted R2: 0.6424
```

Interpretación:

El modelo explica aproximadamente el 64% de la variabilidad del logaritmo del valor de mercado, lo que constituye un resultado sólido para una especificación econométrica interpretable y parsimoniosa.

---

### 11.3 Principales coeficientes

Variables deportivas:

```text
minutes_played: positivo y significativo
goals_per90: positivo y significativo
assists_per90: positivo y significativo
age: negativo y significativo
```

Interpretación:

- Los minutos jugados capturan exposición competitiva y confianza del entrenador.
- Los goles y asistencias por 90 capturan producción ofensiva, muy premiada por el mercado.
- La edad tiene efecto negativo en esta muestra de jugadores jóvenes, consistente con la prima de potencial futuro.

Efectos de liga relevantes:

```text
Premier League: positivo y significativo
Eredivisie: negativo y significativo
Liga Portugal: negativo y significativo
Ligue 1: negativo y significativo
```

Interpretación:

- La Premier League presenta una prima estructural de mercado.
- Eredivisie y Liga Portugal muestran descuentos relativos, lo que puede ser relevante para scouting de oportunidades.

---

## 12. Diagnóstico econométrico

### 12.1 Multicolinealidad

El VIF muestra valores generalmente aceptables para la mayoría de variables.

Valores relevantes:

```text
age: 17.7635
minutes_played: 4.6060
goals_per90: 2.1186
assists_per90: 1.9408
```

Interpretación:

- No se detecta multicolinealidad severa generalizada.
- La edad presenta VIF elevado, pero se mantiene por su importancia teórica en valoración de jugadores.

---

### 12.2 Condition Number

Resultado:

```text
Condition number: 31,293.66
```

Interpretación:

El valor elevado puede deberse a diferencias de escala entre variables y a la inclusión de dummies. Se justifica el uso de errores robustos HC3 y la interpretación prudente de coeficientes.

---

### 12.3 Residuos

Conclusiones del análisis gráfico:

- Relación clara entre valor observado y predicho en escala logarítmica.
- Residuos aproximadamente centrados en cero.
- Dispersión esperable en los extremos del mercado.
- No se observa un patrón estructural extremo en residuos vs predicciones.

---

## 13. Inefficiency Score y rankings

### 13.1 Definición final

```text
inefficiency_score = predicted_log_market_value - observed_log_market_value
```

Interpretación:

```text
Inefficiency Score > 0 → potencial infravaloración
Inefficiency Score < 0 → potencial sobrevaloración
```

---

### 13.2 Gap monetario

Definición:

```text
market_value_gap_eur = predicted_market_value_eur - market_value_eur
market_value_gap_pct = market_value_gap_eur / market_value_eur
```

Interpretación:

```text
Gap positivo → valor estimado superior al valor observado
Gap negativo → valor observado superior al valor estimado
```

---

### 13.3 Confidence Score

Se utiliza como medida de fiabilidad asociada principalmente a la calidad del matching.

Variables consideradas:

- `matching_method`
- `matching_confidence`
- `age_diff`
- `club_score`

Estado actual:

En el modelo final, la mayoría de observaciones utilizadas presentan matching exacto validado, por lo que el `confidence_score` se concentra cerca de 1.

---

### 13.4 Opportunity Score

Definición conceptual:

```text
opportunity_score = inefficiency_score_z * confidence_score
```

Uso:

Priorizar jugadores con alta infravaloración estimada y alta confianza de integración.

---

## 14. Resultados de negocio iniciales

El modelo permite generar dos rankings principales:

### Ranking de jugadores potencialmente infravalorados

Características detectadas:

- jugadores jóvenes
- valores observados relativamente bajos
- valor esperado notablemente superior al valor observado
- presencia de ligas y clubes con menor exposición relativa

Uso recomendado:

```text
Lista inicial de scouting cuantitativo para revisión cualitativa posterior.
```

---

### Ranking de jugadores potencialmente sobrevalorados

Características detectadas:

- jugadores pertenecientes a clubes de alta reputación
- valores observados muy superiores al valor estimado por rendimiento básico
- fuerte componente de reputación, narrativa, potencial percibido o prima de club

Uso recomendado:

```text
Identificación de casos donde el mercado puede estar incorporando factores no observados por el modelo.
```

---

## 15. Limitaciones actuales

### 15.1 Datos

- El match rate actual es del 52.47%.
- No existe identificador común entre Transfermarkt y FBref.
- La muestra final del modelo econométrico es de 1,012 observaciones.
- Understat todavía no está integrado.
- StatsBomb no se usa como fuente core.

---

### 15.2 Modelo

- Modelo estimado in-sample.
- No existe todavía validación temporal out-of-sample.
- Variables deportivas aún básicas.
- No se incluyen variables contractuales.
- No se incluyen salarios.
- No se incluyen lesiones.
- No se incluyen internacionalidades.
- No se incluyen métricas avanzadas como xG/xA en el modelo final.

---

### 15.3 Interpretación

- Transfermarkt no es precio real de transferencia, sino estimación de mercado.
- Los residuos no deben interpretarse automáticamente como ineficiencias puras.
- Parte del residuo puede capturar variables omitidas: reputación, potencial, club, agente, contrato, nacionalidad o exposición mediática.

---

## 16. Decisiones metodológicas clave consolidadas

1. Unidad de análisis jugador-temporada.
2. Uso de `log_market_value_eur` como target principal.
3. Integración Transfermarkt + FBref mediante matching validado.
4. Uso de OLS como modelo econométrico interpretable.
5. Inclusión de fixed effects por liga, temporada y posición.
6. Uso de errores estándar robustos HC3.
7. Construcción del Inefficiency Score como diferencia entre valor esperado y observado.
8. Separación entre modelo explicativo, scoring e interpretación de negocio.
9. Interpretación del sistema como herramienta de apoyo al scouting, no como sustituto del criterio experto.

---

## 17. Estado actual del proyecto

### Completado

- Definición del problema de negocio.
- Definición de objetivos analíticos.
- Diseño metodológico CRISP-DM.
- Definición de unidad de análisis jugador-temporada.
- Selección de fuentes de datos.
- Descarga y procesamiento de Transfermarkt.
- Integración de FBref.
- Matching robusto Transfermarkt-FBref.
- Construcción de `player_season_panel.parquet`.
- Construcción de `player_season_modeling.parquet`.
- EDA inicial.
- Baseline econométrico.
- Modelo econométrico final OLS + FE + HC3.
- Diagnóstico de multicolinealidad.
- Análisis de residuos.
- Inefficiency Score corregido.
- Opportunity Score inicial.
- Rankings de infravalorados y sobrevalorados.
- Conclusiones académicas incorporadas al notebook 3.

---

## 18. Próximo paso exacto

El siguiente paso recomendado es avanzar hacia:

```text
04_machine_learning_model.ipynb
```

Objetivo:

Comparar el modelo econométrico interpretable con modelos supervisados no lineales.

Modelos candidatos:

- Random Forest Regressor
- Gradient Boosting
- XGBoost
- LightGBM

Evaluación recomendada:

- MAE log
- RMSE log
- R²
- validación temporal
- comparación contra OLS
- análisis de feature importance
- análisis de estabilidad del ranking

---

## 19. Roadmap actualizado

### Corto plazo

- Guardar outputs analíticos en `data/outputs/`.
- Versionar notebooks 02 y 03.
- Crear notebook de Machine Learning.
- Definir validación temporal.
- Añadir tablas finales para memoria.

### Medio plazo

- Incorporar variables avanzadas de FBref.
- Integrar Understat para xG y xA.
- Mejorar Confidence Score.
- Evaluar modelos ML.
- Construir ranking final combinando:

```text
Inefficiency Score + Growth Score + Confidence Score
```

### Largo plazo

- Construir Growth Model.
- Simular retorno económico.
- Crear dashboard de scouting.
- Preparar despliegue conceptual.
- Redactar memoria final.

---

## 20. Conclusión

El proyecto ha alcanzado un hito relevante: ya no se limita a la preparación de datos, sino que dispone de un modelo econométrico funcional, interpretable y conectado directamente con el objetivo de negocio.

El sistema actual permite estimar el valor de mercado esperado de jugadores, comparar dicha estimación con el valor observado y generar rankings iniciales de oportunidades de mercado.

Aunque todavía existen limitaciones relevantes, especialmente en validación temporal, variables omitidas y cobertura de fuentes avanzadas, la base metodológica y técnica es sólida para continuar hacia modelos de Machine Learning, Growth Score y una solución final orientada a scouting profesional.
