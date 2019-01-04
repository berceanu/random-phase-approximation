#!/usr/bin/env python3

import os


if __name__ == "__main__":

    # define blocks for FORTRAN input files
    common_gstate_block = (
        "l6       =   10                     ! output file\n"
        "n0f      =   20   20                ! number of oscillator shells\n"
        "b0       =   -1.6280835             ! oscillator parameter (fm**-1) of basis\n"
        "maxi     =  800                     ! maximal number of iterations\n"
        "xmix     =  0.2                     ! annealing parameter\n"
        "NI62                                ! nucleus under consideration\n"
    )
    zero_temp_gstate_block = (
        "Fixedgap = 00.000    00.000         ! Frozen Gapparmeter for neutr. and proton\n"
        "GA       = 00.000    00.000         ! Pairing-Constants GG = GA/A\n"
        "Init.Gap = 01.000    01.000         ! Initial values for the Gap parameters\n"
        "ivpair   =   1                      ! pair. ME: 0 read, 1 calc. 2 only calc.\n"
        "vfac     =  1.15                    ! vpair multiplication\n"
        "blocking:   0  2  1  1              ! Blocking neutrons: y/n, j, ip, nr\n"
        "blocking:   0  0  0  0              ! Blocking protons:  y/n, j, ip, nr\n"
    )
    finite_temp_gstate_block = (
        "Delta    =  0.000   0.000           ! Gapparameter for neutrons and  protons\n"
        "temp     =  2.0                     ! temperature\n"
        "filename =  T0\n"
    )
    common_estate_block = (
        "j          =   1                    ! resulting j of ph-pairs\n"
        "parity     =   0                    ! parity of ph-pairs 1:+ 0:-\n"
        "ediffmaxu  =   200.0                ! maximal excitation-energy particles\n"
        "ediffmaxd  =   2000.0               ! maximal excitation-energy a-p\n"
        "calc       =   1                    ! 1:calc mat and exc. 0:only exc.\n"
        "xyprint    =   1                    ! saves xy-matrices on disk 1:yes 0:no\n"
        "lorchange  =   0                    ! 1:only changing lorentz-curves\n"
        "lorswidth  =   1.0                  ! width of isoscalar lorentz-curve\n"
        "lorvwidth  =   1.0                  ! width of isovector lorentz-curve\n"
        "hlorswidth =   1.0                  ! width of isoscalar hartree-lorentz-curve\n"
        "hlorvwidth =   1.0                  ! width of isovector hartree-lorentz-curve\n"
        "hartree    =   0                    ! solution also without interact.1:yes\n"
        "matprint   =   1                    ! prints out RPA ascii-matrix yes:1no:0\n"
        "xyread     =   0                    ! x- and y read in for further calc.\n"
        "xyprobe    =   0                    ! making rpa-probe 1:yes 0:no\n"
        "exccalc    =   1                    ! only calculating exc 1:yes 0:no\n"
        "transdens  =   0                    ! calculate trans-dens1:yes0:no\n"
        "transiso   =   0                    ! isosc:0 isovec:1 for tr-dens\n"
        "transerg   =   9.78                 ! energy for tr-dens, specify 2 digits\n"
        "tc_cur     =   0                    ! calculate transition-currents 1:yes 0:no\n"
        "tc_iso     =   1                    ! isoscalar:0 isovector:1 for tr-cur\n"
        "tc_erg     =   12.36                ! energy for tr-curr, specify 2 digits\n"
        "qptresh    =   0.01                 ! for lower occ inqp1noqp2-qp1pairs\n"
        "respair    =   1                    ! 1:pairing in residual inter. 0:no\n"
    )

    # create C++ input files
    with open(os.path.join('out', "ztes_start.dat"), "w") as f:
        f.write(common_estate_block)
    #
    with open(os.path.join('out', "ftes_start.dat"), "w") as f:
        f.write(common_estate_block)

    # create FORTRAN input files
    with open(os.path.join('out', "dish_dis.dat"), "w") as f:
        f.write(common_gstate_block)
        f.write(zero_temp_gstate_block)
    #
    with open(os.path.join('out', "skys_dis.dat"), "w") as f:
        f.write(common_gstate_block)
        f.write(finite_temp_gstate_block)