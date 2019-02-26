#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np
from modules import code_api

# nucleus=get_nucleus(proton_number=50, neutron_number=82)

def main():
    project = signac.init_project('rpa')
    for T in 0.0,:
        for tr_en in 7.75,:
            statepoint = dict(
                # nucleus="SN132",

                # atomic number Z
                proton_number=50

                # neutron number N
                neutron_number=82

                # nucleus angular momentum
                angular_momentum=1, #

                # nucleus parity
                parity="-", #

                # system temperature in MeV
                temperature=T,

                # transition energy in MeV
                transition_energy=tr_en
                )
            project.open_job(statepoint).init()
    
    project.write_statepoints()
    for job in project:
        job.doc.setdefault('run_zero_temp_ground_state', True)
        job.doc.setdefault('run_finite_temp_ground_state', True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
