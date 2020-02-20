from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from figstyle import colourWheel, dashesStyles, width, golden_ratio
from dataash5 import df_path, units
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib import ticker


@dataclass(frozen=True)
class Annotation:
    s: str
    xy: Tuple[float, float]
    xycoords: str = "axes fraction"


@dataclass(frozen=True)
class AxesParameters:
    ylabel: str
    xlabel: str
    xscale: str
    xlim: Tuple[float, float]
    ylim: Tuple[float, float]
    ann: Annotation
    yscale: str = "log"
    line_label: str = "T = %s MeV"


# TODO add new set of figures savefig("T_%s_all_N_%s.pdf" % (T, column)), see all_plots.py
# TODO label the 3 curves by nucleus symbol ${}^{A}$Sn in legend
# TODO use E_n instead of E for cross section x axis label
# TODO use same axes ranges as in "N_%s_all_T_%s"
# TODO move "T=.." annotations to area with no curves
# TODO use GridSpec to produce the final figure


def main():
    isotopes = (76, 86, 96)
    temperatures = (0.0, 1.0, 2.0)

    # strength function
    ee_data = pd.read_hdf(df_path, "excitation_energy").query(
        "neutron_number in @isotopes and temperature in @temperatures"
    )
    df = ee_data.drop(columns=["proton_number", "tabulated_strength_function_mb"])
    sfunc_table = pd.pivot_table(
        df,
        index=["excitation_energy"],
        values=["strength_function_fm"],
        columns=["temperature", "neutron_number"],
    )
    sfunc_prm = AxesParameters(
        ylabel="$R$ %s" % units["strength_function_fm"],
        xlabel="E %s" % units["excitation_energy"],
        xscale="linear",
        xlim=(0.0, 20.0),
        ylim=(3e-2, 1.2e1),
        ann=Annotation(s=r"${}^{%s}$Sn", xy=(0.5, 0.2)),
    )

    # cross section
    ne_data = pd.read_hdf(df_path, "neutron_energy").query(
        "neutron_number in @isotopes and temperature in @temperatures"
    )
    df = ne_data.drop(
        columns=[
            "proton_number",
            "capture_rate",
            "capture_rate_talys",
            "cross_section_talys",
        ]
    )
    xsec_table = pd.pivot_table(
        df,
        index=["neutron_energy"],
        values=["cross_section"],
        columns=["temperature", "neutron_number"],
    )
    xsec_prm = AxesParameters(
        ylabel="Cross-Section %s" % units["cross_section"],
        xlabel="E$_n$ %s" % units["neutron_energy"],
        xscale="log",
        xlim=(1e-3, 20.0),
        ylim=(1e-4, 1e3),
        ann=Annotation(s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn", xy=(0.1, 0.2)),
    )

    # GridSpec Figure
    nrows = len(isotopes)
    nlines = len(temperatures)

    fig = Figure(figsize=(width, width * golden_ratio))  # constrained_layout=True
    gs = GridSpec(
        nrows=nrows,
        ncols=2,
        figure=fig,
        height_ratios=[1.0, 1.0, 1.0],
        width_ratios=[1.0, 1.0],
    )
    gs.update(wspace=0.4, hspace=0.05, bottom=0.06, left=0.0, right=1.02)
    for row in range(nrows):
        # strength function
        ax_left = fig.add_subplot(gs[row, 0])

        for line in range(nlines):
            series = sfunc_table.loc[
                :, ("strength_function_fm", temperatures[line], isotopes[row])
            ]
            ax_left.plot(
                series.index.values,
                series.values,
                color=colourWheel[line % len(colourWheel)],
                linestyle="-",
                dashes=dashesStyles[line % len(dashesStyles)],
                label=sfunc_prm.line_label % temperatures[line],
            )
        ax_left.set_ylabel(sfunc_prm.ylabel)
        ax_left.set_xlabel(sfunc_prm.xlabel)

        ax_left.set_ylim(sfunc_prm.ylim)
        ax_left.set_xlim(sfunc_prm.xlim)
        ax_left.set_yscale(sfunc_prm.yscale)
        ax_left.set_xscale(sfunc_prm.xscale)

        ax_left.annotate(
            s=sfunc_prm.ann.s % (50 + isotopes[row]),
            xy=sfunc_prm.ann.xy,
            xycoords=sfunc_prm.ann.xycoords,
        )

        if row != nrows - 1:  # all but the bottom panel
            ax_left.xaxis.set_major_formatter(ticker.NullFormatter())
            ax_left.xaxis.label.set_visible(False)

        # cross section
        ax_right = fig.add_subplot(gs[row, 1])

        for line in range(nlines):
            series = xsec_table.loc[
                :, ("cross_section", temperatures[line], isotopes[row])
            ]
            ax_right.plot(
                series.index.values,
                series.values,
                color=colourWheel[line % len(colourWheel)],
                linestyle="-",
                dashes=dashesStyles[line % len(dashesStyles)],
                label=xsec_prm.line_label % temperatures[line],
            )
        ax_right.set_ylabel(xsec_prm.ylabel)
        ax_right.set_xlabel(xsec_prm.xlabel)

        ax_right.set_ylim(xsec_prm.ylim)
        ax_right.set_xlim(xsec_prm.xlim)
        ax_right.set_yscale(xsec_prm.yscale)
        ax_right.set_xscale(xsec_prm.xscale)

        ax_right.annotate(
            s=xsec_prm.ann.s % ((50 + isotopes[row] - 1), (50 + isotopes[row])),
            xy=xsec_prm.ann.xy,
            xycoords=xsec_prm.ann.xycoords,
        )

        if row != nrows - 1:  # all but the bottom panel
            ax_right.xaxis.set_major_formatter(ticker.NullFormatter())
            ax_right.xaxis.label.set_visible(False)

    handles, labels = fig.axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center")

    fig.savefig("grid_spec")

    # # strength function
    # for iso in isotopes:
    #     for counter, T in enumerate(temperatures):
    #         series = table.loc[:, ("strength_function_fm", T, iso)]
    #         ax.plot(
    #             series.index.values,
    #             series.values,
    #             color=colourWheel[counter % len(colourWheel)],
    #             linestyle="-",
    #             dashes=dashesStyles[counter % len(dashesStyles)],
    #             label=("T = %s MeV" % T),
    #         )
    #         ax.set_yscale("log")
    #         ax.set_xscale("linear")
    #         ax.set_ylabel("$R$ %s" % units["strength_function_fm"])
    #         ax.set_xlabel("E %s" % units["excitation_energy"])
    #         ax.set_xlim(left=0, right=20)
    #         ax.set_ylim(3e-2, 1.2e1)
    #     ax.annotate(
    #         s=r"${}^{%s}$Sn" % (50 + iso),
    #         xy=(0.1, 0.9),
    #         xycoords="axes fraction",
    #     )
    #     ax.legend(loc="lower right")

    # # cross section
    # for o in isotopes:
    #     fig2, ax1 = pyplot.subplots()
    #     fig2.subplots_adjust(left=0.15, bottom=0.09, right=0.97, top=0.97)
    #     for j1, t in enumerate(temperatures):
    #         series1 = table.loc[:, ("cross_section", t, o)]
    #         ax1.plot(
    #             series1.index.values,
    #             series1.values,
    #             color=colourWheel[j1 % len(colourWheel)],
    #             linestyle="-",
    #             dashes=dashesStyles[j1 % len(dashesStyles)],
    #             label=("T = %s MeV" % t),
    #         )
    #         ax1.set_yscale("log")
    #         ax1.set_xscale("log")
    #         ax1.set_ylabel("Cross-Section %s" % units["cross_section"])
    #         ax1.set_xlabel("E$_n$ %s" % units["neutron_energy"])
    #         ax1.set_xlim(left=1e-3, right=20)
    #         ax1.set_ylim(1e-4, 1e3)
    #     ax1.annotate(
    #         s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn"
    #           % ((50 + o - 1), (50 + o)),
    #         xy=(0.6, 0.9),
    #         xycoords="axes fraction",
    #     )
    #     ax1.legend(loc="lower left")


if __name__ == "__main__":
    main()
