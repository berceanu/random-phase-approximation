#!/usr/bin/env python3
"""This module aggregates many figures into a movie."""

import signac
import argparse
import logging
logger = logging.getLogger(__name__)

def animate(param=0.):
    pass

def main_animate(args):
    rpa = signac.get_project(root='../../')
    aggregation = signac.get_project(root='../')
    animation = signac.get_project(root='./')
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("aggregation project: %s" % aggregation.root_directory())
    logger.info("animation project: %s" % animation.root_directory())


    animate(param=args.param)

def main():
    parser = argparse.ArgumentParser(
        description="this script aggregates many figures into a movie.")
    parser.add_argument(
        '--vlines',
        action='store_true',
        help="Add vertical lines at transition energies to plots.")
    parser.add_argument(
        '--param',
        type=float,
        help="Lower energy threshold for spectrum, in MeV.")

    args = parser.parse_args() # load command line args
    main_animate(args)

if __name__ == '__main__':
    logging.basicConfig(
        filename='animation.log',
        format='%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info('==RUN STARTED==')
    main()
    logger.info('==RUN FINISHED==')