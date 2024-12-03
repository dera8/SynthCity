import xml.etree.ElementTree as ET
import csv
import sys
import json
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

    # Write to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Trips dataset saved as {output_csv}")
    return rows

def save_descriptor(rows, output_csv):
    """
    Automatically save a JSON descriptor of the dataset.

    Parameters:
    - rows: List of dictionaries containing dataset rows.
    - output_csv: Path to the output CSV file.
    """
    descriptor_file = output_csv.replace(".csv", ".json")
    print(f"Saving JSON descriptor to {descriptor_file}...")

    # Convert any date fields in the dataset to strings in the descriptor
    descriptor = {
        "fields": list(rows[0].keys()) if rows else [],
        "row_count": len(rows),
        "example_row": {key: str(value) if isinstance(value, datetime) else value for key, value in (rows[0].items() if rows else {})},  # Convert dates to strings
        "source_csv": output_csv
    }

    with open(descriptor_file, 'w') as json_file:
        json.dump(descriptor, json_file, indent=4)

    print(f"JSON descriptor saved as {descriptor_file}")

def print_help():
    """
    Print the usage help message.
    """
    print("""
Usage: python generate_trips_dataset.py <trips_file> <selected_types> <date> <output_csv>

Example:
    python generate_trips_dataset.py trips.xml bus,truck 2022-04-14 output.csv
    """)

if __name__ == "__main__":
    if "--help" in sys.argv:
        print_help()
        sys.exit(0)

    # Validate arguments
    if len(sys.argv) != 5:
        print_help()
        sys.exit(1)

    # Extract parameters
    trips_file = sys.argv[1]
    selected_types = sys.argv[2]
    selected_date = sys.argv[3]
    output_csv = sys.argv[4]

    # Generate dataset
    dataset_rows = generate_trips_dataset(trips_file, selected_types, selected_date, output_csv)

    # Automatically generate JSON descriptor
    save_descriptor(dataset_rows, output_csv)
