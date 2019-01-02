Relativistic mean field theory in a spherical basis. Finite temperature ground state calculation.

`dis.f` : main program file
`paramet` : input file

Note: The string "STOP  FINAL STOP" is written to `stderr` upon termination of the program.

Changelog:
- replaced `character*40 filename` with `character*4 filename` and `filename(1:4)` with `filename`
- replaced `file=` with `file='skys_' // `
- input file is now called `skys_dis.dat`
- default value for `filename` is `T0__` in `skys_dis.dat`
- added option to take working directory from command line
