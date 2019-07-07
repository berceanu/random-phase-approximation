"""
This module contains functions for plotting TALYS results.
"""
# import pandas as pd
import logging

# from . import util

logger = logging.getLogger(__name__)


# todo refactor
def plot_cross_section(ax, horiz_data, vert_data, label, color, text, linestyle="-"):
    ax.plot(horiz_data, vert_data, color=color, linestyle=linestyle, label=label)

    ax.set(ylabel=r"Cross-Section [mb]", xlabel=r"$E_n$ [MeV]")
    ax.set_yscale("log")
    ax.set_xscale("log")

    ax.text(0.7, 0.95, text, transform=ax.transAxes)
    ax.legend(loc="lower left")


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


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
