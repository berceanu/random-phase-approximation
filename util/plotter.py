#!/usr/bin/env python3

import os    
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

#TODO: 
# (1) mpl.rc params
# (2) customization via https://www.labri.fr/perso/nrougier/teaching/matplotlib
# (3) update snippers
# (4) extract data from Yifei paper
# (5) create regression test within 3% margin

def main():
    # define working folders
    base_path = "/home/berceanu/Development/rpa"
    subfolders = [os.path.join(parent, child) for parent in ["zero_temperature", "finite_temperature"] for child in ["ground_state", "excited_states"]]
    _, ztes_dir, _, ftes_dir = [os.path.join(base_path, subf) for subf in subfolders]

    fname_zt = os.path.join(ztes_dir, "lorvec.out")
    fname_ft = os.path.join(ftes_dir, "lorvec.out")

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
    
    canvas.print_figure("lorentzian.png")

if __name__ == '__main__':
    main()