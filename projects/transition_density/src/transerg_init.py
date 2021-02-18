"""Run after init.py."""
import logging

import signac
import mypackage.util as util


nuclei = {"76": (8.33,), "86": (6.04, 7.97), "96": (5.11, 7.54)}


def main():
    """Main entry point."""
    project = signac.get_project(search=False)

    for job in project:
        if job.sp.transition_energy == 0.42:
            sp_dict = job.statepoint()
            for energy in nuclei[str(job.sp.neutron_number)]:
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
