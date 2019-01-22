#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
from flow import FlowProject, cmd, with_job


class Project(FlowProject):
    pass

# import module run_codes.py
# generate inputs
# define the 4 operations basic operations corresponding to the 4 codes
# define all pre and post-conditions; see .sh scripts
# tackle --load-matrix case






if __name__ == '__main__':
    Project().main()