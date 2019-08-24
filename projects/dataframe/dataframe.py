# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Enabling the `widget` backend.
# This requires jupyter-matplotlib a.k.a. ipympl.
# ipympl can be install via pip or conda.
# %matplotlib widget


import pandas as pd

import warnings

import seaborn as sns
from matplotlib import pyplot

warnings.filterwarnings("ignore", message="Tight layout not applied")

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

pal = sns.cubehelix_palette(n_colors=11, rot=-0.25, light=0.7)


def ridgeplot(df, temperature=0.0):
    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
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

    df2 = df.sort_values(by=["neutron_number", "energy"], ascending=[True, True])

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
        height=0.5,
        palette=pal,
    )

    # Draw the densities in a few steps
    g.map(pyplot.plot, "energy", "strength_function", clip_on=False, alpha=1, lw=1.5)
    g.map(pyplot.fill_between, "energy", "strength_function")
    g.map(pyplot.plot, "energy", "strength_function", clip_on=False, color="w", lw=2)
    g.map(pyplot.axhline, y=0, lw=2, clip_on=False)

    g.map(label, "energy")
    g.set_xlabels(r"$E$ (MeV)")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.93)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)


df = pd.read_pickle("../dataframe.pkl")

lower = df["energy"] >= 0.1
upper = df["energy"] <= 30
both = lower & upper
df_final = df[both]


ridgeplot(df_final, temperature=0.0)

ridgeplot(df_final, temperature=0.5)

ridgeplot(df_final, temperature=1.0)

ridgeplot(df_final, temperature=2.0)
