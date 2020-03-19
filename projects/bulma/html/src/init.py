#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import pathlib

import signac

# from projects.bulma.src.init import prepend_id, copy_file

logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    # prepend_id()
    # copy_file()

    html_proj = signac.init_project("html", workspace="workspace")

    module_path = pathlib.Path(__file__).absolute().parent
    bulma_root = module_path / ".." / ".." / "bulma"
    bulma_proj = signac.get_project(root=bulma_root)

    logger.info("html project: %s" % html_proj.workspace())
    logger.info("bulma project: %s" % bulma_proj.workspace())


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
