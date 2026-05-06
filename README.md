# ⚽ Market Value Dynamics & Inefficiency in European Football Transfers

Sistema de analítica avanzada para identificar jugadores potencialmente infravalorados en el mercado de fichajes europeo mediante econometría aplicada, machine learning y scouting cuantitativo.

---

## 🎯 Problema de negocio

El mercado de fichajes en el fútbol profesional europeo es un entorno altamente competitivo, opaco y con información imperfecta. Los clubes deben tomar decisiones de inversión bajo incertidumbre, combinando scouting tradicional, intuición experta, restricciones presupuestarias y métricas deportivas.

La hipótesis central del proyecto es:

```text
Existen jugadores cuyo rendimiento deportivo justifica un valor de mercado superior al observado.
```

Estas discrepancias pueden deberse a:

- Asimetrías de información.
- Sesgos de popularidad o reputación.
- Diferencias de visibilidad entre ligas.
- Diferencias estructurales entre clubes.
- Sobreexposición o infraexposición mediática.
- Dificultad para comparar jugadores entre contextos competitivos.

El proyecto busca convertir esta hipótesis en un sistema analítico reproducible que ayude a priorizar oportunidades de scouting.

---

## 🧠 Solución propuesta

El proyecto desarrolla un pipeline completo que integra datos de mercado y rendimiento deportivo a nivel jugador-temporada.

La solución permite:

- Construir un panel longitudinal jugador-temporada.
- Integrar Transfermarkt y FBref mediante matching validado.
- Estimar el valor de mercado esperado de cada jugador.
- Comparar valor esperado y valor observado.
- Generar rankings de jugadores potencialmente infravalorados.
- Evaluar la fiabilidad del matching y de las estimaciones.

---

## 📌 Outputs principales

### Inefficiency Score

Mide la discrepancia entre valor esperado y valor observado.

```text
inefficiency_score = predicted_log_market_value - observed_log_market_value
```

Interpretación:

```text
score > 0 → potencial infravaloración
score < 0 → potencial sobrevaloración
```

---

### Market Value Gap

Diferencia monetaria entre valor estimado y valor observado.

```text
market_value_gap_eur = predicted_market_value_eur - market_value_eur
market_value_gap_pct = market_value_gap_eur / market_value_eur
```

---

### Confidence Score

Mide la fiabilidad de la observación en función de la calidad del matching entre fuentes.

Factores considerados:

- método de matching
- diferencia de edad
- similitud de club
- confianza de integración

---

### Opportunity Score

Combina infravaloración estimada y confianza del registro.

```text
opportunity_score = inefficiency_score_z * confidence_score
```

---

## 📊 Unidad de análisis

```text
Jugador–temporada
```

Esta granularidad permite:

- Capturar evolución temporal.
- Comparar jugadores dentro y entre temporadas.
- Integrar datos de mercado y rendimiento.
- Aplicar econometría de panel.
- Construir futuros modelos de crecimiento del valor.

---

## 🌍 Cobertura actual

### Ligas

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

## 📚 Fuentes de datos

### Transfermarkt / Kaggle Player Scores

Fuente:

```text
davidcariboo/player-scores
```

Uso:

- Valor de mercado histórico.
- Edad.
- Club.
- Posición.
- Nacionalidad.
- Construcción del target `market_value_eur`.
- Transformación `log_market_value_eur`.

Resumen:

```text
Transfermarkt rows: 300,435
```

---

### FBref

Uso:

- Minutos jugados.
- Goles por 90.
- Asistencias por 90.
- Métricas ofensivas.
- Métricas defensivas.
- Métricas de progresión.
- Liga, club y temporada.

Resumen:

```text
FBref rows: 11,780
```

---

### Understat

Estado:

```text
Extensión futura
```

Uso previsto:

- xG por 90.
- xA por 90.
- Calidad ofensiva avanzada.

---

### StatsBomb Open Data

Estado:

```text
Extensión opcional
```

Uso previsto:

- Eventos avanzados.
- Presión.
- Acciones defensivas.
- Secuencias de juego.

---

## ⚙️ Arquitectura del proyecto

```text
market-value-football-tfm/

├── data/
│   ├── raw/              # datos originales no versionados
│   ├── interim/          # datos intermedios no versionados
│   ├── processed/        # datasets procesados no versionados
│   └── outputs/          # rankings, tablas y resultados analíticos
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_econometric_baseline.ipynb
│   └── 03_econometric_model.ipynb
│
├── src/
│   ├── data/
│   │   ├── build_transfermarkt_features.py
│   │   ├── build_player_season_panel.py
│   │   └── build_modeling_dataset.py
│   │
│   ├── features/
│   │   └── build_performance_features.py
│   │
│   ├── models/
│   └── visualization/
│
├── docs/
│   ├── data_sources.md
│   └── data_dictionary.md
│
├── reports/
│   ├── figures/
│   └── tables/
│
└── README.md
```

---

## 🔄 Pipeline reproducible

### 1. Construir features Transfermarkt

```bash
python -m src.data.build_transfermarkt_features
```

Output:

```text
data/processed/transfermarkt_features.parquet
```

---

### 2. Construir panel jugador-temporada

```bash
python -m src.data.build_player_season_panel
```

Output:

```text
data/processed/player_season_panel.parquet
```

Resultado actual:

```text
Rows: 11,780
Match rate: 52.47%
exact_age_club_validated: 6,107
fuzzy_age_club_validated: 74
unmatched: 5,599
```

---

### 3. Construir dataset de modelización

```bash
python -m src.data.build_modeling_dataset
```

Output:

```text
data/processed/player_season_modeling.parquet
```

Resultado actual:

```text
Rows: 6,181
Players: 3,024
```

---

### 4. Ejecutar notebooks

```text
notebooks/01_data_understanding.ipynb
notebooks/02_econometric_baseline.ipynb
notebooks/03_econometric_model.ipynb
```

---

## 🔗 Matching Transfermarkt–FBref

El matching es uno de los componentes críticos del proyecto, ya que Transfermarkt y FBref no comparten un identificador único.

El proceso utiliza:

- nombre normalizado
- temporada
- edad
- club
- fuzzy matching bajo umbrales estrictos

Parámetros principales:

```text
MAX_AGE_DIFF = 1.5
MIN_CLUB_SCORE = 70
FUZZY_THRESHOLD = 92
```

Variables de control:

- `matching_method`
- `matching_confidence`
- `age_diff`
- `club_score`

---

## 📈 Modelo econométrico final

Notebook:

```text
notebooks/03_econometric_model.ipynb
```

### Especificación

Target:

```text
log_market_value_eur
```

Variables explicativas:

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

Estimador:

```text
OLS con errores estándar robustos HC3
```

---

## 📊 Resultados actuales del modelo

Muestra final del modelo:

```text
N_obs: 1,012
N_features: 17
```

Métricas:

```text
MAE_log: 0.6363
RMSE_log: 0.7964
R2: 0.6481
Adj_R2: 0.6424
```

Interpretación:

El modelo explica aproximadamente el 64% de la variabilidad del logaritmo del valor de mercado, un resultado sólido para un modelo interpretable con una especificación parsimoniosa.

---

## 🧪 Diagnóstico econométrico

### Multicolinealidad

Valores VIF principales:

```text
age: 17.7635
minutes_played: 4.6060
goals_per90: 2.1186
assists_per90: 1.9408
```

Conclusión:

- La mayoría de variables no presentan multicolinealidad severa.
- La edad presenta VIF elevado, pero se mantiene por relevancia teórica.

---

### Condition Number

```text
Condition number: 31,293.66
```

Conclusión:

El valor elevado aconseja interpretar los coeficientes con prudencia y justifica el uso de errores robustos HC3.

---

## 🧩 Interpretación de resultados

El modelo muestra resultados coherentes con la lógica del mercado:

- `minutes_played`: efecto positivo y significativo.
- `goals_per90`: efecto positivo y significativo.
- `assists_per90`: efecto positivo y significativo.
- `age`: efecto negativo y significativo en la muestra joven.

Efectos de liga relevantes:

- Premier League: prima positiva de mercado.
- Eredivisie: descuento estructural relativo.
- Liga Portugal: descuento estructural relativo.
- Ligue 1: descuento relativo frente a la categoría base.

Desde una perspectiva de scouting, las ligas con descuento estructural pueden ofrecer oportunidades para estrategias tipo `buy low, sell high`.

---

## 📁 Outputs analíticos

Outputs previstos o generados en:

```text
data/outputs/
```

Tipos de outputs:

- ranking de jugadores infravalorados
- ranking de jugadores sobrevalorados
- tabla de métricas del modelo
- tabla de coeficientes
- resumen por liga
- resumen por posición

---

## ✅ Estado del proyecto

### Completado

- Definición del problema de negocio.
- Diseño metodológico CRISP-DM.
- Definición de unidad de análisis jugador-temporada.
- Pipeline Transfermarkt.
- Pipeline FBref.
- Matching Transfermarkt-FBref validado.
- Dataset `player_season_panel.parquet`.
- Dataset `player_season_modeling.parquet`.
- Notebook de EDA.
- Baseline econométrico.
- Modelo econométrico OLS con FE y HC3.
- Inefficiency Score corregido.
- Opportunity Score inicial.
- Rankings de mercado.
- Conclusiones académicas del modelo.

---

## 🚧 Limitaciones actuales

- El match rate actual es del 52.47%.
- La muestra final del modelo OLS es de 1,012 observaciones.
- El modelo actual usa variables deportivas básicas.
- No se ha incorporado todavía Understat.
- No hay aún validación temporal out-of-sample.
- El valor de mercado de Transfermarkt es una estimación, no un precio real de transferencia.
- Los residuos pueden capturar tanto ineficiencias como variables omitidas.

---

## 🚀 Próximos pasos

### Corto plazo

- Crear `04_machine_learning_model.ipynb`.
- Comparar OLS con Random Forest, XGBoost y LightGBM.
- Implementar validación temporal.
- Guardar outputs finales en `data/outputs/`.

### Medio plazo

- Integrar xG y xA.
- Ampliar variables de rendimiento.
- Mejorar Confidence Score.
- Construir Growth Score.

### Largo plazo

- Ranking final combinado.
- Simulación de retorno económico.
- Dashboard de scouting.
- Despliegue conceptual.
- Redacción final de memoria.

---

## 📦 Versionado sugerido

### v0.1-data-pipeline

Pipeline inicial de datos y EDA.

### v0.2-transfermarkt-fbref-matching

Integración multi-fuente y matching validado.

### v0.3-econometric-baseline

Baseline econométrico inicial.

### v0.4-econometric-inefficiency-score

Modelo OLS con fixed effects, errores robustos HC3 e Inefficiency Score operativo.

---

## 👤 Autores

- Isabel Muñoz Martín
- Laura González Macho
- Manuel Pérez Bañuls

Trabajo Fin de Máster — Data Science aplicado al fútbol profesional.

Enfoque: scouting cuantitativo, econometría aplicada y machine learning para identificación de ineficiencias de mercado.
