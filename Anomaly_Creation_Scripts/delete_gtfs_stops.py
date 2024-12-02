import argparse
import csv
import zipfile
import os
import shutil
import json
from datetime import datetime


def delete_stops(gtfs_file, stops_to_delete, output_file):
    """
    Delete specific stops from a GTFS stops.txt file and generate a JSON descriptor.

    Parameters:
        gtfs_file (str): Path to the GTFS zip file.
        stops_to_delete (list): List of stop IDs to delete.
        output_file (str): Path to save the updated GTFS zip file.

    Returns:
        str: Path to the JSON descriptor file.
    """
    with zipfile.ZipFile(gtfs_file, 'r') as gtfs_zip:
        # Extract stops.txt into a temporary directory
        try:
            with gtfs_zip.open('stops.txt') as stops_file:
                stops_data = list(csv.DictReader(line.decode('utf-8') for line in stops_file))
        except KeyError:
            raise FileNotFoundError("The GTFS zip file does not contain a stops.txt file.")

        # Find the existing stop IDs
        existing_stop_ids = {stop['stop_id'] for stop in stops_data}

        # Check if all stops to delete exist
        invalid_stops = [stop for stop in stops_to_delete if stop not in existing_stop_ids]
        if invalid_stops:
            raise ValueError(f"The following stop IDs do not exist in stops.txt: {', '.join(invalid_stops)}")

        # Filter out the stops to delete
        updated_stops = [stop for stop in stops_data if stop['stop_id'] not in stops_to_delete]

        # Write the updated stops.txt file
        temp_dir = "temp_gtfs"
        os.makedirs(temp_dir, exist_ok=True)
        updated_stops_file = os.path.join(temp_dir, 'stops.txt')

        with open(updated_stops_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=stops_data[0].keys())
            writer.writeheader()
            writer.writerows(updated_stops)

        # Copy all files from the original GTFS zip, replacing stops.txt
        with zipfile.ZipFile(output_file, 'w') as updated_gtfs_zip:
            for file_name in gtfs_zip.namelist():
                if file_name != 'stops.txt':
                    with gtfs_zip.open(file_name) as file_content:
                        updated_gtfs_zip.writestr(file_name, file_content.read())

            # Add the updated stops.txt
            with open(updated_stops_file, 'rb') as f:
                updated_gtfs_zip.writestr('stops.txt', f.read())

    # Cleanup temporary directory
    shutil.rmtree(temp_dir)

    # Generate JSON descriptor
    json_descriptor_file = generate_json_descriptor(output_file, stops_to_delete)
    print(f"Updated GTFS file saved as {output_file}")
    print(f"JSON descriptor saved as {json_descriptor_file}")


def generate_json_descriptor(output_file, stops_deleted):
    """
    Generate a JSON descriptor file with details of the operation.

    Parameters:
        output_file (str): Path to the updated GTFS zip file.
        stops_deleted (list): List of stops deleted.

    Returns:
        str: Path to the JSON descriptor file.
    """
    json_file = output_file.replace(".zip", ".json")
    descriptor = {
        "description": "Stops deletion operation in GTFS file.",
        "timestamp": datetime.now().isoformat(),
        "output_file": output_file,
        "stops_deleted": stops_deleted
    }

    with open(json_file, 'w') as f:
        json.dump(descriptor, f, indent=4)

    return json_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete specific stops from a GTFS stops.txt file and generate a JSON descriptor.",
        epilog="Example: python delete_gtfs_stops.py gtfs.zip updated_gtfs.zip 1234 5678"
    )
    parser.add_argument("gtfs_file", help="Path to the input GTFS zip file.")
    parser.add_argument("output_file", help="Path to the output GTFS zip file.")
    parser.add_argument("stops", nargs='+', help="Stop IDs to delete.")
    args = parser.parse_args()

    try:
        delete_stops(args.gtfs_file, args.stops, args.output_file)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except zipfile.BadZipFile:
        print("Error: Invalid GTFS zip file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
