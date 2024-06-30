# Anomaly Detection Scripts
This section provides details on how to use the scripts available for generating anomalies in the traffic simulation.

## Edge Closure Script
This script allows you to close specific roads at designated times to simulate road closures and reroute traffic.

- Run the script:

```python
closed_road_creation.py
```

Follow the prompts:

- Enter the road names to close (comma separated), or 'done' to finish.
- Specify the closure begin and end hours (0-23).

Output:

- An XML file with the road closures will be generated in the current directory.

## GTFS Modification Script
This script modifies GTFS data by either deleting entire routes or a percentage of trips from a specific route.

Run the script:

```python
delete_routes.py
```

Follow the prompts:

- Enter the GTFS zip filename.
- Choose to delete entire routes or a percentage of trips from a specific route.
- Enter the required details (route IDs, percentage).

Output:
- A modified GTFS zip file will be created in the current directory.

## OD Matrix Modification Script
This script allows you to modify the Origin-Destination (OD) matrix by adding or subtracting trips between zones.

```python
zone_flow_modifications.py
```

Follow the prompts:

- Enter the OD matrix filename.
- Specify the from zone, to zone, change type (add/subtract), and the number of trips to modify.

Output:

- A modified OD matrix file will be generated in the current directory.
