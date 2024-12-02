# Anomaly Creation Scripts

A collection of Python scripts to manage and modify transportation data files, including OD matrices, road closures, and GTFS files.

## Table of Contents
- [Scripts](#scripts)
  - [1. Modify OD Matrix by Percentage or Value](#1-modify-od-matrix-by-percentage-or-value)
  - [2. Road Closure Management](#2-road-closure-management)
  - [3. Public Transport Anomaly: Delete a Percentage of Trips in GTFS Files](#3-public-transport-anomaly-delete-a-percentage-of-trips-in-gtfs-files)
  - [4. Public Transport Anomaly: Delete Stops in GTFS Files](#4-public-transport-anomaly-delete-stops-in-gtfs-files)
- [License](#license)

---

## Scripts

### 1. Modify OD Matrix by Percentage or Value

This script allows users to modify an OD matrix by either a given percentage or a fixed value for specified origin-destination (OD) pairs. It supports multiple modifications and outputs both the modified OD matrix and a JSON descriptor with details of the modifications.

- **Usage**:
  ```bash
  python modify_od_matrix.py <command> <od_file> <output_file> <modifications>
  ```
  
- **Example**:
 ```bash
python modify_od_matrix.py modify-percentage od_matrix.od output_matrix.od 1:2,3,4:add:10 5:6,7,8:subtract:20
python modify_od_matrix.py modify-value od_matrix.od output_matrix.od 1:2,3,4:add:100 5:6,7,8:subtract:50
 ```

- **Parameters**:
  - <od_file>: Path to the OD matrix file.
  - <output_file>: Path to save the modified OD matrix file.
  - <from_zone>: Origin zone ID.
  - <to_zone>: Destination zone ID.
  - <operation>: add or subtract.
  - <percentage>: Percentage to add or subtract.
  - <value>: Value to add or subtract.

This script saves the modified OD matrix as modified_od_matrix.od in the current directory.

### 2. Road Closure Management
This script generates an XML file that specifies road closures based on a time interval.

- **Usage**:
 ```bash
python close_roads.py <network_file> <roads_to_close> <begin_hour> <end_hour> <output_file>
 ```
- **Example**:
 ```bash
python close_roads.py osm.net.xml "road1,road2" 8 17 road_closures.xml
 ```

- **Parameters**:
  - <network_file>: Path to the network XML file.
  - <roads_to_close>: Comma-separated list of road IDs to close.
  - <begin_hour>: Starting hour of closure (0-23).
  - <end_hour>: Ending hour of closure (0-23).
  - <output_file>: Output filename for the closure XML.
This script saves the road closure configuration to the specified output_file.

### 3. Public Transport Anomaly: Delete Stops in GTFS Files
This script removes a percentage of trips from the trips.txt file within a GTFS ZIP file based on a route ID.

- **Usage**:
 ```bash
python delete_gtfs_stops.py <gtfs_zip> <output> <stops>
 ```

- **Example**:
 ```bash
python delete_gtfs_stops.py gtfs_data.zip stop1 stop2
 ```

- **Parameters**:
  - <gtfs_zip>: Path to the GTFS ZIP file.
  - <output>: Path to save the modified GTFS ZIP file.
  - <stops>: Stop_IDs to Delete.

This script creates a modified GTFS archive as modified_<gtfs_zip> and deletes the specified percentage of trips for the chosen route ID.

### 4. Public Transport Anomaly: Delete a Percentage of Trips in GTFS Files
This script removes a percentage of trips from the trips.txt file within a GTFS ZIP file based on a route ID.

- **Usage**:
 ```bash
python delete_gtfs_trips.py <gtfs_zip> <route_id> <percentage> <output>
 ```

- **Example**:
 ```bash
python delete_gtfs_trips.py gtfs.zip FGC-63 20 modified_gtfs.zip
 ```

- **Parameters**:
  - <gtfs_zip>: Path to the GTFS ZIP file.
  - <route_id>: Route ID to delete trips from.
  - <percentage>: Percentage of trips to delete (0-100).
  - <output>: Path to save the modified OD matrix file.

This script creates a modified GTFS archive as modified_<gtfs_zip> and deletes the specified percentage of trips for the chosen route ID.

### License:
This project is licensed under the MIT License.
