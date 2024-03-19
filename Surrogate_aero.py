# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:03:32 2022

@author: paubo
"""

import numpy as np
import openmdao.api as om
import pandas as pd


# Set up inputs and outputs

db = pd.read_excel('DragPolarResults3.xlsx')  

Sweep = db[['Sweep']].to_numpy().flatten()
AoA = db[['AoA']].to_numpy().flatten()
Altitude = db[['Altitude']].to_numpy().flatten()
Mach = db[['Mach']].to_numpy().flatten()
CL = db[['CL']].to_numpy().flatten()
CD = db[['CD']].to_numpy().flatten()

aero = om.MetaModelUnStructuredComp(default_surrogate=om.ResponseSurface())
aero.add_input('Sweep', 1.0, training_data=Sweep)
aero.add_input('AoA', 4.0, training_data=AoA)
aero.add_input('Altitude', 4000, training_data=Altitude)
aero.add_input('Mach', 1.3, training_data=Mach)

aero.add_output('CL', 0.5596, training_data=CL)
aero.add_output('CD', 0.0638, training_data=CD)
aero.declare_partials('*', '*', method='fd')
# Set up the OpenMDAO problem
prob = om.Problem()
prob.model.add_subsystem('aero', aero)
prob.setup()

# Set inputs to surrogate model
prob.set_val('aero.Sweep', 41)
prob.set_val('aero.AoA', 10)
prob.set_val('aero.Altitude', 10000)
prob.set_val('aero.Mach', 0.9)

prob.run_model()

print(prob.get_val('aero.CL'))
print(prob.get_val('aero.CD'))

prob.check_partials(compact_print=True);
