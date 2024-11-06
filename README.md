# SUMO ToolBox
This tool is designed to enhance traffic simulation workflows in [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban Mobility). It offers a user-friendly interface for managing road closures, rerouting traffic, modifying origin-destination (OD) matrices, and generating synthetic datasets. The tool facilitates the simulation of varied traffic scenarios, making it ideal for traffic flow studies and infrastructure planning.

## Features
- **OD-Matrices Generation**: create 24-hour OD-matrices based on real daily time lines.
- **Anomaly Creations**: create anomalies in road infrastructure or traffic flow.
  - **Road Closure Management**: Close specific streets and define rerouting paths for traffic, based on a selected time interval.   
  - 
- **OD Matrix Modification**: Adjust traffic flow by adding or subtracting a percentage or a fixed number of trips between selected origin and destination zones.
- **Synthetic Dataset Generation**: Generate synthetic datasets of public transit stops using selected dates, directories, and customized stop files.

## Requirements

- **Python**: Version 3.8 or higher
- **SUMO**: [Simulation of Urban Mobility](https://www.eclipse.org/sumo/)

## Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/your-username/traffic-simulation-tool.git
   cd traffic-simulation-tool

## Usage

1. **Run the Tool**:
   Start the user interface by running the main application file.
   ```bash
   python sumo_toolbox.py

## Interface Overview
Generate PT Stops Dataset: Creates a synthetic dataset for public transit stops using GTFS data and the selected date.
Close Roads: Manages road closures and rerouting for traffic simulations.
Modify OD Matrix by Percentage: Adjusts traffic flows between zones by a specified percentage.
Adjust OD Matrix by Value: Increases or decreases trips between zones by a custom value.

## Step-by-Step Guide
Road Closure Management
Select roads from the list to set as closed.
Define closure start and end times.
Generate the closure XML file to be used in SUMO for rerouting vehicles around the closure.
Modify OD Matrix
Select origin and destination zones from the OD matrix.
Adjust traffic flows by adding or subtracting a percentage or a fixed number of trips.
Save the modified OD matrix as a new file or overwrite the existing file.
Synthetic Dataset Generation
Generate synthetic public transit stop datasets using GTFS data by selecting a date, output file, and directories.
Use the dataset for transit-related simulations in SUMO.

## Example SUMO integration


## Additional Resources




