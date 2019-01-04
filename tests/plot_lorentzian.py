#!/usr/bin/env python3

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

def main():
    fname_zt = "out/ztes_lorvec.out"
    fname_ft = "out/ftes_lorvec.out"

    arr_zt = np.loadtxt(fname_zt)
    arr_ft = np.loadtxt(fname_ft)

    h_axis_zt = arr_zt[:,0]
    arr1d_zt = arr_zt[:,1]

    h_axis_ft =  arr_ft[:,0] #h_axis_zt
    arr1d_ft = arr_ft[:,1]   #1/5 * (np.random.random_sample(arr1d_zt.shape) + 5)

    fig = Figure(figsize=(10, 6))
    canvas = FigureCanvas(fig)
    
    ax = fig.add_subplot(111)
    ax.plot(h_axis_zt, arr1d_zt, color="black", label="T = 0.0 MeV")
    ax.plot(h_axis_ft, arr1d_ft, color="red", linestyle=":", label="T = 2.0 MeV")  

    # ax.scatter(h_axis_ft, arr1d_ft, color="red", label="T = 2.0 MeV")
    # ax.vlines(h_axis_ft, 0, arr1d_ft, colors="red",  linestyles='dotted', label="T = 2.0 MeV")

    # ax.grid()
    ax.set(
        xlim=[0, 30],
        ylim=[0, 4.5],
        ylabel=r"$%s \;(e^2fm^2/MeV)$" % "R",
        xlabel="E (MeV)",
    )
    ax.text(0.02, 0.95, "", transform=ax.transAxes, color="firebrick")
    ax.legend()
    ax.set_title(r"${}^{62} Ni \; 1^{-}$")
    
    canvas.print_figure("out/lorentzian.png")

if __name__ == '__main__':
    main()
