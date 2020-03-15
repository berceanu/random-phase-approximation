#!/usr/bin/env python3
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""

import logging
import pathlib
import shutil

import signac
from mypackage import util

logger = logging.getLogger(__name__)
logfname = "project.log"


def prepend_id(id, fname):
    return f"{id}_{fname}"


def copy_file(fname, from_job, to_job):
    local_fname = prepend_id(from_job.id, fname)
    shutil.copy(from_job.fn(fname), to_job.fn(local_fname))


def main():
    bulma_proj = signac.init_project("bulma", workspace="workspace")

    module_path = pathlib.Path(__file__).absolute().parent
    rpa_root = module_path / ".." / ".." / "rpa"
    rpa_proj = signac.get_project(root=rpa_root)

    logger.info("bulma project: %s" % bulma_proj.workspace())
    logger.info("rpa project: %s" % rpa_proj.workspace())

    statepoint = dict(
        # atomic number Z
        proton_number=50,  # fixed atomic number
        # nucleus angular momentum
        angular_momentum=1,  #
        # nucleus parity
        parity="-",  #
    )
    inset_fname = "inset.png"
    transitions_fname = "dipole_transitions.txt"

    for nn, rpa_jobs in rpa_proj.find_jobs(statepoint).groupby("neutron_number"):
        sp = statepoint.copy()
        sp.update(dict(neutron_number=nn))
        bulma_job = bulma_proj.open_job(sp).init()
        bulma_job.doc.setdefault(
            "nucleus",
            util.get_nucleus(
                proton_number=bulma_job.sp.proton_number,
                neutron_number=bulma_job.sp.neutron_number,
            ),
        )
        logger.info(f"Neutron number: {nn}")
        d = dict()

        for rpa_job in rpa_jobs:
            if rpa_job.sp.transition_energy != 0.42:
                logger.info("Processing %s.." % rpa_job.workspace())
                d[rpa_job.id] = dict(
                    temperature=rpa_job.sp.temperature,
                    transition_energy=rpa_job.sp.transition_energy,
                    transition_strength=rpa_job.sp.transition_strength,
                )
                for fname in (inset_fname, transitions_fname):
                    copy_file(fname, rpa_job, bulma_job)
        bulma_job.doc.setdefault("rpa_jobs", d)


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
