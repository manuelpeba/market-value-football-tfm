import inspect
import soccerdata as sd

print("\n=== FBref public methods ===\n")

for name in sorted(dir(sd.FBref)):
    if name.startswith("_"):
        continue

    attr = getattr(sd.FBref, name)

    if callable(attr):
        try:
            print(f"\n{name}")
            print(inspect.signature(attr))
        except:
            pass