"""This module contains functions for generating the parameter files."""
from collections import defaultdict
import logging
import os

CODE_NAME = { # mapping from executable names to what they represent
    'zero' : {
        'ground' : 'dish',
        'excited' : 'ztes'
    },
    'finite' : {
        'ground' : 'skys',
        'excited' : 'ftes' 
    }
}


def generate_inputs(nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78,
                    out_path=os.getcwd(), load_matrix=False):
    """Generates input files dish_dis.dat, skys_dis.dat and (z|f)tes_start.dat.

    When looking at different transition energies for the same nucleus, one can avoid re-calculating
    the matrix elements by passing load_matrix=True

    Args:
        nuleus: nucleus under consideration, eg. NI56, NI60, NI62, NI68, ZR90, SN132, PB208
        angular_momentum: 0 or 1
        parity: + or -
        temperature: eg. 2.0 (in MeV)
        transition_energy: eg. 9.78 (in MeV)
        load_matrix: flag that controls the matrix elements calculation, default is to perform the calculation

        out_path: path of folder to write files to
    
    Returns:
        Writes files to out_path (current folder by default).
    Usage:
        generate_inputs(out_path=args.workspace, load_matrix=args.load_matrix,
                    nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78)
    """

    actual_parity = {"-" : 0, "+": 1} # map to the parity as it is defined in the input file

    parameters = { # dictionary containing parameters for string substitution
        'transerg':transition_energy,
        'calc':int(not load_matrix), # do not calculate when you load the matrix
        'xyprint':int(not load_matrix),
        'xyread':int(load_matrix),
        'xyprobe':int(load_matrix),
        'j':angular_momentum,
        'parity':actual_parity[parity],
        'temp':temperature,
        'XA':nuleus
    }

    block = defaultdict(dict)

    # define blocks for FORTRAN input files
    block['zero']['ground'] = block['finite']['ground'] = ( # common gs block
        "l6       =   10                     ! output file\n"
        "n0f      =   20   20                ! number of oscillator shells\n"
        "b0       =   -1.6280835             ! oscillator parameter (fm**-1) of basis\n"
        "maxi     =  800                     ! maximal number of iterations\n"
        "xmix     =  0.2                     ! annealing parameter\n"
        "{XA}                                ! nucleus under consideration\n"
    ).format(**parameters) # substitute parameter values into string

    block['zero']['ground'] += ( # append to common gs block
        "Fixedgap = 00.000    00.000         ! Frozen Gapparmeter for neutr. and proton\n"
        "GA       = 00.000    00.000         ! Pairing-Constants GG = GA/A\n"
        "Init.Gap = 01.000    01.000         ! Initial values for the Gap parameters\n"
        "ivpair   =   1                      ! pair. ME: 0 read, 1 calc. 2 only calc.\n"
        "vfac     =  1.15                    ! vpair multiplication\n"
        "blocking:   0  2  1  1              ! Blocking neutrons: y/n, j, ip, nr\n"
        "blocking:   0  0  0  0              ! Blocking protons:  y/n, j, ip, nr\n"
    )

    block['finite']['ground'] += ( # append to common gs block
        "Delta    =  0.000   0.000           ! Gapparameter for neutrons and  protons\n"
        "temp     =  {temp}                  ! temperature\n"
        "filename =  T0__\n"
    ).format(**parameters)

    # define block for C++ input files
    block['zero']['excited'] = block['finite']['excited'] = ( # common excited state block
        "j          =   {j}                  ! resulting j of ph-pairs\n"
        "parity     =   {parity}             ! parity of ph-pairs 1:+ 0:-\n"
        "ediffmaxu  =   200.0                ! maximal excitation-energy particles\n"
        "ediffmaxd  =   2000.0               ! maximal excitation-energy a-p\n"
        "calc       =   {calc}               ! 1:calc mat and exc. 0:only exc.\n"
        "xyprint    =   {xyprint}            ! saves xy-matrices on disk 1:yes 0:no\n"
        "lorchange  =   0                    ! 1:only changing lorentz-curves\n"
        "lorswidth  =   1.0                  ! width of isoscalar lorentz-curve\n"
        "lorvwidth  =   1.0                  ! width of isovector lorentz-curve\n"
        "hlorswidth =   1.0                  ! width of isoscalar hartree-lorentz-curve\n"
        "hlorvwidth =   1.0                  ! width of isovector hartree-lorentz-curve\n"
        "hartree    =   0                    ! solution also without interact.1:yes\n"
        "matprint   =   1                    ! prints out RPA ascii-matrix yes:1no:0\n"
        "xyread     =   {xyread}             ! x- and y read in for further calc.\n"
        "xyprobe    =   {xyprobe}            ! making rpa-probe 1:yes 0:no\n"
        "exccalc    =   1                    ! only calculating exc 1:yes 0:no\n"
        "transdens  =   0                    ! calculate trans-dens1:yes0:no\n"
        "transiso   =   0                    ! isosc:0 isovec:1 for tr-dens\n"
        "transerg   =   {transerg}           ! energy for tr-dens, specify 2 digits\n"
        "tc_cur     =   0                    ! calculate transition-currents 1:yes 0:no\n"
        "tc_iso     =   1                    ! isoscalar:0 isovector:1 for tr-cur\n"
        "tc_erg     =   12.36                ! energy for tr-curr, specify 2 digits\n"
        "qptresh    =   0.01                 ! for lower occ inqp1noqp2-qp1pairs\n"
        "respair    =   1                    ! 1:pairing in residual inter. 0:no\n"
    ).format(**parameters)

    def write_params_to(fname, block_to_write):
        fpath = os.path.join(out_path, fname)
        with open(fpath, "w") as f:
            f.write(block_to_write)
        logging.info("Wrote {}.".format(fpath))
    
    for temp in ('zero', 'finite'): # create input files
        for state, suffix in zip(('ground', 'excited'), ("_dis.dat", "_start.dat")):
            write_params_to(CODE_NAME[temp][state] + suffix, block[temp][state])

    logging.info('Generated all input files.')

    return