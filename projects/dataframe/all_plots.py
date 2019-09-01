import pandas as pd

# always import plotting first!
from plotting import colourWheel, dashesStyles, width, height
from dataframe import df_path, units  # , model
from matplotlib import pyplot  # , ticker
from mypackage.talys.api import u_factor

isotopes = (76, 86, 96)
niso = len(isotopes)

temperatures = (0.0, 1.0, 2.0)
ntemp = len(temperatures)


# I. read the data
# II. format the data
# III. plot the data


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
    # ne_data = (
    #     pd.read_hdf(df_path, "neutron_energy")
    #     .query("neutron_number in @isotopes and temperature in @temperatures")
    #     .assign(mass_number=lambda frame: frame.proton_number + frame.neutron_number)
    # )

    df = ee_data.drop(
        columns=[
            "mass_number",
            "proton_number",
            "tabulated_strength_function_mb",
            "tabulated_strength_function_fm",
            "strength_function_mb",
        ]
    )
    table = pd.pivot_table(
        df,
        index=["excitation_energy"],
        values=["strength_function_fm"],
        columns=["temperature", "neutron_number"],
    )

    for iso in isotopes:
        fig, ax = pyplot.subplots()
        fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)

        for j, T in enumerate(temperatures):
            series = table.loc[:, ("strength_function_fm", T, iso)]
            ax.plot(
                series.index.values,
                series.values,
                color=colourWheel[j % len(colourWheel)],
                linestyle="-",
                dashes=dashesStyles[j % len(dashesStyles)],
                label="%s MeV" % T,
            )

        ax.set_ylabel("$R$ %s" % units["strength_function_fm"], labelpad=-2)
        ax.set_xlabel("$E$ %s" % units["excitation_energy"], labelpad=-0.5)
        ax.legend(loc="upper left", ncol=1, handlelength=1)
        ax.annotate(s="N = %s" % iso, xy=(0.7, 0.8), xycoords="axes fraction")

        fig.set_size_inches(width, height)
        fig.savefig("N_%s_all_T.pdf" % iso)

    # for T in temperatures:
    # data = data(T)
    # create figure, ax
    # for iso in isotopes:
    # data = data(iso, T)
    # plot_dipole_strength_vs_energy(ax, data)
    # save figure

    # convert fm to mb and repeat the two loops above

    # repeat everything above, for cross_section


if __name__ == "__main__":
    main()
