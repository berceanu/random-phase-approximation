#!/usr/bin/env bash

# Usage: dish.sh [PATH]
path=$1

# working dir can be passed, defaults to current dir
path=${path:-$PWD}

cd "${path}"
echo "$0 working path: $PWD"


# check that dish_dis.dat exists
if [[ ! -f "dish_dis.dat" ]]; then
  echo "dish_dis.dat not found!"
  exit 1
fi

# simulate intense computation
sleep 5s

# write to stdout
echo
echo " ********************************************************************"
echo " *   Iteration converged after  72 steps   si =     0.0000008921    *"
echo " ********************************************************************"
echo

# write dish_qrpa.wel
outfile="dish_qrpa.wel"
touch $outfile
echo "  0.633747321351E-10  0.524831938961E-10  0.434303050245E-10  0.359115635970E-10" >> $outfile
echo "  0.296718666476E-10  0.244976736384E-10  0.202103830482E-10  0.166607392860E-10" >> $outfile
echo "  0.137241138642E-10  0.112965277146E-10  0.929130121495E-11  0.763623536321E-11" >> $outfile
echo "  0.627124197615E-11" >> $outfile
echo >> $outfile


# write to stderr
>&2 echo "STOP  FINAL STOP"
>&2 echo

# ./dish.sh out/ > dish_stdout.txt 2> dish_stderr.txt

# PRE-condition
# dish_dis.dat exists and nonempty

# POST-conditions
# dish_stderr.txt must end with "FINAL STOP"
# dish_stdout.txt must end with "Iteration converged after"
# dish_qrpa.wel must exist and not be empty

# Note: don't need to run in case of --load-matrix