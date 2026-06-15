# TM.6.7b — Future Architecture

## Entregable 3 — Scouting IQ Target Data Architecture (2026–2030)

### Objetivo

Definir la arquitectura objetivo de datos para Scouting IQ durante el período 2026–2030, garantizando sostenibilidad operativa, independencia de proveedores individuales, trazabilidad metodológica y capacidad de evolución hacia un producto profesional de scouting y recruitment intelligence.

La arquitectura propuesta se basa en una filosofía de capas desacopladas donde cada fuente aporta una función específica dentro del ecosistema analítico.

---

# Principios de Diseño

## 1. Separación entre histórico y actualidad

La arquitectura distingue explícitamente entre:

```text
Historical Layers
```

utilizadas para:

* investigación;
* econometría;
* machine learning;
* evaluación histórica;

y

```text
Current Snapshot Layers
```

utilizadas para:

* scouting;
* recruitment;
* monitoring;
* toma de decisiones.

Esto evita la contaminación entre datasets de entrenamiento y contexto operativo actual.

---

## 2. Independencia de proveedor

Ningún componente crítico del sistema debe depender exclusivamente de una única fuente externa.

Cada dominio funcional debe disponer de:

* fuente principal;
* alternativa viable;
* estrategia de sustitución.

---

## 3. Reproducibilidad

Toda transformación debe ser:

* auditable;
* reproducible;
* versionable;
* trazable.

Las capas operativas deben estar acompañadas por:

* metadata;
* health reports;
* governance reports;
* snapshot registries.

---

## 4. Escalabilidad

La arquitectura debe permitir:

* incorporación de nuevas ligas;
* incorporación de nuevas fuentes;
* incorporación de nuevas métricas;
* ampliación de funcionalidades DSS.

Sin necesidad de rediseñar la plataforma.

---

# Arquitectura Objetivo

## Layer 1 — Market Intelligence

### Fuente principal

Transfermarkt

### Responsabilidad

Información económica del mercado:

```text
Market Value
Market Value History
Contract Expiration
Club Context
Competition Context
Player Identity
Transfers
```

### Componentes

```text
Historical Market Layer

Current Market Snapshot

Market Metadata

Market Health Reports
```

### Estado

```text
TM.6.6c
COMPLETADO
```

---

# Layer 2 — Performance Intelligence

## Fuente principal

FBref Standard

### Responsabilidad

Contexto deportivo actual:

```text
Minutes
Goals
Assists
Starts
Availability
Basic Shooting
Playing Time
```

### Componentes

```text
Historical Performance Layer

Current Performance Snapshot

Performance Metadata

Performance Health Reports
```

### Estado

```text
TM.6.7a
IMPLEMENTADO
```

---

# Layer 3 — Expected Goals Intelligence

## Fuente objetivo

Understat

### Responsabilidad

Producción ofensiva esperada:

```text
xG
xAG
npxG
Shot Quality
Conversion Efficiency
```

### Justificación

Permite recuperar la funcionalidad perdida tras la congelación de FBref Advanced.

### Componentes futuros

```text
Historical xG Layer

Current xG Snapshot

xG Intelligence Dashboard

Expected Goals Metadata
```

### Estado

```text
TM.6.8
PLANIFICADO
```

---

# Layer 4 — Advanced Performance Intelligence

## Fuente objetivo

DataMB

### Responsabilidad

Métricas avanzadas de creación y progresión:

```text
Progressive Passes

Progressive Carries

Key Passes

SCA

GCA

Defensive Actions

Possession Metrics
```

### Justificación

Representa el principal candidato para sustituir parcialmente FBref Advanced.

### Componentes futuros

```text
Advanced Performance Layer

Advanced Snapshot

Advanced Metadata

Advanced Health Reports
```

### Estado

```text
TM.6.7b
EN EVALUACIÓN
```

---

# Layer 5 — Proprietary Scouting Intelligence

## Fuente

Scouting IQ Role Engine

### Responsabilidad

Generar métricas propietarias independientes de proveedores externos.

### Componentes

```text
Role Discovery Engine

Role Similarity Engine

Role DNA

Role Explanation Engine
```

### Evolución prevista

Generación de indicadores propios:

```text
Scouting IQ Progression Index

Scouting IQ Creation Index

Scouting IQ Defensive Activity Index

Scouting IQ Role Fit Score

Scouting IQ Recruitment Fit Score
```

### Ventaja estratégica

Reduce dependencia de terceros y genera diferenciación competitiva.

### Estado

```text
TM.6.x
OPERATIVO
```

---

# Layer 6 — Research & Innovation

## Fuente principal

StatsBomb Open Data

### Responsabilidad

Investigación avanzada.

No forma parte de la capa operativa.

### Casos de uso

```text
Feature Engineering

Role Validation

Event Data Research

Spatial Analysis

Prototype Metrics
```

### Resultados esperados

Desarrollo de futuras métricas propietarias.

### Estado

```text
TM.8.0
PLANIFICADO
```

---

# Decision Support System Layer

## Executive Overview

Consumirá:

```text
Market Layer
Performance Layer
Opportunity Layer
```

---

## Player Intelligence

Consumirá:

```text
Market Snapshot

Performance Snapshot

xG Snapshot

Role Intelligence
```

---

## Recruitment Intelligence

Consumirá:

```text
Role Intelligence

Performance Intelligence

xG Intelligence

Contract Intelligence
```

---

## Contract Intelligence

Consumirá:

```text
Transfermarkt Layer
```

---

## Strategy Center

Consumirá:

```text
Opportunity Scores

Portfolio Scores

Risk Scores

Performance Context

Market Context
```

---

# Flujo de Datos Objetivo

```text
TRANSFERMARKT
        │
        ▼
Market Intelligence Layer
        │
        ▼

FBREF STANDARD
        │
        ▼
Performance Intelligence Layer
        │
        ▼

UNDERSTAT
        │
        ▼
Expected Goals Layer
        │
        ▼

DATAMB
        │
        ▼
Advanced Performance Layer
        │
        ▼

ROLE ENGINE
        │
        ▼
Proprietary Intelligence Layer
        │
        ▼

DECISION SUPPORT SYSTEM
```

---

# Roadmap de Evolución

## Fase Actual

```text
TM.6.6c
Snapshot Governance
```

```text
TM.6.7a
Current Performance Snapshot
```

---

## Próxima Fase

```text
TM.6.8
Understat Integration
```

Objetivo:

```text
xG Layer
```

---

## Medio Plazo

```text
TM.7.0
Current Performance Intelligence
```

Objetivo:

Integración completa de snapshots en DSS.

---

## Largo Plazo

```text
TM.8.0
StatsBomb Research Lab
```

Objetivo:

Desarrollo de métricas propietarias basadas en event data.

---

# Conclusión

La arquitectura objetivo propuesta transforma Scouting IQ desde un sistema dependiente de fuentes externas concretas hacia una plataforma multicapa basada en gobernanza, trazabilidad y resiliencia operativa.

La combinación de Transfermarkt, FBref Standard, Understat, DataMB y un Role Engine propietario permite mantener la sostenibilidad del producto a largo plazo, minimizar riesgos de dependencia y sentar las bases para futuras capacidades avanzadas de scouting, recruitment intelligence y analítica deportiva aplicada.
