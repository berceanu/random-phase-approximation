"""
This module contains functions for loading/postprocessing TALYS data.
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def read_cross_section(fn, residual_production=False):
    if residual_production:
        df = pd.read_csv(
            fn, sep=r"\s+", header=None, comment="#", names=["energy", "xs"]
        )
    else:
        df = (
            pd.read_csv(
                fn,
                sep=r"\s+",
                header=None,
                comment="#",
                names=[
                    "E",
                    "xs",
                    "gamma_xs",
                    "res_prod_xs",
                    "direct",
                    "preequilibrium",
                    "compound",
                ],
            )
            .drop(["xs", "gamma_xs", "res_prod_xs", "direct", "preequilibrium"], axis=1)
            .rename(columns={"E": "energy", "compound": "xs"})
        )
    return df


def read_astrorate(fn):
    df = pd.read_csv(fn, sep=r"\s+", skiprows=2, header=None)
    # read first two lines
    with open(fn, "r") as f:
        _, line2 = f.readline(), f.readline()
    df.columns = line2.lstrip("#").strip().split()
    return df


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
