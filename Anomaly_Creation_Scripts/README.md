# Anomaly Creation Scripts

A collection of Python scripts to manage and modify transportation data files, including OD matrices, road closures, and GTFS files.

## Table of Contents
- [Scripts](#scripts)
  - [1. Modify OD Matrix by Percentage](#1-modify-od-matrix-by-percentage)
  - [2. Adjust OD Matrix by Value](#2-adjust-od-matrix-by-value)
  - [3. Road Closure Management](#3-road-closure-management)
  - [4. Public Transport Anomaly: Delete a Percentage of Trips in GTFS Files](#4-public-transport-anomaly-delete-a-percentage-of-trips-in-gtfs-files)
- [Usage](#usage)
- [License](#license)

---

## Scripts

### 1. Modify OD Matrix by Percentage

This script reads an OD matrix file and modifies the number of trips between specified zones by a given percentage.

- **Filename**: `modify_od_matrix_by_percentage.py`
- **Usage**:
  ```bash
  python modify_od_matrix_by_percentage.py <od_file> <from_zone> <to_zone> <operation> <percentage>
  ```
  
- **Example**:
 ```bash
python modify_od_matrix_by_percentage.py od_matrix.od 1 2 add 10
 ```

- **Parameters**:
  - <od_file>: Path to the OD matrix file.
  - <from_zone>: Origin zone ID.
  - <to_zone>: Destination zone ID.
  - <operation>: add or subtract.
  - <percentage>: Percentage to add or subtract.

This script saves the modified OD matrix as modified_od_matrix.od in the current directory.

### 2. Adjust OD Matrix by Value
This script adjusts the number of trips between specific zones in an OD matrix by a fixed value.

- **Filename**: adjust_od_matrix_by_value.py
- **Usage**:
 ```bash
python adjust_od_matrix_by_value.py <od_file> <from_zone> <to_zone> <operation> <value>
 ```
- **Example**:
 ```bash
python adjust_od_matrix_by_value.py od_matrix.od 1 2 subtract 5
 ```

- **Parameters**:
  - <od_file>: Path to the OD matrix file.
  - <from_zone>: Origin zone ID.
  - <to_zone>: Destination zone ID.
  - <operation>: add or subtract.
  - <value>: Value to add or subtract.
    
This script saves the adjusted OD matrix as adjusted_od_matrix.od.

### 3. Road Closure Management
This script generates an XML file that specifies road closures based on a time interval.

- **Filename**: road_closure_management.py
- **Usage**:
 ```bash
python road_closure_management.py <network_file> <roads_to_close> <begin_hour> <end_hour> <output_file>
 ```
- **Example**:
 ```bash
python road_closure_management.py network.xml "road1,road2" 8 17 road_closures.xml
 ```

- **Parameters**:
<network_file>: Path to the network XML file.
<roads_to_close>: Comma-separated list of road IDs to close.
<begin_hour>: Starting hour of closure (0-23).
<end_hour>: Ending hour of closure (0-23).
<output_file>: Output filename for the closure XML.
This script saves the road closure configuration to the specified output_file.

### 4. Public Transport Anomaly: Delete a Percentage of Trips in GTFS Files
This script removes a percentage of trips from the trips.txt file within a GTFS ZIP file based on a route ID.

-**Filename**: public_transport_anomaly.py
-**Usage**:
 ```bash
python public_transport_anomaly.py <gtfs_zip> <route_id> <percentage>
 ```

-**Example**:
 ```bash
python public_transport_anomaly.py gtfs_data.zip route1 20
 ```

-**Parameters**:
  -<gtfs_zip>: Path to the GTFS ZIP file.
  - <route_id>: Route ID to delete trips from.
  - <percentage>: Percentage of trips to delete (0-100).

This script creates a modified GTFS archive as modified_<gtfs_zip> and deletes the specified percentage of trips for the chosen route ID.

### Usage:
To use these scripts, please make sure you have Python 3.x installed. Download or clone this repository and run the desired script from the command line as shown in the examples above.

Each script provides an inline Usage message if run with incorrect or no arguments.

### License:
This project is licensed under the MIT License.
