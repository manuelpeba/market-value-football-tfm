from pathlib import Path
import unicodedata
import warnings

import numpy as np
import pandas as pd


# =============================================================================
# Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_EXTERNAL = PROJECT_ROOT / "data" / "external"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_ROLES = PROJECT_ROOT / "reports" / "roles"

FBREF_ADVANCED_PATH = DATA_EXTERNAL / "fbref_top5_2017_2025.csv"

ROLE_LABELS_PATH = REPORTS_ROLES / "player_role_labels.csv"

OUTPUT_PARQUET = DATA_PROCESSED / "player_role_explainability.parquet"
OUTPUT_DNA_CSV = REPORTS_ROLES / "player_role_dna.csv"
OUTPUT_SUMMARY_CSV = REPORTS_ROLES / "role_explainability_summary.csv"
OUTPUT_COVERAGE_CSV = REPORTS_ROLES / "role_explainability_feature_coverage.csv"
OUTPUT_ROLE_PROFILES_CSV = REPORTS_ROLES / "role_tactical_profiles.csv"


# =============================================================================
# Tactical dimensions using real Kaggle FBref columns
# =============================================================================

TACTICAL_DIMENSIONS = {
    "finishing_index_role": [
        "Per 90 Minutes_Gls",
        "Per 90 Minutes_xG",
        "Per 90 Minutes_npxG",
        "Standard_SoT%",
        "Standard_G/Sh",
        "Standard_G/SoT",
        "Expected_G-xG",
        "Expected_np:G-xG",
        "Expected_npxG/Sh",
    ],
    "chance_creation_index": [
        "Per 90 Minutes_Ast",
        "Per 90 Minutes_xAG",
        "Expected_xAG",
        "Expected_xA",
        "KP_",
        "PPA_",
        "CrsPA_",
        "GCA_GCA90",
        "GCA_GCA",
    ],
    "ball_progression_index": [
        "Progression_PrgC",
        "Progression_PrgP",
        "Progression_PrgR",
        "PrgP_",
        "Total_PrgDist",
        "1/3_",
        "PPA_",
    ],
    "passing_security_index": [
        "Total_Cmp%",
        "Short_Cmp%",
        "Medium_Cmp%",
        "Long_Cmp%",
        "Total_Att",
        "Total_Cmp",
    ],
    "passing_volume_index": [
        "Total_Att",
        "Total_Cmp",
        "Short_Att",
        "Medium_Att",
        "Long_Att",
        "Outcomes_Cmp",
    ],
    "crossing_width_index": [
        "Pass Types_Crs",
        "CrsPA_",
        "Corner Kicks_In",
        "Corner Kicks_Out",
    ],
    "availability_index_role": [
        "Playing Time_MP",
        "Playing Time_Starts",
        "Playing Time_Min",
        "Playing Time_90s",
        "90s_",
    ],
    "discipline_risk_index": [
        "Performance_CrdY",
        "Performance_CrdR",
    ],
}


ROLE_EXPECTED_DIMENSIONS = {
    "Ball Winner": [
        "ball_progression_index",
        "passing_security_index",
        "availability_index_role",
    ],
    "Aggressive Defender": [
        "ball_progression_index",
        "passing_security_index",
        "availability_index_role",
    ],
    "Aerial Defender": [
        "availability_index_role",
        "passing_security_index",
        "ball_progression_index",
    ],
    "Ball-Playing Centre-Back": [
        "ball_progression_index",
        "passing_security_index",
        "passing_volume_index",
        "availability_index_role",
    ],
    "Creative Playmaker": [
        "chance_creation_index",
        "ball_progression_index",
        "passing_security_index",
    ],
    "Attacking Progressor": [
        "ball_progression_index",
        "chance_creation_index",
        "passing_volume_index",
    ],
    "Box Finisher": [
        "finishing_index_role",
        "chance_creation_index",
        "availability_index_role",
    ],
    "Creator Forward": [
        "chance_creation_index",
        "finishing_index_role",
        "ball_progression_index",
    ],
    "Mobile Forward": [
        "ball_progression_index",
        "finishing_index_role",
        "chance_creation_index",
    ],
}


ID_COLS_OUTPUT = [
    "league",
    "season",
    "team",
    "player",
    "nation_",
    "pos_",
    "age_",
    "Playing Time_Min",
    "Playing Time_90s",
    "primary_role",
    "secondary_role",
    "role_confidence",
    "role_purity",
    "role_ambiguity",
    "primary_role_similarity",
    "secondary_role_similarity",
    "positional_taxonomy",
]


# =============================================================================
# Helpers
# =============================================================================

def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("ø", "o").replace("đ", "d").replace("ß", "ss")

    for token in ["-", "_", ".", "'", "’", "`"]:
        text = text.replace(token, " ")

    return " ".join(text.split())


def safe_numeric(series: pd.Series) -> pd.Series:
    if series.dtype == "object":
        series = (
            series.astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace("%", "", regex=False)
            .replace({"": np.nan, "nan": np.nan, "None": np.nan})
        )
    return pd.to_numeric(series, errors="coerce")


def read_fbref_advanced() -> pd.DataFrame:
    if not FBREF_ADVANCED_PATH.exists():
        raise FileNotFoundError(f"No existe: {FBREF_ADVANCED_PATH}")

    df = pd.read_csv(
        FBREF_ADVANCED_PATH,
        sep=";",
        decimal=",",
        engine="python",
    )

    return df


def read_role_labels() -> pd.DataFrame | None:
    if not ROLE_LABELS_PATH.exists():
        warnings.warn(f"No existe role labels: {ROLE_LABELS_PATH}")
        return None

    return pd.read_csv(ROLE_LABELS_PATH, low_memory=False)


def build_match_key(df: pd.DataFrame, player_col: str, team_col: str | None, season_col: str) -> pd.Series:
    player_key = df[player_col].map(normalize_text)
    season_key = df[season_col].astype(str).str.strip()

    if team_col and team_col in df.columns:
        team_key = df[team_col].map(normalize_text)
    else:
        team_key = ""

    return player_key + "|" + team_key.astype(str) + "|" + season_key


def find_role_column(df: pd.DataFrame) -> str | None:
    for col in ["primary_role", "role", "tactical_role"]:
        if col in df.columns:
            return col
    return None


def infer_role_label_columns(role_df: pd.DataFrame) -> dict[str, str | None]:
    player_col = None
    team_col = None
    season_col = None

    for col in ["player", "player_name_fbref", "player_name", "player_name_tm"]:
        if col in role_df.columns:
            player_col = col
            break

    for col in ["team", "club", "squad"]:
        if col in role_df.columns:
            team_col = col
            break

    for col in ["season", "season_start_year", "season_start_year_fbref"]:
        if col in role_df.columns:
            season_col = col
            break

    return {
        "player_col": player_col,
        "team_col": team_col,
        "season_col": season_col,
    }


def percentile_by_group(df: pd.DataFrame, col: str, group_cols: list[str]) -> pd.Series:
    values = safe_numeric(df[col])

    valid_groups = [c for c in group_cols if c in df.columns]

    if not valid_groups:
        return values.rank(pct=True) * 100

    return values.groupby([df[c] for c in valid_groups]).rank(pct=True) * 100


def build_dimension(
    df: pd.DataFrame,
    dimension: str,
    columns: list[str],
    group_cols: list[str],
) -> tuple[pd.Series, list[str]]:
    used = [c for c in columns if c in df.columns]

    if not used:
        warnings.warn(f"No hay columnas disponibles para {dimension}")
        return pd.Series(np.nan, index=df.index), []

    transformed = []

    for col in used:
        s = safe_numeric(df[col])

        if s.notna().sum() == 0:
            continue

        # Tarjetas como riesgo: más tarjetas = peor, por eso se invierte.
        if dimension == "discipline_risk_index":
            pct = percentile_by_group(df, col, group_cols)
            transformed.append(100 - pct)
        else:
            transformed.append(percentile_by_group(df, col, group_cols))

    if not transformed:
        return pd.Series(np.nan, index=df.index), used

    result = pd.concat(transformed, axis=1).mean(axis=1, skipna=True)
    return result.clip(0, 100), used


def role_fit(row: pd.Series) -> float:
    role = row.get("primary_role", np.nan)

    # No calcular fit explicativo si el jugador no tiene rol asignado
    if pd.isna(role) or str(role).strip() in ["", "None", "nan"]:
        return np.nan

    if role in ROLE_EXPECTED_DIMENSIONS:
        dims = ROLE_EXPECTED_DIMENSIONS[role]
    else:
        dims = list(TACTICAL_DIMENSIONS.keys())

    vals = [row.get(dim, np.nan) for dim in dims]
    vals = [float(v) for v in vals if pd.notna(v)]

    if not vals:
        return np.nan

    return float(np.mean(vals))


def role_quality(row: pd.Series) -> str:
    role = row.get("primary_role", np.nan)

    # Evita clasificar como High a jugadores sin rol
    if pd.isna(role) or str(role).strip() in ["", "None", "nan"]:
        return "No role assigned"

    if role in ROLE_EXPECTED_DIMENSIONS:
        dims = ROLE_EXPECTED_DIMENSIONS[role]
    else:
        dims = list(TACTICAL_DIMENSIONS.keys())

    expected = len(dims)
    available = sum(pd.notna(row.get(dim, np.nan)) for dim in dims)

    if expected == 0 or available == 0:
        return "Insufficient"

    coverage = available / expected

    if coverage >= 0.90:
        return "High"
    if coverage >= 0.67:
        return "Medium"
    if coverage >= 0.34:
        return "Low"

    return "Insufficient"


def top_role_drivers(row: pd.Series, n: int = 3) -> str:
    role = row.get("primary_role", np.nan)

    if pd.isna(role) or str(role).strip() in ["", "None", "nan"]:
        return "Sin rol táctico asignado. La capa de índices está disponible, pero no se genera explicación de rol."

    if role in ROLE_EXPECTED_DIMENSIONS:
        dims = ROLE_EXPECTED_DIMENSIONS[role]
    else:
        dims = list(TACTICAL_DIMENSIONS.keys())

    values = []

    for dim in dims:
        val = row.get(dim, np.nan)
        if pd.notna(val):
            values.append((dim, float(val)))

    values = sorted(values, key=lambda x: x[1], reverse=True)

    if not values:
        return "Sin señal táctica suficiente para explicar el rol."

    readable = []
    for dim, val in values[:n]:
        label = (
            dim.replace("_index_role", "")
            .replace("_index", "")
            .replace("_", " ")
            .title()
        )
        readable.append(f"{label} P{val:.0f}")

    return "Rol explicado principalmente por: " + " · ".join(readable)


def create_role_labels_merge(fbref: pd.DataFrame, roles: pd.DataFrame | None) -> pd.DataFrame:
    if roles is None:
        return fbref

    info = infer_role_label_columns(roles)

    if not info["player_col"] or not info["season_col"]:
        warnings.warn("No se pudieron inferir columnas de merge en player_role_labels.csv")
        return fbref

    fbref = fbref.copy()
    roles = roles.copy()

    fbref["_merge_key"] = build_match_key(
        fbref,
        player_col="player",
        team_col="team",
        season_col="season",
    )

    roles["_merge_key"] = build_match_key(
        roles,
        player_col=info["player_col"],
        team_col=info["team_col"],
        season_col=info["season_col"],
    )

    role_cols = [
        c for c in [
            "_merge_key",
            "primary_role",
            "secondary_role",
            "role_confidence",
            "role_purity",
            "role_ambiguity",
            "primary_role_similarity",
            "secondary_role_similarity",
            "positional_taxonomy",
            "expected_taxonomy",
            "assigned_taxonomy",
        ]
        if c in roles.columns
    ]

    roles_small = roles[role_cols].drop_duplicates("_merge_key")

    merged = fbref.merge(
        roles_small,
        on="_merge_key",
        how="left",
        validate="many_to_one",
    )

    merged = merged.drop(columns=["_merge_key"], errors="ignore")

    return merged


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    REPORTS_ROLES.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Loading advanced FBref dataset: {FBREF_ADVANCED_PATH}")
    fbref = read_fbref_advanced()

    print(f"[INFO] FBref advanced shape: {fbref.shape}")

    roles = read_role_labels()
    if roles is not None:
        print(f"[INFO] Role labels shape: {roles.shape}")

    df = create_role_labels_merge(fbref, roles)

    print(f"[INFO] Dataset after role merge: {df.shape}")

    group_cols = ["pos_", "league"]

    coverage_rows = []

    for dimension, cols in TACTICAL_DIMENSIONS.items():
        values, used = build_dimension(
            df=df,
            dimension=dimension,
            columns=cols,
            group_cols=group_cols,
        )

        df[dimension] = values

        coverage_rows.append(
            {
                "dimension": dimension,
                "candidate_columns": len(cols),
                "used_columns_n": len(used),
                "used_columns": " | ".join(used),
                "coverage_pct": round(float(values.notna().mean() * 100), 2),
                "mean": round(float(values.mean(skipna=True)), 2)
                if values.notna().any()
                else np.nan,
            }
        )

    index_cols = list(TACTICAL_DIMENSIONS.keys())

    df["role_fit_explainability_score"] = df.apply(role_fit, axis=1)
    df["role_explainability_quality"] = df.apply(role_quality, axis=1)
    df["role_explanation_text"] = df.apply(top_role_drivers, axis=1)

    df["dominant_tactical_dimension"] = df[index_cols].idxmax(axis=1)
    df["dominant_tactical_score"] = df[index_cols].max(axis=1)

    df.to_parquet(OUTPUT_PARQUET, index=False)

    output_cols = [c for c in ID_COLS_OUTPUT if c in df.columns]
    output_cols += index_cols + [
        "role_fit_explainability_score",
        "role_explainability_quality",
        "dominant_tactical_dimension",
        "dominant_tactical_score",
        "role_explanation_text",
    ]

    player_dna = df[output_cols].copy()
    player_dna.to_csv(OUTPUT_DNA_CSV, index=False)

    coverage = pd.DataFrame(coverage_rows)
    coverage.to_csv(OUTPUT_COVERAGE_CSV, index=False)

    role_col = find_role_column(df)

    if role_col:
        df_roles_only = df[
            df[role_col].notna()
            & ~df[role_col].astype(str).str.strip().isin(["", "None", "nan"])
        ].copy()

        summary = (
            df_roles_only.groupby(role_col, dropna=False)
            .agg(
                observations=("player", "size"),
                players=("player", "nunique"),
                avg_role_fit=("role_fit_explainability_score", "mean"),
                high_quality_pct=(
                    "role_explainability_quality",
                    lambda s: round((s == "High").mean() * 100, 2),
                ),
                avg_finishing=("finishing_index_role", "mean"),
                avg_chance_creation=("chance_creation_index", "mean"),
                avg_ball_progression=("ball_progression_index", "mean"),
                avg_passing_security=("passing_security_index", "mean"),
                avg_passing_volume=("passing_volume_index", "mean"),
                avg_crossing_width=("crossing_width_index", "mean"),
                avg_availability=("availability_index_role", "mean"),
            )
            .reset_index()
            .sort_values("avg_role_fit", ascending=False)
        )

        no_role_summary = pd.DataFrame(
            {
                "metric": [
                    "rows_without_role",
                    "pct_without_role",
                ],
                "value": [
                    int(df[role_col].isna().sum()),
                    round(float(df[role_col].isna().mean() * 100), 2),
                ],
            }
        )
        no_role_summary.to_csv(REPORTS_ROLES / "role_explainability_no_role_summary.csv", index=False)

    else:
        summary = pd.DataFrame(
            {
                "warning": [
                    "No se encontró primary_role tras el merge. Revisar claves entre FBref avanzado y player_role_labels.csv."
                ]
            }
        )

    summary.to_csv(OUTPUT_SUMMARY_CSV, index=False)
    summary.to_csv(OUTPUT_ROLE_PROFILES_CSV, index=False)

    print("[OK] Role Explainability Engine v2 generated")
    print(f"[OK] Output parquet: {OUTPUT_PARQUET}")
    print(f"[OK] Player DNA CSV: {OUTPUT_DNA_CSV}")
    print(f"[OK] Summary CSV: {OUTPUT_SUMMARY_CSV}")
    print(f"[OK] Coverage CSV: {OUTPUT_COVERAGE_CSV}")

    print("\n[INFO] Coverage")
    print(coverage.to_string(index=False))

    print("\n[INFO] Quality distribution")
    print(df["role_explainability_quality"].value_counts(dropna=False).to_string())

    if "primary_role" in df.columns:
        print("\n[INFO] Role match coverage")
        print(f"Rows with primary_role: {df['primary_role'].notna().mean() * 100:.2f}%")

    print("\n[INFO] Sample")
    sample_cols = [
        "player",
        "team",
        "league",
        "season",
        "pos_",
        "primary_role",
        "finishing_index_role",
        "chance_creation_index",
        "ball_progression_index",
        "passing_security_index",
        "availability_index_role",
        "role_fit_explainability_score",
        "role_explainability_quality",
        "role_explanation_text",
    ]
    sample_cols = [c for c in sample_cols if c in df.columns]
    print(df[sample_cols].head(20).to_string(index=False))


if __name__ == "__main__":
    main()