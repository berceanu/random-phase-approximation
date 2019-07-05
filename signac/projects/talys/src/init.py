#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import pathlib

import signac
import mypackage.util as util
from mypackage.talys_api import energy_file, input_file, database_file_path


logger = logging.getLogger(__name__)
logfname = "project.log"


def main():
    talys_proj = signac.init_project("talys", workspace="workspace")
    logger.info("talys project: %s" % talys_proj.workspace())

    rpa_proj = signac.get_project(root="../rpa/")
    logger.info("rpa project: %s" % rpa_proj.workspace())

    for z_fn, jobs in rpa_proj.find_jobs({"proton_number": 50}).groupbydoc("z_file"):
        for rpa_job in jobs:
            logger.info(f"Processing %s.." % rpa_job.workspace())
            sp = rpa_proj.get_statepoint(rpa_job.get_id())

            for yn in "y", "n":
                sp.update(
                    dict(
                        # flag for calculation of astrophysics reaction rate
                        astro=yn
                    )
                )
                talys_job = talys_proj.open_job(sp).init()

                util.copy_file(source=rpa_job.fn(z_fn), destination=talys_job.fn(z_fn))
                talys_job.doc.setdefault("z_file", z_fn)

                energy_file(talys_job)
                input_file(talys_job)

                talys_job.doc.setdefault(
                    "database_file", database_file_path(talys_job).as_posix()
                )

                db_fpath = pathlib.Path(talys_job.doc["database_file"])
                database_file_backup = db_fpath.parent / (
                    db_fpath.stem + f"_{talys_job.get_id()}.bck"
                )
                talys_job.doc.setdefault(
                    "database_file_backup", database_file_backup.as_posix()
                )
                # todo refactor into mypackage.talys_api


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
