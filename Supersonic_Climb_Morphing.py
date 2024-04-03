# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 11:44:20 2022

@author: paubo
"""

import matplotlib.pyplot as plt

import openmdao.api as om

import dymos as dm
from dymos.examples.plotting import plot_results
from dymos.models.eom import FlightPathEOM2D
from min_time_climb.prop import PropGroup
from dymos.models.atmosphere import USatm1976Comp
from min_time_climb.doc.aero_partial_coloring import AeroGroup



class MinTimeClimbODE(om.Group):

    def initialize(self):
        self.options.declare('num_nodes', types=int)
        self.options.declare('fd', types=bool, default=False, desc='If True, use fd for partials')
        self.options.declare('partial_coloring', types=bool, default=False,
                             desc='If True and fd is True, color the approximated partials')

    def setup(self):
        nn = self.options['num_nodes']

        self.add_subsystem(name='atmos',
                           subsys=USatm1976Comp(num_nodes=nn, h_def='geodetic'),
                           promotes_inputs=['h'])

        self.add_subsystem(name='aero',
                           subsys=AeroGroup(num_nodes=nn,
                                            fd=self.options['fd'],
                                            partial_coloring=self.options['partial_coloring']),
                           promotes_inputs=['v', 'alpha', 'S', 'h', 'sweep','tipchord','twist'])

        self.connect('atmos.sos', 'aero.sos')
        self.connect('atmos.rho', 'aero.rho')

        self.add_subsystem(name='prop',
                           subsys=PropGroup(num_nodes=nn),
                           promotes_inputs=['h', 'Isp', 'throttle'])

        self.connect('aero.mach', 'prop.mach')

        self.add_subsystem(name='flight_dynamics',
                           subsys=FlightPathEOM2D(num_nodes=nn),
                           promotes_inputs=['m', 'v', 'gam', 'alpha'])

        self.connect('aero.f_drag', 'flight_dynamics.D')
        self.connect('aero.f_lift', 'flight_dynamics.L')
        self.connect('prop.thrust', 'flight_dynamics.T')

def runExperiment(debug,objective,flightphase,sweep,twist,tipchord,h):
  #
  # Instantiate the problem and configure the optimization driver
  #

  p = om.Problem(model=om.Group())
    

  p.driver = om.ScipyOptimizeDriver()
  p.driver.options['optimizer'] = 'SLSQP'
  p.driver.declare_coloring()
  p.driver.options['maxiter'] = 1200

  p.driver.add_recorder(om.SqliteRecorder('morphing_solution.sql'))
  p.driver.recording_options['record_desvars'] = True
  p.driver.recording_options['record_responses'] = True
  p.driver.recording_options['record_objectives'] = True
  p.driver.recording_options['record_constraints'] = True
  p.driver.recording_options['includes'] = ['*timeseries*']

  #
  # Instantiate the trajectory and phase
  #
  traj = dm.Trajectory()

  phase = dm.Phase(ode_class=MinTimeClimbODE, 
                transcription=dm.GaussLobatto(num_segments=17, compressed=False))

  traj.add_phase('phase0', phase)

  p.model.add_subsystem('traj', traj)


  #
  # Set the options on the optimization variables
  # Note the use of explicit state units here since much of the ODE uses imperial units
  # and we prefer to solve this problem using metric units.
  #
  phase.set_time_options(fix_initial=True, duration_bounds=(50, 400),
                        duration_ref=100.0)

  phase.add_state('r', fix_initial=True, lower=0, upper=1.0E6, units='m',
                  ref=1.0E3, defect_ref=1.0E3,
                  rate_source='flight_dynamics.r_dot')

  phase.add_state('h', fix_initial=True, lower=0, upper=20000.0, units='m',
                  ref=1.0E2, defect_ref=1.0E2,
                  rate_source='flight_dynamics.h_dot')

  phase.add_state('v', fix_initial=True, lower=10.0, units='m/s',
                  ref=1.0E2, defect_ref=1.0E2,
                  rate_source='flight_dynamics.v_dot')

  phase.add_state('gam', fix_initial=True, lower=-1.5, upper=1.5, units='rad',
                  ref=1.0, defect_ref=1.0,
                  rate_source='flight_dynamics.gam_dot')

  phase.add_state('m', fix_initial=True, lower=10.0, upper=2.0E5, units='kg',
                  ref=1.0E3, defect_ref=1.0E3,
                  rate_source='prop.m_dot')


  phase.add_control('alpha', units='deg', lower=-6.0, upper=16.0, scaler=1.0,
                    rate_continuity=True, rate_continuity_scaler=100.0,
                    rate2_continuity=False)

  phase.add_control('twist', units='deg', lower=twist[0], upper=twist[1], scaler=10.0,
                rate_continuity=True, rate_continuity_scaler=100.0,
                rate2_continuity=False)
  
  phase.add_control('tipchord', units='m', lower=tipchord[0], upper=tipchord[1], scaler=2.0,
                    rate_continuity=True, rate_continuity_scaler=100.0,
                    rate2_continuity=False) 

  phase.add_control('sweep', units='deg', lower=sweep[0], upper=sweep[1], scaler=1.0,
                  rate_continuity=True, rate_continuity_scaler=100.0,
                  rate2_continuity=False)

  phase.add_parameter('S', val=296.27, units='m**2', opt=False, targets=['S'])
  phase.add_parameter('Isp', val=3000.0, units='s', opt=False, targets=['Isp'])
  phase.add_parameter('throttle', val=1.0, opt=False, targets=['throttle'])

  #
  # Setup the boundary and path constraints
  #
  phase.add_boundary_constraint('h', loc='final', equals=20000, scaler=1.0E-3)
  phase.add_boundary_constraint('aero.mach', loc='final', equals=1.3)
  phase.add_boundary_constraint('gam', loc='final', equals=0.0)

  phase.add_path_constraint(name='h', lower=100.0, upper=20000, ref=20000)
  phase.add_path_constraint(name='aero.mach', lower=0.1, upper=1.9)

  # Phase string 
  if flightphase == 0:
    phase_text = 'Climb'
  elif flightphase == 1:
    phase_text = 'Descend'
  elif flightphase == 2:
    phase_text = 'Cruise'
  else: 
    raise Exception("Wrong phase was selected.")


  # Minimize time at the end of the phase
  if objective == 0:
    phase.add_objective('time', loc='final', ref=1.0)
    plot_title = 'Supersonic Minimum Airtime ' + phase_text + ' Solution'
  elif objective == 1:
    phase.add_objective('m', loc='final', scaler=-1)
    plot_title = 'Supersonic Minimum Fuel ' + phase_text + ' Solution'
  else:
     raise Exception("Wrong objective function was selected.")

  # Debugging
  if debug == True:
    phase.add_timeseries_output('aero.CL', units=None, shape=(1,))
    phase.add_timeseries_output('aero.CD', units=None, shape=(1,))
    phase.add_timeseries_output('aero.f_lift', units=None, shape=(1,))
    phase.add_timeseries_output('aero.f_drag', units=None, shape=(1,))
    phase.add_timeseries_output('prop.thrust', units=None, shape=(1,))
    phase.add_timeseries_output('aero.q', units=None, shape=(1,))

  # Run OpenMDAO Solver
  p.model.linear_solver = om.DirectSolver()

  #
  # Setup the problem and set the initial guess
  #
  p.setup(check=True)

  p['traj.phase0.t_initial'] = 0.0
  p['traj.phase0.t_duration'] = 400

  p.set_val('traj.phase0.states:r', phase.interp('r', [0.0, 50000.0]))
  p.set_val('traj.phase0.states:h', phase.interp('h', h))
  p.set_val('traj.phase0.states:v', phase.interp('v', [135.964, 483.159]))
  p.set_val('traj.phase0.states:gam', phase.interp('gam', [0.0, 0.0]))
  p.set_val('traj.phase0.states:m', phase.interp('m', [170000, 10000.]))
  p.set_val('traj.phase0.controls:alpha', phase.interp('alpha', [-6.0, 16.0]))
  p.set_val('traj.phase0.controls:twist', phase.interp('twist', twist))
  p.set_val('traj.phase0.controls:tipchord', phase.interp('tipchord', tipchord))
  p.set_val('traj.phase0.controls:sweep', phase.interp('sweep', sweep))

  #
  # Solve for the optimal trajectory
  #
  dm.run_problem(p, simulate=True)


  sol = om.CaseReader('dymos_solution.db').get_case('final')
  sim = om.CaseReader('dymos_simulation.db').get_case('final')


  if debug == True:
    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.q',
                          'time (s)', 'Dynamic Pressure')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)
    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.CL',
                          'time (s)', 'lift coefficient')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)

    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.CD',
                          'time (s)', 'drag coefficient')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)


    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.f_lift',
                          'time (s)', 'lift')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)


    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.f_drag',
                          'time (s)', 'drag')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)

    plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.thrust',
                          'time (s)', 'thrust')],
                        title='Debugging',
                        p_sol=p, p_sim=sim)



  plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.h',
                'time (s)', 'altitude (m)'),('traj.phase0.timeseries.time', 'traj.phase0.timeseries.v',
                                'time (s)', 'speed (m/s)'), ('traj.phase0.timeseries.time', 'traj.phase0.timeseries.mach',
                                'time (s)', 'Mach (-)'),('traj.phase0.timeseries.time', 'traj.phase0.timeseries.m',
                  'time (s)', 'mass (kg)'),('traj.phase0.timeseries.time', 'traj.phase0.timeseries.alpha',
                  'time (s)', 'alpha (deg)'),
                ('traj.phase0.timeseries.time', 'traj.phase0.timeseries.sweep',
                'time (s)', 'sweep (deg)'),('traj.phase0.timeseries.time', 'traj.phase0.timeseries.twist',
                  'time (s)', 'twist (deg)'),('traj.phase0.timeseries.time', 'traj.phase0.timeseries.tipchord',
                  'time (s)', 'Tip Chord (m)')],
              title=plot_title,
              p_sol=sol, p_sim=sim)
  plt.show()

# Setting up flags
debug = False
objective = 0 # 0 == Airtime ; 1 == Fuel Usage
variable_geometry = False
flightphase = 0 # 0 == Climb ; 1 == Descend ; 2 == Cruise

if flightphase == 0:
  h = [100.0, 20000.0]
elif flightphase == 1:
  h = [20000.0, 1500.0]
elif flightphase == 2:
  h = [20000.0, 20000.0]

if variable_geometry == True:
  twist = [-5.0, 5.0]
  tipchord = [5.0, 15.0]
  sweep = [1.0, 65.0]
else:
  twist = [-4, -4]
  tipchord = [6.0,6.0]
  sweep = [30.0, 30.0]
runExperiment(debug,objective,flightphase,sweep,twist,tipchord,h)
