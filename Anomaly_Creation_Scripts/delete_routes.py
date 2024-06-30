import csv
import random
import zipfile
from io import TextIOWrapper
import os

# Function to load GTFS data from a zip file
def load_gtfs_data_from_zip(zip_filename, txt_filename):
    with zipfile.ZipFile(zip_filename, 'r') as z:
        with z.open(txt_filename) as file:
            reader = csv.DictReader(TextIOWrapper(file, 'utf-8'))
            data = list(reader)
    return data, reader.fieldnames

# Function to save GTFS data to a zip file without creating blank rows
def save_gtfs_data_to_zip(zip_filename, txt_filename, data, fieldnames):
    temp_zip_filename = f"modified_{zip_filename}"
    with zipfile.ZipFile(zip_filename, 'r') as z:
        with zipfile.ZipFile(temp_zip_filename, 'w') as new_z:
            for item in z.infolist():
                if item.filename != txt_filename:
                    new_z.writestr(item, z.read(item.filename))
            with new_z.open(txt_filename, 'w') as file:
                writer = csv.DictWriter(TextIOWrapper(file, 'utf-8', newline=''), fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
    return temp_zip_filename

# Function to delete routes based on route IDs
def delete_routes(data, routes_to_delete):
    return [row for row in data if row['route_id'] not in routes_to_delete]

# Function to delete a percentage of trips for a specific route
def delete_percentage_of_trips_from_route(data, route_id, percentage):
    trip_ids = list({row['trip_id'] for row in data if row['route_id'] == route_id})
    num_to_delete = int(len(trip_ids) * (percentage / 100))
    trips_to_delete = set(random.sample(trip_ids, num_to_delete))
    return [row for row in data if not (row['route_id'] == route_id and row['trip_id'] in trips_to_delete)]

# Function to validate the route ID against the trips.txt data
def validate_route_id(route_id, data):
    return any(row['route_id'] == route_id for row in data)

# Main function
def main():
    # Prompt the user to enter the GTFS zip filename and validate it
    while True:
        gtfs_zip_filename = input("Enter the GTFS zip filename: ")
        if os.path.isfile(gtfs_zip_filename) and gtfs_zip_filename.endswith('.zip'):
            break
        else:
            print("Invalid filename. Please enter a valid GTFS zip filename.")

    txt_filename = 'trips.txt'

    data, fieldnames = load_gtfs_data_from_zip(gtfs_zip_filename, txt_filename)

    # Present options to the user
    print("Choose an option:")
    print("1. Delete entire routes")
    print("2. Delete a percentage of trips from a specific route")
    choice = input("Enter 1 or 2: ")

    # Process the user's choice
    if choice == '1':
        # If the user chose to delete routes, ask for route IDs to delete
        while True:
            routes_to_delete = input("Enter route IDs to delete (comma separated, case sensitive): ").split(',')
            routes_to_delete = [route.strip() for route in routes_to_delete]
            if all(validate_route_id(route, data) for route in routes_to_delete):
                break
            else:
                print("Error: One or more Route IDs are not found in the data. Please re-enter the correct Route IDs.")
        modified_data = delete_routes(data, routes_to_delete)
    elif choice == '2':
        while True:
            try:
                # If the user chose to delete a percentage of trips, ask for the route ID and the percentage
                route_id = input("Enter the route ID to delete a percentage of trips from (case sensitive): ").strip()
                if not validate_route_id(route_id, data):
                    raise ValueError("Route ID not found in the data.")
                percentage = float(input("Enter the percentage of trips to delete: ").strip())
                if percentage < 0 or percentage > 100:
                    raise ValueError("Percentage must be between 0 and 100.")
                break
            except ValueError as e:
                print(f"Error: {e}")
        modified_data = delete_percentage_of_trips_from_route(data, route_id, percentage)
    else:
        print("Invalid choice.")
        return

    # Save the modified GTFS data to a new zip file
    new_zip_filename = save_gtfs_data_to_zip(gtfs_zip_filename, txt_filename, modified_data, fieldnames)
    if new_zip_filename:
        print(f"Modified GTFS data saved to {new_zip_filename}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()




