# modify_od_matrix_by_percentage.py
import sys

def modify_od_matrix(od_file, from_zone, to_zone, operation, percentage):
    output_file = "modified_od_matrix.od"
    percentage = float(percentage) / 100

    with open(od_file, 'r') as file, open(output_file, 'w') as out_file:
        for line in file:
            parts = line.split()
            if len(parts) != 3:
                out_file.write(line)
                continue

            origin, destination, trips = int(parts[0]), int(parts[1]), int(parts[2])

            if origin == int(from_zone) and destination == int(to_zone):
                trips = int(trips * (1 + percentage)) if operation == "add" else int(trips * (1 - percentage))
                trips = max(0, trips)

            out_file.write(f"{origin} {destination} {trips}\n")

    print(f"Modified OD matrix saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python modify_od_matrix_by_percentage.py <od_file> <from_zone> <to_zone> <operation> <percentage>")
    else:
        modify_od_matrix(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])