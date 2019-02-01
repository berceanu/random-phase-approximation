#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
from flow import FlowProject, cmd, with_job
from signac import get_project
import re
import os
import shutil
import random
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import logging
logger = logging.getLogger(__name__)
from modules import code_api

# @with_job

#####################
# UTILITY FUNCTIONS #
#####################

# https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file/18603065#18603065
def read_last_line(filename):
    with open(filename, "rb") as f:
        _ = f.readline()            # Read the first line.
        f.seek(-2, os.SEEK_END)     # Jump to the second last byte.
        while f.read(1) != b"\n":   # Until EOL is found...
            f.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
        last = f.readline()         # Read last line.
    return last

def isemptyfile(filename):
    return lambda job: job.isfile(filename) and os.stat(job.fn(filename)).st_size == 0

def file_contains(filename, text):
    """Returns a function that checks if `filename` contains `text`."""
    return lambda job: job.isfile(filename) and text in open(job.fn(filename), 'r').read()

def arefiles(job, filenames):
    """Check if all `filenames` are in `job` folder."""
    return all(job.isfile(fn) for fn in filenames)

###########################

code = code_api.NameMapping()

class Project(FlowProject):
    pass

####################
# OPERATION LABELS #
####################

@Project.label
def isovector_plotted(job):
    if job.isfile('lorvec.png'):
        return "isovec_plotted"
    return "isovec_not_plotted"

def _progress(job, temp, code_mapping=code_api.NameMapping()):
    fn = code_mapping.stdout_file(temp, state='excited')
    if job.isfile(fn):
        last_line = read_last_line(job.fn(fn)).decode('UTF-8')
        if 'pa1 = ' in last_line:
            percentage = last_line.split()[-1]
        else: # already finished the matrix calculation
            percentage = "100.00"
    else: # didn't yet start the matrix calculation
        percentage = "0.00"

    return f"run_{temp}_temp_excited_state: {float(percentage):.2f}%"

@Project.label
def progress_zero(job):
    return _progress(job, temp='zero', code_mapping=code)

@Project.label
def progress_finite(job):
    return _progress(job, temp='finite', code_mapping=code)


##########################
# GENERATING INPUT FILES #
##########################

def bin_files_exist(job, temp):
    """Check if job folder has the required .bin files for loading."""
    return arefiles(job, code.bin_files(temp))

def _prepare_run(job, temp, code_mapping=code_api.NameMapping()):
    filter = {param:job.sp[param] 
                for param in ('nucleus', 'angular_momentum', 'parity', 'temperature')}

    project = get_project()
    jobs_for_restart = [job for job in project.find_jobs(filter)
                            if bin_files_exist(job, temp)]
    assert job not in jobs_for_restart
    try:
        job_for_restart = random.choice(jobs_for_restart)
    except IndexError: # prepare full calculation
        logger.info('Full calculation required.')
        code_input = code_api.GenerateInputs(out_path=job.ws, **job.sp, mapping=code_mapping)
        code_input.write_param_files(temp)
        # job.doc[f'run_{temp}_temp_ground_state'] = True
    else:  # prepare restart
        logger.info('Restart possible.')
        code_input = code_api.GenerateInputs(out_path=job.ws, **job.sp,
                                    load_matrix=True, mapping=code_mapping)
        code_input.write_param_files(temp, state='excited')
        dotwelfn = code_mapping.wel_file(temp)
        shutil.copy(job_for_restart.fn(dotwelfn), job.fn(dotwelfn))
        for fn in code_mapping.bin_files(temp):
            shutil.copy(job_for_restart.fn(fn), job.fn(fn))
        job.doc['restarted_from'] = job_for_restart._id
        #job.doc[f'run_{temp}_temp_ground_state'] = False

@Project.operation
@Project.pre(lambda job: job.sp.temperature == 0)
@Project.post.isfile(code.input_file(temp='zero', state='excited'))
def prepare_run_zero(job):
    _prepare_run(job, temp='zero', code_mapping=code)

@Project.operation
@Project.pre(lambda job: job.sp.temperature != 0)
@Project.post.isfile(code.input_file(temp='finite', state='excited'))
def prepare_run_finite(job):
    _prepare_run(job, temp='finite', code_mapping=code)

#################
# RUNNING CODES #
#################

def _run_code(job, temp, state, codepath='bin', code_mapping=code_api.NameMapping()):
    code = os.path.join(codepath, code_mapping.exec_file(temp, state))
    stdout_file = job.fn(code_mapping.stdout_file(temp, state))
    stderr_file = job.fn(code_mapping.stderr_file(temp, state))

    return f"{code} {job.ws} > {stdout_file} 2> {stderr_file}"


#### ZERO TEMP GROUND STATE ####
@Project.operation
@cmd
# @Project.pre.true('run_zero_temp_ground_state')
@Project.pre.isfile(code.input_file(temp='zero', state='ground')) 
@Project.post.isfile(code.wel_file(temp='zero')) 
@Project.post(file_contains(code.stderr_file(temp='zero', state='ground'),
                             'FINAL STOP'))
@Project.post(file_contains(code.stdout_file(temp='zero', state='ground'),
                             'Iteration converged'))
def run_zero_temp_ground_state(job):
    return _run_code(job, temp='zero', state='ground', code_mapping=code)


#### ZERO TEMP EXCITED STATE ####
@Project.operation
@cmd
@Project.pre.isfile(code.input_file(temp='zero', state='excited')) 
@Project.pre.isfile(code.wel_file(temp='zero'))
@Project.post.isfile(code.isovec_file(temp='zero'))
@Project.post(file_contains(code.stdout_file(temp='zero', state='excited'),
                             'program terminated without errors'))
@Project.post(isemptyfile(code.stderr_file(temp='zero', state='excited')))
def run_zero_temp_excited_state(job):
    return _run_code(job, temp='zero', state='excited', code_mapping=code)


#### FINITE TEMP GROUND STATE ####
@Project.operation
@cmd
# @Project.pre.true('run_finite_temp_ground_state')
@Project.pre.isfile(code.input_file(temp='finite', state='ground')) 
@Project.post.isfile(code.wel_file(temp='finite')) 
@Project.post(file_contains(code.stderr_file(temp='finite', state='ground'),
                             'FINAL STOP'))
@Project.post(file_contains(code.stdout_file(temp='finite', state='ground'),
                             'Iteration converged'))
def run_finite_temp_ground_state(job):
    return _run_code(job, temp='finite', state='ground', code_mapping=code)


#### FINITE TEMP EXCITED STATE ####
@Project.operation
@cmd
@Project.pre.isfile(code.input_file(temp='finite', state='excited')) 
@Project.pre.isfile(code.wel_file(temp='finite'))
@Project.post.isfile(code.isovec_file(temp='finite'))
@Project.post(file_contains(code.stdout_file(temp='finite', state='excited'),
                             'program terminated without errors'))
@Project.post(isemptyfile(code.stderr_file(temp='finite', state='excited')))
def run_finite_temp_excited_state(job):
    return _run_code(job, temp='finite', state='excited', code_mapping=code)



############
# PLOTTING #
############

def _plot_isovector(job, temp, code_mapping=code_api.NameMapping()):
    def split_element_mass(job):
        pattern = re.compile(r"([A-Z]*)(\d*)")
        element, mass_number = pattern.sub(r'\1 \2', job.sp.nucleus).split()
        element = element.title() # capitalize first letter only
        return element, mass_number

    arr = np.loadtxt(job.fn(code_mapping.isovec_file(temp)))
    h_axis = arr[:,0]
    arr1d = arr[:,1]

    fig = Figure(figsize=(10, 6))
    canvas = FigureCanvas(fig)

    ax = fig.add_subplot(111)
    ax.plot(h_axis, arr1d, label=f"T = {job.sp.temperature} MeV",
                           color='black',
                           linestyle='-')

    ax.grid()
    ax.set(
        xlim=[0, 30],
        ylim=[0, 4.5],
        ylabel=r"$R \; (e^2fm^2/MeV)$",
        xlabel="E (MeV)",
    )
    # ax.text(0.02, 0.95, "", transform=ax.transAxes, color="firebrick")
    ax.legend()

    element, mass = split_element_mass(job)
    ax.set_title(fr"${{}}^{{{mass}}} {element} \; {job.sp.angular_momentum}^{{{job.sp.parity}}}$")

    canvas.print_figure(job.fn('lorvec.png'))

@Project.operation
@Project.pre.isfile(code.isovec_file(temp='zero'))
@Project.post.isfile('lorvec.png')
def plot_zero(job):
    _plot_isovector(job, temp='zero', code_mapping=code)

@Project.operation
@Project.pre.isfile(code.isovec_file(temp='finite'))
@Project.post.isfile('lorvec.png')
def plot_finite(job):
    _plot_isovector(job, temp='finite', code_mapping=code)

####################################
# EXTRACT DIPOLE TRANSITIONS TABLE #
####################################

def _extract_transitions(job, temp, code_mapping=code_api.NameMapping()):
    first_marker = "1=n/2=p       E/hole      E/particle  XX-YY/%"
    last_marker = "Sum XX-YY after normalization *"
    #
    infn = job.fn(code_mapping.stdout_file(temp, state='excited'))
    outfn = job.fn('dipole_transitions.txt')
    #
    with open(infn, 'r') as infile, open(outfn, 'w') as outfile:
        copy = False
        for line in infile:
            if first_marker in line.strip():
                copy = True
            elif last_marker in line.strip():
                copy = False
            elif copy:
                outfile.write(line)

@Project.operation
@Project.pre(file_contains(code.stdout_file(temp='zero', state='excited'),
                             "1=n/2=p       E/hole      E/particle  XX-YY/%"))
@Project.post.isfile('dipole_transitions.txt')
def dipole_trans_zero(job):
    _extract_transitions(job, temp='zero', code_mapping=code)

@Project.operation
@Project.pre(file_contains(code.stdout_file(temp='finite', state='excited'),
                             "1=n/2=p       E/hole      E/particle  XX-YY/%"))
@Project.post.isfile('dipole_transitions.txt')
def dipole_trans_finite(job):
    _extract_transitions(job, temp='finite', code_mapping=code)


#TODO incorporate into main `rpa` repo
#TODO reproduce plots in Yf paper

if __name__ == '__main__':
    logging.basicConfig(
        filename='project.log',
        format='%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info('==RUN STARTED==')
    Project().main()
    logger.info('==RUN FINISHED==')
