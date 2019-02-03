#%%
import pandas as pd
import numpy as np
import signac as sg
from src.modules import code_api
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from IPython.display import Image
from IPython.core.display import HTML
import re


#%%
code = code_api.NameMapping()



#%%
def split_element_mass(job):
    pattern = re.compile(r"([A-Z]*)(\d*)")
    element, mass_number = pattern.sub(r'\1 \2', job.sp.nucleus).split()
    element = element.title() # capitalize first letter only
    return element, mass_number

#%%
def plot_job(job, ax, code_mapping=code_api.NameMapping()):
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
    df = df[(df.energy < 30)]

    ax.plot(df.energy, df.transition_strength, label=f"T = {job.sp.temperature} MeV",
                            color=STYLE[str(job.sp.temperature)]['color'],
                            linestyle=STYLE[str(job.sp.temperature)]['linestyle'])

    ax.set(
        xlim=[0, 30],
        ylim=[0, 4.5],
        ylabel=r"$R \; (e^2fm^2/MeV)$",
        xlabel="E (MeV)",
    )

    ax.legend()
    # ax.grid()



#%%
project = sg.get_project()
filter = dict(nucleus="NI62", angular_momentum=1, parity="-", transition_energy=9.78)
selection = project.find_jobs(filter)

fig = Figure(figsize=(10, 6)) 
canvas = FigureCanvas(fig)    
ax = fig.add_subplot(111)  

for T, group in selection.groupby('temperature'):
    print(f"T = {T} MeV")
    for job in group:
        print(f"job id: {job._id}")
        plot_job(job, ax, code_mapping=code)

element, mass = split_element_mass(job)
fig.suptitle(fr"${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

fn = f"{element}{mass}.png"
canvas.print_png(fn)
fig.clear()
Image(filename = fn)


# for kT, group in project.groupby('kT'):
#     print(kT, np.mean([job.sp.pressure] for job in group])