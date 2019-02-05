# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %autosave 0

# %%
# Enabling the `widget` backend.
# This requires jupyter-matplotlib a.k.a. ipympl.
# ipympl can be install via pip or conda.
##conda install -c conda-forge ipympl
# If using the Notebook
##conda install -c conda-forge widgetsnbextension
# https://github.com/matplotlib/jupyter-matplotlib
# %matplotlib widget

# %%
import pandas as pd
import numpy as np
import signac as sg
from modules import code_api
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
#from IPython.display import Image
import re

# %%
code = code_api.NameMapping()

# %%
project = sg.get_project()

# %%
is_finite = lambda job: 'finite' if job.sp.temperature > 0 else 'zero'

# %%
def split_element_mass(job):
    pattern = re.compile(r"([A-Z]*)(\d*)")
    element, mass_number = pattern.sub(r'\1 \2', job.sp.nucleus).split()
    element = element.title() # capitalize first letter only
    return element, mass_number

# %%
def out_file_plot(job, temp, skalvec, lorexc, ax=None, code_mapping=code_api.NameMapping()):
    STYLE = {'0.0': dict(color='dodgerblue', linestyle='solid'),
             '1.0': dict(color='lawngreen', linestyle='dashed'),
             '2.0': dict(color='firebrick', linestyle='dashdot')}

    fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))

    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                header=None, names=['energy', 'transition_strength'])

    df = df[df.energy < 30] # MeV

    if ax:
        if lorexc == 'excitation':
            ax.vlines(df.energy, 0., df.transition_strength, label='_nolegend_',
                      colors=STYLE[str(job.sp.temperature)]['color'],
                     linestyles=STYLE[str(job.sp.temperature)]['linestyle'])
        elif lorexc == 'lorentzian':
            ax.plot(df.energy, df.transition_strength, label=f"T = {job.sp.temperature} MeV",
                    color=STYLE[str(job.sp.temperature)]['color'],
                   linestyle=STYLE[str(job.sp.temperature)]['linestyle'])
        else:
            raise ValueError
        
    return df

# %%
filter = dict(nucleus="SN132", angular_momentum=1, parity="-", transition_energy=0.0)

selection = project.find_jobs(filter)

fig = plt.figure(figsize=(10, 6))
#fig = Figure(figsize=(12, 6)) 
#canvas = FigureCanvas(fig)


gs = GridSpec(2, 1)
ax = {'isoscalar': fig.add_subplot(gs[0,0]),
      'isovector': fig.add_subplot(gs[1,0])}

for job in selection:
    
    if job.sp.temperature > 0:
        temp = 'finite'
    else:
        temp = 'zero'
        
    for skalvec in 'isoscalar', 'isovector':
        for sp in ("top", "bottom", "right"):
            ax[skalvec].spines[sp].set_visible(False)
        ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
        ax[skalvec].set_title(skalvec)
        for lorexc in 'excitation', 'lorentzian':
            df = out_file_plot(job=job, ax=ax[skalvec], temp=is_finite(job), skalvec=skalvec, lorexc=lorexc, code_mapping=code)
        
    ax['isoscalar'].legend()
    ax['isovector'].set(xlabel="E (MeV)")
    fig.subplots_adjust(hspace=0.3)

    element, mass = split_element_mass(job)
    fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

#plt.show()
#fn = "iso_all.png"
#canvas.print_png(fn)
#Image(filename = fn)

# %%
filter.update(temperature=2.0)
one_job = project.find_jobs(filter)
assert len(one_job) == 1
job = next(one_job)

df = out_file_plot(job=job, temp=is_finite(job), skalvec='isovector', lorexc='excitation', code_mapping=code)

# %%
df.applymap('{:,.2f}'.format)[(df.energy > 3.) & (df.energy < 8.) & (df.transition_strength > .1)]

# %%
df[np.isclose(df.energy, 7.77, atol=0.01)]

# %%
# TODO T = 0 Mev, E = 7.75 MeV

