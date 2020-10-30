import pandas as pd

from figstyle import colourWheel, dashesStyles, width, golden_ratio
from dataash5 import df_path, units
from matplotlib import pyplot, ticker

my_astroT = 0.0001


def main():
    ne_data = pd.read_hdf(df_path, "capture_rate").assign(
        mass_number=lambda frame: frame.proton_number + frame.neutron_number
    )
    df = ne_data.drop(
        columns=[
            "proton_number",
        ]
    )
    massnum = df["mass_number"].unique()
    table = pd.pivot_table(
        df, index=["mass_number"], values=["capture_rate"], columns=["astroT"]
    )
    series = table.loc[:, ("capture_rate", my_astroT)]

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.14, bottom=0.14, right=0.97, top=0.97)

    ax.plot(
        series.index.values,
        series.values,
        marker="o",
        color=colourWheel[1 % len(colourWheel)],
        dashes=dashesStyles[1 % len(dashesStyles)],
        label="astroT = %s x 10**9 K" % my_astroT,
    )
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(ticker.FixedLocator(massnum))
    ax.set_ylabel("Neutron Capture Rate %s" % units["capture_rate"])
    ax.set_xlabel("A")
    ax.set_xlim(left=massnum[0] - 1, right=massnum[-1] + 1)

    ax.legend(loc="upper right", ncol=1, handlelength=1)

    ax.annotate(s="Sn", xy=(0.1, 0.6), xycoords="axes fraction")
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    fig.set_size_inches(width, width / golden_ratio)
    fig.savefig("capture_rate_vs_N")


if __name__ == "__main__":
    main()
