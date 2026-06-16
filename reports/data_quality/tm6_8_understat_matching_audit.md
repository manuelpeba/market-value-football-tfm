# TM.6.8c — Understat Matching Strategy & DSS Coverage Audit

Audit date: 2026-06-16

## Matching Strategy

Current audit method:

```text
player_name_norm + league
```

Future productive method:

```text
player_id_tm + understat_player_id crosswalk
```

## Coverage Results

| Dataset | Rows Total | Big 5 Rows | Matched Rows | Coverage Big 5 | Coverage Total | Player Col | League Col |
|---|---:|---:|---:|---:|---:|---|---|
| DSS | 757 | 478 | 368 | 76.99% | 48.61% | player_name_norm | display_league |
| Portfolio | 6208 | 3912 | 2952 | 75.46% | 47.55% | player_name_norm | display_league |
| Contract | 757 | 478 | 368 | 76.99% | 48.61% | player_name_norm | display_league |

## Governance Note

This audit uses conservative name + league matching. It is valid for coverage estimation, but productive DSS enrichment should use a controlled mapping layer between `player_id_tm` and `understat_player_id`.

## Output Files

- `C:\Users\manue\Projects\market-value-football-tfm\reports\data_quality\tm6_8_understat_matching_audit.csv`
- `C:\Users\manue\Projects\market-value-football-tfm\reports\data_quality\tm6_8_understat_matching_audit.json`
- `C:\Users\manue\Projects\market-value-football-tfm\reports\data_quality\tm6_8_understat_matching_unmatched_big5.csv`