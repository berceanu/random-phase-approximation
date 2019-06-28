#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np
import mypackage.code_api as code_api
import mypackage.util as util

def main():
    project = signac.init_project('rpa', workspace='debug_workspace')

    statepoint = dict(
        # atomic number Z
        proton_number=50, # fixed atomic number

        # neutron number N
        neutron_number=90,

        # nucleus angular momentum
        angular_momentum=1, #

        # nucleus parity
        parity="-", #

        # system temperature in MeV
        temperature=0.0,

        # transition energy in MeV
        transition_energy=0.42 # 0.42 is random
        )
    project.open_job(statepoint).init()


    for job in project:
        nprot = job.sp.proton_number
        nneutr = job.sp.neutron_number
        nucleus = util.get_nucleus(proton_number=nprot, neutron_number=nneutr)
        job.doc.setdefault('nucleus', nucleus)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
