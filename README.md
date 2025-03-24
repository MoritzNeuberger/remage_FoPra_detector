# Remage Simulation Tutorial

This tutorial guides you through the process of setting up a simple test stand geometry and running a simulation using remage. Follow the steps below to generate geometry, run the simulation, and visualize the results.

## Prerequisites

Ensure you have Apptainer installed on your system. If not, you can install it by following the instructions on the [Apptainer website](https://apptainer.org/).

## Steps

### Step 1: Create a python environment with the relevant packages

Create a venv environment, activate it and install all the required python packages.
```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install pyg4ometry legend_pygeom_tools legend_pygeom_hpges numpy awkward matplotlib
```

### Step 2: Run the Geometry Generation Script

Run the `generate_geometryl.py` script to generate the `simple_teststand.gdml` and `pv_reg.mac` files:
```sh
python generate_geometryl.py
```
   
### Step 3: Modify the `run.mac` File

Copy the sensitive volume registration lines from `pv_reg.mac` into `run.mac` in the indicated area before the `/run/initialize` line. This step is crucial for ensuring the simulation recognizes the necessary volumes.

### Step 4: Create and Enter the Latest Remage Container

1. Build the Remage container:
```sh
apptainer build remage_latest.sif docker://legendexp/remage:latest
```

2. Enter the Remage container:
```sh
apptainer shell remage_latest.sif
```

### Step 5: Run Remage

Execute the Remage simulation using the `run.mac` script:
```sh
remage run.mac
```
   
### Step 6: Visualize the Simulation

Run the `analyze_simulation.py` script to visualize the simulation results:
```sh
python analyze_simulation.py
```
