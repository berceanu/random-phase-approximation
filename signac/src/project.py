#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
from flow import FlowProject, cmd, with_job
from signac import get_project
from util import CODE_NAME, generate_inputs
import os



class Project(FlowProject):
    pass


def input_files_exist(job):
    """Check if input files are present in the workspace"""
    is_file = []
    for temp in ('zero', 'finite'):
        for state, suffix in zip(('ground', 'excited'), ("_dis.dat", "_start.dat")):
            fpath = job.fn(CODE_NAME[temp][state] + suffix)
            is_file.append(os.path.isfile(fpath))
    return all(is_file)

# generate inputs
@Project.operation
@Project.post(input_files_exist)
def geninputs(job):
    """Generate all 4 input files."""
    generate_inputs(out_path=job.ws, **job.sp)


# define the 4 operations basic operations corresponding to the 4 codes
@Project.operation
@cmd
@Project.pre(lambda job: not job.sp.load_matrix)
@Project.pre.isfile('dish_dis.dat')
@Project.post.isfile('dish_qrpa.wel')
@Project.post.isfile('dish_stdout.txt')
@Project.post.isfile('dish_stderr.txt')
@Project.post(lambda job: 'FINAL STOP' in list(open(job.fn('dish_stderr.txt')))[-2])
@Project.post(lambda job: 'Iteration converged after' in list(open(job.fn('dish_stdout.txt')))[-3])
def run_zero_temp_ground_state(job):
    """Run dish FORTRAN code"""
    program = 'bin/dish.sh'
    path = job.ws 
    stdout_file = job.fn("dish_stdout.txt")
    stderr_file = job.fn("dish_stderr.txt")

    return f"{program} {path} > {stdout_file} 2> {stderr_file}"


@Project.operation
@cmd
@Project.pre.isfile('dish_qrpa.wel')
@Project.pre.isfile('ztes_start.dat')
# @Project.pre the 6 binary files should be present if load_matrix=True
# @Project.pre(lambda job: binaries_present() if job.sp.load_matrix else True)
@Project.post.isfile('ztes_lorvec.out')
@Project.post.isfile('ztes_stderr.txt')
@Project.post.isfile('ztes_stdout.txt')
@Project.post(lambda job: os.stat(job.fn('ztes_stderr.txt')).st_size==0)
@Project.post(lambda job: 'program terminated without errors' in list(open(job.fn('ztes_stdout.txt')))[-2])
def run_zero_temp_excited_state(job):
    """Run ztes C++ code"""
    program = 'bin/ztes.sh'
    path = job.ws 
    stdout_file = job.fn("ztes_stdout.txt")
    stderr_file = job.fn("ztes_stderr.txt")

    return f"{program} {path} > {stdout_file} 2> {stderr_file}"


# 1. need to calculate job {load_matrix=True, transition_energy=x, temperature=y, nucleus="NI62", angular_momentum=1, parity="-"}
# 2. find results of _full calculation_ job {load_matrix=False, transition_energy=x, temperature=y, nucleus="NI62", angular_momentum=1, parity="-"}
# 4. copy the 6 binary files, as well as `dish_qrpa.wel`

@Project.operation
# @Project.post(binaries_present)
@Project.post(lambda job: 'need_full_calculation' in job.doc)
def look_for_previous_results(job):
    project = get_project()
    previous_results = project.find_jobs(dict(job.sp, load_matrix=True))
    if len(previous_results):
        # copy the 6 binary files from other job, as well as `dish_qrpa.wel`
        job.doc.need_full_calculation = False
    else:
        job.doc.need_full_calculation = True


# Project.operation
# Project.pre.true('need_full_calculation')
# Project.post(data_available)
# def full_calculation(job):
    # code for full calculation



# @Project.operation
# @Project.operation


if __name__ == '__main__':
    Project().main()