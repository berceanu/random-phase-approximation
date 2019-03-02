#!/usr/bin/env python3
"""This module aggregates many figures into a movie."""

from flow import FlowProject, cmd
import signac
import subprocess
import argparse
import logging
logger = logging.getLogger(__name__)

logfile = 'animation.log'

def sh(*cmd, **kwargs):
    logger.info(cmd[0])
    stdout = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            **kwargs).communicate()[0].decode('utf-8')
    return stdout


# http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/
def ffmpeg_command(
    framerate=15, # fps
    resolution=r'1920x1080',
    input_files=r'pic%04d.png', # pic0001.png, pic0002.png, ...
    output_file=r'test.mp4',
    ):
    return rf"ffmpeg -r {framerate} -f image2 -s {resolution} -i {input_files} -vcodec libx264 -crf 25  -pix_fmt yuv420p {output_file}"


def main_animate(args):
    rpa = signac.get_project(root='../../')
    aggregation = signac.get_project(root='../')
    animation = signac.get_project(root='./')
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("aggregation project: %s" % aggregation.root_directory())
    logger.info("animation project: %s" % animation.root_directory())

    command = ffmpeg_command(framerate=args.framerate)


    with animation.open_job({}): # .init() implicitly called
        # copy all the .png files from `aggregation` project, appending sorted numerics index
        # call ffmpeg in job folder
        sh(command, shell=True)


def main():
    parser = argparse.ArgumentParser(
        description="this script aggregates many figures into a movie.")
    parser.add_argument(
        '--vlines',
        action='store_true',
        help="Add vertical lines at transition energies to plots.")
    parser.add_argument(
        '--framerate',
        type=int,
        default=15,
        help="Desired video framerate, in fps.")

    args = parser.parse_args() # load command line args
    main_animate(args)

if __name__ == '__main__':
    logging.basicConfig(
        filename=logfile,
        format='%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info('==RUN STARTED==')
    main()
    logger.info('==RUN FINISHED==')




