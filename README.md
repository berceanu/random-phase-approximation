# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.

TODO:
- write table to output file
- create Python wrapper
- make list of available nuclei
- progress bar for C++ codes

PARAMETERS TO VARY:
- nucleus
- temperature
- angular momentum J
- parity pi

WORKFLOW:
- compile using `make run`
- execute with `./run`
- `dis.dat` -> FORTRAN -> `[q]rpa.wel` + `start.dat` -> C++ -> `lorvec.out`: Lorentzian isovector line shapes
- for table: change `transerg` to `9.78` (or other desired energy). Output on screen.
- to avoid matrix elements calculation, change `calc, xyprint` from `1` to `0` and `xyread` from `0` to `1`.
