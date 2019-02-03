#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np


def main():
    project = signac.init_project('rpa')
    # for energy in np.linspace(480/50, 490/50, 11): #9.81 #9.78
    for T in (0.0, 1.0, 2.0):
        statepoint = dict(
                # nucleus of interest
                nucleus="NI62", #

                # nucleus angular momentum
                angular_momentum=1, #

                # nucleus parity
                parity="-", #

                # system temperature in MeV
                temperature=T,

                # transition energy in MeV
                transition_energy=9.78
                )
        project.open_job(statepoint).init()
    
    # project.write_statepoints()
    # for job in project:
    #     job.doc.setdefault('run_zero_temp_ground_state', True)
    #     job.doc.setdefault('run_finite_temp_ground_state', True)

# TODO reproduce
# - Fig. 2:  (Ni-62 1-) , T=0.0 MeV, T=1.0 MeV, T=2.0 MeV; isovector dipole response
# - Table 2: (Ni-62 1-) ,                       T=2.0 MeV; FTRRPA transition amplitudes for dipole state at E=9.78, E=10.03

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
