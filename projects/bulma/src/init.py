#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""

import logging
import pathlib
import shutil

import signac

logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    bulma_proj = signac.init_project("bulma", workspace="workspace")

    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".." / ".." / "rpa"
    rpa_proj = signac.get_project(root=rpa_root)

    logger.info("bulma project: %s" % bulma_proj.workspace())
    logger.info("rpa project: %s" % rpa_proj.workspace())

    for rpa_job in rpa_proj:
        if rpa_job.sp.transition_energy != 0.42:
            fname = "inset.png"
            local_fname = f"{rpa_job.id}_{fname}"
            shutil.copy(rpa_job.fn(fname), local_fname)
            print(
                f"{local_fname}: {rpa_job.sp.temperature}, {rpa_job.sp.transition_energy}"
            )


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
