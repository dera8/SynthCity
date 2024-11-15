# generate_stops_dataset.py
import pandas as pd
import sys
from datetime import datetime

def generate_stops_dataset(stopout_file, gtfs_dir, custom_gtfs_stops_file, date_str):
    try:
        # Define file paths
        stops_path = f"{gtfs_dir}/stops.txt"
        stop_times_path = f"{gtfs_dir}/stop_times.txt"
        trips_path = f"{gtfs_dir}/trips.txt"

        # Load data
        csv_stops = pd.read_csv(stops_path)
        csv_stop_times = pd.read_csv(stop_times_path)
        csv_trips = pd.read_csv(trips_path)
        csv_stopout = pd.read_csv(stopout_file, sep=';')
        csv_gtfs_stops = pd.read_csv(custom_gtfs_stops_file, sep=';')

        # Merge datasets
        merged_data = (
            csv_stop_times
            .merge(csv_trips, on="trip_id")
            .merge(csv_stops, on="stop_id")
            .merge(csv_stopout.rename(columns={'stopinfo_id': 'trip_id'}), on="trip_id")
            .merge(csv_gtfs_stops, left_on="stop_id", right_on="busStop_id")
        )

        # Convert times to datetime format with the given date
        merged_data['arrival_time'] = pd.to_datetime(date_str + ' ' + merged_data['arrival_time'], errors='coerce')
        merged_data['departure_time'] = pd.to_datetime(date_str + ' ' + merged_data['departure_time'], errors='coerce')
        merged_data['stopinfo_started'] = pd.to_datetime(date_str + ' ' + merged_data['stopinfo_started'], errors='coerce')
        
        # Calculate delay
        merged_data['sumo_delay'] = (merged_data['stopinfo_started'] - merged_data['arrival_time']).dt.total_seconds()

        # Generate output filename based on the date
        output_file = f"stops_dataset_{datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y_%m_%d')}.csv"
        
        # Save the final dataset
        merged_data.to_csv(output_file, index=False, sep=';')
        print(f"Stops dataset saved as {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_stops_dataset.py <stopout_file> <gtfs_dir> <custom_gtfs_stops_file> <date>")
    else:
        generate_stops_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
