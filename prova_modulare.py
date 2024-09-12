#crea calendario per stopout

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from tkcalendar import Calendar
from tkinter import Tk, Label, Entry, Button, Toplevel
from tkinter import StringVar, Listbox, MULTIPLE

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
from io import TextIOWrapper
from datetime import datetime
from datetime import timedelta

class SimulationApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Simulation Tool")
        master.geometry("800x800")

        # File and Data Handlers
        self.file_handler = FileHandler()
        self.data_processor = DataProcessor()

        # Initialize file variables
        self.network_file = None
        self.gtfs_file = None
        self.od_matrix_file = None
        self.available_roads = []

        self.private_percentages = None
        self.public_percentages = None
        
        self.stopout_file = None
        self.gtfs_path = None
        self.custom_gtfs_stops_file = None
        
        self.private_csv = None
        self.public_csv = None
        self.private_percentages = [0.8, 0.5, 0.4, 0.3, 0.4, 1.2, 4.5, 7.4, 6.6, 5.2, 5.0, 5.0, 5.2, 5.3, 5.6, 6.7, 8.4, 8.6, 7.4, 5.0, 3.9, 3.0, 2.1, 1.6]
        self.public_percentages = [0.3, 0.4, 0.4, 0.6, 0.8, 2.0, 4.8, 7.5, 9.0, 8.7, 9.0, 9.0, 7.5, 8.4, 7.8, 6.9, 5.4, 4.0, 2.7, 1.8, 1.2, 0.9, 0.6, 0.3]  
              
        # Initialize UI
        self.create_widgets()

    def create_widgets(self):
        """Create the main UI widgets."""
        # Frame for configuration options
        config_frame = tk.Frame(self.master)
        config_frame.pack(pady=10)

        # File selection inputs
        self.create_file_selection_inputs(config_frame)

        # Action buttons
        self.create_action_buttons()

        # Text area for logs
        self.output_text = tk.Text(self.master, height=10, width=80)
        self.output_text.pack(pady=10)

    def create_file_selection_inputs(self, frame):
        """Create inputs for file selection."""
        # Network File Selection
        self.network_label = tk.Label(frame, text="Network File:")
        self.network_label.grid(row=0, column=0, sticky='w', padx=5)

        self.network_entry = tk.Entry(frame, width=50)
        self.network_entry.grid(row=0, column=1, padx=5)

        self.load_network_button = tk.Button(frame, text="Browse", command=self.load_network_file)
        self.load_network_button.grid(row=0, column=2, padx=5)
        
        # OD Matrix File Selection
        self.od_matrix_label = tk.Label(frame, text="OD Matrix File:")
        self.od_matrix_label.grid(row=2, column=0, sticky='w', padx=5)

        self.od_matrix_entry = tk.Entry(frame, width=50)
        self.od_matrix_entry.grid(row=2, column=1, padx=5)

        self.load_od_matrix_button = tk.Button(frame, text="Browse", command=self.load_od_matrix_file)
        self.load_od_matrix_button.grid(row=2, column=2, padx=5)
        
        # GTFS File Selection
        self.gtfs_label = tk.Label(frame, text="GTFS Zip File:")
        self.gtfs_label.grid(row=1, column=0, sticky='w', padx=5)

        self.gtfs_entry_main = tk.Entry(frame, width=50)
        self.gtfs_entry_main.grid(row=1, column=1, padx=5)

        self.load_gtfs_button = tk.Button(frame, text="Browse", command=self.load_gtfs_file_main)
        self.load_gtfs_button.grid(row=1, column=2, padx=5)

    def create_action_buttons(self):
        """Create action buttons."""
        action_frame = tk.Frame(self.master)
        action_frame.pack(pady=10)
        
        self.create_od_button = tk.Button(self.master, text="Generate OD Matrices", command=self.generate_od_matrices).pack(pady=10)

        self.close_roads_button = tk.Button(action_frame, text="Close Roads", command=self.close_roads)
        self.close_roads_button.grid(row=0, column=3, padx=5)
        
        self.modify_od_button = tk.Button(action_frame, text="Modify OD Matrix", command=self.adjust_od_matrix)
        self.modify_od_button.grid(row=0, column=5, padx=5)
        
        self.modify_gtfs_button = tk.Button(action_frame, text="Modify GTFS", command=self.modify_gtfs)
        self.modify_gtfs_button.grid(row=0, column=4, padx=5)
        
        self.synth_stop_button =tk.Button(self.master, text="Generate PT Stops Dataset", command=self.generate_synthetic_dataset).pack(pady=10)  
        
        self.synth_edge_button = tk.Button(self.master, text="Generate Edge Dataset", command=self.open_generate_dataset_window).pack(pady=10)

        self.trips_stop_button = tk.Button(self.master, text="Generate Trips Dataset", command=self.open_trips_xml_window).pack(pady=10)

    def load_network_file(self):
        """Load network file, update entry field, and populate road list."""
        self.network_file = filedialog.askopenfilename(title="Select Network File", filetypes=[("XML files", "*.xml")])
        if self.network_file:
            self.network_entry.delete(0, tk.END)
            self.network_entry.insert(0, self.network_file)
            self.output_text.insert(tk.END, f"Loaded Network File: {self.network_file}\n")
            edges = self.file_handler.parse_edges_from_network_file(self.network_file)
            if edges:
                self.available_roads = self.data_processor.populate_road_list(edges)
                self.output_text.insert(tk.END, f"Available roads loaded: {len(self.available_roads)} roads found.\n")
        else:
            self.output_text.insert(tk.END, "No network file selected.\n")
            
    def load_od_matrix_file(self):
        """Load OD matrix file and update the entry field."""
        self.od_matrix_file = filedialog.askopenfilename(title="Select OD Matrix File", filetypes=[("OD files", "*.od")])
        if self.od_matrix_file:
            self.od_matrix_entry.delete(0, tk.END)
            self.od_matrix_entry.insert(0, self.od_matrix_file)
            self.output_text.insert(tk.END, f"Loaded OD Matrix File: {self.od_matrix_file}\n")
        else:
            self.output_text.insert(tk.END, "No OD matrix file selected.\n")
            
    def load_gtfs_file_main(self):
        """Load GTFS file and update the entry field."""
        self.gtfs_file = filedialog.askopenfilename(title="Select GTFS Zip File", filetypes=[("Zip files", "*.zip")])
        if self.gtfs_file:
            self.gtfs_entry_main.delete(0, tk.END)
            self.gtfs_entry_main.insert(0, self.gtfs_file)
            self.output_text.insert(tk.END, f"Loaded GTFS File: {self.gtfs_file}\n")
        else:
            self.output_text.insert(tk.END, "No GTFS file selected.\n")
            
            
    def close_roads(self):
        """Close roads based on user input."""
        if not self.network_file:
            messagebox.showerror("Error", "Network file is not loaded.")
            return

        edges = self.file_handler.parse_edges_from_network_file(self.network_file)
        if not edges:
            return

        closure_window = tk.Toplevel(self.master)
        closure_window.title("Close Roads")
        closure_window.geometry("500x600")

        tk.Label(closure_window, text="Search roads:").pack(pady=5)

        # Entry for searching roads
        search_entry = tk.Entry(closure_window)
        search_entry.pack(pady=5)

        # Frame to contain Listbox and Scrollbar
        listbox_frame = tk.Frame(closure_window)
        listbox_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Listbox for selecting roads
        road_names_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=50, height=20)
        road_names_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Listbox and Scrollbar
        road_names_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=road_names_listbox.yview)

        # Populate the Listbox with road names
        all_road_names = sorted(edges.keys())  # Sort for better readability
        for road_name in all_road_names:
            road_names_listbox.insert(tk.END, road_name)

        # Function to update the listbox based on the search query
        
        def update_listbox(*args):
            search_query = search_entry.get().strip().lower()
            road_names_listbox.delete(0, tk.END)
            for road_name in all_road_names:
                if search_query in road_name.lower():
                    road_names_listbox.insert(tk.END, road_name)

        # Bind the search entry to the update function
        search_entry.bind("<KeyRelease>", update_listbox)

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

            self.data_processor.add_road_closure(edges, selected_road_names, begin_seconds, end_seconds)
            xml_element = self.data_processor.generate_closure_xml(self.data_processor.edges_closures)
            #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Correct usage of datetime
            output_filename = f'road_closures_{timestamp}.xml'
            if self.file_handler.save_xml_file(xml_element, output_filename):
                self.output_text.insert(tk.END, f"XML file '{output_filename}' has been generated.\n")
            closure_window.destroy()

        tk.Button(closure_window, text="Generate Closure XML", command=process_closure).pack(pady=20)

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
                header_lines, updated_od_data = self.data_processor.modify_od_matrix(
                    self.od_matrix_file, from_zone, to_zone, operation, amount, self.file_handler
                )
                
                # Ask the user whether to overwrite or save as a new file
                save_as_new = messagebox.askyesno("Save OD Matrix", "Do you want to save the modified OD matrix as a new file?")

                if save_as_new:
                    save_file_path = filedialog.asksaveasfilename(defaultextension=".od", filetypes=[("OD matrices", "*.od"), ("All files", "*.*")])
                    if save_file_path:
                        self.file_handler.write_od_matrix(save_file_path, header_lines, updated_od_data)
                        self.output_text.insert(tk.END, f"OD Matrix saved as new file: {save_file_path}\n")
                else:
                    self.file_handler.write_od_matrix(self.od_matrix_file, header_lines, updated_od_data)
                    self.output_text.insert(tk.END, f"OD Matrix modified and saved: {from_zone} -> {to_zone}, {operation} {amount} trips.\n")
            
            except ValueError:
                messagebox.showerror("Error", "Amount should be an integer.")

        submit_button = tk.Button(modify_od_window, text="Submit", command=submit_modification)
        submit_button.pack(pady=10)  # Ensure the button is packed into the window

    def modify_gtfs(self):
        """Allow user to modify GTFS data by selecting routes to delete or modify."""
        if not self.gtfs_file:
            messagebox.showerror("Error", "GTFS file is not loaded.")
            return

        # Load trips.txt and routes.txt from GTFS zip
        routes_data, trips_fieldnames = self.file_handler.load_gtfs_data_from_zip(self.gtfs_file, 'trips.txt')
        routes_info, _ = self.file_handler.load_gtfs_data_from_zip(self.gtfs_file, 'routes.txt')  # Load routes.txt

        modify_window = tk.Toplevel(self.master)
        modify_window.title("Modify GTFS")
        modify_window.geometry("500x600")

        tk.Label(modify_window, text="Search routes:").pack(pady=5)

        # Entry for searching routes
        search_entry = tk.Entry(modify_window)
        search_entry.pack(pady=5)

        # Frame to contain Listbox and Scrollbar
        listbox_frame = tk.Frame(modify_window)
        listbox_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Listbox for selecting routes
        route_ids_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=50, height=20)
        route_ids_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Listbox and Scrollbar
        route_ids_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=route_ids_listbox.yview)

        # Create a dictionary mapping route_id to route_long_name
        route_dict = {row['route_id']: row.get('route_long_name', '') for row in routes_info}

        # Create a dictionary to track remaining trips in trips.txt per route_id
        trips_by_route = {route_id: [] for route_id in route_dict}

        # Populate the trips_by_route dictionary with trip info from trips.txt
        for trip in routes_data:
            route_id = trip['route_id']
            if route_id in trips_by_route:
                trips_by_route[route_id].append(trip)

        # Populate the Listbox with both route_id and route_long_name if there are trips left
        all_routes = [f"{route_id}: {route_dict[route_id]}" for route_id in trips_by_route if trips_by_route[route_id]]
        for route in all_routes:
            route_ids_listbox.insert(tk.END, route)

        # Function to update the listbox based on the search query
        def update_listbox(*args):
            search_query = search_entry.get().strip().lower()
            route_ids_listbox.delete(0, tk.END)
            for route in all_routes:
                if search_query in route.lower():
                    route_ids_listbox.insert(tk.END, route)

        # Bind the search entry to the update function
        search_entry.bind("<KeyRelease>", update_listbox)

        tk.Label(modify_window, text="Enter percentage of trips to delete (0-100):").pack(pady=5)
        percentage_entry = tk.Entry(modify_window, width=10)
        percentage_entry.pack(pady=5)

        def process_modification():
            nonlocal all_routes  # Ensure we are referring to the outer `all_routes` variable
            selected_indices = route_ids_listbox.curselection()
            selected_route_entries = [route_ids_listbox.get(i) for i in selected_indices]

            # Extract the route_id from the "route_id: route_long_name" format
            selected_route_ids = [entry.split(":")[0].strip() for entry in selected_route_entries]
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

            # Track route_ids to remove if 100% of trips are deleted
            routes_to_remove = []

            for route_id in selected_route_ids:
                # Delete percentage of trips for the selected route
                modified_data = self.data_processor.delete_percentage_of_trips_from_route(modified_data, route_id, percentage)

                # Check if there are remaining trips for this route_id
                remaining_trips = [row for row in modified_data if row['route_id'] == route_id]
                trips_by_route[route_id] = remaining_trips

                # If no remaining trips, mark this route_id for removal
                if not remaining_trips:
                    routes_to_remove.append(route_id)

            # Update the trips.txt file with the modified data
            new_gtfs_filename = self.file_handler.save_gtfs_data_to_zip(self.gtfs_file, 'trips.txt', modified_data, trips_fieldnames)
            self.output_text.insert(tk.END, f"Modified GTFS saved as {new_gtfs_filename}\n")

            # Remove route_ids that have no trips left in trips.txt from the listbox
            for route_id in routes_to_remove:
                all_routes = [route for route in all_routes if not route.startswith(route_id)]
                route_ids_listbox.delete(0, tk.END)  # Clear the listbox
                for route in all_routes:
                    route_ids_listbox.insert(tk.END, route)

        tk.Button(modify_window, text="Apply Modification", command=process_modification).pack(pady=20)
   
    
    def generate_synthetic_dataset(self):
        """Open a window for generating the synthetic dataset."""
        synth_window = Toplevel(self.master)
        synth_window.title("Generate PT Stops Dataset")
        synth_window.geometry("600x600")

        # Stop Output File
        Label(synth_window, text="Stop Output File:").pack(pady=5)
        stopout_frame = tk.Frame(synth_window)
        stopout_frame.pack(pady=5)
        self.stopout_entry = Entry(stopout_frame, width=60)
        self.stopout_entry.pack(side=tk.LEFT)
        Button(stopout_frame, text="Browse", command=self.load_stopout_file).pack(side=tk.LEFT, padx=5)

        # GTFS Directory
        Label(synth_window, text="GTFS Directory:").pack(pady=5)
        gtfs_frame = tk.Frame(synth_window)
        gtfs_frame.pack(pady=5)
        self.gtfs_entry_synth = Entry(gtfs_frame, width=60)
        self.gtfs_entry_synth.pack(side=tk.LEFT)
        Button(gtfs_frame, text="Browse", command=self.load_gtfs_directory_synth).pack(side=tk.LEFT, padx=5)

        # Custom GTFS Stops File
        Label(synth_window, text="Simulated GTFS Stops File:").pack(pady=5)
        custom_gtfs_frame = tk.Frame(synth_window)
        custom_gtfs_frame.pack(pady=5)
        self.custom_gtfs_entry = Entry(custom_gtfs_frame, width=60)
        self.custom_gtfs_entry.pack(side=tk.LEFT)
        Button(custom_gtfs_frame, text="Browse", command=self.load_custom_gtfs_stops_file).pack(side=tk.LEFT, padx=5)

        # Calendar Input for Date Selection
        Label(synth_window, text="Select the date for arrival, departure, and stopinfo started times:").pack(pady=20)
        self.date_cal = Calendar(synth_window, selectmode='day', date_pattern='dd/mm/yyyy')
        self.date_cal.pack(pady=5)

        # Button to generate CSV
        Button(synth_window, text="Generate Dataset", command=self.process_generation).pack(pady=20)

    def load_stopout_file(self):
        """Load the stop output file and display the path in the entry."""
        stopout_file = self.file_handler.load_stopout_file()
        if stopout_file:
            self.stopout_entry.delete(0, tk.END)
            self.stopout_entry.insert(0, stopout_file)

    def load_gtfs_directory_synth(self):
        """Load the GTFS directory and update the entry field in the Generate Synthetic Dataset window."""
        gtfs_path = filedialog.askdirectory(title="Select GTFS Directory")
        if gtfs_path:
            self.gtfs_entry_synth.delete(0, tk.END)
            self.gtfs_entry_synth.insert(0, gtfs_path)
        else:
            # Handle case where no directory is selected
            pass

    def load_custom_gtfs_stops_file(self):
        """Load the custom GTFS stops file and display the path in the entry."""
        custom_gtfs_stops_file = self.file_handler.load_custom_gtfs_stops_file()
        if custom_gtfs_stops_file:
            self.custom_gtfs_entry.delete(0, tk.END)
            self.custom_gtfs_entry.insert(0, custom_gtfs_stops_file)

    def process_generation(self):
        """Generate the synthetic dataset based on the selected files and dates."""
        selected_date = self.date_cal.get_date()

        if not self.stopout_entry.get():
            messagebox.showerror("Error", "No stop output file loaded.")
            return
        if not self.gtfs_entry.get():
            messagebox.showerror("Error", "No GTFS directory loaded.")
            return
        if not self.custom_gtfs_entry.get():
            messagebox.showerror("Error", "No custom GTFS stops file loaded.")
            return

        try:
            # Generate the dataset
            file_name = self.data_processor.generate_stopout_dataset(
                self.stopout_entry.get(), self.gtfs_entry.get(), self.custom_gtfs_entry.get(), selected_date
            )
            messagebox.showinfo("Success", f"Dataset successfully created and saved as '{file_name}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

            
    def generate_od_matrices(self):
        gen_window = tk.Toplevel(self.master)
        gen_window.title("Generate OD Matrices")
        gen_window.geometry("500x500")

        private_sliders = []
        public_sliders = []

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
                private_normalized_percentages = self.data_processor.normalize_percentages([slider.get() for slider in private_sliders])
                public_normalized_percentages = self.data_processor.normalize_percentages([slider.get() for slider in public_sliders])

                if create_private and not self.data_processor.validate_percentages(private_normalized_percentages):
                    messagebox.showwarning("Warning", "Please set valid percentages for Private Transport (cannot be equal to 0).")
                    return

                if create_public and not self.data_processor.validate_percentages(public_normalized_percentages):
                    messagebox.showwarning("Warning", "Please set valid percentages for Public Transport (cannot be equal to 0).")
                    return

                if create_private and private_csv:
                    output_file = self.data_processor.create_od_matrices_for_csv(private_csv, private_normalized_percentages, prefix="private")
                    self.output_text.insert(tk.END, f"Private OD Matrix saved as '{output_file}'\n")

                if create_public and public_csv:
                    output_file = self.data_processor.create_od_matrices_for_csv(public_csv, public_normalized_percentages, prefix="public")
                    self.output_text.insert(tk.END, f"Public OD Matrix saved as '{output_file}'\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error generating OD matrices: {e}")

        # Private Transport CSV File Selection
        tk.Label(gen_window, text="Private CSV File:").pack(anchor='w', padx=5, pady=2)
        private_csv_entry = tk.Entry(gen_window, width=70)
        private_csv_entry.pack(anchor='w', padx=5, pady=2)
        tk.Button(gen_window, text="Browse", command=lambda: self.file_handler.load_csv_file(private_csv_entry, self.output_text)).pack(anchor='w', padx=5, pady=2)

        # Public Transport CSV File Selection
        tk.Label(gen_window, text="Public CSV File:").pack(anchor='w', padx=5, pady=2)
        public_csv_entry = tk.Entry(gen_window, width=70)
        public_csv_entry.pack(anchor='w', padx=5, pady=2)
        tk.Button(gen_window, text="Browse", command=lambda: self.file_handler.load_csv_file(public_csv_entry, self.output_text)).pack(anchor='w', padx=5, pady=2)

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

    def open_generate_dataset_window(self):
        """Open a window for generating the edge dataset."""
        edge_window = Toplevel(self.master)
        edge_window.title("Generate Edge Dataset")
        edge_window.geometry("600x600")

        # Entry for the Edge XML file path
        Label(edge_window, text="Edge XML File:").pack(pady=5)
        self.edge_entry = Entry(edge_window, width=60)
        self.edge_entry.pack(pady=5)
        Button(edge_window, text="Browse", command=self.load_edge_file).pack(pady=5)

        # Entry for the TAZ XML file path
        Label(edge_window, text="Districts (TAZ) XML File:").pack(pady=5)
        self.taz_entry = Entry(edge_window, width=60)
        self.taz_entry.pack(pady=5)
        Button(edge_window, text="Browse", command=self.load_taz_file).pack(pady=5)

        # Entry for CSV filename
        Label(edge_window, text="Enter the name for the output CSV file:").pack(pady=5)
        self.csv_entry = Entry(edge_window, width=60)
        self.csv_entry.pack(pady=5)

        # Calendar for date selection
        Label(edge_window, text="Select the date:").pack(pady=5)
        self.cal = Calendar(edge_window, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=5)

        # Button to generate CSV
        Button(edge_window, text="Generate CSV", command=self.generate_csv).pack(pady=20)

    def load_edge_file(self):
        """Load the edge XML file and display the path in the entry."""
        edge_file = self.file_handler.select_edge_xml_file()
        if edge_file:
            self.edge_entry.delete(0, 'end')
            self.edge_entry.insert(0, edge_file)

    def load_taz_file(self):
        """Load the TAZ XML file and display the path in the entry."""
        taz_file = self.file_handler.select_taz_xml_file()
        if taz_file:
            self.taz_entry.delete(0, 'end')
            self.taz_entry.insert(0, taz_file)

    def generate_csv(self):
        """Generate the CSV dataset based on the selected files and date."""
        edge_xml_filename = self.edge_entry.get()
        taz_xml_filename = self.taz_entry.get()
        csv_filename = self.csv_entry.get()
        date_str = self.cal.get_date()

        if not edge_xml_filename or not taz_xml_filename or not csv_filename:
            print("Error: Please ensure all files are selected and a CSV filename is provided.")
            return

        self.data_processor.extract_data_from_xml(edge_xml_filename, taz_xml_filename, csv_filename, date_str)

    def open_trips_xml_window(self):
        """Open a window to load files and process trips XML data."""
        
        # Create a new window
        trips_window = Toplevel(self.master)
        trips_window.title("Process Trips XML")
        trips_window.geometry("600x700")

        # Load Trips XML File
        Label(trips_window, text="Trips XML File:").pack(pady=5)
        trips_frame = tk.Frame(trips_window)
        trips_frame.pack(pady=5)
        self.trips_entry = Entry(trips_frame, width=60)  # trips_entry is created here
        self.trips_entry.pack(side=tk.LEFT)
        Button(trips_frame, text="Browse", command=self.load_trips_xml_file).pack(side=tk.LEFT, padx=5)

        # Button to retrieve unique types and vTypes
        Button(trips_window, text="Retrieve Unique Types and vTypes", command=self.retrieve_unique_values).pack(pady=10)

        # Listbox for displaying and selecting unique values (Multiple Selection)
        Label(trips_window, text="Select types or vTypes to include in CSV:").pack(pady=5)
        self.unique_values_listbox = Listbox(trips_window, selectmode=MULTIPLE, height=10)
        self.unique_values_listbox.pack(pady=5)

        # Calendar for selecting the date for 'depart' and 'arrival'
        Label(trips_window, text="Select the date for depart and arrival:").pack(pady=5)
        self.cal = Calendar(trips_window, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)

        # Button to process and save CSV
        Button(trips_window, text="Process and Save as CSV", command=self.process_and_save_csv).pack(pady=20)

    def load_trips_xml_file(self):
        """Load the trips XML file and display the path in the entry."""
        trips_file = self.file_handler.load_xml_file()
        if trips_file and len(trips_file) > 0:
            self.trips_entry.delete(0, tk.END)
            self.trips_entry.insert(0, trips_file)

    def retrieve_unique_values(self):
        """Retrieve unique types and vTypes from the XML file and display in Listbox."""
        xml_file = self.trips_entry.get()

        if not xml_file:
            messagebox.showerror("Error", "No XML file loaded.")
            return

        # Get unique types and vTypes
        types, vtypes = self.data_processor.get_unique_types_and_vtypes(xml_file)

        # Combine both lists and update Listbox
        unique_values = types + vtypes
        self.unique_values_listbox.delete(0, tk.END)
        for value in unique_values:
            self.unique_values_listbox.insert(tk.END, value)

    def process_and_save_csv(self):
        """Process the XML based on selected criteria and save as a CSV."""
        xml_file = self.trips_entry.get()
        selected_indices = self.unique_values_listbox.curselection()

        if not xml_file or not selected_indices:
            messagebox.showerror("Error", "Please load a file and select at least one filter value.")
            return

        selected_values = [self.unique_values_listbox.get(i) for i in selected_indices]

        # Get the selected date from the calendar
        selected_date = self.cal.get_date()

        # Determine whether the user selected 'type' or 'vType'
        types, vtypes = self.data_processor.get_unique_types_and_vtypes(xml_file)
        filter_by = 'type' if any(value in selected_values for value in types) else 'vType'

        # Choose where to save the CSV file
        csv_file = self.file_handler.save_csv_file()
        if not csv_file:
            messagebox.showerror("Error", "No CSV file selected for saving.")
            return

        # Process the XML and save the result as CSV
        self.data_processor.process_trips_xml(xml_file, filter_by, selected_values, csv_file, selected_date)

    
class FileHandler:
    def __init__(self):
        """Initialize the FileHandler class."""
        self.supported_file_types = [
            ("CSV files", "*.csv"),
            ("XML files", "*.xml"),
            ("All files", "*.*")
        ]

    def load_file(self, file_type=None):
        """Handle file loading."""
        if file_type == 'csv':
            return self.load_csv_file()
        elif file_type == 'xml':
            return self.load_xml_file()
        else:
            return filedialog.askopenfilename(filetypes=self.supported_file_types)
            
    def load_csv_file(self, entry_field, output_text):
        """Load a CSV file and update the entry field."""
        try:
            csv_file = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
            if csv_file:
                entry_field.delete(0, tk.END)
                entry_field.insert(0, csv_file)
                output_text.insert(tk.END, f"Loaded CSV File: {csv_file}\n")
            else:
                output_text.insert(tk.END, "No CSV file selected.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading CSV file: {e}")

    def load_xml_file(self):
        """Open a dialog to select an XML file and return its path."""
        file_path = filedialog.askopenfilename(title="Select trips XML File", filetypes=[("XML files", "*.xml")])
        return file_path  # Return the file path as a string
        
    def load_stopout_file(self):
        """Load the stop output file."""
        file_path = filedialog.askopenfilename(title="Select Stop Output File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        return file_path if file_path else None

    def load_gtfs_file_main(self):
        """Load GTFS zip file in the Main GUI and update the entry field."""
        self.gtfs_file = filedialog.askopenfilename(title="Select GTFS Zip File", filetypes=[("Zip files", "*.zip")])
        if self.gtfs_file:
            self.gtfs_entry_main.delete(0, tk.END)
            self.gtfs_entry_main.insert(0, self.gtfs_file)
            # Output feedback can be managed separately if needed
        else:
            # Handle case where no file is selected
            pass

    def load_custom_gtfs_stops_file(self):
        """Load the custom GTFS stops file."""
        file_path = filedialog.askopenfilename(title="Select Custom GTFS Stops File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        return file_path if file_path else None

    def parse_edges_from_network_file(self, network_file):
        """Parse edges from the network file."""
        edges = {}
        try:
            tree = ET.parse(network_file)
            root = tree.getroot()
            for edge in root.findall('edge'):
                edge_id = edge.attrib['id']
                edge_name = edge.attrib.get('name', 'Unknown')
                if edge_name not in edges:
                    edges[edge_name] = []
                edges[edge_name].append(edge_id)
            return edges
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing network file: {str(e)}")
            return None

    def save_xml_file(self, xml_element, output_filename):
        """Save an XML element to a file."""
        try:
            xml_str = minidom.parseString(ET.tostring(xml_element)).toprettyxml(indent="    ")
            with open(output_filename, 'w') as f:
                f.write(xml_str)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save XML file: {e}")
            return False
    
    def read_od_matrix(self, filename):
        """Read an OD matrix from a file."""
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
        """Write an OD matrix to a file."""
        with open(filename, 'w') as file:
            for line in header_lines:
                file.write(f"{line}\n")
            for entry in od_data:
                file.write(f"{entry[0]:4d} {entry[1]:4d} {entry[2]:4d}\n")
                
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
    
    def select_edge_xml_file(self):
        """Prompt the user to select the edge XML file."""
        return filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

    def select_taz_xml_file(self):
        """Prompt the user to select the TAZ XML file."""
        return filedialog.askopenfilename(filetypes=[("XML files", "*.taz.xml")])
        
    def open_trips_xml_window(self):
        """Open a window to load files and process trips XML data."""
        
        # Create a new window
        trips_window = Toplevel(self.master)
        trips_window.title("Process Trips XML")
        trips_window.geometry("600x600")

        # Load Trips XML File
        Label(trips_window, text="Trips XML File:").pack(pady=5)
        trips_frame = tk.Frame(trips_window)
        trips_frame.pack(pady=5)
        self.trips_entry = Entry(trips_frame, width=60)
        self.trips_entry.pack(side=tk.LEFT)
        Button(trips_frame, text="Browse", command=self.load_trips_xml_file).pack(side=tk.LEFT, padx=5)

        # Button to retrieve unique types and vTypes
        Button(trips_window, text="Retrieve Unique Types and vTypes", command=self.retrieve_unique_values).pack(pady=10)

        # Listbox for displaying and selecting unique values (Multiple Selection)
        Label(trips_window, text="Select types or vTypes to include in CSV:").pack(pady=5)
        self.unique_values_listbox = Listbox(trips_window, selectmode=MULTIPLE, height=10)
        self.unique_values_listbox.pack(pady=5)

        # Button to process and save CSV
        Button(trips_window, text="Process and Save as CSV", command=self.process_and_save_csv).pack(pady=20)

    def load_trips_xml_file(self):
        """Load the trips XML file and display the path in the entry."""
        trips_file = self.file_handler.load_xml_file()
        if trips_file and len(trips_file) > 0:
            self.trips_entry.delete(0, tk.END)
            self.trips_entry.insert(0, trips_file)

    def retrieve_unique_values(self):
        """Retrieve unique types and vTypes from the XML file and display in Listbox."""
        xml_file = self.trips_entry.get()

        if not xml_file:
            print("No XML file loaded.")
            return

        # Get unique types and vTypes
        types, vtypes = self.data_processor.get_unique_types_and_vtypes(xml_file)

        # Combine both lists and update Listbox
        unique_values = types + vtypes
        self.unique_values_listbox.delete(0, tk.END)
        for value in unique_values:
            self.unique_values_listbox.insert(tk.END, value)
       

    def save_csv_file(self):
        """Open a dialog to save a CSV file and return the file path."""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        return file_path
        
class DataProcessor:
    def __init__(self):
        self.edges_closures = []

    def populate_road_list(self, edges):
        """Process and store available roads from network data."""
        return list(edges.keys())

    def create_rerouter_element(self, rerouter_id, edge_ids, begin, end):
        """Create a rerouter element for road closures."""
        rerouter = ET.Element('rerouter', id=str(rerouter_id), edges=' '.join(edge_ids))
        interval = ET.SubElement(rerouter, 'interval', begin=str(begin), end=str(end))
        for edge_id in edge_ids:
            closingReroute = ET.SubElement(interval, 'closingReroute', id=edge_id, disallow='all')
        return rerouter

    def generate_closure_xml(self, edges_closures):
        """Generate an XML structure for road closures."""
        additional = ET.Element('additional')
        for rerouter_id, (edge_ids, begin, end) in enumerate(edges_closures, start=1):
            rerouter_element = self.create_rerouter_element(rerouter_id, edge_ids, begin, end)
            additional.append(rerouter_element)
        return additional

    def add_road_closure(self, edges, selected_road_names, begin_seconds, end_seconds):
        """Add road closure information to the internal list."""
        for road_name in selected_road_names:
            edge_ids = edges.get(road_name)
            if edge_ids:
                self.edges_closures.append((edge_ids, begin_seconds, end_seconds))
            else:
                messagebox.showwarning("Warning", f"Road {road_name} not found in the network.")
                
    def modify_od_matrix(self, od_matrix_file, from_zone, to_zone, operation, amount, file_handler):
        """Modify the OD matrix based on user input."""
        header_lines, od_data = file_handler.read_od_matrix(od_matrix_file)

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

        return header_lines, updated_od_data
        
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

    def normalize_percentages(self, percentages):
        """Normalize the percentage values to sum to 1."""
        total = sum(percentages)
        if total == 0:
            return percentages
        return [x / total for x in percentages]

    def validate_percentages(self, percentages):
        """Validate that all percentages are set and non-zero."""
        return all(p > 0 for p in percentages)
        
    def generate_stopout_dataset(self, stopout_file, gtfs_path, custom_gtfs_stops_file, arrival_date, departure_date, stopinfo_started_date):
        """Generate synthetic dataset based on the stop output data."""
        try:
            # Load GTFS data from files
            stops_path = os.path.join(gtfs_path, "stops.txt")
            stop_times_path = os.path.join(gtfs_path, "stop_times.txt")
            trips_path = os.path.join(gtfs_path, "trips.txt")

            # Load data from CSV files
            csv_stops = pd.read_csv(stops_path, sep=',', dtype='unicode')
            csv_stop_times = pd.read_csv(stop_times_path, sep=',', dtype='unicode')
            csv_trips = pd.read_csv(trips_path, sep=',', dtype='unicode')
            csv_stopout = pd.read_csv(stopout_file, sep=';', dtype='unicode')
            csv_gtfs_stops = pd.read_csv(custom_gtfs_stops_file, sep=';', dtype='unicode')

            # File merging
            csv_stop_times_trips = csv_stop_times.merge(csv_trips, on=['trip_id'])
            csv_stoptimes_stops = csv_stop_times.merge(csv_stops, on=["stop_id"])
            csv_stoptimes_stops2 = csv_stoptimes_stops[['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_name', 'stop_sequence', 'stop_lat', 'stop_lon']]
            csv_stopout.rename(columns={'stopinfo_busStop': 'busStop_id'}, inplace=True)
            csv_stopout.rename(columns={'stopinfo_id': 'trip_id'}, inplace=True)
            csv_stopout2 = csv_stopout[['busStop_id', 'stopinfo_delay', 'stopinfo_ended', 'trip_id', 'stopinfo_initialPersons', 'stopinfo_loadedPersons', 'stopinfo_started', 'stopinfo_type', 'stopinfo_unloadedPersons']]
            csv_stops_stopout2 = csv_gtfs_stops.merge(csv_stopout2, on=["busStop_id"])
            csv_stopout3 = csv_stoptimes_stops2.merge(csv_stops_stopout2, on=["trip_id", "stop_name"])
            routes = pd.read_csv(trips_path, sep=',', dtype='unicode')
            csv_stopout4 = csv_stopout3.merge(routes, on=["trip_id"])

            # Arrival and departure time correction
            data = csv_stopout4
            data['arrival_time'] = data['arrival_time'].str.replace('^24:', '00:', regex=True)
            data['arrival_time'] = data['arrival_time'].str.replace('^25:', '01:', regex=True)
            data['arrival_time'] = data['arrival_time'].str.replace('^26:', '02:', regex=True)
            data['arrival_time'] = data['arrival_time'].str.replace('^27:', '03:', regex=True)
            data['arrival_time'] = data['arrival_time'].str.replace('^28:', '04:', regex=True)

            data['departure_time'] = data['departure_time'].str.replace('^24:', '00:', regex=True)
            data['departure_time'] = data['departure_time'].str.replace('^25:', '01:', regex=True)
            data['departure_time'] = data['departure_time'].str.replace('^26:', '02:', regex=True)
            data['departure_time'] = data['departure_time'].str.replace('^27:', '03:', regex=True)
            data['departure_time'] = data['departure_time'].str.replace('^28:', '04:', regex=True)

            data['stopinfo_started'] = data['stopinfo_started'].str.replace('^1:00:', '00:', regex=True)

            # Add date
            data['arrival_time'] = pd.to_datetime(arrival_date + ' ' + data['arrival_time'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            data['departure_time'] = pd.to_datetime(departure_date + ' ' + data['departure_time'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            data['stopinfo_started'] = pd.to_datetime(stopinfo_started_date + ' ' + data['stopinfo_started'].str.split('.').str[0], format='%d/%m/%Y %H:%M:%S', errors='coerce')

            # Check for null values after conversion
            if data['arrival_time'].isnull().any() or data['departure_time'].isnull().any() or data['stopinfo_started'].isnull().any():
                raise ValueError("Invalid time format. Please ensure the times are in the correct format.")

            # Rename columns
            data.rename(columns={'busStop_id': 'stop_id_SUMO'}, inplace=True)

            # Calculate SUMO delay
            data['sumo_delay'] = (data['stopinfo_started'] - data['arrival_time']).dt.total_seconds()

            # Generate output file name based on the user-provided arrival date
            arrival_date_dt = datetime.strptime(arrival_date, '%d/%m/%Y')
            file_name = f"Dataset_{arrival_date_dt.day}_{arrival_date_dt.strftime('%B')}_{arrival_date_dt.year}.csv"

            # Save the final synthetic dataset
            data.to_csv(file_name, index=False, sep=';')
            return file_name

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: {e}. Please check the file path and ensure the file exists.")
        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(f"Error: {e}. There is an issue with parsing the CSV files. Please check the file format.")
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
            
    def create_od_matrices_for_csv(self, csv_file, percentages, prefix):
        """Create OD matrices based on the CSV file and percentages."""
        generated_files = []
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

                generated_files.append(filename)

        except Exception as e:
            raise Exception(f"Error generating OD matrices: {e}")

        return generated_files
        
    def normalize_percentages(self, percentages):
            """Normalize the percentage values to sum to 1."""
            total = sum(percentages)
            if total == 0:
                return percentages
            return [x / total for x in percentages]

    def validate_percentages(self, percentages):
            """Validate that all percentages are set and non-zero."""
            return all(p > 0 for p in percentages)

    def extract_data_from_xml(self, edge_xml_filename, taz_xml_filename, csv_filename, date_str):
        """Extract data from XML files and write to a CSV file."""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.")
            return

        # Parse edge XML file
        edge_tree = ET.parse(edge_xml_filename)
        edge_root = edge_tree.getroot()

        # Parse TAZ XML file
        taz_tree = ET.parse(taz_xml_filename)
        taz_root = taz_tree.getroot()

        # Dictionary to hold TAZ data
        taz_data = {}
        for taz in taz_root.findall('taz'):
            taz_id = taz.attrib.get('id', '')
            edges = taz.attrib.get('edges', '').split()
            for edge_id in edges:
                taz_data[edge_id] = taz_id

        # List to hold data rows
        data_rows = []

        # Iterate over each interval
        for interval in edge_root.findall('interval'):
            interval_begin = interval.attrib.get('begin', '')
            interval_end = interval.attrib.get('end', '')
            for edge in interval.findall('edge'):
                edge_id = edge.attrib.get('id', '')
                entered = edge.attrib.get('entered', '0')
                left = edge.attrib.get('left', '0')
                traveltime = edge.attrib.get('traveltime', '0')
                density = edge.attrib.get('density', '0')
                occupancy = edge.attrib.get('occupancy', '0')
                speed = edge.attrib.get('speed', '0')
                taz = taz_data.get(edge_id, '')

                # Append the extracted data to the rows list
                data_rows.append({
                    'date': date_str,
                    'interval_begin': interval_begin,
                    'interval_end': interval_end,
                    'edge_id': edge_id,
                    'entered': entered,
                    'left': left,
                    'traveltime': traveltime,
                    'density': density,
                    'occupancy': occupancy,
                    'speed': speed,
                    'taz': taz
                })

        # Write data to CSV
        with open(csv_filename, mode='w', newline='') as csv_file:
            fieldnames = ['date', 'interval_begin', 'interval_end', 'edge_id', 'entered', 'left', 'traveltime', 'density', 'occupancy', 'speed', 'taz']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for row in data_rows:
                writer.writerow(row)

        print(f"Data has been successfully written to {csv_filename}")
        
    def get_unique_types_and_vtypes(self, xml_file):
        """Retrieve unique 'type' and 'vType' values from the XML file."""
        tree = ET.parse(xml_file)
        root = tree.getroot()

        types = set()
        vtypes = set()

        for tripinfo in root.findall('tripinfo'):
            type_value = tripinfo.attrib.get('type')
            vtype_value = tripinfo.attrib.get('vType')
            
            if type_value:
                types.add(type_value)
            if vtype_value:
                vtypes.add(vtype_value)

        return sorted(types), sorted(vtypes)  # Return sorted lists of unique types and vTypes

    def process_trips_xml(self, xml_file, filter_by, filter_values, csv_file, selected_date):
        """Process the XML file, filter by selected types or vTypes, and save the result as a CSV file."""
        tree = ET.parse(xml_file)
        root = tree.getroot()

        rows = []
        headers = ["id", "depart", "arrival", "duration", "routeLength", "timeLoss", "speedFactor", "waitingTime"]

        for tripinfo in root.findall('tripinfo'):
            if tripinfo.attrib.get(filter_by) in filter_values:
                # Apply the selected date to the depart and arrival times
                depart_time = tripinfo.attrib.get("depart", "")
                arrival_time = tripinfo.attrib.get("arrival", "")
                
                # Combine the selected date with the time from the XML (if available)
                if depart_time:
                    depart = f"{selected_date} {depart_time.split(' ')[-1]}"  # Format: yyyy-mm-dd HH:MM:SS
                else:
                    depart = selected_date

                if arrival_time:
                    arrival = f"{selected_date} {arrival_time.split(' ')[-1]}"  # Format: yyyy-mm-dd HH:MM:SS
                else:
                    arrival = selected_date

                # Process the timeLoss to remove fractional seconds
                raw_time_loss = tripinfo.attrib.get("timeLoss", "00:00:00")
                
                # Remove the fractional part of the time (anything after the dot)
                time_loss = raw_time_loss.split('.')[0]  # Keep only the hh:mm:ss part

                # Append row to be saved in the CSV
                row = {
                    "id": tripinfo.attrib.get("id"),
                    "depart": depart,
                    "arrival": arrival,
                    "duration": tripinfo.attrib.get("duration"),
                    "routeLength": tripinfo.attrib.get("routeLength"),
                    "timeLoss": time_loss,  # formatted as hh:mm:ss without fractional seconds
                    "speedFactor": tripinfo.attrib.get("speedFactor"),
                    "waitingTime": tripinfo.attrib.get("waitingTime")
                }
                rows.append(row)

        # Save to CSV
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Processed data saved to: {csv_file}")
   

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
