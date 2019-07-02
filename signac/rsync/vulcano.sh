#!/usr/bin/env bash

source=${HOME}/Development/random-phase-approximation/signac/aggregation/

rsync -rtvu --delete-delay ${source} vulcano:/home/yifei/berceanu/aggregation/
# -r recursive
# -t present file modification times
# -v verbose
# -u update, ie. don't copy files already present in destination
# --delete-delay for deleting destination files not present in source

