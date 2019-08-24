import pkg_resources
import pathlib

import numpy as np
import pandas as pd

from matplotlib import pyplot, ticker, colors

# from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

from dataframe import mpl_turbo_data

pyplot.register_cmap(name="turbo", data=mpl_turbo_data, lut=256)

# mpl.use("pdf")
# mpl.use('agg')
mpl.use("Qt5Agg")
print(mpl.get_backend())

# Load style file
pyplot.style.use("PaperDoubleFig.mplstyle")

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

# Make some style choices for plotting
colourWheel = [
    "#329932",
    "#ff6961",
    "b",
    "#6a3d9a",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#6a3d9a",
    "#b15928",
    "#67001f",
    "#b2182b",
    "#d6604d",
    "#f4a582",
    "#fddbc7",
    "#f7f7f7",
    "#d1e5f0",
    "#92c5de",
    "#4393c3",
    "#2166ac",
    "#053061",
]

dashesStyles = [[3, 1], [1000, 1], [2, 1, 10, 1], [4, 1, 1, 1, 1, 1]]

aps_column_width = 3.404  # inches
golden_ratio = 1.618

width = aps_column_width
height = aps_column_width / golden_ratio

screen_dpi = 123  # pixels / inch

df_path = pathlib.Path(
    pkg_resources.resource_filename("dataframe", "data/dataframe.pkl")
)
df = pd.read_pickle(df_path)

lower = df["energy"] >= 0.1
upper = df["energy"] <= 30
both = lower & upper
df2 = df[both]

df3 = df2.sort_values(by=["neutron_number", "energy"], ascending=[True, True])

df4 = df3[df3["temperature"] == 2.0]

pyplot.close("all")
fig, ax = pyplot.subplots()
fig.subplots_adjust(left=0.09, bottom=0.14, right=0.97, top=0.97)
dy = 0
for j, neutron_number in enumerate(df4.neutron_number.unique()):
    isotope = df4.neutron_number == neutron_number
    mydf = df4[isotope]
    ax.plot(
        mydf.energy,
        mydf.strength_function + j * dy,
        color=colourWheel[j % len(colourWheel)],
        linestyle="-",
        dashes=dashesStyles[j % len(dashesStyles)],
        label=neutron_number,
    )

ax.set_ylabel(r"$R$ [e${}^{2}$fm${}^{2}$/MeV]", labelpad=-2)
ax.set_xlabel(r"$E$ [MeV]", labelpad=--0.5)
ax.set_xlim(0.1, 30)
ax.set_ylim(0, 10)

ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.yaxis.major.formatter._useMathText = True
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
# ax.yaxis.set_label_coords(0.63,1.01)
ax.legend(loc="upper left", ncol=2, handlelength=1)
ax.annotate(s=r"$T = 0$", xy=(0.7, 0.8), xycoords="axes fraction")

fig.set_size_inches(width, height)
pyplot.show()
# fig.savefig("plot.pdf")  # facecolor='C7'

df5 = df4[df4.neutron_number == 76]
nenergy = df5.energy.size
print(f"Number of energy grid points: {nenergy}")

x = np.empty(nenergy)
x = df5.energy

all_temperatures = np.sort(df3.temperature.unique())
print(f"All temperatures: {all_temperatures}")


def all_strength_functions_for_temperature(temperature, df, nenergy):

    all_neutron_numbers = df.neutron_number.unique()
    nisotopes = len(all_neutron_numbers)

    df2 = df[df["temperature"] == temperature]

    y = np.empty((nisotopes, nenergy))

    for j, neutron_number in enumerate(all_neutron_numbers):
        isotope = df2.neutron_number == neutron_number
        isodf = df2[isotope]
        y[j, :] = isodf.strength_function
    return y, all_neutron_numbers


y, neutron_numbers = all_strength_functions_for_temperature(0.0, df3, nenergy)
nn = np.append(neutron_numbers - 1, neutron_numbers[-1] + 1)

# pyplot.close("all")
fig, axarr = pyplot.subplots(4, 1, constrained_layout=True)
axes = {str(temp): ax for temp, ax in zip(np.flip(all_temperatures), axarr.flat)}

for temp in all_temperatures:
    ax = axes[str(temp)]

    y, neutron_numbers = all_strength_functions_for_temperature(temp, df3, nenergy)
    nn = np.append(neutron_numbers - 1, neutron_numbers[-1] + 1)

    mappable = ax.pcolormesh(
        x, nn, y, norm=colors.LogNorm(), vmin=0.05, vmax=4.5, cmap="turbo"
    )  # norm=colors.LogNorm(vmin=0.2, vmax=5.0)
    ax.annotate(
        s=f"$T = {temp}$",
        xy=(0.75, 0.68),
        xycoords="axes fraction",
        color="b",
        fontsize=10,
    )
    for N in neutron_numbers:
        ax.annotate(s=str(N), xy=(29, N - 0.9), xycoords="data", color="w", fontsize=7)

    for N in neutron_numbers[:-1]:
        ax.axhline(N + 1, color="w", lw=0.5)


cb = fig.colorbar(mappable, ax=axarr.flat, location="top", shrink=1.0, aspect=30)
cb.outline.set_visible(False)
cb.set_label(r"$R$ [e${}^{2}$fm${}^{2}$/MeV]")
cb.ax.xaxis.set_minor_locator(ticker.NullLocator())
cb.ax.xaxis.set_minor_formatter(ticker.NullFormatter())
cb.ax.xaxis.set_major_locator(
    ticker.FixedLocator(np.around(np.logspace(-1.30103, 0.60206, 10), decimals=1))
)
cb.ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

for ax in axarr[:-1].flat:
    ax.set_xticklabels([])

for ax in axarr.flat:
    ax.set_xlim(0.1, 30)
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_formatter(ticker.NullFormatter())

    ax.xaxis.set_major_locator(ticker.FixedLocator([5, 10, 15, 20, 25]))

    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

#     ax.xaxis.tick_bottom()

axes["0.0"].set_xlabel(r"$E$ [MeV]", labelpad=-0.5)

fig.set_size_inches(width, width * golden_ratio)
# fig.savefig("colormesh.pdf")  # facecolor='C7'

pyplot.show()
