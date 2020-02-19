"""
Package containing plotting customizations and routines.
"""
import pkg_resources  # NOQA: E402
from matplotlib import pyplot  # NOQA: E402
from figstyle.style import colourWheel, dashesStyles, width, golden_ratio  # NOQA: F401
from figstyle.turbo_colormap import mpl_turbo_data  # NOQA: F401

# Load style file
style_path = pkg_resources.resource_filename(
    "figstyle", "data/paper_double_fig.mplstyle"
)
pyplot.style.use(style_path)

# register the "turbo" colormap
pyplot.register_cmap(name="turbo", data=mpl_turbo_data, lut=256)
