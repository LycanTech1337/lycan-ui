import json

# Input and output file names
input_file = "src/classes/satellites.json"
output_file = "satellites.geojson"

try:
    # Load the original satellite data
    with open(input_file, "r") as f:
        satellites = json.load(f)

    # Convert to GeoJSON format
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for sat in satellites:
        feature = {
            "type": "Feature",
            "properties": {
                "name": sat.get("name"),
                "system": sat.get("system"),
                "altitude": sat.get("altitude")
            },
            "geometry": {
                "type": "Point",
                "coordinates": [sat["lon"], sat["lat"]]  # GeoJSON expects [lon, lat]
            }
        }
        geojson["features"].append(feature)

    # Write GeoJSON to output file
    with open(output_file, "w") as f:
        json.dump(geojson, f, indent=2)

    print(f"GeoJSON file created: {output_file}")

except FileNotFoundError:
    print(f"Input file '{input_file}' not found.")
except json.JSONDecodeError:
    print(f"Input file '{input_file}' is not valid JSON.")
except Exception as e:
    print(f"An error occurred: {e}")
