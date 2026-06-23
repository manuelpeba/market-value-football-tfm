from pathlib import Path
import re

p = Path("app/streamlit_app.py")
s = p.read_text(encoding="utf-8")
p.with_suffix(".py.bak_tm697_fix_role_market_dynamic_map").write_text(s, encoding="utf-8")

old = '''    families = {
        "DEF": ["Ball-Playing Centre-Back", "Aerial Defender", "Aggressive Defender"],
        "MID": ["Ball Winner", "Attacking Progressor", "Creative Playmaker"],
        "ATT": ["Box Finisher", "Creator Forward", "Mobile Forward"],
    }
    family_cards = []
    for fam, roles in families.items():
        available_roles = [r for r in roles if r in role_values]
        if not available_roles:
            continue
        pills = "".join(f"<span class='role-map-pill {'role-map-pill-active' if r == selected_role else ''}'>{html.escape(r)}</span>" for r in available_roles)
        fam_label = {"DEF": "DEFENDERS" if LANG == "EN" else "DEFENSAS", "MID": "MIDFIELDERS" if LANG == "EN" else "CENTROCAMPISTAS", "ATT": "FORWARDS" if LANG == "EN" else "ATACANTES"}[fam]
        family_cards.append(f"<div class='role-map-family'><b>{fam_label}</b><div>{pills}</div></div>")'''

new = '''    # TM.6.9.7: dynamic role map. Cloud may load the newer role taxonomy
    # (Ball Progressor, Defensive Anchor, Box-to-Box Engine), while older local
    # exports used the 9-role tactical taxonomy. Do not hardcode only one schema.
    def _role_market_family(role_label: object) -> str:
        key = normalize_join_text(role_label)

        if any(x in key for x in [
            "centre back", "center back", "aerial defender", "aggressive defender",
            "defensive anchor", "defender", "stopper", "anchor"
        ]):
            return "DEF"

        if any(x in key for x in [
            "box finisher", "creator forward", "mobile forward", "forward",
            "finisher", "striker", "wing", "attacker"
        ]):
            return "ATT"

        # Default for the current role-discovery taxonomy:
        # Ball Progressor, Ball Winner, Box-to-Box Engine, Creative Playmaker,
        # Attacking Progressor.
        return "MID"

    family_order = ["DEF", "MID", "ATT"]
    family_roles = {fam: [] for fam in family_order}

    for role in role_values:
        if not is_valid_role_value(role):
            continue
        fam = _role_market_family(role)
        family_roles.setdefault(fam, []).append(str(role))

    # Stable order inside each family: selected first, then by visible count.
    role_counts = (
        df_roles["primary_role"].dropna().astype(str).value_counts().to_dict()
        if "primary_role" in df_roles.columns else {}
    )

    family_cards = []
    for fam in family_order:
        available_roles = family_roles.get(fam, [])
        if not available_roles:
            continue

        available_roles = sorted(
            available_roles,
            key=lambda r: (0 if str(r) == str(selected_role) else 1, -int(role_counts.get(r, 0)), str(r))
        )

        pills = "".join(
            f"<span class='role-map-pill {'role-map-pill-active' if r == selected_role else ''}'>{html.escape(r)}</span>"
            for r in available_roles
        )
        fam_label = {
            "DEF": "DEFENDERS" if LANG == "EN" else "DEFENSAS",
            "MID": "MIDFIELDERS" if LANG == "EN" else "CENTROCAMPISTAS",
            "ATT": "FORWARDS" if LANG == "EN" else "ATACANTES",
        }[fam]
        family_cards.append(f"<div class='role-map-family'><b>{fam_label}</b><div>{pills}</div></div>")'''

if old not in s:
    raise SystemExit("ERROR: bloque hardcodeado de families no encontrado")

s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("OK: Role Market map now uses dynamic Cloud/local role taxonomy")
