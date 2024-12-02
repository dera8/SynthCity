# SUMO ToolBox
This tool is designed to enhance traffic simulation workflows in [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban Mobility). It offers a user-friendly interface for managing road closures, rerouting traffic, modifying origin-destination (OD) matrices, and generating synthetic datasets. The tool facilitates the simulation of varied traffic scenarios, making it ideal for traffic flow studies and infrastructure planning.

## Features
  - **OD-Matrices Generation**: create 24-hour OD-matrices based on real daily time lines [1].
  - **Anomaly Creations**: create anomalies in road infrastructure or traffic flow.
  - **Synthetic Dataset Generation**: Generate synthetic datasets using selected dates, directories, and customized stop files.

## Requirements

- **Python**: Version 3.11 or higher
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
- **Generate PT Stops Dataset**: Creates a synthetic dataset for public transit stops using GTFS data and the selected date.
- **Generate Edge Dataset**: Creates a synthetic dataset for edges measurements like density and number of entered vehicles.
- **Generate Trip Dataset**:  Generates a synthetic trip dataset containing information like trip duration and number of reroutings.
- **Close Roads**: Manages road closures and rerouting for traffic simulations.
- **Modify OD Matrix**: Adjusts traffic flows between zones by a specified percentage or value.
- **Road Closure Management**: Close specific streets and define rerouting paths for traffic based on a selected time interval.   
- **Modify GTFS Trips**: Delete a percentage of trips in GTFS files.
- **Modify GTFS Stops**: Delete stops in gtfs files.  

## References 
[1] https://sumo.dlr.de/docs/Demand/Importing_O/D_Matrices.html#daily_time_lines 
