# TM.6.7b — Advanced Performance Data Strategy

## Entregable 2 — Matriz de Sustitución de FBref Advanced

### Objetivo

Identificar qué métricas avanzadas utilizadas actualmente por Scouting IQ dependen de FBref Advanced y definir una estrategia de sustitución sostenible para el período 2026-2030.

Este análisis permite cuantificar el impacto de la congelación de FBref Advanced en 2024-2025 y diseñar una hoja de ruta para preservar las capacidades analíticas del DSS.

---

# Situación Actual

Actualmente Scouting IQ utiliza métricas procedentes de:

```text
FBref Standard
+
FBref Advanced
+
Transfermarkt
```

La capa avanzada proporciona una parte significativa del valor analítico del sistema:

* Role Discovery Engine
* Role Similarity Engine
* Performance Intelligence
* Recruitment Intelligence
* Feature Engineering avanzado
* XGBoost v13B

La congelación de FBref Advanced implica que estas métricas dejan de actualizarse después de la temporada 2024-2025.

---

# Matriz de Sustitución

| Grupo Funcional | Métrica Actual              | Fuente Actual  | Impacto DSS | Alternativa Recomendada | Prioridad |
| --------------- | --------------------------- | -------------- | ----------- | ----------------------- | --------- |
| Finishing       | xG                          | FBref Advanced | Muy Alta    | Understat               | Crítica   |
| Finishing       | xAG                         | FBref Advanced | Muy Alta    | Understat               | Crítica   |
| Finishing       | npxG                        | FBref Advanced | Muy Alta    | Understat               | Crítica   |
| Passing         | Progressive Passes          | FBref Advanced | Alta        | DataMB                  | Alta      |
| Carrying        | Progressive Carries         | FBref Advanced | Alta        | DataMB                  | Alta      |
| Creation        | Key Passes                  | FBref Advanced | Alta        | DataMB                  | Alta      |
| Creation        | Shot Creating Actions (SCA) | FBref Advanced | Muy Alta    | DataMB                  | Alta      |
| Creation        | Goal Creating Actions (GCA) | FBref Advanced | Muy Alta    | DataMB                  | Alta      |
| Defence         | Tackles                     | FBref Advanced | Media       | DataMB                  | Media     |
| Defence         | Interceptions               | FBref Advanced | Media       | DataMB                  | Media     |
| Defence         | Defensive Actions           | FBref Advanced | Alta        | DataMB                  | Media     |
| Possession      | Touches avanzados           | FBref Advanced | Media       | DataMB                  | Baja      |
| Possession      | Carries avanzados           | FBref Advanced | Alta        | DataMB                  | Alta      |
| Aerial          | Aerials Won                 | FBref Advanced | Media       | DataMB                  | Baja      |

---

# Impacto sobre Modelos Existentes

## Econometría

Impacto esperado:

```text
BAJO
```

Motivo:

Los modelos econométricos se entrenan sobre datasets históricos cerrados.

La pérdida de actualización no afecta:

* OLS
* Fixed Effects
* Random Effects

porque ya utilizan observaciones históricas consolidadas.

---

## XGBoost v13B

Impacto esperado:

```text
MEDIO
```

Las variables críticas son:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas métricas ya existen y permanecen disponibles para entrenamiento histórico.

El problema aparece únicamente en futuras actualizaciones del producto.

---

## Role Discovery Engine

Impacto esperado:

```text
ALTO
```

Dependencias directas:

```text
Progressive Passes
Progressive Carries
Creation Metrics
Defensive Activity
```

Es el componente más afectado.

---

## Recruitment Intelligence

Impacto esperado:

```text
ALTO
```

La calidad del scouting depende directamente de:

```text
Creation
Progression
Defensive Output
```

---

# Clasificación de Riesgo

## Riesgo Crítico

Métricas cuya desaparición degradaría significativamente el producto:

```text
xG
xAG
npxG

Progressive Passes
Progressive Carries

SCA
GCA
```

---

## Riesgo Medio

```text
Defensive Actions
Interceptions
Tackles
```

Pueden aproximarse mediante proxies.

---

## Riesgo Bajo

```text
Touches
Aerials
Possession Metrics
```

No son críticas para la propuesta de valor actual.

---

# Estrategia Recomendada

## Fase 1 — Sustitución inmediata

### Understat

Incorporar:

```text
xG
xAG
npxG
```

Beneficios:

* coste cero;
* actualización continua;
* alta defensa académica.

Resultado:

```text
Expected Goals Layer
```

---

## Fase 2 — Recuperación de progresión y creación

Evaluar:

```text
DataMB
```

Objetivo:

Recuperar:

```text
Progressive Passes
Progressive Carries

Key Passes

SCA
GCA
```

Resultado:

```text
Advanced Creation Layer
```

---

## Fase 3 — Métricas propietarias

Desarrollar:

```text
Role Engine 2.0
```

Generando:

```text
Scouting IQ Progression Index

Scouting IQ Creation Index

Scouting IQ Defensive Activity Index

Scouting IQ Role Fit Score
```

Objetivo:

Reducir dependencia de proveedores externos.

---

# Arquitectura Objetivo 2026-2030

Transfermarkt

↓

Market Layer

FBref Standard

↓

Current Performance Layer

Understat

↓

Expected Goals Layer

DataMB

↓

Advanced Creation Layer

Role Engine Propio

↓

Scouting Intelligence Layer

StatsBomb Open

↓

Research & Innovation Layer

---

# Gap Analysis

## Cobertura Actual

```text
FBref Advanced
```

Aporta aproximadamente:

```text
100%
```

de las métricas avanzadas utilizadas por TM.6.

---

## Cobertura tras congelación

```text
FBref Standard
```

Mantiene aproximadamente:

```text
35%-40%
```

de la capacidad analítica.

---

## Cobertura Objetivo

```text
FBref Standard
+
Understat
+
DataMB
```

Permitiría recuperar:

```text
80%-90%
```

de la funcionalidad original.

---

# Conclusión

La desaparición de FBref Advanced como fuente actualizable no compromete la validez académica del TFM ni los modelos históricos ya entrenados. Sin embargo, sí afecta a la evolución futura del DSS y especialmente a los módulos de Role Intelligence y Recruitment Intelligence.

La estrategia recomendada consiste en sustituir la capa de Expected Goals mediante Understat, recuperar las métricas de progresión y creación mediante DataMB y continuar desarrollando métricas propietarias derivadas del Role Engine para reducir progresivamente la dependencia de proveedores externos.

Esta estrategia permite preservar entre el 80% y el 90% de la capacidad analítica actual de Scouting IQ manteniendo un coste operativo reducido y una elevada sostenibilidad a largo plazo.
