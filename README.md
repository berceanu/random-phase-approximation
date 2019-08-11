# rpa

RPA for zero and finite temperature, both FORTRAN (ground state) and C++ (excited states) codes.
See the original [paper](http://dx.doi.org/10.1016/j.physletb.2009.10.046).

DEPENDENCIES:

- `cmake` >= 3.10.2
- `build-essential` on Ubuntu
- `gfortran` >= 7.3.0
- `$ conda env create -f environment.yml`

PARAMETERS TO VARY:

- nucleus under consideration: `NI56`, `NI60`, `NI62`, `NI68`, `ZR90`, `SN132`, `PB208`
	- note the various isotopes of Ni
- angular momentum of particle-hole pairs `j` : `1` or `0`
- `parity` of particle-hole pairs: + or - (`1` or `0`)
- temperature `temp` : `1.0` or `2.0` (in MeV)
- transition energy for calculating transition amplitudes `transerg` : `9.78`, `10.03` etc (in MeV)
	- we must avoid the whole matrix elements calculation when looking at different transition energies

FILES:

- `_[q]rpa.wel` : FORTRAN output
- `_start.dat` : C++ input
- `_lorvec.out` : C++ output, Lorentzian line shapes (isovector)
- `_excvec.out` : C++ output, discrete line shapes (isovector)

UTILITIES in `util`:

- `plotter.py` : generate `lorentzian.png` from `lorvec.out`
- `draft.py` : run codes
- `parse_makefile.py` : convert `Makefile` to `CMakeLists.txt`
- `prefix_resub.py` : add a prefix to all filenames in a codebase

WORKFLOW:

- `dish_dis.dat` -> FORTRAN (`dish`) -> `dish_qrpa.wel` + `ztes_start.dat` -> C++ (`ztes`) -> `ztes_lorvec.out` zero temperature
- `skys_dis.dat` -> FORTRAN (`skys`) -> `skys_rpa.wel` + `ftes_start.dat` -> C++ (`ftes`) -> `ftes_lorvec.out` finite temperature

1. generate `_start.dat` and `_dis.dat`
2. run both ground state `Fortran` codes
3. run both excited state `C++` codes

- for table: change `transerg` to `9.78` (or other desired energy). Output on screen
- to avoid matrix elements calculation, change `calc, xyprint` from `1` to `0`, `xyread`, `xyprobe` from `0` to `1`
    - doing this will require the files : `(z|f)tes_arpa.bin`,
      `(z|f)tes_brpa.bin`, `(z|f)tes_xrpa.bin`, `(z|f)tes_yrpa.bin`,
      `(z|f)tes_erpa.bin`, `(z|f)tes_c_erpa.bin` so the code has to be run before to generate these files
    - note: _not_ changing `xyprobe` makes the code produce different results

ACRONYMS:

- _HFB_ : Hartree–Fock Bogoliubov
- _RMF_ : Relativistic Mean-Field
- _FTRRPA_ : self-consistent Finite-Temperature Relativistic Random Phase Approximation
- _QRPA_ : Quasiparticle Random Phase Approximation
- _RQRPA_ : Relativistic Quasiparticle Random Phase Approximation, `excited_states`
- _SKYS_ : Relativistic mean field theory in a spherical basis, `finite_temperature/ground_state`
- _DISH_ : _DISHFB_, Relativistic mean field theory with HFB in a spherical basis, `zero_temperature/ground_state`
