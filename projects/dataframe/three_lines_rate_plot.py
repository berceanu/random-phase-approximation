import pandas as pd
from dataclasses import dataclass

from figstyle import colourWheel, dashesStyles, width, golden_ratio
from dataash5 import line_one_path, line_two_path, line_three_path, units
from matplotlib import pyplot, ticker
from pathlib import PosixPath
from typing import List


def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        if int(base) > 1:
            return r"${0} \times 10^{{{1}}}$".format(base, int(exponent))
        else:
            return r"$10^{{{0}}}$".format(int(exponent))
    else:
        return float_str


@dataclass
class CaptureRateLine:
    """Holds data for each plot line in the capture rate plot."""

    path: PosixPath
    astroT: float
    psf_temperature: float
    marker: str
    color: str
    dashes: List[int]

    def kelvin_to_electronvolt(self):
        from scipy.constants import physical_constants
        from math import log10

        kB = physical_constants["Boltzmann constant in eV/K"]
        astroT = (self.astroT * 1e9 * kB[0], "eV", 0.0)
        if log10(astroT[0]) > 5.0:
            astroT = (astroT[0] / 1e6, "MeV", 0.0)
        return astroT

    def label(self, electronvolt=True) -> str:
        decimals = 2 if self.psf_temperature else 0

        if electronvolt:
            astroT = self.kelvin_to_electronvolt()
            astroT_str = f"{astroT[0]:.2f}"
        else:
            astroT = (self.astroT * 1e9, "K", 0.0)
            astroT_str = latex_float(astroT[0])
        return fr"astroT = {astroT_str} {astroT[1]}, T = {self.psf_temperature:.{decimals}f} MeV"

    def series(self):
        ne_data = pd.read_hdf(self.path, "capture_rate").assign(
            mass_number=lambda frame: frame.proton_number + frame.neutron_number
        )
        df = ne_data.drop(columns=["proton_number"])
        table = pd.pivot_table(
            df, index=["mass_number"], values=["capture_rate"], columns=["astroT"]
        )
        series = table.loc[:, ("capture_rate", self.astroT)]
        return series

    def mass_numbers(self):
        return self.series().index.values

    def plot(self, ax):
        ax.plot(
            self.mass_numbers(),
            self.series().values,
            marker=self.marker,
            color=self.color,
            dashes=self.dashes,
            label=self.label(electronvolt=False),
        )
        ax.xaxis.set_major_locator(ticker.FixedLocator(self.mass_numbers()))
        ax.set_xlim(left=self.mass_numbers()[0] - 1, right=self.mass_numbers()[-1] + 1)

        return ax


def main():
    line_one = CaptureRateLine(
        path=line_one_path,
        astroT=0.0001,
        psf_temperature=0.0,
        marker="v",
        color=colourWheel[2],
        dashes=dashesStyles[2],
    )
    line_two = CaptureRateLine(
        path=line_two_path,
        astroT=10.0,
        psf_temperature=0.0,
        marker="^",
        color=colourWheel[1],
        dashes=dashesStyles[1],
    )
    line_three = CaptureRateLine(
        path=line_three_path,
        astroT=10.0,
        psf_temperature=0.862,
        marker="o",
        color=colourWheel[0],
        dashes=dashesStyles[0],
    )

    fig, ax = pyplot.subplots()
    fig.subplots_adjust(left=0.14, bottom=0.14, right=0.97, top=0.97)

    for line in (line_one, line_two, line_three):
        line.plot(ax)

    ax.set_yscale("log")
    ax.set_ylabel("Neutron Capture Rate %s" % units["capture_rate"])
    ax.set_xlabel("A")

    ax.legend(loc="lower left", ncol=1, handlelength=1)

    ax.annotate(s="Sn", xy=(0.1, 0.8), xycoords="axes fraction")
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    fig.set_size_inches(width, width / golden_ratio)
    fig.savefig("capture_rate_vs_A")


if __name__ == "__main__":
    main()
