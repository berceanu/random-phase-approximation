"""This module contains the operation functions for this project."""
import logging
import os
import random
import shutil

from flow import FlowProject, cmd
from signac import get_project
import mypackage.code_api as code_api
from mypackage.util import arefiles, file_contains, isemptyfile
import pandas as pd

logger = logging.getLogger(__name__)
logfname = "project.log"


code = code_api.NameMapping()


class Project(FlowProject):
    pass


##########################
# GENERATING INPUT FILES #
##########################


def bin_files_exist(job, temp):
    """Check if job folder has the required .bin files for loading."""
    return arefiles(code.bin_files(temp))(job)


def _prepare_run(job, temp, code_mapping=code_api.NameMapping()):
    my_filter = {
        param: job.sp[param]
        for param in (
            "proton_number",
            "neutron_number",
            "angular_momentum",
            "parity",
            "temperature",
        )
    }

    project = get_project()
    jobs_for_restart = [
        job for job in project.find_jobs(my_filter) if bin_files_exist(job, temp)
    ]
    assert job not in jobs_for_restart
    try:
        job_for_restart = random.choice(jobs_for_restart)
    except IndexError:  # prepare full calculation
        logger.info("Full calculation required.")
        code_input = code_api.GenerateInputs(
            out_path=job.ws, mapping=code_mapping, **dict(job.sp)
        )
        code_input.write_param_files(temp)
    else:  # prepare restart
        logger.info("Restart possible.")
        code_input = code_api.GenerateInputs(
            out_path=job.ws, mapping=code_mapping, **dict(job.sp), load_matrix=True
        )
        code_input.write_param_files(temp, state="excited")
        dotwelfn = code_mapping.wel_file(temp)
        shutil.copy(job_for_restart.fn(dotwelfn), job.fn(dotwelfn))
        for fn in code_mapping.bin_files(temp):
            shutil.copy(job_for_restart.fn(fn), job.fn(fn))

        stderr_file = code_mapping.stderr_file(temp, state="ground")
        shutil.copy(job_for_restart.fn(stderr_file), job.fn(stderr_file))
        stdout_file = code_mapping.stdout_file(temp, state="ground")
        shutil.copy(job_for_restart.fn(stdout_file), job.fn(stdout_file))

        job.doc["restarted_from"] = job_for_restart.id


@Project.operation
@Project.pre(lambda job: job.sp.temperature == 0)
@Project.post.isfile(code.input_file(temp="zero", state="excited"))
def prepare_run_zero(job):
    _prepare_run(job, temp="zero", code_mapping=code)


#################
# RUNNING CODES #
#################


def _run_code(
    job, temp, state, codepath="../../bin", code_mapping=code_api.NameMapping()
):
    code_cmd = os.path.join(codepath, code_mapping.exec_file(temp, state))
    assert os.path.isfile(code_cmd), f"{code_cmd} not found!"

    stdout_file = job.fn(code_mapping.stdout_file(temp, state))
    stderr_file = job.fn(code_mapping.stderr_file(temp, state))

    run_command = f"{code_cmd} {job.ws} > {stdout_file} 2> {stderr_file}"
    command = f"echo {run_command} >> {logfname} ; {run_command}"

    return command


# ZERO TEMP GROUND STATE #
@Project.operation
@cmd
@Project.pre.isfile(code.input_file(temp="zero", state="ground"))
@Project.post.isfile(code.wel_file(temp="zero"))
@Project.post(
    file_contains(code.stderr_file(temp="zero", state="ground"), "FINAL STOP")
)
@Project.post(
    file_contains(code.stdout_file(temp="zero", state="ground"), "Iteration converged")
)
def run_zero_temp_ground_state(job):
    return _run_code(job, temp="zero", state="ground", code_mapping=code)


# ZERO TEMP EXCITED STATE #
@Project.operation
@cmd
@Project.pre.isfile(code.input_file(temp="zero", state="excited"))
@Project.pre.after(run_zero_temp_ground_state)
@Project.post(arefiles(code.out_files(temp="zero")))
@Project.post(
    file_contains(
        code.stdout_file(temp="zero", state="excited"),
        "program terminated without errors",
    )
)
@Project.post(isemptyfile(code.stderr_file(temp="zero", state="excited")))
def run_zero_temp_excited_state(job):
    return _run_code(job, temp="zero", state="excited", code_mapping=code)


###########################
# TOP TRANSITION ENERGIES #
###########################


def out_file_to_df(
    job,
    temp,
    code_mapping=code_api.NameMapping(),
    lorentzian_or_excitation="excitation",
):
    fn = job.fn(code_mapping.out_file(temp, "isovector", lorentzian_or_excitation))
    dataframe = pd.read_csv(
        fn,
        delim_whitespace=True,
        comment="#",
        skip_blank_lines=True,
        header=None,
        names=["energy", "transition_strength"],
    )
    return dataframe


def nlargest_to_file(df, max_energy=10, n=3, fn="transerg.dat"):
    df = df[df.energy < max_energy]  # MeV
    top_n = df.nlargest(n, columns="transition_strength")
    top_n.to_csv(fn, float_format="%.6e", index_label="old_index", encoding="utf-8")


def _out_file_to_transerg(
    job, temp, code_mapping=code_api.NameMapping(),
):
    df = out_file_to_df(job, temp, code_mapping)
    nlargest_to_file(df, fn=job.fn("transerg.dat"))


@Project.operation
@Project.pre(arefiles(code.out_files(temp="zero")))
@Project.post.isfile("transerg.dat")
def out_file_to_transerg_zero(job):
    _out_file_to_transerg(job, temp="zero", code_mapping=code)


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfname,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("==RUN STARTED==")
    Project().main()
    logger.info("==RUN FINISHED==")
