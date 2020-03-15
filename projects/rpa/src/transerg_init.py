#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import pandas as pd
import signac
import mypackage.util as util


def top_transition_energies(fname):
    df = pd.read_csv(fname, usecols=["energy", "transition_strength"])
    for row in df.itertuples(name="Row", index=False):
        yield row.energy, row.transition_strength


def main():
    project = signac.get_project(search=False)

    for job in project:
        if (job.sp.transition_energy == 0.42) and (job.isfile("transerg.dat")):
            sp_dict = job.statepoint()
            for energy, strength in top_transition_energies(
                job.fn("transerg.dat")
            ):  # n values
                statepoint = sp_dict.copy()  # shallow copy!
                statepoint.update(
                    {"transition_energy": energy, "transition_strength": strength}
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
