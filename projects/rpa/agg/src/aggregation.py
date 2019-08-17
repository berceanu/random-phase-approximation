#!/usr/bin/env python3
"""This module plots the dipole strengths for a single nucleus at various temperatures."""

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib import rcParams
from cycler import cycler
from collections import defaultdict
import pandas as pd
import copy
import signac as sg
import mypackage.code_api as code_api
import mypackage.util as util
import argparse
import itertools as it
import logging

logger = logging.getLogger(__name__)

# matplotlib settings
min_exp = tuple(rcParams["axes.formatter.limits"])[0]
y_formatter = ScalarFormatter(useMathText=True)
y_formatter.set_powerlimits((min_exp, 5))

line_colors = ["C0", "C1", "C2", "C3"]
line_styles = ["-", "--", ":", "-."]

cyl = cycler(color=line_colors) + cycler(linestyle=line_styles)
vert_cyl = cycler(colors=line_colors) + cycler(linestyles=line_styles)

loop_cy_iter = cyl()
vert_loop_cy_iter = vert_cyl()

STYLE = defaultdict(lambda: next(loop_cy_iter))
vert_STYLE = defaultdict(lambda: next(vert_loop_cy_iter))


def isofigure(
    job_group,
    isoscalar_panel=False,
    vlines=False,
    minEnergy=None,
    maxEnergy=None,
    maxIsoscalarR=100000.0,
    maxIsovectorR=13.0,  # e^2*fm^2/MeV
    code_mapping=code_api.NameMapping(),
):

    if not minEnergy:
        minEnergy = 0.0  # MeV
    if not maxEnergy:
        maxEnergy = 30.0  # MeV

    plot_type = ["lorentzian"]
    if vlines:
        plot_type.append("excitation")

    panels = ["isovector"]
    if isoscalar_panel:
        panels.append("isoscalar")
        fig = Figure(figsize=(12, 6))  # width, height in inches
        _ = FigureCanvas(fig)
        gs = GridSpec(2, 1)
        ax = {
            "isoscalar": fig.add_subplot(gs[0, 0]),
            "isovector": fig.add_subplot(gs[1, 0]),
        }
    else:  # no isoscalar panel
        fig = Figure(figsize=(10, 4))
        _ = FigureCanvas(fig)
        gs = GridSpec(1, 1)
        ax = {"isovector": fig.add_subplot(gs[0, 0])}

    def isoplotax(ax=plt.gca(), lorexc="lorentzian"):
        if lorexc == "excitation":
            ax.vlines(
                df.energy,
                0.0,
                df.transition_strength,
                label="_nolegend_",
                **vert_STYLE[str(job.sp.temperature)],
            )

        elif lorexc == "lorentzian":
            ax.plot(
                df.energy,
                df.transition_strength,
                label=f"T = {job.sp.temperature} MeV",
                **STYLE[str(job.sp.temperature)],
            )

        else:
            raise ValueError("`lorexc` must be either 'lorentzian' or 'excitation'")

    for job in sorted(job_group, key=lambda job: job.sp.temperature):
        temp = "finite" if job.sp.temperature > 0 else "zero"

        for skalvec in panels:
            for sp in "top", "bottom", "right":
                ax[skalvec].spines[sp].set_visible(False)
            ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
            ax[skalvec].set_title(skalvec)

            for lorexc in plot_type:
                fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))
                df = pd.read_csv(
                    fn,
                    delim_whitespace=True,
                    comment="#",
                    skip_blank_lines=True,
                    header=None,
                    names=["energy", "transition_strength"],
                )
                df = df[(df.energy >= minEnergy) & (df.energy <= maxEnergy)]  # MeV

                isoplotax(ax=ax[skalvec], lorexc=lorexc)

    ax["isovector"].legend()
    ax["isovector"].set(xlabel="E (MeV)", ylim=[None, maxIsovectorR])
    if isoscalar_panel:
        ax["isoscalar"].set(ylim=[None, maxIsoscalarR])
        ax["isoscalar"].yaxis.set_major_formatter(y_formatter)
        fig.subplots_adjust(hspace=0.3)

    return fig


def main_groupby(args):
    rpa = sg.get_project(root="../")
    aggregation = sg.get_project(root="./")
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("agg project: %s" % aggregation.root_directory())

    code = code_api.NameMapping()

    for (z, n), group in rpa.groupby(("proton_number", "neutron_number")):
        logger.info("(Z, N) =  (%s, %s)" % (z, n))

        atomic_symbol, mass_number = util.get_nucleus(z, n, joined=False)

        gr1, gr2 = it.tee(group)

        statepoints = []
        origin = {}
        for job in gr1:
            origin[f"T = {job.sp.temperature} MeV".replace(".", "_")] = str(job)
            sp = copy.deepcopy(job.sp())
            statepoints.append(sp)
        const_sp = dict(set.intersection(*(set(d.items()) for d in statepoints)))

        fig = isofigure(
            gr2,
            isoscalar_panel=args.isoscalar,
            vlines=args.vlines,
            minEnergy=args.minEnergy,
            maxEnergy=args.maxEnergy,
            maxIsoscalarR=args.maxIsoscalarR,
            maxIsovectorR=args.maxIsovectorR,
            code_mapping=code,
        )

        with aggregation.open_job(
            const_sp
        ) as agg_job:  # .init() implicitly called here
            agg_job.doc["nucleus"] = str(mass_number) + atomic_symbol
            agg_job.doc.update(origin)

            fig.suptitle(
                (
                    fr"Transition strength distribution of ${{}}^{{{mass_number}}} {atomic_symbol} \; "
                    fr"{agg_job.sp.angular_momentum}^{{{agg_job.sp.parity}}}$"
                )
            )

            # save figure to disk in agg_job's folder
            fig.canvas.print_png("iso_all_temp_all.png")


def main():
    parser = argparse.ArgumentParser(
        description="this script plots the aggregated transition strengths "
        "for each nucleus over all temperatures."
    )
    parser.add_argument(
        "--vlines",
        action="store_true",
        help="Add vertical lines at transition energies to plots.",
    )
    parser.add_argument(
        "--isoscalar", action="store_true", help="Plot isoscalar component as well."
    )
    parser.add_argument(
        "--minEnergy", type=float, help="Lower energy threshold for spectrum, in MeV."
    )
    parser.add_argument(
        "--maxEnergy", type=float, help="Upper energy threshold for spectrum, in MeV."
    )
    parser.add_argument(
        "--maxIsovectorR",
        type=float,
        help="Upper transition strength threshold for isovector spectrum, in e^2*fm^2/MeV.",
    )
    parser.add_argument(
        "--maxIsoscalarR",
        type=float,
        help="Upper transition strength threshold for isoscalar spectrum, in e^2*fm^2/MeV.",
    )

    args = parser.parse_args()  # load command line args
    main_groupby(args)


if __name__ == "__main__":
    logging.basicConfig(
        filename="project.log",
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==RUN STARTED==")
    main()
    logger.info("==RUN FINISHED==")
