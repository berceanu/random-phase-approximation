#!/usr/bin/env python3

import os
import sys
# import sh
import argparse
import subprocess
import shutil

import logging
from collections import defaultdict

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np


level = logging.INFO
format = '  %(message)s'
handlers = [logging.FileHandler('run_codes.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


CODE_NAME = { # mapping from executable names to what they represent
    'zero' : {
        'ground' : 'dish',
        'excited' : 'ztes'
    },
    'finite' : {
        'ground' : 'skys',
        'excited' : 'ftes' 
    }
}



def generate_inputs(nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78,
                    out_path=os.getcwd(), load_matrix=False):
    """Generates input files dish_dis.dat, skys_dis.dat and (z|f)tes_start.dat.

    When looking at different transition energies for the same nucleus, one can avoid re-calculating
    the matrix elements by passing load_matrix=True

    Args:
        nuleus: nucleus under consideration, eg. NI56, NI60, NI62, NI68, ZR90, SN132, PB208
        angular_momentum: 0 or 1
        parity: + or -
        temperature: eg. 2.0 (in MeV)
        transition_energy: eg. 9.78 (in MeV)
        load_matrix: flag that controls the matrix elements calculation, default is to perform the calculation

        out_path: path of folder to write files to
    
    Returns:
        Writes files to out_path (current folder by default).
    """

    actual_parity = {"-" : 0, "+": 1} # map to the parity as it is defined in the input file

    parameters = { # dictionary containing parameters for string substitution
        'transerg':transition_energy,
        'calc':int(not load_matrix), # do not calculate when you load the matrix
        'xyprint':int(not load_matrix),
        'xyread':int(load_matrix),
        'xyprobe':int(load_matrix),
        'j':angular_momentum,
        'parity':actual_parity[parity],
        'temp':temperature,
        'XA':nuleus
    }

    block = defaultdict(dict)

    # define blocks for FORTRAN input files
    block['zero']['ground'] = block['finite']['ground'] = ( # common gs block
        "l6       =   10                     ! output file\n"
        "n0f      =   20   20                ! number of oscillator shells\n"
        "b0       =   -1.6280835             ! oscillator parameter (fm**-1) of basis\n"
        "maxi     =  800                     ! maximal number of iterations\n"
        "xmix     =  0.2                     ! annealing parameter\n"
        "{XA}                                ! nucleus under consideration\n"
    ).format(**parameters) # substitute parameter values into string

    block['zero']['ground'] += ( # append to common gs block
        "Fixedgap = 00.000    00.000         ! Frozen Gapparmeter for neutr. and proton\n"
        "GA       = 00.000    00.000         ! Pairing-Constants GG = GA/A\n"
        "Init.Gap = 01.000    01.000         ! Initial values for the Gap parameters\n"
        "ivpair   =   1                      ! pair. ME: 0 read, 1 calc. 2 only calc.\n"
        "vfac     =  1.15                    ! vpair multiplication\n"
        "blocking:   0  2  1  1              ! Blocking neutrons: y/n, j, ip, nr\n"
        "blocking:   0  0  0  0              ! Blocking protons:  y/n, j, ip, nr\n"
    )

    block['finite']['ground'] += ( # append to common gs block
        "Delta    =  0.000   0.000           ! Gapparameter for neutrons and  protons\n"
        "temp     =  {temp}                  ! temperature\n"
        "filename =  T0__\n"
    ).format(**parameters)

    # define block for C++ input files
    block['zero']['excited'] = block['finite']['excited'] = ( # common excited state block
        "j          =   {j}                  ! resulting j of ph-pairs\n"
        "parity     =   {parity}             ! parity of ph-pairs 1:+ 0:-\n"
        "ediffmaxu  =   200.0                ! maximal excitation-energy particles\n"
        "ediffmaxd  =   2000.0               ! maximal excitation-energy a-p\n"
        "calc       =   {calc}               ! 1:calc mat and exc. 0:only exc.\n"
        "xyprint    =   {xyprint}            ! saves xy-matrices on disk 1:yes 0:no\n"
        "lorchange  =   0                    ! 1:only changing lorentz-curves\n"
        "lorswidth  =   1.0                  ! width of isoscalar lorentz-curve\n"
        "lorvwidth  =   1.0                  ! width of isovector lorentz-curve\n"
        "hlorswidth =   1.0                  ! width of isoscalar hartree-lorentz-curve\n"
        "hlorvwidth =   1.0                  ! width of isovector hartree-lorentz-curve\n"
        "hartree    =   0                    ! solution also without interact.1:yes\n"
        "matprint   =   1                    ! prints out RPA ascii-matrix yes:1no:0\n"
        "xyread     =   {xyread}             ! x- and y read in for further calc.\n"
        "xyprobe    =   {xyprobe}            ! making rpa-probe 1:yes 0:no\n"
        "exccalc    =   1                    ! only calculating exc 1:yes 0:no\n"
        "transdens  =   0                    ! calculate trans-dens1:yes0:no\n"
        "transiso   =   0                    ! isosc:0 isovec:1 for tr-dens\n"
        "transerg   =   {transerg}           ! energy for tr-dens, specify 2 digits\n"
        "tc_cur     =   0                    ! calculate transition-currents 1:yes 0:no\n"
        "tc_iso     =   1                    ! isoscalar:0 isovector:1 for tr-cur\n"
        "tc_erg     =   12.36                ! energy for tr-curr, specify 2 digits\n"
        "qptresh    =   0.01                 ! for lower occ inqp1noqp2-qp1pairs\n"
        "respair    =   1                    ! 1:pairing in residual inter. 0:no\n"
    ).format(**parameters)

    def write_params_to(fname, block_to_write):
        fpath = os.path.join(out_path, fname)
        with open(fpath, "w") as f:
            f.write(block_to_write)
        logging.info("Wrote {}.".format(fpath))
    
    for temp in ('zero', 'finite'): # create input files
        for state, suffix in zip(('ground', 'excited'), ("_dis.dat", "_start.dat")):
            write_params_to(CODE_NAME[temp][state] + suffix, block[temp][state])

    logging.info('Generated all input files.')

    return


def run_executables(exenames=['dish','skys','ztes','ftes'], out_path=os.getcwd(), exepath='../bin'):
    """Run the executable names in the list, redirecting their outputs to files"""

    for f in exenames:
        program=os.path.join(exepath, f)
        path=out_path
        stdout_file = os.path.join(out_path,f+"_stdout.txt")
        stderr_file = os.path.join(out_path,f+"_stderr.txt")
        cmd = f"{program} {path} > {stdout_file} 2> {stderr_file}"
        logging.info(cmd)
        subprocess.run(cmd, shell=True).returncode

        logging.info(f"Finished running {f}.")
    
    logging.info('Finished running all executables.')
    
    return


def plot_lorvec(workspace=os.getcwd()):
    plotparams = {
        'zero' : {'color':'black', 'label':'T = 0.0 MeV'},
        'finite' : {'color':'red', 'linestyle':':', 'label':'T = 2.0 MeV'}
    }

    for temp in ('zero', 'finite'):
        fpath = os.path.join(workspace, CODE_NAME[temp]['excited'] + "_lorvec.out")
        if not os.path.isfile(fpath):
            sys.exit(f"{fpath} not found, exiting.")

        arr = np.loadtxt(fpath)
        h_axis = arr[:,0]
        arr1d = arr[:,1]

        fig = Figure(figsize=(10, 6))
        canvas = FigureCanvas(fig)
    
        ax = fig.add_subplot(111)
        ax.plot(h_axis, arr1d, **plotparams[temp])

        ax.grid()
        ax.set(
            xlim=[0, 30],
            ylim=[0, 4.5],
            ylabel=r"$%s \;(e^2fm^2/MeV)$" % "R",
            xlabel="E (MeV)",
        )
        ax.text(0.02, 0.95, "", transform=ax.transAxes, color="firebrick")
        ax.legend()
        ax.set_title(r"${}^{62} Ni \; 1^{-}$")
    
        pngfile = os.path.join(workspace, CODE_NAME[temp]['excited'] + "_lorvec.png")
        canvas.print_figure(pngfile)


def main_generate(args):
    def mkdir_if_not_exists(folder):
        try: # try creating the working directory
            os.makedirs(folder)
        except OSError:
            if os.path.exists(folder):
                sys.exit("Folder {} already exists, exiting.".format(folder))
            else:
                sys.exit("Error creating {} folder. Check permissions. Exiting.".format(folder))

    # create output folder
    mkdir_if_not_exists(args.workspace)

    # generate input files for FORTRAN and C++ 
    generate_inputs(out_path=args.workspace, load_matrix=args.load_matrix,
                    nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78)

def main_run(args):
    def get_all_codenames():
        codes = []
        for temp in ('zero', 'finite'):
            for state in ('ground', 'excited'):
                codes.append(CODE_NAME[temp][state])
        return codes

    # get list of executable names
    executable_names = get_all_codenames()

    # check if executables are actually on disk
    for f in executable_names:
        fpath = os.path.join(args.code_dir, f)
        if not os.path.isfile(fpath):
            sys.exit(f"Executable {fpath} not found, exiting.")

    # check if input files are present in the workspace
    for temp in ('zero', 'finite'): # create input files
        for state, suffix in zip(('ground', 'excited'), ("_dis.dat", "_start.dat")):
            fpath = os.path.join(args.workspace, CODE_NAME[temp][state] + suffix)
            if not os.path.isfile(fpath):
                sys.exit(f"{fpath} not found, exiting.")

    if args.load_matrix:
        flist = ['_arpa.bin', '_brpa.bin', '_xrpa.bin', '_yrpa.bin' ,'_erpa.bin' ,'_c_erpa.bin']
        for f in flist:
            for temp in ('zero', 'finite'):
                fpath = os.path.join(args.load_mat_from, CODE_NAME[temp]['excited'] + f)
                shutil.copy(fpath, args.workspace)
                logging.info(f'Copied {fpath} to {args.workspace}.')
                

    # run the FORTRAN and C++ 
    run_executables(out_path=args.workspace,
                    exenames=executable_names, exepath=args.code_dir)


def main_plot(args):
    # post-process the output of the FORTRAN and C++                         
    plot_lorvec(workspace=args.workspace)


def main_all(args):
    # generate input files
    main_generate(args)

    # run all codes
    main_run(args)

    # plot the results
    main_plot(args)


def main():
    parser = argparse.ArgumentParser(
        description="this script can generate input files, run the "
                    "FORTAN and C++ codes and plot the results.")
    parser.add_argument(
        '-w', '--workspace',
        type=str,
        required=True,
        help="The path to the workspace directory.")
    parser.add_argument(
        '--load-matrix',
        action='store_true',
        help="Load matrix from disk, skipping calculation.")
    parser.add_argument(
        '--load-mat-from',
        type=str,
        help="Where to load the matrix from.")
    subparsers = parser.add_subparsers()

    parser_all = subparsers.add_parser('all')
    parser_all.set_defaults(func=main_all)

    parser_generate = subparsers.add_parser('generate')
    parser_generate.set_defaults(func=main_generate)

    parser_run = subparsers.add_parser('run')
    for subparser in [parser_all, parser_run]:
        subparser.add_argument(
            '--code-dir',
            type=str,
            default='../bin',
            help="The path to the compiled codes directory.")    
    parser_run.set_defaults(func=main_run)

    parser_plot = subparsers.add_parser('plot')
    parser_plot.set_defaults(func=main_plot)


    args = parser.parse_args() # load command line args

    if args.load_matrix and not args.load_mat_from:
        parser.error('The --load-matrix flag requires --load-mat-from')

    # must specify: generate, run, plot or all
    if not hasattr(args, 'func'): 
        parser.print_usage()
        sys.exit(2)
    try: # call generate, run or plot or all
        args.func(args)
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        sys.stderr.write("Interrupted.\n")
        sys.exit(1)
    except Exception as error:
        sys.stderr.write('{}\n'.format(str(error)))
        sys.exit(1)
    else:
        sys.exit(0)
    





    

if __name__ == '__main__':
    main()


    #TODO: copy files as in run_no_matrix.sh, based on --no-matrix flag
    #TODO: convert into module and import into signac program
    #TODO: create install script such that I can do python setup.py install --user
    #TODO: use virtualenv, see https://click.palletsprojects.com/en/7.x/quickstart/









