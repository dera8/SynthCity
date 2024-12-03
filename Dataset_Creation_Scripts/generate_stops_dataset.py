import pandas as pd
import sys
from datetime import datetime
import json

def main():
    try:
        # Check for --help argument
        if '--help' in sys.argv:
            print_help()
            return

        # Validate the number of arguments
        if len(sys.argv) != 7:
            print_help()
            return
        
        # Extract parameters from command-line arguments
        stopout_filename = sys.argv[1]
        gtfs_path = sys.argv[2]
        custom_gtfs_stops_file = sys.argv[3]
        arrival_date = sys.argv[4]
        departure_date = sys.argv[5]
        stopinfo_started_date = sys.argv[6]

        # Validate the date format (dd/mm/yyyy)
        arrival_date = validate_date_format(arrival_date)
        departure_date = validate_date_format(departure_date)
        stopinfo_started_date = validate_date_format(stopinfo_started_date)

        # Read data from CSV files
        csv_stops = pd.read_csv(f"{gtfs_path}/stops.txt", sep=',', dtype='unicode')
        csv_stop_times = pd.read_csv(f"{gtfs_path}/stop_times.txt", sep=',', dtype='unicode')
        csv_trips = pd.read_csv(f"{gtfs_path}/trips.txt", sep=',', dtype='unicode')
        csv_stopout = pd.read_csv(stopout_filename, sep=';', dtype='unicode')
        csv_gtfs_stops = pd.read_csv(custom_gtfs_stops_file, sep=';', dtype='unicode')

        # File merging
        csv_stop_times_trips = csv_stop_times.merge(csv_trips, on=['trip_id'])
        csv_stoptimes_stops = csv_stop_times.merge(csv_stops, on=["stop_id"])
        csv_stoptimes_stops2 = csv_stoptimes_stops[['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_name', 'stop_sequence', 'stop_lat', 'stop_lon']]
        csv_stopout.rename(columns={'stopinfo_busStop': 'busStop_id'}, inplace=True)
        csv_stopout.rename(columns={'stopinfo_id': 'trip_id'}, inplace=True)
        csv_stopout2 = csv_stopout[['busStop_id', 'stopinfo_delay', 'stopinfo_ended', 'trip_id', 'stopinfo_initialPersons', 'stopinfo_loadedPersons', 'stopinfo_started', 'stopinfo_type', 'stopinfo_unloadedPersons']]
        csv_stops_stopout2 = csv_gtfs_stops.merge(csv_stopout2, on=["busStop_id"])
        csv_stopout3 = csv_stoptimes_stops2.merge(csv_stops_stopout2, on=["trip_id", "stop_name"])
        routes = pd.read_csv(f"{gtfs_path}/trips.txt", sep=',', dtype='unicode')
        csv_stopout4 = csv_stopout3.merge(routes, on=["trip_id"])

        # Arrival and departure time correction
        data = csv_stopout4
        data['arrival_time'] = data['arrival_time'].str.replace('^24:', '00:', regex=True)
        data['arrival_time'] = data['arrival_time'].str.replace('^25:', '01:', regex=True)
        data['arrival_time'] = data['arrival_time'].str.replace('^26:', '02:', regex=True)
        data['arrival_time'] = data['arrival_time'].str.replace('^27:', '03:', regex=True)
        data['arrival_time'] = data['arrival_time'].str.replace('^28:', '04:', regex=True)

        data['departure_time'] = data['departure_time'].str.replace('^24:', '00:', regex=True)
        data['departure_time'] = data['departure_time'].str.replace('^25:', '01:', regex=True)
        data['departure_time'] = data['departure_time'].str.replace('^26:', '02:', regex=True)
        data['departure_time'] = data['departure_time'].str.replace('^27:', '03:', regex=True)
        data['departure_time'] = data['departure_time'].str.replace('^28:', '04:', regex=True)

        data['stopinfo_started'] = data['stopinfo_started'].str.replace('^1:00:', '00:', regex=True)

        # Add date to time fields
        data['arrival_time'] = pd.to_datetime(arrival_date + ' ' + data['arrival_time'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        data['departure_time'] = pd.to_datetime(departure_date + ' ' + data['departure_time'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        data['stopinfo_started'] = pd.to_datetime(stopinfo_started_date + ' ' + data['stopinfo_started'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        # Check for null values after conversion
        if data['arrival_time'].isnull().any() or data['departure_time'].isnull().any() or data['stopinfo_started'].isnull().any():
            raise ValueError("Invalid time format. Please ensure the times are in the correct format.")

        # Rename columns
        data.rename(columns={'busStop_id': 'stop_id_SUMO'}, inplace=True)

        # Calculate SUMO delay
        data['sumo_delay'] = (data['stopinfo_started'] - data['arrival_time']).dt.total_seconds()

        # Generate output file name based on the user-provided arrival date
        arrival_date_dt = datetime.strptime(arrival_date, '%d/%m/%Y')
        file_name = f"stops_dataset_{arrival_date_dt.day}_{arrival_date_dt.strftime('%B')}_{arrival_date_dt.year}.csv"

        # Save the final synthetic dataset
        data.to_csv(file_name, index=False, sep=';')
        print(f"Dataset successfully created and saved as '{file_name}'")

        # Save the JSON descriptor
        save_descriptor(data, file_name)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path and ensure the file exists.")
    except pd.errors.ParserError as e:
        print(f"Error: {e}. There is an issue with parsing the CSV files. Please check the file format.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def validate_date_format(date_str):
    """
    Validates the date format (dd/mm/yyyy) and returns a datetime object.
    """
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Please use the format dd/mm/yyyy.")

def save_descriptor(data, output_csv):
    """
    Automatically save a JSON descriptor of the dataset.

    Parameters:
    - data: DataFrame containing dataset rows.
    - output_csv: Path to the output CSV file.
    """
    descriptor_file = output_csv.replace(".csv", ".json")
    print(f"Saving JSON descriptor to {descriptor_file}...")

    # Prepare descriptor with string conversion for datetime columns
    descriptor = {
        "fields": list(data.columns),
        "row_count": len(data),
        "example_row": data.iloc[0].to_dict() if len(data) > 0 else {},
        "source_csv": output_csv
    }

    # Convert datetime columns to string format
    for field in descriptor["example_row"]:
        if isinstance(descriptor["example_row"][field], pd.Timestamp):
            descriptor["example_row"][field] = descriptor["example_row"][field].strftime('%d/%m/%Y %H:%M:%S')

    # Write descriptor to JSON
    with open(descriptor_file, 'w') as json_file:
        json.dump(descriptor, json_file, indent=4)

    print(f"JSON descriptor saved as {descriptor_file}")

def print_help():
    """
    Print the usage help message.
    """
    print("""
Usage: python generate_stopout_dataset.py <stopout_file> <gtfs_path> <custom_gtfs_stops_file> <arrival_date> <departure_date> <stopinfo_started_date>

Example:
    python generate_stopout_dataset.py stops_11aprile.out.csv gtfs/ gtfs_pt_stops.add_filtered.csv 2024-04-01 2024-04-01 2024-04-01
    """)

if __name__ == "__main__":
    main()
