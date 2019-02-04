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
import pandas as pd
import numpy as np
import signac as sg
from modules import code_api
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from IPython.display import Image
import re

# %%
def split_element_mass(job):
    pattern = re.compile(r"([A-Z]*)(\d*)")
    element, mass_number = pattern.sub(r'\1 \2', job.sp.nucleus).split()
    element = element.title() # capitalize first letter only
    return element, mass_number


# %%
def plot_isovec(job, ax, code_mapping=code_api.NameMapping()):
    STYLE = {'0.0': dict(color='dodgerblue', linestyle='-'),
             '1.0': dict(color='lawngreen', linestyle='--'),
             '2.0': dict(color='firebrick', linestyle='-.')}

    if job.sp.temperature > 0:
        temp = 'finite'
    else:
        temp = 'zero'
    fn = job.fn(code_mapping.isovec_file(temp))
    #
    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                     header=None, names=['energy', 'transition_strength'])
    df = df[(df.energy < 30)] # MeV

    ax.plot(df.energy, df.transition_strength, label=f"T = {job.sp.temperature} MeV",
                            color=STYLE[str(job.sp.temperature)]['color'],
                            linestyle=STYLE[str(job.sp.temperature)]['linestyle'])
    
    return df

# %%
def plot_excvec(job, ax, code_mapping=code_api.NameMapping()):
    if job.sp.temperature > 0:
        temp = 'finite'
    else:
        temp = 'zero'
    fn = job.fn(code_mapping.excvec_file(temp))
    #
    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                     header=None, names=['energy', 'transition_strength'])
    df = df[(df.energy < 30) & (df.transition_strength > 0.1)]
    
    ax.vlines(df.energy, 0., df.transition_strength, colors='red')

    return df

# %%
code = code_api.NameMapping()
project = sg.get_project()

# %%
filter = dict(nucleus="NI62", angular_momentum=1, parity="-", transition_energy=9.78)
selection = project.find_jobs(filter)

# %%
fig = Figure(figsize=(10, 6)) 
canvas = FigureCanvas(fig)    
ax = fig.add_subplot(111)  

for T, group in selection.groupby('temperature'):
    print(f"T = {T} MeV")
    for job in group:
        print(f"job id: {job._id}")
        _ = plot_isovec(job, ax, code_mapping=code)

ax.set(
    xlim=[0, 30],
    ylim=[0, 4.5],
    ylabel=r"$R \; (e^2fm^2/MeV)$",
    xlabel="E (MeV)")

ax.legend()
ax.grid()

element, mass = split_element_mass(job)
ax.set_title(fr"${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")
fig.suptitle("Isovector dipole transition strength Lorentzian distribution")

fn = f"lorvec_T_all_{element}{mass}.png"
canvas.print_png(fn)
fig.clear()
Image(filename = fn)

# %%
one_job = project.find_jobs(dict(nucleus="NI62", angular_momentum=1, parity="-", transition_energy=9.78, temperature=2.0))
assert len(one_job) == 1

# %%
def transition_energies(df):
    for idx in df.index:
        en = df.loc[idx, 'energy']
        yield float("{0:.2f}".format(en))

# %%
fig = Figure(figsize=(10, 6)) 
canvas = FigureCanvas(fig)    
ax = fig.add_subplot(111)  
df = plot_excvec(one_job, ax, code_mapping=code)
ax.set(
    ylabel=r"$R \; (e^2fm^2/MeV)$",
    xlabel="E (MeV)")

element, mass = split_element_mass(one_job)
ax.set_title(fr"${{}}^{{{mass}}} {element} \; {one_job.sp.angular_momentum}^{{{one_job.sp.parity}}}$ at T = {one_job.sp.temperature} MeV")
fig.suptitle("Isovector dipole transition strength distribution")

fn = f"excvec_T_{one_job.sp.temperature}_{element}{mass}.png"
canvas.print_png(fn)
fig.clear()
Image(filename = fn)

#%%
tr_en = transition_energies(df)
next(tr_en)
next(tr_en)