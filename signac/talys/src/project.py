#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging
import pathlib
from dataclasses import dataclass

import mypackage.util as util
import pandas as pd
from flow import FlowProject, cmd, with_job
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)
logfname = "project.log"


#####################
# UTILITY FUNCTIONS #
#####################


def arefiles(file_names):
    """Check if all ``file_names`` are in ``job`` folder."""
    return lambda job: all(job.isfile(fn) for fn in file_names)


class Project(FlowProject):
    pass


@dataclass
class TalysData:
    output_fname: str = "output.txt"
    talys_bin = pathlib.PosixPath("~/bin/talys").expanduser()
    stderr_fname: str = "stderr.txt"
    cross_section_fname: str = "xs000000.tot"
    cross_section_png: str = "xsec.png"

    def run_command(self) -> str:
        """Construct the TALYS command to be ran."""
        assert self.talys_bin.is_file(), f"{self.talys_bin} not found!"

        return f"{self.talys_bin} < {self.input_fname} > {self.output_fname} 2> {self.stderr_fname}"


talys_data = TalysData()


def get_element_path(job):
    hfb_path = pathlib.PosixPath("~/src/talys/structure/gamma/hfb/").expanduser()

    element, _ = util.split_element_mass(job)
    element_path = hfb_path / f"{element}.psf"

    assert element_path.is_file(), f"{element_path} not found!"

    return element_path


def get_backup_path(job):
    p = get_element_path(job)
    return p.parent / (p.stem + f"_{job}.bck")


@Project.operation
@Project.pre.after(talys_input_file)
@Project.pre.after(talys_energy_file)
@Project.pre(lambda job: get_element_path(job).is_file())
@Project.post(lambda job: get_backup_path(job).is_file())
def backup_element(job):
    """backup TALYS database file"""
    util.copy_file(source=get_element_path(job), destination=get_backup_path(job))


@Project.operation
@Project.pre(lambda job: job.isfile(z_fn(job)))
@Project.pre.after(backup_element)
@Project.post(
    lambda job: filecmp.cmp(get_element_path(job), pathlib.Path(job.fn(z_fn(job))))
)
def replace_talys_file(job):
    util.copy_file(
        source=pathlib.Path(job.fn(z_fn(job))),
        destination=get_element_path(job),
        exist_ok=True,
    )


@Project.operation
@with_job
@cmd
@Project.pre.after(replace_talys_file)
@Project.post(arefiles((talys_data.output_fname, talys_data.cross_section_fname)))
def run_talys(job):
    """run TALYS"""
    command: str = talys_data.run_command()

    return f"echo {command} >> {logfname} && {command}"


@Project.operation
@Project.pre.after(run_talys)
@Project.post(lambda job: filecmp.cmp(get_element_path(job), get_backup_path(job)))
def restore_backup(job):
    util.copy_file(
        source=get_backup_path(job), destination=get_element_path(job), exist_ok=True
    )
    get_backup_path(job).unlink()  # delete backup file


@Project.operation
@Project.pre.after(run_talys)
@Project.post.isfile(talys_data.cross_section_png)
def plot_cross_section(job):
    """Plot the TALYS output to get cross-section."""
    cross_section = pd.read_csv(
        job.fn(talys_data.cross_section_fname),
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
    canvas.print_png(job.fn(talys_data.cross_section_png))
    logger.info("Saved %s" % job.fn(talys_data.cross_section_png))


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
