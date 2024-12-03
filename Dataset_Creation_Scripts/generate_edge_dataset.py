import xml.etree.ElementTree as ET
import csv
import sys
import json
from datetime import datetime


def generate_edge_dataset(edge_file, taz_file, output_csv, date_str):
    """
    Generate a dataset from edge and TAZ XML files, and save as CSV.

    Parameters:
    - edge_file: Path to the edge XML file.
    - taz_file: Path to the TAZ XML file.
    - output_csv: Path to save the generated CSV file.
    - date_str: Date string in 'YYYY-MM-DD' format to include in the dataset.
    """
    try:
        # Parse the input date
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Parse XML files
        print("Parsing XML files...")
        edge_tree = ET.parse(edge_file)
        edge_root = edge_tree.getroot()
        taz_tree = ET.parse(taz_file)
        taz_root = taz_tree.getroot()

        # Extract TAZ data
        print("Extracting TAZ data...")
        taz_data = {
            edge_id: taz.get("id", "")
            for taz in taz_root.findall("taz")
            for edge_id in taz.get("edges", "").split()
        }

        # Process edge data
        rows = []
        print("Processing edge data...")
        for interval in edge_root.findall("interval"):
            for edge in interval.findall("edge"):
                edge_id = edge.get("id")
                rows.append({
                    "date": str(date),  # Convert date to string
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

        # Write to CSV
        print(f"Saving dataset to {output_csv}...")
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"Edge dataset successfully saved as {output_csv}")
        return rows

    except Exception as e:
        print(f"Error: {e}")


def save_descriptor(rows, output_csv):
    """
    Automatically save a JSON descriptor of the dataset.

    Parameters:
    - rows: List of dictionaries containing dataset rows.
    - output_csv: Path to the output CSV file.
    """
    descriptor_file = output_csv.replace(".csv", ".json")
    print(f"Saving JSON descriptor to {descriptor_file}...")

    # Convert date fields in the descriptor to strings
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
Usage: python generate_edge_dataset.py <edge_file> <taz_file> <output_csv> <date>

Example:
    python generate_edge_dataset.py edges.xml taz.xml output.csv 2022-04-14
    """)


if __name__ == "__main__":
    if "--help" in sys.argv:
        print_help()
        sys.exit(0)

    # Validate arguments
    if len(sys.argv) < 5:
        print_help()
        sys.exit(1)

    # Extract parameters
    edge_file = sys.argv[1]
    taz_file = sys.argv[2]
    output_csv = sys.argv[3]
    date_str = sys.argv[4]

    # Generate dataset
    dataset_rows = generate_edge_dataset(edge_file, taz_file, output_csv, date_str)

    # Automatically generate JSON descriptor
    save_descriptor(dataset_rows, output_csv)
