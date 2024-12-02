import argparse
import json
from datetime import datetime


def modify_od_matrix(od_file, modifications, mode, output_file):
    """
    Modify an OD matrix based on percentage or value for multiple origin-destination pairs.

    Parameters:
        od_file (str): Path to the OD matrix file.
        modifications (list): List of modifications as dictionaries.
        mode (str): Either 'percentage' or 'value'.
        output_file (str): Name of the output file.

    Returns:
        str: Path to the modified OD matrix file.
    """
    with open(od_file, 'r') as file, open(output_file, 'w') as out_file:
        for line in file:
            line = line.strip()

            # Skip metadata or comment lines
            if not line or line.startswith('*') or ';' in line or line.startswith('$OR'):
                out_file.write(line + "\n")
                continue

            parts = line.split()
            if len(parts) != 3:
                out_file.write(line + "\n")
                continue

            try:
                origin, destination, trips = int(parts[0]), int(parts[1]), int(parts[2])

                for mod in modifications:
                    from_zone, to_zones, operation, value = mod
                    if origin == from_zone and destination in to_zones:
                        if mode == "percentage":
                            modification = trips * (value / 100)
                            trips = trips + modification if operation == "add" else max(0, trips - modification)
                        elif mode == "value":
                            trips = trips + value if operation == "add" else max(0, trips - value)

                out_file.write(f"{origin} {destination} {int(trips)}\n")
            except ValueError:
                out_file.write(line + "\n")

    print(f"Modified OD matrix saved as {output_file}")
    return output_file


def parse_modifications(modifications_list, mode):
    """
    Parse the list of modifications from the command line.

    Parameters:
        modifications_list (list): List of modification strings.
        mode (str): Either 'percentage' or 'value'.

    Returns:
        list: Parsed modifications as a list of tuples.
    """
    modifications = []
    for mod in modifications_list:
        parts = mod.split(":")
        if len(parts) != 4:
            raise ValueError(f"Invalid modification format: {mod}")

        from_zone = int(parts[0])
        to_zones = list(map(int, parts[1].split(",")))
        operation = parts[2]
        if operation not in ["add", "subtract"]:
            raise ValueError(f"Invalid operation: {operation}. Choose 'add' or 'subtract'.")

        value = float(parts[3]) if mode == "percentage" else int(parts[3])
        modifications.append((from_zone, to_zones, operation, value))
    return modifications


def generate_json_descriptor(output_file, description, operation_details):
    """
    Generate a JSON descriptor for the modifications.

    Parameters:
        output_file (str): Path to the output file.
        description (str): Description of the operation.
        operation_details (dict): Details of the operation.

    Returns:
        str: Path to the JSON descriptor file.
    """
    descriptor_file = output_file.replace(".od", ".json")
    descriptor = {
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "operation_details": operation_details
    }

    with open(descriptor_file, 'w') as json_file:
        json.dump(descriptor, json_file, indent=4)

    print(f"JSON descriptor saved as {descriptor_file}")
    return descriptor_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modify OD matrices by percentage or value for multiple origin-destination pairs.",
        epilog="Examples:\n"
               "  python modify_od_matrix.py modify-percentage od_file.od output.od 1:2,3,4:add:10\n"
               "  python modify_od_matrix.py modify-value od_file.od output.od 1:2,3,4:add:100",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: Modify OD matrix by percentage
    parser_percentage = subparsers.add_parser(
        "modify-percentage",
        help="Modify OD matrix by percentage."
    )
    parser_percentage.add_argument("od_file", help="Path to the OD matrix file.")
    parser_percentage.add_argument("output_file", help="Path to the output OD matrix file.")
    parser_percentage.add_argument(
        "modifications",
        nargs="+",
        help="List of modifications in the format 'from_zone:to_zone1,to_zone2:operation:percentage'."
    )

    # Subcommand: Modify OD matrix by value
    parser_value = subparsers.add_parser(
        "modify-value",
        help="Modify OD matrix by value."
    )
    parser_value.add_argument("od_file", help="Path to the OD matrix file.")
    parser_value.add_argument("output_file", help="Path to the output OD matrix file.")
    parser_value.add_argument(
        "modifications",
        nargs="+",
        help="List of modifications in the format 'from_zone:to_zone1,to_zone2:operation:value'."
    )

    args = parser.parse_args()

    if args.command == "modify-percentage":
        modifications = parse_modifications(args.modifications, "percentage")
        output_file = modify_od_matrix(args.od_file, modifications, "percentage", args.output_file)
        generate_json_descriptor(
            output_file,
            "Modify OD matrix by percentage.",
            vars(args)
        )

    elif args.command == "modify-value":
        modifications = parse_modifications(args.modifications, "value")
        output_file = modify_od_matrix(args.od_file, modifications, "value", args.output_file)
        generate_json_descriptor(
            output_file,
            "Modify OD matrix by value.",
            vars(args)
        )
