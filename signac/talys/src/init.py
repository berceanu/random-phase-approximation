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
from mypackage.talys_api import ConfigurationSyntaxError, TalysAPI


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
        digits = 1

        my_v, step = np.linspace(0.1, 30.0, 300, retstep=True)
        assert math.isclose(step, 0.1), f"step {step} is not 0.1!"
        
    return my_v.round(digits)


def input_file(job):
    """Generate TALYS input file."""
    element, mass = util.split_element_mass(job)
    # we hit the element with N - 1 with 1 neutron
    input_contents = env.get_template(talys_api.input_template_fn).render(
        element=element, mass=mass - 1, energy_fname=talys_api.energy_fn, astro=job.sp.astro
    )
    util.write_contents_to(job.fn(talys_api.input_fn), input_contents)


def energy_file(job):
    """Generate TALYS energy input file."""
    file_path = pathlib.Path(job.fn(talys_api.energy_fn))
    np.savetxt(file_path, job.sp.projectile_energy, fmt="%.3f", newline=os.linesep)
    logger.info("Wrote %s" % file_path)


def database_file_path(job):
    """Return path to job's nucleus data file in TALYS database."""
    element, _ = util.split_element_mass(job)
    database_file = talys_api.hfb_path / f"{element}.psf"

    assert database_file.is_file(), f"{database_file} not found!"
    return database_file


def main():
    talys_proj = signac.init_project("talys", workspace="workspace")

    # todo run on full 56-job workspace/

    statepoint = dict(
        # atomic number Z
        proton_number=50,
        # neutron number N
        neutron_number=96,
        # nucleus angular momentum
        angular_momentum=1,
        # nucleus parity
        parity="-",
        # system temperature in MeV
        temperature=2.0,
        # transition energy in MeV
        transition_energy=0.42,  # 0.42 is random
        # flag for calculation of astrophysics reaction rate
        astro="n",  # / "y" todo run with "y" as well
        # incoming neutron energy
        projectile_energy=energy_values(log=True),
    )
    extra_keys = ("astro", "projectile_energy")

    talys_proj.open_job(statepoint).init()
    rpa_proj = signac.get_project(root="../")
    logger.info("rpa project: %s" % rpa_proj.workspace())
    logger.info("talys project: %s" % talys_proj.workspace())

    for talys_job in talys_proj:
        energy_file(talys_job)
        input_file(talys_job)

        talys_job.doc.setdefault(
            "database_file", database_file_path(talys_job).as_posix()
        )

        p = pathlib.Path(talys_job.doc["database_file"])
        database_file_backup = p.parent / (p.stem + f"_{talys_job}.bck")
        talys_job.doc.setdefault(
            "database_file_backup", database_file_backup.as_posix()
        )

        rpa_job = rpa_proj.open_job(
            statepoint=util.remove_from_dict(dict(talys_job.sp), extra_keys)
        )

        if rpa_job in rpa_proj:
            logger.info(f"Processing %s.." % rpa_job.workspace())
            z_fn = rpa_job.doc["z_file"]
            util.copy_file(source=rpa_job.fn(z_fn), destination=talys_job.fn(z_fn))
            talys_job.doc.setdefault("z_file", z_fn)
        else:
            msg = f"{rpa_job} not found in {rpa_proj.root_directory()}"
            logger.error(msg)
            raise ConfigurationSyntaxError(msg)


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
