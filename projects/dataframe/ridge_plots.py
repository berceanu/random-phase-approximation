import warnings

import matplotlib as mpl

mpl.use("TkAgg")

from dataash5 import df_path, units  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from matplotlib import pyplot  # noqa: E402

warnings.filterwarnings("ignore", message="Tight layout not applied")

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

pal = sns.cubehelix_palette(n_colors=11, rot=-0.25, light=0.7)


# https://seaborn.pydata.org/examples/kde_ridgeplot.html
def ridge_plot(d_frame, temp):
    # Define and use a simple function to label the plot in axes coordinates
    def set_label(x, color, label):
        ax = pyplot.gca()
        ax.text(
            0,
            0,
            label,
            fontweight="bold",
            color=color,
            ha="left",
            va="center",
            transform=ax.transAxes,
        )

    # Initialize the FacetGrid object
    # https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
    g = sns.FacetGrid(
        d_frame,
        row="neutron_number",
        hue="neutron_number",
        aspect=15,
        height=0.5,
        palette=pal,
    )

    # Draw the densities in a few steps
    g.map(
        pyplot.plot,
        "excitation_energy",
        "strength_function_fm",
        clip_on=False,
        alpha=1,
        lw=1.5,
    )
    g.map(pyplot.fill_between, "excitation_energy", "strength_function_fm")
    g.map(
        pyplot.plot,
        "excitation_energy",
        "strength_function_fm",
        clip_on=False,
        color="w",
        lw=2,
    )
    g.map(pyplot.axhline, y=0, lw=2, clip_on=False)

    g.map(set_label, "excitation_energy")
    g.set_xlabels("$E$ %s" % units["excitation_energy"])

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.75)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)

    g.fig.suptitle(f"T = {temp} MeV.")


if __name__ == "__main__":
    df = pd.read_hdf(df_path, "excitation_energy")

    for temperature in df["temperature"].unique():
        print(temperature)
        df2 = df.query("temperature == %s" % temperature)

        ridge_plot(df2, temperature)
