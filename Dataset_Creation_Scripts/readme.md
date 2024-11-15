# Transportation Data Management Scripts

A collection of Python scripts for generating datasets for stops, edges, and trips from GTFS and SUMO files.

## Table of Contents
- [Scripts](#scripts)
  - [generate_stops_dataset.py](#generate_stops_datasetpy)
  - [generate_edge_dataset.py](#generate_edge_datasetpy)
  - [generate_trips_dataset.py](#generate_trips_datasetpy)
- [Usage Examples](#usage-examples)
- [License](#license)

---

## Scripts

### generate_stops_dataset.py

This script generates a stops dataset by merging and processing data from GTFS files, a custom stops file, and stop output data. It includes handling for time corrections and delay calculations.

- **Usage**:
  ```bash
  python generate_stops_dataset.py <stopout_file> <gtfs_dir> <custom_gtfs_stops_file> <date>
  ```
- **Parameters**:
  - `<stopout_file>`: Path to the stops output file (e.g., `stop_output.csv`).
  - `<gtfs_dir>`: Directory containing GTFS files (e.g., `gtfs_directory`).
  - `<custom_gtfs_stops_file>`: Path to the custom GTFS stops file (e.g., `custom_stops.csv`).
  - `<date>`: Date in the format `YYYY-MM-DD` to be combined with times.

- **Example**:
  ```bash
  python generate_stops_dataset.py stop_output.csv gtfs_directory custom_stops.csv 2024-11-12
  ```

This will create a file named `stops_dataset_2024_11_12.csv` with the processed stop data.

---

### generate_edge_dataset.py

This script generates a dataset of edges by extracting and merging data from an XML edge file and a TAZ (Traffic Analysis Zone) XML file. The output dataset includes information about traffic volume, density, speed, and TAZ zones for each edge.

- **Usage**:
  ```bash
  python generate_edge_dataset.py <edge_file> <taz_file> <output_csv> <date>
  ```
- **Parameters**:
  - `<edge_file>`: Path to the XML file containing edge data (e.g., `edges.xml`).
  - `<taz_file>`: Path to the TAZ XML file containing traffic analysis zones (e.g., `taz.xml`).
  - `<output_csv>`: Filename for the output CSV file (e.g., `edges_dataset.csv`).
  - `<date>`: Date in the format `YYYY-MM-DD` to include as a column in the dataset.

- **Example**:
  ```bash
  python generate_edge_dataset.py edges.xml taz.xml edge_dataset.csv 2024-11-12
  ```

This will create a file named `edge_dataset.csv` containing edge-related data for the specified date.

---

### generate_trips_dataset.py

This script generates a dataset of trips by filtering and processing data from an XML file containing trip information. It allows you to specify types of trips and includes start and end times, trip durations, and other relevant metrics.

- **Usage**:
  ```bash
  python generate_trips_dataset.py <trips_file> <selected_types> <date> <output_csv>
  ```
- **Parameters**:
  - `<trips_file>`: Path to the XML file containing trip data (e.g., `trips.xml`).
  - `<selected_types>`: Comma-separated list of types (e.g., `bus,tram`) to filter.
  - `<date>`: Date in the format `YYYY-MM-DD` to combine with trip start and end times.
  - `<output_csv>`: Filename for the output CSV file (e.g., `trips_dataset.csv`).

- **Example**:
  ```bash
  python generate_trips_dataset.py trips.xml bus,tram 2024-11-12 trips_dataset.csv
  ```

This will create a file named `trips_dataset.csv` containing filtered trip data for the specified date.

---

## Usage Examples

### Running All Scripts

1. **Generate Stops Dataset**:
   ```bash
   python generate_stops_dataset.py stop_output.csv gtfs_directory custom_stops.csv 2024-11-12
   ```

2. **Generate Edge Dataset**:
   ```bash
   python generate_edge_dataset.py edges.xml taz.xml edge_dataset.csv 2024-11-12
   ```

3. **Generate Trips Dataset**:
   ```bash
   python generate_trips_dataset.py trips.xml bus,tram 2024-11-12 trips_dataset.csv
   ```

---

## License

This project is licensed under the MIT License.
