#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple wrapper for calling TALYS code."""

import hashlib
import logging
import os
import pathlib
import subprocess
from dataclasses import dataclass

import numpy as np
from jinja2 import Environment, FileSystemLoader
from numpy.testing import assert_allclose

# pass folder containing the template
file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

logger = logging.getLogger(__name__)
logfile = "wrapper.log"


def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


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


def talys_command(
        talys_bin=pathlib.PosixPath("~/bin/talys").expanduser(),
        input_file: str = "input",
        output_file: str = "output",
) -> str:
    """Construct the TALYS command to be ran.

    :param talys_bin: absolute path to the TALYS binary
    :param input_file: input file name
    :param output_file: output file name
    :return: TALYS command
    """
    return rf"{talys_bin} < {input_file} > {output_file}"


def main():
    # generate TALYS input file
    sn = NuclearElement("sn", 145)
    input_contents = env.get_template("input.j2").render(element=sn, astro="n")
    input_fname = "input.txt"

    # generate energy input file
    v1 = np.linspace(0.001, 0.01, 10)
    v2 = np.linspace(0.015, 0.03, 4)
    v3 = np.linspace(0.04, 0.2, 17)
    v4 = np.linspace(0.22, 0.3, 5)
    v5 = np.linspace(0.35, 0.4, 2)
    v6 = np.linspace(0.5, 30.0, 296)

    my_v = np.empty(334, dtype=np.float64)
    np.concatenate((v1, v2, v3, v4, v5, v6), out=my_v)

    energy_fname = "energy.in"
    v_ref = np.loadtxt(pathlib.Path.cwd() / energy_fname)
    assert_allclose(my_v, v_ref)

    # write files to job folder
    dir_name: str = hash_string(input_contents)
    p = pathlib.Path.cwd() / dir_name
    p.mkdir(exist_ok=True)

    filepath = p / input_fname
    with filepath.open("w", encoding="utf-8") as f:
        f.write(input_contents)
    logger.info("Wrote %s" % filepath)

    filepath = p / energy_fname
    np.savetxt(filepath, my_v, fmt="%.3f", newline=os.linesep)
    logger.info("Wrote %s" % filepath)

    # run TALYS
    command = talys_command(input_file=input_fname, output_file="output.txt")
    sh(command, shell=True, cwd=p)


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfile,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main()
