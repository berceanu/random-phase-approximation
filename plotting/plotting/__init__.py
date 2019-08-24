"""
Package containing plotting customizations and routines.
"""
import matplotlib as mpl

mpl.use("TkAgg")

import pkg_resources  # noqa: E402
from matplotlib import pyplot  # noqa: E402
from plotting.style import (
    colourWheel,
    dashesStyles,
    width,
    height,
    golden_ratio,
)  # NOQA: F401
from plotting.turbo_colormap import mpl_turbo_data  # NOQA: F401

# Load style file
style_path = pkg_resources.resource_filename(
    "plotting", "data/paper_double_fig.mplstyle"
)
pyplot.style.use(style_path)

# use nice LaTeX fonts
pyplot.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{cmbright}",
        ],
    }
)

# register the "turbo" colormap
pyplot.register_cmap(name="turbo", data=mpl_turbo_data, lut=256)
