"""Run after init.py."""
import logging

import signac
import mypackage.util as util
from decimal import Decimal


def two_digits(x):
    return round(Decimal(x), 2)


nuclei = {
    "50": {
        "76": (two_digits(8.33),),
        "86": (two_digits(6.04), two_digits(8.28)),
        "96": (two_digits(5.11), two_digits(7.54)),
    },
    "58": {"82": (two_digits(8.40), two_digits(15.10))},
}


def main():
    """Main entry point."""
    project = signac.get_project(search=False)

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
