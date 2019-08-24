import pandas as pd

# always import plotting first!
from plotting import colourWheel, dashesStyles, width, height
from dataframe import df_path
from matplotlib import pyplot, ticker

if __name__ == "__main__":
    # read the dataframe from file
    df = pd.read_pickle(df_path)

    # filter energy bounds
    lower = df["energy"] >= 0.1
    upper = df["energy"] <= 30
    both = lower & upper
    df2 = df[both]

    # sort by neutron number and energy
    df3 = df2.sort_values(by=["neutron_number", "energy"], ascending=[True, True])

    # select data with T = 2 MeV
    df4 = df3[df3["temperature"] == 2.0]

    # plot all isotopes for T = 2 MeV
    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
    dy = 0
    for j, neutron_number in enumerate(df4.neutron_number.unique()):
        isotope = df4.neutron_number == neutron_number
        mydf = df4[isotope]
        # print(mydf.energy.size)
        ax.plot(
            mydf.energy,
            mydf.strength_function + j * dy,
            color=colourWheel[j % len(colourWheel)],
            linestyle="-",
            dashes=dashesStyles[j % len(dashesStyles)],
            label=neutron_number,
        )

    ax.set_ylabel(r"$R$ [e${}^{2}$fm${}^{2}$/MeV]", labelpad=-2)
    ax.set_xlabel(r"$E$ [MeV]", labelpad=--0.5)
    ax.set_xlim(0.1, 30)
    ax.set_ylim(0, 10)

    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.major.formatter._useMathText = True
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    # ax.yaxis.set_label_coords(0.63,1.01)
    ax.legend(loc="upper left", ncol=2, handlelength=1)
    ax.annotate(s=r"$T = 0$", xy=(0.7, 0.8), xycoords="axes fraction")

    fig.set_size_inches(width, height)
    # fig.savefig("plot.pdf")  # facecolor='C7'

    # See https://tomaugspurger.github.io/method-chaining
