from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from dataash5 import df_path, units
from figstyle import colourWheel, dashesStyles, width
from matplotlib import ticker
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from pandas.core.frame import DataFrame


@dataclass(frozen=True)
class Annotation:
    s: str
    xy: Tuple[float, float]
    xycoords: str = "axes fraction"


@dataclass(frozen=True)
class Column:
    name: str
    data: DataFrame


@dataclass(frozen=True)
class TextLabels:
    line_label: str
    ann: Annotation


@dataclass(frozen=True)
class AxesParameters:
    ylabel: str
    xlabel: str
    xscale: str
    xlim: Tuple[float, float]
    ylim: Tuple[float, float]
    yscale: str = "log"


def grid_labels_agg_by_temperature(temp, mass_number):
    left_labels = TextLabels(
        line_label=r"${}^{%s}$Sn" % mass_number,
        ann=Annotation(s="T = %s MeV" % temp, xy=(0.07, 0.95)),
    )
    right_labels = TextLabels(
        line_label=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn"
        % ((mass_number - 1), mass_number),
        ann=Annotation(s="T = %s MeV" % temp, xy=(0.45, 0.95)),
    )
    return left_labels, right_labels


def grid_labels_agg_by_isotope(temp, mass_number):
    left_labels = TextLabels(
        line_label="T = %s MeV" % temp,
        ann=Annotation(s=r"${}^{%s}$Sn" % mass_number, xy=(0.1, 0.9)),
    )
    right_labels = TextLabels(
        line_label="T = %s MeV" % temp,
        ann=Annotation(
            s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn" % ((mass_number - 1), mass_number),
            xy=(0.1, 0.2),
        ),
    )
    return left_labels, right_labels


def grid_figure(
    temperatures,
    isotopes,
    column_left,
    column_right,
    param_left,
    param_right,
    aggregate_by,
    figname,
):
    if aggregate_by == "temperature":
        nrows = len(temperatures)
        nlines = len(isotopes)
    elif aggregate_by == "isotope":
        nrows = len(isotopes)
        nlines = len(temperatures)
    else:
        raise ValueError("Invalid aggregation")

    fig = Figure(figsize=(width, width * 1.4))  # constrained_layout=True
    gs = GridSpec(
        nrows=nrows,
        ncols=2,
        figure=fig,
        height_ratios=[1.0, 1.0, 1.0],
        width_ratios=[1.0, 1.0],
    )
    gs.update(wspace=0.28, hspace=0.03, bottom=0.06, left=0.11, right=0.99, top=0.99)

    for row in range(nrows):
        ax_left = fig.add_subplot(gs[row, 0])  # strength function
        ax_right = fig.add_subplot(gs[row, 1])  # cross section

        for line in range(nlines):
            if aggregate_by == "temperature":
                temp = temperatures[row]
                iso = isotopes[line]
                mass_number = 50 + iso
                labels_left, labels_right = grid_labels_agg_by_temperature(
                    temp, mass_number
                )
            elif aggregate_by == "isotope":
                temp = temperatures[line]
                iso = isotopes[row]
                mass_number = 50 + iso
                labels_left, labels_right = grid_labels_agg_by_isotope(
                    temp, mass_number
                )

            series_left = column_left.data.loc[:, (column_left.name, temp, iso)]
            series_right = column_right.data.loc[:, (column_right.name, temp, iso)]
            for ax, series, labels in zip(
                (ax_left, ax_right),
                (series_left, series_right),
                (labels_left, labels_right),
            ):
                ax.plot(
                    series.index.values,
                    series.values,
                    color=colourWheel[line % len(colourWheel)],
                    linestyle="-",
                    dashes=dashesStyles[line % len(dashesStyles)],
                    label=labels.line_label,
                )

        for ax, param, labels in zip(
            (ax_left, ax_right), (param_left, param_right), (labels_left, labels_right)
        ):
            ax.set_xlabel(param.xlabel)  # labelpad=-0.5
            ax.set_ylim(param.ylim)
            ax.set_xlim(param.xlim)
            ax.set_yscale(param.yscale)
            ax.set_xscale(param.xscale)
            ax.annotate(
                s=labels.ann.s, xy=labels.ann.xy, xycoords=labels.ann.xycoords,
            )

        if row != nrows - 1:  # all but the bottom panel
            for ax in (ax_left, ax_right):
                ax.xaxis.set_major_formatter(ticker.NullFormatter())
                ax.xaxis.label.set_visible(False)

    for ax in fig.axes:
        ax.tick_params(axis="both", which="major", labelsize=6)
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

    for ax in fig.axes[1::2]:  # right column
        ax.yaxis.set_major_locator(ticker.LogLocator(numticks=4))

    fig.axes[-4].legend(
        *fig.axes[-2].get_legend_handles_labels(),
        loc="lower right",
        handlelength=1.5,
        handletextpad=0.1,
        fontsize=7,
    )  # ncol=1, handlelength=1

    if aggregate_by == "temperature":
        fig.axes[-3].legend(
            *fig.axes[-1].get_legend_handles_labels(),
            loc="lower left",
            handlelength=1.5,
            handletextpad=0.1,
            fontsize=7,
        )  # ncol=1, handlelength=1

    fig.text(
        0.03, 0.57, param_left.ylabel, ha="center", va="center", rotation="vertical"
    )
    fig.text(
        0.52, 0.57, param_right.ylabel, ha="center", va="center", rotation="vertical"
    )

    fig.savefig(figname)


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
    sfunc_col = Column(name="strength_function_fm", data=sfunc_table)
    sfunc_prm = AxesParameters(
        ylabel="$R$ %s" % units["strength_function_fm"],
        xlabel="E %s" % units["excitation_energy"],
        xscale="linear",
        xlim=(0.0, 20.0),
        ylim=(3e-2, 1.2e1),
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
    xsec_col = Column(name="cross_section", data=xsec_table)
    xsec_prm = AxesParameters(
        ylabel="Cross-Section %s" % units["cross_section"],
        xlabel="E$_n$ %s" % units["neutron_energy"],
        xscale="log",
        xlim=(1e-3, 20.0),
        ylim=(1e-4, 1e3),
    )

    grid_figure(
        temperatures,
        isotopes,
        column_left=sfunc_col,
        column_right=xsec_col,
        param_left=sfunc_prm,
        param_right=xsec_prm,
        aggregate_by="temperature",
        figname="strength_cross_section_T_trial",
    )

    grid_figure(
        temperatures,
        isotopes,
        column_left=sfunc_col,
        column_right=xsec_col,
        param_left=sfunc_prm,
        param_right=xsec_prm,
        aggregate_by="isotope",
        figname="strength_cross_section_N_trial",
    )


if __name__ == "__main__":
    main()
