#!/usr/bin/env bash

rm -rf out
mkdir out

./generate_inputs.py

./dish out/ > out/dish_stdout.txt 2> out/dish_stderr.txt
./skys out/ > out/skys_stdout.txt 2> out/skys_stderr.txt
./ztes out/ > out/ztes_stdout.txt 2> out/ztes_stderr.txt
./ftes out/ > out/ftes_stdout.txt 2> out/ftes_stderr.txt

./plot_lorentzian.py
