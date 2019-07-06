"""
This module contains functions for plotting TALYS results.
"""
# import pandas as pd
import logging

# from . import util

logger = logging.getLogger(__name__)


def plot_cross_section(ax, horiz_data, vert_data, label):
    ax.loglog(horiz_data, vert_data, color="black", label=label)

    ax.set(ylabel=r"Cross-Section [mb]", xlabel=r"$E_n$ [MeV]")
    # element, mass = util.split_element_mass(job)
    ax.text(
        0.7,
        0.95,
        # r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (mass - 1, element, mass, element),
        transform=ax.transAxes,
        color="black",
    )
    ax.legend(loc="lower left")


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
