# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.

TODO:
- write table to output file
- create Python wrapper
- make list of available nuclei
- remove `filetest.py` and `transerg.in`
- `./run` codes and compare results with `lorentzian.png`; see the original [paper](http://dx.doi.org/10.1016/j.physletb.2009.10.046)
- mock C++ and Fortran codes with minimal functionality
- prepend all filenames with `working_dir` command line parameter, defaulting to `.`
- write `generate_inputs` function -- see `draft.py`
- implement `_read_last_line` condition function; add "DONE" line to output
- add compilation optimization flags

PARAMETERS TO VARY:
- nucleus
- temperature
- angular momentum J
- parity $\Pi$


FILES:
- `dis.dat` : FORTRAN input
- `[q]rpa.wel` : FORTRAN output
- `start.dat` : C++ input
- `lorvec.out` : C++ output, Lorentzian line shapes (isovector)
- `excvec.out` : C++ output, discrete line shapes (isovector)
- `plotter.py` : generate `lorentzian.png` from `lorvec.out`
- `draft.py` : run steps below

WORKFLOW:
- `dis.dat` -> FORTRAN -> `[q]rpa.wel` + `start.dat` -> C++ -> `lorvec.out`
1. `make clean`
2. `make run`
3. generate `start.dat` and `dis.dat`
4. run both ground state `Fortran` codes with `./run`
5. generate `[q]rpa.wel`
6. run both excited state `C++` codes

- for table: change `transerg` to `9.78` (or other desired energy). Output on screen
- to avoid matrix elements calculation, change `calc, xyprint` from `1` to `0` and `xyread` from `0` to `1`
