#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging

import pandas as pd
from flow import FlowProject
from mypackage.util import arefiles, match_split, frac_to_html

logger = logging.getLogger(__name__)
logfname = "project.log"


def np_to_html(n_or_p):
    np_mapping = {1: "&nu;", 2: "&pi;"}
    return np_mapping[n_or_p]


def state_to_html(state):
    state_orbital, state_frac = match_split(state)
    state_frac_html = frac_to_html(state_frac)
    return state_orbital + state_frac_html


def row_to_html(row):
    np_html = np_to_html(row["n_or_p"])

    from_state_html = state_to_html(row["from_state"])
    to_state_html = state_to_html(row["to_state"])

    return f"{np_html}{from_state_html}&rarr;{np_html}{to_state_html}"


def transitions_table(fname):
    dip_conf = pd.read_csv(
        fname,
        sep=r"\s+",
        header=None,
        usecols=[0, 1, 3, 4, 6, 7],
        names=[
            "n_or_p",
            "hole_energy",
            "particle_energy",
            "from_state",
            "to_state",
            "amplitude",
        ],
        dtype={
            "n_or_p": pd.Int64Dtype()
        },  # TODO pandas 1.0 , "from_state": pd.StringDtype(), "to_state": pd.StringDtype()}
    )

    filtered_conf = dip_conf[dip_conf.amplitude > 1]

    df = filtered_conf.sort_values(by=["n_or_p", "amplitude"], ascending=[False, False])

    df["transition"] = df.apply(row_to_html, axis=1)

    return df.loc[:, ["transition", "amplitude"]]


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(
    lambda job: all(
        job.isfile(fn)
        for fn in [
            rpa_id + "_dipole_transitions.txt" for rpa_id in job.doc.rpa_jobs.keys()
        ]
    )
)
@Project.post.isfile("dipole_transitions.h5")
def h5_transitions(job):
    appended_data = []

    for rpa_id, d in job.doc.rpa_jobs.items():
        fname = rpa_id + "_dipole_transitions.txt"
        transition_energy = d["transition_energy"]

        df = transitions_table(job.fn(fname)).set_index("transition")
        df2 = pd.concat([df], keys=[transition_energy], names=["transition_energy"])
        appended_data.append(df2)

    full_df = pd.concat(appended_data)
    full_df.to_hdf(job.fn("dipole_transitions.h5"), key="dipole_transitions")


@Project.operation
@Project.pre(arefiles(("excitation.out", "lorentzian.out")))
@Project.post.isfile("inset.png")
def plot_inset(job):
    import numpy as np
    from matplotlib.ticker import MultipleLocator
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.gridspec import GridSpec

    fig = Figure(figsize=(12, 4))
    canvas = FigureCanvas(fig)
    gs = GridSpec(1, 1)
    ax = fig.add_subplot(gs[0, 0])

    for lorexc in "excitation", "lorentzian":
        df = pd.read_csv(
            job.fn(f"{lorexc}.out"),
            delim_whitespace=True,
            comment="#",
            skip_blank_lines=True,
            header=None,
            names=["energy", "transition_strength"],
        )
        df = df[(df.energy >= 0.0) & (df.energy <= 10.0)]  # MeV
        if lorexc == "excitation":
            ax.vlines(df.energy, 0.0, df.transition_strength, colors="black")
            for v in job.doc.rpa_jobs.values():
                df_close = df[np.isclose(df.energy, v["transition_energy"], atol=0.01)]
                ax.vlines(
                    df_close.energy, 0.0, df_close.transition_strength, colors="red"
                )
        elif lorexc == "lorentzian":
            ax.plot(df.energy, df.transition_strength, color="black")

    ax.set(
        ylabel=r"$R \; (e^2fm^2/MeV)$",
        xlabel="E (MeV)",
        ylim=[-0.1, 4.0],
        xlim=[0.0, 10.0],
    )
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))

    for sp in "top", "right":
        ax.spines[sp].set_visible(False)

    canvas.print_png(job.fn("inset.png"))


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
