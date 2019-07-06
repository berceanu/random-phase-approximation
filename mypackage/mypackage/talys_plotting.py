"""
This module contains functions for plotting TALYS results.
"""
# import pandas as pd
import logging

# from . import util

logger = logging.getLogger(__name__)


def plot_cross_section(ax, horiz_data, vert_data, label, color, text):
    ax.loglog(horiz_data, vert_data, color=color, label=label)

    ax.set(ylabel=r"Cross-Section [mb]", xlabel=r"$E_n$ [MeV]")
    ax.text(
        0.7,
        0.95,
        text,
        transform=ax.transAxes,
        # color="black",
    )
    ax.legend(loc="lower left")


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
