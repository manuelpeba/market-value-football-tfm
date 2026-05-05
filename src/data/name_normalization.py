import re
import unicodedata

def normalize_name(name):
    if name is None:
        return ""

    name = str(name).lower().strip()
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^a-z\s]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name