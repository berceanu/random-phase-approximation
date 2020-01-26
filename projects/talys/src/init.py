#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac
import mypackage.util as util
from mypackage.talys.api import TalysAPI

logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = TalysAPI()


def main():
    talys_proj = signac.init_project("talys", workspace="workspace")
    logger.info("talys project: %s" % talys_proj.workspace())

    rpa_proj = signac.get_project(root="../rpa/")
    logger.info("rpa project: %s" % rpa_proj.workspace())

    for psf, jobs in rpa_proj.find_jobs({"proton_number": 50}).groupbydoc(
        "photon_strength_function"
    ):
        for rpa_job in jobs:
            logger.info(f"Processing %s.." % rpa_job.workspace())
            sp = rpa_proj.open_job(id=rpa_job.id).statepoint()

            for yn in "y", "n":
                sp.update(
                    dict(
                        # flag for calculation of astrophysics reaction rate
                        astro=yn
                    )
                )
                talys_job = talys_proj.open_job(sp).init()

                util.copy_file(source=rpa_job.fn(psf), destination=talys_job.fn(psf))
                talys_job.doc.setdefault("photon_strength_function", psf)

                talys_api.energy_file(talys_job)
                talys_api.input_file(talys_job)


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
