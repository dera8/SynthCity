import pandas as pd
import sys
from datetime import datetime

def main():
    try:
        # User input for file names
        stopout_filename = input("Enter the filename for stops output (e.g., stops_11aprile.out.csv): ")

        # Read data from csv files
        csv_stops = pd.read_csv("gtfs/stops.txt", sep=',', dtype='unicode')
        csv_stop_times = pd.read_csv("gtfs/stop_times.txt", sep=',', dtype='unicode')
        csv_trips = pd.read_csv("gtfs/trips.txt", sep=',', dtype='unicode')
        csv_stopout = pd.read_csv(stopout_filename, sep=';', dtype='unicode')
        csv_gtfs_stops = pd.read_csv("gtfs_pt_stops.add_filtered.csv", sep=';', dtype='unicode')

        # File merging
        csv_stop_times_trips = csv_stop_times.merge(csv_trips, on=['vehicle_id'])
        csv_stoptimes_stops = csv_stop_times.merge(csv_stops, on=["stop_id"])
        csv_stoptimes_stops2 = csv_stoptimes_stops[['vehicle_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_name', 'stop_sequence', 'stop_lat', 'stop_lon']]
        csv_stopout.rename(columns={'stopinfo_busStop': 'busStop_id'}, inplace=True)
        csv_stopout.rename(columns={'stopinfo_id': 'vehicle_id'}, inplace=True)
        csv_stopout2 = csv_stopout[['busStop_id', 'stopinfo_delay', 'stopinfo_ended', 'vehicle_id', 'stopinfo_initialPersons', 'stopinfo_loadedPersons', 'stopinfo_started', 'stopinfo_type', 'stopinfo_unloadedPersons']]
        csv_stops_stopout2 = csv_gtfs_stops.merge(csv_stopout2, on=["busStop_id"])
        csv_stopout3 = csv_stoptimes_stops2.merge(csv_stops_stopout2, on=["vehicle_id", "stop_name"])
        routes = pd.read_csv("gtfs/trips.txt", sep=',', dtype='unicode')
        csv_stopout4 = csv_stopout3.merge(routes, on=["vehicle_id"])

        # User input for datetime
        arrival_date = input("Enter the date for arrival time (dd/mm/yyyy): ")
        departure_date = input("Enter the date for departure time (dd/mm/yyyy): ")
        stopinfo_started_date = input("Enter the date for stopinfo started time (dd/mm/yyyy): ")

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

        # Add date
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
        file_name = f"Dataset_{arrival_date_dt.day}_{arrival_date_dt.strftime('%B')}_{arrival_date_dt.year}.csv"

        # Save the final synthetic dataset
        data.to_csv(file_name, index=False, sep=';')
        print(f"Dataset successfully created and saved as '{file_name}'")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path and ensure the file exists.")
    except pd.errors.ParserError as e:
        print(f"Error: {e}. There is an issue with parsing the CSV files. Please check the file format.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


