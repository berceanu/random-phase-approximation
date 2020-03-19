#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging

from flow import FlowProject

logger = logging.getLogger(__name__)
logfname = "project.log"


class Project(FlowProject):
    pass


@Project.operation
@Project.pre(
    lambda job: all(
        job.isfile(fn)
        for fn in [
            bulma_id + "_dipole_transitions.h5"
            for bulma_id in job.doc.bulma_jobs.keys()
        ]
    )
)
@Project.pre(
    lambda job: all(
        job.isfile(fn)
        for fn in [bulma_id + "_inset.png" for bulma_id in job.doc.bulma_jobs.keys()]
    )
)
@Project.post.isfile("index.html")
def create_webpage(job):
    for bulma_id, d in job.doc.bulma_jobs.items():
        dipole_transitions = bulma_id + "_dipole_transitions.h5"
        inset = bulma_id + "_inset.png"
        temperature = d["temperature"]
        print(dipole_transitions, inset, temperature)


# def get_template(template_file):
#     """Get a jinja template with latex tags.
#
#     modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
#     """
#     latex_jinja_env = jinja2.Environment(
#         line_statement_prefix="#",
#         line_comment_prefix="##",
#         trim_blocks=True,
#         autoescape=False,
#         loader=jinja2.FileSystemLoader(os.path.abspath("/")),
#     )
#     template = latex_jinja_env.get_template(os.path.realpath(template_file))
#     return template
#


#
# @Project.operation
# @Project.pre.isfile("dipole_transitions.txt")
# @Project.post.isfile("dipole_transitions.html")
# def get_table(job):
#     from mypackage.util import match_split, frac_to_html
#
#     dip_conf = pd.read_csv(
#         job.fn("dipole_transitions.txt"),
#         sep=r"\s+",
#         header=None,
#         usecols=[0, 1, 3, 4, 6, 7],
#         names=[
#             "n_or_p",
#             "hole_energy",
#             "particle_energy",
#             "from_state",
#             "to_state",
#             "transition_amplitude",
#         ],
#     )
#     with pd.option_context("mode.use_inf_as_null", True):
#         dip_conf = dip_conf.dropna()  # drop inf values
#
#     filtered_conf = dip_conf[dip_conf.transition_amplitude > 1]
#     df = filtered_conf.sort_values(
#         by=["n_or_p", "transition_amplitude"], ascending=[False, False]
#     )
#
#     table = []
#     for idx in df.index:
#         np_mapping = {1: "&nu;", 2: "&pi;"}
#         neutron_proton = np_mapping[df.loc[idx, "n_or_p"]]
#
#         from_state = df.loc[idx, "from_state"]
#         from_state_orbital, from_state_frac = match_split(from_state)
#         from_state_frac_html = frac_to_html(from_state_frac)
#
#         to_state = df.loc[idx, "to_state"]
#         to_state_orbital, to_state_frac = match_split(to_state)
#         to_state_frac_html = frac_to_html(to_state_frac)
#
#         transition_amplitude = df.loc[idx, "transition_amplitude"]
#
#         row = {
#             "transition": (
#                 f"{neutron_proton}{from_state_orbital}{from_state_frac_html}&rarr;"
#                 f"{neutron_proton}{to_state_orbital}{to_state_frac_html}"
#             ),
#             "amplitude": f"{transition_amplitude:.2f}",
#         }
#         table.append(row)
#
#     # working directory must be ~/Development/random-phase-approximation/projects/rpa
#     template = get_template("src/templates/dipole_transitions.j2")
#     rendered_template = template.render(dict(table=table))
#
#     with open(job.fn("dipole_transitions.html"), "w") as outfile:
#         outfile.write(rendered_template)


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
