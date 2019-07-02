#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import math
import os
import pathlib

import mypackage.util as util
import numpy as np
import signac
from jinja2 import Environment, FileSystemLoader

# pass folder containing the template
file_loader = FileSystemLoader("src/templates")
env = Environment(loader=file_loader)

logger = logging.getLogger(__name__)
logfname = "project.log"


def energy_values():
    """Generate energy input file contents."""
    my_v, step = np.linspace(0.1, 30.0, 300, retstep=True)
    assert math.isclose(step, 0.1), f"step {step} is not 0.1!"

    return my_v.round(1)


def talys_input_file(job):
    """Generate TALYS input file."""
    element, mass = util.split_element_mass(job)
    # we hit the element with N - 1 with 1 neutron
    input_contents = env.get_template("input.j2").render(
        element=element, mass=mass - 1, energy_fname="energy.in", astro=job.sp.astro
    )
    file_path = pathlib.Path(job.fn("input.txt"))
    util.write_contents_to(file_path, input_contents)


def talys_energy_file(job):
    """Generate TALYS energy input file."""
    file_path = pathlib.Path(job.fn("energy.in"))
    np.savetxt(file_path, job.sp.projectile_energy, fmt="%.3f", newline=os.linesep)
    logger.info("Wrote %s" % file_path)


def main():
    talys = signac.init_project("talys", workspace="workspace")

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
        # todo add description
        astro="n",  # / "y"
        # incoming neutron energy
        projectile_energy=energy_values(),
    )
    extra_keys = ("astro", "projectile_energy")

    talys.open_job(statepoint).init()
    rpa = signac.get_project(root="../")
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("talys project: %s" % talys.root_directory())

    for talys_job in talys:
        talys_energy_file(talys_job)
        talys_input_file(talys_job)

        rpa_job = rpa.open_job(
            statepoint=util.remove_from_dict(talys_job.sp, extra_keys)
        )

        fname = rpa_job.doc["talys_input"]
        util.copy_file(source=rpa_job.fn(fname), destination=talys_job.fn(fname))


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
