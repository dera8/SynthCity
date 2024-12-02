import zipfile
import random
import sys
import csv
import os
import json
from datetime import datetime
import argparse


def delete_percentage_of_trips(gtfs_zip, route_id, percentage, output_zip):
    """
    Delete a percentage of trips from a GTFS file based on the specified route.

    Parameters:
        gtfs_zip (str): Path to the GTFS ZIP file.
        route_id (str): Route ID to filter trips.
        percentage (float): Percentage of trips to delete.
        output_zip (str): Path to the output GTFS ZIP file.

    Returns:
        int: Number of trips deleted.
    """
    temp_dir = "temp_gtfs"
    percentage = float(percentage) / 100
    trips_deleted = 0

    # Extract GTFS ZIP file
    with zipfile.ZipFile(gtfs_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    trips_file = os.path.join(temp_dir, "trips.txt")
    modified_trips_file = os.path.join(temp_dir, "modified_trips.txt")

    # Check if the route_id exists and delete trips
    route_exists = False
    with open(trips_file, 'r') as file, open(modified_trips_file, 'w', newline='') as out_file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['route_id'] == route_id:
                route_exists = True
                if random.random() < percentage:
                    trips_deleted += 1
                    continue  # Skip this row to "delete" it
            writer.writerow(row)

    if not route_exists:
        print(f"Error: Route ID '{route_id}' not found in trips.txt.")
        clean_temp_files(temp_dir)
        sys.exit(1)

    if trips_deleted == 0:
        print(f"No trips deleted for Route ID '{route_id}'. Check the percentage value.")
    else:
        print(f"{trips_deleted} trips deleted for Route ID '{route_id}'.")

    os.replace(modified_trips_file, trips_file)

    # Create a new ZIP file with the modified data
    with zipfile.ZipFile(output_zip, 'w') as zip_ref:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    clean_temp_files(temp_dir)
    print(f"Modified GTFS archive created as {output_zip}")
    return trips_deleted


def clean_temp_files(temp_dir):
    """
    Clean up temporary files and directories.

    Parameters:
        temp_dir (str): Path to the temporary directory.
    """
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def generate_json_descriptor(output_zip, route_id, percentage, trips_deleted):
    """
    Generate a JSON descriptor for the modification.

    Parameters:
        output_zip (str): Path to the modified GTFS ZIP file.
        route_id (str): Route ID affected by the modification.
        percentage (float): Percentage of trips deleted.
        trips_deleted (int): Number of trips deleted.

    Returns:
        str: Path to the JSON descriptor file.
    """
    descriptor_file = output_zip.replace(".zip", ".json")
    descriptor = {
        "description": "GTFS modification: Delete a percentage of trips.",
        "timestamp": datetime.now().isoformat(),
        "route_id": route_id,
        "percentage_deleted": percentage,
        "trips_deleted": trips_deleted,
        "output_file": output_zip
    }

    with open(descriptor_file, 'w') as json_file:
        json.dump(descriptor, json_file, indent=4)

    print(f"JSON descriptor saved as {descriptor_file}")
    return descriptor_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete a percentage of trips from a GTFS file based on the specified route.",
        epilog="Example: python public_transport_anomaly.py gtfs.zip route_1 20 modified_gtfs.zip"
    )
    parser.add_argument("gtfs_zip", help="Path to the GTFS ZIP file.")
    parser.add_argument("route_id", help="Route ID to filter trips.")
    parser.add_argument("percentage", type=float, help="Percentage of trips to delete (0-100).")
    parser.add_argument("output_zip", help="Path to the output GTFS ZIP file.")

    args = parser.parse_args()

    trips_deleted = delete_percentage_of_trips(args.gtfs_zip, args.route_id, args.percentage, args.output_zip)
    generate_json_descriptor(args.output_zip, args.route_id, args.percentage, trips_deleted)
