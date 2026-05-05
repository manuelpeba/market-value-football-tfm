from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data/processed/player_season_panel.parquet"
OUTPUT = ROOT / "data/processed/player_season_modeling.parquet"

df = pd.read_parquet(INPUT)

# Unificar nombres de columnas procedentes del merge
if "season_start_year_fbref" in df.columns:
    df["season_start_year"] = df["season_start_year_fbref"]
elif "season_start_year_tm" in df.columns:
    df["season_start_year"] = df["season_start_year_tm"]
else:
    raise KeyError("No season_start_year column found.")

if "age_tm" in df.columns:
    df["age"] = df["age_tm"]
elif "age_fbref" in df.columns:
    df["age"] = df["age_fbref"]
else:
    raise KeyError("No age column found.")

if "position_group" in df.columns:
    df["position_group"] = df["position_group"]
elif "position_group_tm" in df.columns:
    df["position_group"] = df["position_group_tm"]
elif "position_group_fbref" in df.columns:
    df["position_group"] = df["position_group_fbref"]
else:
    df["position_group"] = "UNK"

# Filtros de modelización
df = df[
    (df["season_start_year"] >= 2020) &
    (df["season_start_year"] <= 2023)
]

df = df[
    (df["age"] >= 18) &
    (df["age"] <= 23)
]

df = df[df["minutes_played"] >= 300]
df = df[df["market_value_eur"].notna()]

# Limpieza mínima
df = df.drop_duplicates(subset=["player_name_fbref", "season"])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(OUTPUT, index=False)

print("Modeling dataset construido")
print(f"Rows: {len(df):,}")
print(f"Players: {df['player_name_fbref'].nunique():,}")
print(f"Seasons: {df['season'].min()} - {df['season'].max()}")
print(f"Output: {OUTPUT}")