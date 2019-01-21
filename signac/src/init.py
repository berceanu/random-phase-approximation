#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac ##
import numpy as np


def main():
    project = signac.init_project('rpa')
    for p in np.linspace(0.5, 5.0, 10):
        statepoint = dict(
                # system size
                N=512,

                # Lennard-Jones potential parameters
                sigma=1.0,
                epsilon=1.0,
                r_cut=2.5,

                # thermal energy
                kT=1.0,
                # presure
                p=p,
                # thermostat coupling constant
                tau=1.0,
                # barostat coupling constant
                tauP=1.0)
        project.open_job(statepoint).init()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
