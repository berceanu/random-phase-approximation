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
class AxesParameters:
    ylabel: str
    xlabel: str
    xscale: str
    xlim: Tuple[float, float]
    ylim: Tuple[float, float]
    yscale: str = "log"


def get_col_line_labels_by_temperature(mass_number):
    left_line_label = r"${}^{%s}$Sn" % mass_number
    right_line_label = r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn" % (
        (mass_number - 1),
        mass_number,
    )
    return left_line_label, right_line_label


def get_col_line_labels_by_isotope(temp):
    left_line_label = "T = %s MeV" % temp
    right_line_label = "T = %s MeV" % temp
    return left_line_label, right_line_label


def get_col_annotations_by_temperature(temp):
    left_annotations = Annotation(s="T = %s MeV" % temp, xy=(0.07, 0.95))
    right_annotations = Annotation(s="T = %s MeV" % temp, xy=(0.45, 0.95))
    return left_annotations, right_annotations


def get_col_annotations_by_isotope(mass_number):
    left_annotations = Annotation(s=r"${}^{%s}$Sn" % mass_number, xy=(0.1, 0.95))
    right_annotations = Annotation(
        s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn" % ((mass_number - 1), mass_number),
        xy=(0.35, 0.95),
    )
    return left_annotations, right_annotations


def grid_figure(
    temperatures,
    isotopes,
    column_left,
    column_right,
    ax_param_left,
    ax_param_right,
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
        raise ValueError

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
                (
                    line_label_col_left,
                    line_label_col_right,
                ) = get_col_line_labels_by_temperature(mass_number)
            elif aggregate_by == "isotope":
                iso = isotopes[row]
                temp = temperatures[line]
                (
                    line_label_col_left,
                    line_label_col_right,
                ) = get_col_line_labels_by_isotope(temp)
            else:
                raise ValueError

            for ax, column, line_label_col in zip(
                (ax_left, ax_right),
                (column_left, column_right),
                (line_label_col_left, line_label_col_right),
            ):
                series = column.data.loc[:, (column.name, temp, iso)]
                ax.plot(
                    series.index.values,
                    series.values,
                    color=colourWheel[line % len(colourWheel)],
                    linestyle="-",
                    dashes=dashesStyles[line % len(dashesStyles)],
                    label=line_label_col,
                )

        if aggregate_by == "temperature":
            temp = temperatures[row]
            ann_col_left, ann_col_right = get_col_annotations_by_temperature(temp)
        elif aggregate_by == "isotope":
            iso = isotopes[row]
            mass_number = 50 + iso
            ann_col_left, ann_col_right = get_col_annotations_by_isotope(mass_number)
        else:
            raise ValueError

        for ax, ax_param, ann_col in zip(
            (ax_left, ax_right),
            (ax_param_left, ax_param_right),
            (ann_col_left, ann_col_right),
        ):
            ax.set_xlabel(ax_param.xlabel)  # labelpad=-0.5
            ax.set_ylim(ax_param.ylim)
            ax.set_xlim(ax_param.xlim)
            ax.set_yscale(ax_param.yscale)
            ax.set_xscale(ax_param.xscale)
            ax.annotate(
                s=ann_col.s,
                xy=ann_col.xy,
                xycoords=ann_col.xycoords,
            )

    for ax in fig.axes[:-2]:  # all rows except bottom one
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

    for x, ax_param in zip((0.03, 0.52), (ax_param_left, ax_param_right)):
        fig.text(
            x, 0.57, ax_param.ylabel, ha="center", va="center", rotation="vertical"
        )

    for ax_index, loc in zip((2, 3), ("lower right", "lower left")):
        fig.axes[ax_index].legend(
            *fig.axes[ax_index - 2].get_legend_handles_labels(),
            loc=loc,
            handlelength=1.5,
            handletextpad=0.1,
            fontsize=7,
        )  # ncol=1

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
    sfunc_ax_prm = AxesParameters(
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
    xsec_ax_prm = AxesParameters(
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
        ax_param_left=sfunc_ax_prm,
        ax_param_right=xsec_ax_prm,
        aggregate_by="temperature",
        figname="strength_cross_section_T",
    )

    grid_figure(
        temperatures,
        isotopes,
        column_left=sfunc_col,
        column_right=xsec_col,
        ax_param_left=sfunc_ax_prm,
        ax_param_right=xsec_ax_prm,
        aggregate_by="isotope",
        figname="strength_cross_section_N",
    )


if __name__ == "__main__":
    main()
