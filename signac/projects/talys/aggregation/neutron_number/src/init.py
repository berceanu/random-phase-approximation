#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging

import signac

logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    talys_aggregation_proj = signac.init_project("talys-aggregation")
    logger.info("talys-aggregation project: %s" % talys_aggregation_proj.workspace())

    talys_proj = signac.get_project(root="../")
    logger.info("talys project: %s" % talys_proj.workspace())

    hfb_qrpa_proj = signac.get_project(root="../hfb_qrpa/")
    logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())


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
