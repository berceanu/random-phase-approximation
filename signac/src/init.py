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
    #for T in (0.0, 1.0, 2.0):
    for tr_en in (9.78, 10.03):
        statepoint = dict(
                # nucleus of interest
                nucleus="NI62", #

                # nucleus angular momentum
                angular_momentum=1, #

                # nucleus parity
                parity="-", #

                # system temperature in MeV
                temperature=2.0,

                # transition energy in MeV
                transition_energy=tr_en
                )
        project.open_job(statepoint).init()
    
    # project.write_statepoints()
    # for job in project:
    #     job.doc.setdefault('run_zero_temp_ground_state', True)
    #     job.doc.setdefault('run_finite_temp_ground_state', True)

# TODO reproduce Fig. 1 Sn132

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
