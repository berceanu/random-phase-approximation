#!/usr/bin/env bash

source=/mnt/ra5_aberceanu/rpa/workspace/
destination=/home/berceanu/Development/random-phase-approximation/signac/workspace/

rsync -rtvu --delete-delay ${source} ${destination}
# -r recursive
# -t present file modification times
# -v verbose
# -u update, ie. don't copy files already present in destination
# --delete-delay for deleting destination files not present in source

