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
    gs.update(wspace=0.4, hspace=0.05, bottom=0.06, left=0.06, right=0.97, top=0.95)
    for row in range(nrows):
        # strength function
        ax_left = fig.add_subplot(gs[row, 0])
        # cross section
        ax_right = fig.add_subplot(gs[row, 1])

        for line in range(nlines):
            sfunc_series = sfunc_table.loc[
                :, ("strength_function_fm", temperatures[line], isotopes[row])
            ]
            xsec_series = xsec_table.loc[
                :, ("cross_section", temperatures[line], isotopes[row])
            ]

            for ax, series, param in zip(
                (ax_left, ax_right), (sfunc_series, xsec_series), (sfunc_prm, xsec_prm)
            ):
                ax.plot(
                    series.index.values,
                    series.values,
                    color=colourWheel[line % len(colourWheel)],
                    linestyle="-",
                    dashes=dashesStyles[line % len(dashesStyles)],
                    label=param.line_label % temperatures[line],
                )

        for ax, param in zip((ax_left, ax_right), (sfunc_prm, xsec_prm)):
            ax.set_ylabel(param.ylabel)
            ax.set_xlabel(param.xlabel)
            ax.set_ylim(param.ylim)
            ax.set_xlim(param.xlim)
            ax.set_yscale(param.yscale)
            ax.set_xscale(param.xscale)

        ax_left.annotate(
            s=sfunc_prm.ann.s % (50 + isotopes[row]),
            xy=sfunc_prm.ann.xy,
            xycoords=sfunc_prm.ann.xycoords,
        )
        ax_right.annotate(
            s=xsec_prm.ann.s % ((50 + isotopes[row] - 1), (50 + isotopes[row])),
            xy=xsec_prm.ann.xy,
            xycoords=xsec_prm.ann.xycoords,
        )

        if row != nrows - 1:  # all but the bottom panel
            for ax in (ax_left, ax_right):
                ax.xaxis.set_major_formatter(ticker.NullFormatter())
                ax.xaxis.label.set_visible(False)

    handles, labels = fig.axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=nlines)

    fig.savefig("grid_spec")

    # cb.ax.xaxis.set_minor_locator(ticker.NullLocator())
    # cb.ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    # cb.ax.xaxis.set_major_locator(
    #     ticker.FixedLocator([0.1, 0.2, 0.4, 0.6, 1.0, 2.0, 4.0])
    # )  # np.around(np.logspace(-1.30103, 0.60206, 10), decimals=1)
    # cb.ax.xaxis.set_major_formatter(ticker.ScalarFormatter())


if __name__ == "__main__":
    main()
