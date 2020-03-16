#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging
import os
import random
import re
import shutil

import jinja2
import mypackage.code_api as code_api
import mypackage.talys.api as talys
import mypackage.util as util
import numpy as np
import pandas as pd
from flow import FlowProject, cmd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from mypackage.util import arefiles, file_contains, read_last_line, isemptyfile
from signac import get_project

logger = logging.getLogger(__name__)
logfname = "project.log"

PNG_FILE = "iso_all.png"

code = code_api.NameMapping()
talys_api = talys.TalysAPI()


class Project(FlowProject):
    pass


####################
# OPERATION LABELS #
####################


@Project.label
def plotted(job):
    return job.isfile(PNG_FILE)


def _progress(job, temp, code_mapping=code_api.NameMapping()):
    fn = code_mapping.stdout_file(temp, state="excited")
    if job.isfile(fn):
        last_line = read_last_line(job.fn(fn)).decode("UTF-8")
        if "pa1 = " in last_line:
            percentage = last_line.split()[-1]
        else:  # already finished the matrix calculation
            percentage = "100.00"
    else:  # didn't yet start the matrix calculation
        percentage = "0.00"

    return "run_{}_temp_excited_state: {:.2f}%".format(temp, float(percentage))


@Project.label
def progress_zero(job):
    return _progress(job, temp="zero", code_mapping=code)


@Project.label
def progress_finite(job):
    return _progress(job, temp="finite", code_mapping=code)


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
        # job.doc[f'run_{temp}_temp_ground_state'] = True
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


@Project.operation
@Project.pre(lambda job: job.sp.temperature != 0)
@Project.post.isfile(code.input_file(temp="finite", state="excited"))
def prepare_run_finite(job):
    _prepare_run(job, temp="finite", code_mapping=code)


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
# @Project.pre.true('run_zero_temp_ground_state')
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
# @Project.pre.isfile(code.wel_file(temp='zero'))
# use all of run_zero_temp_ground_state's post-conditions as pre-conditions
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


# FINITE TEMP GROUND STATE #
@Project.operation
@cmd
# @Project.pre.true('run_finite_temp_ground_state')
@Project.pre.isfile(code.input_file(temp="finite", state="ground"))
@Project.post.isfile(code.wel_file(temp="finite"))
@Project.post(
    file_contains(code.stderr_file(temp="finite", state="ground"), "FINAL STOP")
)
@Project.post(
    file_contains(
        code.stdout_file(temp="finite", state="ground"), "Iteration converged"
    )
)
def run_finite_temp_ground_state(job):
    return _run_code(job, temp="finite", state="ground", code_mapping=code)


# FINITE TEMP EXCITED STATE #
@Project.operation
@cmd
@Project.pre.isfile(code.input_file(temp="finite", state="excited"))
# @Project.pre.isfile(code.wel_file(temp='finite'))
@Project.pre.after(run_finite_temp_ground_state)
@Project.post(arefiles(code.out_files(temp="finite")))
@Project.post(
    file_contains(
        code.stdout_file(temp="finite", state="excited"),
        "program terminated without errors",
    )
)
@Project.post(isemptyfile(code.stderr_file(temp="finite", state="excited")))
def run_finite_temp_excited_state(job):
    return _run_code(job, temp="finite", state="excited", code_mapping=code)


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


@Project.operation
@Project.pre(arefiles(code.out_files(temp="finite")))
@Project.post.isfile("transerg.dat")
def out_file_to_transerg_finite(job):
    _out_file_to_transerg(job, temp="finite", code_mapping=code)


############
# PLOTTING #
############


def _plot_inset(job, temp, code_mapping=code_api.NameMapping()):
    from matplotlib.ticker import MultipleLocator

    fig = Figure(figsize=(12, 4))
    canvas = FigureCanvas(fig)
    gs = GridSpec(1, 1)
    ax = fig.add_subplot(gs[0, 0])

    for lorexc in "excitation", "lorentzian":
        df = out_file_to_df(job, temp, code_mapping, lorentzian_or_excitation=lorexc)
        df = df[(df.energy >= 0.0) & (df.energy <= 10.0)]  # MeV
        if lorexc == "excitation":
            ax.vlines(df.energy, 0.0, df.transition_strength, colors="black")
            if job.sp.transition_energy != 0.42:
                df = df[np.isclose(df.energy, job.sp.transition_energy, atol=0.01)]
                ax.vlines(df.energy, 0.0, df.transition_strength, colors="red")
        elif lorexc == "lorentzian":
            ax.plot(df.energy, df.transition_strength, color="black")

    ax.set_title("isovector")
    ax.set(
        ylabel=r"$R \; (e^2fm^2/MeV)$",
        xlabel="E (MeV)",
        ylim=[-0.1, 3.0],
        xlim=[0.0, 10.0],
    )
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))

    for sp in "top", "right":
        ax.spines[sp].set_visible(False)

    atomic_symbol, mass_number = util.get_nucleus(
        job.sp.proton_number, job.sp.neutron_number, joined=False
    )
    fig.suptitle(
        (
            fr"Transition strength distribution of ${{}}^{{{mass_number}}} {atomic_symbol} \; "
            fr"{job.sp.angular_momentum}^{{{job.sp.parity}}}$ at T = {job.sp.temperature} MeV"
        )
    )
    canvas.print_png(job.fn("inset.png"))


@Project.operation
@Project.pre(arefiles(code.out_files(temp="zero")))
@Project.post.isfile("inset.png")
def plot_inset_zero(job):
    _plot_inset(job, temp="zero", code_mapping=code)


@Project.operation
@Project.pre(arefiles(code.out_files(temp="finite")))
@Project.post.isfile("inset.png")
def plot_inset_finite(job):
    _plot_inset(job, temp="finite", code_mapping=code)


def _plot_iso(job, temp, code_mapping=code_api.NameMapping()):
    def _out_file_plot(
        job,
        axis,
        temperature,
        isoscalar_or_isovector,
        lorentzian_or_excitation,
        codemapping=code_api.NameMapping(),
    ):

        fn = job.fn(
            codemapping.out_file(
                temperature, isoscalar_or_isovector, lorentzian_or_excitation
            )
        )

        dataframe = pd.read_csv(
            fn,
            delim_whitespace=True,
            comment="#",
            skip_blank_lines=True,
            header=None,
            names=["energy", "transition_strength"],
        )

        dataframe = dataframe[dataframe.energy < 30]  # MeV

        if lorentzian_or_excitation == "excitation":
            axis.vlines(
                dataframe.energy, 0.0, dataframe.transition_strength, colors="black"
            )
        elif lorentzian_or_excitation == "lorentzian":
            axis.plot(dataframe.energy, dataframe.transition_strength, color="black")
        else:
            raise ValueError

        return dataframe

    fig = Figure(figsize=(12, 6))
    canvas = FigureCanvas(fig)

    gs = GridSpec(2, 1)
    ax = {
        "isoscalar": fig.add_subplot(gs[0, 0]),
        "isovector": fig.add_subplot(gs[1, 0]),
    }

    for skalvec in "isoscalar", "isovector":
        for sp in ("top", "bottom", "right"):
            ax[skalvec].spines[sp].set_visible(False)
        ax[skalvec].set(ylabel=r"$R \; (e^2fm^2/MeV)$")
        ax[skalvec].set_title(skalvec)
        for lorexc in "excitation", "lorentzian":
            df = _out_file_plot(
                job=job,
                axis=ax[skalvec],
                temperature=temp,
                isoscalar_or_isovector=skalvec,
                lorentzian_or_excitation=lorexc,
                codemapping=code_mapping,
            )
            if lorexc == "excitation" and job.sp.transition_energy != 0.42:
                df = df[np.isclose(df.energy, job.sp.transition_energy, atol=0.01)]
                ax[skalvec].vlines(df.energy, 0.0, df.transition_strength, colors="red")

    ax["isovector"].set(xlabel="E (MeV)")
    fig.subplots_adjust(hspace=0.3)

    atomic_symbol, mass_number = util.get_nucleus(
        job.sp.proton_number, job.sp.neutron_number, joined=False
    )
    fig.suptitle(
        (
            fr"Transition strength distribution of ${{}}^{{{mass_number}}} {atomic_symbol} \; "
            fr"{job.sp.angular_momentum}^{{{job.sp.parity}}}$ at T = {job.sp.temperature} MeV"
        )
    )

    canvas.print_png(job.fn(PNG_FILE))


@Project.operation
@Project.pre(arefiles(code.out_files(temp="zero")))
@Project.post.isfile(PNG_FILE)
def plot_zero(job):
    _plot_iso(job, temp="zero", code_mapping=code)


@Project.operation
@Project.pre(arefiles(code.out_files(temp="finite")))
@Project.post.isfile(PNG_FILE)
def plot_finite(job):
    _plot_iso(job, temp="finite", code_mapping=code)


####################################
# EXTRACT DIPOLE TRANSITIONS TABLE #
####################################


def _extract_transitions(job, temp, code_mapping=code_api.NameMapping()):
    first_marker = "1=n/2=p       E/hole      E/particle  XX-YY/%"
    last_marker = "Sum XX-YY after normalization *"
    #
    infn = job.fn(code_mapping.stdout_file(temp, state="excited"))
    outfn = job.fn("dipole_transitions.txt")
    #
    with open(infn, "r") as infile, open(outfn, "w") as outfile:
        copy = False
        for line in infile:
            if first_marker in line.strip():
                copy = True
            elif last_marker in line.strip():
                copy = False
            elif copy:
                outfile.write(line)


@Project.operation
@Project.pre(
    file_contains(
        code.stdout_file(temp="zero", state="excited"),
        "1=n/2=p       E/hole      E/particle  XX-YY/%",
    )
)
@Project.post.isfile("dipole_transitions.txt")
def extract_transitions_zero(job):
    _extract_transitions(job, temp="zero", code_mapping=code)


@Project.operation
@Project.pre(
    file_contains(
        code.stdout_file(temp="finite", state="excited"),
        "1=n/2=p       E/hole      E/particle  XX-YY/%",
    )
)
@Project.post.isfile("dipole_transitions.txt")
def extract_transitions_finite(job):
    _extract_transitions(job, temp="finite", code_mapping=code)


@Project.operation
@Project.pre.isfile("dipole_transitions.txt")
@Project.post.isfile("dipole_transitions.html")
def get_table(job):
    def match_split(orbital_frac):
        regex = re.compile(r"(?P<orbital>\d+[a-z]+)(?P<frac>\d+/\d+)")
        m = regex.search(orbital_frac)
        return m.group("orbital"), m.group("frac")

    def frac_to_html(frac):
        numerator, denominator = frac.split("/")
        return f"<sub>{numerator}&frasl;{denominator}</sub>"

    dip_conf = pd.read_csv(
        job.fn("dipole_transitions.txt"),
        sep=r"\s+",
        header=None,
        usecols=[0, 1, 3, 4, 6, 7],
        names=[
            "n_or_p",
            "hole_energy",
            "particle_energy",
            "from_state",
            "to_state",
            "transition_amplitude",
        ],
    )
    with pd.option_context("mode.use_inf_as_null", True):
        dip_conf = dip_conf.dropna()  # drop inf values

    filtered_conf = dip_conf[dip_conf.transition_amplitude > 1]
    df = filtered_conf.sort_values(
        by=["n_or_p", "transition_amplitude"], ascending=[False, False]
    )

    table = []
    for idx in df.index:
        np_mapping = {1: "&nu;", 2: "&pi;"}
        neutron_proton = np_mapping[df.loc[idx, "n_or_p"]]

        from_state = df.loc[idx, "from_state"]
        from_state_orbital, from_state_frac = match_split(from_state)
        from_state_frac_html = frac_to_html(from_state_frac)

        to_state = df.loc[idx, "to_state"]
        to_state_orbital, to_state_frac = match_split(to_state)
        to_state_frac_html = frac_to_html(to_state_frac)

        transition_amplitude = df.loc[idx, "transition_amplitude"]

        row = {
            "transition": (
                f"{neutron_proton}{from_state_orbital}{from_state_frac_html}&rarr;"
                f"{neutron_proton}{to_state_orbital}{to_state_frac_html}"
            ),
            "amplitude": f"{transition_amplitude:.2f}",
        }
        table.append(row)

    latex_jinja_env = jinja2.Environment(
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath("/")),
    )
    template = latex_jinja_env.get_template(
        os.path.realpath("src/templates/dipole_transitions.j2")
    )  # working directory must be ~/Development/random-phase-approximation/projects/rpa
    rendered_template = template.render(dict(table=table))

    with open(job.fn("dipole_transitions.html"), "w") as outfile:
        outfile.write(rendered_template)


#################################
# GENERATE INPUT FOR TALYS CODE #
#################################


def _generate_talys_input(job, temp, code_mapping=code_api.NameMapping()):
    job_mass_number = job.sp.proton_number + job.sp.neutron_number
    fn = job.fn(
        code_mapping.out_file(temp=temp, skalvec="isovector", lorexc="lorentzian")
    )

    lorvec_df = talys.lorvec_to_df(fname=fn, Z=job.sp.proton_number, A=job_mass_number)

    talys_dict = talys.fn_to_dict(
        fname=talys_api.template_photon_strength_function_path(job),
        proton_number=job.sp.proton_number,
    )
    talys_df = talys.dict_to_df(talys_dict)

    mass_numbers = talys.atomic_mass_numbers(talys_df)
    logger.info(
        "{} contains atomic mass numbers from A={} to A={}.".format(
            talys_api.template_photon_strength_function_path(job),
            mass_numbers.min(),
            mass_numbers.max(),
        )
    )

    if job_mass_number in mass_numbers:
        talys_df_new = talys.replace_table(
            Z=job.sp.proton_number, A=job_mass_number, talys=talys_df, lorvec=lorvec_df
        )
        new_talys_dict = talys.df_to_dict(talys_df_new)
        talys.dict_to_fn(
            new_talys_dict,
            fname=job.fn(talys.psf_fn(job)),
            proton_number=job.sp.proton_number,
        )
        job.doc.setdefault("photon_strength_function", talys.psf_fn(job))
    else:
        logger.warning(
            "(Z,A)=({},{}) not found in {}!".format(
                job.sp.proton_number,
                job_mass_number,
                talys_api.template_photon_strength_function_path(job),
            )
        )


# only Sn isotopes (Z = 50) will get processed
@Project.operation
@Project.pre(
    lambda job: os.path.isfile(talys_api.template_photon_strength_function_path(job))
)
@Project.pre.isfile(
    code.out_file(temp="zero", skalvec="isovector", lorexc="lorentzian")
)
@Project.post(lambda job: job.isfile(talys.psf_fn(job)))
def generate_talys_input_zero(job):
    _generate_talys_input(job, temp="zero", code_mapping=code)


@Project.operation
@Project.pre(
    lambda job: os.path.isfile(talys_api.template_photon_strength_function_path(job))
)
@Project.pre.isfile(
    code.out_file(temp="finite", skalvec="isovector", lorexc="lorentzian")
)
@Project.post(lambda job: job.isfile(talys.psf_fn(job)))
def generate_talys_input_finite(job):
    _generate_talys_input(job, temp="finite", code_mapping=code)


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
