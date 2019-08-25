import numpy as np
import pandas as pd

# always import plotting first!
from plotting import width
from dataframe import df_path, units

from matplotlib import pyplot, ticker, colors

if __name__ == "__main__":
    df = pd.read_hdf(df_path, "computed_dipole_strengths")

    low_energy = 0.1  # MeV
    high_energy = 30  # MeV
    mask = (df["energy"] >= low_energy) & (df["energy"] <= high_energy)
    df = df[mask]

    chosen_temperatures = (0.0, 1.0, 2.0)

    fig, axarr = pyplot.subplots(len(chosen_temperatures), 1, constrained_layout=True)
    axes = {str(T): ax for T, ax in zip(np.flip(chosen_temperatures), axarr.flat)}

    for T in chosen_temperatures:
        df_single_T = df.loc[pd.IndexSlice[:, :, T], :]

        isotopes = df_single_T.index.unique(level="neutron_number").values
        y = df_single_T.loc[:, "strength_function"].values.reshape(isotopes.size, -1)
        x = np.empty(y.shape[1])
        x[:] = df_single_T.iloc[0 : y.shape[1], 0].values

        nn_boundaries = np.append(isotopes - 1, isotopes[-1] + 1)

        ax = axes[str(T)]

        mappable = ax.pcolormesh(
            x,
            nn_boundaries,
            y,
            norm=colors.LogNorm(),
            vmin=0.05,
            vmax=4.5,
            cmap="turbo",
            linewidth=0,
            rasterized=True,
        )

        ax.annotate(
            s=f"$T = {T}$ MeV", xy=(0.70, 0.68), xycoords="axes fraction", color="b"
        )

        for N in isotopes:
            ax.annotate(
                s=str(N), xy=(29, N - 0.9), xycoords="data", color="w", fontsize=7
            )
            if N < isotopes[-1]:
                ax.axhline(N + 1, color="w", lw=0.2)

    cb = fig.colorbar(mappable, ax=axarr.flat, location="top", shrink=1.0, aspect=30)
    cb.outline.set_visible(False)
    cb.set_label("$R$ %s" % units["strength_function"])
    cb.ax.xaxis.set_minor_locator(ticker.NullLocator())
    cb.ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    cb.ax.xaxis.set_major_locator(
        ticker.FixedLocator([0.1, 0.2, 0.4, 0.6, 1.0, 2.0, 4.0])
    )  # np.around(np.logspace(-1.30103, 0.60206, 10), decimals=1)
    cb.ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

    for ax in axarr[:-1].flat:
        ax.set_xticklabels([])

    for ax in axarr.flat:
        ax.set_xlim(low_energy, high_energy)
        ax.yaxis.set_minor_locator(ticker.NullLocator())
        ax.yaxis.set_minor_formatter(ticker.NullFormatter())

        # https://jakevdp.github.io/PythonDataScienceHandbook/04.10-customizing-ticks.html
        ax.yaxis.set_major_locator(ticker.NullLocator())
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

        ax.xaxis.set_major_locator(ticker.FixedLocator([5, 10, 15, 20, 25]))

        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

    #     ax.xaxis.tick_bottom()

    axes["0.0"].set_xlabel("$E$ %s" % units["energy"], labelpad=-0.5)

    fig.set_size_inches(width, 1.4 * width)
    fig.savefig("colormesh.pdf")  # facecolor='C7'