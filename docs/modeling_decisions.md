# 📊 Decisiones de modelización

<div align="center">

![Econometrics](https://img.shields.io/badge/Econometrics-OLS-green)
![Machine Learning](https://img.shields.io/badge/ML-Tuned%20XGBoost-blue)
![Scoring](https://img.shields.io/badge/Scoring-Engine-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Interpretability](https://img.shields.io/badge/Interpretability-SHAP-success)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-blue)

</div>

---

# 📑 Tabla de contenidos

- Objetivo del documento
- Filosofía de modelización
- Decisiones econométricas
- Decisiones ML
- Explainability
- Decisiones de scoring
- Opportunity Score
- Ranking Engine
- Trade-offs metodológicos
- Prevención de leakage
- Limitaciones
- Próximas decisiones

---

# 🧠 Objetivo del documento

Este documento recoge las decisiones metodológicas adoptadas durante el desarrollo del sistema analítico y su justificación desde una perspectiva:

- econométrica
- Machine Learning
- sports analytics
- scouting cuantitativo
- reproducibilidad

---

# ⚙️ Filosofía de modelización

El sistema adopta una arquitectura híbrida:

| Componente | Función |
|---|---|
| Growth OLS | benchmark interpretable |
| Tuned XGBoost | mejor modelo predictivo |
| SHAP | interpretabilidad |
| Scoring Engine | señal accionable |
| Ranking Engine | outputs de negocio |

Objetivo:

```text
maximizar utilidad de scouting
y no únicamente métricas predictivas
```

---

# 📈 Decisiones econométricas

Modelo seleccionado:

```python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
growth variables +
league FE +
position FE
```

Decisiones:

- HC3 robust covariance
- transformación logarítmica
- fixed effects
- validación temporal estricta

Resultado:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS |0.9046|0.7278|0.5255|

Rol:

```text
baseline interpretable
```

---

# 🤖 Decisiones Machine Learning

Pipeline:

```text
src/models/machine_learning/train_ml_tuned.py
```

Modelos:

- Tuned Random Forest
- Tuned XGBoost
- Tuned LightGBM
- HistGradientBoosting

Resultados:

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Tuned RF |0.9076|0.7315|0.5200|
| Tuned XGBoost |0.8753|0.7004|0.5536|
| Tuned LightGBM |0.8864|0.7162|0.5421|
| HistGradientBoosting |0.8825|0.7118|0.5462|

Decisión:

```text
Tuned XGBoost = modelo predictivo principal
```

---

# 🔍 Explainability

Métodos implementados:

Global:

- Feature importance
- SHAP summary

Local:

- SHAP por jugador
- reportes individuales

Decisión:

SHAP pasa a ser el mecanismo principal de interpretación.

---

# 💡 Decisiones sobre scoring (Sprint 5)

Objetivo:

Transformar predicciones en señales accionables para scouting.

Arquitectura:

```text
Predicciones
↓
Inefficiency Score
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Rankings
```

---

## Inefficiency Score

Definición:

```python
predicted_market_value_eur - market_value_eur
```

Rol:

- detectar infravaloración
- detectar sobrevaloración

---

## Growth Score

Variables utilizadas:

- market_value_growth_prev
- breakout_indicator
- growth_index
- career_year
- edad relativa

Objetivo:

```text
capturar potencial futuro
```

---

## Confidence Score

Componentes:

- matching_confidence
- minutos jugados
- estabilidad temporal
- completitud de features

Objetivo:

```text
reducir falsos positivos
```

---

## Opportunity Score

Implementación:

```python
(
0.5 * inefficiency_score_z
+
0.3 * growth_score_z
+
0.2 * confidence_score
)
```

Justificación:

Inefficiency mantiene mayor peso al representar la señal principal.

Growth introduce upside potencial.

Confidence penaliza casos menos fiables.

---

# 📊 Ranking Engine

Pipeline:

```text
generate_rankings.py
```

Outputs:

```text
top_undervalued_global.csv
top_undervalued_by_league.csv
top_undervalued_by_position.csv
top_high_potential.csv
top_low_risk.csv
scouting_shortlist.csv
```

Resultados actuales:

| Métrica | Valor |
|---|---:|
| Observaciones scoreadas |1138|
| Scouting targets |53|
| Alta prioridad |376|

---

# ⚖️ Trade-offs metodológicos

| Trade-off | Decisión |
|---|---|
| Interpretabilidad vs precisión | equilibrio |
| OLS vs ML | arquitectura híbrida |
| Cobertura vs matching estricto | priorizar calidad |
| Complejidad vs reproducibilidad | modularización |

---

# 🛡️ Prevención de leakage

Controles implementados:

- temporal split
- exclusión variables futuras
- separación train/test
- outputs fuera del dataset

Variables excluidas:

- market_value_next_eur
- delta_log_market_value_1y
- rankings derivados

---

# 📉 Limitaciones actuales

Pendiente:

- xG / xA
- métricas defensivas avanzadas
- eventos StatsBomb
- modelos por posición
- estabilidad longitudinal rankings

---

# 🚀 Próximas decisiones previstas

- scoring calibrado por posición
- simulación ROI
- Opportunity Score dinámico
- dashboard interactivo
- validación longitudinal

---

# 🧠 Conclusión

El proyecto ha evolucionado desde:

```text
modelo predictivo
```

hacia:

```text
sistema cuantitativo completo de scouting
```

La incorporación del Scoring Engine y Ranking Engine transforma predicciones en outputs accionables y defendibles desde una perspectiva de negocio.
