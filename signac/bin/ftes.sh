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

CALC=`grep "^calc" ftes_start.dat | awk '{print $3}'`

BinFiles=('ftes_arpa.bin' 'ftes_brpa.bin' 'ftes_xrpa.bin' 'ftes_yrpa.bin' 'ftes_erpa.bin' 'ftes_c_erpa.bin')


if [[ $CALC -eq 1 ]]; then
  echo "Doing the full calculation."
  # generate all the .bin files
  for i in "${BinFiles[@]}"; do
    echo -n $'\x01' > $i
  done
elif [[ $CALC -eq 0 ]]; then
  echo "Loading pre-computed matrix."
  # check that the .bin files are present
  for i in "${BinFiles[@]}"; do
    if [[ ! -f $i ]]; then
      echo "${i} not found!"
      exit 1
    fi
  done
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