#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""

import logging
import pathlib
import shutil

import signac
from mypackage import util, code_api

logger = logging.getLogger(__name__)
logfname = "project.log"

CODE = code_api.NameMapping()


def main():
    bulma_proj = signac.init_project("bulma", workspace="workspace")

    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".." / ".." / "rpa"
    rpa_proj = signac.get_project(root=rpa_root)

    logger.info("bulma project: %s" % bulma_proj.workspace())
    logger.info("rpa project: %s" % rpa_proj.workspace())

    statepoint = dict(
        # atomic number Z
        proton_number=50,  # fixed atomic number
        # nucleus angular momentum
        angular_momentum=1,  #
        # nucleus parity
        parity="-",  #
    )

    for nn_temp, rpa_jobs in rpa_proj.find_jobs(statepoint).groupby(
        ("neutron_number", "temperature")
    ):
        sp = statepoint.copy()
        sp.update(dict(neutron_number=nn_temp[0], temperature=nn_temp[1]))
        bulma_job = bulma_proj.open_job(sp).init()

        rpa_jobs_json = dict()
        temp = "finite" if bulma_job.sp.temperature > 0 else "zero"

        for rpa_job in rpa_jobs:
            logger.info("Processing %s.." % rpa_job.workspace())
            if rpa_job.sp.transition_energy == 0.42:
                bulma_job.doc.setdefault("restarted_from", rpa_job.id)
                for lorexc in ("lorentzian", "excitation"):
                    shutil.copy(
                        rpa_job.fn(CODE.out_file(temp, "isovector", lorexc)),
                        bulma_job.fn(f"{lorexc}.out"),
                    )
            else:
                rpa_jobs_json[rpa_job.id] = dict(
                    transition_energy=rpa_job.sp.transition_energy,
                    transition_strength=rpa_job.doc.transition_strength,
                )
                util.copy_file_with_id("dipole_transitions.txt", rpa_job, bulma_job)

        bulma_job.doc.setdefault("rpa_jobs", rpa_jobs_json)


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfname,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==INIT STARTED==")
    main()
    logger.info("==INIT FINISHED==")
