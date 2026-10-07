import csv

def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

key = {r["file"]: r["error"] for r in load("answer_key.csv")}
flagged = {r["file"]: r["reason"] for r in load("output/exceptions.csv")}

expected = {f: e for f, e in key.items() if e}
caught = [f for f in expected if flagged.get(f) == expected[f]]
missed = [f for f in expected if f not in caught]
false_pos = [f for f in flagged if f not in expected]

print(f"Injected errors: {len(expected)}")
print(f"Caught correctly: {len(caught)}")
print(f"Missed: {missed}")
print(f"False positives: {false_pos}")