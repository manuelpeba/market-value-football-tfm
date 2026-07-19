# Evolución del proyecto y releases

## Propósito

Este documento mantiene la cronología canónica del proyecto. El [README principal](../README.md) es la autoridad sobre el estado productivo; esta cronología explica cómo se alcanzó ese estado y evita presentar como pendiente un bloque ya completado.

## Evolución por releases

| Release | Evolución principal |
| --- | --- |
| `v0.1.0` | Data Pipeline |
| `v0.2.0` | Econometric Baseline |
| `v0.3.0` | Tracking experimental con MLflow |
| `v0.4.0` | Machine Learning |
| `v0.5.0` | Explainability |
| `v0.6.0` | Scoring Engine |
| `v0.7.0` | Dashboard |
| `v0.8.0` | Productización del dashboard |
| `v1.0.0` | Scouting Intelligence Platform |
| `v1.1.0` | Recruitment Intelligence |
| `v1.2.0` | Multi-League Expansion |
| `v1.2.1` | Transfer Strategy Engine |
| `v1.2.2` | Multi-League DSS Integration |
| `v1.3.0` | Recruitment Intelligence & DSS |
| `v1.4.0` | Contract Intelligence Layer |
| `v2.0.0` | DSS Architecture, Data Contracts & Productization |

## Evolución por sprints

| Sprint | Estado | Contribución |
| --- | --- | --- |
| 1 | Completado | Normalización posicional |
| 2 | Completado | Dinámica temporal y variables de crecimiento |
| 3 | Completado | Índices compuestos de fútbol |
| 4 / 4C | Completado | Machine Learning y explainability |
| 5 | Completado | Opportunity Framework y scoring |
| 6 | Completado | Evaluación de negocio |
| 7 | Completado | Executive Dashboard |
| 9 | Completado | Decision Support Layer |
| 10 | Completado | Player Intelligence y Risk Framework |
| 11 | Completado | Recruitment Intelligence |
| 12 | Completado | Productización e internacionalización |
| 13A | Completado | Expansión a once ligas |
| 13A.1 | Completado | Validación externa y auditoría de cobertura; máximo histórico `R² = 0,5664` |
| 13B | Completado | Métricas avanzadas y modelos productivos v13B |
| 14 | Completado | Transfer Strategy Engine |
| 14.1 | Completado | Player Level Layer y optimización de cartera |
| TM.2 | Completado | Integración multi-liga de extremo a extremo en el DSS |
| TM.3 | Completado | Contract Intelligence Layer |
| TM.6.x | Completado | Identidad visual, activos, UX móvil y consistencia Cloud/local |
| TM.7.0 | Completado | Current Snapshot Authority |
| TM.7.1 | Completado | Presentation Layer canónica |
| TM.7.6 | Completado | Retirada de vistas legacy |
| TM.8.6 | Completado | Auditoría y cierre de rendimiento |
| TM.8.9 | Completado | Single Source of Truth e Identity Registry |
| TM.8.10 | Completado | DataFrame Contract Layer, Risk Authority y cierre de `v2.0.0` |

## Estado productivo v2.0.0

- Modelado histórico: `data/processed/player_season_modeling_v13b_productive_candidate.parquet`.
- Econometría oficial: Growth OLS v13B.
- Machine Learning productivo: Tuned XGBoost v13B, `R² = 0,4453`.
- Universo DSS: 757 jugadores y once competiciones.
- Cobertura contractual documentada: 95,90 %.
- Autoridades separadas: modeling, snapshot, identity, presentation y risk.
- Aplicación: DSS Streamlit operativo, bilingüe, responsive y optimizado mediante contexto centralizado.

## Roadmap vigente

Los bloques TM.2, TM.3, TM.6.x, TM.7.x y TM.8.x anteriores no son roadmap: forman parte del historial completado. Las líneas abiertas de `v2.0.0` son:

- benchmark TabPFN;
- benchmark CatBoost;
- modularización de `app/streamlit_app.py`;
- promoción automatizada de snapshots;
- CI para contratos y documentación;
- UEFA Club Strength Layer;
- National Team Layer;
- European Competition Layer;
- Club Development Index;
- Injury Prediction como línea independiente de Health Intelligence.

## Regla de mantenimiento

Una funcionalidad solo debe figurar como completada cuando esté implementada y validada. El roadmap describe trabajo futuro; los resultados históricos se conservan con su sprint y artefacto para evitar mezclar benchmarks experimentales con autoridades productivas.
