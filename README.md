# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.
See the original [paper](http://dx.doi.org/10.1016/j.physletb.2009.10.046).

TODO:
- write table to output file
- make list of available nuclei
- remove `filetest.py` and `transerg.in`
- write `generate_inputs` function -- see `draft.py`
- implement `_read_last_line` condition function; add "DONE" line to output

PARAMETERS TO VARY:
- nucleus
- temperature
- angular momentum J
- parity $\Pi$


FILES:
- `_[q]rpa.wel` : FORTRAN output
- `_start.dat` : C++ input
- `_lorvec.out` : C++ output, Lorentzian line shapes (isovector)
- `_excvec.out` : C++ output, discrete line shapes (isovector)

UTILITIES in `util`:
- `plotter.py` : generate `lorentzian.png` from `lorvec.out`
- `draft.py` : run codes
- `make.py` : convert `Makefile` to `CMakeLists.txt`
- `prefix_resub.py` : add a prefix to all filenames in a codebase

WORKFLOW:
zero temperature:
- `dish_dis.dat` -> FORTRAN (`dish`) -> `dish_qrpa.wel` + `ztes_start.dat` -> C++ (`ztes`) -> `ztes_lorvec.out`
finite temperature:
- `skys_dis.dat` -> FORTRAN (`skys`) -> `skys_rpa.wel` + `ftes_start.dat` -> C++ (`ftes`) -> `ftes_lorvec.out`

1. generate `_start.dat` and `_dis.dat`
2. run both ground state `Fortran` codes
3. run both excited state `C++` codes

- for table: change `transerg` to `9.78` (or other desired energy). Output on screen
- to avoid matrix elements calculation, change `calc, xyprint` from `1` to `0` and `xyread` from `0` to `1`

