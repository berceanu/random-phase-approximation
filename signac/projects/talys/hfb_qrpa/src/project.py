#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging

import mypackage.util as util
import pandas as pd
from flow import FlowProject
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from mypackage.talys_api import TalysAPI

logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = TalysAPI()


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


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(arefiles((talys_api.input_fn, talys_api.energy_fn)))
@Project.post.isfile(talys_api.output_fn)
@Project.post(
    file_contains(
        talys_api.output_fn,
        "The TALYS team congratulates you with this successful calculation.",
    )
)
def run_talys(job):
    """Run TALYS binary with the original database file (HFB + QRPA result)."""
    command: str = talys_api.run_command
    # run TALYS in the job's folder
    util.sh(command, shell=True, cwd=job.workspace())


@Project.operation
@Project.pre.after(run_talys)
@Project.pre.isfile(talys_api.cross_section_fn)
@Project.post.isfile(talys_api.cross_section_png_fn)
def plot_cross_section(job):
    """Plot the TALYS output to get cross-section."""
    cross_section = pd.read_csv(
        job.fn(talys_api.cross_section_fn),
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
        label=f"HFB-QRPA",
    )

    ax.set(ylabel=r"Cross-Section [mb]", xlabel=r"$E_n$ [MeV]")
    element, mass = util.split_element_mass(job)
    ax.text(
        0.7,
        0.95,
        r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (mass - 1, element, mass, element),
        transform=ax.transAxes,
        color="black",
    )
    ax.legend(loc="lower left")
    canvas.print_png(job.fn(talys_api.cross_section_png_fn))
    logger.info("Saved %s" % job.fn(talys_api.cross_section_png_fn))


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
