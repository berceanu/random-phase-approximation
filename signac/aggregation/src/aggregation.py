#!/usr/bin/env python3
"""This module plots the dipole strengths for a single nucleus at various temperatures."""

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
import logging
logger = logging.getLogger(__name__)
import argparse
import itertools as it


line_colors = ['C0', 'C1', 'C2', 'C3']
line_styles = ['-', '--', ':', '-.']

cyl = cycler(c=line_colors) + cycler(ls=line_styles)
vert_cyl = cycler(colors=line_colors) + cycler(linestyles=line_styles)

loop_cy_iter = cyl()
vert_loop_cy_iter = vert_cyl()

STYLE = defaultdict(lambda : next(loop_cy_iter))
vert_STYLE = defaultdict(lambda : next(vert_loop_cy_iter))


def out_file_plot(job, temp, skalvec, lorexc, ax=None,
                    code_mapping=code_api.NameMapping(),
                    minEnergy=0., maxEnergy=30., # MeV
                    ):
    fn = job.fn(code_mapping.out_file(temp, skalvec, lorexc))

    df = pd.read_csv(fn, delim_whitespace=True, comment='#', skip_blank_lines=True,
                header=None, names=['energy', 'transition_strength'])

    df = df[(df.energy >= minEnergy) & (df.energy <= maxEnergy)] # MeV

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


def main_aggregation(args):
    pass

def store_aggregated_results(Z, N, rpa_jobs,
                                     plot_type=['excitation', 'lorentzian'],
                                     args=None,
                                     ): # command-line arguments

    nucleus = util.get_nucleus(proton_number=Z, neutron_number=N)    

    is_finite = lambda job: 'finite' if job.sp.temperature > 0 else 'zero'
    code = code_api.NameMapping()

    if args.isoscalar:
        fig = Figure(figsize=(12, 6)) # width, height in inches
        canvas = FigureCanvas(fig)
        gs = GridSpec(2, 1)
        ax = {'isoscalar': fig.add_subplot(gs[0,0]),
              'isovector': fig.add_subplot(gs[1,0])}
        panels = ['isoscalar', 'isovector']
    else: # no isoscalar panel
        fig = Figure(figsize=(12, 5)) 
        canvas = FigureCanvas(fig)
        gs = GridSpec(1, 1)
        ax = {'isovector': fig.add_subplot(gs[0,0])}
        panels = ['isovector']


    origin = {}
    for job in sorted(rpa_jobs, key=lambda job: job.sp.temperature):
        logger.info("plotting %s with T = %s MeV" % (str(job), job.sp.temperature))
        origin[f"T = {job.sp.temperature} MeV".replace('.', '_')] = str(job)
        for skalvec in panels:
            for sp in "top", "bottom", "right":
                ax[skalvec].spines[sp].set_visible(False)
            ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
            ax[skalvec].set_title(skalvec)
            for lorexc in plot_type:
                _ = out_file_plot(job=job, ax=ax[skalvec], temp=is_finite(job), 
                                        skalvec=skalvec, lorexc=lorexc, code_mapping=code,
                                        minEnergy=args.minEnergy, maxEnergy=args.maxEnergy,
                                    )

    ax['isovector'].legend()
    ax['isovector'].set(xlabel="E (MeV)")
    if args.isoscalar:
        fig.subplots_adjust(hspace=0.3)

    # here job is the last one in rpa_jobs
    element, mass = util.split_element_mass(job)
    fig.suptitle(fr"Transition strength distribution of ${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")





def main_groupby(args):
    rpa = sg.get_project(root='../')
    aggregation = sg.get_project(root='./')
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("aggregation project: %s" % aggregation.root_directory())

    ZN = ('proton_number', 'neutron_number')
    for key, group in rpa.groupby(ZN):
        logger.info("(Z, N) =  (%s, %s)" % key)

        gr1, gr2 = it.tee(group)

        statepoints = []
        for job in gr1:
            sp = copy.deepcopy(job.sp())
            # for k in keys:
            #     sp.pop(k, None)
            statepoints.append(sp)
        const_sp = dict(set.intersection(*(set(d.items()) for d in statepoints)))
        print(f"{ZN} = {key}, sp = {const_sp}")
        # do something with gr2

        # store_aggregated_results(*key, group, 
                                    # plot_type=plot_type, args=args)

        with aggregation.open_job(const_sp) as agg_job: # .init() implicitly called here
            # agg_job.doc['nucleus'] = nucleus
            # agg_job.doc.update(origin)

            # save figure to disk in agg_job's folder
            # canvas.print_png(agg_job.fn('iso_all_temp_all.png'))
            logger.info("wrote %s" % agg_job.fn('iso_all_temp_all.png'))




def main():
    parser = argparse.ArgumentParser(
        description="this script plots the aggregated transition strengths "
                    "for each nucleus over all temperatures.")
    parser.add_argument(
        '--vlines',
        action='store_true',
        help="Add vertical lines at transition energies to plots.")
    parser.add_argument(
        '--isoscalar',
        action='store_true',
        help="Plot isoscalar component as well.")
    parser.add_argument(
        '--minEnergy',
        type=float,
        default=0.,
        help="Lower energy threshold for spectrum, in MeV.")
    parser.add_argument(
        '--maxEnergy',
        type=float,
        default=30.,
        help="Upper energy threshold for spectrum, in MeV.")

    args = parser.parse_args() # load command line args

    plot_type = ['lorentzian']
    if args.vlines:
        plot_type.append('excitation')

    main_groupby(args)

if __name__ == '__main__':
    logging.basicConfig(
        filename='aggregation.log',
        format='%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info('==RUN STARTED==')
    main()
    logger.info('==RUN FINISHED==')