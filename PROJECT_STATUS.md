# Estado del proyecto

## 1. Resumen ejecutivo

El proyecto tiene como objetivo desarrollar un sistema analítico para identificar jugadores infravalorados en el mercado de fichajes europeo mediante la estimación del valor de mercado esperado.

El sistema se basa en la integración de múltiples fuentes de datos y la aplicación de modelos econométricos sobre un dataset estructurado a nivel jugador–temporada.

Estado actual:

- Dataset final de panel: 23,580 observaciones
- Dataset modelizable: 3,297 observaciones
- Jugadores únicos: 1,847
- Cobertura temporal: 2019-2020 a 2024-2025
- Cobertura geográfica: 7 ligas europeas

El sistema ya permite estimar valor de mercado esperado y está preparado para construir el Inefficiency Score.

---

## 2. Fase actual (CRISP-DM)

Fase actual del proyecto:

```

Modeling → Evaluation

```

Fases completadas:

- Business understanding
- Data understanding
- Data preparation

Fases en curso:

- Modelización econométrica
- Evaluación del modelo

---

## 3. Arquitectura del pipeline de datos

El pipeline implementado sigue una estructura modular:

1. Ingesta de datos
   - FBref (HTML parsing)
   - Transfermarkt (CSV estructurado)

2. Feature engineering
   - Variables por 90 minutos
   - Transformaciones logarítmicas
   - Normalización de nombres

3. Integración (matching)
   - Construcción del panel jugador–temporada

4. Dataset de modelización
   - Filtrado por calidad, edad y minutos

---

## 4. Problema crítico: integración FBref – Transfermarkt

### 4.1 Naturaleza del problema

El principal reto técnico del proyecto reside en la integración de las fuentes FBref y Transfermarkt, ya que:

- No existe identificador único común entre datasets
- Diferencias en naming de jugadores (idioma, acentos, abreviaturas)
- Diferencias en naming de clubes
- Desalineación en edades (por fechas de captura distintas)
- Diferencias en granularidad temporal

Este problema es estructural en proyectos de sports analytics y representa una fuente clave de incertidumbre.

---

### 4.2 Consecuencias del problema

Sin un matching robusto:

- Se generan uniones incorrectas (false positives)
- Se pierden observaciones válidas (false negatives)
- Se introduce ruido en el modelo
- Se compromete la validez del Inefficiency Score

---

### 4.3 Estrategia de solución implementada

Se ha diseñado un sistema de matching jerárquico basado en múltiples validaciones:

#### 1. Normalización de nombres

- Lowercase
- Eliminación de acentos
- Eliminación de caracteres especiales

#### 2. Matching exacto

- Nombre normalizado
- Edad
- Temporada

#### 3. Matching validado por club

- Similaridad de strings (fuzzy matching)
- Score mínimo de similitud

#### 4. Matching fuzzy

- Distancia de Levenshtein
- Umbral de aceptación elevado

#### 5. Validación por edad

- Diferencia máxima permitida: 1.5 años

---

### 4.4 Reducción del espacio de búsqueda

Para mejorar eficiencia y precisión:

- Filtro por temporada
- Filtro por liga
- Filtro por rango de edad

Resultado:

- Reducción de 616,377 → 293,640 registros en Transfermarkt

---

### 4.5 Resultados del matching

Resultados finales:

- Match rate: 88.36%
- Observaciones emparejadas: 20,836

Distribución:

- exact_age_validated: dominante
- exact_age_club_validated: relevante
- fuzzy matching: residual

---

### 4.6 Validación del matching

Indicadores de calidad:

- Diferencia media de edad ≈ 0.72 años
- Club score medio ≈ 32 (sin filtro fuerte de club)
- Distribución estable por liga y temporada

---

### 4.7 Trade-off metodológico

Se ha tomado una decisión clave:

**Priorizar recall sobre precisión en fases iniciales**

Justificación:

- Mantener mayor volumen de datos para modelización
- Controlar ruido posteriormente mediante:
  - filtros
  - variables de confianza
  - robustez del modelo

---

## 5. Dataset final de modelización

Tras aplicar filtros:

- Observaciones: 3,297
- Jugadores: 1,847

Filtros aplicados:

- Matching válido
- Edad entre 18–23 años
- Minutos jugados mínimos
- Valor de mercado disponible

---

## 6. Calidad del dataset

Fortalezas:

- Alta cobertura temporal
- Buen balance entre ligas
- Variables relevantes para modelización

Limitaciones:

- Sesgo por liga
- Sesgo por posición
- Ruido residual en matching

---

## 7. Estado de la modelización

Preparado para:

- Modelo OLS con efectos fijos:
  - Liga
  - Temporada
  - Posición

Objetivo:

Estimar:

- Valor de mercado esperado
- Inefficiency Score

---

## 8. Próximos pasos

1. Construcción del modelo econométrico final
2. Evaluación out-of-sample
3. Cálculo del Inefficiency Score
4. Ranking de jugadores infravalorados
5. Interpretación económica de resultados

---

## 9. Conclusión

El proyecto ha superado con éxito la fase más crítica desde el punto de vista técnico: la integración de fuentes heterogéneas sin identificador común.

El sistema resultante es metodológicamente sólido y permite avanzar hacia la modelización con un nivel de calidad adecuado para un Trabajo de Fin de Máster.

La complejidad del matching y su resolución constituyen uno de los principales aportes del proyecto.

