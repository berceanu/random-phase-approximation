import pathlib
import warnings

import pandas as pd
import pkg_resources
import seaborn as sns
from matplotlib import pyplot
import matplotlib as mpl

warnings.filterwarnings("ignore", message="Tight layout not applied")

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

pal = sns.cubehelix_palette(n_colors=11, rot=-0.25, light=0.7)
mpl.use("Qt5Agg")


# https://seaborn.pydata.org/examples/kde_ridgeplot.html
def ridge_plot(d_frame, temperature):
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

    df2 = d_frame.sort_values(by=["neutron_number", "energy"], ascending=[True, True])

    # filter by temperature
    df3 = df2[df2["temperature"] == temperature]
    print(f"Selected temperature is {temperature} MeV.")

    # Initialize the FacetGrid object
    # https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
    g = sns.FacetGrid(
        df3,
        row="neutron_number",
        hue="neutron_number",
        aspect=15,
        height=3.3 / 15,
        palette=pal,
    )

    # Draw the densities in a few steps
    g.map(pyplot.plot, "energy", "strength_function", clip_on=False, alpha=1, lw=1.5)
    g.map(pyplot.fill_between, "energy", "strength_function")
    g.map(pyplot.plot, "energy", "strength_function", clip_on=False, color="w", lw=2)
    g.map(pyplot.axhline, y=0, lw=2, clip_on=False)

    g.map(set_label, "energy")
    g.set_xlabels(r"$E$ (MeV)")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.93)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)

    pyplot.show()


if __name__ == "__main__":
    df_path = pathlib.Path(pkg_resources.resource_filename("dataframe", "data"))

    df = pd.read_pickle(df_path / "dataframe.pkl")

    lower = df["energy"] >= 0.1
    upper = df["energy"] <= 30
    both = lower & upper
    df_final = df[both]

    ridge_plot(df_final, temperature=0.0)
    ridge_plot(df_final, temperature=0.5)
    ridge_plot(df_final, temperature=1.0)
    ridge_plot(df_final, temperature=2.0)
