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


nuclei = {
    "50": {
        "76": (two_digits(8.33),),
        "86": (two_digits(6.04), two_digits(8.28)),
        "96": (two_digits(5.11), two_digits(7.54)),
    },
    "58": {"82": (two_digits(8.373686))},
}


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

    for job in project:
        if job.sp.transition_energy == two_digits(0.42):
            sp_dict = job.statepoint()
            for energy in nuclei[str(job.sp.proton_number)][str(job.sp.neutron_number)]:
                statepoint = sp_dict.copy()  # shallow copy!
                statepoint.update(dict(transition_energy=energy))
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
