from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.gridspec import GridSpec
import pandas as pd
import random
import re
import signac as sg
import mypackage.code_api as code_api


rpa = sg.get_project(root='../')
aggregation = sg.get_project()

# everything but the temperature
filter = dict(proton_number=50, neutron_number=82,
                angular_momentum=1, parity="-", transition_energy=0.42)

selection = rpa.find_jobs(filter)

code = code_api.NameMapping()

is_finite = lambda job: 'finite' if job.sp.temperature > 0 else 'zero'

def split_element_mass(job):
    pattern = re.compile(r"([A-Z]*)(\d*)")
    element, mass_number = pattern.sub(r'\1 \2', job.doc.nucleus).split()
    element = element.title() # capitalize first letter only
    return element, mass_number

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


def store_aggregated_results(rpa_jobs, **statepoint):
    fig = Figure(figsize=(10, 6)) 
    canvas = FigureCanvas(fig)


    gs = GridSpec(2, 1)
    ax = {'isoscalar': fig.add_subplot(gs[0,0]),
        'isovector': fig.add_subplot(gs[1,0])}

    for job in rpa_jobs:
        for skalvec in 'isoscalar', 'isovector':
            for sp in "top", "bottom", "right":
                ax[skalvec].spines[sp].set_visible(False)
            ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
            ax[skalvec].set_title(skalvec)
            for lorexc in 'excitation', 'lorentzian':
                _ = out_file_plot(job=job, ax=ax[skalvec], temp=is_finite(job), skalvec=skalvec, lorexc=lorexc, code_mapping=code)

    ax['isoscalar'].legend()
    ax['isovector'].set(xlabel="E (MeV)")
    fig.subplots_adjust(hspace=0.3)

    # here job is the last one in rpa_jobs
    element, mass = split_element_mass(job)
    fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

    with aggregation.open_job(dict(**statepoint)) as agg_job: # .init() implicitly called here
        agg_job.doc.setdefault('origin', [str(job) for job in rpa_jobs])
        # save figure to disk in agg_job's folder
        canvas.print_png(agg_job.fn('iso_all_temp_all.png'))


store_aggregated_results(selection, **filter)



