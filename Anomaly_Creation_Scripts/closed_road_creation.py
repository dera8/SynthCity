import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

def parse_edges_from_network_file(network_filename):
    tree = ET.parse(network_filename)
    root = tree.getroot()
    edges = {}
    for edge in root.findall('edge'):
        edge_id = edge.attrib['id']
        edge_name = edge.attrib.get('name', 'Unknown')
        if edge_name not in edges:
            edges[edge_name] = []
        edges[edge_name].append(edge_id)
    return edges

def create_rerouter_element(rerouter_id, edge_ids, begin, end):
    rerouter = ET.Element('rerouter', id=str(rerouter_id), edges=' '.join(edge_ids))
    interval = ET.SubElement(rerouter, 'interval', begin=str(begin), end=str(end))
    for edge_id in edge_ids:
        closingReroute = ET.SubElement(interval, 'closingReroute', id=edge_id, disallow='all')
    return rerouter

def generate_closure_xml(edges_closures, output_filename):
    additional = ET.Element('additional')
    for rerouter_id, (edge_ids, begin, end) in enumerate(edges_closures, start=1):
        rerouter_element = create_rerouter_element(rerouter_id, edge_ids, begin, end)
        additional.append(rerouter_element)
    xml_str = minidom.parseString(ET.tostring(additional)).toprettyxml(indent="    ")
    with open(output_filename, 'w') as f:
        f.write(xml_str)

def main():
    network_filename = 'osm.net.xml'
    edges = parse_edges_from_network_file(network_filename)
    

    edges_closures = []
    while True:
        selected_road_names = input("Enter the road names to close (comma separated), or 'done' to finish: ")
        if selected_road_names.lower() == 'done':
            break
        selected_road_names = selected_road_names.split(',')
        selected_road_names = [name.strip() for name in selected_road_names]

        begin_hour = int(input("Enter closure begin hour (0-23): "))
        end_hour = int(input("Enter closure end hour (0-23): "))
        
        # Convert hours to seconds
        begin_seconds = begin_hour * 3600
        end_seconds = end_hour * 3600
        
        for road_name in selected_road_names:
            edge_ids = edges.get(road_name)
            if edge_ids:
                edges_closures.append((edge_ids, begin_seconds, end_seconds))
            else:
                print(f"Road {road_name} not found in the network.")

    # Generate a unique filename using the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'road_closures_{timestamp}.xml'
    
    generate_closure_xml(edges_closures, output_filename)
    print(f"XML file '{output_filename}' has been generated.")

if __name__ == '__main__':
    main()





