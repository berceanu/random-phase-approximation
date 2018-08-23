#!/usr/bin/env python3

import subprocess
import sys
from threading import Thread


def async_stream_process_stdout(process, log_fn):
    """ Stream the stdout and stderr for a process out to display async
    :param process: the process to stream the log for
    :param log_fn: a function that will be called for each log line
    :return: None
    """
    logging_thread = Thread(target=stream_process_stdout,
                            args=(process, log_fn, ))
    logging_thread.start()

    return logging_thread

def stream_process_stdout(process, log_fn):
    """ Stream the stdout and stderr for a process out to display
    :param process: the process to stream the logs for
    :param log_fn: a function that will be called for each log line
    :return: None
    """
    while True:
        line = process.stdout.readline().rstrip().decode('utf-8')
        if not line:
            break

        log_fn(line)

def log_fn(process):
    return lambda line: sys.stdout.write('{}: {:.2f}%\n'.format(process, float(line.split()[-1]))) if 'pa1 = ' in line else None

if __name__ == "__main__":

    # ps_one = subprocess.Popen("./run", stdout=subprocess.PIPE, bufsize=1,
    #  cwd="./zero_temperature/excited_states/")
    # ps_two = subprocess.Popen("./run", stdout=subprocess.PIPE, bufsize=1,
    #  cwd="./finite_temperature/excited_states/")

    # logger_one = async_stream_process_stdout(ps_one, log_fn('zero T'))
    # logger_two = async_stream_process_stdout(ps_two, log_fn('finite T'))

    # logger_one.join()
    # logger_two.join()


    common_gstate_block = ("l6       =   10                     ! output file\n"
                           "n0f      =   20   20                ! number of oscillator shells\n"
                           "b0       =   -1.6280835             ! oscillator parameter (fm**-1) of basis\n"
                           "maxi     =  800                     ! maximal number of iterations\n"
                           "xmix     =  0.2                     ! annealing parameter\n"
                           "NI62                                ! nucleus under consideration\n"
                          )
    
    zero_temp_gstate_block = ("Fixedgap = 00.000    00.000         ! Frozen Gapparmeter for neutr. and proton\n"
                              "GA       = 00.000    00.000         ! Pairing-Constants GG = GA/A\n"
                              "Init.Gap = 01.000    01.000         ! Initial values for the Gap parameters\n"
                              "ivpair   =   1                      ! pair. ME: 0 read, 1 calc. 2 only calc.\n"
                              "vfac     =  1.15                    ! vpair multiplication\n"
                              "blocking:   0  2  1  1              ! Blocking neutrons: y/n, j, ip, nr\n"
                              "blocking:   0  0  0  0              ! Blocking protons:  y/n, j, ip, nr\n"
                             )
    
    finite_temp_gstate_block = ("Delta    =  0.000   0.000           ! Gapparameter for neutrons and  protons\n"
                                "temp     =  2.0                     ! temperature\n"
                                "filename =  T0\n"
                               )
    

    with open('dis.dat', 'w') as f:
        f.write(common_gstate_block)
        f.write(zero_temp_gstate_block)

    with open('dis.dat', 'w') as f:
        f.write(common_gstate_block)
        f.write(finite_temp_gstate_block)