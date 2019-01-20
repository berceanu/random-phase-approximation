#!/usr/bin/env bash

# Usage: ftes.sh [PATH]
path=$1

# working dir can be passed, defaults to current dir
path=${path:-$PWD}

cd "${path}"
echo "$0 working path: $PWD"


# check that ftes_start.dat exists
if [[ ! -f "ftes_start.dat" ]]; then
  echo "ftes_start.dat not found!"
  exit 1
fi

# check that skys_rpa.wel exists
if [[ ! -f "skys_rpa.wel" ]]; then
  echo "skys_rpa.wel not found!"
  exit 1
fi

# simulate intense computation
sleep 5s

# write ftes_lorvec.out
outfile="ftes_lorvec.out"
touch $outfile
echo "4.998000e+01	5.058397e-03" >> $outfile
echo "4.999000e+01	5.039383e-03" >> $outfile
echo "5.000000e+01	5.020894e-03" >> $outfile
echo >> $outfile

# write to stdout
echo "program terminated without errors"
echo


# ./ftes.sh out/ > ftes_stdout.txt 2> ftes_stderr.txt

# PRE-condition
# ftes_start.dat exists and nonempty
# skys_rpa.wel exists and nonempty

# POST-conditions
# ftes_stderr.txt must be empty
# ftes_stdout.txt must end with "program terminated without errors"
# ftes_lorvec.out must exist and not be empty

# Note: need to run also in case of --load-matrix