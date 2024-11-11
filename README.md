# SUMO ToolBox
This tool is designed to enhance traffic simulation workflows in [SUMO](https://www.eclipse.org/sumo/) (Simulation of Urban Mobility). It offers a user-friendly interface for managing road closures, rerouting traffic, modifying origin-destination (OD) matrices, and generating synthetic datasets. The tool facilitates the simulation of varied traffic scenarios, making it ideal for traffic flow studies and infrastructure planning.

## Features
  - **OD-Matrices Generation**: create 24-hour OD-matrices based on real daily time lines.
  - **Anomaly Creations**: create anomalies in road infrastructure or traffic flow.
  - **Synthetic Dataset Generation**: Generate synthetic datasets using selected dates, directories, and customized stop files.

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
**Road Closure Management**: Close specific streets and define rerouting paths for traffic, based on a selected time interval.   
**Public Transport Anomaly**: Delete a percentage of trips in gtfs files.  

## Example SUMO integration

