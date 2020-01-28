import pandas as pd

# always import figstyle first!
from figstyle import colourWheel, dashesStyles, width, height
from dataash5 import df_path, units  # , model
from matplotlib import pyplot  # , ticker
from mypackage.talys.api import u_factor

isotopes = (76, 86, 96)
niso = len(isotopes)

temperatures = (0.0, 1.0, 2.0)
ntemp = len(temperatures)


def plot_series(ax, table, column, temperature, neutron_number, counter, label, annotation,
                plot_type="linear-linear", energy_interval=(0.1, 10)):
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
    ax.set_xlim(left=energy_interval[0], right=energy_interval[1])

    ax.set_ylabel("$R$ %s" % units[column], labelpad=-2)
    ax.set_xlabel("$E$ %s" % units["excitation_energy"], labelpad=-0.5)
    ax.legend(loc="upper left", ncol=1, handlelength=1)
    ax.annotate(s=annotation, xy=(0.7, 0.8), xycoords="axes fraction")


def plot_table(column, table, include_talys=False, plot_type="linear-linear"):
    for iso in isotopes:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
        for j, T in enumerate(temperatures):
            plot_series(ax=ax, table=table, column=column, temperature=T, neutron_number=iso,
                        counter=j, label="%s MeV" % T, annotation="N = %s" % iso, plot_type=plot_type)
            if T == 0 and include_talys:
                plot_series(ax=ax, table=table, column="tabulated_" + column, temperature=T, neutron_number=iso,
                            counter=niso + j, label="%s MeV TALYS" % T, annotation="N = %s" % iso, plot_type=plot_type)

        fig.set_size_inches(width, height)
        fig.savefig("N_%s_all_T_%s.pdf" % (iso, column))

    for T in temperatures:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
        for j, iso in enumerate(isotopes):
            plot_series(ax=ax, table=table, column=column, temperature=T, neutron_number=iso,
                        counter=j, label="%s" % iso, annotation="T = %s MeV" % T, plot_type=plot_type)
            if T == 0 and include_talys:
                plot_series(ax=ax, table=table, column="tabulated_" + column, temperature=T, neutron_number=iso,
                            counter=niso + j, label="%s TALYS" % iso, annotation="T = %s MeV" % T, plot_type=plot_type)

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
    df = ee_data.drop(
        columns=[
            "mass_number",
            "proton_number",
        ]
    )
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

    ###

    # plot_table(column="strength_function_fm", table=table, include_talys=True, plot_type="log-log")
    # plot_table(column="strength_function_mb", table=table, include_talys=True)

    # cross_section
    ne_data = (
        pd.read_hdf(df_path, "neutron_energy")
        .query("neutron_number in @isotopes and temperature in @temperatures")
        .assign(mass_number=lambda frame: frame.proton_number + frame.neutron_number)
        .rename(columns={"cross_section_talys": "tabulated_cross_section"})
    )
    df = ne_data.drop(
        columns=[
            "mass_number",
            "proton_number",
            "capture_rate",
            "capture_rate_talys",
        ]
    )
    table = pd.pivot_table(
        df,
        index=["neutron_energy"],
        values=[
            "cross_section",
            "tabulated_cross_section",
        ],
        columns=["temperature", "neutron_number"],
    )

    # plot_table(column="cross_section", table=table, include_talys=True, plot_type="log-log")

    # capture rate
    df = ne_data.drop(
        columns=[
            "proton_number",
            "cross_section",
            "tabulated_cross_section",
            "neutron_energy",
        ]
    )
    table = pd.pivot_table(
        df,
        index=["neutron_number"],
        values=[
            "capture_rate",
            "capture_rate_talys",
        ],
        columns=["temperature"]
    )
    print(table)
    print(table.index)
    print(table.columns)
    print(table.loc[:, ("capture_rate", 0.0)])

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
    for j, T in enumerate(temperatures):
        series = table.loc[:, ("capture_rate", T)]

        ax.plot(
            series.index.values,
            series.values,
            color=colourWheel[j % len(colourWheel)],
            linestyle="-",
            dashes=dashesStyles[j % len(dashesStyles)],
            label=str(T),
        )

    table = pd.pivot_table(
        df,
        index=["temperature"],
        values=[
            "capture_rate",
            "capture_rate_talys",
        ],
        columns=["neutron_number"]
    )

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
    for j, iso in enumerate(isotopes):
        series = table.loc[:, ("capture_rate", iso)]

        ax.plot(
            series.index.values,
            series.values,
            color=colourWheel[j % len(colourWheel)],
            linestyle="-",
            dashes=dashesStyles[j % len(dashesStyles)],
            label=str(iso),
        )


if __name__ == "__main__":
    main()
