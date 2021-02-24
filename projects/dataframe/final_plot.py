import pandas as pd
from matplotlib import pyplot, ticker
from figstyle import colourWheel, dashesStyles


def main():
    """Main entry point."""
    df = pd.read_csv("three_lines.csv", index_col="A")

    # Ratio between black data and blue data.

    fig, ax = pyplot.subplots(figsize=(3.404, 3.404 / 1.618), facecolor="white")
    fig.subplots_adjust(left=0.14, bottom=0.14, right=0.97, top=0.97)

    # ax.plot(
    #     "red",
    #     data=df,
    #     label=r"astroT = $10^{5}$ K, T = 0 MeV",
    #     marker="v",
    #     color=colourWheel[2],
    #     dashes=dashesStyles[2],
    # )
    ax.plot(
        df.index.to_numpy(),
        df.black / df.blue,
        label=r"astroT = $10^{10}$ K",
        marker="^",
        color=colourWheel[1],
        dashes=dashesStyles[1],
    )
    # ax.plot(
    #     "black",
    #     data=df,
    #     label=r"astroT = $10^{10}$ K, T = 0.86 MeV",
    #     marker="o",
    #     color=colourWheel[0],
    #     dashes=dashesStyles[0],
    # )

    ax.set_xlim(left=df.index.to_numpy()[0] - 1, right=df.index.to_numpy()[-1] + 1)
    ax.set_ylim(1.0, 2.0)

    # ax.set_yscale("log")
    ax.set_ylabel(
        "$\\lambda_{T=0.86\\,\\mathrm{MeV}} / \\lambda_{T=0.0\\,\\mathrm{MeV}}$"
    )
    ax.set_xlabel("A")

    ax.legend(loc="upper left", ncol=1, handlelength=1)

    ax.annotate(s="Sn", xy=(0.8, 0.8), xycoords="axes fraction")
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    ax.xaxis.set_major_locator(ticker.FixedLocator(df.index.to_numpy()))

    # locmaj = ticker.LogLocator(base=10.0, numticks=12)
    # ax.yaxis.set_major_locator(locmaj)

    # locmin = ticker.LogLocator(base=10.0, subs=(0.2, 0.4, 0.6, 0.8), numticks=12)
    # ax.yaxis.set_minor_locator(locmin)
    # ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    fig.savefig("Fig4.pdf")
    pyplot.close(fig)


if __name__ == "__main__":
    main()
