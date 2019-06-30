#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple wrapper for calling TALYS code."""

import logging
import subprocess
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader

# pass folder containing the template
file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

logger = logging.getLogger(__name__)
logfile = "wrapper.log"


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


def ffmpeg_command(
        framerate=4.0,  # fps
        resolution="1920x1080",  # width x height
        input_files="pic%04d.png",  # pic0001.png, pic0002.png, ...
        output_file="test.mp4",
):
    return (
        rf"ffmpeg -r {framerate} -f image2 -s {resolution} -i {input_files} "
        rf"-vcodec libx264 -crf 25  -pix_fmt yuv420p -y {output_file}"
    )


def main():
    sn = NuclearElement("sn", 145)

    input_contents = env.get_template("input.j2").render(element=sn, astro="n")

    with open('input', 'w') as f:
        f.write(input_contents)

    logger.info('Wrote %s' % 'input')


if __name__ == "__main__":
    logging.basicConfig(
        filename=logfile,
        format="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main()
