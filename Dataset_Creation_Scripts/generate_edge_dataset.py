# generate_edge_dataset.py
import xml.etree.ElementTree as ET
import csv
import sys
from datetime import datetime

def generate_edge_dataset(edge_file, taz_file, output_csv, date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    edge_tree = ET.parse(edge_file)
    edge_root = edge_tree.getroot()
    taz_tree = ET.parse(taz_file)
    taz_root = taz_tree.getroot()

    taz_data = {edge_id: taz.get("id", "") for taz in taz_root.findall("taz") for edge_id in taz.get("edges", "").split()}

    rows = []
    for interval in edge_root.findall("interval"):
        for edge in interval.findall("edge"):
            edge_id = edge.get("id")
            rows.append({
                "date": date,
                "interval_begin": interval.get("begin"),
                "interval_end": interval.get("end"),
                "edge_id": edge_id,
                "entered": edge.get("entered", "0"),
                "left": edge.get("left", "0"),
                "traveltime": edge.get("traveltime", "0"),
                "density": edge.get("density", "0"),
                "occupancy": edge.get("occupancy", "0"),
                "speed": edge.get("speed", "0"),
                "taz": taz_data.get(edge_id, "")
            })

    with open(output_csv, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Edge dataset saved as {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_edge_dataset.py <edge_file> <taz_file> <output_csv> <date>")
    else:
        generate_edge_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])