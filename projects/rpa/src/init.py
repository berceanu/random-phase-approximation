#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac
import mypackage.util as util


def main():
    project = signac.init_project("rpa", workspace="workspace")

    for N in range(76, 96 + 2, 2):
        for T in (0.0,):
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

    for job in project:
        job.doc.setdefault(
            "nucleus",
            util.get_nucleus(
                proton_number=job.sp.proton_number, neutron_number=job.sp.neutron_number
            ),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
