#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac  ##
import mypackage.util as util


def main():
    project = signac.init_project("rpa", workspace="workspace")

    for N in range(76, 96 + 2, 2):
        for T in (0.0, 0.5, 1.0, 2.0):
            statepoint = dict(
                # atomic number Z
                proton_number=50,  # fixed atomic number
                # neutron number N
                neutron_number=N,
                # nucleus angular momentum
                angular_momentum=1,  #
                # nucleus parity
                parity="-",  #
                # system temperature in MeV
                temperature=T,
                # transition energy in MeV
                transition_energy=0.42,  # 0.42 is random
            )
            project.open_job(statepoint).init()

    for Z in range(44, 48 + 2, 2):
        for T in (0.0, 0.5, 1.0, 2.0):
            statepoint = dict(
                # atomic number Z
                proton_number=Z,
                # neutron number N
                neutron_number=82,  # fixed
                # nucleus angular momentum
                angular_momentum=1,  #
                # nucleus parity
                parity="-",  #
                # system temperature in MeV
                temperature=T,
                # transition energy in MeV
                transition_energy=0.42,  # 0.42 is random
            )
            project.open_job(statepoint).init()

    for job in project:
        nprot = job.sp.proton_number
        nneutr = job.sp.neutron_number
        nucleus = util.get_nucleus(proton_number=nprot, neutron_number=nneutr)
        job.doc.setdefault("nucleus", nucleus)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
