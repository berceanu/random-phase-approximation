#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np
from modules import code_api


def main():
    project = signac.init_project('rpa')
    for N in range(76, 96 + 2, 2):
        for T in (0.0, 1.0, 2.0):
            statepoint = dict(
                # atomic number Z
                proton_number=50, # fixed atomic number

                # neutron number N
                neutron_number=N,

                # nucleus angular momentum
                angular_momentum=1, #

                # nucleus parity
                parity="-", #

                # system temperature in MeV
                temperature=T,

                # transition energy in MeV
                transition_energy=0.42 # 0.42 is random
                )
            project.open_job(statepoint).init()

    for job in project:
        nprot = job.sp.proton_number
        nneutr = job.sp.neutron_number
        nucleus = code_api.get_nucleus(proton_number=nprot, neutron_number=nneutr)
        job.doc.setdefault('nucleus', nucleus)



    # project.write_statepoints()
    # for job in project:
    #     job.doc.setdefault('run_zero_temp_ground_state', True)
    #     job.doc.setdefault('run_finite_temp_ground_state', True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
