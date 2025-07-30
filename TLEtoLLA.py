from sgp4.api import Satrec, jday
from datetime import datetime
import requests
import numpy as np
import json
import os
from math import degrees, atan2, sqrt, asin

def fetch_and_process_tle(url, system):
    response = requests.get(url)
    tle_data = response.text.strip().splitlines()

    satellites = []
    for i in range(0, len(tle_data), 3):
        name = tle_data[i].strip()
        line1 = tle_data[i + 1].strip()
        line2 = tle_data[i + 2].strip()

        satrec = Satrec.twoline2rv(line1, line2)

        now = datetime.utcnow()
        jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond * 1e-6)

        e, r, v = satrec.sgp4(jd, fr)
        if e != 0:
            continue

        gmst = (18.697374558 + 24.06570982441908 * (jd + fr - 2451545.0)) % 24
        theta = gmst * (np.pi / 12.0)
        x, y, z = r
        xe = x * np.cos(theta) + y * np.sin(theta)
        ye = -x * np.sin(theta) + y * np.cos(theta)
        ze = z

        r_mag = sqrt(xe**2 + ye**2 + ze**2)
        lat = degrees(asin(ze / r_mag))
        lon = degrees(atan2(ye, xe))
        alt = r_mag - 6371

        satellites.append({
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "altitude": round(alt, 4),
            "system": system.upper(),
            "name": name.lower().replace(" ", "-")
        })

    return satellites

# Main interaction
output_file = "src/classes/satellites.json"


# Load existing data if available, handle empty or invalid JSON
if os.path.exists(output_file):
    try:
        with open(output_file, "r") as f:
            content = f.read().strip()
            if content:
                all_satellites = json.loads(content)
            else:
                all_satellites = []
    except Exception:
        all_satellites = []
else:
    all_satellites = []

while True:
    url = input("Enter the TLE URL for the GNSS system (or 'done' to finish): ").strip()
    if url.lower() == 'done':
        break

    system = input("Enter the name of the GNSS system (e.g. GPS, GLONASS, Galileo): ").strip()
    
    try:
        new_sats = fetch_and_process_tle(url, system)
        all_satellites += new_sats
        print(f"Added {len(new_sats)} satellites from {system}.")
    except Exception as e:
        print(f"Error processing {system}: {e}")

# Save all satellites to file
with open(output_file, "w") as f:
    json.dump(all_satellites, f, indent=2)

print(f"\nAll satellite data saved to {output_file}")
