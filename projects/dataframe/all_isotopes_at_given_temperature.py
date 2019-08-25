import pandas as pd

# always import plotting first!
from plotting import colourWheel, dashesStyles, width, height
from dataframe import df_path, units
from matplotlib import pyplot, ticker

if __name__ == "__main__":
    selected_temperature = 2.0  # MeV
    # read the dataframe from file
    df = (
        pd.read_hdf(df_path, "computed_dipole_strengths")
        .loc[pd.IndexSlice[:, :, selected_temperature], :]
        .query("0.1 <= energy <= 30")
        .reset_index()
    )
    model = df.model.unique()
    df = df.drop(["model", "temperature"], axis=1).set_index("neutron_number")

    # plot all isotopes
    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
    dy = 0
    for j, neutron_number in enumerate(df.index.unique()):
        mydf = df.loc[neutron_number, :]
        # print(mydf.energy.size)
        ax.plot(
            mydf.energy,
            mydf.strength_function + j * dy,
            color=colourWheel[j % len(colourWheel)],
            linestyle="-",
            dashes=dashesStyles[j % len(dashesStyles)],
            label=neutron_number,
        )

    ax.set_ylabel("$R$ %s" % units["strength_function"], labelpad=-2)
    ax.set_xlabel("$E$ %s" % units["energy"], labelpad=-0.5)
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
    ax.annotate(s=model[0], xy=(0.7, 0.5), xycoords="axes fraction")

    fig.set_size_inches(width, height)
    # fig.savefig("plot.pdf")  # facecolor='C7'

    # See https://tomaugspurger.github.io/method-chaining
