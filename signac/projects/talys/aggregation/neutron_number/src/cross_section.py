#!/usr/bin/env python3
import logging

import signac

logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    proj = signac.init_project("proj")
    logger.info("current project: %s" % proj.workspace())

    talys_proj = signac.get_project(root="../../")
    logger.info("talys project: %s" % talys_proj.workspace())

    hfb_qrpa_proj = signac.get_project(root="../../hfb_qrpa/")
    logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())

    for neutron_number, jobs in talys_proj.find_jobs(
        {"proton_number": 50, "astro": "n"}
    ).groupby("neutron_number"):
        print("\n", neutron_number, "\n")
        for job in jobs:
            print(job.sp.neutron_number + job.sp.proton_number, job.sp.temperature)


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
