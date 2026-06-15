# TM.6.7b — Source Comparison Matrix

## Entregable 4 — Comparative Assessment of Advanced Football Data Providers

### Objetivo

Comparar de forma estructurada las principales fuentes de datos potencialmente utilizables para la evolución de Scouting IQ tras la congelación de FBref Advanced en la temporada 2024-2025.

El análisis considera criterios técnicos, económicos, metodológicos y operativos para determinar la viabilidad de cada proveedor como componente de la arquitectura futura.

---

# Criterios de Evaluación

## Cobertura

Capacidad para cubrir:

* ligas objetivo;
* jugadores;
* temporadas;
* competiciones.

## Profundidad Analítica

Disponibilidad de:

* xG;
* xAG;
* progresión;
* creación;
* defensa avanzada;
* métricas espaciales.

## Actualización

Frecuencia de refresh.

## Coste

Coste económico estimado para uso académico o producto.

## Riesgo

Dependencia tecnológica, estabilidad y posibles limitaciones legales.

## Integración

Facilidad de ingestión dentro del ecosistema Scouting IQ.

---

# Matriz Comparativa

| Fuente                     | Cobertura | Profundidad Analítica | Refresh | Coste | Riesgo | Integración | Valor Global |
| -------------------------- | --------- | --------------------- | ------- | ----- | ------ | ----------- | ------------ |
| FBref Standard             | 5/5       | 2/5                   | 5/5     | 5/5   | 5/5    | 5/5         | 4.5/5        |
| FBref Advanced (Histórico) | 5/5       | 5/5                   | 0/5     | 5/5   | 2/5    | 5/5         | 3.7/5        |
| Understat                  | 3/5       | 4/5                   | 5/5     | 5/5   | 4/5    | 4/5         | 4.2/5        |
| DataMB                     | 4/5       | 5/5                   | 4/5     | 3/5   | 4/5    | 3/5         | 3.9/5        |
| StatsBomb Open             | 2/5       | 5/5                   | 2/5     | 5/5   | 5/5    | 4/5         | 3.8/5        |
| Sofascore                  | 5/5       | 4/5                   | 5/5     | 5/5   | 1/5    | 2/5         | 3.7/5        |
| Fotmob                     | 5/5       | 4/5                   | 5/5     | 5/5   | 1/5    | 2/5         | 3.7/5        |
| Kaggle Alternativos        | 3/5       | 3/5                   | 2/5     | 5/5   | 3/5    | 5/5         | 3.5/5        |
| APIs Comerciales           | 5/5       | 5/5                   | 5/5     | 1/5   | 5/5    | 5/5         | 4.3/5        |

---

# Análisis por Fuente

## FBref Standard

### Fortalezas

* Actualización continua.
* Cobertura amplia.
* Integración ya operativa.
* Coste cero.

### Debilidades

* Escasa profundidad analítica.
* Sin métricas modernas de progresión.

### Papel recomendado

Current Performance Layer.

---

## FBref Advanced Histórico

### Fortalezas

* Excelente profundidad.
* Totalmente integrado.

### Debilidades

* Sin continuidad futura.

### Papel recomendado

Historical Advanced Benchmark.

---

## Understat

### Fortalezas

* Excelente capa de xG.
* Actualización continua.
* Referencia ampliamente aceptada.

### Debilidades

* Menor amplitud de métricas.

### Papel recomendado

Expected Goals Intelligence Layer.

---

## DataMB

### Fortalezas

* Sustituto más cercano de FBref Advanced.
* Amplia variedad de métricas modernas.
* Especialmente útil para Role Intelligence.

### Debilidades

* Requiere validación de licencia.
* Requiere validación de automatización.

### Papel recomendado

Advanced Performance Layer.

---

## StatsBomb Open Data

### Fortalezas

* Datos de eventos.
* Máxima riqueza analítica.
* Ideal para investigación.

### Debilidades

* Cobertura insuficiente para DSS.

### Papel recomendado

Research & Innovation Layer.

---

## Sofascore

### Fortalezas

* Cobertura enorme.
* Actualización continua.

### Debilidades

* Dependencia de scraping.
* Riesgo de cambios de plataforma.

### Papel recomendado

No utilizar como capa crítica.

---

## Fotmob

### Fortalezas

* Amplia cobertura.
* Datos modernos.

### Debilidades

* Riesgo operativo similar a Sofascore.

### Papel recomendado

No utilizar como componente estratégico principal.

---

## Kaggle Alternativos

### Fortalezas

* Gratuitos.
* Fácil integración.

### Debilidades

* Calidad heterogénea.
* Actualización irregular.

### Papel recomendado

Complemento puntual.

---

## APIs Comerciales

### Fortalezas

* Cobertura máxima.
* Actualización garantizada.
* Profundidad analítica completa.

### Debilidades

* Coste elevado.

### Papel recomendado

Escenario profesional futuro.

---

# Ranking Estratégico

## Corto Plazo

### 1. Understat

Objetivo:

```text
Recuperar xG Intelligence
```

### 2. FBref Standard

Objetivo:

```text
Mantener capa operativa actualizable
```

### 3. DataMB

Objetivo:

```text
Evaluar sustitución de FBref Advanced
```

---

# Medio Plazo

### 1. DataMB

Objetivo:

```text
Progression Intelligence
Creation Intelligence
```

### 2. Role Engine Propio

Objetivo:

```text
Reducir dependencia externa
```

---

# Largo Plazo

### 1. StatsBomb Open

Objetivo:

```text
Feature Innovation
Role Validation
Event-Based Analytics
```

### 2. APIs Comerciales

Objetivo:

```text
Escenario Enterprise
```

---

# Recomendación Final

La estrategia óptima para Scouting IQ consiste en mantener FBref Standard como fuente operativa principal, incorporar Understat como capa especializada de métricas esperadas y evaluar DataMB como reemplazo funcional de FBref Advanced.

StatsBomb Open Data debe posicionarse como entorno de investigación y desarrollo para futuras métricas propietarias, mientras que Sofascore y Fotmob no deben formar parte de la arquitectura crítica debido a su dependencia de mecanismos no oficiales de acceso.

Esta combinación ofrece el mejor equilibrio entre cobertura, sostenibilidad, coste y defensa metodológica para la evolución del proyecto entre 2026 y 2030.
