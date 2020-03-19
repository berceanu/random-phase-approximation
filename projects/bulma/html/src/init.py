#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import pathlib

import signac
from mypackage import util

logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    html_proj = signac.init_project("html", workspace="workspace")

    module_path = pathlib.Path(__file__).absolute().parent
    bulma_root = module_path / ".." / ".." / "bulma"
    bulma_proj = signac.get_project(root=bulma_root)

    logger.info("html project: %s" % html_proj.workspace())
    logger.info("bulma project: %s" % bulma_proj.workspace())

    statepoint = dict(
        # atomic number Z
        proton_number=50,  # fixed atomic number
        # nucleus angular momentum
        angular_momentum=1,  #
        # nucleus parity
        parity="-",  #
    )
    for nn, bulma_jobs in bulma_proj.find_jobs(statepoint).groupby("neutron_number"):
        sp = statepoint.copy()
        sp.update(dict(neutron_number=nn))
        html_job = html_proj.open_job(sp).init()

        bulma_jobs_json = dict()
        for bulma_job in bulma_jobs:
            logger.info("Processing %s.." % bulma_job.workspace())
            bulma_jobs_json[bulma_job.id] = dict(temperature=bulma_job.sp.temperature,)
            for fname in ("inset.png", "dipole_transitions.h5"):
                util.copy_file_with_id(fname, bulma_job, html_job)

        html_job.doc.setdefault("bulma_jobs", bulma_jobs_json)


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
