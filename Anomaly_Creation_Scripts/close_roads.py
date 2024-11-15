# close_roads.py
import xml.etree.ElementTree as ET
import sys

def road_closure_management(network_file, roads_to_close, begin_hour, end_hour, output_file):
    begin_seconds = int(begin_hour) * 3600
    end_seconds = int(end_hour) * 3600
    roads = roads_to_close.split(",")

    additional = ET.Element("additional")

    for road in roads:
        rerouter = ET.SubElement(additional, "rerouter", id=f"rerouter_{road}", edges=road)
        interval = ET.SubElement(rerouter, "interval", begin=str(begin_seconds), end=str(end_seconds))
        ET.SubElement(interval, "closingReroute", id=road, disallow="all")

    tree = ET.ElementTree(additional)
    tree.write(output_file)
    print(f"Road closure XML saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python road_closure_management.py <network_file> <roads_to_close> <begin_hour> <end_hour> <output_file>")
    else:
        road_closure_management(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])