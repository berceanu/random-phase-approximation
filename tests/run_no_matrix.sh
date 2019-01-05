#!/usr/bin/env bash

rm -rf out_no_matrix
mkdir out_no_matrix

./generate_inputs_no_matrix.py

cp full_calc_out/ztes_arpa.bin out_no_matrix/
cp full_calc_out/ztes_brpa.bin out_no_matrix/

cp full_calc_out/ftes_arpa.bin out_no_matrix/
cp full_calc_out/ftes_brpa.bin out_no_matrix/

cp full_calc_out/ztes_xrpa.bin out_no_matrix/
cp full_calc_out/ztes_yrpa.bin out_no_matrix/
cp full_calc_out/ztes_erpa.bin out_no_matrix/
cp full_calc_out/ztes_c_erpa.bin out_no_matrix/

cp full_calc_out/ftes_xrpa.bin out_no_matrix/
cp full_calc_out/ftes_yrpa.bin out_no_matrix/
cp full_calc_out/ftes_erpa.bin out_no_matrix/
cp full_calc_out/ftes_c_erpa.bin out_no_matrix/

./dish out_no_matrix/ > out_no_matrix/dish_stdout.txt 2> out_no_matrix/dish_stderr.txt
./skys out_no_matrix/ > out_no_matrix/skys_stdout.txt 2> out_no_matrix/skys_stderr.txt
./ztes out_no_matrix/ > out_no_matrix/ztes_stdout.txt 2> out_no_matrix/ztes_stderr.txt
./ftes out_no_matrix/ > out_no_matrix/ftes_stdout.txt 2> out_no_matrix/ftes_stderr.txt

./plot_lorentzian.py
