#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac

# pass folder containing the template

logger = logging.getLogger(__name__)
logfname = "project.log"


# {
#  'proton_number': 'int([50], 1)',
#  'neutron_number': 'int([76, 78, 80, ..., 94, 96], 11)',

#  'temperature': 'float([0.0, 0.5, 1.0, 2.0], 4)',

# *'astro': 'str([n, y], 2)',
# }


def main():
    talys_aggregation_proj = signac.init_project("talys-aggregation")
    logger.info("talys-aggregation project: %s" % talys_aggregation_proj.workspace())

    talys_proj = signac.get_project(root="../")
    logger.info("talys project: %s" % talys_proj.workspace())

    hfb_qrpa_proj = signac.get_project(root="../hfb_qrpa/")
    logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())

    # astro="n"
    # cross section: (temperature, mass number, energy)

    # cross section vs energy @ fixed (aggregated) temperature
    # cross section vs energy @ fixed (aggregated) mass number
    # Note: add HFB+QRPA result as well from hfb_qrpa_proj

    # astro="y"
    # neutron capture rate: (mass number, temperature)

    # neutron capture rate vs mass number @ fixed (aggregated) temperature
    # neutron capture rate vs temperature @ fixed (aggregated) mass number
    # Note: the HFB+QRPA result now depends on temperature

    for z_fn, jobs in talys_proj.find_jobs({"proton_number": 50}).groupbydoc("z_file"):
        for rpa_job in jobs:
            logger.info(f"Processing %s.." % rpa_job.workspace())
            sp = talys_proj.get_statepoint(rpa_job.get_id())

            for yn in "y", "n":
                sp.update(
                    dict(
                        # flag for calculation of astrophysics reaction rate
                        astro=yn
                    )
                )
                # talys_job = talys_aggregation_proj.open_job(sp).init()


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
