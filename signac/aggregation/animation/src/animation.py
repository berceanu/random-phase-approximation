#!/usr/bin/env python3
"""This module aggregates many figures into a movie."""

from flow import FlowProject, cmd
import signac
import subprocess
import argparse
import shutil
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
    framerate=4., # fps
    resolution='1920x1080', # width x height
    input_files='pic%04d.png', # pic0001.png, pic0002.png, ...
    output_file='test.mp4',
    ):
    return (rf"ffmpeg -r {framerate} -f image2 -s {resolution} -i {input_files} "
                   rf"-vcodec libx264 -crf 25  -pix_fmt yuv420p -y {output_file} &>> {logfile}")


def main_animate(args):
    rpa = signac.get_project(root='../../')
    aggregation = signac.get_project(root='../')
    animation = signac.get_project(root='./')
    logger.info("rpa project: %s" % rpa.root_directory())
    logger.info("aggregation project: %s" % aggregation.root_directory())
    logger.info("animation project: %s" % animation.root_directory())

    pngfname = 'iso_all_temp_all.png'
    pngstem, _ = pngfname.split('.')

    input_files = pngstem + '_%04d.png'

    command = ffmpeg_command(framerate=args.framerate,
                             resolution=args.resolution,
                             input_files=input_files,
                             output_file=pngstem + ".mp4"
                             )

    # rpa_schema = rpa.detect_schema()
    # print(rpa_schema)

    with animation.open_job({}) as anim_job: # .init() implicitly called

        neutrons = []
        origin={}
        for counter, agg_job in enumerate(sorted(aggregation.find_jobs(
            {'proton_number': args.protonNumber, 'neutron_number': {'$gte': args.minNeutronNumber}}),
                key=lambda job: job.sp['neutron_number']),
                    1): # start counting from 1
            logger.info('(Z, N) = ({}, {}); id = {}; file = iso_all_temp_all_{:04d}.png'.format(
                agg_job.sp['proton_number'], agg_job.sp['neutron_number'],
                agg_job._id, counter)
                )

            neutrons.append(agg_job.sp['neutron_number'])
            origin[f"N = {agg_job.sp['neutron_number']}"] = str(agg_job)

            png_counted = input_files % counter

            # copy all the .png files from `aggregation` project,
            #  appending sorted numerics index
            shutil.copy(agg_job.fn(pngfname), anim_job.fn(png_counted))

        # call ffmpeg in job folder
        sh(command, shell=True)

        anim_job.sp['proton_number'] = args.protonNumber
        anim_job.sp['neutron_number'] = neutrons
        anim_job.doc.update(origin)



def main():
    parser = argparse.ArgumentParser(
        description="this script aggregates many figures into a movie.")
    parser.add_argument(
        '--protonNumber',
        type=int,
        default=50, # Tin (Sn)
        help="Proton number Z.")
    parser.add_argument(
        '--minNeutronNumber',
        type=int,
        default=76,
        help="Minimum neutron number N for isotopes.")        
    parser.add_argument(
        '--framerate',
        type=float,
        default=4.,
        help="Desired video framerate, in fps.")
    parser.add_argument(
        '--resolution',
        type=str,
        default='1920x1080',
        help="Desired video resolution, width x height, in pixels.")

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




