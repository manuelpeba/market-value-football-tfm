# TM.6.7b — Advanced Performance Data Strategy

## Entregable 1 — Auditoría Estratégica de Fuentes de Datos de Rendimiento Avanzado

### Objetivo

Evaluar las alternativas disponibles para garantizar la sostenibilidad de la capa de rendimiento avanzado de Scouting IQ tras la congelación de las métricas avanzadas históricas de FBref en la temporada 2024-2025.

La auditoría considera criterios técnicos, económicos, operativos y metodológicos con el objetivo de definir una arquitectura de datos robusta para el período 2026-2030.

---

# Resumen Ejecutivo

La auditoría concluye que ninguna fuente individual reemplaza completamente la combinación actual de FBref Standard + FBref Advanced.

La estrategia recomendada es una arquitectura multicapa:

* Transfermarkt → Inteligencia de mercado.
* FBref Standard → Rendimiento actual.
* Understat → xG Intelligence Layer.
* Role Engine propio → Métricas propietarias.
* StatsBomb Open → Investigación y desarrollo.
* DataMB → Potencial sustituto futuro de FBref Advanced.

Esta arquitectura minimiza el riesgo de dependencia de proveedor único y mejora la resiliencia del producto.

---

# Comparativa Estratégica

| Fuente                   | Cobertura Ligas | Cobertura Temporal | Métricas Avanzadas | Refresh   | Coste      | Riesgo Dependencia | Integración  |
| ------------------------ | --------------- | ------------------ | ------------------ | --------- | ---------- | ------------------ | ------------ |
| FBref Standard           | Muy Alta        | 2019-Actualidad    | Baja               | Alta      | Gratuito   | Bajo               | Muy Fácil    |
| FBref Advanced Histórico | Muy Alta        | 2017-2025          | Muy Alta           | Congelado | Gratuito   | Alto               | Ya Integrado |
| Understat                | Top-5 ligas     | Actualidad         | Media-Alta         | Alta      | Gratuito   | Bajo               | Fácil        |
| DataMB                   | Muy Alta        | Actualidad         | Muy Alta           | Alta      | Freemium   | Medio              | Media        |
| StatsBomb Open           | Baja            | Variable           | Muy Alta           | Baja      | Gratuito   | Bajo               | Fácil        |
| Sofascore                | Muy Alta        | Actualidad         | Alta               | Alta      | No Oficial | Alto               | Difícil      |
| Fotmob                   | Muy Alta        | Actualidad         | Alta               | Alta      | No Oficial | Alto               | Difícil      |
| Kaggle Alternativos      | Variable        | Variable           | Variable           | Baja      | Gratuito   | Medio              | Fácil        |
| APIs Comerciales         | Muy Alta        | Actualidad         | Muy Alta           | Muy Alta  | Alto       | Bajo               | Fácil        |

---

# Evaluación Individual

## FBref Standard

### Ventajas

* Fuente ya integrada.
* Cobertura completa de las ligas objetivo.
* Actualización frecuente.
* Muy estable.
* Coste cero.

### Limitaciones

* Sin progresiones.
* Sin creación avanzada.
* Sin métricas defensivas avanzadas.
* Sin SCA/GCA.

### Rol Recomendado

Current Performance Layer.

---

## FBref Advanced Histórico

### Ventajas

* Excelente profundidad analítica.
* Totalmente integrado en el proyecto.
* Cobertura histórica suficiente para econometría y ML.

### Limitaciones

* Sin actualización posterior a 2024-2025.
* Dependencia de una fuente congelada.

### Rol Recomendado

Historical Advanced Layer.

---

## Understat

### Métricas Principales

* xG
* xA
* npxG
* Shot Quality
* Conversion Rates

### Ventajas

* Actualización continua.
* Metodología consolidada.
* Amplia utilización en investigación académica.

### Limitaciones

* Cobertura centrada en grandes ligas.
* No ofrece profundidad de progresión o posesión.

### Rol Recomendado

xG Intelligence Layer.

### Valor Estratégico

★★★★★

---

## DataMB

### Métricas Disponibles

* Progressive Passes
* Progressive Carries
* Key Passes
* Defensive Actions
* Possession Metrics
* Role Profiles

### Ventajas

* Cobertura moderna.
* Amplio catálogo de métricas.
* Cercano a la profundidad de FBref Advanced.

### Limitaciones

* Necesidad de validar licencia.
* Necesidad de validar automatización.
* Dependencia de proveedor externo.

### Rol Recomendado

Principal candidato a sustituto futuro de FBref Advanced.

### Valor Estratégico

★★★★★

---

## StatsBomb Open Data

### Ventajas

* Datos de eventos.
* Coordenadas espaciales.
* Máxima riqueza analítica.

### Permite construir

* xG propio.
* xA propio.
* Progressive Value.
* Packing Metrics.
* Field Tilt.
* Role Discovery avanzado.

### Limitaciones

* Cobertura insuficiente para DSS.
* No cubre adecuadamente las 11 ligas objetivo.

### Rol Recomendado

Research & Innovation Layer.

### Valor Estratégico

★★★★★ para I+D

★★☆☆☆ para operación

---

## Sofascore y Fotmob

### Ventajas

* Cobertura masiva.
* Métricas modernas.

### Limitaciones

* Riesgo legal.
* Dependencia de scraping.
* Cambios frecuentes.

### Rol Recomendado

No utilizar como capa crítica.

---

## APIs Comerciales

### Ventajas

* Máxima calidad.
* Actualización garantizada.
* Cobertura completa.

### Limitaciones

* Coste elevado.
* Fuera del alcance actual del proyecto.

### Rol Recomendado

Escenario futuro profesional.

---

# Arquitectura Objetivo Recomendada

## Capa Operativa

Transfermarkt

↓

Market Intelligence Layer

FBref Standard

↓

Current Performance Layer

Understat

↓

Expected Goals Layer

Role Engine Propio

↓

Scouting Intelligence Layer

---

## Capa de Investigación

StatsBomb Open

↓

Research & Innovation Layer

---

# Ranking Final

| Prioridad | Fuente              | Valor Estratégico |
| --------- | ------------------- | ----------------- |
| 1         | FBref Standard      | Muy Alto          |
| 2         | Understat           | Muy Alto          |
| 3         | DataMB              | Muy Alto          |
| 4         | StatsBomb Open      | Alto (I+D)        |
| 5         | APIs Comerciales    | Alto              |
| 6         | Kaggle Alternativos | Medio             |
| 7         | Sofascore           | Bajo              |
| 8         | Fotmob              | Bajo              |

---

# Conclusión

La estrategia recomendada para Scouting IQ consiste en mantener FBref Standard como fuente principal de rendimiento actual, incorporar Understat como capa especializada de xG Intelligence, utilizar el Role Engine propio como mecanismo de diferenciación competitiva y emplear StatsBomb Open exclusivamente como entorno de investigación para el desarrollo de futuras métricas propietarias.

DataMB emerge como el principal candidato para sustituir parcialmente la funcionalidad perdida de FBref Advanced, siempre que la licencia y los mecanismos de integración resulten viables.

Esta arquitectura minimiza el riesgo de dependencia de proveedor único, garantiza la sostenibilidad del producto y mantiene la defensa metodológica necesaria para un trabajo académico de nivel TFM.