# Sprint 13A — Multi-League Expansion Coverage Summary

## Overview

Sprint 13A focused on expanding the scouting universe and evaluating the external validity of the player valuation framework across a broader set of European football competitions.

The objective was not to improve predictive performance, but rather to assess whether the existing analytical architecture could generalize to additional competitive environments while maintaining operational usefulness.

---

## Competitions Included

### Original Scope

* Premier League
* LaLiga
* Bundesliga
* Serie A
* Ligue 1
* Eredivisie
* Liga Portugal

### Added in Sprint 13A

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

### Final Coverage

The expanded system now covers:

* 11 professional competitions
* 7 seasons (2019-2020 to 2025-2026)
* 43,591 player-season observations

---

## FBref Coverage Results

FBref data ingestion was successfully completed for all targeted competitions and seasons.

### Dataset Summary

| Metric                     |  Value |
| -------------------------- | -----: |
| Competitions               |     11 |
| Seasons                    |      7 |
| Player-Season Observations | 43,591 |
| Coverage Combinations      |     77 |

Coverage was complete across all targeted league-season combinations.

---

## Transfermarkt Matching Results

Player matching was performed using:

* Exact name matching
* Age validation
* Club validation
* Fuzzy matching fallback

### Global Matching Performance

| Metric                 |  Value |
| ---------------------- | -----: |
| Total Observations     | 43,591 |
| Matched Observations   | 33,115 |
| Unmatched Observations | 10,476 |
| Global Match Rate      | 75.97% |

### Match Rate by Competition

| Competition              | Match Rate |
| ------------------------ | ---------: |
| Bundesliga               |     92.75% |
| Premier League           |     92.62% |
| Serie A                  |     91.10% |
| Eredivisie               |     89.95% |
| Ligue 1                  |     89.70% |
| LaLiga                   |     84.26% |
| Belgian Pro League       |     79.68% |
| Liga Portugal            |     75.10% |
| Austrian Bundesliga      |     56.00% |
| Championship             |     50.36% |
| Spanish Segunda División |     43.03% |

---

## Coverage Audit Findings

A dedicated audit was conducted to investigate the lower matching rates observed in secondary competitions.

Representative unmatched players were manually inspected.

### Example Case

Player:

* Matt Grimes

Findings:

* Successfully matched between 2019-2020 and 2022-2023.
* Present in FBref during 2023-2024, 2024-2025 and 2025-2026.
* No corresponding market value observations were available in the Transfermarkt Kaggle dataset after June 2023.

Last available valuation:

* Date: 2023-06-01
* Season: 2022-2023

This pattern suggests that a significant proportion of unmatched observations are not caused by failures in the matching algorithm itself.

---

## Main Limitation Identified

The primary limitation identified during Sprint 13A is associated with the economic data source.

Specifically:

* Coverage is substantially lower in secondary competitions.
* Coverage decreases for more recent seasons.
* Several valid FBref observations do not have corresponding Transfermarkt market value records available in the Kaggle dataset.

Therefore, the observed reduction in matching rates is attributed primarily to limitations in Transfermarkt-Kaggle coverage rather than to deficiencies in the matching methodology.

---

## Methodological Implications

The expansion of the sporting data layer can be considered successful.

The system now operates across a substantially broader recruitment universe, including:

* Major European leagues
* Export-oriented leagues
* Secondary professional competitions

This strengthens the external validity of the overall framework and demonstrates that the analytical pipeline can scale beyond the original competition set.

---

## Future Research

A dedicated backlog item has been created:

### TM.1 — Transfermarkt Coverage Audit

Objective:

Determine whether the observed coverage limitations originate from:

* The Transfermarkt Kaggle dataset
* Transfermarkt as a source
* The extraction process used to generate the dataset

This investigation falls outside the scope of Sprint 13A and the current TFM deliverables.

---

## Conclusion

Sprint 13A successfully expanded the scouting universe from 7 to 11 competitions while preserving the existing analytical architecture.

The results support the external validity of the proposed methodology and provide a significantly broader recruitment universe for subsequent stages of the project.

The main limitation identified concerns the availability of market value information in the Transfermarkt-Kaggle dataset, particularly for secondary competitions and recent seasons.
