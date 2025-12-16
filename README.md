# 🏙️ SynthCity: A Framework for Generating Synthetic Urban Mobility Datasets With Customizable Anomalous Scenarios

[![DOI](https://img.shields.io/badge/DOI-10.1109/OJITS.2025.3626948-blue.svg)](https://doi.org/10.1109/OJITS.2025.3626948)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![SUMO](https://img.shields.io/badge/SUMO-v1.19-green.svg)](https://eclipse.dev/sumo/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

> Official repository for the paper  
> **"A Framework for Generating Synthetic Urban Mobility Datasets With Customizable Anomalous Scenarios"**  
> *IEEE Open Journal of Intelligent Transportation Systems*, January 2025  
> DOI: [10.1109/OJITS.2025.3626948](https://doi.org/10.1109/OJITS.2025.3626948)

---

## 📖 Overview

**SynthCity** is an open-source framework that automatically generates **synthetic urban mobility datasets** featuring **customizable anomalous scenarios**, such as strikes, road closures, and sudden changes in travel demand.

Built on [**Eclipse SUMO**](https://eclipse.dev/sumo/), SynthCity integrates open data formats (OpenStreetMap – OSM, GTFS, OD matrices, shapefiles) into a unified architecture for **simulation, dataset generation, and anomaly injection**.

It provides both a **Graphical User Interface (GUI)** and a **Command Line Interface (CLI)**, empowering researchers, practitioners, and urban planners to model realistic *what-if* mobility conditions with minimal effort.

---

## 🧩 Main Features

- 🧠 **Anomaly Injector Module**  
  Automatically modifies simulation inputs to model:
  - 🚉 *Public transport disruptions* (strikes, stop closures, trip cancellations)  
  - 🚧 *Network disruptions* (road closures, detours, accidents)  
  - 🎫 *Travel demand variations* (event-driven surges or drops)

- 📊 **Synthetic Dataset Generator Module**  
  Converts SUMO outputs into structured CSV + JSON datasets ready for analysis:
  - **Public Transport:** stop-level data with occupancy, delay, and service stats  
  - **Private Vehicles:** trip-level data with duration, route length, and speed  
  - **Network Edges:** edge-level metrics (density, flow, mean speed)

---

## 🧪 Case Study – Genoa, Italy 🇮🇹

SynthCity was validated using **publicly available open data** from the city of **Genoa**, including:

- 🗺️ **OpenStreetMap network**
- 🚍 **GTFS data from AMT Genova**
- 🧮 **Origin–Destination (OD) matrices** from the City of Genoa

Three representative anomalous scenarios were simulated:

1. 🚇 **Metro Strike** — full suspension of subway service  
2. 🎉 **Special Event** — localized demand surge near the stadium  
3. 🚧 **Road Closure** — disruption of a major arterial road with dynamic rerouting  

The resulting dataset includes **millions of multimodal mobility records** and exhibits **realistic spatio-temporal patterns**, making it suitable for research in:

- 🧠 AI-based mobility modeling  
- 🚦 Intelligent Transportation Systems (ITS)  
- 🏙️ Urban planning and scenario analysis

Link to the dataset: https://doi.org/10.5281/zenodo.17517746 

---

## 📁 Repository Structure

```
SynthCity-main
├── 4april_trips.csv
├── Dataset_definitivo_14aprile_new.zip
├── edge_april28.zip
├── README.md
├── Anomaly_Creation_Scripts
│   ├── README.md
│   ├── close_roads.py
│   ├── delete_gtfs_stops.py
│   ├── modify_gtfs_trips.py
│   ├── modify_od_matrix.py
│   ├── traci_close_road.py
├── Dataset_Creation_Scripts
│   ├── generate_edge_dataset.py
│   ├── generate_stops_dataset.py
│   ├── generate_trip_dataset.py
│   ├── readme.md
├── SynthCity-GUI
│   ├── README.md
│   ├── SynthCityWeb-main.zip
│   ├── SynthCityWebServer-main.zip
│   ├── requirements.txt
```

## 🧾 **Citation**

If you use **SynthCity** in your research, please cite:

D. Russo, F. Rocco Di Torrepadula, L. L. L. Starace, S. Di Martino and N. Mazzocca, "A Framework for Generating Synthetic Urban Mobility Datasets With Customizable Anomalous Scenarios," in IEEE Open Journal of Intelligent Transportation Systems, doi: 10.1109/OJITS.2025.3626948.
 
```bibtex
@article{russo2025framework,
  title={A Framework for Generating Synthetic Urban Mobility Datasets With Customizable Anomalous Scenarios},
  author={Russo, Debora and Di Torrepadula, Franca Rocco and Starace, Luigi Libero Lucio and Di Martino, Sergio and Mazzocca, Nicola},
  journal={IEEE Open Journal of Intelligent Transportation Systems},
  volume={6},
  pages={1439--1458},
  year={2025},
  publisher={IEEE}
  doi={10.1109/OJITS.2025.3626948}
  }


