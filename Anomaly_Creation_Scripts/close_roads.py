import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import zipfile
import os
import csv
import json
from datetime import datetime
import argparse


def parse_edges_from_network_file(network_file):
    """
    Parse edges from the SUMO network file and create a mapping of road names to edge IDs.

    Parameters:
        network_file (str): Path to the SUMO network file.

    Returns:
        dict: A dictionary mapping road names to lists of edge IDs.
    """
    try:
        tree = ET.parse(network_file)
        root = tree.getroot()

        edges_mapping = {}
        for edge in root.findall("edge"):
            edge_id = edge.get("id")
            edge_name = edge.get("name")

            if edge_name:  # Only consider edges with names
                if edge_name not in edges_mapping:
                    edges_mapping[edge_name] = []
                edges_mapping[edge_name].append(edge_id)

        return edges_mapping

    except Exception as e:
        raise RuntimeError(f"Error parsing network file: {e}")


def update_gtfs_files(gtfs_zip, closed_edges, output_gtfs_zip):
    """
    Update GTFS files to reflect road closures by removing stops on closed edges.

    Parameters:
        gtfs_zip (str): Path to the GTFS ZIP file.
        closed_edges (list): List of closed edge IDs.
        output_gtfs_zip (str): Path to the updated GTFS ZIP file.
    """
    temp_dir = "temp_gtfs"
    os.makedirs(temp_dir, exist_ok=True)

    # Extract GTFS ZIP file
    with zipfile.ZipFile(gtfs_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    stops_file = os.path.join(temp_dir, "stops.txt")
    stop_times_file = os.path.join(temp_dir, "stop_times.txt")

    if not all(os.path.exists(f) for f in [stops_file, stop_times_file]):
        raise FileNotFoundError("Required GTFS files (stops.txt, stop_times.txt) not found.")

    # Filter stops based on closed edges
    closed_stops = set()
    with open(stops_file, 'r') as f:
        reader = csv.DictReader(f)
        stops = list(reader)
        for stop in stops:
            if stop["stop_id"] in closed_edges:  # Assuming stop_id relates to edge_id
                closed_stops.add(stop["stop_id"])

    # Update stop_times.txt
    updated_stop_times_file = os.path.join(temp_dir, "updated_stop_times.txt")
    with open(stop_times_file, 'r') as infile, open(updated_stop_times_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row["stop_id"] not in closed_stops:
                writer.writerow(row)

    os.replace(updated_stop_times_file, stop_times_file)

    # Repackage updated GTFS files
    with zipfile.ZipFile(output_gtfs_zip, 'w') as zip_ref:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    # Clean up
    for root, _, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        os.rmdir(root)

    print(f"Updated GTFS archive saved as {output_gtfs_zip}")


def road_closure_management(network_file, road_name, begin_hour, end_hour, output_file, gtfs_zip=None, output_gtfs_zip=None):
    """
    Generate an XML file for managing road closures in SUMO simulations and optionally update GTFS files.

    Parameters:
        network_file (str): Path to the SUMO network file.
        road_name (str): Name of the road to close.
        begin_hour (str): Starting hour of closure (e.g., "8").
        end_hour (str): Ending hour of closure (e.g., "17").
        output_file (str): Path to the output XML file.
        gtfs_zip (str, optional): Path to the GTFS ZIP file to update.
        output_gtfs_zip (str, optional): Path to save the updated GTFS ZIP file.
    """
    try:
        # Parse edges from the network file
        edges_mapping = parse_edges_from_network_file(network_file)

        # Find edge IDs corresponding to the road name
        if road_name not in edges_mapping:
            raise ValueError(f"Road name '{road_name}' not found in the network file.")

        edge_ids = edges_mapping[road_name]

        # Convert hours to seconds
        begin_seconds = int(begin_hour) * 3600
        end_seconds = int(end_hour) * 3600

        # Create the root element for the XML
        additional = ET.Element("additional")

        # Generate closures for each edge ID
        for i, edge_id in enumerate(edge_ids, start=1):
            rerouter = ET.SubElement(additional, "rerouter", id=str(i), edges=edge_id)
            interval = ET.SubElement(rerouter, "interval", begin=str(begin_seconds), end=str(end_seconds))
            ET.SubElement(interval, "closingReroute", id=f"{edge_id}-ClosedEdge", disallow="all")

        # Format the XML with proper indentation
        rough_string = ET.tostring(additional, encoding="utf-8")
        parsed_xml = minidom.parseString(rough_string)
        pretty_xml_as_string = parsed_xml.toprettyxml(indent="    ")

        # Write the formatted XML to a file
        with open(output_file, "w", encoding="utf-8") as xml_file:
            xml_file.write(pretty_xml_as_string)

        print(f"Road closure XML saved as {output_file}")

        # Update GTFS files if provided
        if gtfs_zip and output_gtfs_zip:
            update_gtfs_files(gtfs_zip, edge_ids, output_gtfs_zip)

        # Generate JSON descriptor
        generate_json_descriptor(network_file, road_name, begin_hour, end_hour, output_file)

    except Exception as e:
        print(f"Error: {e}")


def generate_json_descriptor(network_file, road_name, begin_hour, end_hour, output_file):
    """
    Generate a JSON descriptor with information about the road closure configuration.

    Parameters:
        network_file (str): Path to the SUMO network file.
        road_name (str): Name of the road to close.
        begin_hour (str): Starting hour of closure (e.g., "8").
        end_hour (str): Ending hour of closure (e.g., "17").
        output_file (str): Path to the output XML file.
    """
    descriptor = {
        "network_file": network_file,
        "road_name": road_name,
        "begin_hour": int(begin_hour),
        "end_hour": int(end_hour),
        "output_file": output_file
    }

    json_output_file = output_file.replace(".xml", ".json")
    with open(json_output_file, "w", encoding="utf-8") as json_file:
        json.dump(descriptor, json_file, indent=4)

    print(f"JSON descriptor saved as {json_output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a road closure XML and optionally update GTFS files for SUMO simulations.",
        epilog="Example usage: python close_roads.py osm.net.xml 'Via Giovanni Prà' 8 17 road_closures.xml --gtfs_zip input_gtfs.zip --output_gtfs_zip updated_gtfs.zip"
    )

    parser.add_argument(
        "network_file",
        help="Path to the SUMO network file (e.g., osm.net.xml)."
    )
    parser.add_argument(
        "road_name",
        help="Name of the road to close (e.g., 'Via Giovanni Prà')."
    )
    parser.add_argument(
        "begin_hour",
        type=int,
        help="Starting hour of the closure (0-23)."
    )
    parser.add_argument(
        "end_hour",
        type=int,
        help="Ending hour of the closure (0-23)."
    )
    parser.add_argument(
        "output_file",
        help="Name of the output XML file (e.g., road_closures.xml)."
    )
    parser.add_argument(
        "--gtfs_zip",
        help="Path to the GTFS ZIP file to update (optional)."
    )
    parser.add_argument(
        "--output_gtfs_zip",
        help="Path to save the updated GTFS ZIP file (optional)."
    )

    args = parser.parse_args()
    road_closure_management(
        args.network_file,
        args.road_name,
        args.begin_hour,
        args.end_hour,
        args.output_file,
        args.gtfs_zip,
        args.output_gtfs_zip
    )
