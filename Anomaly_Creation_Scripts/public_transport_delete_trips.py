# public_transport_anomaly.py
import zipfile
import random
import sys
import csv
import os

def delete_percentage_of_trips(gtfs_zip, route_id, percentage):
    temp_dir = "temp_gtfs"
    percentage = float(percentage) / 100
    output_zip = f"modified_{gtfs_zip}"

    with zipfile.ZipFile(gtfs_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    trips_file = os.path.join(temp_dir, "trips.txt")
    modified_trips_file = os.path.join(temp_dir, "modified_trips.txt")

    with open(trips_file, 'r') as file, open(modified_trips_file, 'w', newline='') as out_file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['route_id'] == route_id and random.random() < percentage:
                continue
            writer.writerow(row)

    os.replace(modified_trips_file, trips_file)

    with zipfile.ZipFile(output_zip, 'w') as zip_ref:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                zip_ref.write(os.path.join(root, file), file)

    print(f"Modified GTFS archive created as {output_zip}")

    # Clean up temporary files
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python public_transport_anomaly.py <gtfs_zip> <route_id> <percentage>")
    else:
        delete_percentage_of_trips(sys.argv[1], sys.argv[2], sys.argv[3])