# TM.4.1 — Data Validation & Freshness Audit

Generated at: `2026-06-13T01:20:40.360235+00:00` UTC

## Executive diagnosis

- Project root: `C:\Users\manue\Projects\market-value-football-tfm`
- Dataset files detected: **539**.
- Dataset modified range UTC: **2026-04-01T07:41:42+00:00 → 2026-06-12T00:20:45.537046+00:00**.
- Streamlit explicit dataset loads detected: **21**.
- Datasets containing contractual columns: **0**.
- Datasets containing market-value columns: **109**.
- Target-player internal matches found: **2719** rows.
- Expected module dataset references missing: **4**.

## Priority findings

1. **Critical:** no detected dataset contains the expected contract columns. Contract Intelligence cannot be considered data-validated until the TM.3 contract artifact is present or the dashboard source is aligned.
2. Case-level rows were found. Review `tm41_case_audit.csv` for Raúl Asencio, Nico/Nicolò Savona and Javi Rodríguez.
3. Market-value datasets were detected. Review `tm41_market_value_audit.csv` to assess update-date coverage and invalid values.
4. Review file modification timestamps and hashes in `tm41_dataset_inventory.csv` before demo/release.

## Output files

- `reports/data_quality/tm41_dataset_inventory.csv`
- `reports/data_quality/tm41_module_dataset_map.csv`
- `reports/data_quality/tm41_streamlit_dataset_refs.csv`
- `reports/data_quality/tm41_column_audit.csv`
- `reports/data_quality/tm41_case_audit.csv`
- `reports/data_quality/tm41_contract_audit.csv`
- `reports/data_quality/tm41_market_value_audit.csv`
