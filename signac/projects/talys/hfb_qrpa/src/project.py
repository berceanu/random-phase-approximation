#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging

import mypackage.util as util
from flow import FlowProject
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from mypackage.talys_api import TalysAPI
import mypackage.talys_data as data
import mypackage.talys_plotting as plotting

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


# todo move to mypackage.util


def arefiles(file_names):
    """Check if all ``file_names`` are in ``job`` folder."""
    return lambda job: all(job.isfile(fn) for fn in file_names)


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(arefiles((talys_api.input_fn, talys_api.energy_fn)))
@Project.post.isfile(talys_api.output_fn)
@Project.post(
    file_contains(  # todo check last line only
        talys_api.output_fn,
        "The TALYS team congratulates you with this successful calculation.",
    )
)
def run_talys(job):
    """Run TALYS binary with the original database file (HFB + QRPA result)."""
    command: str = talys_api.run_command
    # run TALYS in the job's folder
    util.sh(command, shell=True, cwd=job.workspace())


# todo move to mypackage.talys_plots
@Project.operation
@Project.pre.after(run_talys)
@Project.pre.isfile(talys_api.cross_section_fn)
@Project.post.isfile(talys_api.cross_section_png_fn)
def plot_cross_section(job):
    """Plot the TALYS output to get cross-section."""

    cross_section = data.read_cross_section(job.fn(talys_api.cross_section_fn))

    fig = Figure(figsize=(6.4, 6.4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    atomic_symbol, mass_number = util.get_nucleus(
        job.sp.proton_number, job.sp.neutron_number, joined=False
    )
    text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
        mass_number - 1,
        atomic_symbol,
        mass_number,
        atomic_symbol,
    )

    plotting.plot_cross_section(
        ax,
        cross_section["energy"],
        cross_section["compound"],
        color="black",
        label=f"HFB-QRPA",
        text=text,
    )

    canvas.print_png(job.fn(talys_api.cross_section_png_fn))
    logger.info("Saved %s" % job.fn(talys_api.cross_section_png_fn))


# todo extract datapoint(s) for the astro="y" case

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
