#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging
import os

import jinja2
import pandas as pd
from flow import FlowProject

logger = logging.getLogger(__name__)
logfname = "project.log"


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(lambda job: job.sp.temperature == 0)
@Project.post.isfile("bla.txt")
def prepare_run_zero(job):
    pass


def get_template(template_file):
    """Get a jinja template with latex tags.

    modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
    """
    latex_jinja_env = jinja2.Environment(
        line_statement_prefix="#",
        line_comment_prefix="##",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath("/")),
    )
    template = latex_jinja_env.get_template(os.path.realpath(template_file))
    return template


@Project.operation
@Project.pre.isfile("dipole_transitions.txt")
@Project.post.isfile("dipole_transitions.html")
def get_table(job):
    from mypackage.util import match_split, frac_to_html

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

    # working directory must be ~/Development/random-phase-approximation/projects/rpa
    template = get_template("src/templates/dipole_transitions.j2")
    rendered_template = template.render(dict(table=table))

    with open(job.fn("dipole_transitions.html"), "w") as outfile:
        outfile.write(rendered_template)


# def _plot_inset(job, temp, code_mapping=code_api.NameMapping()):
#     from matplotlib.ticker import MultipleLocator
#
#     fig = Figure(figsize=(12, 4))
#     canvas = FigureCanvas(fig)
#     gs = GridSpec(1, 1)
#     ax = fig.add_subplot(gs[0, 0])
#
#     for lorexc in "excitation", "lorentzian":
#         df = out_file_to_df(job, temp, code_mapping, lorentzian_or_excitation=lorexc)
#         df = df[(df.energy >= 0.0) & (df.energy <= 10.0)]  # MeV
#         if lorexc == "excitation":
#             ax.vlines(df.energy, 0.0, df.transition_strength, colors="black")
#             if job.sp.transition_energy != 0.42:
#                 df = df[np.isclose(df.energy, job.sp.transition_energy, atol=0.01)]
#                 ax.vlines(df.energy, 0.0, df.transition_strength, colors="red")
#         elif lorexc == "lorentzian":
#             ax.plot(df.energy, df.transition_strength, color="black")
#
#     ax.set_title("isovector")
#     ax.set(
#         ylabel=r"$R \; (e^2fm^2/MeV)$",
#         xlabel="E (MeV)",
#         ylim=[-0.1, 3.0],
#         xlim=[0.0, 10.0],
#     )
#     ax.xaxis.set_major_locator(MultipleLocator(1))
#     ax.xaxis.set_minor_locator(MultipleLocator(0.25))
#
#     for sp in "top", "right":
#         ax.spines[sp].set_visible(False)
#
#     atomic_symbol, mass_number = util.get_nucleus(
#         job.sp.proton_number, job.sp.neutron_number, joined=False
#     )
#     fig.suptitle(
#         (
#             fr"Transition strength distribution of ${{}}^{{{mass_number}}} {atomic_symbol} \; "
#             fr"{job.sp.angular_momentum}^{{{job.sp.parity}}}$ at T = {job.sp.temperature} MeV"
#         )
#     )
#     canvas.print_png(job.fn("inset.png"))
#
#
# @Project.operation
# @Project.pre(arefiles(code.out_files(temp="zero")))
# @Project.post.isfile("inset.png")
# def plot_inset_zero(job):
#     _plot_inset(job, temp="zero", code_mapping=code)
#
#
# @Project.operation
# @Project.pre(arefiles(code.out_files(temp="finite")))
# @Project.post.isfile("inset.png")
# def plot_inset_finite(job):
#     _plot_inset(job, temp="finite", code_mapping=code)
