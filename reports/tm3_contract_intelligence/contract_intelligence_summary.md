# TM.3 Contract Intelligence Summary

## Status

COMPLETED

## Inputs

reports\rankings\scoring_dataset.csv
data\raw\transfermarkt\update_2025_2026\players.csv

## Snapshot Date

2025-07-01

## Methodological Decision

Contract Intelligence is integrated only into the current scouting and DSS layer.

It is not added to historical modeling datasets and does not modify econometric models, machine learning models, Opportunity Score, Risk Score or Recruitment Intelligence.

This avoids temporal leakage because the contract source is a current Transfermarkt snapshot.

## Matching Strategy

Contract data is integrated through normalized player names.

Club-level matching was intentionally not used in the production merge because it reduced coverage excessively due to naming differences between sources.

Expired contracts are retained in the full dataset for auditability but excluded from executive rankings.

## Hybrid DSS Score

recruitment_contract_score =
0.55 * contract_recruitment_opportunity_score
+ 0.30 * contract_opportunity_score
+ 0.15 * risk_inverse_score

risk_inverse_score = 100 - risk_score

If opportunity_score is unavailable, contract_recruitment_opportunity_score is proxied from inefficiency_rank.

## Coverage

Scoring rows: 6,208
Rows with contract expiration: 5,952
Rows with active contract expiration: 5,920
Rows with already expired contract: 32
Row-level contract coverage: 95.88%
Row-level active contract coverage: 95.36%
Rows with recruitment_contract_score: 5,920
Hybrid score coverage: 95.36%

Unique player-club-league combinations: 776
Unique combinations with contract expiration: 744
Unique combinations with active contract expiration: 740
Unique-level contract coverage: 95.88%
Unique-level active contract coverage: 95.36%

## Outputs

reports/tm3_contract_intelligence/contract_intelligence_dataset.csv
reports/tm3_contract_intelligence/top_contract_opportunities.csv
reports/tm3_contract_intelligence/top_recruitment_contract_targets.csv
reports/tm3_contract_intelligence/contract_status_distribution.csv
reports/tm3_contract_intelligence/contract_intelligence_summary.md
