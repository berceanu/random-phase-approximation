import pandas as pd

from figstyle import colourWheel, dashesStyles, width, height
from dataash5 import df_path, units
from matplotlib import pyplot, ticker

isotopes = list(range(76, 98, 2))
niso = len(isotopes)

temperatures = (0.5, 1.0, 2.0)
ntemp = len(temperatures)


def plot_capture_rate_vs_n(ax, column, table, temperature, counter):
    series = table.loc[:, (column, temperature)]

    ax.plot(
        series.index.values,
        series.values,
        "-o",
        color=colourWheel[counter % len(colourWheel)],
        dashes=dashesStyles[counter % len(dashesStyles)],
        label="T = %s MeV" % temperature,
    )
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(ticker.FixedLocator(isotopes))
    ax.set_ylabel("Neutron Capture Rate %s" % units[column])
    ax.set_xlabel("N")
    ax.set_xlim(left=isotopes[0] - 1, right=isotopes[-1] + 1)

    ax.legend(loc="upper right", ncol=1, handlelength=1)


def main():
    ne_data = pd.read_hdf(df_path, "neutron_energy").query(
        "neutron_number in @isotopes and temperature in @temperatures"
    )
    df = ne_data.drop(
        columns=[
            "proton_number",
            "cross_section",
            "cross_section_talys",
            "capture_rate_talys",
            "neutron_energy",
        ]
    )
    table = pd.pivot_table(
        df, index=["neutron_number"], values=["capture_rate"], columns=["temperature"],
    )

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.14, bottom=0.09, right=0.97, top=0.97)
    for j, T in enumerate(temperatures):
        plot_capture_rate_vs_n(
            ax=ax, column="capture_rate", table=table, temperature=T, counter=j
        )
    ax.annotate(s="Sn", xy=(0.1, 0.6), xycoords="axes fraction")
    fig.set_size_inches(width, height)
    fig.savefig("capture_rate_vs_N.pdf")


if __name__ == "__main__":
    main()
