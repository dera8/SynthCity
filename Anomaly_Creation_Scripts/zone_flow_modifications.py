def read_od_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    header_lines = []
    od_data_lines = []
    for line in lines:
        if line.startswith('*') or line.startswith('$') or '.' in line:
            header_lines.append(line.strip())
        else:
            od_data_lines.append(line.strip())

    od_data = []
    for line in od_data_lines:
        if line:
            parts = line.split()
            if len(parts) == 3:
                try:
                    od_data.append([int(parts[0]), int(parts[1]), int(parts[2])])
                except ValueError:
                    continue

    return header_lines, od_data

def write_od_matrix(filename, header_lines, od_data):
    with open(filename, 'w') as file:
        for line in header_lines:
            file.write(f"{line}\n")
        for entry in od_data:
            file.write(f"{entry[0]:4d} {entry[1]:4d} {entry[2]:4d}\n")

def main():
    od_matrix_filename = input("Enter the OD matrix filename: ")
    
    header_lines, od_data = read_od_matrix(od_matrix_filename)
    
    print("Current OD matrix data:")
    for entry in od_data:
        print(entry)
    
    try:
        from_zone = int(input("Enter the from zone: "))
        to_zone = int(input("Enter the to zone: "))
        change_type = input("Enter 'add' or 'subtract': ").lower()
        amount = int(input("Enter the number of trips to modify: "))
    except ValueError:
        print("Invalid input. Zone and number of trips must be integers.")
        return

    if amount < 0:
        print("Amount cannot be negative")
        return
    
    # Check if the specified from-to pair exists in the OD matrix
    from_to_exists = any(entry[0] == from_zone and entry[1] == to_zone for entry in od_data)
    if not from_to_exists:
        print(f"From zone {from_zone} to zone {to_zone} does not exist in the OD matrix.")
        return

    # Add or subtract flows
    found = False
    for entry in od_data:
        if entry[0] == from_zone and entry[1] == to_zone:
            if change_type == 'add':
                entry[2] += amount
            elif change_type == 'subtract':
                entry[2] -= amount
                if entry[2] < 0:
                    entry[2] = 0
            else:
                print("Invalid change type. Please enter 'add' or 'subtract'.")
                return
            found = True
            break

    if not found:
        print(f"From zone {from_zone} to zone {to_zone} not found in OD matrix.")
        return
    
    new_filename = f"modified_{od_matrix_filename.split('.')[0]}_{from_zone}_{to_zone}.od"
    write_od_matrix(new_filename, header_lines, od_data)
    print(f"Modified OD matrix written to {new_filename}")

if __name__ == "__main__":
    main()




if __name__ == "__main__":
    main()


