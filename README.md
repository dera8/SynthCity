# SUMO_Toolbox

## Project Overview
This project focuses on enhancing urban mobility analysis through synthetic traffic data generation using the SUMO (Simulation of Urban MObility) software. We aim to create a detailed and realistic simulation of urban traffic scenarios, incorporating both private and public transportation systems. This project includes datasets, configurations, and scripts necessary to run and analyze traffic simulations in the city of Genoa.

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Dataset Description](#dataset-description)
  - [Scenario Configuration](#scenario-configuration)
  - [Simulation Execution](#simulation-execution)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will help you set up and run the traffic simulations on your local machine.

### Prerequisites

- **SUMO:** Ensure you have SUMO installed. You can download it from [SUMO Download Page](https://sumo.dlr.de/docs/Downloads.php).
- **Python:** Python 3.x is required to run the supplementary scripts.
- **Git:** To clone this repository.

## Usage

### Dataset Description

The dataset is created with the following files:

- **Network File:** `osm.net.xml` - The road network of the city.
- **Route Files:** 
    - `pubblici.routes_modified.xml` - Routes for public transportation.
    - `privati.routes.xml` - Routes for private vehicles.
- **Additional Files:** 
    - `gtfs_pt_stops.add.xml` - Public transport stops.
    - `gtfs_pt_vehicles.add2.xml` - Public transport vehicles.

### Scenario Configuration

The scenario configuration file (`sumo_config.xml`) is used to set up the simulation parameters. Below is a breakdown of the configuration elements:

```xml
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">

    <input>  
        <net-file value="osm.net.xml"/>
        <route-files value="pubblici.routes_modified.xml,privati.routes.xml"/> 
        <additional-files value="gtfs_pt_stops.add.xml,gtfs_pt_vehicles.add2.xml,edgeadd.xml"/> 
        <time>  
            <begin value="0"/> 
            <human-readable-time value="true"/>  
        </time>  
    </input> 

    <output>  
        <tripinfo-output value="trips_dayyear.out.xml"/> 
        <stop-output value="stops_dayyear.out.xml"/>
        <edgedata-output value="edge_dayyear.xml"/>
    </output> 

    <processing>  
        <ignore-route-errors value="true"/>
        <time-to-teleport value="-1"/>  
        <ignore-junction-blocker value="1"/> 
    </processing> 

    <mesoscopic>  
        <mesosim value="true"/>
        <meso-junction-control value="true"/>  
        <meso-overtaking value="true"/>
        <meso-lane-queue value="true"/>
    </mesoscopic>  

</configuration>


### Simulation Execution
Prepare the simulation:

Ensure all input files are in place and correctly referenced in the configuration file.

Run the simulation:

```sh
sumo -c cfg.xml or right-click on the file.

Analyze the output:

trips_8april.out.xml contains detailed trip information.
stops_8april.out.xml contains data on stops made by public transport.
edge_8april.xml provides edge-based traffic data.



