#!/usr/bin/env bash

source=/home/berceanu/Development/random-phase-approximation/signac/workspace/
destination=/media/FLAPS/ra5_aberceanu/rpa/workspace/

rsync -rtvu --delete-delay ${source} ${destination}
# -r recursive
# -t present file modification times
# -v verbose
# -u update, ie. don't copy files already present in destination
# --delete-delay for deleting destination files not present in source
