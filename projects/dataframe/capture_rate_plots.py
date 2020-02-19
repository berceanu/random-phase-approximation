import pandas as pd

# always import figstyle first!
from figstyle import colourWheel, dashesStyles, width, height
from dataash5 import df_path, units
from matplotlib import pyplot, ticker

isotopes = list(range(76, 98, 2))
niso = len(isotopes)

temperatures = (0.0, 0.5, 1.0, 2.0)
ntemp = len(temperatures)

# TODO remove file


def plot_capture_rate_vs_n(ax, column, table, temperature, counter):
    series = table.loc[:, (column, temperature)]

    ax.plot(
        series.index.values,
        series.values,
        "-o",
        color=colourWheel[counter % len(colourWheel)],
        dashes=dashesStyles[counter % len(dashesStyles)],
        label="%s MeV" % temperature,
    )
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(ticker.FixedLocator(isotopes))
    ax.set_ylabel("Neutron Capture Rate %s" % units[column], labelpad=-2)
    ax.set_xlabel("$N$", labelpad=-0.5)
    ax.set_xlim(left=isotopes[0], right=isotopes[-1])

    ax.legend(loc="upper right", ncol=1, handlelength=1)


def main():
    ne_data = (
        pd.read_hdf(df_path, "neutron_energy")
        .query("neutron_number in @isotopes and temperature in @temperatures")
        .assign(mass_number=lambda frame: frame.proton_number + frame.neutron_number)
    )
    df = ne_data.drop(
        columns=[
            "proton_number",
            "mass_number",
            "cross_section",
            "cross_section_talys",
            "neutron_energy",
        ]
    )
    table = pd.pivot_table(
        df,
        index=["neutron_number"],
        values=["capture_rate", "capture_rate_talys"],
        columns=["temperature"],
    )

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.10, bottom=0.14, right=0.97, top=0.97)
    for j, T in enumerate(temperatures):
        plot_capture_rate_vs_n(
            ax=ax, column="capture_rate", table=table, temperature=T, counter=j
        )
    fig.set_size_inches(width, height)
    fig.savefig("capture_rate_vs_N.pdf")

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.10, bottom=0.14, right=0.97, top=0.97)
    for j, T in enumerate(temperatures[1:]):
        plot_capture_rate_vs_n(
            ax=ax, column="capture_rate_talys", table=table, temperature=T, counter=j
        )
    fig.set_size_inches(width, height)
    fig.savefig("capture_rate_vs_N_TALYS.pdf")

    table = pd.pivot_table(
        df,
        index=["temperature"],
        values=["capture_rate", "capture_rate_talys"],
        columns=["neutron_number"],
    )

    def plot_capture_rate_vs_t(ax, column, table, isotope, counter, xticks):
        series = table.loc[:, (column, isotope)]

        ax.plot(
            series.index.values,
            series.values,
            "-o",
            color=colourWheel[counter % len(colourWheel)],
            dashes=dashesStyles[counter % len(dashesStyles)],
            label="%s" % isotope,
        )
        ax.set_yscale("log")
        ax.xaxis.set_major_locator(ticker.FixedLocator(xticks))
        ax.set_ylabel("Neutron Capture Rate %s" % units[column], labelpad=-2)
        ax.set_xlabel("$T$ %s" % units["temperature"], labelpad=-0.5)

        ax.legend(loc="upper right", ncol=1, handlelength=1)

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.10, bottom=0.14, right=0.97, top=0.97)
    for j, iso in enumerate((76, 86, 96)):
        plot_capture_rate_vs_t(
            ax=ax,
            column="capture_rate",
            table=table,
            isotope=iso,
            counter=j,
            xticks=(0.0, 0.5, 1.0, 1.5, 2.0),
        )
    fig.set_size_inches(width, height)
    fig.savefig("capture_rate_vs_T.pdf")

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.10, bottom=0.14, right=0.97, top=0.97)
    for j, iso in enumerate((76, 86, 96)):
        plot_capture_rate_vs_t(
            ax=ax,
            column="capture_rate_talys",
            table=table,
            isotope=iso,
            counter=j,
            xticks=(0.5, 1.0, 1.5, 2.0),
        )
    fig.set_size_inches(width, height)
    fig.savefig("capture_rate_vs_T_TALYS.pdf")


if __name__ == "__main__":
    main()
