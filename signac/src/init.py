#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np


def main():
    project = signac.init_project('rpa')
    for tr_en in np.linspace(480/50, 490/50, 11):
        statepoint = dict(
                # nucleus of interest
                nucleus="NI62",

                # nucleus angular momentum
                angular_momentum=1,

                # nucleus parity
                parity="-",

                # system temperature in MeV
                temperature=2.0,

                # transition energy in MeV
                transition_energy=tr_en,

                # do full calculation
                load_matrix=False
                )
        project.open_job(statepoint).init()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
