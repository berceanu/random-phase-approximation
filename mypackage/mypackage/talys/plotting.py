"""
This module contains functions for plotting TALYS results.
"""
import logging

from matplotlib.ticker import MaxNLocator

logger = logging.getLogger(__name__)


def plot_cross_section(
    ax,
    horiz_data,
    vert_data,
    label,
    color,
    text=None,
    linestyle="-",
    title=None,
    legend=True,
):
    ax.plot(horiz_data, vert_data, color=color, linestyle=linestyle, label=label)

    ax.set(ylabel=r"Cross-Section [mb]", xlabel=r"$E_n$ [MeV]")
    ax.set_yscale("log")
    ax.set_xscale("log")

    if text is not None:
        ax.text(0.7, 0.95, text, transform=ax.transAxes)
    if legend:
        ax.legend(loc="lower left")

    if title is not None:
        ax.title.set_text(title)


def plot_capture_rate_vs_temp(
    ax, horiz_data, vert_data, label, color="black", title=None
):
    ax.plot(horiz_data, vert_data, "-o", color=color, label=label)

    ax.set(
        ylabel=r"Neutron Capture Rate [s${}^{-1}$cm${}^{3}$mol${}^{-1}$]",
        xlabel=r"$T_9$ [MeV]",
    )
    ax.ticklabel_format(
        axis="y",
        style="scientific",
        scilimits=(0, 0),
        useOffset=False,
        useMathText=True,
    )

    if title is not None:
        ax.title.set_text(title)

    ax.legend(loc="best")


def plot_capture_rate_vs_mass(
    ax, horiz_data, vert_data, label, color="black", title=None
):
    ax.plot(horiz_data, vert_data, "-o", color=color, label=label)

    ax.set(
        ylabel=r"Neutron Capture Rate [s${}^{-1}$cm${}^{3}$mol${}^{-1}$]", xlabel=r"A"
    )

    # ax.ticklabel_format(
    #     axis="y",
    #     style="scientific",
    #     scilimits=(0, 0),
    #     useOffset=False,
    #     useMathText=True,
    # )
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    if title is not None:
        ax.title.set_text(title)

    ax.legend(loc="best")


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
