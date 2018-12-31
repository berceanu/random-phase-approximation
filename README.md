# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.

TODO:
- write table to output file
- create Python wrapper
- make list of available nuclei


PARAMETERS TO VARY:
- nucleus
- temperature
- angular momentum J
- parity pi


`dis.dat` : FORTRAN input
`[q]rpa.wel` : FORTRAN output
`start.dat` : C++ input
`lorvec.out` : C++ output, Lorentzian line shapes (isovector)
`excvec.out` : C++ output, discrete line shapes (isovector)


`plotter.py` : generate `lorentzian.png` from `lorvec.out`
`draft.py` : run steps below

1. `make clean`
2. `make run`
3. generate `start.dat` and `dis.dat`
4. run both ground state `Fortran` codes with `./run`
5. generate `[q]rpa.wel`
6. run both excited state `C++` codes

- `dis.dat` -> FORTRAN -> `[q]rpa.wel` + `start.dat` -> C++ -> `lorvec.out`
- for table: change `transerg` to `9.78` (or other desired energy). Output on screen
- to avoid matrix elements calculation, change `calc, xyprint` from `1` to `0` and `xyread` from `0` to `1`
