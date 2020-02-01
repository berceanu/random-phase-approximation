import pandas as pd

from figstyle import colourWheel, dashesStyles, width, height
from dataash5 import df_path, units
from matplotlib import pyplot

isotopes = (76, 86, 96)
niso = len(isotopes)

temperatures = (0.0, 1.0, 2.0)
ntemp = len(temperatures)


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
            ax.annotate(s="N = %s" % iso, xy=(0.1, 0.9), xycoords="axes fraction")
            ax.legend(loc="lower right")
        fig.set_size_inches(width, height)
        fig.savefig("N_%s_all_T_%s.pdf" % (iso, column))


def main():
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
