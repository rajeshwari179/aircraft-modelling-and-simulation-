# CSE-6730-Project-Group-1-Aircraft-Modelling-and-Simulation
Code repo for Group 1's CSE 6730 project

The aim is to create a simulation of a variable-geometry aircraft for climb, cruise & descent. This project relies on 2 tools:

1. [Dymos](https://openmdao.github.io/dymos/) and [OpenMDAO](https://openmdao.org/) - NASA tools for variable control optimization. An example for a climb simulation for a fixed wing aircraft is provided [here](https://openmdao.github.io/dymos/examples/min_time_climb/min_time_climb.html).
2. [OpenVSP](https://openvsp.org/) - NASA tool for aircraft modelling. 


# How to run:
To run the experiment, run *Supersonic_Climb_Morphing.py*. The different flags at the end of the file will determine the parameters for the experiment:
* objective = 0 # 0 == Airtime ; 1 == Fuel Usage
* variable_geometry = False
* phase = 0 # 0 == Climb ; 1 == Descend ; 2 == Cruise
To test the main experiment, which has been implemented, set the objective to Fuel Usage, Variable Geometry to true, and Phase to Climb.

# Other Dependencies:

## Python Project Dependencies: (Install these using pip)
* openmdao
* dymos
* matplotlib
* openpyxl
