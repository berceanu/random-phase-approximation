#!/usr/bin/env bash

version="0.1"

while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -V | --version )
    echo $version
    exit
    ;;
  -h | --help )
    echo "Usage: $(basename $0) [-p PATH] [-f]"
    exit
    ;;
  -p | --path )
    shift; path=$1
    ;;
  -f | --flag )
    flag=1
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

# workdir=$(dirname)

# working dir can be passed via -p, defaults to current dir
path=${path:-$PWD}

echo "Working path: ${path}"
# echo "${flag}"

if [[ -e "file.txt" ]]; then
  echo "file exists"
fi

# f"{program} {path} > {stdout_file} 2> {stderr_file}"

# check that dish_dis.dat exists
# output dish_qrpa.wel
# write something to stdout

echo ""
echo ""
echo " ********************************************************************"
echo " *   Iteration converged after  72 steps   si =     0.0000008921    *"
echo " ********************************************************************"
echo ""



 ********************************************************************
 *   Iteration converged after  72 steps   si =     0.0000008921    *
 ********************************************************************

# POST-conditions
# dish_stderr.txt must contain "FINAL STOP"
# dish_stdout.txt must end with "Iteration converged after"