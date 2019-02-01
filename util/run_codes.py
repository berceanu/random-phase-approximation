#!/usr/bin/env python3

import os
import sys
# import sh
import argparse
import subprocess
import shutil

import logging

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

from util import CODE_NAME, generate_inputs


def run_executables(exenames=['dish','skys','ztes','ftes'], out_path=os.getcwd(), mock=False,
                    exepath='../bin'):
    """Run the executable names in the list, redirecting their outputs to files"""

    for f in exenames:
        program=os.path.join(exepath, f)
        path=out_path
        stdout_file = os.path.join(out_path,f+"_stdout.txt")
        stderr_file = os.path.join(out_path,f+"_stderr.txt")
        if mock: # use bash scripts instead
            cmd = f"{program}.sh {path} > {stdout_file} 2> {stderr_file}"
        else:
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
    # generate input files for FORTRAN and C++ 
    generate_inputs(out_path=args.workspace, load_matrix=args.load_matrix,
                    nucleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78)

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
    for temp in ('zero', 'finite'):
        for state, suffix in zip(('ground', 'excited'), ("_dis.dat", "_start.dat")):
            fpath = os.path.join(args.workspace, CODE_NAME[temp][state] + suffix)
            if not os.path.isfile(fpath):
                sys.exit(f"{fpath} not found, exiting.")

    if args.load_matrix:
        flist = ['_arpa.bin', '_brpa.bin', '_xrpa.bin', '_yrpa.bin' ,'_erpa.bin' ,'_c_erpa.bin']
        for f in flist:
            for temp in ('zero', 'finite'):
                fpath = os.path.join(args.from_dir, CODE_NAME[temp]['excited'] + f)
                shutil.copy(fpath, args.workspace)
                logging.info(f'Copied {fpath} to {args.workspace}.')
                

    # run the FORTRAN and C++ 
    run_executables(out_path=args.workspace, mock=args.mock,
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
        '--from-dir',
        type=str,
        default=os.getcwd(),
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
        subparser.add_argument(
            '--mock',
            action='store_true',
            help='Do a mock run, using bash scripts instead of real codes.')
    parser_run.set_defaults(func=main_run)

    parser_plot = subparsers.add_parser('plot')
    parser_plot.set_defaults(func=main_plot)


    args = parser.parse_args() # load command line args

    if args.load_matrix and not args.from_dir:
        parser.error('The --load-matrix flag requires --from-dir')
    
    if not os.path.exists(args.workspace):
        sys.stderr.write(f'Cannot find workspace folder {args.workspace}\n')
        sys.exit(1)

    logfile = os.path.join(args.workspace, 'run_codes.log')
    handlers = [logging.FileHandler(logfile), logging.StreamHandler()] # also log to console
    logging.basicConfig(level=logging.INFO, format='  %(message)s', handlers=handlers)

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
    


# Usage example:
# == real run ==
# mkdir -p ../tests/out/full_calc
# mkdir -p ../tests/out/load_mat
# ./run_codes.py -w ../tests/out/full_calc all // runtime: 23 minutes
# ./run_codes.py -w ../tests/out/load_mat --load-matrix --from-dir ../tests/out/full_calc all  // runtime: 5 minutes
# == mock run ==
# mkdir -p ../tests/out/full_calc_mock
# mkdir -p ../tests/out/load_mat_mock
# ./run_codes.py -w ../tests/out/full_calc_mock all --mock
# ./run_codes.py -w ../tests/out/load_mat_mock --load-matrix --from-dir ../tests/out/full_calc_mock all --mock

if __name__ == '__main__':
    main()

#TODO: installation via pipenv
