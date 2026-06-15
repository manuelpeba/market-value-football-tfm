# TM.6.7b — Strategic Recommendation

## Entregable 5 — Final Recommendation & Decision Framework

### Objetivo

Definir la estrategia recomendada para la evolución de la capa de rendimiento avanzado de Scouting IQ tras la congelación de FBref Advanced en la temporada 2024-2025.

Este documento sintetiza los hallazgos obtenidos en:

* Entregable 1 — Source Strategy
* Entregable 2 — FBref Advanced Replacement Matrix
* Entregable 3 — Future Architecture
* Entregable 4 — Source Comparison Matrix

y establece una hoja de ruta ejecutiva para la evolución del producto y del ecosistema de datos.

---

# Resumen Ejecutivo

La auditoría realizada confirma que FBref Advanced constituye actualmente una de las fuentes más valiosas del ecosistema Scouting IQ debido a su combinación de:

* cobertura;
* profundidad analítica;
* facilidad de integración;
* coste cero.

Sin embargo, la congelación de dicha fuente a partir de la temporada 2024-2025 impide considerarla una solución sostenible para futuras actualizaciones del producto.

Por este motivo, la estrategia recomendada consiste en evolucionar desde una arquitectura dependiente de proveedor hacia una arquitectura multicapa basada en especialización funcional.

---

# Principales Hallazgos

## Hallazgo 1

La capa histórica del proyecto no está en riesgo.

Los modelos econométricos y de machine learning ya han sido entrenados sobre datasets históricos completos.

Por tanto:

```text
No es necesario reconstruir
ni reentrenar el histórico.
```

El problema afecta exclusivamente a:

```text
actualización futura
monitorización
scouting operativo
recruitment intelligence
```

---

## Hallazgo 2

No existe actualmente una fuente gratuita que sustituya completamente a FBref Advanced.

Las alternativas disponibles cubren únicamente partes específicas del problema:

| Necesidad           | Mejor Alternativa |
| ------------------- | ----------------- |
| xG                  | Understat         |
| xAG                 | Understat         |
| npxG                | Understat         |
| Progressive Passes  | DataMB            |
| Progressive Carries | DataMB            |
| Key Passes          | DataMB            |
| SCA                 | DataMB            |
| GCA                 | DataMB            |
| Event Data          | StatsBomb Open    |

La sustitución deberá realizarse mediante una combinación de fuentes.

---

## Hallazgo 3

El Role Engine desarrollado en TM.5 y TM.6 reduce significativamente el riesgo de dependencia externa.

Actualmente Scouting IQ ya dispone de:

```text
Role Discovery

Role Similarity

Role DNA

Role Explanation Engine
```

Esto constituye una ventaja estratégica porque parte del valor del sistema ya no depende directamente de métricas de terceros.

---

# Decisión Estratégica Recomendada

## Mantener

### Transfermarkt

Como fuente principal de:

```text
Market Intelligence
Contract Intelligence
```

---

### FBref Standard

Como fuente principal de:

```text
Current Performance Intelligence
```

---

### FBref Advanced Histórico

Como fuente oficial de:

```text
Historical Advanced Benchmark
```

Debe permanecer congelado y versionado.

No debe intentarse reconstruir artificialmente.

---

# Incorporar

## Understat

### Prioridad

CRÍTICA

### Objetivo

Crear:

```text
Expected Goals Intelligence Layer
```

Métricas:

```text
xG
xAG
npxG
```

Beneficios:

* actualización continua;
* coste cero;
* elevada aceptación académica.

---

## DataMB

### Prioridad

ALTA

### Objetivo

Validar viabilidad de:

```text
Advanced Performance Layer
```

Métricas objetivo:

```text
Progressive Passes

Progressive Carries

Key Passes

SCA

GCA

Defensive Actions
```

---

# Desarrollar

## Role Engine 2.0

### Objetivo

Generar métricas propietarias.

Ejemplos:

```text
Scouting IQ Progression Index

Scouting IQ Creation Index

Scouting IQ Defensive Activity Index

Scouting IQ Recruitment Fit Score
```

### Beneficio

Reducir progresivamente la dependencia de proveedores externos.

---

# Reservar para Investigación

## StatsBomb Open Data

### Rol recomendado

```text
Research Layer
```

No debe considerarse sustituto operativo de FBref Advanced.

Debe utilizarse para:

```text
Feature Engineering

Role Validation

Event Analytics

Metric Innovation
```

---

# Arquitectura Objetivo Recomendada

```text
TRANSFERMARKT
        │
        ▼
Market Intelligence Layer

FBREF STANDARD
        │
        ▼
Current Performance Layer

UNDERSTAT
        │
        ▼
Expected Goals Layer

DATAMB
        │
        ▼
Advanced Performance Layer

ROLE ENGINE
        │
        ▼
Proprietary Scouting Layer

STATSBOMB OPEN
        │
        ▼
Research & Innovation Layer

DECISION SUPPORT SYSTEM
```

---

# Roadmap Recomendado

## TM.6.8

### Understat Integration

Objetivo:

```text
Expected Goals Intelligence Layer
```

Entregables:

```text
understat_audit

understat_snapshot

understat_metadata

understat_health_report

understat_dashboard_integration
```

---

## TM.7.0

### Current Performance Intelligence

Objetivo:

Integrar todas las capas actuales dentro del DSS.

Módulos afectados:

```text
Player Intelligence

Recruitment Intelligence

Strategy Center
```

---

## TM.8.0

### StatsBomb Research Lab

Objetivo:

Diseñar métricas propietarias basadas en event data.

---

# Evaluación Final

## Viabilidad Técnica

```text
MUY ALTA
```

---

## Viabilidad Académica

```text
MUY ALTA
```

---

## Viabilidad Económica

```text
ALTA
```

---

## Riesgo Operativo

```text
BAJO
```

tras la adopción de una arquitectura multicapa.

---

# Recomendación Final

Se recomienda adoptar una estrategia basada en:

```text
FBref Standard
+
Transfermarkt
+
Understat
+
Role Engine Propio
```

como núcleo operativo de Scouting IQ durante el período 2026–2030.

DataMB debe evaluarse como sustituto funcional parcial de FBref Advanced, mientras que StatsBomb Open Data debe emplearse como plataforma de investigación para la generación de futuras métricas propietarias.

Esta aproximación ofrece el mejor equilibrio entre sostenibilidad, calidad analítica, coste operativo y defensa metodológica, alineándose tanto con los objetivos académicos del TFM como con la evolución potencial de Scouting IQ hacia una plataforma profesional de football intelligence.
