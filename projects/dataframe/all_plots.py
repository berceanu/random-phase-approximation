import pandas as pd

# always import figstyle first!
from figstyle import colourWheel, dashesStyles, width, height
from dataash5 import df_path, units  # , model
from matplotlib import pyplot
from mypackage.talys.api import u_factor

isotopes = (76, 86, 96)
niso = len(isotopes)

temperatures = (0.0, 1.0, 2.0)
ntemp = len(temperatures)

# TODO remove file


def plot_series(
    ax,
    table,
    column,
    temperature,
    neutron_number,
    counter,
    label,
    annotation,
    plot_type="linear-linear",
    energy_interval=(0.1, 10),
    ylabel=None,
):  # "$R$ %s" % units[column]
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

    ax.set_ylabel(ylabel, labelpad=-2)
    ax.set_xlabel("$E$ %s" % units["excitation_energy"], labelpad=-0.5)
    ax.set_xlim(left=energy_interval[0], right=energy_interval[1])

    ax.legend(loc="upper left", ncol=1, handlelength=1)
    ax.annotate(s=annotation, xy=(0.7, 0.8), xycoords="axes fraction")


def plot_table(
    column,
    table,
    include_talys=False,
    talys_column=None,
    plot_type="linear-linear",
    energy_interval=(0.1, 10),
    ylabel=None,
):  # "$R$ %s" % units[column]
    for iso in isotopes:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.12, bottom=0.14, right=0.97, top=0.97)
        for j, T in enumerate(temperatures):
            plot_series(
                ax=ax,
                table=table,
                column=column,
                temperature=T,
                neutron_number=iso,
                counter=j,
                label="%s MeV" % T,
                annotation="N = %s" % iso,
                plot_type=plot_type,
                energy_interval=energy_interval,
                ylabel=ylabel,
            )
            if T == 0 and include_talys:
                plot_series(
                    ax=ax,
                    table=table,
                    column=talys_column,
                    temperature=T,
                    neutron_number=iso,
                    counter=niso + j,
                    label="TALYS %s MeV" % T,
                    annotation="N = %s" % iso,
                    plot_type=plot_type,
                    energy_interval=energy_interval,
                    ylabel=ylabel,
                )
        fig.set_size_inches(width, height)
        fig.savefig("N_%s_all_T_%s.pdf" % (iso, column))

    for T in temperatures:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.12, bottom=0.14, right=0.97, top=0.97)
        for j, iso in enumerate(isotopes):
            plot_series(
                ax=ax,
                table=table,
                column=column,
                temperature=T,
                neutron_number=iso,
                counter=j,
                label="%s" % iso,
                annotation="T = %s MeV" % T,
                plot_type=plot_type,
                energy_interval=energy_interval,
                ylabel=ylabel,
            )
            if T == 0 and include_talys:
                plot_series(
                    ax=ax,
                    table=table,
                    column=talys_column,
                    temperature=T,
                    neutron_number=iso,
                    counter=niso + j,
                    label="TALYS %s" % iso,
                    annotation="T = %s MeV" % T,
                    plot_type=plot_type,
                    energy_interval=energy_interval,
                    ylabel=ylabel,
                )
        fig.set_size_inches(width, height)
        fig.savefig("T_%s_all_N_%s.pdf" % (T, column))


def main():
    ee_data = (
        pd.read_hdf(df_path, "excitation_energy")
        .query("neutron_number in @isotopes and temperature in @temperatures")
        .assign(
            mass_number=lambda frame: frame.proton_number + frame.neutron_number,
            strength_function_mb=lambda frame: frame.strength_function_fm * u_factor,
            tabulated_strength_function_fm=lambda frame: frame.tabulated_strength_function_mb
            / u_factor,
        )
    )
    df = ee_data.drop(columns=["mass_number", "proton_number"])
    table = pd.pivot_table(
        df,
        index=["excitation_energy"],
        values=[
            "strength_function_fm",
            "strength_function_mb",
            "tabulated_strength_function_fm",
            "tabulated_strength_function_mb",
        ],
        columns=["temperature", "neutron_number"],
    )
    #
    plot_table(
        column="strength_function_fm",
        talys_column="tabulated_strength_function_fm",
        table=table,
        include_talys=False,
        plot_type="log-linear",
        energy_interval=(0, 20),
        ylabel="$R$ %s" % units["strength_function_fm"],
    )
    #
    #    plot_table(
    #        column="strength_function_mb",
    #        talys_column="tabulated_strength_function_mb",
    #        table=table,
    #        include_talys=False,
    #        plot_type="log-log",
    #        energy_interval=(0.1, 10),
    #        ylabel="$R$ %s" % units["strength_function_mb"],
    #    )
    #
    # cross_section
    ne_data = (
        pd.read_hdf(df_path, "neutron_energy")
        .query("neutron_number in @isotopes and temperature in @temperatures")
        .assign(mass_number=lambda frame: frame.proton_number + frame.neutron_number)
    )
    df = ne_data.drop(
        columns=["mass_number", "proton_number", "capture_rate", "capture_rate_talys"]
    )
    table = pd.pivot_table(
        df,
        index=["neutron_energy"],
        values=["cross_section", "cross_section_talys"],
        columns=["temperature", "neutron_number"],
    )

    plot_table(
        column="cross_section",
        talys_column="cross_section_talys",
        table=table,
        include_talys=False,
        plot_type="log-log",
        energy_interval=(0, 20),
        ylabel="Cross-Section %s" % units["cross_section"],
    )


if __name__ == "__main__":
    main()
