#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
from flow import FlowProject, cmd, with_job
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
@Project.pre.isfile('dish_dis.dat')
@Project.post.isfile('dish_qrpa.wel')
def run_zero_temp_ground_state(job):
    """Run dish FORTRAN code"""
    program = 'bin/dish.sh'
    path = job.ws 
    stdout_file = job.fn("dish_stdout.txt")
    stderr_file = job.fn("dish_stderr.txt")

    return f"{program} {path} > {stdout_file} 2> {stderr_file}"

# POST-conditions
# dish_stderr.txt must end with "FINAL STOP"
# dish_stdout.txt must end with "Iteration converged after"
# Note: don't need to run in case of --load-matrix


@Project.operation
@cmd
@Project.pre.after(run_zero_temp_ground_state)
@Project.pre.isfile('ztes_start.dat')
@Project.post.isfile('ztes_lorvec.out')
def run_zero_temp_excited_state(job):
    """Run ztes C++ code"""
    program = 'bin/ztes.sh'
    path = job.ws 
    stdout_file = job.fn("ztes_stdout.txt")
    stderr_file = job.fn("ztes_stderr.txt")

    return f"{program} {path} > {stdout_file} 2> {stderr_file}"

# POST-conditions
# ztes_stderr.txt must be empty
# ztes_stdout.txt must end with "program terminated without errors"
# Note: need to run also in case of --load-matrix


# @Project.operation
# @Project.operation
# @Project.operation


# define all pre and post-conditions
# tackle --load-matrix case
@Project.operation
@Project.post.isfile('result.txt')
@Project.post(lambda job: 'Iteration converged' in list(open(job.fn('file.txt'))[-2])
def calculation(job):
    pass


if __name__ == '__main__':
    Project().main()