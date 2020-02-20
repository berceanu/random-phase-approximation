from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from figstyle import colourWheel, dashesStyles, width, golden_ratio
from dataash5 import df_path, units
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

isotopes = (76, 86, 96)
niso = len(isotopes)

temperatures = (0.0, 1.0, 2.0)
ntemp = len(temperatures)


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
    legend_loc: str
    ann: Annotation
    yscale: str = "log"
    line_label: str = "T = %s MeV"


def annotate_axes(figr: Figure):
    """Takes a figure and puts an 'axN' label in the center of each Axes"""
    for i, axis in enumerate(figr.axes):
        axis.text(0.5, 0.5, f"ax{i + 1:d}", va="center", ha="center")
        axis.tick_params(labelbottom=False, labelleft=False)


def plot_series(
    ax,
    table,
    column,
    temperature,
    neutron_number,
    counter,
    label,
    ylabel,
    xlabel,
    plot_type="linear-linear",
    energy_interval=(0.1, 10),
):
    series = table.loc[:, (column, temperature, neutron_number)]

    ax.plot(
        series.index.values,
        series.values,
        color=colourWheel[counter % len(colourWheel)],
        linestyle="-",
        dashes=dashesStyles[counter % len(dashesStyles)],
        label=label,
    )

    ax.set_yscale(plot_type.split("-")[0])
    ax.set_xscale(plot_type.split("-")[1])

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xlim(left=energy_interval[0], right=energy_interval[1])
    if column == "strength_function_fm":
        ax.set_ylim(3e-2, 1.2e1)
    elif column == "cross_section":
        ax.set_ylim(1e-4, 1e3)


def plot_table(
    column, table, ylabel, xlabel, plot_type="linear-linear", energy_interval=(0.1, 10)
):
    for iso in isotopes:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.15, bottom=0.09, right=0.97, top=0.97)
        for j, T in enumerate(temperatures):
            plot_series(
                ax=ax,
                table=table,
                column=column,
                temperature=T,
                neutron_number=iso,
                counter=j,
                label="T = %s MeV" % T,
                plot_type=plot_type,
                energy_interval=energy_interval,
                ylabel=ylabel,
                xlabel=xlabel,
            )
        if column == "cross_section":
            mass_number_target = 50 + iso - 1
            mass_number_final = mass_number_target + 1
            ax.annotate(
                s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn"
                % (mass_number_target, mass_number_final),
                xy=(0.6, 0.9),
                xycoords="axes fraction",
            )
            ax.legend(loc="lower left")
        else:
            mass_number_final = 50 + iso
            ax.annotate(
                s=r"${}^{%s}$Sn" % mass_number_final,
                xy=(0.1, 0.9),
                xycoords="axes fraction",
            )
            ax.legend(loc="lower right")
        fig.set_size_inches(width, width / golden_ratio)
        fig.savefig("N_%s_all_T_%s" % (iso, column))


# TODO add new set of figures savefig("T_%s_all_N_%s.pdf" % (T, column)), see all_plots.py
# TODO label the 3 curves by nucleus symbol ${}^{A}$Sn in legend
# TODO use E_n instead of E for cross section x axis label
# TODO use same axes ranges as in "N_%s_all_T_%s"
# TODO move "T=.." annotations to area with no curves
# TODO use GridSpec to produce the final figure


def main():
    sfunc_prm = AxesParameters(
        ylabel="$R$ %s" % units["strength_function_fm"],
        xlabel="E %s" % units["excitation_energy"],
        xscale="linear",
        xlim=(0.0, 20.0),
        ylim=(3e-2, 1.2e1),
        legend_loc="lower right",
        ann=Annotation(s=r"${}^{%s}$Sn", xy=(0.1, 0.9)),
    )
    xsec_prm = AxesParameters(
        ylabel="Cross-Section %s" % units["cross_section"],
        xlabel="E$_n$ %s" % units["neutron_energy"],
        xscale="log",
        xlim=(1e-3, 20.0),
        ylim=(1e-4, 1e3),
        legend_loc="lower left",
        ann=Annotation(s=r"${}^{%s}$Sn(n,$\gamma$)${}^{%s}$Sn", xy=(0.6, 0.9)),
    )
    print(sfunc_prm)
    print(xsec_prm)

    fig = Figure(constrained_layout=True)
    gs = GridSpec(
        nrows=3,
        ncols=2,
        figure=fig,
        height_ratios=[1.0, 1.0, 1.0],
        width_ratios=[1.0, 1.0],
    )
    for g in gs:
        ax = fig.add_subplot(g)
        print(ax)
    annotate_axes(fig)
    fig.set_size_inches(width, width * golden_ratio)
    fig.savefig("grid_spec")

    # strength function
    ee_data = pd.read_hdf(df_path, "excitation_energy").query(
        "neutron_number in @isotopes and temperature in @temperatures"
    )
    df = ee_data.drop(columns=["proton_number", "tabulated_strength_function_mb"])
    table = pd.pivot_table(
        df,
        index=["excitation_energy"],
        values=["strength_function_fm"],
        columns=["temperature", "neutron_number"],
    )
    plot_table(
        column="strength_function_fm",
        table=table,
        plot_type="log-linear",
        energy_interval=(0, 20),
        ylabel="$R$ %s" % units["strength_function_fm"],
        xlabel="E %s" % units["excitation_energy"],
    )

    # cross_section
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
    table = pd.pivot_table(
        df,
        index=["neutron_energy"],
        values=["cross_section"],
        columns=["temperature", "neutron_number"],
    )
    plot_table(
        column="cross_section",
        table=table,
        plot_type="log-log",
        energy_interval=(1e-3, 20),
        ylabel="Cross-Section %s" % units["cross_section"],
        xlabel="E$_n$ %s" % units["neutron_energy"],
    )


if __name__ == "__main__":
    main()
