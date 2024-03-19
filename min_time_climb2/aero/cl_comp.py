import numpy as np

import openmdao.api as om


class CLComp(om.ExplicitComponent):

    def initialize(self):
        self.options.declare('num_nodes', types=int)

    def setup(self):
        nn = self.options['num_nodes']

        # Inputs
        self.add_input('CLa', shape=(nn,), desc='alpha lift coefficient', units=None)
        self.add_input('alpha', shape=(nn,), desc='angle of attck', units='rad')
        self.add_input('sweep', shape=(nn,), desc='sweep angle', units='deg')

        # Outputs
        self.add_output(name='CL', val=np.ones(nn), desc='lift coefficient', units=None)

        # Jacobian
        ar = np.arange(nn)
        self.declare_partials(of='CL', wrt='CLa', rows=ar, cols=ar)
        self.declare_partials(of='CL', wrt='alpha', rows=ar, cols=ar)
        self.declare_partials(of='CL', wrt='sweep', rows=ar, cols=ar)
        
    def compute(self, inputs, outputs):
        outputs['CL'][:] = inputs['CLa'] * inputs['alpha'] + 0.02*inputs['sweep']

    def compute_partials(self, inputs, partials):
        partials['CL', 'CLa'] = inputs['alpha']
        partials['CL', 'alpha'] = inputs['CLa']
        partials['CL', 'sweep'] = 0.02
