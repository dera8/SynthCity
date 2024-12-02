import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime
import sys
import json


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
        print(f"Error parsing network file: {e}")
        sys.exit(1)


def road_closure_management(network_file, road_name, begin_hour, end_hour, output_file):
    """
    Generate an XML file for managing road closures in SUMO simulations based on road names.

    Parameters:
        network_file (str): Path to the SUMO network file.
        road_name (str): Name of the road to close.
        begin_hour (str): Starting hour of closure (e.g., "8").
        end_hour (str): Ending hour of closure (e.g., "17").
        output_file (str): Path to the output XML file.
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
    if len(sys.argv) != 6:
        print("Usage: python close_roads.py <network_file> <road_name> <begin_hour> <end_hour> <output_file>")
    else:
        road_closure_management(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
