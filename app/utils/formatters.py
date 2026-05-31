COLUMN_TRANSLATIONS = {
    "player_name_fbref": "Jugador",
    "player_name_tm": "Jugador TM",
    "club": "Club",
    "league": "Liga",
    "season": "Temporada",
    "position_group": "Posición",
    "age": "Edad",
    "minutes_played": "Minutos",
    "market_value_eur": "Valor mercado (€)",
    "predicted_market_value_eur": "Valor estimado (€)",
    "market_value_gap_eur": "Gap mercado (€)",
    "market_value_gap_pct": "Gap mercado (%)",
    "inefficiency_score": "Inefficiency Score",
    "growth_score": "Growth Score",
    "confidence_score": "Confidence Score",
    "opportunity_score": "Opportunity Score",
    "opportunity_tier": "Tier oportunidad",
}


def translate_columns(df):
    return df.rename(columns=COLUMN_TRANSLATIONS)