#!/usr/bin/env bash

#cd ${HOME}/openVPN/
#./openvpn.sh
#cd -
source=/media/FLAPS/ra5_aberceanu/rpa/workspace/
destination=${HOME}/Development/random-phase-approximation/signac/workspace/

rsync -rtvu --delete-delay P6000:${source} ${destination}
# -r recursive
# -t present file modification times
# -v verbose
# -u update, ie. don't copy files already present in destination
# -z activate compression
# --delete-delay for deleting destination files not present in source
