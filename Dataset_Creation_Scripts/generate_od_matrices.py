import pandas as pd
import argparse


def generate_od_matrices(input_file, output_prefix, transport_type, origin_col, destination_col, trips_col):
    """
    Generate OD matrices in o-format type for a given transport type (private or public).

    Parameters:
        input_file (str): Path to the input CSV file containing OD data.
        output_prefix (str): Prefix for the output files (e.g., "private" or "public").
        transport_type (str): Type of transport ("private" or "public").
        origin_col (str): Column name for origin zones.
        destination_col (str): Column name for destination zones.
        trips_col (str): Column name for the number of trips.

    Returns:
        None: Generates OD matrices as .od files.
    """
    try:
        # Read input data
        data = pd.read_csv(input_file, delimiter=';', dtype=str)  # Read everything as string for validation

        # Ensure all specified columns exist
        for col in [origin_col, destination_col, trips_col]:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the input file.")

        # Convert specified columns to integers
        try:
            data[origin_col] = data[origin_col].astype(int)
            data[destination_col] = data[destination_col].astype(int)
            data[trips_col] = data[trips_col].astype(float)  # Allow float for trips, we'll convert later
        except ValueError as e:
            raise ValueError(f"All values in columns '{origin_col}', '{destination_col}', and '{trips_col}' must be numeric. {e}")

        # Define traffic flow rates for the 24 time slots 
        if transport_type.lower() == 'private':
            percentages = [0.9, 0.5, 0.4, 0.3, 0.4, 1.2, 4.5, 7.4, 6.6, 5.2, 5.0, 5.0,
                           5.2, 5.3, 5.6, 6.7, 8.4, 8.6, 7.4, 5.0, 3.9, 3.0, 2.1, 1.6]
        elif transport_type.lower() == 'public':
            percentages = [0.3, 0.4, 0.4, 0.6, 0.8, 2.0, 4.8, 7.5, 9.0, 8.7, 9.0, 9.0,
                           7.5, 8.4, 7.8, 6.9, 5.4, 4.0, 2.7, 1.8, 1.2, 0.9, 0.6, 0.3]
        else:
            raise ValueError("Invalid transport type. Choose 'private' or 'public'.")

        # Validate that the sum of percentages is exactly 100
        total = sum(percentages)
        if abs(total - 100) > 1e-6:  # Allowing for minor floating-point precision errors
            raise ValueError(f"Percentages do not sum to 100. Current sum is {total}.")

        # Normalize percentages to ensure they sum to 1
        normalized_percentages = [x / 100 for x in percentages]

        # Group data by the specified origin, destination, and trips columns
        grouped_data = data.groupby([origin_col, destination_col])[trips_col].sum().reset_index()

        # Generate OD matrices for each hour
        for i in range(24):
            mat_hour = grouped_data.copy()

            # Multiply the total trips by the percentage for the current time slot
            mat_hour[trips_col] = mat_hour[trips_col] * normalized_percentages[i]

            # Convert trips to integers for the OD matrix
            mat_hour[trips_col] = mat_hour[trips_col].astype(int)

            # Adjust the time range for the last hour
            if i == 23:
                time_range = "23.00 23.59"
            else:
                time_range = f"{i}.00 {(i + 1) % 24}.00"

            # Generate header for the OD matrix file
            header = (f"$OR;D2\n"
                      f"* From-Time To-Time\n"
                      f"{time_range}\n"
                      f"*Factor\n1.00\n"
                      f"* some\n* additional\n* comments\n")

            # Write the OD matrix to a file
            output_file = f"{output_prefix}_od_matrix_{i+1}.od"
            with open(output_file, 'w') as file:
                file.write(header)

                # Write OD data
                for _, row in mat_hour.iterrows():
                    file.write(f"{row[origin_col]:>4} {row[destination_col]:>4} {row[trips_col]:>4}\n")

            print(f"Generated OD matrix for hour {i}: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path and ensure the file exists.")
    except pd.errors.ParserError as e:
        print(f"Error: {e}. There is an issue with parsing the CSV file. Please check the file format.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate OD matrices in o-format for private or public transport.",
        epilog="Example: python generate_od_matrices.py od_data.csv private private ORIG DEST TRIPS"
    )

    parser.add_argument(
        "input_file",
        help="Path to the input CSV file containing OD data."
    )
    parser.add_argument(
        "output_prefix",
        help="Prefix for the output files (e.g., 'private' or 'public')."
    )
    parser.add_argument(
        "transport_type",
        choices=["private", "public"],
        help="Type of transport ('private' or 'public')."
    )
    parser.add_argument(
        "origin_col",
        help="Column name for origin zones in the input CSV."
    )
    parser.add_argument(
        "destination_col",
        help="Column name for destination zones in the input CSV."
    )
    parser.add_argument(
        "trips_col",
        help="Column name for the number of trips in the input CSV."
    )

    args = parser.parse_args()
    generate_od_matrices(
        args.input_file,
        args.output_prefix,
        args.transport_type,
        args.origin_col,
        args.destination_col,
        args.trips_col
    )
