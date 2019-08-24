import numpy as np
import pandas as pd

# always import plotting first!
from plotting import width
from dataframe import df_path

from matplotlib import pyplot, ticker, colors


def all_strength_functions_for_temperature(temperature, d_frame, n_energy=2991):
    all_neutron_numbers = d_frame.neutron_number.unique()
    nisotopes = len(all_neutron_numbers)

    d_frame_2 = d_frame[d_frame["temperature"] == temperature]

    all_curves = np.empty((nisotopes, n_energy))
    energy = np.empty(n_energy)

    for i, neutron_nr in enumerate(all_neutron_numbers):
        the_isotope = d_frame_2.neutron_number == neutron_nr
        isodf = d_frame_2[the_isotope]
        all_curves[i, :] = isodf.strength_function
        energy = isodf.energy

    return all_curves, all_neutron_numbers, energy


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
    all_temperatures = np.sort(df3.temperature.unique()).tolist()
    all_temperatures.remove(0.5)

    # plot
    fig, axarr = pyplot.subplots(len(all_temperatures), 1, constrained_layout=True)
    axes = {str(temp): ax for temp, ax in zip(np.flip(all_temperatures), axarr.flat)}

    mappable = None
    for temp in all_temperatures:
        ax = axes[str(temp)]

        y, neutron_numbers, x = all_strength_functions_for_temperature(temp, df3)
        nn = np.append(neutron_numbers - 1, neutron_numbers[-1] + 1)

        mappable = ax.pcolormesh(
            x,
            nn,
            y,
            norm=colors.LogNorm(),
            vmin=0.05,
            vmax=4.5,
            cmap="turbo",
            linewidth=0,
            rasterized=True,
        )  # norm=colors.LogNorm(vmin=0.2, vmax=5.0)
        ax.annotate(
            s=f"$T = {temp}$ MeV", xy=(0.70, 0.68), xycoords="axes fraction", color="b"
        )
        for N in neutron_numbers:
            ax.annotate(
                s=str(N), xy=(29, N - 0.9), xycoords="data", color="w", fontsize=7
            )

        for N in neutron_numbers[:-1]:
            ax.axhline(N + 1, color="w", lw=0.2)

    cb = fig.colorbar(mappable, ax=axarr.flat, location="top", shrink=1.0, aspect=30)
    cb.outline.set_visible(False)
    cb.set_label(r"$R$ [e${}^{2}$fm${}^{2}$/MeV]")
    cb.ax.xaxis.set_minor_locator(ticker.NullLocator())
    cb.ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    cb.ax.xaxis.set_major_locator(
        ticker.FixedLocator([0.1, 0.2, 0.4, 0.6, 1.0, 2.0, 4.0])
    )  # np.around(np.logspace(-1.30103, 0.60206, 10), decimals=1)
    cb.ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

    for ax in axarr[:-1].flat:
        ax.set_xticklabels([])

    for ax in axarr.flat:
        ax.set_xlim(0.1, 30)
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

    axes["0.0"].set_xlabel(r"$E$ [MeV]", labelpad=-0.5)

    fig.set_size_inches(width, 1.4 * width)
    fig.savefig("colormesh.pdf")  # facecolor='C7'
