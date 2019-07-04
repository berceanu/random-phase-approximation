#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import os
import pathlib

import mypackage.util as util
import numpy as np
import signac
from jinja2 import Environment, FileSystemLoader
from mypackage.talys_api import TalysAPI

# pass folder containing the template
file_loader = FileSystemLoader("src/templates")
env = Environment(loader=file_loader)

logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = TalysAPI()


def energy_values(log=False, digits=None):
    """Generate TALYS energy input file contents."""
    import math

    if log:
        if digits is None:
            digits = 3

        v1 = np.linspace(0.001, 0.01, 10)
        v2 = np.linspace(0.015, 0.03, 4)
        v3 = np.linspace(0.04, 0.2, 17)
        v4 = np.linspace(0.22, 0.3, 5)
        v5 = np.linspace(0.35, 0.4, 2)
        v6 = np.linspace(0.5, 30.0, 296)

        my_v = np.empty(
            v1.size + v2.size + v3.size + v4.size + v5.size + v6.size, dtype=np.float64
        )
        np.concatenate((v1, v2, v3, v4, v5, v6), out=my_v)
    else:
        if digits is None:
            digits = 1

        my_v, step = np.linspace(0.1, 30.0, 300, retstep=True)
        assert math.isclose(step, 0.1), f"step {step} is not 0.1!"

    return my_v.round(digits)


def energy_file(job):
    """Generate TALYS energy input file."""
    file_path = pathlib.Path(job.fn(talys_api.energy_fn))
    np.savetxt(file_path, job.sp.projectile_energy, fmt="%.3f", newline=os.linesep)
    logger.info("Wrote %s" % file_path)


def input_file(job):
    """Generate TALYS input file."""
    element, mass = util.split_element_mass(job)
    # we hit the element with N - 1 with 1 neutron
    input_contents = env.get_template(talys_api.input_template_fn).render(
        element=element,
        mass=mass - 1,
        energy_fname=talys_api.energy_fn,
        astro=job.sp.astro,
    )
    util.write_contents_to(job.fn(talys_api.input_fn), input_contents)


def database_file_path(job):
    """Return path to job's nucleus data file in TALYS database."""
    element, _ = util.split_element_mass(job)
    database_file = talys_api.hfb_path / f"{element}.psf"

    assert database_file.is_file(), f"{database_file} not found!"
    return database_file


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
                        astro=yn,
                        # incoming neutron energy
                        projectile_energy=energy_values(log=True),
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
