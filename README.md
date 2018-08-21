# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.

TODO:
- make list of available nuclei

PARAMETERS TO VARY:
- nucleus
- temperature
- angular momentum J
- parity pi

WORKFLOW:
- compile using `make run`
- execute with `./run`
- `dis.dat` -> FORTRAN -> `[q]rpa.wel` + `start.dat` -> C++ -> `lorvec.out`: Lorentzian isovector line shapes
- for table: change `transerg` to `9.78` and `calc, xyprint` from `1` to `0`. Finaly, change `xyread` from `0` to `1` to avoid matrix elements calculation. Output on screen.
