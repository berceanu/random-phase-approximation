#!/usr/bin/env python3
"""This module contains the operation functions for this project.

The workflow defined in this file can be executed from the command
line with

    $ python src/project.py run [job_id [job_id ...]]

See also: $ python src/project.py --help
"""
import logging
import os
from dataclasses import dataclass

import jinja2
import pandas as pd
from flow import FlowProject
from mypackage import util

logger = logging.getLogger(__name__)
logfname = "project.log"


class Project(FlowProject):
    pass


@dataclass(frozen=True)
class Section:
    temperature: float
    inset: str
    table: str


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
@Project.post.isfile("dipole_transitions.html")
def create_webpage(job):
    sections = list()
    for bulma_id, d in job.doc.bulma_jobs.items():
        temperature = d["temperature"]
        inset = bulma_id + "_inset.png"
        dipole_transitions = job.fn(bulma_id + "_dipole_transitions.h5")

        df = pd.read_hdf(dipole_transitions, key="dipole_transitions")
        table_html = df.to_html(
            escape=False,
            float_format="%.2f",
            classes="table is-bordered is-striped is-narrow is-hoverable is-fullwidth",
        )
        sections.append(Section(temperature, inset, table_html))

    atomic_symbol, mass_number = util.get_nucleus(
        job.sp.proton_number, job.sp.neutron_number, joined=False
    )
    nucleus = f"<sup>{mass_number}</sup>{atomic_symbol} {job.sp.angular_momentum}<sup>{job.sp.parity}</sup>"

    template = get_template("src/templates/transitions.j2")
    rendered_template = template.render(dict(sections=sections, title=nucleus))

    with open(job.fn("dipole_transitions.html"), "w") as outfile:
        outfile.write(rendered_template)


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
