#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging
import os

import mypackage.util as util
import pandas as pd
from flow import FlowProject, cmd, with_job
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from talys_utils import talys

logger = logging.getLogger(__name__)
logfname = "project.log"


#####################
# UTILITY FUNCTIONS #
#####################

def file_contains(filename, text):
    """Checks if ``filename`` contains ``text``."""
    return (
        lambda job: job.isfile(filename) and text in open(job.fn(filename), "r").read()
    )

def arefiles(file_names):
    """Check if all ``file_names`` are in ``job`` folder."""
    return lambda job: all(job.isfile(fn) for fn in file_names)


def areidentical(f1, f2):
    """Return True if the two files are identical."""
    from filecmp import cmp

    # Not identical if either file is missing.
    if (not os.path.isfile(f1)) or (not os.path.isfile(f2)):
        return False

    return cmp(f1, f2)


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(lambda job: os.path.isfile(job.doc["database_file"]))
@Project.post(lambda job: os.path.isfile(job.doc["database_file_backup"]))
def backup_database_file(job):
    """Backup TALYS database file (eg Sn.psf to Sn_<job._id>.bck)"""
    util.copy_file(
        source=job.doc["database_file"], destination=job.doc["database_file_backup"]
    )


@Project.operation
@Project.pre(lambda job: job.isfile(job.doc["z_file"]))
@Project.pre(lambda job: os.path.isfile(job.doc["database_file"]))
@Project.pre.after(backup_database_file)
@Project.post(
    lambda job: areidentical(job.fn(job.doc["z_file"]), job.doc["database_file"])
)
def replace_database_file(job):
    """Replace TALYS database file (eg Sn.psf) with the job's file (eg. z050)."""
    util.copy_file(
        source=job.fn(job.doc["z_file"]),
        destination=job.doc["database_file"],
        exist_ok=True,
    )


@Project.operation
@with_job
@cmd
@Project.pre.after(replace_database_file)
@Project.post.isfile(talys.output_fn)
@Project.post(file_contains(talys.output_fn, "The TALYS team congratulates you with this successful calculation."))
def run_talys(job):
    """Run TALYS binary with the new database file."""
    command: str = talys.run_command

    return f"echo {command} >> {logfname} && {command}"


@Project.operation
@Project.pre.after(run_talys)
@Project.post(
    lambda job: areidentical(job.doc["database_file"], job.doc["database_file_backup"])
)
def restore_database_file(job):
    """Restore original TALYS database file (eg Sn.psf)."""
    util.copy_file(
        source=job.doc["database_file_backup"],
        destination=job.doc["database_file"],
        exist_ok=True,
    )


@Project.operation
@Project.pre.after(run_talys)
@Project.pre.after(restore_database_file)
@Project.post(lambda job: not os.path.isfile(job.doc["database_file_backup"]))
def remove_database_file_backup(job):
    """Delete TALYS database file backup (eg. Sn_<job._id>.bck)."""
    os.remove(job.doc["database_file_backup"])


@Project.operation
@Project.pre.after(run_talys)
@Project.pre.isfile(talys.cross_section_fn)
@Project.post.isfile(talys.cross_section_png_fn)
def plot_cross_section(job):
    """Plot the TALYS output to get cross-section."""
    cross_section = pd.read_csv(
        job.fn(talys.cross_section_fn),
        sep=r"\s+",
        header=None,
        comment="#",
        names=[
            "energy",
            "xs",
            "gamma_xs",
            "xs_over_res_prod_xs",
            "direct",
            "preequilibrium",
            "compound",
        ],
    )

    fig = Figure(figsize=(6.4, 6.4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    ax.loglog(
        cross_section["energy"],
        cross_section["compound"],
        color="black",
        label=f"T={job.sp.temperature}",
    )

    ax.set(
        xlim=[1e-3, 10.0],
        ylim=[1e-4, 100.0],
        ylabel=r"Cross-Section [mb]",
        xlabel=r"$E_n$ [MeV]",
    )
    element, mass = util.split_element_mass(job)
    ax.text(
        0.7,
        0.95,
        r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (mass - 1, element, mass, element),
        transform=ax.transAxes,
        color="black",
    )
    ax.legend(loc="lower left")
    canvas.print_png(job.fn(talys.cross_section_png_fn))
    logger.info("Saved %s" % job.fn(talys.cross_section_png_fn))


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfname,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==RUN STARTED==")
    Project().main()
    logger.info("==RUN FINISHED==")
