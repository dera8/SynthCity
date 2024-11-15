# generate_trips_dataset.py
import xml.etree.ElementTree as ET
import csv
import sys
from datetime import datetime

def generate_trips_dataset(trips_file, selected_types, selected_date, output_csv):
    selected_types_set = set(selected_types.split(","))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    rows = []
    tree = ET.parse(trips_file)
    root = tree.getroot()

    for tripinfo in root.findall("tripinfo"):
        if tripinfo.get("type") in selected_types_set or tripinfo.get("vType") in selected_types_set:
            depart = selected_date.strftime('%Y-%m-%d') + " " + tripinfo.get("depart", "00:00:00")
            arrival = selected_date.strftime('%Y-%m-%d') + " " + tripinfo.get("arrival", "00:00:00")

            rows.append({
                "id": tripinfo.get("id"),
                "depart": depart,
                "arrival": arrival,
                "duration": tripinfo.get("duration"),
                "routeLength": tripinfo.get("routeLength"),
                "timeLoss": tripinfo.get("timeLoss").split(".")[0],
                "speedFactor": tripinfo.get("speedFactor"),
                "waitingTime": tripinfo.get("waitingTime")
            })

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Trips dataset saved as {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_trips_dataset.py <trips_file> <selected_types> <date> <output_csv>")
    else:
        generate_trips_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
