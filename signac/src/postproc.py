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
import mypackage.code_api as code_api
import matplotlib.pyplot as plt
from cycler import cycler
from collections import defaultdict
from matplotlib.gridspec import GridSpec
import mypackage.util as util

# %%
code = code_api.NameMapping()

# %%
project = sg.get_project()
project

# %%
is_finite = lambda job: 'finite' if job.sp.temperature > 0 else 'zero'

# %%
line_colors = ['C0', 'C1', 'C2', 'C3']
line_styles = ['-', '--', ':', '-.']

cyl = cycler(c=line_colors) + cycler(ls=line_styles)
vert_cyl = cycler(colors=line_colors) + cycler(linestyles=line_styles)

loop_cy_iter = cyl()
vert_loop_cy_iter = vert_cyl()

STYLE = defaultdict(lambda : next(loop_cy_iter))
vert_STYLE = defaultdict(lambda : next(vert_loop_cy_iter))

# %%
def out_file_plot(job, temp, skalvec, lorexc, ax=None, code_mapping=code_api.NameMapping()):
    fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))

    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                header=None, names=['energy', 'transition_strength'])

    df = df[df.energy < 30] # MeV

    if ax:
        if lorexc == 'excitation':
            ax.vlines(df.energy, 0., df.transition_strength, label='_nolegend_',
                          **vert_STYLE[str(job.sp.temperature)])
        elif lorexc == 'lorentzian':
            ax.plot(df.energy, df.transition_strength, label=f"T = {job.sp.temperature} MeV",
                        **STYLE[str(job.sp.temperature)])
        else:
            raise ValueError
        
    return df

# %%
# everything but the temperature
filter = dict(proton_number=50, neutron_number=82,
                 angular_momentum=1, parity="-", transition_energy=0.42)

selection = project.find_jobs(filter)

assert len(selection)

fig = plt.figure(figsize=(10, 6))

gs = GridSpec(2, 1)
ax = {'isoscalar': fig.add_subplot(gs[0,0]),
      'isovector': fig.add_subplot(gs[1,0])}

for job in sorted(selection, key=lambda job: job.sp.temperature):    
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

element, mass = util.split_element_mass(job)
fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

# %%
for key, group in project.groupby(('proton_number', 'neutron_number')):
    fig = plt.figure(figsize=(10, 6))

    gs = GridSpec(2, 1)
    ax = {'isoscalar': fig.add_subplot(gs[0,0]),
          'isovector': fig.add_subplot(gs[1,0])}
    for job in sorted(group, key=lambda job: job.sp.temperature):
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

    element, mass = util.split_element_mass(job)
    fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

# %%



# %%



# %%
filter.update(temperature=2.0)
one_job = project.find_jobs(filter)
assert len(one_job) == 1
job = next(iter(one_job))

df = out_file_plot(job=job, temp=is_finite(job), skalvec='isovector', lorexc='excitation', code_mapping=code)

# %%
df.applymap('{:,.2f}'.format)[(df.energy > 3.) & (df.energy < 8.) & (df.transition_strength > .1)]

# %%
df[np.isclose(df.energy, 7.77, atol=0.01)]

# %%
# T = 0 Mev, E = 7.75 MeV


# %%
filter.update(temperature=0.0)
one_job = project.find_jobs(filter)
assert len(one_job) == 1
job = next(iter(one_job))

df = out_file_plot(job=job, temp=is_finite(job), skalvec='isovector', lorexc='excitation', code_mapping=code)

# %%
df[np.isclose(df.energy, 7.75, atol=0.01)].applymap('{:,.2f}'.format)

# %%


