import pandas as pd

# always import figstyle first!
from figstyle import colourWheel, dashesStyles, width, height
from dataframe import df_path, units, model
from matplotlib import pyplot, ticker


def main():
    selected_temperature = 2.0  # MeV

    # read the dataframe from file
    df = (
        pd.read_hdf(df_path, "excitation_energy")
        .query("temperature == %s" % selected_temperature)
        .drop(["temperature"], axis=1)
        .set_index("neutron_number")
    )

    # plot all isotopes
    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
    for j, neutron_number in enumerate(df.index.unique()):
        mydf = df.loc[neutron_number, :]
        # print(mydf.energy.size)
        ax.plot(
            mydf["excitation_energy"],
            mydf["strength_function_fm"],
            color=colourWheel[j % len(colourWheel)],
            linestyle="-",
            dashes=dashesStyles[j % len(dashesStyles)],
            label=neutron_number,
        )

    ax.set_ylabel("$R$ %s" % units["strength_function_fm"], labelpad=-2)
    ax.set_xlabel("$E$ %s" % units["excitation_energy"], labelpad=-0.5)
    ax.set_xlim(0.1, 30)
    ax.set_ylim(0, 10)

    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.major.formatter._useMathText = True
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    # ax.yaxis.set_label_coords(0.63,1.01)
    ax.legend(loc="upper left", ncol=2, handlelength=1)
    ax.annotate(
        s="$T = %s$" % selected_temperature, xy=(0.7, 0.8), xycoords="axes fraction"
    )
    ax.annotate(s=model(selected_temperature), xy=(0.7, 0.5), xycoords="axes fraction")

    fig.set_size_inches(width, height)
    fig.savefig("plot.pdf")  # facecolor='C7'

    # See https://tomaugspurger.github.io/method-chaining


if __name__ == "__main__":
    main()
