import numpy as np
import openmdao.api as om
import pandas as pd
db = pd.read_excel('Results_Final.xlsx')  
Sweep = db['Sweep'].to_numpy().flatten()
tipchord = db['TipChord'].to_numpy().flatten()
Twist = db['Twist'].to_numpy().flatten()
AoA = db['AoA'].to_numpy().flatten()
Altitude = db['Altitude'].to_numpy().flatten()
Mach = db['Mach'].to_numpy().flatten()
CL = db['CL'].to_numpy().flatten()
CD = db['CD'].to_numpy().flatten()

# Note in the data that Mach varies fastest (the first 10 datapoints correspond to Alt=0)
# Altitude is given in ft and thrust is given in lbf
AERO_DATA = {'twist': np.array([-15,-5,5,14,15]),
             'tipchord': np.array([5,7,9,11,13,15]),
             'sweep': np.array([1,5,9,17,33,37,41,45,49,53,57,61,65]),
             'h': np.array([0,4000,8000,12000,16000,18000]),
             'mach': np.array([0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9], dtype=np.float64),
             'alpha': np.array([-6,-4,-2,0,1,2,3,4,6,8,10,12,14,16]),
             'CL' : CL.reshape(5,6,13,6,10,14),
             'CD' : CD.reshape(5,6,13,6,10,14)
                }


class LiftDragCoeffComp(om.MetaModelStructuredComp):
    """ Interpolates aerodynamics for lift/drag coefficients """

    def setup(self):
        nn = self.options['vec_size']
        self.add_input(name='twist', val=np.ones(nn), units='deg', training_data=AERO_DATA['twist'])
        self.add_input(name='tipchord', val=np.ones(nn), units='m', training_data=AERO_DATA['tipchord'])
        self.add_input(name='sweep', val= np.ones(nn), units='deg', training_data=AERO_DATA['sweep'])
        self.add_input(name='h', val=0.0 * np.ones(nn), units='m', training_data=AERO_DATA['h'])
        self.add_input(name='mach', val=0.2 * np.ones(nn), training_data=AERO_DATA['mach'])
        self.add_input(name='alpha', val=0.0 * np.ones(nn), units='deg', training_data=AERO_DATA['alpha'])
        self.add_output(name='CL', val=np.zeros(nn),
                        training_data=AERO_DATA['CL'])
        self.add_output(name='CD', val=np.zeros(nn),
                        training_data=AERO_DATA['CD'])
