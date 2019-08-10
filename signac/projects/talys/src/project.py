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
from mypackage.talys.api import TalysAPI
import mypackage.talys.data as data
import mypackage.talys.plotting as plotting
from mypackage.util import arefiles, last_line_contains

logger = logging.getLogger(__name__)
logfname = "project.log"

talys_api = TalysAPI()


class Project(FlowProject):
    pass


# NB: do not run this operation in parallel because of race conditions on the database file.
@Project.operation
@Project.pre(arefiles((talys_api.input_fn, talys_api.energy_fn)))
@Project.post.isfile(talys_api.output_fn)
@Project.post(
    last_line_contains(
        talys_api.output_fn,
        "The TALYS team congratulates you with this successful calculation.",
    )
)
def run_talys(job):
    @talys_api.replaced_database_file(job=job)
    def really_run_talys():
        """Run TALYS binary with the new database file."""
        command: str = talys_api.run_command
        # run TALYS in the job's folder
        util.sh(command, shell=True, cwd=job.workspace())

    really_run_talys()


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
        label=f"T={job.sp.temperature}",
        title=text,
    )

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
