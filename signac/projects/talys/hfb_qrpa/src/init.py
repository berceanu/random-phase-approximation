#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import signac

from mypackage.talys.api import TalysAPI


logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = TalysAPI()


def main():
    hfb_qrpa_proj = signac.init_project("hfb_qrpa", workspace="workspace")
    logger.info("hfb_qrpa project: %s" % hfb_qrpa_proj.workspace())

    rpa_proj = signac.get_project(root="../../rpa/")
    logger.info("rpa project: %s" % rpa_proj.workspace())

    for rpa_job in rpa_proj.find_jobs(dict(proton_number=50, temperature=0.0)):
        logger.info(f"Processing %s.." % rpa_job.workspace())
        sp = rpa_proj.get_statepoint(rpa_job.get_id())
        del sp["temperature"]
        del sp["transition_energy"]

        for yn in "y", "n":
            sp.update(
                dict(
                    # flag for calculation of astrophysics reaction rate
                    astro=yn
                )
            )
            talys_job = hfb_qrpa_proj.open_job(sp).init()

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
