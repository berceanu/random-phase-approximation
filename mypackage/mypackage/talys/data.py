"""
This module contains functions for loading/postprocessing TALYS data.
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def read_cross_section(fn):
    df = pd.read_csv(fn, sep=r"\s+", header=None, comment="#", names=["energy", "xs"])
    return df


def read_astrorate(fn):
    df = pd.read_csv(fn, sep=r"\s+", comment="#")
    return df


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
