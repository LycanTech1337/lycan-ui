import json
from collections import Counter

# Path to the output file from the previous script
filename = "satellites.json"

try:
    with open(filename, "r") as f:
        satellites = json.load(f)

    total = len(satellites)
    print(f"Total satellites in file: {total}")

    # Optional: Breakdown by system
    system_counts = Counter(sat["system"] for sat in satellites)
    print("\nBreakdown by GNSS system:")
    for system, count in system_counts.items():
        print(f"  {system}: {count}")

except FileNotFoundError:
    print(f"File '{filename}' not found.")
except json.JSONDecodeError:
    print(f"File '{filename}' is not valid JSON.")
