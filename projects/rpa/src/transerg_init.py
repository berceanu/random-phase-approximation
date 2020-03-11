#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import pandas as pd
import signac
import mypackage.util as util


def top_transition_energies(fname):
    series = pd.read_csv(fname, usecols=["energy"], squeeze=True,)
    for energy in series:
        yield energy


def main():
    project = signac.get_project(search=False)
    print(project)

    for job in project:
        if (job.sp.transition_energy == 0.42) and (job.isfile("transerg.dat")):
            sp_dict = job.statepoint()
            for energy in top_transition_energies(job.fn("transerg.dat")):  # n values
                statepoint = sp_dict.copy()  # shallow copy!
                statepoint.update({"transition_energy": energy})
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
