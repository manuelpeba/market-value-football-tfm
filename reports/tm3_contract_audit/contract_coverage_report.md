# TM.3 Contract Data Audit

## Status

```text
CONTRACT DATA AVAILABLE
```

## Audit scope

- Root scanned: `C:\Users\manue\Projects\market-value-football-tfm`
- Tabular files scanned: `531`
- Exact contract columns searched:

```text
contract_end, contract_expiration_date, contract_expires, contract_remaining, contract_until, expiration_year, remaining_contract
```

## Results

| Metric | Value |
|---|---:|
| Exact contract columns found | 4 |
| Semantic contract columns found | 0 |
| Contract coverage computable | True |

## Interpretation

Contract-related columns were detected in tabular artifacts. Next step: compute observation-level, league-level and season-level coverage.

## Generated outputs

```text
reports/tm3_contract_audit/contract_coverage.csv
reports/tm3_contract_audit/contract_coverage_by_league.csv
reports/tm3_contract_audit/contract_coverage_report.md
reports/tm3_contract_audit/contract_column_candidates.csv
reports/tm3_contract_audit/contract_text_mentions.csv
```
