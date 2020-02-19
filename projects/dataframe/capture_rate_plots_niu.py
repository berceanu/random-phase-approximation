import pandas as pd

from figstyle import colourWheel, dashesStyles, width, golden_ratio
from dataash5 import df_path, units
from matplotlib import pyplot, ticker

temperatures = (1.0, 2.0)
MARKERS = {"1.0": "o", "2.0": "s"}


def plot_capture_rate_vs_n(ax, column, table, temperature, counter, mass_numbers):
    series = table.loc[:, (column, temperature)]

    ax.plot(
        series.index.values,
        series.values,
        marker=MARKERS[str(temperature)],
        color=colourWheel[counter % len(colourWheel)],
        dashes=dashesStyles[counter % len(dashesStyles)],
        label="T = %s MeV" % temperature,
    )
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(ticker.FixedLocator(mass_numbers))
    ax.set_ylabel("Neutron Capture Rate %s" % units[column])
    ax.set_xlabel("A")
    ax.set_xlim(left=mass_numbers[0] - 1, right=mass_numbers[-1] + 1)

    ax.legend(loc="upper right", ncol=1, handlelength=1)


def main():
    ne_data = (
        pd.read_hdf(df_path, "neutron_energy")
        .query("temperature in @temperatures")
        .assign(mass_number=lambda frame: frame.proton_number + frame.neutron_number)
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
    massnum = df["mass_number"].unique()
    table = pd.pivot_table(
        df, index=["mass_number"], values=["capture_rate"], columns=["temperature"]
    )

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.14, bottom=0.14, right=0.97, top=0.97)
    for j, T in enumerate(temperatures):
        plot_capture_rate_vs_n(
            ax=ax,
            column="capture_rate",
            table=table,
            temperature=T,
            counter=j + 1,
            mass_numbers=massnum,
        )
    ax.annotate(s="Sn", xy=(0.1, 0.6), xycoords="axes fraction")
    fig.set_size_inches(width, width / golden_ratio)
    fig.savefig("capture_rate_vs_N")


if __name__ == "__main__":
    main()
