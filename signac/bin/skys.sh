#!/usr/bin/env bash

# Usage: skys.sh [PATH]
path=$1

# working dir can be passed, defaults to current dir
path=${path:-$PWD}

cd "${path}"
echo "$0 working path: $PWD"


# check that skys_dis.dat exists
if [[ ! -f "skys_dis.dat" ]]; then
  echo "skys_dis.dat not found!"
  exit 1
fi

# simulate intense computation
sleep 5s

# write to stdout
echo
echo " ********************************************************************"
echo " *   Iteration converged after  53 steps   si =     0.0000006099    *"
echo " ********************************************************************"
echo " entropy:      20.512015544254822     "
echo

# write skys_rpa.wel
outfile="skys_rpa.wel"
touch $outfile
echo "  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00" >> $outfile
echo "  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00" >> $outfile
echo "  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00  0.000000000000E+00" >> $outfile
echo "  0.000000000000E+00" >> $outfile
echo >> $outfile


# write to stderr
>&2 echo "Note: The following floating-point exceptions are signalling: IEEE_DENORMAL"
>&2 echo "STOP  FINAL STOP"
>&2 echo


# ./skys.sh out/ > skys_stdout.txt 2> skys_stderr.txt

# PRE-condition
# skys_dis.dat exists and nonempty

# POST-conditions
# skys_stderr.txt must end with "FINAL STOP"
# skys_stdout.txt must end with "Iteration converged after"
# skys_rpa.wel must exist and not be empty

# Note: don't need to run in case of --load-matrix