import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime
import os
import zipfile
import random
import csv
import time 


import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from io import TextIOWrapper

class SimulationApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Simulation Tool")
        master.geometry("800x800")

        # Initialize file variables
        self.network_file = None
        self.gtfs_file = None
        self.od_matrix_file = None
        self.available_roads = []
        
        self.private_percentages = None
        self.public_percentages = None
              
        # Initialize file variables
        self.private_csv = None
        self.public_csv = None
        self.private_percentages = [0.8, 0.5, 0.4, 0.3, 0.4, 1.2, 4.5, 7.4, 6.6, 5.2, 5.0, 5.0, 5.2, 5.3, 5.6, 6.7, 8.4, 8.6, 7.4, 5.0, 3.9, 3.0, 2.1, 1.6]
        self.public_percentages = [0.3, 0.4, 0.4, 0.6, 0.8, 2.0, 4.8, 7.5, 9.0, 8.7, 9.0, 9.0, 7.5, 8.4, 7.8, 6.9, 5.4, 4.0, 2.7, 1.8, 1.2, 0.9, 0.6, 0.3]


        # Create UI widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame for configuration options
        config_frame = tk.Frame(self.master)
        config_frame.pack(pady=10)

        # File selection inputs
        self.create_file_selection_inputs(config_frame)

        # Anomaly options
        #self.create_anomaly_options_inputs(config_frame)

        # Action buttons
        self.create_action_buttons()

        # Text area for logs
        self.output_text = tk.Text(self.master, height=10, width=80)
        self.output_text.pack(pady=10)

        # Area for plots
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.pack(pady=10)

    def create_file_selection_inputs(self, frame):
        # Network File Selection
        self.network_label = tk.Label(frame, text="Network File:")
        self.network_label.grid(row=0, column=0, sticky='w', padx=5)

        self.network_entry = tk.Entry(frame, width=50)
        self.network_entry.grid(row=0, column=1, padx=5)

        self.load_network_button = tk.Button(frame, text="Browse", command=self.load_network_file)
        self.load_network_button.grid(row=0, column=2, padx=5)

        # GTFS File Selection
        self.gtfs_label = tk.Label(frame, text="GTFS Zip File:")
        self.gtfs_label.grid(row=1, column=0, sticky='w', padx=5)

        self.gtfs_entry = tk.Entry(frame, width=50)
        self.gtfs_entry.grid(row=1, column=1, padx=5)

        self.load_gtfs_button = tk.Button(frame, text="Browse", command=self.load_gtfs_file)
        self.load_gtfs_button.grid(row=1, column=2, padx=5)

        # OD Matrix File Selection
        self.od_matrix_label = tk.Label(frame, text="OD Matrix File:")
        self.od_matrix_label.grid(row=2, column=0, sticky='w', padx=5)

        self.od_matrix_entry = tk.Entry(frame, width=50)
        self.od_matrix_entry.grid(row=2, column=1, padx=5)

        self.load_od_matrix_button = tk.Button(frame, text="Browse", command=self.load_od_matrix_file)
        self.load_od_matrix_button.grid(row=2, column=2, padx=5)
        
        self.createmat_button =  tk.Button(frame, text="Browse", command=self.generate_od_matrices)
        

    # def create_anomaly_options_inputs(self, frame):
        # # Anomaly Options
        # self.anomaly_frame = tk.LabelFrame(frame, text="Anomaly Options")
        # self.anomaly_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky='w')

        # self.anomaly_type_label = tk.Label(self.anomaly_frame, text="Anomaly Type:")
        # self.anomaly_type_label.grid(row=0, column=0, sticky='w', padx=5)

        # self.anomaly_type = ttk.Combobox(self.anomaly_frame, values=["None", "Point", "Collective", "Contextual"])
        # self.anomaly_type.set("None")
        # self.anomaly_type.grid(row=0, column=1, padx=5)

        # self.anomaly_freq_label = tk.Label(self.anomaly_frame, text="Anomaly Frequency (%):")
        # self.anomaly_freq_label.grid(row=1, column=0, sticky='w', padx=5)

        # self.anomaly_freq_entry = tk.Entry(self.anomaly_frame, width=10)
        # self.anomaly_freq_entry.insert(0, "5")
        # self.anomaly_freq_entry.grid(row=1, column=1, padx=5)

    def create_action_buttons(self):
        # Buttons for actions
        action_frame = tk.Frame(self.master)
        action_frame.pack(pady=10)

        self.createmat_button = tk.Button(action_frame, text="Generate OD Matrices", command=self.generate_od_matrices)
        self.createmat_button.grid(row=0, column=0, padx=5)

        self.run_simulation_button = tk.Button(action_frame, text="Run SUMO Simulation", command=self.run_sumo_simulation)
        self.run_simulation_button.grid(row=0, column=1, padx=5)

        self.export_button = tk.Button(action_frame, text="Export Results", command=self.export_results)
        self.export_button.grid(row=0, column=2, padx=5)

        self.close_roads_button = tk.Button(action_frame, text="Close Roads", command=self.close_roads)
        self.close_roads_button.grid(row=0, column=3, padx=5)

        self.modify_gtfs_button = tk.Button(action_frame, text="Modify GTFS", command=self.modify_gtfs)
        self.modify_gtfs_button.grid(row=0, column=4, padx=5)

        self.modify_od_button = tk.Button(action_frame, text="Modify OD Matrix", command=self.adjust_od_matrix)
        self.modify_od_button.grid(row=0, column=5, padx=5)

    def load_network_file(self):
        """Load network file, update entry field, and populate road list."""
        self.network_file = filedialog.askopenfilename(title="Select Network File", filetypes=[("XML files", "*.xml")])
        if self.network_file:
            self.network_entry.delete(0, tk.END)
            self.network_entry.insert(0, self.network_file)
            self.output_text.insert(tk.END, f"Loaded Network File: {self.network_file}\n")
            self.populate_road_list()
        else:
            self.output_text.insert(tk.END, "No network file selected.\n")

    def load_gtfs_file(self):
        """Load GTFS file and update the entry field."""
        self.gtfs_file = filedialog.askopenfilename(title="Select GTFS Zip File", filetypes=[("Zip files", "*.zip")])
        if self.gtfs_file:
            self.gtfs_entry.delete(0, tk.END)
            self.gtfs_entry.insert(0, self.gtfs_file)
            self.output_text.insert(tk.END, f"Loaded GTFS File: {self.gtfs_file}\n")
        else:
            self.output_text.insert(tk.END, "No GTFS file selected.\n")

    def load_od_matrix_file(self):
        """Load OD matrix file and update the entry field."""
        self.od_matrix_file = filedialog.askopenfilename(title="Select OD Matrix File", filetypes=[("OD files", "*.od")])
        if self.od_matrix_file:
            self.od_matrix_entry.delete(0, tk.END)
            self.od_matrix_entry.insert(0, self.od_matrix_file)
            self.output_text.insert(tk.END, f"Loaded OD Matrix File: {self.od_matrix_file}\n")
        else:
            self.output_text.insert(tk.END, "No OD matrix file selected.\n")

    def run_sumo_simulation(self):
        """Run SUMO simulation."""
        try:
            # Example of running a SUMO simulation
            os.system('sumo -c your_simulation_config_file.sumocfg')
            self.output_text.insert(tk.END, "SUMO Simulation complete.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error running SUMO simulation: {str(e)}\n")

    def export_results(self):
        """Export results of the simulation."""
        try:
            # Example of exporting simulation results
            results = np.random.rand(100, 4)
            df = pd.DataFrame(results, columns=['Time', 'VehicleID', 'Position', 'Speed'])
            df.to_csv('simulation_results.csv', index=False)
            self.output_text.insert(tk.END, "Results exported to simulation_results.csv\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error exporting results: {str(e)}\n")

    def populate_road_list(self):
        """Parse network file and populate road list."""
        try:
            tree = ET.parse(self.network_file)
            root = tree.getroot()
            self.available_roads = [edge.get('id') for edge in root.findall('edge') if edge.get('function') == 'normal']
            self.output_text.insert(tk.END, f"Available roads loaded: {len(self.available_roads)} roads found.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error parsing network file: {str(e)}\n")

    def close_roads(self):
        """Close roads based on user input."""
        if not self.network_file:
            messagebox.showerror("Error", "Network file is not loaded.")
            return

        edges = self.parse_edges_from_network_file(self.network_file)

        closure_window = tk.Toplevel(self.master)
        closure_window.title("Close Roads")
        closure_window.geometry("400x400")

        tk.Label(closure_window, text="Select roads to close:").pack(pady=5)

        # Create a Listbox for selecting roads
        road_names_listbox = tk.Listbox(closure_window, selectmode=tk.MULTIPLE, width=50, height=10)
        road_names_listbox.pack(pady=5)

        # Populate the Listbox with road names
        for road_name in edges.keys():
            road_names_listbox.insert(tk.END, road_name)

        tk.Label(closure_window, text="Enter closure begin hour (0-23):").pack(pady=5)
        begin_hour_entry = tk.Entry(closure_window, width=10)
        begin_hour_entry.pack(pady=5)

        tk.Label(closure_window, text="Enter closure end hour (0-23):").pack(pady=5)
        end_hour_entry = tk.Entry(closure_window, width=10)
        end_hour_entry.pack(pady=5)

        def process_closure():
            selected_indices = road_names_listbox.curselection()
            selected_road_names = [road_names_listbox.get(i) for i in selected_indices]
            begin_hour = begin_hour_entry.get()
            end_hour = end_hour_entry.get()

            if not selected_road_names or not begin_hour or not end_hour:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            try:
                begin_seconds = int(begin_hour) * 3600
                end_seconds = int(end_hour) * 3600
            except ValueError:
                messagebox.showerror("Error", "Please enter valid hour values.")
                return

            edges_closures = []
            for road_name in selected_road_names:
                edge_ids = edges.get(road_name)
                if edge_ids:
                    edges_closures.append((edge_ids, begin_seconds, end_seconds))
                else:
                    messagebox.showwarning("Warning", f"Road {road_name} not found in the network.")

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f'road_closures_{timestamp}.xml'
            self.generate_closure_xml(edges_closures, output_filename)
            self.output_text.insert(tk.END, f"XML file '{output_filename}' has been generated.\n")
            closure_window.destroy()

        tk.Button(closure_window, text="Generate Closure XML", command=process_closure).pack(pady=20)

    def parse_edges_from_network_file(self, network_filename):
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

    def create_rerouter_element(self, rerouter_id, edge_ids, begin, end):
        rerouter = ET.Element('rerouter', id=str(rerouter_id), edges=' '.join(edge_ids))
        interval = ET.SubElement(rerouter, 'interval', begin=str(begin), end=str(end))
        for edge_id in edge_ids:
            closingReroute = ET.SubElement(interval, 'closingReroute', id=edge_id, disallow='all')
        return rerouter

    def generate_closure_xml(self, edges_closures, output_filename):
        additional = ET.Element('additional')
        for rerouter_id, (edge_ids, begin, end) in enumerate(edges_closures, start=1):
            rerouter_element = self.create_rerouter_element(rerouter_id, edge_ids, begin, end)
            additional.append(rerouter_element)
        xml_str = minidom.parseString(ET.tostring(additional)).toprettyxml(indent="    ")
        with open(output_filename, 'w') as f:
            f.write(xml_str)

    def populate_road_list(self):
        """Populate available roads list from network file."""
        if self.network_file:
            edges = self.parse_edges_from_network_file(self.network_file)
            self.available_roads = list(edges.keys())
            
    def read_od_matrix(self, filename):
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

    def write_od_matrix(self, filename, header_lines, od_data):
        with open(filename, 'w') as file:
            for line in header_lines:
                file.write(f"{line}\n")
            for entry in od_data:
                file.write(f"{entry[0]:4d} {entry[1]:4d} {entry[2]:4d}\n")

    def adjust_od_matrix(self):
        """Open a window to adjust the OD matrix."""
        if not self.od_matrix_file:
            messagebox.showerror("Error", "OD matrix file is not loaded.")
            return

        modify_od_window = tk.Toplevel(self.master)
        modify_od_window.title("Modify OD Matrix")
        modify_od_window.geometry("400x400")

        tk.Label(modify_od_window, text="From Zone:").pack(pady=5)
        from_zone_entry = tk.Entry(modify_od_window)
        from_zone_entry.pack(pady=5)

        tk.Label(modify_od_window, text="To Zone:").pack(pady=5)
        to_zone_entry = tk.Entry(modify_od_window)
        to_zone_entry.pack(pady=5)

        tk.Label(modify_od_window, text="Enter 'add' or 'subtract':").pack(pady=5)
        operation_entry = tk.Entry(modify_od_window)
        operation_entry.pack(pady=5)

        tk.Label(modify_od_window, text="Amount to Modify:").pack(pady=5)
        amount_entry = tk.Entry(modify_od_window)
        amount_entry.pack(pady=5)

        def submit_modification():
            from_zone = from_zone_entry.get().strip()
            to_zone = to_zone_entry.get().strip()
            operation = operation_entry.get().strip().lower()
            try:
                amount = int(amount_entry.get().strip())
                self.modify_od_matrix(from_zone, to_zone, operation, amount)
            except ValueError:
                messagebox.showerror("Error", "Amount should be an integer.")

        submit_button = tk.Button(modify_od_window, text="Submit", command=submit_modification)
        submit_button.pack(pady=10)

    def modify_od_matrix(self, from_zone, to_zone, operation, amount):
        """Modify the OD matrix based on user input."""
        header_lines, od_data = self.read_od_matrix(self.od_matrix_file)

        od_matrix = {(row[0], row[1]): row[2] for row in od_data}

        if (int(from_zone), int(to_zone)) not in od_matrix:
            messagebox.showerror("Error", "Invalid zone(s) specified.")
            return

        if operation == 'add':
            od_matrix[(int(from_zone), int(to_zone))] += amount
        elif operation == 'subtract':
            new_value = od_matrix[(int(from_zone), int(to_zone))] - amount
            if new_value < 0:
                messagebox.showerror("Error", "Resulting number of trips cannot be negative.")
                return
            od_matrix[(int(from_zone), int(to_zone))] = new_value
        else:
            messagebox.showerror("Error", "Invalid operation. Use 'add' or 'subtract'.")
            return

        updated_od_data = [[key[0], key[1], value] for key, value in od_matrix.items()]

        # Ask the user whether to overwrite or save as a new file
        save_as_new = messagebox.askyesno("Save OD Matrix", "Do you want to save the modified OD matrix as a new file?")

        if save_as_new:
            save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if save_file_path:
                self.write_od_matrix(save_file_path, header_lines, updated_od_data)
                self.output_text.insert(tk.END, f"OD Matrix saved as new file: {save_file_path}\n")
        else:
            self.write_od_matrix(self.od_matrix_file, header_lines, updated_od_data)
            self.output_text.insert(tk.END, f"OD Matrix modified and saved: {from_zone} -> {to_zone}, {operation} {amount} trips.\n")
        
    def modify_gtfs(self):
        """Allow user to modify GTFS data by selecting routes to delete or modify."""
        if not self.gtfs_file:
            messagebox.showerror("Error", "GTFS file is not loaded.")
            return

        routes_data, fieldnames = self.load_gtfs_data_from_zip(self.gtfs_file, 'trips.txt')

        modify_window = tk.Toplevel(self.master)
        modify_window.title("Modify GTFS")
        modify_window.geometry("400x400")

        tk.Label(modify_window, text="Select routes to modify:").pack(pady=5)

        # Listbox for selecting routes
        route_ids_listbox = tk.Listbox(modify_window, selectmode=tk.MULTIPLE, width=50, height=10)
        route_ids_listbox.pack(pady=5)

        # Populate the Listbox with route IDs
        route_ids = list({row['route_id'] for row in routes_data})
        for route_id in route_ids:
            route_ids_listbox.insert(tk.END, route_id)

        tk.Label(modify_window, text="Enter percentage of trips to delete (0-100):").pack(pady=5)
        percentage_entry = tk.Entry(modify_window, width=10)
        percentage_entry.pack(pady=5)

        def process_modification():
            selected_indices = route_ids_listbox.curselection()
            selected_route_ids = [route_ids_listbox.get(i) for i in selected_indices]
            percentage = percentage_entry.get()

            if not selected_route_ids or not percentage:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            try:
                percentage = float(percentage)
                if percentage < 0 or percentage > 100:
                    raise ValueError("Percentage must be between 0 and 100.")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                return

            modified_data = routes_data
            for route_id in selected_route_ids:
                modified_data = self.delete_percentage_of_trips_from_route(modified_data, route_id, percentage)

            new_gtfs_filename = self.save_gtfs_data_to_zip(self.gtfs_file, 'trips.txt', modified_data, fieldnames)
            self.output_text.insert(tk.END, f"Modified GTFS saved as {new_gtfs_filename}\n")
            modify_window.destroy()

        tk.Button(modify_window, text="Apply Modification", command=process_modification).pack(pady=20)

    def load_gtfs_data_from_zip(self, zip_filename, txt_filename):
        """Load GTFS data from a zip file."""
        with zipfile.ZipFile(zip_filename, 'r') as z:
            with z.open(txt_filename) as file:
                reader = csv.DictReader(TextIOWrapper(file, 'utf-8'))
                data = list(reader)
        return data, reader.fieldnames

    def save_gtfs_data_to_zip(self, zip_filename, txt_filename, data, fieldnames):
        """Save GTFS data to a zip file without creating blank rows."""
        base_dir = os.path.dirname(zip_filename)
        base_name = os.path.basename(zip_filename)
        temp_zip_filename = os.path.join(base_dir, f"modified_{int(time.time())}_{base_name}")

        with zipfile.ZipFile(zip_filename, 'r') as z:
            with zipfile.ZipFile(temp_zip_filename, 'w') as new_z:
                for item in z.infolist():
                    if item.filename != txt_filename:
                        new_z.writestr(item, z.read(item.filename))
                with new_z.open(txt_filename, 'w') as file:
                    writer = csv.DictWriter(TextIOWrapper(file, 'utf-8', newline=''), fieldnames=fieldnames)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)
        return temp_zip_filename

    def delete_routes(self, data, routes_to_delete):
        """Delete routes based on route IDs."""
        return [row for row in data if row['route_id'] not in routes_to_delete]

    def delete_percentage_of_trips_from_route(self, data, route_id, percentage):
        """Delete a percentage of trips for a specific route."""
        trip_ids = list({row['trip_id'] for row in data if row['route_id'] == route_id})
        num_to_delete = int(len(trip_ids) * (percentage / 100))
        trips_to_delete = set(random.sample(trip_ids, num_to_delete))
        return [row for row in data if not (row['route_id'] == route_id and row['trip_id'] in trips_to_delete)]

    def validate_route_id(self, route_id, data):
        """Validate the route ID against the trips.txt data."""
        return any(row['route_id'] == route_id for row in data)
        
        closure_window = tk.Toplevel(self.master)
        closure_window.title("Close Roads")
        closure_window.geometry("400x400")

        tk.Label(closure_window, text="Select roads to close:").pack(pady=5)
        
    def normalize_percentages(self, percentages):
        """Normalize the percentage values to sum to 1."""
        total = sum(percentages)
        if total == 0:
            return percentages
        return [x / total for x in percentages]
        
    def validate_percentages(self, percentages):
            """Validate that all percentages are set and non-zero."""
            return all(p > 0 for p in percentages)

    def create_od_matrices_for_csv(self, csv_file, percentages, prefix):
        """Create OD matrices based on the CSV file and percentages."""
        try:
            # Read the CSV file
            data = pd.read_csv(csv_file, delimiter=';')
            data['NumViaggi'] = data['NumViaggi'].astype(float)

            # Get all unique OD pairs
            od_pairs = data.groupby(['ORIG_COD_ZONA', 'DEST_COD_ZONA'])['NumViaggi'].sum().reset_index()

            for i in range(24):
                if percentages[i] == 0:
                    continue  # Skip hours with 0 percentage

                header = f"$OR;D2\n* From-Time To-Time\n{i}.00 {(i + 1) % 24}.00\n*Factor\n1.00\n* some\n* additional\n* comments\n"

                filename = f"od_matrix_{prefix}_{i+1}.od"
                with open(filename, 'w') as file:
                    file.write(header)

                    # Distribute trips across OD pairs based on the percentage for this hour
                    for _, row in od_pairs.iterrows():
                        origine = int(row['ORIG_COD_ZONA'])
                        destinazione = int(row['DEST_COD_ZONA'])
                        # Calculate the number of trips for this OD pair at this hour
                        trips = int(row['NumViaggi'] * percentages[i])
                        
                        file.write(f"{origine:>4} {destinazione:>4} {trips:>4}\n")

                self.output_text.insert(tk.END, f"Generated {filename}\n")

        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found. Please ensure the file exists.")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "CSV file is empty or cannot be read.")
        except KeyError as e:
            messagebox.showerror("Error", f"Missing expected column in CSV file: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing CSV file: {e}") 
        
    def generate_od_matrices(self):
        gen_window = tk.Toplevel(self.master)
        gen_window.title("Generate OD Matrices")
        gen_window.geometry("500x500")

        private_sliders = []
        public_sliders = []

        def load_csv_file(entry_field):
            """Load a CSV file and update the entry field."""
            try:
                csv_file = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
                if csv_file:
                    entry_field.delete(0, tk.END)
                    entry_field.insert(0, csv_file)
                    self.output_text.insert(tk.END, f"Loaded CSV File: {csv_file}\n")
                else:
                    self.output_text.insert(tk.END, "No CSV file selected.\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading CSV file: {e}")

        def add_percentage_sliders(parent_frame):
            """Add percentage sliders to the parent frame."""
            private_frame = tk.Frame(parent_frame)
            private_frame.pack(side=tk.LEFT, padx=10)

            tk.Label(private_frame, text="Private Transport Percentages:").pack(pady=5)
            for i in range(24):
                tk.Label(private_frame, text=f"Hour {i}:").pack()
                slider = tk.Scale(private_frame, from_=0, to=10, orient='horizontal', length=200, resolution=0.1)
                slider.set(self.private_percentages[i])
                slider.pack(pady=2)
                private_sliders.append(slider)

            public_frame = tk.Frame(parent_frame)
            public_frame.pack(side=tk.LEFT, padx=10)

            tk.Label(public_frame, text="Public Transport Percentages:").pack(pady=5)
            for i in range(24):
                tk.Label(public_frame, text=f"Hour {i}:").pack()
                slider = tk.Scale(public_frame, from_=0, to=10, orient='horizontal', length=200, resolution=0.1)
                slider.set(self.public_percentages[i])
                slider.pack(pady=2)
                public_sliders.append(slider)

        def generate_od_matrix(private_csv, public_csv, create_private, create_public):
            """Generate OD matrices based on user input."""
            try:
                private_normalized_percentages = self.normalize_percentages([slider.get() for slider in private_sliders])
                public_normalized_percentages = self.normalize_percentages([slider.get() for slider in public_sliders])

                if create_private and not self.validate_percentages(private_normalized_percentages):
                    messagebox.showwarning("Warning", "Please set valid percentages for Private Transport (cannot be equal to 0).")
                    return

                if create_public and not self.validate_percentages(public_normalized_percentages):
                    messagebox.showwarning("Warning", "Please set valid percentages for Public Transport (cannot be equal to 0).")
                    return

                if create_private and private_csv:
                    self.create_od_matrices_for_csv(private_csv, private_normalized_percentages, prefix="private")

                if create_public and public_csv:
                    self.create_od_matrices_for_csv(public_csv, public_normalized_percentages, prefix="public")

            except Exception as e:
                messagebox.showerror("Error", f"Error generating OD matrices: {e}")

        # Private Transport CSV File Selection
        tk.Label(gen_window, text="Private CSV File:").pack(anchor='w', padx=5, pady=2)
        private_csv_entry = tk.Entry(gen_window, width=70)
        private_csv_entry.pack(anchor='w', padx=5, pady=2)
        tk.Button(gen_window, text="Browse", command=lambda: load_csv_file(private_csv_entry)).pack(anchor='w', padx=5, pady=2)

        # Public Transport CSV File Selection
        tk.Label(gen_window, text="Public CSV File:").pack(anchor='w', padx=5, pady=2)
        public_csv_entry = tk.Entry(gen_window, width=70)
        public_csv_entry.pack(anchor='w', padx=5, pady=2)
        tk.Button(gen_window, text="Browse", command=lambda: load_csv_file(public_csv_entry)).pack(anchor='w', padx=5, pady=2)

        # Tabs for different sections
        notebook = ttk.Notebook(gen_window)
        notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create a tab for percentage inputs
        percentage_tab = tk.Frame(notebook)
        notebook.add(percentage_tab, text="Percentages")

        # Create a canvas for the scrollable frame
        canvas = tk.Canvas(percentage_tab)
        scrollbar = tk.Scrollbar(percentage_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mouse wheel for scrolling
        canvas.bind_all("<MouseWheel>")  # Windows and macOS
        canvas.bind_all("<Button-4>")  # Linux
        canvas.bind_all("<Button-5>")  # Linux

        # Add sliders to the scrollable frame
        add_percentage_sliders(scrollable_frame)

        # Create a tab for action buttons
        action_tab = tk.Frame(notebook)
        notebook.add(action_tab, text="Actions")

        # Matrix generation options
        create_private_matrix_var = tk.BooleanVar(value=True)
        create_public_matrix_var = tk.BooleanVar(value=True)

        tk.Checkbutton(action_tab, text="Generate Private OD Matrices", variable=create_private_matrix_var).pack(anchor='w', pady=2)
        tk.Checkbutton(action_tab, text="Generate Public OD Matrices", variable=create_public_matrix_var).pack(anchor='w', pady=2)

        # Button to trigger matrix generation
        tk.Button(action_tab, text="Generate OD Matrices", command=lambda: generate_od_matrix(private_csv_entry.get(), public_csv_entry.get(), create_private_matrix_var.get(), create_public_matrix_var.get())).pack(pady=20)

   

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()