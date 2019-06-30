#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple wrapper for calling TALYS code."""

import hashlib
import logging
import subprocess
from dataclasses import dataclass
import pathlib

from jinja2 import Environment, FileSystemLoader

# pass folder containing the template
file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

logger = logging.getLogger(__name__)
logfile = "wrapper.log"


def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


@dataclass
class NuclearElement:
    name: str
    mass: int


def sh(*cmd, **kwargs):
    logger.info(cmd[0])
    stdout = (
        subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs
        )
            .communicate()[0]
            .decode("utf-8")
    )
    logger.info(stdout)
    return stdout


def talys_command(input_file: str = "input", output_file: str = "output", wd=pathlib.Path.cwd()) -> str:
    """Construct the TALYS command to be ran.

    :param input_file: input file name
    :param output_file: output file name
    :return: TALYS command
    """
    return rf"talys < {input_file} > {output_file}"


def main():
    # generate TALYS input file
    sn = NuclearElement("sn", 145)
    input_contents = env.get_template("input.j2").render(element=sn, astro="n")
    input_fname = "input.txt"

    # write input file to job folder
    dir_name: str = hash_string(input_contents)
    p = pathlib.Path.cwd() / dir_name
    p.mkdir()
    filepath = p / input_fname
    with filepath.open("w", encoding="utf-8") as f:
        f.write(input_contents)
    logger.info("Wrote %s" % input_fname)

    # run TALYS
    command = talys_command(input_fname, "output.txt", wd=p)
    # sh(command, shell=True, cwd=p)

# todo generate energy.in from np.linspace/logspace

if __name__ == "__main__":
    logging.basicConfig(
        filename=logfile,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main()
