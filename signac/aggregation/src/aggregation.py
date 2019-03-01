from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.gridspec import GridSpec
from cycler import cycler
from collections import defaultdict
import pandas as pd
import random
import copy
import signac as sg
import mypackage.code_api as code_api
import mypackage.util as util


rpa = sg.get_project(root='../')
aggregation = sg.get_project(root='./')

code = code_api.NameMapping()

line_colors = ['C0', 'C1', 'C2', 'C3']
line_styles = ['-', '--', ':', '-.']

cyl = cycler(c=line_colors) + cycler(ls=line_styles)
vert_cyl = cycler(colors=line_colors) + cycler(linestyles=line_styles)

loop_cy_iter = cyl()
vert_loop_cy_iter = vert_cyl()
 
STYLE = defaultdict(lambda : next(loop_cy_iter))
vert_STYLE = defaultdict(lambda : next(vert_loop_cy_iter))


def out_file_plot(job, temp, skalvec, lorexc, ax=None, code_mapping=code_api.NameMapping()):

    fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))

    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                header=None, names=['energy', 'transition_strength'])

    df = df[df.energy < 30] # MeV

    if ax:
        if lorexc == 'excitation':
            ax.vlines(df.energy, 0., df.transition_strength,
                        label='_nolegend_',
                        **vert_STYLE[str(job.sp.temperature)])
        elif lorexc == 'lorentzian':
            ax.plot(df.energy, df.transition_strength, 
                        label=f"T = {job.sp.temperature} MeV",
                        **STYLE[str(job.sp.temperature)])
        else:
            raise ValueError
        
    return df


def store_aggregated_results(rpa_jobs):
    is_finite = lambda job: 'finite' if job.sp.temperature > 0 else 'zero'

    fig = Figure(figsize=(10, 6)) 
    canvas = FigureCanvas(fig)


    gs = GridSpec(2, 1)
    ax = {'isoscalar': fig.add_subplot(gs[0,0]),
          'isovector': fig.add_subplot(gs[1,0])}

    origin = list()
    for job in sorted(rpa_jobs, key=lambda job: job.sp.temperature):
        origin.append(str(job))
        for skalvec in 'isoscalar', 'isovector':
            for sp in "top", "bottom", "right":
                ax[skalvec].spines[sp].set_visible(False)
            ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
            ax[skalvec].set_title(skalvec)
            for lorexc in 'excitation', 'lorentzian':
                _ = out_file_plot(job=job, ax=ax[skalvec], temp=is_finite(job), 
                                    skalvec=skalvec, lorexc=lorexc, code_mapping=code)

    ax['isoscalar'].legend()
    ax['isovector'].set(xlabel="E (MeV)")
    fig.subplots_adjust(hspace=0.3)

    # here job is the last one in rpa_jobs
    element, mass = util.split_element_mass(job)
    fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

    statepoint = copy.deepcopy(job.sp())
    del statepoint['temperature']

    with aggregation.open_job(statepoint) as agg_job: # .init() implicitly called here
        agg_job.doc['origin'] = origin
        # save figure to disk in agg_job's folder
        canvas.print_png(agg_job.fn('iso_all_temp_all.png'))


for key, group in rpa.groupby(('proton_number', 'neutron_number')):
    store_aggregated_results(group)
