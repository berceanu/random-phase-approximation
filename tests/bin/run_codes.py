#!/usr/bin/env python3

import os
import sys
import sh


name_of_code = { # mapping from executable names to what they represent
    'zero_temp_ground_state':'dish',
    'finite_temp_ground_state':'skys',
    'zero_temp_excited_state':'ztes',
    'finite_temp_excited_state':'ftes'
}



def generate_inputs(nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78,
                    out_path='.',
                    compute_matrix=True):
    """Generates input files dish_dis.dat, skys_dis.dat and (z|f)tes_start.dat.

    When looking at different transition energies for the same nucleus, one can avoid re-calculating
    the matrix elements by passing compute_matrix=False

    Args:
        nuleus: nucleus under consideration, eg. NI56, NI60, NI62, NI68, ZR90, SN132, PB208
        angular_momentum: 0 or 1
        parity: + or -
        temperature: eg. 2.0 (in MeV)
        transition_energy: eg. 9.78 (in MeV)
        compute_matrix: flag that controls the matrix elements calculation, default is to perform the calculation

        out_path: path of folder to write files to
    
    Returns:
        Writes files to out_path (current folder by default).
    """

    actual_parity = {"-" : 0, "+": 1} # map to the parity as it is defined in the input file

    parameters = { # dictionary containing parameters for string substitution
        'transerg':transition_energy,
        'calc':int(compute_matrix),
        'xyprint':int(compute_matrix),
        'xyread':int(not compute_matrix), # this is 0 when compute_matrix is True
        'xyprobe':int(not compute_matrix),
        'j':angular_momentum,
        'parity':actual_parity[parity],
        'temp':temperature,
        'XA':nuleus
    }

    # define blocks for FORTRAN input files
    common_gstate_block = (
        "l6       =   10                     ! output file\n"
        "n0f      =   20   20                ! number of oscillator shells\n"
        "b0       =   -1.6280835             ! oscillator parameter (fm**-1) of basis\n"
        "maxi     =  800                     ! maximal number of iterations\n"
        "xmix     =  0.2                     ! annealing parameter\n"
        "{XA}                                ! nucleus under consideration\n"
    ).format(**parameters) # substitute parameter values into string

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
        "temp     =  {temp}                  ! temperature\n"
        "filename =  T0__\n"
    ).format(**parameters)

    # define block for C++ input files
    common_estate_block = (
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

    def write_params_to(fname_prefix, fname_postfix, blocks_to_write):
        fname = fname_prefix + fname_postfix
        fpath = os.path.join(out_path, fname)
        with open(fpath, "w") as f:
            for block in blocks_to_write:
                f.write(block)
        print("Wrote {}.".format(fpath))
        
    # create C++ input files
    for codename in (name_of_code['zero_temp_excited_state'],\
                     name_of_code['finite_temp_excited_state']):
        write_params_to(codename, "_start.dat", [common_estate_block])
                    
    # create FORTRAN input files
    fort_postfix = '_dis.dat'
    write_params_to(name_of_code['zero_temp_ground_state'], fort_postfix,
                   [common_gstate_block, zero_temp_gstate_block])
    #
    write_params_to(name_of_code['finite_temp_ground_state'], fort_postfix,
                   [common_gstate_block, finite_temp_gstate_block])

    print('Generated all input files.')

    return



def run_executable_names(exenames=['dish','skys','ztes','ftes'], out_path='.', exepath='../bin',
                         compute_matrix=True):
    """Run the executable_names in the list, according to pattern.

    {binary} {path} > {path}/{binary_stdout.txt} 2> {path}/{binary_stderr.txt}
    """

    run = {exefile : sh.Command(os.path.join(exepath, exefile)) for exefile in exenames}

    for f in exenames:
        stdout_file = os.path.join(out_path,f+"_stdout.txt")
        stderr_file = os.path.join(out_path,f+"_stderr.txt")

        run[f](out_path, _out=stdout_file, _err=stderr_file)
        print("Finished running {}.".format(f))
    
    print('Finished all executables.')
    
    return


def plot_lorvec():
    pass



if __name__ == "__main__":
    """Generates the inputs based on the command line arguments."""

    script_name = sys.argv[0]

    # did we get 2 command line args?
    if len(sys.argv) - 1 != 2:
        sys.exit("""Usage:
    {} read_matrix/ --no-matrix
    {} calc_matrix/ --with-matrix""".format(script_name, script_name))

    # parse second command line arg
    try:
        matrix_flag = sys.argv[2] # --no-matrix if we want to avoid matrix calculation
    except IndexError:
        sys.exit("Didn't provide --with-matrix or --no-matrix argument, exiting.")
    else:
        if matrix_flag == "--no-matrix":
            compute_matrix = False
        elif matrix_flag == "--with-matrix":
            compute_matrix = True
        else:
            sys.exit("Invalid command line argument {}, exiting.".format(matrix_flag))

    # parse first command line arg
    try:
        out_path = sys.argv[1] # get output folder from command line, eg. out/
    except IndexError:
        sys.exit('Need to provide output folder, exiting.')
    else:
        try:
            os.makedirs(out_path)
        except OSError:
            if os.path.exists(out_path):
                sys.exit("Folder {} already exists, exiting.".format(out_path))
            else:
                sys.exit("Error creating {} folder. Check permissions. Exiting.".format(out_path))


    # get executable names for passing to functions
    executable_names = list(name_of_code.values())

    # generate input files for FORTRAN and C++ codes
    generate_inputs(out_path=out_path, compute_matrix=compute_matrix,
                    nuleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78)


    # run the FORTRAN and C++ codes
    run_executable_names(out_path=out_path, compute_matrix=compute_matrix,
                         exenames=executable_names, exepath='../bin')

    # post-process the output of the FORTRAN and C++ codes                        
    plot_lorvec()

    #TODO: add plotting function, copy files as in run_no_matrix.sh, based on --no-matrix flag








