#!/usr/bin/env bash

# Usage: ztes.sh [PATH]
path=$1

# working dir can be passed, defaults to current dir
path=${path:-$PWD}

cd "${path}"
echo "$0 working path: $PWD"


# check that ztes_start.dat exists
if [[ ! -f "ztes_start.dat" ]]; then
  echo "ztes_start.dat not found!"
  exit 1
fi

# check that dish_qrpa.wel exists
if [[ ! -f "dish_qrpa.wel" ]]; then
  echo "dish_qrpa.wel not found!"
  exit 1
fi

# simulate intense computation
sleep 5s

# write ztes_lorvec.out
outfile="ztes_lorvec.out"
touch $outfile
echo "4.998000e+01	8.508468e-03" >> $outfile
echo "4.999000e+01	8.464015e-03" >> $outfile
echo "5.000000e+01	8.418575e-03" >> $outfile
echo >> $outfile

# write to stdout
echo "calculation of strengths finished"
echo "program terminated without errors"
echo


# ./ztes.sh out/ > ztes_stdout.txt 2> ztes_stderr.txt

# PRE-condition
# ztes_start.dat exists and nonempty
# dish_qrpa.wel exists and nonempty

# POST-conditions
# ztes_stderr.txt must be empty
# ztes_stdout.txt must end with "program terminated without errors"
# ztes_lorvec.out must exist and not be empty

# Note: need to run also in case of --load-matrix