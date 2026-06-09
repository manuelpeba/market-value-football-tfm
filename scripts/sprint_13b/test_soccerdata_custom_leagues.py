import soccerdata as sd

print("\nAvailable FBref leagues:")
for league in sd.FBref.available_leagues():
    print("-", league)

CUSTOM_LEAGUES = [
    "NED-Eredivisie",
    "POR-Primeira Liga",
    "ENG-Championship",
    "BEL-Belgian Pro League",
    "AUT-Austrian Bundesliga",
    "ESP-Segunda División",
]

print("\nCustom league test:")

for league in CUSTOM_LEAGUES:
    print(f"\n=== {league} ===")
    try:
        fbref = sd.FBref(leagues=[league], seasons=["2025-2026"])
        df = fbref.read_player_season_stats(stat_type="shooting")
        print("OK", df.shape)
        print(df.head(2))
    except Exception as exc:
        print("ERROR", repr(exc))