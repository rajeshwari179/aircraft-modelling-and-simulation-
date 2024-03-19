import numpy as np
import pandas as pd
import openmdao.api as om


class LiftDragCoeffComp(om.ExplicitComponent):

    def initialize(self):
        self.options.declare('num_nodes', types=int)

    def setup(self):
        nn = self.options['num_nodes']

        # Inputs
        self.add_input('mach', shape=(nn,), desc='Mach number', units=None)
        self.add_input('h', shape=(nn,), desc='altitude', units='m')
        self.add_input('alpha', shape=(nn,), desc='angle of attck', units='deg')
        self.add_input('sweep', shape=(nn,), desc='sweep angle', units='deg')
        # Outputs
        self.add_output(name='CL', val=np.ones(nn), desc='lift coefficient', units=None)
        self.add_output(name='CD', val=np.ones(nn), desc='drag coefficient', units=None)

        # Jacobian
        ar = np.arange(nn)
        self.declare_partials(of='CL', wrt='mach', rows=ar, cols=ar)
        self.declare_partials(of='CL', wrt='h', rows=ar, cols=ar)
        self.declare_partials(of='CL', wrt='alpha', rows=ar, cols=ar)
        self.declare_partials(of='CL', wrt='sweep', rows=ar, cols=ar)
        
        self.declare_partials(of='CD', wrt='mach', rows=ar, cols=ar)
        self.declare_partials(of='CD', wrt='h', rows=ar, cols=ar)
        self.declare_partials(of='CD', wrt='alpha', rows=ar, cols=ar)
        self.declare_partials(of='CD', wrt='sweep', rows=ar, cols=ar)

    def compute(self, inputs, outputs):
        M = inputs['mach']
        h = inputs['mach']
        alpha = inputs['alpha']
        sweep = inputs['sweep']


        
        outputs['CL'][:] = 0.0 + 2.368707986087357e-07 *h + 0.09307989052386303 *alpha + -0.06550316497243491 *M + 0.006815647948620546 *sweep + 3.751485727653883e-12 *h**2 + 3.964897211099411e-08 *h*alpha + -4.486524394304196e-07 *h*M + -1.8268679316844648e-09 *h*sweep + 0.0004818148227933809 *alpha**2 + 0.049857451418150504 *alpha*M + -0.0011267238474617985 *alpha*sweep + 0.5655837912088061 *M**2 + -0.011690886643118239 *M*sweep + -6.191185798327924e-05 *sweep**2
        outputs['CD'][:] = 0.0 + 4.3396852174745575e-07 *h + -0.0008958497127749826 *alpha + 0.018095458080017703 *M + 0.002188780579068273 *sweep + 1.0531056190347051e-11 *h**2 + 5.470666550726072e-08 *h*alpha + -7.939332880993814e-07 *h*M + -1.353112608932816e-09 *h*sweep + 0.0014505213528099071 *alpha**2 + 0.01818757185515245 *alpha*M + -0.0002040915718363592 *alpha*sweep + 0.11522636217948708 *M**2 + -0.0033384697148089917 *M*sweep + -1.1882284382287273e-05 *sweep**2
        #else:
            #outputs['CL'][:] = 0.0 + 4.733059849646947e-09 *h + 0.15173584168243653 *alpha + -0.028620243756841787 *M + -0.002708275911261341 *sweep + 1.9176403934032663e-13 *h**2 + 3.15794198925399e-09 *h*alpha + -1.0198762084461114e-08 *h*M + 3.339499249002007e-11 *h*sweep + -0.0001587149169884985 *alpha**2 + -0.062100289595689036 *alpha*M + 2.9947973540362495e-05 *alpha*sweep + -0.08586073127072043 *M**2 + 0.004806266352693484 *M*sweep + -7.561305361307199e-05 *sweep**2    
            #outputs['CD'][:] = 0.0 + -9.108839982588111e-07 *h + 0.0266483192255351 *alpha + 0.0024087498072763946 *M + -0.00137130090550479 *sweep + 7.215325757534976e-12 *h**2 + 1.0789981201502964e-09 *h*alpha + 6.798085197924137e-07 *h*M + 1.8715364138735094e-10 *h*sweep + 0.0010158604756804182 *alpha**2 + -0.014463173651765448 *alpha*M + -2.2420003853002087e-05 *alpha*sweep + 0.0072262494218280765 *M**2 + 0.0017450418628987554 *M*sweep + -2.2297036297039332e-05 *sweep**2
        #
        # All Mach Numbers      
        #outputs['CL'][:] = 0.000000217562723*inputs['h']+0.108637152*inputs['alpha']+0.636039681*inputs['mach']+-0.00111936675*inputs['sweep']+2.32759711E-12*inputs['h']**2+0.00000002505256*inputs['h']*inputs['alpha']+-0.000000238068896*inputs['h']*inputs['mach']+-0.00000000108276286*inputs['h']*inputs['sweep']+0.000225602927*inputs['alpha']**2+-0.015997577*inputs['alpha']*inputs['mach']+-0.000664055119*inputs['alpha']*inputs['sweep']+-0.432231693*inputs['mach']**2+0.0038910433*inputs['mach']*inputs['sweep']+-0.0000673923362*inputs['sweep']**2
        #outputs['CD'][:] = 3.03587176e-07*inputs['h']+6.00387587e-03*inputs['alpha']+1.33028556e-01*inputs['mach']+7.08356698e-04*inputs['sweep']+9.20476401e-12*inputs['h']**2+3.32555985e-08*inputs['h']*inputs['alpha']+-2.64282818e-07*inputs['h']*inputs['mach']+-7.37006120e-10*inputs['h']*inputs['sweep']+1.27665700e-03*inputs['alpha']**2+9.95899285e-04*inputs['alpha']*inputs['mach']+-1.31422945e-04*inputs['alpha']*inputs['sweep']+-5.56068076e-02*inputs['mach']**2+1.13194990e-04*inputs['mach']*inputs['sweep']+-1.60481851e-05*inputs['sweep']**2

    def compute_partials(self, inputs, partials):
        
        M = inputs['mach']
        h = inputs['mach']
        alpha = inputs['alpha']
        sweep = inputs['sweep']

        partials['CL', 'h'][:] = 2.368707986087357e-07 + 3.751485727653883e-12 *h*2 + 3.964897211099411e-08 *alpha + -4.486524394304196e-07 *M + -1.8268679316844648e-09 *sweep
        partials['CL', 'alpha'][:] = 0.09307989052386303 + 3.964897211099411e-08 *h + 0.0004818148227933809 *alpha*2 + 0.049857451418150504 *M + -0.0011267238474617985 *sweep
        partials['CL', 'mach'][:] = -0.06550316497243491 + -4.486524394304196e-07 *h + 0.049857451418150504 *alpha + 0.5655837912088061 *M*2 + -0.011690886643118239 *sweep
        partials['CL', 'sweep'][:] = 0.006815647948620546 + -1.8268679316844648e-09 *h + -0.0011267238474617985 *alpha + -0.011690886643118239 *M + -6.191185798327924e-05 *sweep*2
        partials['CD', 'h'][:] = 4.3396852174745575e-07 + 1.0531056190347051e-11 *h*2 + 5.470666550726072e-08 *alpha + -7.939332880993814e-07 *M + -1.353112608932816e-09 *sweep
        partials['CD', 'alpha'][:] = -0.0008958497127749826 + 5.470666550726072e-08 *h + 0.0014505213528099071 *alpha*2 + 0.01818757185515245 *M + -0.0002040915718363592 *sweep
        partials['CD', 'mach'][:] = 0.018095458080017703 + -7.939332880993814e-07 *h + 0.01818757185515245 *alpha + 0.11522636217948708 *M*2 + -0.0033384697148089917 *sweep  
        partials['CD', 'sweep'][:] = 0.002188780579068273 + -1.353112608932816e-09 *h + -0.0002040915718363592 *alpha + -0.0033384697148089917 *M + -1.1882284382287273e-05 *sweep*2
        #else:
            #partials['CL', 'h'][:] = 4.733059849646947e-09 + 1.9176403934032663e-13 *h*2 + 3.15794198925399e-09 *alpha + -1.0198762084461114e-08 *M + 3.339499249002007e-11 *sweep
            #partials['CL', 'alpha'][:] = 0.15173584168243653 + 3.15794198925399e-09 *h + -0.0001587149169884985 *alpha*2 + -0.062100289595689036 *M + 2.9947973540362495e-05 *sweep
            #partials['CL', 'mach'][:] = -0.028620243756841787 + -1.0198762084461114e-08 *h + -0.062100289595689036 *alpha + -0.08586073127072043 *M*2 + 0.004806266352693484 *sweep 
            #partials['CL', 'sweep'][:] = -0.002708275911261341 + 3.339499249002007e-11 *h + 2.9947973540362495e-05 *alpha + 0.004806266352693484 *M + -7.561305361307199e-05 *sweep*2 
            #partials['CD', 'h'][:] =-9.108839982588111e-07 + 7.215325757534976e-12 *h*2 + 1.0789981201502964e-09 *alpha + 6.798085197924137e-07 *M + 1.8715364138735094e-10 *sweep
            #partials['CD', 'alpha'][:] = 0.0266483192255351 + 1.0789981201502964e-09 *h + 0.0010158604756804182 *alpha*2 + -0.014463173651765448 *M + -2.2420003853002087e-05 *sweep
            #partials['CD', 'mach'][:] = 0.0024087498072763946 + 6.798085197924137e-07 *h + -0.014463173651765448 *alpha + 0.0072262494218280765 *M*2 + 0.0017450418628987554 *sweep
            #partials['CD', 'sweep'][:] = -0.00137130090550479 + 1.8715364138735094e-10 *h + -2.2420003853002087e-05 *alpha + 0.0017450418628987554 *M + -2.2297036297039332e-05 *sweep*2        
        #
        # All Mach Numbers
        #partials['CL', 'mach'] = 0.636039681 + -0.000000238068896*inputs['h'] + -0.015997577*inputs['alpha'] + 2 * -0.432231693*inputs['mach'] + 0.0038910433*inputs['sweep']
        #partials['CL', 'h'] = 0.000000217562723 + 2.32759711E-12*inputs['h'] * 2 + 0.00000002505256*inputs['alpha'] + -0.000000238068896*inputs['mach'] + -0.00000000108276286*inputs['sweep']
        #partials['CL', 'alpha'] = 0.108637152 + 0.00000002505256*inputs['h'] + 0.000225602927*inputs['alpha'] * 2 + -0.015997577*inputs['mach'] + -0.000664055119*inputs['sweep']
        #partials['CL', 'sweep'] = -0.00111936675 + -0.00000000108276286*inputs['h'] + -0.000664055119*inputs['alpha'] + 0.0038910433*inputs['mach'] + -0.0000673923362 * 2 * inputs['sweep']
        #partials['CD', 'mach'] = 1.33028556e-01 + -2.64282818e-07*inputs['h'] + 9.95899285e-04*inputs['alpha'] + -5.56068076e-02*inputs['mach']*2 + 1.13194990e-04*inputs['sweep']
        #partials['CD', 'h'] = 3.03587176e-07 + 9.20476401e-12*inputs['h']*2 + 3.32555985e-08*inputs['alpha'] + -2.64282818e-07*inputs['mach'] + -7.37006120e-10*inputs['sweep']
        #partials['CD', 'alpha'] = 6.00387587e-03 + 3.32555985e-08*inputs['h'] + 1.27665700e-03*inputs['alpha']*2 + 9.95899285e-04*inputs['mach'] + -1.31422945e-04*inputs['sweep']
        #partials['CD', 'sweep'] = 7.08356698e-04 + -7.37006120e-10*inputs['h'] + -1.31422945e-04*inputs['alpha'] + 1.13194990e-04*inputs['mach'] + -1.60481851e-05*inputs['sweep']*2
