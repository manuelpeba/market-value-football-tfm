from pathlib import Path
import re
import unicodedata

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

DSS_PATH = ROOT / "reports" / "dss" / "global_prospect_universe.csv"

CONTRACTS_PATH = (
    ROOT
    / "data"
    / "raw"
    / "transfermarkt"
    / "update_2025_2026"
    / "players.csv"
)

OUTPUT_DIR = ROOT / "reports" / "tm3_contract_intelligence"

SNAPSHOT_DATE = pd.Timestamp("2025-07-01")


def normalize_text(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^a-z0-9 ]", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def contract_status(score):
    if pd.isna(score):
        return "Contract Unknown"

    if score >= 80:
        return "Contract Opportunity"

    if score >= 60:
        return "Negotiable Target"

    if score >= 40:
        return "Neutral Contract"

    if score >= 20:
        return "Protected Asset"

    return "Long-Term Locked Asset"


def select_latest_contract_rows(contracts: pd.DataFrame) -> pd.DataFrame:
    contracts = contracts.copy()

    required_cols = [
        "name_key",
        "contract_expiration_date",
        "current_club_name",
        "market_value_in_eur",
    ]

    missing_cols = [c for c in required_cols if c not in contracts.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required contract source columns: {missing_cols}"
        )

    contracts["contract_expiration_date"] = pd.to_datetime(
        contracts["contract_expiration_date"],
        errors="coerce",
    )

    contracts["market_value_in_eur"] = pd.to_numeric(
        contracts["market_value_in_eur"],
        errors="coerce",
    )

    candidate_sort_cols = [
        "name_key",
        "contract_expiration_date",
        "updated_at",
        "last_updated",
        "date",
        "valuation_date",
        "market_value_date",
        "value_update_date",
        "season",
        "last_season",
        "market_value_in_eur",
    ]

    sort_cols = [
        c for c in candidate_sort_cols
        if c in contracts.columns
    ]

    ascending = [
        True if c == "name_key" else False
        for c in sort_cols
    ]

    for c in sort_cols:
        if c not in ["name_key", "season", "last_season", "market_value_in_eur"]:
            contracts[c] = pd.to_datetime(
                contracts[c],
                errors="coerce",
            )

    contracts_small = (
        contracts
        .sort_values(
            sort_cols,
            ascending=ascending,
            na_position="last",
        )
        .drop_duplicates("name_key", keep="first")
        [required_cols]
    )

    return contracts_small


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not DSS_PATH.exists():
        raise FileNotFoundError(f"DSS dataset not found: {DSS_PATH}")

    if not CONTRACTS_PATH.exists():
        raise FileNotFoundError(f"Contract source not found: {CONTRACTS_PATH}")

    dss = pd.read_csv(DSS_PATH)
    contracts = pd.read_csv(CONTRACTS_PATH)

    if "player_name_fbref" not in dss.columns:
        raise ValueError("DSS dataset must contain player_name_fbref")

    if "name" not in contracts.columns:
        raise ValueError("Transfermarkt players.csv must contain name")

    dss["name_key"] = dss["player_name_fbref"].map(normalize_text)
    contracts["name_key"] = contracts["name"].map(normalize_text)

    contracts_small = select_latest_contract_rows(contracts)

    df = dss.merge(
        contracts_small,
        on="name_key",
        how="left",
    )

    df["contract_expiration_date"] = pd.to_datetime(
        df["contract_expiration_date"],
        errors="coerce",
    )

    active_contract = (
        df["contract_expiration_date"].notna()
        & (df["contract_expiration_date"] >= SNAPSHOT_DATE)
    )

    months_remaining = (
        (df["contract_expiration_date"] - SNAPSHOT_DATE).dt.days / 30.44
    )

    df["contract_months_remaining"] = (
        months_remaining.clip(lower=0).round(1)
    )

    df["contract_years_remaining"] = (
        df["contract_months_remaining"] / 12
    ).round(2)

    df["contract_expiring_12m"] = (
        active_contract
        & (df["contract_months_remaining"] <= 12)
    ).astype(int)

    df["contract_critical_zone"] = (
        active_contract
        & (df["contract_months_remaining"] <= 6)
    ).astype(int)

    df["free_agent_horizon"] = (
        active_contract
        & (df["contract_months_remaining"] <= 18)
    ).astype(int)

    df["negotiation_leverage_score"] = np.where(
        active_contract,
        100 * (1 - df["contract_months_remaining"] / 60),
        np.nan,
    )

    df["negotiation_leverage_score"] = (
        df["negotiation_leverage_score"]
        .clip(0, 100)
        .round(2)
    )

    df["contract_opportunity_score"] = np.where(
        active_contract,
        (
            0.70 * df["negotiation_leverage_score"]
            + 20 * df["free_agent_horizon"]
            + 10 * df["contract_critical_zone"]
        ),
        np.nan,
    )

    df["contract_opportunity_score"] = (
        df["contract_opportunity_score"]
        .clip(0, 100)
        .round(2)
    )

    df["contract_status"] = (
        df["contract_opportunity_score"]
        .apply(contract_status)
    )

    df["recruitment_contract_score"] = (
        0.70 * df["opportunity_score"]
        + 0.30 * df["contract_opportunity_score"]
    ).round(2)

    dataset_path = OUTPUT_DIR / "contract_intelligence_dataset.csv"

    df.to_csv(dataset_path, index=False)

    top_contract = (
        df[df["contract_opportunity_score"].notna()]
        .sort_values("contract_opportunity_score", ascending=False)
        .head(25)
    )

    top_contract.to_csv(
        OUTPUT_DIR / "top_contract_opportunities.csv",
        index=False,
    )

    top_targets = (
        df[df["recruitment_contract_score"].notna()]
        .sort_values("recruitment_contract_score", ascending=False)
        .head(25)
    )

    top_targets.to_csv(
        OUTPUT_DIR / "top_recruitment_contract_targets.csv",
        index=False,
    )

    status_distribution = (
        df["contract_status"]
        .value_counts(dropna=False)
        .reset_index()
    )

    status_distribution.columns = [
        "contract_status",
        "players",
    ]

    status_distribution.to_csv(
        OUTPUT_DIR / "contract_status_distribution.csv",
        index=False,
    )

    coverage = df["contract_expiration_date"].notna().mean() * 100

    print("TM.3 Contract Intelligence completed")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Dataset: {dataset_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Contract coverage: {coverage:.2f}%")
    print(f"Snapshot date: {SNAPSHOT_DATE.date()}")


if __name__ == "__main__":
    main()