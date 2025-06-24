import traci

# STEP 1: Define SUMO configuration
sumo_binary = "sumo-gui"  # Use "sumo" for CLI mode
sumo_config = "cfg_rip1.sumocfg"  # Replace with your actual SUMO config file
sumo_cmd = [sumo_binary, "-c", sumo_config]

# STEP 2: Start TraCI
traci.start(sumo_cmd)

# STEP 3: Define the edge to be closed
edge_to_close = "42155763-AddedOffRampEdge"

# Define closure timing (in seconds)
closure_start = 10000       # Closure starts at 02:46:40
closure_end = 57600         # Reopens at 16:00:00

# Flags to avoid repeating actions
closed = False
reopened = False

# STEP 4: Run simulation step-by-step
try:
    while traci.simulation.getMinExpectedNumber() > 0:
        step = traci.simulation.getTime()

        # Edge closure
        if step >= closure_start and not closed:
            try:
                traci.edge.setAllowed(edge_to_close, [])  # Disallow all vehicle types
                print(f"[STEP {step}] ➤ Edge CLOSED: {edge_to_close}")

                # Reroute all active vehicles
                for veh_id in traci.vehicle.getIDList():
                    try:
                        traci.vehicle.rerouteTraveltime(veh_id)
                    except traci.TraCIException as e:
                        print(f"⚠️ Could not reroute vehicle {veh_id}: {e}")
                        try:
                            traci.vehicle.setSpeed(veh_id, 0)
                        except:
                            pass
                closed = True

            except traci.TraCIException as e:
                print(f"⚠️ Could not close edge '{edge_to_close}': {e}")

        # Edge reopening
        if step >= closure_end and closed and not reopened:
            try:
                traci.edge.setAllowed(edge_to_close, ["passenger", "bus", "truck"])  # Restore allowed types
                print(f"[STEP {step}] ➤ Edge REOPENED: {edge_to_close}")
                reopened = True
            except traci.TraCIException as e:
                print(f"⚠️ Could not reopen edge '{edge_to_close}': {e}")

        traci.simulationStep()

except traci.exceptions.FatalTraCIError:
    print("⚠️ SUMO closed unexpectedly. Possibly a vehicle had no valid route or the network was disconnected.")

finally:
    traci.close()
