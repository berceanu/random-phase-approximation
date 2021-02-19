"""Run after init.py."""
import logging

import signac
import mypackage.util as util
from decimal import Decimal
import pandas as pd


def two_digits(x):
    return str(round(Decimal(x), 2))


def top_transition_energies(fname):
    df = pd.read_csv(fname, usecols=["energy", "transition_strength"])
    for row in df.itertuples(name="Row", index=False):
        yield row.energy, row.transition_strength


def main():
    """Main entry point."""

    project = signac.get_project(search=False)

    for job in project:
        if (
            (job.sp.transition_energy == two_digits(0.42))
            and (job.isfile("transerg.dat"))
            and (job.sp.proton_number == 58)
        ):
            print(util.get_nucleus(58, job.sp.neutron_number))
            for energy, strength in top_transition_energies(job.fn("transerg.dat")):
                print(energy, strength)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
